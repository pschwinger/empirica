#!/bin/bash
#
# Example of using the Semantic Self-Aware Kit from command line
#

echo "🧠 Semantic Self-Aware Kit - CLI Example"
echo "========================================"

# Ensure we're in the right directory
cd "$(dirname "$0")/.."

# 1. Self-test
echo -e "\n1. Running self-test..."
.venv/bin/semantic-kit self-test

# 2. List components
echo -e "\n2. Listing available components..."
.venv/bin/semantic-kit list-components

# 3. Run metacognitive cascade
echo -e "\n3. Running metacognitive cascade..."
.venv/bin/semantic-kit cascade "Should I analyze the codebase structure?"

# 4. Demonstrate framework capabilities
echo -e "\n4. Demonstrating framework capabilities..."
.venv/bin/semantic-kit demo

echo -e "\n✅ CLI example completed successfully!"