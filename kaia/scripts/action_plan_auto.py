from openai import OpenAI
import pandas as pd
import os
import argparse
from dotenv import load_dotenv
import importlib.resources

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate Action Plan from Technical Specification')
parser.add_argument('tech_spec_file', help='Path to the technical specification markdown file (required)')
parser.add_argument('--prd-file', help='Path to the PRD file for additional context (optional)')
parser.add_argument('--output', default='output/action_plan.md', help='Path to the output markdown file (default: output/action_plan.md)')
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

# Load technical specification
if not os.path.exists(args.tech_spec_file):
    raise SystemExit(f"❌ Technical specification file not found: {args.tech_spec_file}")

with open(args.tech_spec_file, "r") as f:
    tech_spec_content = f.read().strip()

# Load PRD if provided
prd_context = ""
if args.prd_file and os.path.exists(args.prd_file):
    with open(args.prd_file, "r") as f:
        prd_context = f.read().strip()

# Load the action plan template
def load_template():
    """Load the action plan template from the prompts directory"""
    try:
        # Try using importlib.resources first (Python 3.7+)
        with importlib.resources.files('kaia.prompts').joinpath('action_plan_template.md').open('r') as f:
            return f.read()
    except (ImportError, AttributeError):
        # Fallback for older Python versions or if package not installed
        template_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'action_plan_template.md')
        with open(template_path, 'r') as f:
            return f.read()

# Load template and replace placeholders
template = load_template()
prompt = template.replace("{{SPEC_MD}}", tech_spec_content).replace("{{PRD_MD}}", prd_context or "")

print("Generating Action Plan...")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

action_plan_content = response.choices[0].message.content

# Ensure output directory exists
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Write to markdown file
with open(args.output, "w") as out_file:
    out_file.write(action_plan_content)

print(f"\nAction Plan generated successfully: {args.output}") 