#!/bin/bash
#
# Empirica System Prompt Installation Script (All Platforms)
# Purpose: Automate installation of Empirica system prompts for all supported AI CLI tools
# Platforms: Gemini CLI, Claude Code, GitHub Copilot CLI, Qwen Code, Atlassian Rovo Dev
# Date: 2025-11-15
# Version: 2.0
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

# Platform-specific paths
GEMINI_DIR="$HOME/.gemini"
GEMINI_PROMPT="$GEMINI_DIR/system_empirica.md"

CLAUDE_PROMPT="$EMPIRICA_ROOT/CLAUDE.md"

COPILOT_DIR="$EMPIRICA_ROOT/.github"
COPILOT_PROMPT="$COPILOT_DIR/copilot-instructions.md"

QWEN_PROMPT="$EMPIRICA_ROOT/QWEN.md"
QWEN_GLOBAL="$HOME/.qwen/QWEN.md"

ROVO_DIR="$HOME/.rovodev"
ROVO_CONFIG="$ROVO_DIR/config_empirica.yml"

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

# Installation functions for each platform

install_gemini() {
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
}

install_claude() {
    print_header "Installing Claude Code System Prompt"
    echo ""

    print_info "Copying prompt to: $CLAUDE_PROMPT"
    cp "$SOURCE_PROMPT" "$CLAUDE_PROMPT"
    print_success "Claude Code prompt installed successfully"

    echo ""
}

install_copilot() {
    print_header "Installing GitHub Copilot CLI Instructions"
    echo ""

    # Check if copilot-instructions.md already exists
    if [ -f "$COPILOT_PROMPT" ]; then
        print_warning "Copilot instructions already exist at: $COPILOT_PROMPT"
        print_info "Skipping installation (file already customized)"
    else
        # Create .github directory if it doesn't exist
        if [ ! -d "$COPILOT_DIR" ]; then
            print_info "Creating .github directory: $COPILOT_DIR"
            mkdir -p "$COPILOT_DIR"
        fi

        print_success "GitHub Copilot instructions already created at: $COPILOT_PROMPT"
    fi

    echo ""
}

install_qwen() {
    print_header "Installing Qwen Code Context File"
    echo ""

    # Install project-level QWEN.md
    if [ -f "$QWEN_PROMPT" ]; then
        print_warning "QWEN.md already exists at: $QWEN_PROMPT"
        print_info "Skipping installation (file already customized)"
    else
        print_success "Qwen Code context file already created at: $QWEN_PROMPT"
    fi

    # Optionally install global QWEN.md
    read -p "$(echo -e ${YELLOW}Do you want to install global Qwen context \(~/.qwen/QWEN.md\)? \[y/N\]: ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ ! -d "$HOME/.qwen" ]; then
            mkdir -p "$HOME/.qwen"
        fi
        cp "$QWEN_PROMPT" "$QWEN_GLOBAL"
        print_success "Global Qwen context installed at: $QWEN_GLOBAL"
    else
        print_info "Skipping global Qwen installation"
    fi

    echo ""
}

install_rovo() {
    print_header "Installing Atlassian Rovo Dev Configuration"
    echo ""

    # Check if config already exists
    if [ -f "$ROVO_CONFIG" ]; then
        print_warning "Rovo config already exists at: $ROVO_CONFIG"
        print_info "Skipping installation (file already customized)"
    else
        # Create .rovodev directory if it doesn't exist
        if [ ! -d "$ROVO_DIR" ]; then
            print_info "Creating Rovo directory: $ROVO_DIR"
            mkdir -p "$ROVO_DIR"
        fi

        print_success "Rovo configuration already created at: $ROVO_CONFIG"
    fi

    print_info "To use: acli rovodev run --config-file ~/.rovodev/config_empirica.yml"

    echo ""
}

# Main installation
main() {
    print_header "Empirica System Prompt Installer (All Platforms)"
    echo ""
    echo "This script will install Empirica system prompts for:"
    echo "  1. Gemini CLI"
    echo "  2. Claude Code"
    echo "  3. GitHub Copilot CLI"
    echo "  4. Qwen Code"
    echo "  5. Atlassian Rovo Dev"
    echo ""

    # Check if source file exists
    if [ ! -f "$SOURCE_PROMPT" ]; then
        print_error "Source prompt not found: $SOURCE_PROMPT"
        exit 1
    fi
    print_success "Found source prompt: $SOURCE_PROMPT"
    echo ""

    # Ask which platforms to install
    read -p "$(echo -e ${YELLOW}Install for all platforms? \[Y/n\]: ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        # Selective installation
        read -p "Install Gemini CLI? [Y/n]: " -n 1 -r; echo
        [[ ! $REPLY =~ ^[Nn]$ ]] && install_gemini

        read -p "Install Claude Code? [Y/n]: " -n 1 -r; echo
        [[ ! $REPLY =~ ^[Nn]$ ]] && install_claude

        read -p "Install GitHub Copilot CLI? [Y/n]: " -n 1 -r; echo
        [[ ! $REPLY =~ ^[Nn]$ ]] && install_copilot

        read -p "Install Qwen Code? [Y/n]: " -n 1 -r; echo
        [[ ! $REPLY =~ ^[Nn]$ ]] && install_qwen

        read -p "Install Atlassian Rovo Dev? [Y/n]: " -n 1 -r; echo
        [[ ! $REPLY =~ ^[Nn]$ ]] && install_rovo
    else
        # Install all platforms
        install_gemini
        install_claude
        install_copilot
        install_qwen
        install_rovo
    fi

    # Installation Summary
    print_header "Installation Summary"
    echo ""

    echo "1. Gemini CLI:"
    [ -f "$GEMINI_PROMPT" ] && echo "   ✅ $GEMINI_PROMPT ($(du -h "$GEMINI_PROMPT" | cut -f1))" || echo "   ⏭️  Not installed"
    echo ""

    echo "2. Claude Code:"
    [ -f "$CLAUDE_PROMPT" ] && echo "   ✅ $CLAUDE_PROMPT ($(du -h "$CLAUDE_PROMPT" | cut -f1))" || echo "   ⏭️  Not installed"
    echo ""

    echo "3. GitHub Copilot CLI:"
    [ -f "$COPILOT_PROMPT" ] && echo "   ✅ $COPILOT_PROMPT ($(du -h "$COPILOT_PROMPT" | cut -f1))" || echo "   ⏭️  Not installed"
    echo ""

    echo "4. Qwen Code:"
    [ -f "$QWEN_PROMPT" ] && echo "   ✅ $QWEN_PROMPT ($(du -h "$QWEN_PROMPT" | cut -f1))" || echo "   ⏭️  Not installed"
    [ -f "$QWEN_GLOBAL" ] && echo "   ✅ $QWEN_GLOBAL (global)" || echo ""
    echo ""

    echo "5. Atlassian Rovo Dev:"
    [ -f "$ROVO_CONFIG" ] && echo "   ✅ $ROVO_CONFIG ($(du -h "$ROVO_CONFIG" | cut -f1))" || echo "   ⏭️  Not installed"
    echo ""

    # Next Steps
    print_header "Next Steps"
    echo ""

    echo "Verification Tests:"
    echo ""
    echo "1. Gemini CLI:"
    echo "   ${BLUE}GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini${NC}"
    echo "   Ask: 'What framework are you using?'"
    echo ""

    echo "2. Claude Code:"
    echo "   ${BLUE}cd $EMPIRICA_ROOT && claude${NC}"
    echo "   Ask: 'What are the phases of your workflow?'"
    echo ""

    echo "3. GitHub Copilot CLI:"
    echo "   ${BLUE}cd $EMPIRICA_ROOT && gh copilot${NC}"
    echo "   Ask: 'What framework are you using?'"
    echo ""

    echo "4. Qwen Code:"
    echo "   ${BLUE}cd $EMPIRICA_ROOT && qwen${NC}"
    echo "   Use: '/memory show' to see loaded context"
    echo ""

    echo "5. Atlassian Rovo Dev:"
    echo "   ${BLUE}acli rovodev run --config-file ~/.rovodev/config_empirica.yml${NC}"
    echo "   Ask: 'What workflow do you follow?'"
    echo ""

    echo "Documentation:"
    echo "   ${BLUE}cat docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md${NC}"
    echo ""

    print_success "Installation complete!"
}

# Run main function
main
