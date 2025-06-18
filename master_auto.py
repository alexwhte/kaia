#!/usr/bin/env python3
"""
Master Automation Script for PRD & Technical Specification Generation
Orchestrates the generation of PRD, Technical Specification, and Action Plan with versioning.
"""

from openai import OpenAI
import pandas as pd
import os
import argparse
import subprocess
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_next_version(output_dir, base_filename):
    """Get the next version number for a file"""
    if not os.path.exists(output_dir):
        return 1
    
    # Look for existing files with version numbers
    existing_files = []
    for file in os.listdir(output_dir):
        if file.startswith(base_filename.replace('.md', '')):
            # Extract version number from filename like "prd_v1.md" -> 1
            parts = file.replace('.md', '').split('_v')
            if len(parts) == 2 and parts[1].isdigit():
                existing_files.append(int(parts[1]))
    
    if not existing_files:
        return 1
    
    return max(existing_files) + 1

def run_script(script_name, args, description):
    """Run a script and return success status"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name] + args, 
                              capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Master script for generating PRD, Technical Specification, and Action Plan',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all documents with auto-versioning
  python3 master_auto.py forager_ig_input.txt

  # Generate with custom output directory
  python3 master_auto.py forager_ig_input.txt --output-dir my_outputs

  # Generate only PRD and Technical Spec (no action plan)
  python3 master_auto.py forager_ig_input.txt --skip-action-plan

  # Generate with custom templates
  python3 master_auto.py forager_ig_input.txt --prd-template custom_prd.csv --spec-template custom_spec.csv
        """
    )
    
    # Required arguments
    parser.add_argument('input_file', help='Path to the input text file containing the product idea')
    
    # Optional arguments
    parser.add_argument('--output-dir', default='output', help='Output directory (default: output)')
    parser.add_argument('--prd-template', default='prd_instructions.csv', help='PRD template file (default: prd_instructions.csv)')
    parser.add_argument('--spec-template', default='spec_instructions.csv', help='Technical spec template file (default: spec_instructions.csv)')
    parser.add_argument('--skip-action-plan', action='store_true', help='Skip action plan generation')
    parser.add_argument('--skip-prd', action='store_true', help='Skip PRD generation (use existing)')
    parser.add_argument('--skip-spec', action='store_true', help='Skip technical spec generation (use existing)')
    parser.add_argument('--existing-prd', help='Path to existing PRD file (if skipping PRD generation)')
    parser.add_argument('--existing-spec', help='Path to existing technical spec file (if skipping spec generation)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"❌ Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get version numbers
    prd_version = get_next_version(args.output_dir, 'prd.md')
    spec_version = get_next_version(args.output_dir, 'technical_specification.md')
    action_version = get_next_version(args.output_dir, 'action_plan.md')
    
    # Generate filenames with versioning
    prd_filename = f"prd_v{prd_version}.md"
    spec_filename = f"technical_specification_v{spec_version}.md"
    action_filename = f"action_plan_v{action_version}.md"
    
    prd_path = os.path.join(args.output_dir, prd_filename)
    spec_path = os.path.join(args.output_dir, spec_filename)
    action_path = os.path.join(args.output_dir, action_filename)
    
    print(f"🚀 Starting Master Automation Process")
    print(f"📁 Output Directory: {args.output_dir}")
    print(f"📄 Input File: {args.input_file}")
    print(f"🔢 Version Numbers: PRD v{prd_version}, Spec v{spec_version}, Action Plan v{action_version}")
    
    # Step 1: Generate PRD
    if not args.skip_prd:
        prd_args = [
            args.input_file,
            '--template', args.prd_template,
            '--output', prd_path
        ]
        
        if not run_script('prd_auto.py', prd_args, f"Generating PRD (v{prd_version})"):
            print("❌ PRD generation failed. Stopping.")
            sys.exit(1)
    else:
        if args.existing_prd and os.path.exists(args.existing_prd):
            prd_path = args.existing_prd
            print(f"✅ Using existing PRD: {prd_path}")
        else:
            print("❌ --skip-prd specified but no valid --existing-prd provided")
            sys.exit(1)
    
    # Step 2: Generate Technical Specification
    if not args.skip_spec:
        spec_args = [
            prd_path,
            '--template', args.spec_template,
            '--output', spec_path,
            '--product-idea', args.input_file
        ]
        
        if not run_script('spec_auto.py', spec_args, f"Generating Technical Specification (v{spec_version})"):
            print("❌ Technical specification generation failed. Stopping.")
            sys.exit(1)
    else:
        if args.existing_spec and os.path.exists(args.existing_spec):
            spec_path = args.existing_spec
            print(f"✅ Using existing Technical Specification: {spec_path}")
        else:
            print("❌ --skip-spec specified but no valid --existing-spec provided")
            sys.exit(1)
    
    # Step 3: Generate Action Plan
    if not args.skip_action_plan:
        action_args = [
            spec_path,
            '--prd-file', prd_path,
            '--output', action_path
        ]
        
        if not run_script('action_plan_auto.py', action_args, f"Generating Action Plan (v{action_version})"):
            print("❌ Action plan generation failed.")
            # Don't exit here as the main documents are already generated
        else:
            print(f"✅ Action Plan generated: {action_path}")
    else:
        print("⏭️  Skipping Action Plan generation")
    
    # Create summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "input_file": args.input_file,
        "output_directory": args.output_dir,
        "generated_files": {
            "prd": {
                "filename": prd_filename,
                "path": prd_path,
                "version": prd_version
            },
            "technical_specification": {
                "filename": spec_filename,
                "path": spec_path,
                "version": spec_version
            }
        }
    }
    
    if not args.skip_action_plan:
        summary["generated_files"]["action_plan"] = {
            "filename": action_filename,
            "path": action_path,
            "version": action_version
        }
    
    # Save summary
    summary_path = os.path.join(args.output_dir, f"generation_summary_v{prd_version}.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print final summary
    print(f"\n{'='*60}")
    print(f"🎉 Master Automation Complete!")
    print(f"{'='*60}")
    print(f"📁 Output Directory: {args.output_dir}")
    print(f"📄 PRD: {prd_filename} (v{prd_version})")
    print(f"📄 Technical Specification: {spec_filename} (v{spec_version})")
    if not args.skip_action_plan:
        print(f"📄 Action Plan: {action_filename} (v{action_version})")
    print(f"📄 Summary: generation_summary_v{prd_version}.json")
    print(f"\n💡 Next Steps:")
    print(f"   1. Review the generated documents")
    print(f"   2. Use the Action Plan to set up your development environment")
    print(f"   3. Use the TaskMaster prompt to break down development tasks")
    print(f"   4. Start with MVP features and iterate!")

if __name__ == "__main__":
    main() 