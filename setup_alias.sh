#!/bin/bash

# Setup script for PRD Auto CLI alias
# This script adds an alias to your shell configuration for easy access to the PRD Auto tools

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Setting up PRD Auto CLI alias...${NC}"

# Get the project directory (where this script is located)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine shell configuration file
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo -e "${RED}❌ Unsupported shell: $SHELL${NC}"
    exit 1
fi

echo -e "${YELLOW}📝 Detected shell: $SHELL_NAME${NC}"
echo -e "${YELLOW}📝 Config file: $SHELL_CONFIG${NC}"

# Create the alias line
ALIAS_LINE="alias kaia='python3 $PROJECT_DIR/scripts/master_auto.py'"

# Check if alias already exists
if grep -q "alias kaia=" "$SHELL_CONFIG"; then
    echo -e "${YELLOW}🔄 Updating existing kaia alias...${NC}"
    # Remove existing alias line
    sed -i '' '/alias kaia=/d' "$SHELL_CONFIG"
fi

# Add the alias to the shell configuration
echo "" >> "$SHELL_CONFIG"
echo "# PRD Auto CLI alias" >> "$SHELL_CONFIG"
echo "$ALIAS_LINE" >> "$SHELL_CONFIG"

echo -e "${GREEN}✅ Alias added to $SHELL_CONFIG${NC}"
echo -e "${YELLOW}🔄 Please restart your terminal or run: source $SHELL_CONFIG${NC}"
echo -e "${GREEN}🚀 Then you can use: kaia your_product_idea${NC}" 