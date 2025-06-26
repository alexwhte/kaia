#!/usr/bin/env python3
"""
Action Plan Auto - Generate Action Plan from Technical Specification markdown file
"""

import os
import sys
import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def extract_critical_sections(content, content_type):
    """Extract only the most critical sections to reduce token usage"""
    
    if content_type == "tech_spec":
        # Critical sections for action plan generation - expanded for better context
        critical_sections = [
            "Purpose & Scope",
            "High-Level Architecture Diagram", 
            "Key Components",
            "External Integrations & APIs",
            "Data Models & Schemas",
            "Non-Functional Requirements"        ]
        
        extracted_content = []
        lines = content.split('\n')
        current_section = None
        in_critical_section = False
        
        for line in lines:
            # Check if this is a section header
            if line.startswith('## '):
                section_name = line.replace('## ', '').strip()
                if section_name in critical_sections:
                    current_section = section_name
                    in_critical_section = True
                    extracted_content.append(f"\n{line}")
                else:
                    in_critical_section = False
            elif in_critical_section:
                extracted_content.append(line)
        
        return '\n'.join(extracted_content)
    
    elif content_type == "prd":
        # Critical sections for action plan generation
        critical_sections = [
            "User Requirements",
            "Product Overview"
        ]
        
        extracted_content = []
        lines = content.split('\n')
        current_section = None
        in_critical_section = False
        
        for line in lines:
            # Check if this is a section header
            if line.startswith('## '):
                section_name = line.replace('## ', '').strip()
                if section_name in critical_sections:
                    current_section = section_name
                    in_critical_section = True
                    extracted_content.append(f"\n{line}")
                else:
                    in_critical_section = False
            elif in_critical_section:
                extracted_content.append(line)
        
        return '\n'.join(extracted_content)
    
    return content

def extract_prd_user_requirements(prd_content):
    """Extract only the 'User Requirements' and 'Product Overview' sections from the PRD."""
    sections_to_keep = ["Product Overview", "User Requirements"]
    extracted = []
    lines = prd_content.split('\n')
    in_section = False
    for line in lines:
        if line.startswith('## '):
            section = line.replace('## ', '').strip()
            in_section = section in sections_to_keep
            if in_section:
                extracted.append(f"\n{line}")
        elif in_section:
            extracted.append(line)
    return '\n'.join(extracted)

def generate_action_plan(client, spec_content, prd_content=None):
    """Generate Action Plan using OpenAI API with template"""
    
    # Extract critical sections from tech spec
    critical_spec = extract_critical_sections(spec_content, "tech_spec")
    
    print(f"📊 Using critical sections only:")
    print(f"   Technical Spec: {len(spec_content.split())} words → {len(critical_spec.split())} words")
    if prd_content:
        prd_user_reqs = extract_prd_user_requirements(prd_content)
        print(f"   PRD: {len(prd_content.split())} words → {len(prd_user_reqs.split())} words (user requirements only)")
    else:
        prd_user_reqs = None
    
    # Load the action plan template
    template_path = Path(__file__).parent.parent / "templates" / "action_plan_template.md"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading template file: {e}")
        return None
    
    # Replace placeholders in template with critical sections only
    prompt = template_content.replace("{{SPEC_MD}}", critical_spec)
    
    if prd_user_reqs:
        prompt = prompt.replace("{{PRD_MD}}", prd_user_reqs)
    else:
        # If no PRD provided, use a placeholder
        prompt = prompt.replace("{{PRD_MD}}", "No PRD provided - using technical specification only.")
    
    # Replace product name placeholder
    prompt = prompt.replace("{{PRODUCT_NAME}}", "Product")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a pragmatic Technical Lead collaborating with a Senior Product Manager. Generate actionable, implementation-focused content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating Action Plan: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate Action Plan from Technical Specification markdown file')
    parser.add_argument('tech_spec_file', help='Path to Technical Specification markdown file')
    parser.add_argument('--prd-file', help='Path to PRD file for additional context (optional)')
    parser.add_argument('--output', default='output/action_plan.md', help='Output file path (default: output/action_plan.md)')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in a .env file or environment variable")
        sys.exit(1)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Read technical specification file
    try:
        with open(args.tech_spec_file, 'r', encoding='utf-8') as file:
            spec_content = file.read().strip()
    except FileNotFoundError:
        print(f"Error: Technical specification file '{args.tech_spec_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading technical specification file: {e}")
        sys.exit(1)
    
    # Read PRD file if provided
    prd_content = None
    if args.prd_file:
        try:
            with open(args.prd_file, 'r', encoding='utf-8') as file:
                prd_content = file.read().strip()
        except FileNotFoundError:
            print(f"Warning: PRD file '{args.prd_file}' not found, proceeding without PRD context")
        except Exception as e:
            print(f"Warning: Error reading PRD file: {e}, proceeding without PRD context")
    
    # Generate Action Plan
    print("Generating Action Plan...")
    action_plan_content = generate_action_plan(client, spec_content, prd_content)
    
    if not action_plan_content:
        print("Failed to generate Action Plan")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(action_plan_content)
        print(f"✅ Action Plan generated successfully: {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 