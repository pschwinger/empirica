#!/usr/bin/env python3
"""
🤝 Collaboration Framework Component
Self-contained AI-to-AI collaboration and partnership management

This component provides comprehensive collaboration capabilities including:
- Multi-AI coordination and task management
- Partnership protocols and communication
- Task distribution and load balancing
- Collaborative workflow optimization
"""

from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import threading
import queue

# ============================================================================
# CORE PARTNERSHIP ENGINE (from original partnership_core.py)
# ============================================================================

class PartnershipType(Enum):
    """Types of AI partnerships"""
    PEER_TO_PEER = "peer_to_peer"
    HIERARCHICAL = "hierarchical"
    SPECIALIZED = "specialized"
    TEMPORARY = "temporary"

@dataclass
class AIPartner:
    """Represents an AI partner in collaboration"""
    ai_id: str
    name: str
    capabilities: List[str]
    role: str = "general"
    status: str = "active"
    last_seen: datetime = field(default_factory=datetime.now)
    trust_score: float = 1.0
    
class CollaborationProtocol:
    """Protocol for AI collaboration communication"""
    
    def __init__(self, protocol_name: str):
        self.protocol_name = protocol_name
        self.message_handlers: Dict[str, Callable] = {}
        self.active_sessions: Dict[str, Any] = {}
        
    def register_handler(self, message_type: str, handler: Callable) -> bool:
        """Register message handler for protocol"""
        try:
            self.message_handlers[message_type] = handler
            return True
        except Exception as e:
            print(f"Failed to register handler for {message_type}: {e}")
            return False
    
    def send_message(self, recipient: str, message_type: str, data: Any) -> bool:
        """Send message to AI partner"""
        try:
            message = {
                'type': message_type,
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'protocol': self.protocol_name
            }
            
            # In a real implementation, this would send via network/IPC
            print(f"📤 Message sent to {recipient}: {message_type}")
            return True
        except Exception as e:
            print(f"Failed to send message to {recipient}: {e}")
            return False
    
    def handle_message(self, sender: str, message: Dict[str, Any]) -> bool:
        """Handle incoming message"""
        try:
            message_type = message.get('type')
            if message_type in self.message_handlers:
                handler = self.message_handlers[message_type]
                return handler(sender, message.get('data'))
            else:
                print(f"No handler for message type: {message_type}")
                return False
        except Exception as e:
            print(f"Error handling message from {sender}: {e}")
            return False

class PartnershipEngine:
    """Core partnership management engine"""
    
    def __init__(self):
        self.partners: Dict[str, AIPartner] = {}
        self.partnerships: Dict[str, Dict[str, Any]] = {}
        self.protocols: Dict[str, CollaborationProtocol] = {}
        self.communication_log: List[Dict[str, Any]] = []
        
    def register_partner(self, partner: AIPartner) -> bool:
        """Register a new AI partner"""
        try:
            self.partners[partner.ai_id] = partner
            print(f"🤝 Partner registered: {partner.name} ({partner.ai_id})")
            return True
        except Exception as e:
            print(f"Failed to register partner {partner.ai_id}: {e}")
            return False
    
    def create_partnership(self, partner1_id: str, partner2_id: str, 
                          partnership_type: PartnershipType,
                          terms: Dict[str, Any] = None) -> str:
        """Create partnership between two AIs"""
        try:
            partnership_id = f"{partner1_id}_{partner2_id}_{partnership_type.value}"
            
            partnership = {
                'id': partnership_id,
                'partners': [partner1_id, partner2_id],
                'type': partnership_type,
                'terms': terms or {},
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            self.partnerships[partnership_id] = partnership
            print(f"🤝 Partnership created: {partnership_id}")
            return partnership_id
        except Exception as e:
            print(f"Failed to create partnership: {e}")
            return ""
    
    def get_partner_capabilities(self, ai_id: str) -> List[str]:
        """Get capabilities of specific partner"""
        partner = self.partners.get(ai_id)
        return partner.capabilities if partner else []
    
    def find_partners_by_capability(self, capability: str) -> List[AIPartner]:
        """Find partners with specific capability"""
        matching_partners = []
        for partner in self.partners.values():
            if capability in partner.capabilities:
                matching_partners.append(partner)
        return matching_partners
    
    def update_trust_score(self, ai_id: str, score_delta: float) -> bool:
        """Update trust score for partner"""
        if ai_id in self.partners:
            current_score = self.partners[ai_id].trust_score
            new_score = max(0.0, min(1.0, current_score + score_delta))
            self.partners[ai_id].trust_score = new_score
            return True
        return False

# ============================================================================
# COLLABORATION MANAGEMENT AND TASK COORDINATION
# ============================================================================

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AIRole(Enum):
    """AI collaboration roles"""
    LEADER = "leader"
    SPECIALIST = "specialist"
    SUPPORTER = "supporter"
    OBSERVER = "observer"

@dataclass
class CollaborativeTask:
    """Represents a collaborative task"""
    task_id: str
    description: str
    assigned_to: List[str]
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    progress: float = 0.0

class CollaborationManager:
    """Core collaboration management for multi-AI coordination"""
    
    def __init__(self):
        self.partnership_engine = PartnershipEngine()
        self.active_ais: Dict[str, AIRole] = {}
        self.tasks: Dict[str, CollaborativeTask] = {}
        self.task_queue: List[str] = []
        self.completion_callbacks: Dict[str, List[Callable]] = {}
        self.coordination_lock = threading.Lock()
        
    def register_ai(self, ai_id: str, name: str, capabilities: List[str], 
                   role: AIRole = AIRole.SPECIALIST) -> bool:
        """Register AI participant in collaboration"""
        try:
            # Register with partnership engine
            partner = AIPartner(
                ai_id=ai_id,
                name=name,
                capabilities=capabilities,
                role=role.value
            )
            
            self.partnership_engine.register_partner(partner)
            self.active_ais[ai_id] = role
            
            print(f"🤖 AI registered: {name} ({ai_id}) as {role.value}")
            return True
        except Exception as e:
            print(f"❌ Failed to register AI {ai_id}: {e}")
            return False
    
    def create_task(self, task_id: str, description: str, 
                   assigned_to: List[str] = None, priority: int = 1,
                   dependencies: List[str] = None) -> bool:
        """Create a new collaborative task"""
        try:
            with self.coordination_lock:
                # Auto-assign if no specific assignment
                if not assigned_to:
                    assigned_to = self._auto_assign_task(description)
                
                # Validate assigned AIs are registered
                for ai_id in assigned_to:
                    if ai_id not in self.active_ais:
                        print(f"❌ AI {ai_id} not registered")
                        return False
                
                task = CollaborativeTask(
                    task_id=task_id,
                    description=description,
                    assigned_to=assigned_to,
                    priority=priority,
                    dependencies=dependencies or []
                )
                
                self.tasks[task_id] = task
                self._add_to_queue(task_id)
                
                print(f"📋 Task created: {task_id} -> {assigned_to}")
                return True
                
        except Exception as e:
            print(f"❌ Failed to create task {task_id}: {e}")
            return False
    
    def update_task_progress(self, task_id: str, progress: float, 
                           status: TaskStatus = None, result: Any = None) -> bool:
        """Update task progress and status"""
        if task_id not in self.tasks:
            return False
            
        with self.coordination_lock:
            task = self.tasks[task_id]
            task.progress = max(0.0, min(1.0, progress))
            
            if status:
                task.status = status
                
            if result is not None:
                task.result = result
                
            if status == TaskStatus.COMPLETED:
                task.completed_at = datetime.now()
                task.progress = 1.0
                self._trigger_completion_callbacks(task_id)
                
            print(f"📊 Task progress: {task_id} -> {progress:.1%}")
            return True
    
    def get_tasks_for_ai(self, ai_id: str, status: TaskStatus = None) -> List[CollaborativeTask]:
        """Get tasks assigned to specific AI"""
        ai_tasks = []
        for task in self.tasks.values():
            if ai_id in task.assigned_to:
                if status is None or task.status == status:
                    ai_tasks.append(task)
        return ai_tasks
    
    def get_next_task(self, ai_id: str) -> Optional[CollaborativeTask]:
        """Get next available task for AI"""
        with self.coordination_lock:
            for task_id in self.task_queue:
                task = self.tasks[task_id]
                if (ai_id in task.assigned_to and 
                    task.status == TaskStatus.PENDING and
                    self._dependencies_met(task_id)):
                    task.status = TaskStatus.IN_PROGRESS
                    print(f"🎯 Task assigned: {task_id} -> {ai_id}")
                    return task
        return None
    
    def coordinate_task_execution(self, task_id: str) -> bool:
        """Coordinate execution of multi-AI task"""
        if task_id not in self.tasks:
            return False
            
        task = self.tasks[task_id]
        
        # Create partnerships for task collaboration
        if len(task.assigned_to) > 1:
            for i, ai1 in enumerate(task.assigned_to):
                for ai2 in task.assigned_to[i+1:]:
                    partnership_id = self.partnership_engine.create_partnership(
                        ai1, ai2, PartnershipType.TEMPORARY,
                        {'task_id': task_id, 'purpose': 'task_collaboration'}
                    )
        
        return True
    
    def get_collaboration_stats(self) -> Dict[str, Any]:
        """Get comprehensive collaboration statistics"""
        with self.coordination_lock:
            stats = {
                'active_ais': len(self.active_ais),
                'total_tasks': len(self.tasks),
                'pending_tasks': len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
                'in_progress_tasks': len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]),
                'completed_tasks': len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
                'ai_roles': {ai_id: role.value for ai_id, role in self.active_ais.items()},
                'partnerships': len(self.partnership_engine.partnerships),
                'average_task_progress': self._calculate_average_progress()
            }
        return stats
    
    def _auto_assign_task(self, description: str) -> List[str]:
        """Automatically assign task based on AI capabilities"""
        # Simple heuristic assignment
        available_ais = list(self.active_ais.keys())
        if not available_ais:
            return []
            
        # Prefer leaders for coordination tasks
        if 'coordinate' in description.lower() or 'manage' in description.lower():
            leaders = [ai_id for ai_id, role in self.active_ais.items() if role == AIRole.LEADER]
            if leaders:
                return [leaders[0]]
        
        # Return first available AI for now (could be more sophisticated)
        return [available_ais[0]]
    
    def _add_to_queue(self, task_id: str):
        """Add task to queue based on priority"""
        task = self.tasks[task_id]
        inserted = False
        for i, queued_id in enumerate(self.task_queue):
            if self.tasks[queued_id].priority < task.priority:
                self.task_queue.insert(i, task_id)
                break
        if not inserted:
            self.task_queue.append(task_id)
    
    def _dependencies_met(self, task_id: str) -> bool:
        """Check if task dependencies are completed"""
        task = self.tasks[task_id]
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                if self.tasks[dep_id].status != TaskStatus.COMPLETED:
                    return False
        return True
    
    def _trigger_completion_callbacks(self, task_id: str):
        """Trigger callbacks for completed task"""
        if task_id in self.completion_callbacks:
            for callback in self.completion_callbacks[task_id]:
                try:
                    callback(self.tasks[task_id])
                except Exception as e:
                    print(f"Callback error for task {task_id}: {e}")
    
    def _calculate_average_progress(self) -> float:
        """Calculate average progress across all tasks"""
        if not self.tasks:
            return 0.0
        total_progress = sum(task.progress for task in self.tasks.values())
        return total_progress / len(self.tasks)

class TaskCoordinator:
    """Advanced task coordination with load balancing and optimization"""
    
    def __init__(self, collaboration_manager: CollaborationManager):
        self.collaboration_manager = collaboration_manager
        self.ai_workloads: Dict[str, int] = {}
        self.ai_capabilities: Dict[str, List[str]] = {}
        self.performance_metrics: Dict[str, Dict[str, float]] = {}
    
    def set_ai_capabilities(self, ai_id: str, capabilities: List[str]) -> bool:
        """Set AI capabilities for intelligent task assignment"""
        self.ai_capabilities[ai_id] = capabilities
        return True
    
    def auto_assign_task(self, task_id: str, required_capabilities: List[str] = None) -> List[str]:
        """Automatically assign task to best available AIs"""
        available_ais = []
        
        for ai_id in self.collaboration_manager.active_ais:
            # Check capabilities if specified
            if required_capabilities:
                ai_caps = self.ai_capabilities.get(ai_id, [])
                if not all(cap in ai_caps for cap in required_capabilities):
                    continue
            
            # Check current workload
            current_workload = self.ai_workloads.get(ai_id, 0)
            performance = self.performance_metrics.get(ai_id, {}).get('efficiency', 1.0)
            
            available_ais.append((ai_id, current_workload, performance))
        
        # Sort by workload and performance
        available_ais.sort(key=lambda x: (x[1], -x[2]))
        
        # Assign to best available AI(s)
        assigned = []
        for ai_id, _, _ in available_ais[:2]:  # Assign to top 2
            assigned.append(ai_id)
            self.ai_workloads[ai_id] = self.ai_workloads.get(ai_id, 0) + 1
        
        return assigned
    
    def update_performance_metrics(self, ai_id: str, task_id: str, 
                                 completion_time: float, quality_score: float):
        """Update AI performance metrics"""
        if ai_id not in self.performance_metrics:
            self.performance_metrics[ai_id] = {
                'efficiency': 1.0,
                'quality': 1.0,
                'task_count': 0
            }
        
        metrics = self.performance_metrics[ai_id]
        metrics['task_count'] += 1
        
        # Update efficiency (inverse of completion time)
        metrics['efficiency'] = (metrics['efficiency'] * 0.8) + (1.0 / max(completion_time, 0.1) * 0.2)
        
        # Update quality score
        metrics['quality'] = (metrics['quality'] * 0.8) + (quality_score * 0.2)
    
    def get_workload_stats(self) -> Dict[str, Any]:
        """Get current workload and performance statistics"""
        stats = {}
        for ai_id in self.collaboration_manager.active_ais:
            pending = len(self.collaboration_manager.get_tasks_for_ai(ai_id, TaskStatus.PENDING))
            in_progress = len(self.collaboration_manager.get_tasks_for_ai(ai_id, TaskStatus.IN_PROGRESS))
            
            stats[ai_id] = {
                'workload': pending + in_progress,
                'performance': self.performance_metrics.get(ai_id, {}),
                'capabilities': self.ai_capabilities.get(ai_id, [])
            }
        return stats
