# PRD Automation Tool

A comprehensive automation tool that generates Product Requirements Documents (PRD), Technical Specifications, and Action Plans from CSV input files using OpenAI's GPT-4.

## Project Structure

```
prd_auto/
├── scripts/                    # Python automation scripts
│   ├── prd_auto.py            # Generate PRD from CSV input
│   ├── spec_auto.py           # Generate Technical Spec from PRD
│   ├── action_plan_auto.py    # Generate Action Plan from Technical Spec
│   └── master_auto.py         # Master script to run all three
├── output/                    # Generated documents (auto-created)
├── prd_instructions.csv       # PRD generation template
├── spec_instructions.csv      # Technical spec generation template
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd prd_auto

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 2. Run the Complete Pipeline

```bash
# Generate all documents from CSV input
python3 scripts/master_auto.py your_input.csv

# Or with custom version suffix
python3 scripts/master_auto.py your_input.csv --version v1

# Skip specific steps if you have existing files
python3 scripts/master_auto.py your_input.csv --skip-prd --skip-spec
```

### 3. Run Individual Scripts

```bash
# Generate PRD only
python3 scripts/prd_auto.py your_input.csv

# Generate Technical Spec from existing PRD
python3 scripts/spec_auto.py output/prd_20241201_143022.md

# Generate Action Plan from existing Technical Spec
python3 scripts/action_plan_auto.py output/technical_specification_20241201_143022.md --prd-file output/prd_20241201_143022.md
```

## Input Format

Create a CSV file with your product idea. Example:

```csv
Section,Role Emulated,Prompt Instruction,Output Format,Acceptance Criteria
Product Overview,Product Manager,"Create a comprehensive product overview for a social media analytics tool","Clear, concise overview with key value propositions","Includes problem statement, solution, and target audience"
User Requirements,UX Designer,"Define detailed user requirements and use cases","Structured list of user stories and requirements","Covers primary user personas and their needs"
```

## Output Files

All generated files are saved in the `output/` directory with timestamp-based versioning:

- `prd_YYYYMMDD_HHMMSS.md` - Product Requirements Document
- `technical_specification_YYYYMMDD_HHMMSS.md` - Technical Specification
- `action_plan_YYYYMMDD_HHMMSS.md` - Action Plan with setup checklist and TaskMaster prompt

## Features

- **Automated Pipeline**: Generate all documents in sequence
- **Version Control**: Automatic timestamp-based versioning
- **Flexible Input**: Support for any CSV-formatted product idea
- **Modular Design**: Run individual scripts or the complete pipeline
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

### Complete Pipeline
```bash
# Generate everything from a product idea
python3 scripts/master_auto.py my_product_idea.csv
```

### Individual Steps
```bash
# Just the PRD
python3 scripts/prd_auto.py my_product_idea.csv

# Technical spec from existing PRD
python3 scripts/spec_auto.py output/prd_20241201_143022.md

# Action plan from existing spec
python3 scripts/action_plan_auto.py output/technical_specification_20241201_143022.md
```

### Skip Steps
```bash
# Use existing PRD, generate spec and action plan
python3 scripts/master_auto.py my_product_idea.csv --skip-prd

# Use existing PRD and spec, generate only action plan
python3 scripts/master_auto.py my_product_idea.csv --skip-prd --skip-spec
```

## Next Steps

After generating your documents:

1. Review the PRD for completeness and accuracy
2. Use the Technical Specification to plan your architecture
3. Follow the Action Plan's setup checklist
4. Use the TaskMaster prompt to break down development tasks
5. Start with MVP features and iterate

## Troubleshooting

<<<<<<< HEAD
- **API Key Issues**: Ensure your `.env` file contains a valid OpenAI API key
- **Token Limits**: The scripts are optimized to handle large documents efficiently
- **File Not Found**: Make sure input files exist and paths are correct
- **Permission Errors**: Ensure you have write permissions for the output directory 
=======
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
- 
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
>>>>>>> 26849b9144910edc4054cd14e32893af59fd23ce
