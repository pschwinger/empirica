"""
Data structures for reasoning layer outputs
"""

from dataclasses import dataclass
from typing import List, Dict, Literal

@dataclass
class DeprecationJudgment:
    """Result of deprecation analysis"""
    feature: str
    status: Literal["deprecated", "historical", "active"]
    confidence: float  # 0.0-1.0
    reasoning: str
    evidence: List[str]
    recommendation: str
    metadata: Dict = None

@dataclass
class RelationshipAnalysis:
    """Result of doc-code relationship analysis"""
    relationship: Literal["aligned", "partial", "drift", "unrelated"]
    confidence: float
    reasoning: str
    gaps: List[str]
    action: str
    metadata: Dict = None

@dataclass
class ImplementationGap:
    """Result of implementation gap analysis"""
    gap_type: Literal["missing", "different", "extra", "none"]
    severity: Literal["critical", "high", "medium", "low"]
    confidence: float
    reasoning: str
    impact: str
    recommendation: str
    metadata: Dict = None
