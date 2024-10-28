#!/usr/bin/env python3
import subprocess
import sys
import datetime
import os

def run_prokka(out_folder, unique_name, genus, assembly_file, force=True):
    """Prokka annotation을 실행하고 결과 파일들의 경로를 반환하는 함수"""
    
    if ' ' in unique_name:
        sys.exit('Output directory name cannot contain spaces')

    if not os.path.exists(assembly_file):
        sys.exit(f"Assembly file not found: {assembly_file}")

    # Running time 
    now = str(datetime.datetime.now())[0:16]
    print(f'# Starting Prokka annotation for {unique_name} at {now}')

    # Prokka 명령어 확인
    result = subprocess.run(['which', 'prokka'], capture_output=True)
    if result.returncode != 0:
        sys.exit("Prokka is not installed or not in PATH")

    # 출력 디렉토리 생성
    os.makedirs(out_folder, exist_ok=True)

    # Prokka 명령어 구성
    cmd = [
        'prokka',
        '--outdir', out_folder,
        '--gffver', '3',
        '--prefix', unique_name,
        '--genus', genus,
        '--force',
        '--cpus', '4',
        assembly_file
    ]
    
    print(f"Executing command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        sys.exit(f"Prokka failed with error:\n{result.stderr}")
    
    # 결과 파일 경로 반환
    return {
        'txt': os.path.join(out_folder, f"{unique_name}.txt"),
        'faa': os.path.join(out_folder, f"{unique_name}.faa")
    }

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit(f'Usage: {sys.argv[0]} <folder_output_name> <unique_name> <genus_name> <assembly_fasta>')
    
    results = run_prokka(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print(f"\nResults location:")
    print(f"Text summary: {results['txt']}")
    print(f"Protein sequences (FAA): {results['faa']}")
