#!/bin/bash
#
# Empirica System Prompt Installation Script
# Purpose: Automate installation of Empirica system prompts for Gemini CLI and Claude Code
# Date: 2025-11-15
# Version: 1.0
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
EMPIRICA_ROOT="/path/to/empirica"
SOURCE_PROMPT="$EMPIRICA_ROOT/GENERIC_EMPIRICA_SYSTEM_PROMPT.md"
GEMINI_DIR="$HOME/.gemini"
GEMINI_PROMPT="$GEMINI_DIR/system_empirica.md"
CLAUDE_PROMPT="$EMPIRICA_ROOT/CLAUDE.md"

# Functions
print_header() {
    echo -e "${BLUE}=================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Main installation
main() {
    print_header "Empirica System Prompt Installer"
    echo ""

    # Check if source file exists
    if [ ! -f "$SOURCE_PROMPT" ]; then
        print_error "Source prompt not found: $SOURCE_PROMPT"
        exit 1
    fi
    print_success "Found source prompt: $SOURCE_PROMPT"
    echo ""

    # Install Gemini CLI prompt
    print_header "Installing Gemini CLI System Prompt"
    echo ""

    # Create Gemini directory if it doesn't exist
    if [ ! -d "$GEMINI_DIR" ]; then
        print_info "Creating Gemini directory: $GEMINI_DIR"
        mkdir -p "$GEMINI_DIR"
    fi

    # Copy prompt file
    print_info "Copying prompt to: $GEMINI_PROMPT"
    cp "$SOURCE_PROMPT" "$GEMINI_PROMPT"
    print_success "Gemini prompt installed successfully"

    # Check if environment variable is already set
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        if grep -q "GEMINI_SYSTEM_MD" "$SHELL_RC"; then
            print_warning "GEMINI_SYSTEM_MD already set in $SHELL_RC"
        else
            print_info "Adding GEMINI_SYSTEM_MD to $SHELL_RC"
            echo "" >> "$SHELL_RC"
            echo "# Empirica system prompt for Gemini CLI" >> "$SHELL_RC"
            echo "export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md" >> "$SHELL_RC"
            print_success "Environment variable added to $SHELL_RC"
            print_warning "Run 'source $SHELL_RC' or restart your terminal to activate"
        fi
    else
        print_warning "Could not find shell config file (.bashrc or .zshrc)"
        print_info "Add this to your shell config manually:"
        echo "  export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md"
    fi

    echo ""

    # Install Claude Code prompt
    print_header "Installing Claude Code System Prompt"
    echo ""

    print_info "Copying prompt to: $CLAUDE_PROMPT"
    cp "$SOURCE_PROMPT" "$CLAUDE_PROMPT"
    print_success "Claude Code prompt installed successfully"

    echo ""

    # Verification
    print_header "Installation Summary"
    echo ""

    echo "Gemini CLI:"
    echo "  Location: $GEMINI_PROMPT"
    echo "  Size: $(du -h "$GEMINI_PROMPT" | cut -f1)"
    echo "  Env var: GEMINI_SYSTEM_MD=$GEMINI_PROMPT"
    echo ""

    echo "Claude Code:"
    echo "  Location: $CLAUDE_PROMPT"
    echo "  Size: $(du -h "$CLAUDE_PROMPT" | cut -f1)"
    echo "  Auto-load: Yes (when in $EMPIRICA_ROOT)"
    echo ""

    # Next steps
    print_header "Next Steps"
    echo ""

    echo "1. Verify Gemini CLI installation:"
    echo "   ${BLUE}GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini${NC}"
    echo "   Then ask: 'What framework are you using?'"
    echo ""

    echo "2. Verify Claude Code installation:"
    echo "   ${BLUE}cd $EMPIRICA_ROOT${NC}"
    echo "   ${BLUE}claude${NC}"
    echo "   Then ask: 'What framework are you using?'"
    echo ""

    echo "3. Read the installation guide:"
    echo "   ${BLUE}cat docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md${NC}"
    echo ""

    print_success "Installation complete!"
}

# Run main function
main
