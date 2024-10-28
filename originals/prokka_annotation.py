#!/usr/bin/env python3
import subprocess
import sys
import datetime
import os

# help message
if len(sys.argv) < 3:
	print(f'Usage: {sys.argv[0]} <folder_output_name> <unique_name> <genus_name> <assembly_fasta>')
	exit(1)

# get cmd line params
out_folder = sys.argv[1]
unique_name = sys.argv[2]
genus = sys.argv[3]
assembly = sys.argv[4]

if ' ' in unique_name:
	print('do not include spaces in output directory')
	exit(1)

# Running time 
now = str(datetime.datetime.now())
# cut down to 2019-10-23 13:49
now = now[0:16]

#log run command and time/date to screen
print('#' , ' '.join(sys.argv))
print('#' , 'was run on', now)

# run the command
prokkacmd = f'prokka --outdir {out_folder} --gffver 3 --prefix {unique_name} --genus {genus} {assembly}'
# object is returned after run command
blastcmd_run = subprocess.run(prokkacmd, shell=True , stdout = subprocess.PIPE,
stderr=subprocess.PIPE)
# Now we need to check the UNIX return code
# always do this!
# 0 = success
# non-zero =failure
if blastcmd_run.returncode != 0:
  print("FAILED!")
  exit(2)

#current directory
cwd = os.getcwd()

result = cwd+'/'+out_folder+'/'+unique_name+'.txt'

with open(result,'r') as prokka_results:
	for line in prokka_results:
		line = line.rstrip()
		print(line)