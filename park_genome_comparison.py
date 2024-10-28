#!/usr/bin/env python3
import sys
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

def create_venn_diagram(genecount_file, output_file="veenDiagram.pdf"):
    """
    Create a Venn diagram from OrthoFinder gene count results
    
    Args:
        genecount_file (str): Path to Orthogroups.GeneCount.tsv
        output_file (str): Path for output PDF file
        
    Returns:
        dict: Dictionary containing strain names and their unique/shared gene counts
    """
    now = str(datetime.datetime.now())[0:16]
    print(f'# Generating Venn diagram at {now}')

    if not os.path.exists(genecount_file):
        sys.exit(f"Gene count file not found: {genecount_file}")

    # Initialize strain lists
    Strain1, Strain2, Strain3 = [], [], []

    # Read gene counts and populate strain lists
    with open(genecount_file, "r") as genecount:
        header = genecount.readline().rstrip()
        fields = header.split('\t')
        name_strain1, name_strain2, name_strain3 = fields[1:4]
        
        for line in genecount:
            line = line.rstrip()
            field = line.split('\t')
            new_field = list(map(int, field[1:-1]))
            int_field = tuple(map(lambda val: int(val > 0), new_field))
            
            if int_field[0] > 0:
                Strain1.append(field[0])
            if int_field[1] > 0:
                Strain2.append(field[0])
            if int_field[2] > 0:
                Strain3.append(field[0])

    # Convert to sets
    set1 = set(Strain1)
    set2 = set(Strain2)           
    set3 = set(Strain3)           

    # Create Venn diagram
    plt.figure(figsize=(10, 10))
    venn3([set1, set2, set3], (name_strain1, name_strain2, name_strain3))
    plt.savefig(output_file, format="pdf", bbox_inches='tight')
    plt.close()

    # Calculate statistics
    stats = {
        'strains': {
            name_strain1: len(set1),
            name_strain2: len(set2),
            name_strain3: len(set3)
        },
        'shared': {
            f'{name_strain1}_{name_strain2}': len(set1 & set2),
            f'{name_strain2}_{name_strain3}': len(set2 & set3),
            f'{name_strain1}_{name_strain3}': len(set1 & set3),
            'all': len(set1 & set2 & set3)
        },
        'unique': {
            name_strain1: len(set1 - (set2 | set3)),
            name_strain2: len(set2 - (set1 | set3)),
            name_strain3: len(set3 - (set1 | set2))
        }
    }

    print(f"Venn diagram saved as: {output_file}")
    return stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <Orthogroups.GeneCount.tsv>')
        sys.exit(1)
