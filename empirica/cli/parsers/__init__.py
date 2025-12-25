"""
CLI Parser Modules - Modularized argument parsers for Empirica CLI

Each module contains parser definitions for a specific command group.
This modularization makes the CLI more maintainable by breaking down
the monolithic cli_core.py (1176 lines) into focused modules.
"""

from .cascade_parsers import add_cascade_parsers
from .investigation_parsers import add_investigation_parsers
from .performance_parsers import add_performance_parsers
from .skill_parsers import add_skill_parsers
from .utility_parsers import add_utility_parsers
from .config_parsers import add_config_parsers
from .monitor_parsers import add_monitor_parsers
from .session_parsers import add_session_parsers
from .action_parsers import add_action_parsers
from .checkpoint_parsers import add_checkpoint_parsers
from .user_interface_parsers import add_user_interface_parsers
from .vision_parsers import add_vision_parsers
from .epistemics_parsers import add_epistemics_parsers

__all__ = [
    'add_cascade_parsers',
    'add_investigation_parsers',
    'add_performance_parsers',
    'add_skill_parsers',
    'add_utility_parsers',
    'add_config_parsers',
    'add_monitor_parsers',
    'add_session_parsers',
    'add_action_parsers',
    'add_checkpoint_parsers',
    'add_user_interface_parsers',
    'add_vision_parsers',
    'add_epistemics_parsers',
]
