from openai import OpenAI
import pandas as pd
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate Technical Specification from PRD file')
parser.add_argument('prd_file', help='Path to the PRD markdown file (required)')
parser.add_argument('--template', default='spec_instructions.csv', help='Path to the technical spec template CSV file (default: spec_instructions.csv)')
parser.add_argument('--output', default='technical_specification.md', help='Path to the output markdown file (default: technical_specification.md)')
parser.add_argument('--product-idea', help='Path to original product idea file for additional context (optional)')
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

# Start context with PRD content (primary) and product idea (secondary)
cumulative_context = f"PRD Content:\n{prd_content}"
if product_idea_context:
    cumulative_context += f"\n\nOriginal Product Idea:\n{product_idea_context}"

# Store each output
section_outputs = {}

# Iterate through each technical spec section
for _, row in df.iterrows():
    section = row["Section"]
    role = row["Role Emulated"]
    prompt_instruction = row["Prompt Instruction"]
    output_format = row["Output Format"]
    acceptance = row["Acceptance Criteria"]

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

    # Store and extend context
    section_outputs[section] = output
    cumulative_context += f"\n\n--- {section} ---\n{output}"

    print(f"\n--- {section.upper()} COMPLETE ---\n")
    print(output)
    print("\n" + "="*60 + "\n")

# Write to markdown file
with open(args.output, "w") as out_file:
    out_file.write("# Technical Specification\n\n")
    out_file.write("This document provides detailed technical specifications based on the Product Requirements Document (PRD).\n\n")
    
    for section, content in section_outputs.items():
        out_file.write(f"## {section}\n\n{content}\n\n") 