#!/bin/bash

# Setup script to add PRD automation alias to your shell

# Detect shell
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "❌ Unsupported shell: $SHELL"
    exit 1
fi

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create alias
ALIAS_LINE="alias kaia='python3 $PROJECT_DIR/scripts/master_auto.py'"

# Check if alias already exists
if grep -q "alias kaia=" "$SHELL_CONFIG"; then
    echo "🔄 Updating existing kaia alias..."
    # Remove existing alias line
    sed -i '' '/alias kaia=/d' "$SHELL_CONFIG"
fi

# Add alias to shell config
echo "$ALIAS_LINE" >> "$SHELL_CONFIG"

echo "✅ PRD automation alias added to $SHELL_CONFIG"
echo "📝 Added: $ALIAS_LINE"
echo ""
echo "🔄 Please reload your shell or run: source $SHELL_CONFIG"
echo ""
echo "🚀 Then you can use: kaia your_product_idea.txt" 