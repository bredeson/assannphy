#!/usr/bin/env python3
import subprocess
import sys
import datetime
import os

def run_orthofinder(faa_files_dict):
    """
    Run OrthoFinder analysis on the provided FAA files
    
    Args:
        faa_files_dict (dict): Dictionary with strain names as keys and FAA file paths as values
    
    Returns:
        str: Path to OrthoFinder results directory
    """
    # Create a temporary directory for protein files
    protein_dir = "protein_files_for_orthofinder"
    os.makedirs(protein_dir, exist_ok=True)
    
    # Copy all FAA files to the protein directory
    for strain, faa_path in faa_files_dict.items():
        if not os.path.exists(faa_path):
            sys.exit(f"FAA file not found: {faa_path}")
            
        # Create symbolic link instead of copying
        target_path = os.path.join(protein_dir, f"{strain}.faa")
        if os.path.exists(target_path):
            os.remove(target_path)
        os.symlink(os.path.abspath(faa_path), target_path)

    # Running time 
    now = str(datetime.datetime.now())[0:16]
    print('#', 'OrthoFinder analysis started at', now)

    # Run OrthoFinder
    orthofinder_cmd = f'orthofinder -f {protein_dir}'
    print(f"Executing command: {orthofinder_cmd}")
    
    result = subprocess.run(orthofinder_cmd, 
                          shell=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          text=True)

    if result.returncode != 0:
        sys.exit(f"OrthoFinder failed with error:\n{result.stderr}")

    # Find the results directory (most recent OrthoFinder output)
    results_base = os.path.join(protein_dir, "OrthoFinder")
    if not os.path.exists(results_base):
        sys.exit("OrthoFinder output directory not found")

    results_dirs = [d for d in os.listdir(results_base) if d.startswith("Results_")]
    if not results_dirs:
        sys.exit("No results directory found")

    latest_results = sorted(results_dirs)[-1]
    results_path = os.path.join(results_base, latest_results)

    print(f"OrthoFinder analysis completed. Results available in: {results_path}")
    return results_path
