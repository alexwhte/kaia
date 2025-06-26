#!/usr/bin/env python3
"""
Master Script with Corrections - Complete PRD/Spec generation pipeline
with validation extraction and post-generation corrections.
"""

import subprocess
import sys
import os
import argparse

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate PRD and Spec with validation corrections')
    parser.add_argument('input_file', help='Path to the input text file containing the product idea')
    parser.add_argument('--prd-output', default='output/prd_final.md', help='Output PRD file path')
    parser.add_argument('--spec-output', default='output/tech_spec_final.md', help='Output spec file path')
    parser.add_argument('--validation-output', default='output/validation_tracking.md', help='Output validation file path')
    parser.add_argument('--skip-corrections', action='store_true', help='Skip post-generation corrections')
    
    args = parser.parse_args()
    
    print("🚀 Starting PRD/Spec generation pipeline with corrections...")
    
    # Step 1: Generate PRD
    prd_cmd = ['python3', 'scripts/prd_auto.py', args.input_file, '--output', args.prd_output]
    run_command(prd_cmd, "Generating PRD")
    
    # Step 2: Generate Technical Specification
    spec_cmd = ['python3', 'scripts/spec_auto.py', args.prd_output, '--output', args.spec_output]
    run_command(spec_cmd, "Generating Technical Specification")
    
    # Step 3: Extract validation findings
    validation_cmd = ['python3', 'scripts/validation_extractor.py', args.spec_output, '--output', args.validation_output]
    run_command(validation_cmd, "Extracting validation findings")
    
    if args.skip_corrections:
        print("\n⏭️ Skipping post-generation corrections as requested")
        print(f"✅ Pipeline completed:")
        print(f"   - PRD: {args.prd_output}")
        print(f"   - Spec: {args.spec_output}")
        print(f"   - Validation: {args.validation_output}")
        return
    
    # Step 4: Apply post-generation corrections
    print("\n🔧 Applying post-generation corrections...")
    correction_cmd = ['python3', 'scripts/architecture_corrector.py', args.prd_output, args.spec_output, args.validation_output]
    
    try:
        result = subprocess.run(correction_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Corrections applied successfully")
            print(result.stdout)
        else:
            print("⚠️ Corrections failed or no corrections needed:")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"⚠️ Correction step encountered an error: {e}")
        print("Continuing with original files...")
    
    print(f"\n🎉 Pipeline completed:")
    print(f"   - PRD: {args.prd_output}")
    print(f"   - Spec: {args.spec_output}")
    print(f"   - Validation: {args.validation_output}")
    print(f"   - Corrected versions: {args.prd_output.replace('.md', '_corrected.md')}, {args.spec_output.replace('.md', '_corrected.md')}")

if __name__ == "__main__":
    main() 