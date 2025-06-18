# PRD Automation Tool

A command-line tool that automatically generates Product Requirement Documents (PRDs) using OpenAI's GPT-4.

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

Run the script with an input file containing your product idea:

```bash
python prd_auto.py path/to/your/input.txt
```

Optional arguments:
- `--template`: Path to a custom PRD template CSV file (default: prd_instructions.csv)
- `--output`: Path to save the output markdown file (default: full_prd_output.md)

Example:
```bash
python prd_auto.py my_product_idea.txt --template custom_template.csv --output my_prd.md
```

## Input File Format

The input file should contain a clear description of your product idea. The tool will use this as the foundation for generating the PRD.

## Output

The tool generates a markdown file containing a complete PRD with the following sections:
- Product Overview
- Market Context
- Users
- User Requirements
- Metrics & KPIs
- High-Level Technical Architecture
- Go-To-Market
- Appendix (SWOT Analysis and Competitor Analysis) 