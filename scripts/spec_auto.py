from openai import OpenAI
import pandas as pd
import os
import argparse
from dotenv import load_dotenv
import subprocess
import sys

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate Technical Specification from PRD file')
parser.add_argument('prd_file', help='Path to the PRD markdown file (required)')
parser.add_argument('--template', default='templates/spec_instructions.csv', help='Path to the technical spec template CSV file (default: templates/spec_instructions.csv)')
parser.add_argument('--output', default='output/tech_spec.md', help='Path to the output markdown file (default: output/tech_spec.md)')
parser.add_argument('--validation-file', default='output/validation_tracking.md', help='Path to the validation tracking file to update (default: output/validation_tracking.md)')
parser.add_argument('--product-idea', help='Path to original product idea file for additional context (optional)')
parser.add_argument('--generate-action-plan', action='store_true', help='Automatically generate action plan after technical specification')
args = parser.parse_args()

# Initialize OpenAI client with API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise SystemExit("❌ OPENAI_API_KEY not found in environment variables. Please set it in .env file")

client = OpenAI(api_key=api_key)

try:
    client.models.list()  # cheap call, raises if key/org invalid or no quota
except openai.AuthenticationError:
    raise SystemExit("❌ Invalid API key or no billing set up.")
except openai.RateLimitError:
    raise SystemExit("❌ API quota exhausted. Add credits in the dashboard.")

# Load technical spec template
df = pd.read_csv(args.template)

# Load PRD file (primary input)
if not os.path.exists(args.prd_file):
    raise SystemExit(f"❌ PRD file not found: {args.prd_file}")

with open(args.prd_file, "r") as f:
    prd_content = f.read().strip()

# Load original product idea if provided (for additional context)
product_idea_context = ""
if args.product_idea and os.path.exists(args.product_idea):
    with open(args.product_idea, "r") as f:
        product_idea_context = f.read().strip()

# Create base context with full PRD content
base_context = f"PRD Content:\n{prd_content}"

if product_idea_context:
    base_context += f"\n\nOriginal Product Idea:\n{product_idea_context}"

# Store each output
section_outputs = {}

# Define context dependencies for spec sections
context_dependencies = {
    "Purpose & Scope": [],  # No previous spec sections needed
    "High-Level Architecture Diagram": [],  # Based on PRD architecture
    "Data Flow & Sequence Diagrams": ["High-Level Architecture Diagram"],
    "Key Components": ["High-Level Architecture Diagram"],
    "External Integrations & APIs": ["Key Components"],
    "Data Models & Schemas": ["Key Components"],
    "Parsing & NLP Logic": ["Key Components", "Data Models & Schemas"],
    "Edge-Case & Error Handling": ["Key Components", "External Integrations & APIs"],
    "Non-Functional Requirements": ["Key Components"],
    "Security & Privacy": ["External Integrations & APIs", "Data Models & Schemas"],
    "Observability & Monitoring": ["Key Components", "Non-Functional Requirements"],
    "Testing & Validation Plan": ["Key Components", "Non-Functional Requirements"],
    "Implementation Roadmap": ["Key Components", "External Integrations & APIs"],
    "Open Questions & Assumptions": []  # Can reference any previous sections
}

def add_validation_finding(validation_file, section, finding):
    """Add a validation finding to the tracking file."""
    if os.path.exists(validation_file):
        with open(validation_file, "a") as f:
            f.write(f"### {section}\n")
            f.write(f"{finding}\n\n")
    else:
        print(f"⚠️  Validation file not found: {validation_file}")

# Iterate through each technical spec section
for _, row in df.iterrows():
    section = row["Section"]
    role = row["Role Emulated"]
    prompt_instruction = row["Prompt Instruction"]
    output_format = row["Output Format"]
    acceptance = row["Acceptance Criteria"]

    # Build context with base context and dependent sections
    dependent_sections = []
    if section in context_dependencies:
        for dep_section in context_dependencies[section]:
            if dep_section in section_outputs:
                dependent_sections.append(f"--- {dep_section} ---\n{section_outputs[dep_section]}")
    
    cumulative_context = base_context
    if dependent_sections:
        cumulative_context += f"\n\nDependent Sections:\n" + "\n\n".join(dependent_sections)

    # Build full prompt
    full_prompt = f"""{prompt_instruction}

{cumulative_context}

Format:
{output_format}

Acceptance Criteria:
{acceptance}
"""

    print(f"\nRunning section: {section}...\n")

    # Call OpenAI chat completion API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7
    )

    output = response.choices[0].message.content

    # Store output
    section_outputs[section] = output

    # Add validation finding if this is a validation section
    if "Validation" in section or "CTO" in section:
        add_validation_finding(args.validation_file, section, output)

    print(f"\n--- {section.upper()} COMPLETE ---\n")
    print(output)
    print("\n" + "="*60 + "\n")

# Ensure output directory exists
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Write to markdown file
with open(args.output, "w") as out_file:
    out_file.write("# Technical Specification\n\n")
    out_file.write("This document provides detailed technical specifications based on the Product Requirements Document (PRD).\n\n")
    
    for section, content in section_outputs.items():
        # Skip validation sections in the spec output - they go to validation file only
        if "Validation" in section or "CTO" in section:
            continue
        out_file.write(f"## {section}\n\n{content}\n\n")

# Generate action plan if requested
if args.generate_action_plan:
    print("\nGenerating Action Plan...")
    try:
        # Call the action plan script
        action_plan_cmd = [
            sys.executable, 'action_plan_auto.py',
            args.output,
            '--prd-file', args.prd_file,
            '--output', 'output/action_plan.md'
        ]
        
        if args.product_idea:
            action_plan_cmd.extend(['--product-idea', args.product_idea])
        
        result = subprocess.run(action_plan_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Action Plan generated successfully: output/action_plan.md")
        else:
            print(f"❌ Error generating action plan: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error generating action plan: {e}")

print(f"✅ Technical specification generated: {args.output}")
if os.path.exists(args.validation_file):
    print(f"✅ Validation findings added to: {args.validation_file}") 