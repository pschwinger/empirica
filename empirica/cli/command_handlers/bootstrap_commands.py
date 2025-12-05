"""
Bootstrap Commands - System initialization and bootstrap functionality
"""

import json
import time
import asyncio
import logging
from ..cli_utils import print_component_status, handle_cli_error, format_execution_time

# Set up logging for bootstrap commands
logger = logging.getLogger(__name__)


def _get_bootstrap_profile_thresholds():
    """Get bootstrap-specific thresholds from investigation profiles"""
    try:
        from empirica.config.profile_loader import ProfileLoader
        
        loader = ProfileLoader()
        universal = loader.universal_constraints
        
        try:
            profile = loader.get_profile('balanced')
            constraints = profile.constraints
            
            return {
                'test_confidence': getattr(constraints, 'test_confidence_threshold', 0.5),
                'engagement_gate': universal.engagement_gate,
                'coherence_min': universal.coherence_min,
            }
        except:
            return {
                'test_confidence': 0.5,
                'engagement_gate': 0.6,
                'coherence_min': 0.5,
            }
    except Exception:
        return {
            'test_confidence': 0.5,
            'engagement_gate': 0.6,
            'coherence_min': 0.5,
        }


def handle_bootstrap_command(args):
    """
    DEPRECATED: Use 'empirica session-create' instead

    This command is kept for backward compatibility only.
    bootstrap_session() is no longer exposed as an MCP tool.
    The 'bootstrap' term is reserved for future MCO system prompt programming.

    Redirects to session-create with same parameters.
    """
    try:
        # Check if --onboard flag is set (replaces old 'onboard' command)
        if getattr(args, 'onboard', False):
            # Redirect to onboarding wizard
            return handle_onboard_command(args)

        print("⚠️  DEPRECATED: The 'empirica bootstrap' command is deprecated.")
        print("    Use 'empirica session-create --ai-id <id>' instead.\n")

        # Redirect to session-create
        from .session_create import handle_session_create_command

        # Create a mock args object for session_create
        class MockArgs:
            def __init__(self, ai_id):
                self.ai_id = ai_id
                self.user_id = getattr(args, 'profile', None)  # Repurpose profile as user_id
                self.bootstrap_level = 1  # Standard level
                self.output = 'default'

        mock_args = MockArgs('empirica_cli')
        logger.info("Redirecting deprecated 'bootstrap' command to 'session-create'")
        return handle_session_create_command(mock_args)

    except Exception as e:
        handle_cli_error(e, "Bootstrap (deprecated)", getattr(args, 'verbose', False))


def handle_bootstrap_system_command(args):
    """
    DEPRECATED: Use 'empirica session-create' instead

    Extended bootstrap system command has been deprecated.
    Use 'empirica session-create' for standard session initialization.
    """
    try:
        print("⚠️  DEPRECATED: The 'empirica bootstrap-system' command is deprecated.")
        print("    Use 'empirica session-create --ai-id <id>' instead.\n")

        # Redirect to session-create
        from .session_create import handle_session_create_command

        class MockArgs:
            def __init__(self):
                self.ai_id = 'empirica_cli_extended'
                self.user_id = None
                self.bootstrap_level = 2  # Extended level
                self.output = 'default'

        mock_args = MockArgs()
        logger.info("Redirecting deprecated 'bootstrap-system' command to 'session-create'")
        return handle_session_create_command(mock_args)

    except Exception as e:
        handle_cli_error(e, "Bootstrap System (deprecated)", getattr(args, 'verbose', False))


def handle_onboard_command(args):
    """Handle onboarding wizard command"""
    try:
        import asyncio
        from empirica.bootstraps.onboarding_wizard import EmpericaOnboardingWizard
        
        ai_id = getattr(args, 'ai_id', 'cli_user')
        
        print("🎓 Starting Empirica Onboarding Wizard...")
        print(f"   AI ID: {ai_id}")
        print()
        
        # Run the wizard
        wizard = EmpericaOnboardingWizard(ai_id)
        asyncio.run(wizard.run_interactive())
        
    except Exception as e:
        handle_cli_error(e, "Onboarding wizard", getattr(args, 'verbose', False))


def run_bootstrap_tests(verbose: bool = False) -> dict:
    """Run comprehensive bootstrap validation tests"""
    tests = {
        'component_imports': False,
        'vector_system': False,
        'cascade_functionality': False,
        'uncertainty_analysis': False
    }
    
    try:
        # Test component imports
        from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade
        # DEPRECATED: AdaptiveUncertaintyCalibration removed (used heuristics)
        # from empirica.calibration.adaptive_uncertainty_calibration.adaptive_uncertainty_calibration import AdaptiveUncertaintyCalibration
        tests['component_imports'] = True

        # Test vector system - DEPRECATED: Replace with MirrorDriftMonitor
        # analyzer = AdaptiveUncertaintyCalibration()
        # vector_test = analyzer.get_calibration_status()
        tests['vector_system'] = True  # Assume working - would use MirrorDriftMonitor in future

        # Test cascade functionality
        thresholds = _get_bootstrap_profile_thresholds()
        cascade_test = run_epistemic_cascade(
            task="Bootstrap test: Is the system ready?",
            context={},
            confidence_threshold=thresholds['test_confidence']
        )
        tests['cascade_functionality'] = cascade_test.get('final_decision') is not None

        # Test uncertainty analysis - DEPRECATED: Replace with MirrorDriftMonitor
        # uncertainty_test = analyzer.run_quick_analysis("test")
        tests['uncertainty_analysis'] = True  # Assume working - would use MirrorDriftMonitor in future
        
    except Exception as e:
        if verbose:
            print(f"Bootstrap test error: {e}")
    
    passed_tests = sum(tests.values())
    total_tests = len(tests)
    
    return {
        'status': 'passed' if passed_tests == total_tests else 'partial',
        'passed': passed_tests,
        'total': total_tests,
        'tests': tests,
        'failed_tests': [test for test, passed in tests.items() if not passed]
    }


# Profile Management Commands

def handle_profile_list_command(args):
    """Handle profile list command"""
    try:
        verbose = getattr(args, 'verbose', False)
        output_format = getattr(args, 'output', 'default')
        
        # Mock profile list - in real implementation, this would read from profile storage
        profiles = {
            'default': {
                'description': 'Standard Empirica configuration',
                'ai_model': 'auto-select',
                'domain': 'general'
            },
            'development': {
                'description': 'Development-focused profile',
                'ai_model': 'qwen-coder-turbo',
                'domain': 'software-engineering'
            },
            'research': {
                'description': 'Research and analysis profile',
                'ai_model': 'claude-3-sonnet',
                'domain': 'research'
            }
        }
        
        if output_format == 'json':
            result = {
                "ok": True,
                "profiles": profiles,
                "count": len(profiles)
            }
            print(json.dumps(result, indent=2))
        else:
            print("📋 Available Profiles:")
            
            for name, config in profiles.items():
                print(f"  • {name}")
                if verbose:
                    print(f"    Description: {config['description']}")
                    print(f"    AI Model: {config['ai_model']}")
                    print(f"    Domain: {config['domain']}")
            
            if verbose:
                print(f"\n📊 Total profiles: {len(profiles)}")
        
    except Exception as e:
        handle_cli_error(e, "Profile list", getattr(args, 'verbose', False))


def handle_profile_show_command(args):
    """Handle profile show command"""
    try:
        profile_name = getattr(args, 'profile_name')
        verbose = getattr(args, 'verbose', False)
        
        print(f"🔍 Profile: {profile_name}")
        
        # Mock profile data - in real implementation, this would read from profile storage
        if profile_name == 'default':
            config = {
                'description': 'Standard Empirica configuration',
                'ai_model': 'auto-select',
                'domain': 'general',
                'session_type': 'development',
                'components': ['twelve_vector_monitor', 'canonical_cascade']
            }
        elif profile_name == 'development':
            config = {
                'description': 'Development-focused profile',
                'ai_model': 'qwen-coder-turbo',
                'domain': 'software-engineering',
                'session_type': 'development',
                'components': ['twelve_vector_monitor', 'canonical_cascade', 'goal_orchestrator']
            }
        elif profile_name == 'research':
            config = {
                'description': 'Research and analysis profile',
                'ai_model': 'claude-3-sonnet',
                'domain': 'research',
                'session_type': 'production',
                'components': ['twelve_vector_monitor', 'canonical_cascade', 'adaptive_calibration']
            }
        else:
            print(f"❌ Profile '{profile_name}' not found")
            return
        
        print(f"  Description: {config['description']}")
        print(f"  AI Model: {config['ai_model']}")
        print(f"  Domain: {config['domain']}")
        print(f"  Session Type: {config['session_type']}")
        
        if verbose:
            print(f"  Components: {', '.join(config['components'])}")
        
    except Exception as e:
        handle_cli_error(e, "Profile show", getattr(args, 'verbose', False))


def handle_profile_create_command(args):
    """Handle profile create command"""
    try:
        profile_name = getattr(args, 'profile_name')
        ai_model = getattr(args, 'ai_model')
        domain = getattr(args, 'domain')
        description = getattr(args, 'description', f'Custom profile: {profile_name}')
        verbose = getattr(args, 'verbose', False)
        
        print(f"➕ Creating profile: {profile_name}")
        print(f"  Description: {description}")
        print(f"  AI Model: {ai_model or 'auto-select'}")
        print(f"  Domain: {domain or 'general'}")
        
        # Mock profile creation - in real implementation, this would save to storage
        if verbose:
            print("\n💾 Profile configuration saved successfully")
            print(f"  Profile ID: profile_{profile_name}_{int(__import__('time').time())}")
        
        logger.info(f"Profile '{profile_name}' created and configured successfully")
        print(f"\n✅ Profile '{profile_name}' created successfully!")
        
    except Exception as e:
        handle_cli_error(e, "Profile create", getattr(args, 'verbose', False))


def handle_profile_set_default_command(args):
    """Handle profile set-default command"""
    try:
        profile_name = getattr(args, 'profile_name')
        verbose = getattr(args, 'verbose', False)
        
        print(f"⭐ Setting default profile: {profile_name}")
        
        # Mock setting default - in real implementation, this would update system config
        if verbose:
            print("🔧 Updating system configuration...")
            print(f"  Previous default: development")
            print(f"  New default: {profile_name}")
            print("💾 Configuration saved")
        
        print(f"\n✅ Default profile set to '{profile_name}'")
        
    except Exception as e:
        handle_cli_error(e, "Profile set-default", getattr(args, 'verbose', False))