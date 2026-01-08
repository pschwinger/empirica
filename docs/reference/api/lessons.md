# Lessons API - Procedural Knowledge System

**Module:** `empirica.core.lessons.storage.LessonStorageManager`
**Category:** Epistemic Learning
**Stability:** Beta

---

## Overview

The Lessons system provides **epistemic lesson graphs** - procedural knowledge that AIs can learn from and replay. Built on 4-layer storage for optimal retrieval speed.

### Storage Architecture

| Layer | Speed | Purpose | Location |
|-------|-------|---------|----------|
| **HOT** | ns | Graph traversal, relationships | In-memory |
| **WARM** | μs | Metadata queries | SQLite `lessons` table |
| **SEARCH** | ms | Semantic similarity | Qdrant `empirica_lessons` |
| **COLD** | 10ms | Full content | `.empirica/lessons/*.yaml` |

---

## CLI Commands

### `lesson-create`

Create a new lesson from JSON input.

```bash
empirica lesson-create - << 'EOF'
{
  "name": "NotebookLM: Navigate to Studio Tab",
  "version": "1.0",
  "description": "Navigate from Chat to Studio tab",
  "epistemic": {
    "source_confidence": 0.95,
    "teaching_quality": 0.90,
    "reproducibility": 0.85,
    "expected_delta": {"know": 0.15, "do": 0.20, "uncertainty": -0.10}
  },
  "steps": [
    {"order": 1, "phase": "praxic", "action": "Click Studio tab", "target": "Studio tab button", "expected_outcome": "Studio view opens"}
  ],
  "domain": "notebooklm",
  "tags": ["notebooklm", "studio", "atomic"]
}
EOF
```

**Output:**
```json
{
  "ok": true,
  "lesson_id": "8f89dc21e5160e5a",
  "cold_path": ".empirica/lessons/8f89dc21e5160e5a.yaml",
  "qdrant_id": "abc123...",
  "elapsed_ms": 45.2
}
```

---

### `lesson-load`

Load a lesson by ID from storage.

```bash
empirica lesson-load --id 8f89dc21e5160e5a --output json
```

**Output:** Full lesson JSON including steps, epistemic metadata, validation stats.

---

### `lesson-list`

List all lessons, optionally filtered by domain.

```bash
# List all
empirica lesson-list --output json

# Filter by domain
empirica lesson-list --domain notebooklm --output json
```

**Output:**
```json
{
  "ok": true,
  "count": 6,
  "lessons": [
    {"id": "8f89dc21e5160e5a", "name": "NotebookLM: Navigate to Studio Tab", "domain": "notebooklm"},
    ...
  ]
}
```

---

### `lesson-search`

Semantic search for lessons using Qdrant.

```bash
empirica lesson-search --query "how to generate slides in NotebookLM" --output json
```

**Output:**
```json
{
  "ok": true,
  "query": "how to generate slides in NotebookLM",
  "count": 5,
  "lessons": [
    {"id": "9d2533b08863f644", "name": "NotebookLM: Generate Slide Deck", "score": 0.89},
    ...
  ]
}
```

---

### `lesson-recommend`

Find lessons that address epistemic gaps based on current state.

```bash
empirica lesson-recommend --know 0.5 --uncertainty 0.7 --output json
```

**Output:** Lessons sorted by expected impact on weak vectors.

---

### `lesson-path`

Get topological prerequisite path to a target lesson.

```bash
empirica lesson-path --target 9d2533b08863f644 --output json
```

**Output:**
```json
{
  "ok": true,
  "target": "9d2533b08863f644",
  "path_length": 2,
  "path": [
    {"id": "8f89dc21e5160e5a", "name": "NotebookLM: Navigate to Studio Tab"},
    {"id": "9d2533b08863f644", "name": "NotebookLM: Generate Slide Deck"}
  ]
}
```

**Knowledge Graph:** Uses `requires` edges in `knowledge_graph` table to compute topological sort.

---

### `lesson-embed`

Embed all lessons into Qdrant for semantic search.

```bash
empirica lesson-embed --output json
```

**Output:**
```json
{
  "ok": true,
  "embedded_count": 8,
  "failed_count": 0,
  "collection": "empirica_lessons"
}
```

---

### `lesson-replay-start`

Start tracking a lesson replay session.

```bash
empirica lesson-replay-start \
  --lesson-id 8f89dc21e5160e5a \
  --session-id <SESSION_UUID> \
  --output json
```

**Output:**
```json
{
  "ok": true,
  "replay_id": "uuid",
  "lesson_name": "NotebookLM: Navigate to Studio Tab",
  "total_steps": 3
}
```

---

### `lesson-replay-end`

Complete a lesson replay and record outcome.

```bash
empirica lesson-replay-end \
  --replay-id <REPLAY_UUID> \
  --success true \
  --steps-completed 3 \
  --output json
```

**Output:**
```json
{
  "ok": true,
  "replay_id": "uuid",
  "success": true,
  "updated_stats": {"replay_count": 5, "success_rate": 0.80}
}
```

---

### `lesson-stats`

Get lesson system statistics.

```bash
empirica lesson-stats --output json
```

**Output:**
```json
{
  "ok": true,
  "stats": {
    "warm": {"lesson_count": 8, "edge_count": 12, "successful_replays": 15},
    "hot": {"lessons": 8, "domains": 2, "vectors_tracked": 5},
    "cold": {"path": ".empirica/lessons", "file_count": 8},
    "search": {"enabled": true, "collection": "empirica_lessons"}
  }
}
```

---

## Lesson Schema

### Step Phases

| Phase | Description |
|-------|-------------|
| `noetic` | Observation/understanding - look at something, verify state |
| `praxic` | Action/doing - click, type, execute |

### Expected Delta Vectors

| Vector | Description |
|--------|-------------|
| `know` | Knowledge increase |
| `do` | Capability increase |
| `context` | Context understanding |
| `clarity` | Mental model clarity |
| `coherence` | Understanding coherence |
| `signal` | Signal-to-noise improvement |
| `uncertainty` | Uncertainty reduction (negative = good) |

---

## Knowledge Graph Edges

Lessons can be connected via the `knowledge_graph` table:

```sql
INSERT INTO knowledge_graph (id, source_type, source_id, relation_type, target_type, target_id, weight)
VALUES ('kg_nav_enables_slides', 'lesson', 'lesson_A', 'enables', 'lesson', 'lesson_B', 1.0);
```

### Relation Types

| Type | Meaning |
|------|---------|
| `requires` | Target must complete source first |
| `enables` | Completing source unlocks target |
| `related_to` | Semantic similarity |

---

## Python API

```python
from empirica.core.lessons.storage import get_lesson_storage

storage = get_lesson_storage()

# Create lesson
from empirica.core.lessons.schema import Lesson, LessonStep, LessonEpistemic, EpistemicDelta
lesson = Lesson(
    name="My Lesson",
    version="1.0",
    description="...",
    epistemic=LessonEpistemic(
        source_confidence=0.9,
        teaching_quality=0.85,
        reproducibility=0.8,
        expected_delta=EpistemicDelta(know=0.15, uncertainty=-0.10)
    ),
    steps=[LessonStep(order=1, phase="praxic", action="...")],
    domain="my_domain",
    tags=["tag1"]
)
result = storage.create_lesson(lesson)

# Search
results = storage.search_lessons(query="how to do X", limit=5)

# Get learning path
path = storage.get_learning_path(target_lesson_id="abc123")
```

---

## Implementation Files

- `empirica/core/lessons/schema.py` - Dataclasses
- `empirica/core/lessons/storage.py` - 4-layer storage manager
- `empirica/core/lessons/hot_cache.py` - In-memory graph
- `empirica/cli/command_handlers/lesson_commands.py` - CLI handlers
- `empirica/cli/parsers/lesson_parsers.py` - Argument parsers
