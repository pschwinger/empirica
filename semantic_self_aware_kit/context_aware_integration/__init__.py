"""
🔗 Context-Aware Integration - Enterprise Component
Enterprise client systems and advanced context management
"""

from .context_aware_integration import (
    ContextType,
    ContextMetadata,
    ContextAwareClient,
    EnterpriseContextManager,
    IntegrationAdapter,
    ClientProtocolHandler
)

__all__ = [
    'ContextAwareClient',
    'EnterpriseContextManager',
    'IntegrationAdapter',
    'ClientProtocolHandler',
    'ContextType',
    'ContextMetadata'
]

__version__ = "1.0.0"
__component__ = "context_aware_integration"
__tier__ = "enterprise"
__purpose__ = "Enterprise client integration with advanced context-aware capabilities"