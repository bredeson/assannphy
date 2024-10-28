#!/usr/bin/env python3

import os, sys
import subprocess
import datetime
from pathlib import Path

#This works in mamba enviroment with MCscan intalled
# RECOMENDATION
    # Short names for bed files

def gff_to_bed(gff_file, bedname_file):
    '''
    This program requires two inputs: 
    1) The gff_file on versio 3 (compressed or uncompressed)
    2) The name for the bed output file.
    The function is set up for --primary_only
    '''
    gff_to_bed_cmd = f'python -m jcvi.formats.gff bed --type=CDS --key=ID --primary_only {gff_file} -o {bedname_file}'
    gff_to_bed_run = subprocess.run(gff_to_bed_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    return gff_to_bed_run

def fasta_to_cds(fasta, cds):
    '''
    fasta file most be protein fasta, compreseed or not.
    cds is the name for the new fasta file. Recomended a short one. 
    '''
    fasta_to_cds_cmd = f'python -m jcvi.formats.fasta format {fasta} {cds}'
    fasta_to_cds_run = subprocess.run(fasta_to_cds_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    return fasta_to_cds_run


def pair_synteny(orga1, orga2):
    '''
    orga1: First organism to compare. Same name as cds with not file extension.
    orga2: Second organism to compare. Same name as cds with not file extension.
    '''

    pair_synteny_cmd = f'python -m jcvi.compara.catalog ortholog {orga1} {orga2} --cscore=.99 --no_strip_names'
    pair_synteny_run = subprocess.run(pair_synteny_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    synteny_dot_cmd = f'python -m jcvi.graphics.dotplot {orga1}.{orga2}.anchors'
    synteny_dot_run = subprocess.run(synteny_dot_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    synteny_hist_cmd = f'python -m jcvi.compara.synteny depth --histogram {orga1}.{orga2}.anchors'
    synteny_hist_run = subprocess.run(synteny_hist_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)

    return synteny_hist_run

# def synteny_macro(orga1, orga2, orga3):

#     synteny_macro_cmd= f'python -m jcvi.compara.synteny screen --minspan=1 --minsize=1 --simple {orga1}.{orga2}.anchors {orga1}.{orga2}.anchors.new'
#     synteny_macro_run = subprocess.run(synteny_macro_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)
#     synteny_macro_cmd= f'python -m jcvi.compara.synteny screen --minspan=1 --minsize=1 --simple {orga2}.{orga3}.anchors {orga1}.{orga2}.anchors.new'
#     synteny_macro_run = subprocess.run(synteny_macro_cmd, shell=True , stdout = subprocess.PIPE, stderr=subprocess.PIPE)
#     anchors_new1-2= f'{orga1}.{orga2}.anchors.new'
#     anchors_new2-3= f'{orga1}.{orga2}.anchors.new'
#     bed_orga1 = f'{orga1}.bed'
#     bed_orga2 = f'{orga2}.bed'
#     bed_orga3 = f'{orga3}.bed'
#     contigs_list1=[]
#     contigs_list2=[]
#     contigs_list3=[]
#     with open(bed_orga1, "r") as bed_file_org1, open("seqids", "w") as seq_ids:
#         for line in bed_file_org1:
#             line = line.rstrip()
#             contigs = line.split('\t')
#             contigs_id = contigs[0]
#             if contigs_id not in contigs_list1:
#                 contigs_list1.append(contigs_id)
#     with open(bed_orga2, "r") as bed_file_org2, open("seqids", "w") as seq_ids:
#         for line in bed_file_org2:
#             line = line.rstrip()
#             contigs = line.split('\t')
#             contigs_id = contigs[0]
#             if contigs_id not in contigs_list2:
#                 contigs_list2.append(contigs_id)
#     with open(bed_orga3, "r") as bed_file_org3, open("seqids", "w") as seq_ids:
#         for line in bed_file_org3:
#             line = line.rstrip()
#             contigs = line.split('\t')
#             contigs_id = contigs[0]
#             if contigs_id not in contigs_list2:
#                 contigs_list2.append(contigs_id)
#         seq_ids.write(','.join(map(str, contigs_list1))+'\n'+','.join(map(str, contigs_list2))+'\n'+','.join(map(str, contigs_list3))+'\n')


def main():

    progname = sys.argv[0]

    usage = "\n\n\tusage: {} annotation.gff file_name.bed\n\n\n".format(progname)
    
    if len(sys.argv) < 2:
        sys.stderr.write(usage)
        sys.exit(1)
    
    # Running time 
    now = str(datetime.datetime.now())
    now = now[0:16]

    #log run command and time/date to screen
    print('#' , ' '.join(sys.argv))
    print('#' , 'was run on', now)

    # capture command-line arguments
    gff_file = sys.argv[1]
    bedname_file = sys.argv[2]

    if '.gff' not in gff_file:
        print('The annotation file most be gff (version3) or gff.gz') 
        sys.exit(0)
    
    if '.bed' not in bedname_file:
        print('The output file name most be bed format')
        sys.exit(0) 

    gff_to_bed(gff_file, bedname_file)

    print(f'Files {gff_file} was converted to {bedname_file}')

    sys.exit(0)  # always good practice to indicate worked ok!

if __name__ == '__main__':
    main()
    
