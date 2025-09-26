#!/bin/bash
#
# CLI Usage Examples for Semantic Self-Aware Kit
#

echo "⌨️ CLI Usage Examples for Semantic Self-Aware Kit"
echo "=============================================="

# Ensure we're in the right directory
cd "$(dirname "$0")/.."

echo -e "\n1. Getting intelligent suggestions..."
.venv/bin/semantic-kit suggest

echo -e "\n2. Testing self-awareness capabilities..."
.venv/bin/semantic-kit self-test

echo -e "\n3. Running metacognitive cascade..."
.venv/bin/semantic-kit cascade "Should we implement this feature?"

echo -e "\n4. Investigating code..."
.venv/bin/semantic-kit investigate .

echo -e "\n5. Running performance benchmarks..."
.venv/bin/semantic-kit benchmark

echo -e "\n6. Listing all components..."
.venv/bin/semantic-kit list-components

echo -e "\n7. Demonstrating framework capabilities..."
.venv/bin/semantic-kit demo

echo -e "\n8. Testing all components..."
.venv/bin/semantic-kit test-all

echo -e "\n✅ CLI usage examples completed successfully!"