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

- **API Key Issues**: Ensure your `.env` file contains a valid OpenAI API key
- **Token Limits**: The scripts are optimized to handle large documents efficiently
- **File Not Found**: Make sure input files exist and paths are correct
- **Permission Errors**: Ensure you have write permissions for the output directory 