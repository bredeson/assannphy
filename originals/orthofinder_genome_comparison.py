#!/usr/bin/env python3
import subprocess
import sys
import datetime
import os

# Arguments required for OrthoFinder
# 1. folder with genomes fasta files

# help message
if len(sys.argv) < 1:
	print(f'Usage: {sys.argv[0]} <folder_with_proteome.fa>')
	exit(1)

# get cmd line params
folder_with_proteome = sys.argv[1]

# Running time 
now = str(datetime.datetime.now())
# cut down to 2019-10-23 13:49
now = now[0:16]

#log run command and time/date to screen
print('#' , ' '.join(sys.argv))
print('#' , 'was run on', now)

# run the command
orthodfindercmd = f'orthofinder -f {folder_with_proteome}'
# object is returned after run command
orthodfindercmd_run = subprocess.run(orthodfindercmd, shell=True , stdout = subprocess.PIPE,
stderr=subprocess.PIPE)

# Now we need to check the UNIX return code
# always do this!
# 0 = success
# non-zero =failure
if orthodfindercmd_run.returncode != 0:
  print("FAILED!")
  exit(2)
