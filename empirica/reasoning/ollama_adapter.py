"""
Ollama Adapter for Reasoning Service

Connects to Ollama-hosted models for doc-code intelligence reasoning.
Optimized for qwen2.5:32b on empirica-server.
"""

import requests
import json
import logging
from typing import Dict, Optional
from .service import ReasoningService
from .types import DeprecationJudgment, RelationshipAnalysis, ImplementationGap

logger = logging.getLogger(__name__)


class OllamaReasoningModel(ReasoningService):
    """Adapter for Ollama-hosted reasoning models"""
    
    def __init__(
        self,
        model_name: str = "qwen2.5:32b",
        endpoint: str = "http://empirica-server:11434",
        timeout: int = 60
    ):
        self.model_name = model_name
        self.endpoint = endpoint
        self.timeout = timeout
        
    def _call_ollama(
        self,
        prompt: str,
        format: str = "json",
        temperature: float = 0.1,
        max_tokens: int = 2048
    ) -> Dict:
        """
        Low-level Ollama API call
        
        Args:
            prompt: Prompt text
            format: Response format ("json" or None)
            temperature: Sampling temperature (lower = more consistent)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dict with 'response' key containing model output
            
        Raises:
            Exception on connection/timeout errors
        """
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": format,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.9,
                        "num_predict": max_tokens
                    }
                },
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout calling {self.model_name} after {self.timeout}s")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection failed to {self.endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            raise
    
    def _build_deprecation_prompt(self, feature: str, context: Dict) -> str:
        """Build prompt for deprecation analysis"""
        
        doc_mentions = context.get('doc_mentions', [])
        doc_text = "\n".join([f"- {m['context']}" for m in doc_mentions[:3]])
        
        code_exists = context.get('code_exists', False)
        usage_count = context.get('usage_count', 0)
        last_commit = context.get('last_commit', 'unknown')
        
        prompt = f"""You are analyzing whether a software feature is genuinely deprecated.

Feature: {feature}

Documentation mentions:
{doc_text}

Code status: {'Implemented' if code_exists else 'Not found'}
Usage in last 50 sessions: {usage_count} times
Last git commit: {last_commit}

Task: Determine if this feature is:
1. "deprecated" - Currently deprecated, should be removed/marked
2. "historical" - Previously deprecated but now current (historical context only)
3. "active" - Still active and in use

Reasoning guidelines:
- "previously deprecated" = past tense, not current deprecation
- Check if code is actively maintained (recent commits = active)
- Check if usage patterns show active use (many uses = active)
- Consider relationships to other features

Respond in JSON format only, no additional text:
{{
    "status": "deprecated|historical|active",
    "confidence": 0.0-1.0,
    "reasoning": "brief step-by-step analysis",
    "evidence": ["key evidence points"],
    "recommendation": "specific action to take"
}}"""
        
        return prompt
    
    def _parse_deprecation_response(self, response: Dict) -> DeprecationJudgment:
        """Parse Ollama response into DeprecationJudgment"""
        
        try:
            # Extract response text
            response_text = response.get('response', '')
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ['status', 'confidence', 'reasoning', 'evidence', 'recommendation']
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing field in response: {field}")
                    data[field] = "unknown" if field == 'status' else ([] if field == 'evidence' else "")
            
            # Validate status
            valid_statuses = ['deprecated', 'historical', 'active']
            if data['status'] not in valid_statuses:
                logger.warning(f"Invalid status: {data['status']}, defaulting to 'active'")
                data['status'] = 'active'
            
            # Ensure confidence is float
            try:
                confidence = float(data['confidence'])
                confidence = max(0.0, min(1.0, confidence))  # Clamp to 0-1
            except (ValueError, TypeError):
                logger.warning(f"Invalid confidence: {data['confidence']}, defaulting to 0.5")
                confidence = 0.5
            
            return DeprecationJudgment(
                feature="",  # Will be set by caller
                status=data['status'],
                confidence=confidence,
                reasoning=data.get('reasoning', ''),
                evidence=data.get('evidence', []),
                recommendation=data.get('recommendation', ''),
                metadata={'raw_response': response_text}
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.error(f"Response was: {response.get('response', '')[:500]}")
            
            # Return fallback judgment
            return DeprecationJudgment(
                feature="",
                status="active",  # Conservative default
                confidence=0.0,
                reasoning="Failed to parse model response",
                evidence=["JSON parsing error"],
                recommendation="Manual review required",
                metadata={'error': str(e), 'raw_response': response.get('response', '')[:500]}
            )
    
    def analyze_deprecation(
        self,
        feature: str,
        context: Dict
    ) -> DeprecationJudgment:
        """
        Analyze if feature is deprecated using AI reasoning
        
        Args:
            feature: Feature name (command, function, etc.)
            context: Dict with evidence:
                - doc_mentions: List of doc locations mentioning feature
                - code_exists: Bool
                - usage_count: Int (from artifacts)
                - last_commit: Date string
                - related_features: List
                
        Returns:
            DeprecationJudgment with status and reasoning
        """
        logger.info(f"Analyzing deprecation for: {feature}")
        
        try:
            # Build prompt
            prompt = self._build_deprecation_prompt(feature, context)
            
            # Call model
            response = self._call_ollama(prompt, format="json", temperature=0.1)
            
            # Parse response
            judgment = self._parse_deprecation_response(response)
            judgment.feature = feature
            
            logger.info(f"Analysis complete: {feature} -> {judgment.status} (confidence: {judgment.confidence:.2f})")
            
            return judgment
            
        except Exception as e:
            logger.error(f"Error analyzing {feature}: {e}")
            
            # Return fallback judgment
            return DeprecationJudgment(
                feature=feature,
                status="active",  # Conservative default
                confidence=0.0,
                reasoning=f"Analysis failed: {str(e)}",
                evidence=["Error during analysis"],
                recommendation="Manual review required",
                metadata={'error': str(e)}
            )
    
    def analyze_relationship(
        self,
        doc_section: str,
        code_section: str
    ) -> RelationshipAnalysis:
        """Analyze if doc and code describe the same thing"""
        # TODO: Implement in Phase 2
        raise NotImplementedError("Relationship analysis coming in Phase 2")
    
    def analyze_implementation_gap(
        self,
        documented_behavior: str,
        actual_implementation: str
    ) -> ImplementationGap:
        """Analyze if implementation matches documented behavior"""
        # TODO: Implement in Phase 3
        raise NotImplementedError("Implementation gap analysis coming in Phase 3")
