#!/usr/bin/env pyhton3
import sys
import os
import subprocess
import datetime

def SRAid_file (SRAid_file_txt):
    """This function allows you to download the fastq file of the related SRAids from NCBI.
    The download takes place at the dir where the script is present"""
    date = str(datetime.datetime.now())
    date = date[0:16]
    print('The program was run on:', date)

    if len(sys.argv)<2:
        print('The command line is incomplete: <Script_name> <.txt file, SRAid>')
        exit(1)
    
    SRAid = sys.argv[1]
    
    if SRAid.endswith('.txt'):
        with open (SRAid) as file:
            for line in file:
                line = line.rstrip()
                if line.startswith(('@', '>')):
                    print('# Please provide SRAid: eg.SRR12183694 not @SRR12183694')
                    continue
                elif os.path.exists(line +'.fastq'):
                    print('The file with the id already exists:', line, 'in the dir', os.getcwd())
                    continue
                else:
                    print('Downloading the flie:', line)
                    print('File will be downloaded in:', os.getcwd())
                    download = f'fasterq-dump {line}'
                    subprocess.call(download, shell = True)
    elif SRAid.startswith('SRR'):
        SRAid = sys.argv[1:]
        for ID in SRAid:
            if os.path.exists(ID +'.fastq'):
                print('The file with the id already exists:', ID)
                continue
            else:
                print('Downloading the flie:', ID)
                print('File will be downloaded in:', os.getcwd())
                download = f'fasterq-dump {ID}'
                subprocess.call(download, shell=True)
    else:
        if os.path.exists(SRAid +'.fastq'):
            print('The file with the id already exists:', os.getcwd())
           
        

                    



