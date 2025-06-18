# PRD & Technical Specification Automation Tool

A command-line tool that automatically generates Product Requirement Documents (PRDs), Technical Specifications, and Action Plans using OpenAI's GPT-4.

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Option 1: Master Script (Recommended)

Generate all documents with one command, including automatic versioning:

```bash
python3 master_auto.py path/to/your/input.txt
```

> **Note**: This project uses Python 3. On macOS, use `python3` instead of `python`. For convenience, you can use the alias `p` if you've set it up in your shell configuration.

#### Master Script Options:

```bash
# Basic usage with auto-versioning
python3 master_auto.py forager_ig_input.txt

# Custom output directory
python3 master_auto.py forager_ig_input.txt --output-dir my_outputs

# Skip action plan generation
python3 master_auto.py forager_ig_input.txt --skip-action-plan

# Use custom templates
python3 master_auto.py forager_ig_input.txt --prd-template custom_prd.csv --spec-template custom_spec.csv

# Skip PRD generation and use existing file
python3 master_auto.py forager_ig_input.txt --skip-prd --existing-prd output/prd_v1.md

# Skip technical spec generation and use existing file
python3 master_auto.py forager_ig_input.txt --skip-spec --existing-spec output/technical_specification_v1.md
```

#### Versioning System:

The master script automatically versions all output files:
- `prd_v1.md`, `prd_v2.md`, etc.
- `technical_specification_v1.md`, `technical_specification_v2.md`, etc.
- `action_plan_v1.md`, `action_plan_v2.md`, etc.
- `generation_summary_v1.json`, `generation_summary_v2.json`, etc.

### Option 2: Individual Scripts

You can still run each script individually for more control:

#### Step 1: Generate PRD

```bash
python3 prd_auto.py path/to/your/input.txt
```

Optional arguments:
- `--template`: Path to a custom PRD template CSV file (default: prd_instructions.csv)
- `--output`: Path to save the output markdown file (default: output/prd.md)

Example:
```bash
python3 prd_auto.py my_product_idea.txt --template custom_template.csv --output output/my_prd.md
```

#### Step 2: Generate Technical Specification

```bash
python3 spec_auto.py path/to/your/prd.md
```

Optional arguments:
- `--template`: Path to a custom technical spec template CSV file (default: spec_instructions.csv)
- `--output`: Path to save the output markdown file (default: output/technical_specification.md)
- `--product-idea`: Path to original product idea file for additional context (optional)
- `--generate-action-plan`: Automatically generate action plan after technical specification

Example:
```bash
python3 spec_auto.py output/prd.md --product-idea my_product_idea.txt --generate-action-plan
```

#### Step 3: Generate Action Plan (Optional)

```bash
python3 action_plan_auto.py path/to/your/tech_spec.md --prd-file path/to/your/prd.md
```

Optional arguments:
- `--prd-file`: Path to PRD file for additional context (optional)
- `--output`: Path to save the output markdown file (default: output/action_plan.md)

### Complete Workflow Examples

#### Using Master Script (Recommended):
```bash
# Generate everything with one command
python3 master_auto.py forager_ig_input.txt
```

#### Using Individual Scripts:
```bash
# Step 1: Generate PRD
python3 prd_auto.py forager_ig_input.txt

# Step 2: Generate Technical Specification and Action Plan
python3 spec_auto.py output/prd.md --product-idea forager_ig_input.txt --generate-action-plan
```

## Input File Format

The input file should contain a clear description of your product idea. The tool will use this as the foundation for generating the PRD, and then the PRD will be used as the primary input for the technical specification.

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

### Tone & Readability
- **More approachable language**: Removed overly formal terms like "aforementioned"
- **Bullet points**: Used for better readability in scope sections
- **Succinct content**: Focused on essential information without overwhelming detail
- **Confident but friendly tone**: Makes technical content more engaging

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