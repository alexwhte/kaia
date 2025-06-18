from openai import OpenAI
import pandas as pd
import os
import argparse
from dotenv import load_dotenv

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

# Parse technical spec to extract key sections
def extract_spec_sections(spec_content):
    """Extract key sections from technical spec content"""
    sections = {}
    current_section = None
    current_content = []
    
    lines = spec_content.split('\n')
    for line in lines:
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

# Parse PRD to extract key sections
def extract_prd_sections(prd_content):
    """Extract key sections from PRD content"""
    sections = {}
    current_section = None
    current_content = []
    
    lines = prd_content.split('\n')
    for line in lines:
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

spec_sections = extract_spec_sections(tech_spec_content)

# Define key sections for action plan context (most important for planning)
key_spec_sections = [
    "Purpose & Scope",
    "Key Components", 
    "External Integrations & APIs",
    "Implementation Roadmap",
    "Open Questions & Assumptions"
]

# Create focused context with only key sections
base_context_parts = []
for section in key_spec_sections:
    if section in spec_sections:
        base_context_parts.append(f"Technical Spec {section}:\n{spec_sections[section]}")

base_context = "\n\n".join(base_context_parts)

# Add key PRD sections if available
if prd_context:
    prd_sections = extract_prd_sections(prd_context)
    
    # Define key PRD sections for action planning
    key_prd_sections = [
        "Product Overview",
        "User Requirements",
        "Metrics & KPIs"
    ]
    
    prd_context_parts = []
    for section in key_prd_sections:
        if section in prd_sections:
            prd_context_parts.append(f"PRD {section}:\n{prd_sections[section]}")
    
    if prd_context_parts:
        base_context += f"\n\nPRD Context:\n" + "\n\n".join(prd_context_parts)

# Generate Initial Setup Checklist
setup_prompt = f"""You are a Technical Project Manager creating an **Initial Setup Checklist** for a development team.

Based on the technical specification provided, create a comprehensive checklist of setup tasks that need to be completed before development begins.

Include:
• API keys and accounts needed
• Development environment setup
• Database setup
• External service configurations
• Team access and permissions
• Development tools and licenses

Format as a clear checklist with categories. Focus on actionable items that can be completed by the team.

Context:
{base_context}"""

print("Generating Initial Setup Checklist...")

setup_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": setup_prompt}],
    temperature=0.7
)

setup_checklist = setup_response.choices[0].message.content

# Generate TaskMaster Prompt
taskmaster_prompt = f"""You are creating a prompt for TaskMaster (https://www.task-master.dev/) to break down a technical specification into actionable development tasks.

Based on the technical specification provided, create a comprehensive TaskMaster prompt that will:
1. Break down the technical specification into manageable development tasks
2. Prioritize tasks by MVP vs non-MVP
3. Identify dependencies between tasks
4. Suggest appropriate task sizes and complexity
5. Include technical details needed for implementation

The prompt should be structured to work with TaskMaster's capabilities and should help the team create a detailed project plan.

Context:
{base_context}"""

print("Generating TaskMaster Prompt...")

taskmaster_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": taskmaster_prompt}],
    temperature=0.7
)

taskmaster_prompt_content = taskmaster_response.choices[0].message.content

# Generate MVP vs Non-MVP Breakdown
mvp_prompt = f"""You are a Technical Product Manager creating an **MVP vs Non-MVP Breakdown** for development planning.

Based on the technical specification provided, create a clear breakdown of:
1. **MVP Features** - Essential features needed for a working product
2. **Phase 2 Features** - Important but not critical for initial launch
3. **Future Enhancements** - Nice-to-have features for later iterations

For each feature, briefly explain why it's categorized as MVP or not.

Focus on helping the team understand what to build first vs what can come later.

Context:
{base_context}"""

print("Generating MVP Breakdown...")

mvp_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": mvp_prompt}],
    temperature=0.7
)

mvp_breakdown = mvp_response.choices[0].message.content

# Ensure output directory exists
os.makedirs(os.path.dirname(args.output), exist_ok=True)

# Write to markdown file
with open(args.output, "w") as out_file:
    out_file.write("# Action Plan\n\n")
    out_file.write("This document provides actionable next steps for implementing the technical specification.\n\n")
    
    out_file.write("## Initial Setup Checklist\n\n")
    out_file.write("Complete these tasks before starting development:\n\n")
    out_file.write(setup_checklist)
    out_file.write("\n\n")
    
    out_file.write("## MVP vs Non-MVP Breakdown\n\n")
    out_file.write(mvp_breakdown)
    out_file.write("\n\n")
    
    out_file.write("## TaskMaster Prompt\n\n")
    out_file.write("Use this prompt with [TaskMaster](https://www.task-master.dev/) to break down the technical specification into actionable development tasks:\n\n")
    out_file.write("```\n")
    out_file.write(taskmaster_prompt_content)
    out_file.write("\n```\n\n")
    
    out_file.write("## Next Steps\n\n")
    out_file.write("1. Complete the Initial Setup Checklist\n")
    out_file.write("2. Use the TaskMaster prompt to create detailed development tasks\n")
    out_file.write("3. Prioritize MVP features for the first development sprint\n")
    out_file.write("4. Set up development environment and begin implementation\n")

print(f"\nAction Plan generated successfully: {args.output}") 