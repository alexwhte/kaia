# Kaia: Automated Product Requirements & Technical Planning Tool

Kaia is a unified command-line tool that generates Product Requirements Documents (PRD), Technical Specifications, and Action Plans from your product idea using OpenAI's GPT-4.

## Overview

Kaia is designed as part of a broader automation pipeline that transforms product ideas into actionable development tasks:

1. **Product Idea** → **PRD** (business requirements and user needs)
2. **PRD** → **Technical Specification** (system architecture and technical requirements)
3. **Technical Specification** → **Action Plan** (implementation strategy and setup tasks)
4. **Action Plan** → **TaskMaster** (detailed task breakdown for development teams)
5. **TaskMaster** → **Cursor/Development Tools** (code generation and implementation)

This pipeline ensures that your product vision flows seamlessly from high-level requirements down to specific development tasks, with each step building on the previous one to maintain context and alignment.

## Project Structure

```
kaia/
├── scripts/                    # Python automation scripts
│   ├── prd_auto.py            # Generate PRD from text input
│   ├── spec_auto.py           # Generate Technical Spec from PRD
│   ├── action_plan_auto.py    # Generate Action Plan from Technical Spec
│   └── master_auto.py         # Master script to run all three
├── output/                    # Generated documents (auto-created)
├── prd_instructions.csv       # PRD generation template
├── spec_instructions.csv      # Technical spec generation template
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
├── kaia                       # Unified CLI entry point
└── README.md                  # This file
```

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd kaia

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 2. Usage: The `kaia` Command

Kaia provides a single command with subcommands for each step of the workflow:

#### **Full Pipeline (default)**
```bash
./kaia your_product_idea.txt
# or
./kaia all your_product_idea.txt
```
- **Input:** Text file with your product idea
- **Output:** PRD, Technical Spec, and Action Plan in the `output/` folder

#### **Generate PRD only**
```bash
./kaia prd your_product_idea.txt
```
- **Input:** Text file with your product idea
- **Output:** PRD markdown file in `output/`

#### **Generate Technical Spec only**
```bash
./kaia spec output/prd_YYYYMMDD_HHMMSS.md
```
- **Input:** PRD markdown file (generated from previous step)
- **Output:** Technical Specification markdown file in `output/`

#### **Generate Action Plan only**
```bash
./kaia action output/technical_specification_YYYYMMDD_HHMMSS.md --prd-file output/prd_YYYYMMDD_HHMMSS.md
```
- **Input:** Technical Specification markdown file (required), PRD markdown file (optional for extra context)
- **Output:** Action Plan markdown file in `output/`

#### **Options for All Commands**
- `--version v1` — Add a custom version suffix to output files
- `--skip-prd`, `--skip-spec`, `--skip-action-plan` — Skip steps (for `all` pipeline only)

### 3. Input Format

Create a text file with your product idea. Example:

```
A social media analytics tool that helps small businesses understand their audience 
and optimize their content strategy. The tool should analyze engagement patterns, 
identify trending topics, and provide actionable insights for content creation.
```

### 4. Output Files

All generated files are saved in the `output/` directory with timestamp-based versioning:

- `prd_YYYYMMDD_HHMMSS.md` - Product Requirements Document
- `technical_specification_YYYYMMDD_HHMMSS.md` - Technical Specification
- `action_plan_YYYYMMDD_HHMMSS.md` - Action Plan with setup checklist and TaskMaster prompt

## Features

- **Unified CLI**: One command for the full pipeline or any step
- **Automated Pipeline**: Generate all documents in sequence
- **Version Control**: Automatic timestamp-based versioning
- **Flexible Input**: Support for any text-formatted product idea
- **Modular Design**: Run individual steps or the complete pipeline
- **Action Planning**: Includes setup checklists and TaskMaster integration
- **Clean Output**: Professional markdown formatting

## Templates

The tool uses two CSV templates:

1. **prd_instructions.csv** - Defines PRD sections and generation prompts
2. **spec_instructions.csv** - Defines technical specification sections and prompts

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
./kaia my_product_idea.txt
```

### Individual Steps
```bash
./kaia prd my_product_idea.txt
./kaia spec output/prd_YYYYMMDD_HHMMSS.md
./kaia action output/technical_specification_YYYYMMDD_HHMMSS.md
```

### Skip Steps (Pipeline Only)
```bash
./kaia all my_product_idea.txt --skip-prd
./kaia all my_product_idea.txt --skip-prd --skip-spec
```

## Next Steps

After generating your documents:

1. Review the PRD for completeness and accuracy
2. Use the Technical Specification to plan your architecture
3. Follow the Action Plan's setup checklist
4. Use the TaskMaster prompt to break down development tasks
5. Start with MVP features and iterate

## Troubleshooting

- **API Key Issues**: Ensure your `.env` file contains a valid OpenAI API key
- **Token Limits**: The scripts are optimized to handle large documents efficiently
- **File Not Found**: Make sure input files exist and paths are correct
- **Permission Errors**: Ensure you have write permissions for the output directory

## Output

All generated files are saved to the `output/` folder by default with automatic versioning.

### PRD Output
The PRD tool generates a markdown file containing a complete PRD with the following sections:
- Product Overview
- Market Context
- Users
- User Requirements
- Metrics & KPIs
- High-Level Technical Architecture
- Go-To-Market
- Appendix (SWOT Analysis and Competitor Analysis)

### Technical Specification Output
The technical specification tool generates a detailed technical document based on the PRD with the following sections:
- Purpose & Scope
- High-Level Architecture Diagram
- Data Flow & Sequence Diagrams
- Key Components
- External Integrations & APIs
- Data Models & Schemas
- Parsing & NLP Logic
- Edge-Case & Error Handling
- Non-Functional Requirements
- Security & Privacy
- Observability & Monitoring
- Testing & Validation Plan
- Implementation Roadmap
- Open Questions & Assumptions

### Action Plan Output
The action plan tool generates a practical implementation guide with:
- Initial Setup Checklist (API keys, environment setup, etc.)
- MVP vs Non-MVP Breakdown
- TaskMaster Prompt for development task breakdown
- Next Steps for the development team

### Generation Summary
The master script creates a JSON summary file containing:
- Timestamp of generation
- Input file used
- Output directory
- Generated file paths and versions
- Metadata for tracking

## Key Improvements

### Notion Compatibility
- **Proper formatting**: Key components use sub-bullets for better Notion import
- **Clean structure**: Avoids formatting issues when copying to Notion

### Visual Diagrams
- **Mermaid syntax**: Proper sequence diagrams that render correctly
- **ASCII architecture**: Clear visual representation of system components

### MVP Focus
- **Implementation Roadmap**: Maps PRD requirements to technical implementation
- **MVP prioritization**: Clear distinction between essential and future features
- **Actionable subtasks**: Specific technical tasks for each requirement

### TaskMaster Integration
- **Ready-to-use prompts**: Generated prompts for [TaskMaster](https://www.task-master.dev/)
- **Development task breakdown**: Structured for team collaboration
- **Dependency mapping**: Clear task relationships and priorities

### Versioning & Automation
- **Automatic versioning**: Each run creates new versioned files
- **Master script**: One command generates all documents
- **Flexible workflow**: Can skip steps or use existing files
- **Generation tracking**: JSON summaries for audit trail

### Tone & Readability
- **More approachable language**: Removed overly formal terms like "aforementioned"
- **Bullet points**: Used for better readability in scope sections
- **Succinct content**: Focused on essential information without overwhelming detail
- **Confident but friendly tone**: Makes technical content more engaging

## Development Notes

### Python Command Usage
- This project requires Python 3
- On macOS, use `python3` instead of `python`
- For convenience, you can use the alias `p` (e.g., `p master_auto.py input.txt`)
- To set up the alias, add this line to your `~/.zshrc`:
  ```bash
  alias p="python3"
  ```

### Template Customization
All scripts use CSV template files that define the structure and prompts for each section. You can customize these templates by:
1. Modifying the existing `prd_instructions.csv` or `spec_instructions.csv` files
2. Creating new template files and specifying them with the `--template` argument

### Workflow Notes
- The technical specification is designed to be generated **after** the PRD
- The PRD file serves as the primary input for the technical specification
- The original product idea can be provided as additional context for the technical specification
- This ensures the technical specification is fully aligned with the approved PRD requirements
- All output files are automatically saved to the `output/` folder with versioning
- The action plan provides immediate next steps for development teams
- TaskMaster integration enables seamless transition from planning to execution
- The master script provides a complete automation workflow with versioning 
