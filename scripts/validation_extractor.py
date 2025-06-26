#!/usr/bin/env python3
"""
Validation Extractor - Extracts validation findings from technical specification
and creates a separate validation tracking file.
"""

import re
import argparse
import os

def extract_validation_findings(spec_file):
    """Extract validation findings from technical specification."""
    
    with open(spec_file, 'r') as f:
        content = f.read()
    
    validation_data = {
        'cto_validation': '',
        'technical_validation': '',
        'open_questions': '',
        'assumptions': '',
        'issues_concerns': ''
    }
    
    # Extract CTO Technical Validation
    cto_match = re.search(r'## CTO Technical Validation(.*?)(?=##|$)', content, re.DOTALL)
    if cto_match:
        validation_data['cto_validation'] = cto_match.group(1).strip()
    
    # Extract Technical Validation Findings & Decisions
    tech_val_match = re.search(r'## Technical Validation Findings & Decisions(.*?)(?=##|$)', content, re.DOTALL)
    if tech_val_match:
        validation_data['technical_validation'] = tech_val_match.group(1).strip()
    
    # Extract Open Questions & Assumptions
    open_q_match = re.search(r'## Open Questions & Assumptions(.*?)(?=##|$)', content, re.DOTALL)
    if open_q_match:
        validation_data['open_questions'] = open_q_match.group(1).strip()
    
    return validation_data

def create_validation_file(validation_data, output_file):
    """Create a validation tracking markdown file."""
    
    with open(output_file, 'w') as f:
        f.write("# Technical Validation Tracking\n\n")
        f.write("This document tracks validation findings and corrections applied to the technical architecture.\n\n")
        
        f.write("## CTO Technical Validation\n\n")
        if validation_data['cto_validation']:
            f.write(validation_data['cto_validation'])
        else:
            f.write("*No CTO validation found in specification.*\n")
        f.write("\n\n")
        
        f.write("## Technical Validation Findings\n\n")
        if validation_data['technical_validation']:
            f.write(validation_data['technical_validation'])
        else:
            f.write("*No technical validation findings found in specification.*\n")
        f.write("\n\n")
        
        f.write("## Open Questions & Assumptions\n\n")
        if validation_data['open_questions']:
            f.write(validation_data['open_questions'])
        else:
            f.write("*No open questions found in specification.*\n")
        f.write("\n\n")
        
        f.write("## Corrections Applied\n\n")
        f.write("*This section will be updated after post-generation corrections are applied.*\n\n")
        f.write("### Architecture Changes Made\n")
        f.write("- *Pending correction analysis*\n\n")
        f.write("### Validation Issues Resolved\n")
        f.write("- *Pending correction analysis*\n\n")
        f.write("### Remaining Open Issues\n")
        f.write("- *Pending correction analysis*\n")

def main():
    parser = argparse.ArgumentParser(description='Extract validation findings from technical specification')
    parser.add_argument('spec_file', help='Path to the technical specification file')
    parser.add_argument('--output', default='output/validation_tracking.md', help='Output validation file path')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Extract validation findings
    validation_data = extract_validation_findings(args.spec_file)
    
    # Create validation tracking file
    create_validation_file(validation_data, args.output)
    
    print(f"✅ Validation findings extracted to: {args.output}")

if __name__ == "__main__":
    main() 