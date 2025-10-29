#!/usr/bin/env python3
"""
Milestones Auto - Generate comprehensive milestone specifications from Technical Specification and Action Plan
Creates a single detailed milestone spec file for developers and AI agents
"""

import os
import sys
import argparse
import re
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def extract_milestones_from_action_plan(action_plan_content):
    """Extract milestone sections using structured markers"""
    milestones = []
    
    # Find all milestone sections using the markers
    pattern = r'<!-- MILESTONE_START -->(.*?)<!-- MILESTONE_END -->'
    matches = re.findall(pattern, action_plan_content, re.DOTALL)
    
    for i, match in enumerate(matches):
        milestone_content = match.strip()
        # Extract milestone name from the first line
        lines = milestone_content.split('\n')
        for line in lines:
            if line.startswith('## Milestone'):
                milestone_name = line.replace('## ', '').strip()
                break
        else:
            milestone_name = f"Milestone {i}"
        
        milestones.append({
            'name': milestone_name,
            'content': milestone_content
        })
    
    print(f"Total milestones extracted: {len(milestones)}")
    return milestones

def extract_critical_sections(content, content_type):
    """Extract only the most critical sections for milestone generation"""
    
    if content_type == "tech_spec":
        # Minimal set for unique, testable milestones
        critical_sections = [
            "Key Components",
            "Data Flow & Sequence Diagrams",
            "Data Models & Schemas",
            "Implementation Roadmap"
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
    
    elif content_type == "prd":
        # Minimal set for unique, testable milestones
        critical_sections = [
            "User Requirements"
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

def generate_comprehensive_milestone_specs(client, tech_spec_content, prd_content):
    """Generate comprehensive milestone specifications using OpenAI API"""
    
    # Extract only critical sections to reduce token usage
    critical_tech_spec = extract_critical_sections(tech_spec_content, "tech_spec")
    critical_prd = extract_critical_sections(prd_content, "prd")
    
    print(f"📊 Token optimization:")
    print(f"   Technical Spec: {len(tech_spec_content.split())} words → {len(critical_tech_spec.split())} words")
    print(f"   PRD: {len(prd_content.split())} words → {len(critical_prd.split())} words")
    
    prompt = f"""You are an expert Technical Lead creating milestone specifications for developers.

TECHNICAL SPECIFICATION:
{critical_tech_spec}

PRODUCT REQUIREMENTS:
{critical_prd}

Create 3-6 logical development milestones with this structure for each:

## [MILESTONE_NAME]

### Technical Requirements
- API endpoints and data models
- Database schema changes
- Integration points

### Implementation Guide
- Step-by-step implementation
- Code structure decisions
- Error handling

### Testing & Validation
- Unit test requirements
- Integration test scenarios
- Acceptance criteria

### Dependencies & Prerequisites
- External services and APIs
- Internal system dependencies

Focus on WHAT to build and HOW to build it. Make each milestone actionable for developers."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert software architect creating detailed, actionable milestone specifications for development teams. Focus on specific technical implementation details and clear, step-by-step guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating milestone specifications: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive milestone specifications from Technical Specification and PRD')
    parser.add_argument('tech_spec_file', help='Path to Technical Specification markdown file')
    parser.add_argument('--prd-file', help='Path to PRD file (optional)')
    parser.add_argument('--milestone', help='Specific milestone to generate (e.g., "Milestone 1 - Core Authentication")')
    parser.add_argument('--description', help='Description for the milestone (required if --milestone is used)')
    parser.add_argument('-o', '--output', default='output/milestone_specs.md', 
                       help='Output file path (default: output/milestone_specs.md)')
    parser.add_argument('--split-files', action='store_true', 
                       help='Split into individual milestone files (future enhancement)')
    
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
            tech_spec_content = file.read().strip()
    except FileNotFoundError:
        print(f"Error: Technical specification file '{args.tech_spec_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading technical specification file: {e}")
        sys.exit(1)
    
    # Determine PRD content
    if args.prd_file:
        try:
            with open(args.prd_file, 'r', encoding='utf-8') as file:
                prd_content = file.read().strip()
        except FileNotFoundError:
            print(f"Error: PRD file '{args.prd_file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading PRD file: {e}")
            sys.exit(1)
    else:
        # Use minimal context if no PRD provided
        prd_content = """
## Product Overview
Basic product requirements for milestone generation.

## User Requirements
Core user needs and functionality requirements.
"""
    
    # Generate comprehensive milestone specifications
    print("Generating comprehensive milestone specifications...")
    
    milestone_specs = generate_comprehensive_milestone_specs(
        client, 
        tech_spec_content, 
        prd_content
    )
    
    if not milestone_specs:
        print("Failed to generate milestone specifications")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write milestone specifications
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(milestone_specs)
        print(f"✅ Generated comprehensive milestone specifications: {output_path}")
    except Exception as e:
        print(f"Error writing milestone specifications: {e}")
        sys.exit(1)
    
    print(f"\n🎉 Milestone specifications generated successfully!")
    print(f"📁 Output file: {output_path}")
    
    if args.split_files:
        print("⚠️  File splitting feature not yet implemented. Use the single comprehensive file for now.")

if __name__ == "__main__":
    main() 