#!/usr/bin/env python3
import subprocess
import sys
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

#/Users/pfb2024/PROYECT_pfb2024/ExampleData/OrthoFinder/Results_Oct26_2/Orthogroups/Orthogroups.GeneCount.tsv


# Arguments required for genome comparsion
# 1. Gene Count for orthologroups
# 2. Name Strain 1 in file 1
# 3. Name Strain 2 in file 1
# 4. Name Strain 3 in file 1

# help message
if len(sys.argv) < 1:
	print(f'Usage: {sys.argv[0]} <Orthogroups.GeneCount.tsv>')
	exit(1)

# get cmd line params
ort_genecount = sys.argv[1]

# Running time 
now = str(datetime.datetime.now())
# cut down to 2019-10-23 13:49
now = now[0:16]

#log run command and time/date to screen
print('#' , ' '.join(sys.argv))
print('#' , 'was run on', now)


Strain1= []
Strain2= []
Strain3= []

with open(ort_genecount, "r") as genecount:
    genecount.readline()
    for line in genecount:
        line = line.rstrip()
        field = line.split('\t')
        new_fiel=list(map(int, field[1:-1]))
        int_field=tuple(map(lambda val: int(val > 0), new_fiel))
        #print(int_field)
        if int_field[0] > 0:
            Strain1.append(field[0])
        if int_field[1] > 0:
            Strain2.append(field[0])
        if int_field[2] > 0:
            Strain3.append(field[0])

set1 = set(Strain1)
set2 = set(Strain2)           
set3 = set(Strain3)           

#print(Strain2)

name_strain1 = ''
name_strain2 = ''
name_strain3 = ''

with open(ort_genecount, "r") as genecount:
    for line in genecount:
        if line.startswith('Orthogroup'):
            line = line.rstrip()
            field = line.split('\t')
            name_strain1 = field[1]
            name_strain2 = field[2]
            name_strain3 = field[3]


venn3([set1, set2, set3], (name_strain1, name_strain2, name_strain3))
plt.savefig("veenDiagram.pdf", format="pdf")
plt.show()
