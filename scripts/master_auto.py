#!/usr/bin/env python3
"""
Master Auto - Generate complete PRD, Technical Specification, Action Plan, and Milestone Specifications
Runs all automation scripts in sequence with versioned output files
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

def run_script(script_name, args, description):
    """Run a Python script and return success status"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        print(f"❌ Error: Script {script_name} not found at {script_path}")
        return False
    
    try:
        # Build command
        cmd = [sys.executable, str(script_path)] + args
        print(f"Running: {' '.join(cmd)}")
        
        # Run script
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        
        print(f"✅ {description} completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def get_next_version(output_dir):
    """Get the next version number for output files"""
    if not output_dir.exists():
        return 1
    
    # Look for existing files with version numbers
    existing_versions = []
    for file in output_dir.glob("*_v*.md"):
        # Extract version number from filename like "prd_v1.md" -> 1
        parts = file.stem.split('_v')
        if len(parts) >= 2 and parts[-1].isdigit():
            existing_versions.append(int(parts[-1]))
    
    if not existing_versions:
        return 1
    
    return max(existing_versions) + 1

def main():
    parser = argparse.ArgumentParser(description='Generate complete PRD, Technical Specification, Action Plan, and Milestone Specifications')
    parser.add_argument('product_idea', help='Product idea or description')
    parser.add_argument('--version', help='Version suffix for output files (default: auto-generated)')
    parser.add_argument('--output-dir', default='output', help='Output directory (default: output)')
    parser.add_argument('--skip-prd', action='store_true', help='Skip PRD generation')
    parser.add_argument('--skip-spec', action='store_true', help='Skip Technical Specification generation')
    parser.add_argument('--skip-action-plan', action='store_true', help='Skip Action Plan generation')
    parser.add_argument('--skip-milestones', action='store_true', help='Skip Milestone Specifications generation')
    parser.add_argument('--skip-gtm', action='store_true', help='Skip Go-To-Market Plan generation')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate version suffix if not provided
    if not args.version:
        args.version = str(get_next_version(output_dir))
    
    print(f"🎯 Starting complete automation pipeline")
    print(f"📁 Output directory: {output_dir}")
    print(f"🏷️  Version: {args.version}")
    
    # Track generated files for next steps
    generated_files = {}
    temp_files = []  # Track temporary files for cleanup
    
    # Check if product_idea is a file path or raw text
    product_idea_input = Path(args.product_idea)
    if not product_idea_input.exists() or not product_idea_input.is_file():
        # It's raw text, create a temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write(args.product_idea)
        temp_file.close()
        product_idea_input = Path(temp_file.name)
        temp_files.append(product_idea_input)
    
    # Step 1: Generate PRD
    if not args.skip_prd:
        prd_output = output_dir / f"prd_{args.version}.md"
        success = run_script(
            "prd_auto.py",
            [str(product_idea_input), "--output", str(prd_output)],
            "PRD Generation"
        )
        if success:
            generated_files['prd'] = prd_output
        else:
            print("❌ PRD generation failed. Stopping pipeline.")
            # Clean up temp files
            for temp_file in temp_files:
                if temp_file.exists():
                    temp_file.unlink()
            sys.exit(1)
    else:
        print("⏭️  Skipping PRD generation")
    
    # Step 2: Generate Technical Specification
    if not args.skip_spec:
        spec_output = output_dir / f"tech_spec_{args.version}.md"
        if 'prd' in generated_files:
            # Use PRD as input
            success = run_script(
                "spec_auto.py",
                [str(generated_files['prd']), "--output", str(spec_output)],
                "Technical Specification Generation"
            )
        else:
            # Use product idea directly (or temp file if it was raw text)
            success = run_script(
                "spec_auto.py",
                [str(product_idea_input), "--output", str(spec_output)],
                "Technical Specification Generation"
            )
        
        if success:
            generated_files['spec'] = spec_output
        else:
            print("❌ Technical Specification generation failed. Stopping pipeline.")
            sys.exit(1)
    else:
        print("⏭️  Skipping Technical Specification generation")
    
    # Step 3: Generate Action Plan
    if not args.skip_action_plan:
        action_plan_output = output_dir / f"action_plan_{args.version}.md"
        if 'spec' in generated_files and 'prd' in generated_files:
            # Use both spec and PRD as input
            success = run_script(
                "action_plan_auto.py",
                [str(generated_files['spec']), "--prd-file", str(generated_files['prd']), "--output", str(action_plan_output)],
                "Action Plan Generation"
            )
        elif 'spec' in generated_files:
            # Use only spec as input
            success = run_script(
                "action_plan_auto.py",
                [str(generated_files['spec']), "--output", str(action_plan_output)],
                "Action Plan Generation"
            )
        else:
            print("❌ Need Technical Specification for Action Plan generation")
            sys.exit(1)
        
        if success:
            generated_files['action_plan'] = action_plan_output
        else:
            print("❌ Action Plan generation failed. Stopping pipeline.")
            sys.exit(1)
    else:
        print("⏭️  Skipping Action Plan generation")
    
    # Step 4: Generate Milestone Specifications
    if not args.skip_milestones:
        milestone_output = output_dir / f"milestone_specs_{args.version}.md"
        if 'spec' in generated_files and 'action_plan' in generated_files:
            # Use both spec and action plan as input
            success = run_script(
                "milestones_auto.py",
                [str(generated_files['spec']), "--action-plan-file", str(generated_files['action_plan']), "--output", str(milestone_output)],
                "Milestone Specifications Generation"
            )
        elif 'spec' in generated_files:
            # Use only spec as input
            success = run_script(
                "milestones_auto.py",
                [str(generated_files['spec']), "--output", str(milestone_output)],
                "Milestone Specifications Generation"
            )
        else:
            print("❌ Need Technical Specification for Milestone Specifications generation")
            sys.exit(1)
        
        if success:
            generated_files['milestones'] = milestone_output
        else:
            print("❌ Milestone Specifications generation failed. Stopping pipeline.")
            sys.exit(1)
    else:
        print("⏭️  Skipping Milestone Specifications generation")
    
    # Step 5: Generate Go-To-Market Plan
    if not args.skip_gtm:
        gtm_output = output_dir / f"gtm_plan_{args.version}.md"
        if 'prd' in generated_files:
            # Use PRD as input
            success = run_script(
                "gtm_auto.py",
                [str(generated_files['prd']), "--output", str(gtm_output)],
                "Go-To-Market Plan Generation"
            )
        else:
            # Use product idea directly (or temp file if it was raw text)
            success = run_script(
                "gtm_auto.py",
                [str(product_idea_input), "--output", str(gtm_output)],
                "Go-To-Market Plan Generation"
            )
        
        if success:
            generated_files['gtm'] = gtm_output
        else:
            print("❌ Go-To-Market Plan generation failed. Stopping pipeline.")
            sys.exit(1)
    else:
        print("⏭️  Skipping Go-To-Market Plan generation")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🎉 Complete automation pipeline finished successfully!")
    print(f"{'='*60}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🏷️  Version: {args.version}")
    print(f"\n📄 Generated files:")
    
    for doc_type, file_path in generated_files.items():
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   ✅ {doc_type.upper()}: {file_path.name} ({size:,} bytes)")
        else:
            print(f"   ❌ {doc_type.upper()}: {file_path.name} (file not found)")
    
    # Clean up temporary files
    for temp_file in temp_files:
        if temp_file.exists():
            temp_file.unlink()
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Review the generated documents")
    print(f"   2. Customize as needed for your specific requirements")
    print(f"   3. Share with your development team")
    print(f"   4. Use milestone specifications for detailed development planning")

if __name__ == "__main__":
    main() 