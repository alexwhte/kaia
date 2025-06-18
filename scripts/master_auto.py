#!/usr/bin/env python3
"""
Master script to run the complete PRD automation pipeline:
1. Generate PRD from CSV input
2. Generate Technical Specification from PRD
3. Generate Action Plan from Technical Specification
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime

def run_script(script_name, args):
    """Run a Python script and return success status"""
    cmd = [sys.executable, script_name] + args
    print(f"\n🚀 Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {script_name} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print(f"❌ {script_name} failed")
        if result.stderr:
            print(result.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Run complete PRD automation pipeline')
    parser.add_argument('input_file', help='Path to the input CSV file (e.g., prd_instructions.csv)')
    parser.add_argument('--skip-prd', action='store_true', help='Skip PRD generation')
    parser.add_argument('--skip-spec', action='store_true', help='Skip technical specification generation')
    parser.add_argument('--skip-action-plan', action='store_true', help='Skip action plan generation')
    parser.add_argument('--version', help='Version suffix for output files (e.g., v1, v2)')
    args = parser.parse_args()

    # Generate version suffix
    if args.version:
        version_suffix = f"_{args.version}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_suffix = f"_{timestamp}"

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Step 1: Generate PRD
    if not args.skip_prd:
        prd_output = f"output/prd{version_suffix}.md"
        if not run_script('prd_auto.py', [args.input_file, '--output', prd_output]):
            print("❌ Pipeline failed at PRD generation")
            sys.exit(1)
    else:
        # Find existing PRD file
        prd_files = [f for f in os.listdir('output') if f.startswith('prd') and f.endswith('.md')]
        if not prd_files:
            print("❌ No existing PRD file found and PRD generation was skipped")
            sys.exit(1)
        prd_output = f"output/{sorted(prd_files)[-1]}"  # Use most recent
        print(f"📄 Using existing PRD: {prd_output}")

    # Step 2: Generate Technical Specification
    if not args.skip_spec:
        spec_output = f"output/technical_specification{version_suffix}.md"
        if not run_script('spec_auto.py', [prd_output, '--output', spec_output]):
            print("❌ Pipeline failed at technical specification generation")
            sys.exit(1)
    else:
        # Find existing spec file
        spec_files = [f for f in os.listdir('output') if f.startswith('technical_specification') and f.endswith('.md')]
        if not spec_files:
            print("❌ No existing technical specification file found and spec generation was skipped")
            sys.exit(1)
        spec_output = f"output/{sorted(spec_files)[-1]}"  # Use most recent
        print(f"📄 Using existing technical specification: {spec_output}")

    # Step 3: Generate Action Plan
    if not args.skip_action_plan:
        action_plan_output = f"output/action_plan{version_suffix}.md"
        if not run_script('action_plan_auto.py', [spec_output, '--prd-file', prd_output, '--output', action_plan_output]):
            print("❌ Pipeline failed at action plan generation")
            sys.exit(1)
    else:
        print("⏭️ Skipping action plan generation")

    print(f"\n🎉 Pipeline completed successfully!")
    print(f"📁 Output files:")
    if not args.skip_prd:
        print(f"   • PRD: {prd_output}")
    if not args.skip_spec:
        print(f"   • Technical Specification: {spec_output}")
    if not args.skip_action_plan:
        print(f"   • Action Plan: {action_plan_output}")

if __name__ == "__main__":
    main() 