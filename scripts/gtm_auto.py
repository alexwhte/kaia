#!/usr/bin/env python3
"""
GTM Auto - Generate Go-To-Market Plan from PRD and Technical Specification
Creates a comprehensive GTM strategy with SWOT analysis
"""

import os
import sys
import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def generate_gtm_plan(client, prd_content, tech_spec_content):
    """Generate Go-To-Market Plan using OpenAI API"""
    
    prompt = """You are an expert Product Marketing Manager creating a comprehensive Go-To-Market Plan.

PRD CONTENT:
{prd_content}

TECHNICAL SPECIFICATION:
{tech_spec_content}

Please create a detailed Go-To-Market Plan that includes:

## Go-To-Market Strategy
- Target audience segments (2-3 primary segments)
- Core positioning statement
- Key messaging pillars (3 main pillars)
- Launch tactics table with channel, tactic, KPI, and owner
- 30-60-90 day success metrics

## SWOT Analysis
- **Strengths** (internal advantages)
- **Weaknesses** (internal limitations)
- **Opportunities** (external factors to leverage)
- **Threats** (external challenges)
- Summary insights and differentiation strategy

## Competitive Positioning
- Competitive landscape overview
- Key differentiators
- Market positioning strategy

## Launch Timeline & Milestones
- Pre-launch activities
- Launch phases
- Post-launch optimization

Please provide a well-structured, actionable GTM plan that can guide marketing and business development efforts.""".format(prd_content=prd_content, tech_spec_content=tech_spec_content)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Product Marketing Manager and Competitive Intelligence Analyst with extensive experience in creating comprehensive Go-To-Market strategies. Focus on actionable insights, clear positioning, and measurable outcomes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating GTM Plan: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate Go-To-Market Plan from PRD and Technical Specification')
    parser.add_argument('prd_file', help='Path to PRD markdown file')
    parser.add_argument('tech_spec_file', help='Path to Technical Specification markdown file')
    parser.add_argument('-o', '--output', help='Output file path (default: output/gtm_plan.md)')
    
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
    
    # Read PRD file
    try:
        with open(args.prd_file, 'r', encoding='utf-8') as file:
            prd_content = file.read().strip()
    except FileNotFoundError:
        print(f"Error: PRD file '{args.prd_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading PRD file: {e}")
        sys.exit(1)
    
    # Read Technical Specification file
    try:
        with open(args.tech_spec_file, 'r', encoding='utf-8') as file:
            tech_spec_content = file.read().strip()
    except FileNotFoundError:
        print(f"Error: Technical specification file '{args.tech_spec_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading technical specification file: {e}")
        sys.exit(1)
    
    # Generate GTM Plan
    print("Generating Go-To-Market Plan...")
    gtm_content = generate_gtm_plan(client, prd_content, tech_spec_content)
    
    if not gtm_content:
        print("Failed to generate GTM Plan")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = "output/gtm_plan.md"
    
    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(gtm_content)
        print(f"Go-To-Market Plan generated successfully: {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 