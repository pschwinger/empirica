"""
CRM Schema

Database table schemas for CRM (Client Relationship Management) module.
Enables relational epistemics - tracking what AI knows about entities (clients).
"""

SCHEMAS = [
    # Clients: Persistent relationship entities
    """
    CREATE TABLE IF NOT EXISTS clients (
        client_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,

        -- Knowledge base links
        notebooklm_url TEXT,
        knowledge_base_urls TEXT,  -- JSON array of additional URLs

        -- Contact information
        contacts TEXT,  -- JSON array: [{name, email, role, notes}]

        -- Classification
        client_type TEXT DEFAULT 'prospect',  -- prospect, active, partner, churned
        industry TEXT,
        tags TEXT,  -- JSON array

        -- Metadata
        created_at REAL NOT NULL,
        updated_at REAL,
        created_by_ai_id TEXT,

        -- Epistemic state (aggregate across engagements)
        relationship_health REAL DEFAULT 0.5,  -- 0.0-1.0
        engagement_frequency REAL DEFAULT 0.0,  -- interactions per week
        knowledge_depth REAL DEFAULT 0.0,  -- how well do I know them

        -- Status
        status TEXT DEFAULT 'active',  -- active, inactive, archived
        last_contact_at REAL,
        next_action TEXT,
        next_action_due REAL
    )
    """,

    # Engagements: Time-bounded client interactions
    """
    CREATE TABLE IF NOT EXISTS engagements (
        engagement_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,

        -- What is this engagement about
        title TEXT NOT NULL,
        description TEXT,
        engagement_type TEXT DEFAULT 'outreach',  -- outreach, demo, negotiation, support, review

        -- Linked goal (optional)
        goal_id TEXT,

        -- Timeline
        started_at REAL NOT NULL,
        ended_at REAL,
        status TEXT DEFAULT 'active',  -- active, completed, stalled, lost

        -- Outcome tracking
        outcome TEXT,  -- won, lost, deferred, ongoing
        outcome_notes TEXT,

        -- Value tracking (optional)
        estimated_value REAL,
        actual_value REAL,
        currency TEXT DEFAULT 'USD',

        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
    )
    """,

    # Client-scoped findings (links existing findings to clients)
    """
    CREATE TABLE IF NOT EXISTS client_findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id TEXT NOT NULL,
        finding_id TEXT NOT NULL,
        relevance REAL DEFAULT 1.0,  -- how relevant is this finding to client
        created_at REAL NOT NULL,

        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        UNIQUE(client_id, finding_id)
    )
    """,

    # Client-scoped unknowns
    """
    CREATE TABLE IF NOT EXISTS client_unknowns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id TEXT NOT NULL,
        unknown_id TEXT NOT NULL,
        priority TEXT DEFAULT 'medium',  -- critical, high, medium, low
        created_at REAL NOT NULL,

        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        UNIQUE(client_id, unknown_id)
    )
    """,

    # Client interactions log (lightweight activity tracking)
    """
    CREATE TABLE IF NOT EXISTS client_interactions (
        interaction_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        engagement_id TEXT,
        session_id TEXT,

        -- What happened
        interaction_type TEXT NOT NULL,  -- email, call, meeting, demo, document
        summary TEXT NOT NULL,

        -- Who was involved
        contacts_involved TEXT,  -- JSON array of contact names
        ai_id TEXT,

        -- When
        occurred_at REAL NOT NULL,

        -- Sentiment/outcome
        sentiment TEXT,  -- positive, neutral, negative
        follow_up_required INTEGER DEFAULT 0,
        follow_up_notes TEXT,

        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    )
    """,

    # Indexes for performance
    "CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status)",
    "CREATE INDEX IF NOT EXISTS idx_clients_type ON clients(client_type)",
    "CREATE INDEX IF NOT EXISTS idx_engagements_client ON engagements(client_id)",
    "CREATE INDEX IF NOT EXISTS idx_engagements_status ON engagements(status)",
    "CREATE INDEX IF NOT EXISTS idx_client_findings_client ON client_findings(client_id)",
    "CREATE INDEX IF NOT EXISTS idx_client_unknowns_client ON client_unknowns(client_id)",
    "CREATE INDEX IF NOT EXISTS idx_interactions_client ON client_interactions(client_id)",
    "CREATE INDEX IF NOT EXISTS idx_interactions_date ON client_interactions(occurred_at)",
]
