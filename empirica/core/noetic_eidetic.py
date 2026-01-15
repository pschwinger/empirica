"""
Noetic Eidetic Memory - Conceptual reasoning extraction from CASCADE phases.

Episodic memory captures WHAT happened (narratives, timelines).
Eidetic memory captures FACTS with confidence.

This module extracts NOETIC CONCEPTS - the WHY/WHICH/FOR WHOM reasoning
that explains the epistemic journey, not just records it.

Noetic concepts are stored as eidetic facts because they represent
stable conceptual knowledge derived from reasoning, not temporal narratives.
"""

import logging
import re
import uuid
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# Fact types for noetic concepts
NOETIC_FACT_TYPES = {
    "task_understanding": "PREFLIGHT: Why this task matters, constraints, stakeholders",
    "decision_rationale": "CHECK: Why proceed/investigate, approach selection reasoning",
    "learning_insight": "POSTFLIGHT: Patterns discovered, generalizable knowledge",
    "epistemic_principle": "Cross-session: Recurring principles about learning/knowing",
}


def extract_noetic_concepts(
    reasoning: str,
    phase: str,
    task_context: Optional[str] = None,
    vectors: Optional[Dict[str, float]] = None,
) -> List[Dict]:
    """
    Extract noetic concepts (why/which/for whom) from CASCADE phase reasoning.

    Args:
        reasoning: The reasoning text from PREFLIGHT/CHECK/POSTFLIGHT
        phase: CASCADE phase (PREFLIGHT, CHECK, POSTFLIGHT)
        task_context: Optional task description for richer extraction
        vectors: Optional epistemic vectors for confidence weighting

    Returns:
        List of noetic concepts ready for eidetic embedding
    """
    if not reasoning:
        return []

    concepts = []

    # Phase-specific extraction
    if phase == "PREFLIGHT":
        concepts.extend(_extract_preflight_concepts(reasoning, task_context, vectors))
    elif phase == "CHECK":
        concepts.extend(_extract_check_concepts(reasoning, vectors))
    elif phase == "POSTFLIGHT":
        concepts.extend(_extract_postflight_concepts(reasoning, task_context, vectors))

    return concepts


def _extract_preflight_concepts(
    reasoning: str,
    task_context: Optional[str],
    vectors: Optional[Dict[str, float]],
) -> List[Dict]:
    """Extract task understanding concepts from PREFLIGHT reasoning."""
    concepts = []

    # Base confidence from vectors (higher know = more confident understanding)
    base_confidence = 0.6
    if vectors and "know" in vectors:
        base_confidence = min(0.9, 0.5 + vectors["know"] * 0.4)

    # Look for "because", "since", "due to" patterns (WHY)
    why_patterns = [
        r"because\s+(.{20,150}?)(?:\.|$|,\s*(?:and|but|so))",
        r"since\s+(.{20,150}?)(?:\.|$|,\s*(?:and|but|so))",
        r"due to\s+(.{20,100}?)(?:\.|$)",
        r"the reason\s+(?:is|being)?\s*(.{20,150}?)(?:\.|$)",
    ]

    for pattern in why_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:2]:  # Limit to 2 per pattern
            content = f"Task understanding: {match.strip()}"
            concepts.append({
                "fact_type": "task_understanding",
                "content": content,
                "confidence": base_confidence,
                "tags": ["noetic", "preflight", "why"],
            })

    # Look for constraint/requirement mentions (WHICH)
    constraint_patterns = [
        r"(?:must|need to|required to|should)\s+(.{15,100}?)(?:\.|$)",
        r"constraint[s]?:?\s*(.{15,100}?)(?:\.|$)",
    ]

    for pattern in constraint_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:2]:
            content = f"Constraint: {match.strip()}"
            concepts.append({
                "fact_type": "task_understanding",
                "content": content,
                "confidence": base_confidence * 0.9,
                "tags": ["noetic", "preflight", "constraint"],
            })

    # If task_context provided, extract domain/purpose
    if task_context:
        # Simple heuristic: first clause often states purpose
        purpose_match = re.match(r"^(.{20,100}?)(?:\.|,|$)", task_context)
        if purpose_match:
            concepts.append({
                "fact_type": "task_understanding",
                "content": f"Task purpose: {purpose_match.group(1).strip()}",
                "confidence": base_confidence,
                "tags": ["noetic", "preflight", "purpose"],
            })

    return concepts


def _extract_check_concepts(
    reasoning: str,
    vectors: Optional[Dict[str, float]],
) -> List[Dict]:
    """Extract decision rationale concepts from CHECK reasoning."""
    concepts = []

    # Confidence based on uncertainty (lower uncertainty = more confident decision)
    base_confidence = 0.65
    if vectors:
        uncertainty = vectors.get("uncertainty", 0.5)
        base_confidence = min(0.9, 0.5 + (1 - uncertainty) * 0.4)

    # Decision patterns (WHY proceed/investigate)
    decision_patterns = [
        r"(?:decided|choosing|opted)\s+to\s+(\w+)\s+because\s+(.{20,150}?)(?:\.|$)",
        r"proceeding\s+(?:because|since)\s+(.{20,150}?)(?:\.|$)",
        r"investigating\s+(?:because|since|due to)\s+(.{20,150}?)(?:\.|$)",
        r"ready\s+to\s+(?:proceed|continue)\s+(.{15,100}?)(?:\.|$)",
    ]

    for pattern in decision_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:2]:
            if isinstance(match, tuple):
                content = f"Decision: {match[0]} - {match[1].strip()}"
            else:
                content = f"Decision rationale: {match.strip()}"
            concepts.append({
                "fact_type": "decision_rationale",
                "content": content,
                "confidence": base_confidence,
                "tags": ["noetic", "check", "decision"],
            })

    # Approach selection patterns (WHICH)
    approach_patterns = [
        r"(?:chose|selected|using)\s+(.{10,50}?)\s+(?:approach|method|strategy)",
        r"approach:?\s+(.{15,100}?)(?:\.|$)",
    ]

    for pattern in approach_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:1]:
            content = f"Approach chosen: {match.strip()}"
            concepts.append({
                "fact_type": "decision_rationale",
                "content": content,
                "confidence": base_confidence * 0.9,
                "tags": ["noetic", "check", "approach"],
            })

    return concepts


def _extract_postflight_concepts(
    reasoning: str,
    task_context: Optional[str],
    vectors: Optional[Dict[str, float]],
) -> List[Dict]:
    """Extract learning insight concepts from POSTFLIGHT reasoning."""
    concepts = []

    # Higher confidence for learning insights (they're validated by completion)
    base_confidence = 0.75
    if vectors and "completion" in vectors:
        base_confidence = min(0.95, 0.6 + vectors["completion"] * 0.35)

    # Learning patterns (generalizable insights)
    learning_patterns = [
        r"learned\s+(?:that\s+)?(.{20,150}?)(?:\.|$)",
        r"discovered\s+(?:that\s+)?(.{20,150}?)(?:\.|$)",
        r"realized\s+(?:that\s+)?(.{20,150}?)(?:\.|$)",
        r"insight:?\s+(.{20,150}?)(?:\.|$)",
        r"pattern:?\s+(.{20,100}?)(?:\.|$)",
    ]

    for pattern in learning_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:2]:
            content = f"Learning: {match.strip()}"
            concepts.append({
                "fact_type": "learning_insight",
                "content": content,
                "confidence": base_confidence,
                "tags": ["noetic", "postflight", "learning"],
            })

    # Causal patterns (X leads to Y)
    causal_patterns = [
        r"(.{10,50}?)\s+(?:leads to|causes|results in|enables)\s+(.{10,100}?)(?:\.|$)",
        r"when\s+(.{10,50}?),?\s+(?:then\s+)?(.{10,100}?)(?:\.|$)",
    ]

    for pattern in causal_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:1]:
            if isinstance(match, tuple) and len(match) == 2:
                content = f"Causal pattern: {match[0].strip()} → {match[1].strip()}"
                concepts.append({
                    "fact_type": "learning_insight",
                    "content": content,
                    "confidence": base_confidence * 0.85,
                    "tags": ["noetic", "postflight", "causal"],
                })

    # Domain applicability (FOR WHOM)
    domain_patterns = [
        r"applies to\s+(.{10,50}?)(?:\.|$)",
        r"relevant for\s+(.{10,50}?)(?:\.|$)",
        r"useful for\s+(.{10,50}?)(?:\.|$)",
    ]

    for pattern in domain_patterns:
        matches = re.findall(pattern, reasoning, re.IGNORECASE)
        for match in matches[:1]:
            content = f"Applies to: {match.strip()}"
            concepts.append({
                "fact_type": "learning_insight",
                "content": content,
                "confidence": base_confidence * 0.8,
                "tags": ["noetic", "postflight", "domain"],
            })

    return concepts


def embed_noetic_concepts(
    project_id: str,
    session_id: str,
    concepts: List[Dict],
    domain: Optional[str] = None,
) -> Tuple[int, int]:
    """
    Embed extracted noetic concepts into eidetic memory.

    Args:
        project_id: Project UUID
        session_id: Session UUID (for source tracking)
        concepts: List of concept dicts from extract_noetic_concepts
        domain: Optional domain tag for all concepts

    Returns:
        Tuple of (embedded_count, failed_count)
    """
    if not concepts:
        return (0, 0)

    try:
        from empirica.core.qdrant.vector_store import embed_eidetic
    except ImportError:
        logger.warning("Qdrant not available for noetic embedding")
        return (0, len(concepts))

    embedded = 0
    failed = 0

    for concept in concepts:
        fact_id = f"noetic_{session_id}_{uuid.uuid4().hex[:8]}"

        success = embed_eidetic(
            project_id=project_id,
            fact_id=fact_id,
            content=concept["content"],
            fact_type=concept["fact_type"],
            domain=domain or "noetic",
            confidence=concept["confidence"],
            confirmation_count=1,
            source_sessions=[session_id],
            tags=concept.get("tags", []),
        )

        if success:
            embedded += 1
        else:
            failed += 1

    logger.info(f"Noetic concepts embedded: {embedded}, failed: {failed}")
    return (embedded, failed)


def hook_cascade_noetic(
    phase: str,
    session_id: str,
    project_id: str,
    reasoning: str,
    task_context: Optional[str] = None,
    vectors: Optional[Dict[str, float]] = None,
    domain: Optional[str] = None,
) -> Dict:
    """
    Main hook to call from CASCADE phase handlers.

    This extracts noetic concepts from reasoning and embeds them as eidetic facts.

    Args:
        phase: CASCADE phase (PREFLIGHT, CHECK, POSTFLIGHT)
        session_id: Current session UUID
        project_id: Project UUID
        reasoning: The reasoning text from the phase
        task_context: Optional task description
        vectors: Optional epistemic vectors
        domain: Optional domain tag

    Returns:
        Dict with extraction and embedding results
    """
    # Extract concepts
    concepts = extract_noetic_concepts(
        reasoning=reasoning,
        phase=phase,
        task_context=task_context,
        vectors=vectors,
    )

    if not concepts:
        return {
            "ok": True,
            "phase": phase,
            "concepts_extracted": 0,
            "concepts_embedded": 0,
            "note": "No noetic concepts extracted from reasoning",
        }

    # Embed concepts
    embedded, failed = embed_noetic_concepts(
        project_id=project_id,
        session_id=session_id,
        concepts=concepts,
        domain=domain,
    )

    return {
        "ok": True,
        "phase": phase,
        "concepts_extracted": len(concepts),
        "concepts_embedded": embedded,
        "concepts_failed": failed,
        "concepts": [c["content"][:100] for c in concepts],  # Summary
    }
