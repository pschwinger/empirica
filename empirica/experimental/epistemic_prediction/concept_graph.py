"""
Phase 2: Concept Co-occurrence Graphs

Builds graph of concept relationships from findings/unknowns/dead_ends.
Extracts concepts using keyword extraction and tracks co-occurrence
based on session proximity.

Architecture:
- ConceptExtractor: Extracts meaningful concepts from text
- ConceptGraph: Stores and queries concept relationships
- Co-occurrence: Concepts appearing in same session share edges
"""

import json
import logging
import re
import sqlite3
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class RelationshipType(Enum):
    """Types of concept relationships"""
    LEADS_TO = "leads_to"
    SIMILAR = "similar"
    CONTRADICTS = "contradicts"
    DEPENDS_ON = "depends_on"
    CO_OCCURS = "co_occurs"


@dataclass
class ConceptNode:
    """A concept in the knowledge graph"""
    concept_id: str
    concept_text: str
    normalized_text: str
    source_type: str
    frequency: int = 1
    total_impact: float = 0.0
    avg_impact: float = 0.0
    session_ids: List[str] = field(default_factory=list)
    source_ids: List[str] = field(default_factory=list)


@dataclass
class ConceptEdge:
    """Relationship between two concepts"""
    edge_id: str
    source_concept_id: str
    target_concept_id: str
    relationship: RelationshipType
    weight: float
    co_occurrence_count: int = 1
    session_ids: List[str] = field(default_factory=list)


# Stopwords for concept extraction
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "to", "of",
    "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "above", "below", "between", "under",
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "just", "also", "now", "and", "but", "or", "if", "because",
    "until", "while", "this", "that", "these", "those", "it", "its",
    "i", "we", "you", "he", "she", "they", "them", "their", "our", "my",
    "your", "his", "her", "which", "what", "who", "whom", "whose",
    "using", "used", "uses", "make", "made", "making", "get", "got",
    "getting", "set", "setting", "see", "saw", "seen", "seeing",
    "work", "works", "working", "worked", "new", "old", "first", "last",
    "long", "great", "little", "own", "still", "back", "way",
}

# Domain-specific terms to preserve (not filter as stopwords)
DOMAIN_TERMS = {
    "epistemic", "cascade", "preflight", "postflight", "check",
    "session", "finding", "unknown", "deadend", "goal", "subtask",
    "vector", "calibration", "drift", "uncertainty", "confidence",
    "noetic", "praxic", "eidetic", "episodic", "memory",
    "sqlite", "qdrant", "git", "hook", "cli", "mcp",
}


class ConceptExtractor:
    """Extracts meaningful concepts from text."""

    def __init__(
        self,
        min_word_length: int = 3,
        max_ngram: int = 3,
        stopwords: Set[str] = None,
    ):
        self.min_word_length = min_word_length
        self.max_ngram = max_ngram
        self.stopwords = stopwords or STOPWORDS

    def extract(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract concepts from text.

        Returns:
            List of (concept_text, normalized_text) tuples
        """
        if not text:
            return []

        # Clean and tokenize
        text = text.lower()
        text = re.sub(r'[^\w\s\-_]', ' ', text)
        words = text.split()

        # Filter and normalize words
        filtered_words = []
        for word in words:
            word = word.strip('-_')
            if len(word) >= self.min_word_length:
                if word not in self.stopwords or word in DOMAIN_TERMS:
                    filtered_words.append(word)

        concepts = []

        # Extract single words
        for word in filtered_words:
            normalized = self._normalize(word)
            if normalized:
                concepts.append((word, normalized))

        # Extract bigrams
        if self.max_ngram >= 2:
            for i in range(len(filtered_words) - 1):
                bigram = f"{filtered_words[i]} {filtered_words[i+1]}"
                normalized = self._normalize(bigram)
                if normalized:
                    concepts.append((bigram, normalized))

        # Extract trigrams
        if self.max_ngram >= 3:
            for i in range(len(filtered_words) - 2):
                trigram = f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}"
                normalized = self._normalize(trigram)
                if normalized:
                    concepts.append((trigram, normalized))

        return concepts

    def _normalize(self, text: str) -> str:
        """Normalize concept text for matching."""
        text = text.strip().lower()
        text = re.sub(r'\s+', '_', text)
        text = re.sub(r'[^\w_]', '', text)
        return text if len(text) >= self.min_word_length else ""


class ConceptGraph:
    """
    Builds and queries concept co-occurrence graphs.

    Usage:
        graph = ConceptGraph(project_id, db_path)
        graph.build_from_sources()
        neighbors = graph.get_neighbors(concept_id)
        related = graph.find_related_concepts("epistemic")
    """

    def __init__(self, project_id: str, db_path: Path = None):
        self.project_id = project_id
        self.db_path = db_path or Path.cwd() / ".empirica" / "sessions" / "sessions.db"
        self.extractor = ConceptExtractor()
        self._ensure_tables()

    def _ensure_tables(self):
        """Ensure concept graph tables exist."""
        from empirica.data.schema.concept_graph_schema import SCHEMAS
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for schema in SCHEMAS:
            try:
                cursor.execute(schema)
            except sqlite3.Error as e:
                logger.debug(f"Schema execution note: {e}")
        conn.commit()
        conn.close()

    def build_from_sources(self, overwrite: bool = False) -> Dict:
        """
        Build concept graph from findings, unknowns, and dead_ends.

        Returns:
            Stats dict with counts
        """
        if overwrite:
            self._clear_project_data()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Gather all source records with session context
        sources = []

        # Findings
        cursor.execute("""
            SELECT id, session_id, finding, impact
            FROM project_findings
            WHERE project_id = ?
        """, (self.project_id,))
        for row in cursor.fetchall():
            sources.append({
                "id": row[0],
                "session_id": row[1],
                "text": row[2],
                "impact": row[3] or 0.5,
                "source_type": "finding",
            })

        # Unknowns
        cursor.execute("""
            SELECT id, session_id, unknown, impact
            FROM project_unknowns
            WHERE project_id = ?
        """, (self.project_id,))
        for row in cursor.fetchall():
            sources.append({
                "id": row[0],
                "session_id": row[1],
                "text": row[2],
                "impact": row[3] or 0.5,
                "source_type": "unknown",
            })

        # Dead ends (no impact column in this table)
        cursor.execute("""
            SELECT id, session_id, approach, why_failed
            FROM project_dead_ends
            WHERE project_id = ?
        """, (self.project_id,))
        for row in cursor.fetchall():
            text = f"{row[2]} {row[3]}"
            sources.append({
                "id": row[0],
                "session_id": row[1],
                "text": text,
                "impact": 0.5,
                "source_type": "dead_end",
            })

        conn.close()

        if not sources:
            return {"ok": True, "nodes": 0, "edges": 0, "note": "No sources found"}

        # Extract concepts and build graph
        session_concepts = defaultdict(list)
        concept_data = defaultdict(lambda: {
            "frequency": 0,
            "total_impact": 0.0,
            "session_ids": set(),
            "source_ids": set(),
            "source_types": set(),
            "original_text": None,
        })

        for source in sources:
            concepts = self.extractor.extract(source["text"])
            session_id = source["session_id"]

            for concept_text, normalized in concepts:
                data = concept_data[normalized]
                data["frequency"] += 1
                data["total_impact"] += source["impact"]
                data["session_ids"].add(session_id)
                data["source_ids"].add(source["id"])
                data["source_types"].add(source["source_type"])
                if data["original_text"] is None:
                    data["original_text"] = concept_text

                session_concepts[session_id].append(normalized)

        # Filter low-frequency concepts
        MIN_FREQUENCY = 2
        filtered_concepts = {
            k: v for k, v in concept_data.items()
            if v["frequency"] >= MIN_FREQUENCY
        }

        # Store concept nodes
        nodes_stored = self._store_concept_nodes(filtered_concepts)

        # Build and store co-occurrence edges
        edges_stored = self._store_co_occurrence_edges(session_concepts, filtered_concepts)

        return {
            "ok": True,
            "sources_processed": len(sources),
            "concepts_extracted": len(concept_data),
            "nodes_stored": nodes_stored,
            "edges_stored": edges_stored,
        }

    def _clear_project_data(self):
        """Clear existing concept data for project."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM concept_edges WHERE project_id = ?", (self.project_id,))
        cursor.execute("DELETE FROM concept_nodes WHERE project_id = ?", (self.project_id,))
        cursor.execute("DELETE FROM concept_clusters WHERE project_id = ?", (self.project_id,))
        conn.commit()
        conn.close()

    def _store_concept_nodes(self, concept_data: Dict) -> int:
        """Store concept nodes to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = time.time()
        stored = 0

        for normalized, data in concept_data.items():
            concept_id = f"concept_{uuid.uuid4().hex[:12]}"
            avg_impact = data["total_impact"] / data["frequency"] if data["frequency"] > 0 else 0.0

            cursor.execute("""
                INSERT OR REPLACE INTO concept_nodes
                (concept_id, project_id, concept_text, normalized_text, source_type,
                 frequency, total_impact, avg_impact, first_seen_timestamp,
                 last_seen_timestamp, session_ids, source_ids)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                concept_id,
                self.project_id,
                data["original_text"],
                normalized,
                ",".join(data["source_types"]),
                data["frequency"],
                data["total_impact"],
                avg_impact,
                now,
                now,
                json.dumps(list(data["session_ids"])),
                json.dumps(list(data["source_ids"])),
            ))
            stored += 1

        conn.commit()
        conn.close()
        return stored

    def _store_co_occurrence_edges(
        self,
        session_concepts: Dict[str, List[str]],
        filtered_concepts: Dict,
    ) -> int:
        """Store co-occurrence edges between concepts in same session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = time.time()

        # Build co-occurrence counts
        co_occurrence = defaultdict(lambda: {"count": 0, "sessions": set()})

        for session_id, concepts in session_concepts.items():
            # Only count filtered concepts
            valid_concepts = [c for c in set(concepts) if c in filtered_concepts]

            # Create edges between all pairs
            for i, c1 in enumerate(valid_concepts):
                for c2 in valid_concepts[i+1:]:
                    key = tuple(sorted([c1, c2]))
                    co_occurrence[key]["count"] += 1
                    co_occurrence[key]["sessions"].add(session_id)

        # Get concept_id mapping
        cursor.execute("""
            SELECT normalized_text, concept_id FROM concept_nodes
            WHERE project_id = ?
        """, (self.project_id,))
        concept_id_map = {row[0]: row[1] for row in cursor.fetchall()}

        # Store edges
        stored = 0
        for (c1, c2), data in co_occurrence.items():
            if c1 not in concept_id_map or c2 not in concept_id_map:
                continue

            edge_id = f"edge_{uuid.uuid4().hex[:12]}"
            weight = min(1.0, data["count"] / 10.0)

            cursor.execute("""
                INSERT OR REPLACE INTO concept_edges
                (edge_id, project_id, source_concept_id, target_concept_id,
                 relationship_type, weight, co_occurrence_count, session_ids,
                 first_seen_timestamp, last_seen_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                edge_id,
                self.project_id,
                concept_id_map[c1],
                concept_id_map[c2],
                RelationshipType.CO_OCCURS.value,
                weight,
                data["count"],
                json.dumps(list(data["sessions"])),
                now,
                now,
            ))
            stored += 1

        conn.commit()
        conn.close()
        return stored

    def get_concept(self, concept_id: str) -> Optional[ConceptNode]:
        """Get a concept node by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT concept_id, concept_text, normalized_text, source_type,
                   frequency, total_impact, avg_impact, session_ids, source_ids
            FROM concept_nodes
            WHERE concept_id = ? AND project_id = ?
        """, (concept_id, self.project_id))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return ConceptNode(
            concept_id=row[0],
            concept_text=row[1],
            normalized_text=row[2],
            source_type=row[3],
            frequency=row[4],
            total_impact=row[5],
            avg_impact=row[6],
            session_ids=json.loads(row[7]) if row[7] else [],
            source_ids=json.loads(row[8]) if row[8] else [],
        )

    def find_concept_by_text(self, text: str) -> Optional[ConceptNode]:
        """Find concept by normalized text."""
        normalized = self.extractor._normalize(text)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT concept_id, concept_text, normalized_text, source_type,
                   frequency, total_impact, avg_impact, session_ids, source_ids
            FROM concept_nodes
            WHERE normalized_text = ? AND project_id = ?
        """, (normalized, self.project_id))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return ConceptNode(
            concept_id=row[0],
            concept_text=row[1],
            normalized_text=row[2],
            source_type=row[3],
            frequency=row[4],
            total_impact=row[5],
            avg_impact=row[6],
            session_ids=json.loads(row[7]) if row[7] else [],
            source_ids=json.loads(row[8]) if row[8] else [],
        )

    def get_neighbors(
        self,
        concept_id: str,
        min_weight: float = 0.1,
        limit: int = 20,
    ) -> List[Tuple[ConceptNode, float]]:
        """Get neighboring concepts sorted by edge weight."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get edges where this concept is source or target
        cursor.execute("""
            SELECT source_concept_id, target_concept_id, weight
            FROM concept_edges
            WHERE (source_concept_id = ? OR target_concept_id = ?)
              AND project_id = ?
              AND weight >= ?
            ORDER BY weight DESC
            LIMIT ?
        """, (concept_id, concept_id, self.project_id, min_weight, limit))

        edges = cursor.fetchall()
        conn.close()

        # Get neighbor concept IDs
        neighbor_weights = {}
        for src, tgt, weight in edges:
            neighbor_id = tgt if src == concept_id else src
            neighbor_weights[neighbor_id] = weight

        # Fetch neighbor concepts
        results = []
        for neighbor_id, weight in sorted(neighbor_weights.items(), key=lambda x: -x[1]):
            node = self.get_concept(neighbor_id)
            if node:
                results.append((node, weight))

        return results

    def find_related_concepts(
        self,
        search_text: str,
        limit: int = 10,
    ) -> List[Tuple[ConceptNode, float]]:
        """Find concepts related to search text."""
        # First try exact match
        concept = self.find_concept_by_text(search_text)
        if concept:
            return self.get_neighbors(concept.concept_id, limit=limit)

        # Fall back to partial match
        normalized = self.extractor._normalize(search_text)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT concept_id, concept_text, normalized_text, source_type,
                   frequency, total_impact, avg_impact, session_ids, source_ids
            FROM concept_nodes
            WHERE normalized_text LIKE ? AND project_id = ?
            ORDER BY frequency DESC
            LIMIT ?
        """, (f"%{normalized}%", self.project_id, limit))

        results = []
        for row in cursor.fetchall():
            node = ConceptNode(
                concept_id=row[0],
                concept_text=row[1],
                normalized_text=row[2],
                source_type=row[3],
                frequency=row[4],
                total_impact=row[5],
                avg_impact=row[6],
                session_ids=json.loads(row[7]) if row[7] else [],
                source_ids=json.loads(row[8]) if row[8] else [],
            )
            results.append((node, node.avg_impact))

        conn.close()
        return results

    def get_top_concepts(self, limit: int = 20) -> List[ConceptNode]:
        """Get top concepts by frequency."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT concept_id, concept_text, normalized_text, source_type,
                   frequency, total_impact, avg_impact, session_ids, source_ids
            FROM concept_nodes
            WHERE project_id = ?
            ORDER BY frequency DESC
            LIMIT ?
        """, (self.project_id, limit))

        results = []
        for row in cursor.fetchall():
            results.append(ConceptNode(
                concept_id=row[0],
                concept_text=row[1],
                normalized_text=row[2],
                source_type=row[3],
                frequency=row[4],
                total_impact=row[5],
                avg_impact=row[6],
                session_ids=json.loads(row[7]) if row[7] else [],
                source_ids=json.loads(row[8]) if row[8] else [],
            ))

        conn.close()
        return results

    def get_co_occurrence_matrix(
        self,
        concept_ids: List[str] = None,
        limit: int = 20,
    ) -> Dict[str, Dict[str, float]]:
        """Build co-occurrence matrix for concepts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if concept_ids:
            placeholders = ",".join(["?" for _ in concept_ids])
            cursor.execute(f"""
                SELECT source_concept_id, target_concept_id, weight
                FROM concept_edges
                WHERE project_id = ?
                  AND source_concept_id IN ({placeholders})
                  AND target_concept_id IN ({placeholders})
            """, (self.project_id,) + tuple(concept_ids) + tuple(concept_ids))
        else:
            cursor.execute("""
                SELECT source_concept_id, target_concept_id, weight
                FROM concept_edges
                WHERE project_id = ?
                ORDER BY weight DESC
                LIMIT ?
            """, (self.project_id, limit * limit))

        matrix = defaultdict(dict)
        for src, tgt, weight in cursor.fetchall():
            matrix[src][tgt] = weight
            matrix[tgt][src] = weight

        conn.close()
        return dict(matrix)

    def get_stats(self) -> Dict:
        """Get statistics about the concept graph."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*), SUM(frequency), AVG(frequency), AVG(avg_impact)
            FROM concept_nodes WHERE project_id = ?
        """, (self.project_id,))
        node_stats = cursor.fetchone()

        cursor.execute("""
            SELECT COUNT(*), SUM(co_occurrence_count), AVG(weight)
            FROM concept_edges WHERE project_id = ?
        """, (self.project_id,))
        edge_stats = cursor.fetchone()

        conn.close()

        return {
            "nodes": {
                "count": node_stats[0] or 0,
                "total_mentions": node_stats[1] or 0,
                "avg_frequency": node_stats[2] or 0,
                "avg_impact": node_stats[3] or 0,
            },
            "edges": {
                "count": edge_stats[0] or 0,
                "total_co_occurrences": edge_stats[1] or 0,
                "avg_weight": edge_stats[2] or 0,
            },
        }
