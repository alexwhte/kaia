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
parser.add_argument('--template', default='prd_instructions.csv', help='Path to the PRD template CSV file (default: prd_instructions.csv)')
parser.add_argument('--output', default='full_prd_output.md', help='Path to the output markdown file (default: full_prd_output.md)')
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

# Iterate through each PRD section
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
    for section, content in section_outputs.items():
        out_file.write(f"## {section}\n\n{content}\n\n")
