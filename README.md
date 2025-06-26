# PRD Auto: Automated Product Requirements & Technical Planning Tool

PRD Auto is a unified command-line tool that generates Product Requirements Documents (PRD), Technical Specifications, Action Plans, Milestone Specifications, and Go-To-Market Plans from your product idea using OpenAI's GPT-4.

## Overview

PRD Auto is designed as part of a broader automation pipeline that transforms product ideas into actionable development tasks:

1. **Product Idea** → **PRD** (business requirements and user needs)
2. **PRD** → **Technical Specification** (system architecture and technical requirements)
3. **Technical Specification** → **Action Plan** (implementation strategy and setup tasks)
4. **Technical Specification + Action Plan** → **Milestone Specifications** (detailed technical specs for each development phase)
5. **PRD** → **Go-To-Market Plan** (marketing strategy and launch planning)

This pipeline ensures that your product vision flows seamlessly from high-level requirements down to specific development tasks, with each step building on the previous one to maintain context and alignment.

## Project Structure

```
prd_auto/
├── scripts/                    # Python automation scripts
│   ├── prd_auto.py            # Generate PRD from text input
│   ├── spec_auto.py           # Generate Technical Spec from PRD
│   ├── action_plan_auto.py    # Generate Action Plan from Technical Spec
│   ├── milestones_auto.py     # Generate Milestone Specifications
│   ├── gtm_auto.py            # Generate Go-To-Market Plan
│   └── master_auto.py         # Master script to run all five
├── templates/                  # Templates and instructions
│   ├── prd_instructions.csv   # PRD generation template
│   ├── spec_instructions.csv  # Technical spec generation template
│   └── action_plan_template.md # Action plan generation template
├── tests/                      # Test files
│   └── test_action_plan.py    # Action plan script tests
├── kaia                        # Unified CLI entry point
├── output/                    # Generated documents (auto-created)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Quick Start

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd prd_auto

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Set up CLI alias (optional)
./setup_alias.sh
```

### Usage: The `kaia` Command

PRD Auto provides a single command with subcommands for each step of the workflow:

#### **Full Pipeline (default)**
```bash
./kaia "Build a social media app for photographers"
# or
./kaia all "Build a social media app for photographers"
```
- **Input:** Product idea as text
- **Output:** PRD, Technical Spec, Action Plan, Milestone Specs, and GTM Plan in the `output/` folder

#### **Generate PRD only**
```bash
./kaia prd "Build a social media app for photographers"
```
- **Input:** Product idea as text
- **Output:** PRD markdown file in `output/`

#### **Generate Technical Spec only**
```bash
./kaia techspec output/prd_v1.md
```
- **Input:** PRD markdown file (generated from previous step)
- **Output:** Technical Specification markdown file in `output/`

#### **Generate Action Plan only**
```bash
./kaia actionplan output/tech_spec_v1.md --prd-file output/prd_v1.md
```
- **Input:** Technical Specification markdown file (required), PRD markdown file (optional for extra context)
- **Output:** Action Plan markdown file in `output/`

#### **Generate Milestone Specifications only**
```bash
./kaia milestones output/tech_spec_v1.md --action-plan-file output/action_plan_v1.md
```
- **Input:** Technical Specification markdown file (required), Action Plan markdown file (optional)
- **Output:** Comprehensive milestone specifications markdown file in `output/`

#### **Generate Go-To-Market Plan only**
```bash
./kaia gtm output/prd_v1.md
```
- **Input:** PRD markdown file
- **Output:** Go-To-Market Plan markdown file in `output/`

#### **Options for All Commands**
- `--version 1` — Add a custom version suffix to output files
- `--skip-prd`, `--skip-spec`, `--skip-action-plan`, `--skip-milestones`, `--skip-gtm` — Skip steps (for `all` pipeline only)

### Run Individual Scripts

```bash
# Generate PRD only
./kaia prd "Build a social media app for photographers"

# Generate Technical Spec from existing PRD
./kaia techspec output/prd_v1.md

# Generate Action Plan from existing Technical Spec
./kaia actionplan output/tech_spec_v1.md --prd-file output/prd_v1.md

# Generate Milestone Specifications
./kaia milestones output/tech_spec_v1.md --action-plan-file output/action_plan_v1.md

# Generate Go-To-Market Plan
./kaia gtm output/prd_v1.md
```

## Output Files

All generated files are saved in the `output/` directory with versioned naming:

- `prd_v1.md` - Product Requirements Document
- `tech_spec_v1.md` - Technical Specification
- `action_plan_v1.md` - Action Plan with setup checklist and milestones
- `milestone_specs_v1.md` - Detailed milestone specifications for developers
- `gtm_plan_v1.md` - Go-To-Market Plan

## Features

- **Unified CLI**: One command for the full pipeline or any step
- **Automated Pipeline**: Generate all documents in sequence
- **Version Control**: Automatic timestamp-based versioning
- **Flexible Input**: Support for any text-formatted product idea
- **Modular Design**: Run individual steps or the complete pipeline
- **Action Planning**: Includes setup checklists and milestone breakdown
- **Milestone Specifications**: Detailed technical specs for each development phase
- **Go-To-Market Planning**: Marketing strategy and launch planning
- **Clean Output**: Professional markdown formatting

## Templates

The tool uses templates located in the `templates/` folder:

### CSV Templates
1. **templates/prd_instructions.csv** - Defines PRD sections and generation prompts
2. **templates/spec_instructions.csv** - Defines technical specification sections and prompts

### Markdown Templates
3. **templates/action_plan_template.md** - Defines the action plan generation prompt with structured milestone markers

You can customize these templates to match your specific needs.

## Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Dependencies

- Python 3.7+
- OpenAI Python client
- pandas
- python-dotenv

Install with: `pip install -r requirements.txt`

## Usage Examples

### Full Pipeline
```bash
./kaia "Build a social media app for photographers"
```

### Individual Steps
```bash
./kaia prd "Build a social media app for photographers"
./kaia techspec output/prd_v1.md
./kaia actionplan output/tech_spec_v1.md --prd-file output/prd_v1.md
./kaia milestones output/tech_spec_v1.md --action-plan-file output/action_plan_v1.md
./kaia gtm output/prd_v1.md
```

### Skip Steps (Pipeline Only)
```bash
./kaia all "Build a social media app for photographers" --skip-gtm
./kaia all "Build a social media app for photographers" --skip-prd --skip-spec
```

## Next Steps

After generating your documents:

1. Review the PRD for completeness and accuracy
2. Use the Technical Specification to plan your architecture
3. Follow the Action Plan's setup checklist
4. Use the Milestone Specifications for detailed development planning
5. Implement the Go-To-Market Plan for launch strategy
6. Start with MVP features and iterate

## Troubleshooting

- **API Key Issues**: Ensure your `.env` file contains a valid OpenAI API key
- **Token Limits**: The scripts are optimized to handle large documents efficiently
- **File Not Found**: Make sure input files exist and paths are correct
- **Permission Issues**: Ensure the CLI script is executable (`chmod +x kaia`)
