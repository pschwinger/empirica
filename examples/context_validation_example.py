#!/usr/bin/env python3
"""
Example of using Context Validation with the Semantic Self-Aware Kit
"""

from semantic_self_aware_kit.context_validation import create_context_validator

def demonstrate_context_validation():
    """
    Demonstrate context validation capabilities
    """
    print("🔍 Context Validation with Semantic Self-Aware Kit")
    print("=" * 50)
    
    # Create the context validator
    print("\n1. Initializing Context Validator...")
    context_validator = create_context_validator()
    print("   ✅ Context Validator initialized")
    
    # Example 1: Validate code context
    print("\n2. Validating code context...")
    code_context = {
        "file_path": "./src/auth.py",
        "language": "python",
        "framework": "flask",
        "dependencies": ["flask", "bcrypt", "sqlalchemy"],
        "purpose": "user authentication module"
    }
    
    try:
        validation_result = context_validator.validate_context(code_context)
        print("   ✅ Code context validation completed")
        
        # Display validation results
        if isinstance(validation_result, dict):
            is_valid = validation_result.get('is_valid', False)
            issues = validation_result.get('issues', [])
            recommendations = validation_result.get('recommendations', [])
        else:
            is_valid = getattr(validation_result, 'is_valid', False)
            issues = getattr(validation_result, 'issues', [])
            recommendations = getattr(validation_result, 'recommendations', [])
            
        print(f"   ✅ Context Valid: {is_valid}")
        
        if issues:
            print("   ⚠️  Validation Issues:")
            for i, issue in enumerate(issues[:3], 1):  # Show top 3
                print(f"      {i}. {issue}")
        else:
            print("   ✅ No validation issues found")
            
        if recommendations:
            print("   💡 Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {recommendation}")
                
    except Exception as e:
        print(f"   ⚠️  Error during code context validation: {e}")
    
    # Example 2: Validate development environment context
    print("\n3. Validating development environment context...")
    env_context = {
        "python_version": "3.9",
        "os": "linux",
        "available_memory": "8GB",
        "disk_space": "50GB",
        "network_access": "restricted",
        "development_stage": "testing"
    }
    
    try:
        env_validation = context_validator.validate_environment_context(env_context)
        print("   ✅ Environment context validation completed")
        
        # Display environment validation results
        if isinstance(env_validation, dict):
            is_suitable = env_validation.get('is_suitable', False)
            constraints = env_validation.get('constraints', [])
            optimizations = env_validation.get('optimizations', [])
        else:
            is_suitable = getattr(env_validation, 'is_suitable', False)
            constraints = getattr(env_validation, 'constraints', [])
            optimizations = getattr(env_validation, 'optimizations', [])
            
        print(f"   ✅ Environment Suitable: {is_suitable}")
        
        if constraints:
            print("   ⚠️  Environmental Constraints:")
            for i, constraint in enumerate(constraints[:3], 1):  # Show top 3
                print(f"      {i}. {constraint}")
        else:
            print("   ✅ No environmental constraints found")
            
        if optimizations:
            print("   ⚡ Environmental Optimizations:")
            for i, optimization in enumerate(optimizations[:3], 1):  # Show top 3
                print(f"      {i}. {optimization}")
                
    except Exception as e:
        print(f"   ⚠️  Error during environment context validation: {e}")
    
    # Example 3: Validate AI collaboration context
    print("\n4. Validating AI collaboration context...")
    collaboration_context = {
        "collaboration_type": "peer-to-peer",
        "participants": ["qwen_ai", "developer_partner"],
        "communication_protocol": "messaging",
        "trust_level": "medium",
        "task_complexity": "high"
    }
    
    try:
        collab_validation = context_validator.validate_collaboration_context(collaboration_context)
        print("   ✅ Collaboration context validation completed")
        
        # Display collaboration validation results
        if isinstance(collab_validation, dict):
            is_viable = collab_validation.get('is_viable', False)
            risks = collab_validation.get('risks', [])
            collaboration_strategies = collab_validation.get('collaboration_strategies', [])
        else:
            is_viable = getattr(collab_validation, 'is_viable', False)
            risks = getattr(collab_validation, 'risks', [])
            collaboration_strategies = getattr(collab_validation, 'collaboration_strategies', [])
            
        print(f"   ✅ Collaboration Viable: {is_viable}")
        
        if risks:
            print("   ⚠️  Collaboration Risks:")
            for i, risk in enumerate(risks[:3], 1):  # Show top 3
                print(f"      {i}. {risk}")
        else:
            print("   ✅ No collaboration risks identified")
            
        if collaboration_strategies:
            print("   🤝 Collaboration Strategies:")
            for i, strategy in enumerate(collaboration_strategies[:3], 1):  # Show top 3
                print(f"      {i}. {strategy}")
                
    except Exception as e:
        print(f"   ⚠️  Error during collaboration context validation: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Context Validation component ensures that the working context is")
    print("accurate, consistent, and suitable for the intended operations. This")
    print("helps prevent errors and miscommunications by validating assumptions")
    print("about the environment, code, and tasks.")
    
    return {
        "code_validation": validation_result if 'validation_result' in locals() else None,
        "env_validation": env_validation if 'env_validation' in locals() else None,
        "collab_validation": collab_validation if 'collab_validation' in locals() else None
    }

def main():
    results = demonstrate_context_validation()
    print("\n✅ Context validation demonstration completed!")

if __name__ == "__main__":
    main()
