# PRD & Technical Specification Automation Tool

A command-line tool that automatically generates Product Requirement Documents (PRDs) and Technical Specifications using OpenAI's GPT-4.

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

### Step 1: Generate PRD

First, run the PRD script with an input file containing your product idea:

```bash
python3 prd_auto.py path/to/your/input.txt
```

> **Note**: This project uses Python 3. On macOS, use `python3` instead of `python`. For convenience, you can use the alias `p` if you've set it up in your shell configuration.

Optional arguments:
- `--template`: Path to a custom PRD template CSV file (default: prd_instructions.csv)
- `--output`: Path to save the output markdown file (default: full_prd_output.md)

Example:
```bash
python3 prd_auto.py my_product_idea.txt --template custom_template.csv --output my_prd.md
```

### Step 2: Generate Technical Specification

After generating the PRD, run the technical specification script using the PRD file as input:

```bash
python3 spec_auto.py path/to/your/prd.md
```

Optional arguments:
- `--template`: Path to a custom technical spec template CSV file (default: spec_instructions.csv)
- `--output`: Path to save the output markdown file (default: technical_specification.md)
- `--product-idea`: Path to original product idea file for additional context (optional)

Example:
```bash
python3 spec_auto.py my_prd.md --product-idea my_product_idea.txt --output my_tech_spec.md
```

### Complete Workflow Example

```bash
# Step 1: Generate PRD
python3 prd_auto.py forager_ig_input.txt --output prd.md

# Step 2: Generate Technical Specification based on PRD
python3 spec_auto.py prd.md --product-idea forager_ig_input.txt --output tech_spec.md
```

## Input File Format

The input file should contain a clear description of your product idea. The tool will use this as the foundation for generating the PRD, and then the PRD will be used as the primary input for the technical specification.

## Output

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
- Release & Roll-out Strategy
- Open Questions & Assumptions
- Glossary

## Development Notes

### Python Command Usage
- This project requires Python 3
- On macOS, use `python3` instead of `python`
- For convenience, you can use the alias `p` (e.g., `p prd_auto.py input.txt`)
- To set up the alias, add this line to your `~/.zshrc`:
  ```bash
  alias p="python3"
  ```

### Template Customization
Both scripts use CSV template files that define the structure and prompts for each section. You can customize these templates by:
1. Modifying the existing `prd_instructions.csv` or `spec_instructions.csv` files
2. Creating new template files and specifying them with the `--template` argument

### Workflow Notes
- The technical specification is designed to be generated **after** the PRD
- The PRD file serves as the primary input for the technical specification
- The original product idea can be provided as additional context for the technical specification
- This ensures the technical specification is fully aligned with the approved PRD requirements 