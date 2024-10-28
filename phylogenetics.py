#!/usr/bin/env python3

import subprocess
import sys,random
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import AlignIO
from Bio.Align.Applications import MuscleCommandline#ClustalwCommandline
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import matplotlib
import matplotlib.pyplot as plt
import os
#from Bio import PyGraphviz

def combine_files(file_list, fasta_file):
    with open(fasta_file, "w") as output_handle:
        for intput_file in file_list:
            for input_file in input_file:
                for record in SeqIO.parse(input_file, "fasta"):
                    SeqIO.write(record, output_handle, "fasta")
    return fasta_file


def Phylo_tree (input_file, output_file='combined'):
    """ This function reads multiple fasta files, aligns them using MUSCLE and then plots a phylogenetic tree based on the alignment matrix"""
    # Use: python join_fasta.py infile1.fasta infile2.fasta outfile.fasta
    # input_file = sys.argv[1:]
    print(input_file)

    # output_file = 'combined_Ankit.fa'                               #Name of the output file
    # fasta_file= os.path.join(os.getcwd(), output_file+'.fa')
    phylo_file= os.path.join(os.getcwd(), output_file+'.tree.xml')
    align_file= os.path.join(os.getcwd(), output_file+'.aln.fa')
    pdf_file = os.path.join(os.getcwd(), output_file+'.aln.fa.pdf')
    
    print ("Output fasta file = ", output_file)

    a = f'muscle -align {input_file} -output {align_file}'
    subprocess.call(a, shell=True) # This line is used to make sure that variable a runs in the command line
    if a.returncode != 0:
        print('failed')
    with open (align_file) as aln:
        alignment = AlignIO.read(aln,'fasta')
        print(type(alignment))
        calculator = DistanceCalculator('identity')
        distance_matrix = calculator.get_distance(alignment)
        print(distance_matrix)
        constructor = DistanceTreeConstructor(calculator)
        tree = constructor.build_tree(alignment)
        tree.rooted = True
        print(tree)
        tree = tree.as_phyloxml()
        Phylo.write(tree, phylo_file,'phyloxml')
        Phylo.read(phylo_file, 'phyloxml')
        tree.ladderize()
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)
   
        Phylo.draw(tree, axes = axes, do_show = False) 
        plt.savefig(pdf_file)
    

if __name__ == '__main__':
    import glob

    files = glob.glob("Protein_files_for_orthofinder/OrthoFinder/Results_Oct27/Orthogroup_Sequences/*.fa")

    for file_name in files[:5]:
       Phylo_tree (input_file=file_name, output_file=file_name[:-3]+'.TMP')
        
              
