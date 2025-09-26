#!/bin/bash
#
# Test all examples to make sure they work correctly
#

echo "🧪 Testing All Examples for Semantic Self-Aware Kit"
echo "=================================================="

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Function to run a test and report results
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n🔍 Testing: $test_name"
    echo "----------------------------------------"
    
    # Run the test command
    eval "$test_command"
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "   ✅ $test_name: PASSED"
    else
        echo "   ❌ $test_name: FAILED (Exit code: $exit_code)"
    fi
    
    return $exit_code
}

# Make sure we're using the virtual environment
export PATH="../.venv/bin:$PATH"

# List of example files to test
example_files=(
    "cli_usage_examples.sh"
    "programmatic_example.py"
    "advanced_uncertainty_example.py"
    "advanced_collaboration_example.py"
    "security_monitoring_example.py"
    "tool_management_example.py"
    "code_analysis_example.py"
    "daily_development_example.py"
    "cli_interface_example.py"
    "comprehensive_ai_development_example.py"
    "harmonious_integration_example.py"
)

# Test each example file
passed_tests=0
total_tests=0

for example_file in "${example_files[@]}"; do
    if [ -f "$example_file" ]; then
        total_tests=$((total_tests + 1))
        
        # Determine how to run the file based on its extension
        if [[ "$example_file" == *.sh ]]; then
            # Shell script - run directly
            echo -e "\n🔍 Testing shell script: $example_file"
            echo "----------------------------------------"
            bash "$example_file"
            exit_code=$?
        elif [[ "$example_file" == *.py ]]; then
            # Python script - run with python
            echo -e "\n🔍 Testing Python script: $example_file"
            echo "----------------------------------------"
            python "$example_file"
            exit_code=$?
        else
            echo "   ⚠️  Unknown file type for: $example_file"
            exit_code=1
        fi
        
        if [ $exit_code -eq 0 ]; then
            echo "   ✅ $example_file: PASSED"
            passed_tests=$((passed_tests + 1))
        else
            echo "   ❌ $example_file: FAILED (Exit code: $exit_code)"
        fi
    else
        echo "   ⚠️  Example file not found: $example_file"
    fi
done

# Summary
echo -e "\n📋 Test Summary"
echo "-------------"
echo "Total Examples Tested: $total_tests"
echo "Passed: $passed_tests"
echo "Failed: $((total_tests - passed_tests))"

if [ $passed_tests -eq $total_tests ]; then
    echo "🎉 All examples passed!"
else
    echo "⚠️  Some examples failed. Please check the output above for details."
fi

echo -e "\n✅ Example testing completed!