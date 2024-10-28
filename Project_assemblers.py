#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime

def download_sra_files(sra_ids):
    """
    Download multiple SRA files
    
    Args:
        sra_ids (list): List of SRA IDs to download
        
    Returns:
        dict: Dictionary of successfully downloaded files {sra_id: fastq_path}
    """
    date = str(datetime.datetime.now())[0:16]
    print(f'Starting SRA downloads at: {date}')
    
    downloaded_files = {}
    
    for sra_id in sra_ids:
        if not sra_id.startswith('SRR'):
            print(f'Warning: Invalid SRA ID format: {sra_id}')
            continue
            
        fastq_path = f"{sra_id}.fastq"
        
        if os.path.exists(fastq_path):
            print(f'File already exists: {fastq_path}')
            downloaded_files[sra_id] = fastq_path
        else:
            print(f'Downloading: {sra_id}')
            try:
                subprocess.run(['fasterq-dump', sra_id], check=True)
                downloaded_files[sra_id] = fastq_path
            except subprocess.CalledProcessError as e:
                print(f'Error downloading {sra_id}: {str(e)}')
    
    return downloaded_files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: script.py <SRR_ID_1> <SRR_ID_2> ...')
        print('Example: script.py SRR12345678 SRR87654321 SRR11223344')
        sys.exit(1)
    
    # 커맨드 라인에서 SRA ID 목록 가져오기
    sra_ids = sys.argv[1:]
    downloaded_files = download_sra_files(sra_ids)
    
    if not downloaded_files:
        print("No files were downloaded successfully")
        sys.exit(1)
    
    print("\nSuccessfully downloaded files:")
    for sra_id, filepath in downloaded_files.items():
        print(f"{sra_id}: {filepath}")
