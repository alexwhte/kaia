#!/bin/bash

# PRD Automation Tool - Simple runner script
# Usage: ./run.sh your_product_idea.txt [options]

if [ $# -eq 0 ]; then
    echo "❌ Please provide a product idea file"
    echo "Usage: ./run.sh your_product_idea.txt [--version v1] [--skip-prd] [--skip-spec] [--skip-action-plan]"
    exit 1
fi

python3 scripts/master_auto.py "$@" 