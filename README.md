# Kaia: Automated Product Requirements & Technical Planning Tool

Kaia is a unified command-line tool that generates Product Requirements Documents (PRD), Technical Specifications, Action Plans, Milestone Specifications, and Go-To-Market Plans from your product idea using OpenAI's GPT-4.

## Overview

Kaia is designed as part of a broader automation pipeline that transforms product ideas into actionable development tasks:

1. **Product Idea** → **PRD** (business requirements and user needs)
2. **PRD** → **Technical Specification** (system architecture and technical requirements)
3. **Technical Specification** → **Action Plan** (implementation strategy and setup tasks)
4. **Technical Specification + Action Plan** → **Milestone Specifications** (detailed technical specs for each development phase)
5. **PRD** → **Go-To-Market Plan** (marketing strategy and launch planning)

This pipeline ensures that your product vision flows seamlessly from high-level requirements down to specific development tasks, with each step building on the previous one to maintain context and alignment.

## Project Structure

```
kaia/
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
│   └── gtm_instructions.csv   # GTM plan generation template
├── tests/                      # Test files
│   └── test_action_plan.py    # Action plan script tests
├── output/                    # Generated documents (auto-created)
│   └── archive/               # Historical versions of generated documents
├── old/                       # Legacy files and previous versions
├── kaia                       # Unified CLI entry point
├── run.sh                     # Alternative execution script
├── setup_alias.sh             # CLI alias setup script
├── requirements.txt           # Python dependencies
├── tuning.txt                 # AI model tuning parameters and notes
├── forager_ig_input.txt       # Example input file for Forager project
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
├── LICENSE                    # Project license
└── README.md                  # This file
```

## Quick Start

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd kaia

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Set up CLI alias (optional)
./setup_alias.sh
```

### Usage: The `kaia` Command

Kaia provides a single command with subcommands for each step of the workflow:

#### **Full Pipeline (default)**
```bash
./kaia "FridgeFlow: People waste food because they forget what’s in their fridge or when it expires. This mobile app will use image recognition and barcode scanning to track ingredients and suggest recipes. The app looks like a clean grocery dashboard with a “cook now” button that filters by what’s expiring soon."

```
- **Input:** Product idea as text OR you may link a txt file.
- **Output:** PRD, Technical Spec, Action Plan, Milestone Specs, and GTM Plan in the `output/` folder

#### **Generate PRD only**
```bash
./kaia prd "Build XYZ"
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

## Output Files

All generated files are saved in the `output/` directory with versioned naming:

- `prd_v1.md` - Product Requirements Document
- `tech_spec_v1.md` - Technical Specification
- `action_plan_v1.md` - Action Plan with setup checklist and milestones
- `milestone_specs_v1.md` - Detailed milestone specifications for developers
- `gtm_plan_v1.md` - Go-To-Market Plan

### Archive System

The `output/archive/` directory automatically stores historical versions of generated documents, allowing you to track changes and iterations over time. Each run creates timestamped versions for easy reference.

## Features

- **Unified CLI**: One command for the full pipeline or any step
- **Automated Pipeline**: Generate all documents in sequence
- **Version Control**: Automatic timestamp-based versioning with archive system
- **Flexible Input**: Support for any text-formatted product idea
- **Modular Design**: Run individual steps or the complete pipeline
- **Action Planning**: Includes setup checklists and milestone breakdown
- **Milestone Specifications**: Detailed technical specs for each development phase
- **Go-To-Market Planning**: Marketing strategy and launch planning
- **Clean Output**: Professional markdown formatting
- **Historical Tracking**: Automatic archiving of all generated documents

## Templates

The tool uses templates located in the `templates/` folder:

### CSV Templates
1. **templates/prd_instructions.csv** - Defines PRD sections and generation prompts
2. **templates/spec_instructions.csv** - Defines technical specification sections and prompts
3. **templates/gtm_instructions.csv** - Defines go-to-market plan sections and prompts

### Markdown Templates
4. **templates/action_plan_template.md** - Defines the action plan generation prompt with structured milestone markers
You can customize these templates to match your specific needs.

## Configuration

### Environment Variables

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Tuning Parameters
The `tuning.txt` file contains AI model parameters and notes for optimizing generation quality. You can modify these settings to adjust the output style and detail level.

## Dependencies
- Python 3.7+
- OpenAI Python client
- pandas
- python-dotenv

Install with: `pip install -r requirements.txt`

## Troubleshooting

- **API Key Issues**: Ensure your `.env` file contains a valid OpenAI API key
- **Token Limits**: The scripts are optimized to handle large documents efficiently
- **File Not Found**: Make sure input files exist and paths are correct
- **Permission Issues**: Ensure the CLI script is executable (`chmod +x kaia`)
- **Archive Issues**: Check that the `output/archive/` directory exists and is writable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
