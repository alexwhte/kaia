#!/usr/bin/env python3
"""
Architecture Corrector - Applies post-generation corrections to PRD and Spec
based on validation findings, focusing on technical architecture fixes.
"""

import re
import argparse
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def analyze_validation_findings(validation_file):
    """Analyze validation findings to identify basic correction actions needed."""
    
    with open(validation_file, 'r') as f:
        content = f.read()
    
    corrections_needed = []
    
    # Simple checks for common issues
    if 'instagram' in content.lower() and 'transcript' in content.lower():
        if 'does not provide' in content.lower() or 'limitation' in content.lower():
            corrections_needed.append('Instagram API transcript limitation')
    
    if 'missing' in content.lower() and ('speech-to-text' in content.lower() or 'ocr' in content.lower()):
        corrections_needed.append('Missing multimodal processing')
    
    if 'unrealistic' in content.lower() or 'assumption' in content.lower():
        corrections_needed.append('Unrealistic technical assumptions')
    
    return corrections_needed

def apply_architecture_corrections(prd_file, spec_file, corrections_needed):
    """Apply corrections to technical architecture sections."""
    
    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise SystemExit("❌ OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    
    # Read current files
    with open(prd_file, 'r') as f:
        prd_content = f.read()
    
    with open(spec_file, 'r') as f:
        spec_content = f.read()
    
    # Generate correction prompt
    correction_prompt = f"""
You are a Senior Technical Architect correcting technical architecture issues identified in validation.

**Validation Findings:**
{corrections_needed}

**Current PRD Technical Architecture:**
{prd_content}

**Current Spec Technical Architecture:**
{spec_content}

**Correction Requirements:**
1. Fix any API limitations (e.g., Instagram doesn't provide transcripts - use speech-to-text + OCR)
2. Add missing data processing components (speech-to-text, OCR, video processing)
3. Correct unrealistic data flows
4. Ensure consistency between PRD and Spec
5. Keep corrections generic - don't over-engineer for specific products

**Output Format:**
Provide corrected versions of:
1. PRD Technical Architecture section
2. Spec Data Processing & LLM Logic section
3. Updated architecture diagrams

Focus ONLY on technical architecture corrections. Be generic and reusable for any product idea.
"""
    
    # Get corrections from OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": correction_prompt}
        ],
        temperature=0.3
    )
    
    corrections = response.choices[0].message.content
    
    return corrections

def update_files_with_corrections(prd_file, spec_file, corrections):
    """Update the files with the corrected content."""
    
    # Parse corrections and update files
    # This is a simplified version - in practice, you'd want more sophisticated parsing
    
    # For now, create corrected versions
    prd_corrected = prd_file.replace('.md', '_corrected.md')
    spec_corrected = spec_file.replace('.md', '_corrected.md')
    
    with open(prd_corrected, 'w') as f:
        f.write(corrections)
    
    with open(spec_corrected, 'w') as f:
        f.write(corrections)
    
    return prd_corrected, spec_corrected

def update_validation_tracking(validation_file, corrections_applied):
    """Update validation tracking file with corrections applied."""
    
    with open(validation_file, 'r') as f:
        content = f.read()
    
    # Replace the "Pending correction analysis" sections
    corrections_section = f"""
## Corrections Applied

### Architecture Changes Made
{chr(10).join([f"- {correction}" for correction in corrections_applied.get('architecture_changes', [])])}

### Validation Issues Resolved
{chr(10).join([f"- {issue}" for issue in corrections_applied.get('issues_resolved', [])])}

### Remaining Open Issues
{chr(10).join([f"- {issue}" for issue in corrections_applied.get('remaining_issues', [])])}
"""
    
    # Replace the corrections section
    content = re.sub(
        r'## Corrections Applied.*?(?=##|$)',
        corrections_section,
        content,
        flags=re.DOTALL
    )
    
    with open(validation_file, 'w') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Apply post-generation corrections to PRD and Spec')
    parser.add_argument('prd_file', help='Path to the PRD file')
    parser.add_argument('spec_file', help='Path to the technical specification file')
    parser.add_argument('validation_file', help='Path to the validation tracking file')
    
    args = parser.parse_args()
    
    # Analyze validation findings
    print("🔍 Analyzing validation findings...")
    corrections_needed = analyze_validation_findings(args.validation_file)
    
    if not corrections_needed:
        print("✅ No corrections needed - validation passed")
        return
    
    print(f"🔧 Corrections needed: {corrections_needed}")
    
    # Apply corrections
    print("🔧 Applying architecture corrections...")
    corrections = apply_architecture_corrections(args.prd_file, args.spec_file, corrections_needed)
    
    # Update files
    print("📝 Updating files with corrections...")
    prd_corrected, spec_corrected = update_files_with_corrections(args.prd_file, args.spec_file, corrections)
    
    # Update validation tracking
    print("📊 Updating validation tracking...")
    corrections_applied = {
        'architecture_changes': corrections_needed,
        'issues_resolved': ['Technical architecture corrected based on validation findings'],
        'remaining_issues': ['Review corrected architecture for final approval']
    }
    update_validation_tracking(args.validation_file, corrections_applied)
    
    print(f"✅ Corrections applied:")
    print(f"   - PRD corrected: {prd_corrected}")
    print(f"   - Spec corrected: {spec_corrected}")
    print(f"   - Validation updated: {args.validation_file}")

if __name__ == "__main__":
    main() 