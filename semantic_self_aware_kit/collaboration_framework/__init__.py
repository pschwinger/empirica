from typing import Any, Callable

#!/usr/bin/env python3
"""
🤝 Collaboration Framework Component
Self-contained AI-to-AI collaboration and partnership management
"""

from .collaboration_framework import (
    PartnershipEngine,
    CollaborationProtocol,
    AIPartner,
    CollaborationManager,
    TaskCoordinator,
    CollaborativeTask,
    TaskStatus,
    AIRole,
    PartnershipType
)

# Create default instances for immediate use
default_collaboration_manager = CollaborationManager()
default_task_coordinator = TaskCoordinator(default_collaboration_manager)

# Set up default collaboration protocols
try:
    # Create standard collaboration protocol
    standard_protocol = CollaborationProtocol("standard_ai_collaboration")
    
    # Register basic message handlers
    def handle_task_update(sender: str, data: Any) -> bool:
        print(f"📋 Task update from {sender}: {data}")
        return True
    
    def handle_coordination_request(sender: str, data: Any) -> bool:
        print(f"🤝 Coordination request from {sender}: {data}")
        return True
    
    standard_protocol.register_handler("task_update", handle_task_update)
    standard_protocol.register_handler("coordination_request", handle_coordination_request)
    
    default_collaboration_manager.partnership_engine.protocols["standard"] = standard_protocol
    
    print("🤝 Collaboration Framework: Standard protocols initialized")
except Exception as e:
    print(f"⚠️ Protocol initialization failed: {e}")

# Export main classes and instances
__all__ = [
    'PartnershipEngine',
    'CollaborationProtocol',
    'AIPartner',
    'CollaborationManager',
    'TaskCoordinator',
    'CollaborativeTask',
    'TaskStatus',
    'AIRole',
    'PartnershipType',
    'default_collaboration_manager',
    'default_task_coordinator'
]

__version__ = "1.0.0"
__component__ = "collaboration_framework"
__purpose__ = "Multi-AI coordination, partnership, and collaborative task management"

print(f"🤝 Collaboration Framework component ready for AI collaboration!")