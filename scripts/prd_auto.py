from openai import OpenAI
import pandas as pd
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate PRD from input file')
parser.add_argument('input_file', help='Path to the input text file containing the product idea')
parser.add_argument('--template', default='templates/prd_instructions.csv', help='Path to the PRD template CSV file (default: templates/prd_instructions.csv)')
parser.add_argument('--output', default='output/prd.md', help='Path to the output markdown file (default: output/prd.md)')
parser.add_argument('--validation-output', default='output/validation_tracking.md', help='Path to the validation tracking file (default: output/validation_tracking.md)')
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

# Load PRD template
df = pd.read_csv(args.template)

# Load raw product idea
with open(args.input_file, "r") as f:
    product_idea = f.read().strip()

# Start context with raw input
cumulative_context = f"Product Idea:\n{product_idea}"

# Store each output
section_outputs = {}

# Initialize validation tracking file
def init_validation_file(validation_file):
    """Initialize the validation tracking file."""
    os.makedirs(os.path.dirname(validation_file), exist_ok=True)
    with open(validation_file, "w") as f:
        f.write("# Technical Validation Tracking\n\n")
        f.write("This document tracks validation findings and corrections applied to the technical architecture.\n\n")
        f.write("## Validation Findings by Section\n\n")

def add_validation_finding(validation_file, section, finding):
    """Add a validation finding to the tracking file."""
    with open(validation_file, "a") as f:
        f.write(f"### {section}\n")
        f.write(f"{finding}\n\n")

# Initialize validation file
init_validation_file(args.validation_output)

# Iterate through each PRD section
for _, row in df.iterrows():
    section = row["Section"]
    role = row["Role Emulated"]
    prompt_instruction = row["Prompt Instruction"]
    output_format = row["Output Format"]
    acceptance = row["Acceptance Criteria"]

    # Build full prompt (include acceptance criteria for AI guidance but don't output them)
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

    # Store and extend context
    section_outputs[section] = output
    cumulative_context += f"\n\n--- {section} ---\n{output}"

    # Add validation finding if this is a validation section
    if "Validation" in section:
        add_validation_finding(args.validation_output, section, output)

    print(f"\n--- {section.upper()} COMPLETE ---\n")
    print(output)
    print("\n" + "="*60 + "\n")

# Ensure output directory exists
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Write to markdown file (without acceptance criteria)
with open(args.output, "w") as out_file:
    out_file.write("# Product Requirements Document (PRD)\n\n")
    out_file.write("This document outlines the product requirements and specifications.\n\n")
    
    for section, content in section_outputs.items():
        out_file.write(f"## {section}\n\n{content}\n\n")

# Add final sections to validation file
with open(args.validation_output, "a") as f:
    f.write("## Corrections Applied\n\n")
    f.write("*This section will be updated after post-generation corrections are applied.*\n\n")
    f.write("### Architecture Changes Made\n")
    f.write("- *Pending correction analysis*\n\n")
    f.write("### Validation Issues Resolved\n")
    f.write("- *Pending correction analysis*\n\n")
    f.write("### Remaining Open Issues\n")
    f.write("- *Pending correction analysis*\n")

print(f"✅ PRD generated: {args.output}")
print(f"✅ Validation tracking started: {args.validation_output}")
