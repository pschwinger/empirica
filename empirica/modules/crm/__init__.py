"""
CRM Module - Relational Epistemics

Tracks what AI knows about entities (clients) separate from tasks (goals).
Enables persistent relationship management with epistemic tracking.

Key concepts:
- Client: Persistent entity with ongoing relationship
- Engagement: Time-bounded interaction with a client
- Client Memory: Findings/unknowns scoped to a client
"""

from .client_store import (
    ClientStore,
    create_client,
    get_client,
    list_clients,
    update_client,
    archive_client,
)

__all__ = [
    'ClientStore',
    'create_client',
    'get_client',
    'list_clients',
    'update_client',
    'archive_client',
]
