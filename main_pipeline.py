#!/usr/bin/env python3
from Project_assemblers import download_sra_files
from assemblies import run_assemblies, get_contig_files
from park_prokka_annotation import run_prokka
from park_orthofinder import run_orthofinder
import os
from park_genome_comparison import create_venn_diagram
from phylogenetics import Phylo_tree
import glob
def main():
    print("Starting SRA downloads...")

    assemblies = [
        {
            "SRAid": "SRR26130532",
            "strain": "Strepto",
            "platform": "pacbio",
            "genome_size": "10.2m",
            # "file": "SRR26130532.fastq",
            "genus": "Streptomyces"
        },
        {
            "SRAid": "SRR12183694",
            "strain": "Cyano",
            "platform": "pacbio",
            "genome_size": "2.5m",
            #"file": "SRR12183694.fastq",
            "genus": "Cyanobacteria"
        },
        {
            "SRAid": "SRR29409521",
            "strain": "lacto",
            "platform": "pacbio",
            "genome_size": "2.0m",
            #"file": "SRR29409521.fastq",
            "genus": "Lactobacillus"
        }
    ]
    print("\nDownloaded files:")
    for i in range(len(assemblies)):
        assemblies[i]['file'] = download_sra_files([assemblies[i]['SRAid']])
        print(f"{assemblies[i]['SRAid']}: {assemblies[i]['file']}")

    # 1. Assembly 단계
    print("Checking for existing assemblies...")
    contig_files = get_contig_files(assemblies)
    
    if not contig_files:
        print("No existing assemblies found. Starting genome assemblies...")
        run_assemblies(assemblies)
        print("\nWaiting for assemblies to complete...")
        contig_files = get_contig_files(assemblies)
    else:
        print("Found existing assemblies, skipping assembly step.")

    if not contig_files:
        raise Exception("No assembly results found")

    # 2. Prokka annotation
    print("\nChecking for existing annotations...")
    annotation_results = {}
    all_annotations_exist = True
    
    for assembly in assemblies:
        strain = assembly['strain']
        expected_faa = f"{strain}_annotation/{strain}.faa"
        if not os.path.exists(expected_faa):
            all_annotations_exist = False
            break

    if all_annotations_exist:
        print("Found existing annotations, skipping annotation step.")
        for assembly in assemblies:
            strain = assembly['strain']
            annotation_results[strain] = {
                'faa': f"{strain}_annotation/{strain}.faa",
                'txt': f"{strain}_annotation/{strain}.txt"
            }
    else:
        print("Running Prokka annotations...")
        for assembly in assemblies:
            strain = assembly['strain']
            if strain in contig_files:
                try:
                    print(f"\nRunning Prokka annotation for {strain}...")
                    results = run_prokka(
                        out_folder=f"{strain}_annotation",
                        unique_name=strain,
                        genus=assembly['genus'],
                        assembly_file=contig_files[strain],
                        force=True
                    )
                    annotation_results[strain] = results
                except Exception as e:
                    print(f"Error annotating {strain}: {str(e)}")
                    continue

    if not annotation_results:
        raise Exception("No successful annotations completed")

    # 3. OrthoFinder 분석
    print("\nChecking for existing OrthoFinder results...")
    orthofinder_results = None
    
    # 가장 최근의 OrthoFinder 결과 디렉토리 찾기
    protein_dir = "protein_files_for_orthofinder"
    if os.path.exists(protein_dir):
        results_base = os.path.join(protein_dir, "OrthoFinder")
        if os.path.exists(results_base):
            results_dirs = [d for d in os.listdir(results_base) if d.startswith("Results_")]
            if results_dirs:
                latest_results = sorted(results_dirs)[-1]
                orthofinder_results = os.path.join(results_base, latest_results)
                print(f"Found existing OrthoFinder results: {orthofinder_results}")

    if not orthofinder_results:
        print("Running new OrthoFinder analysis...")
        faa_files = {strain: results['faa'] for strain, results in annotation_results.items()}
        orthofinder_results = run_orthofinder(faa_files)
        print(f"\nOrthoFinder analysis completed successfully")

    # 4. Genome Comparison & Venn Diagram
    print("\nChecking for existing Venn diagram...")
    venn_diagram_file = "veenDiagram.pdf"
    
    if os.path.exists(venn_diagram_file):
        print("Found existing Venn diagram, skipping generation step.")
    else:
        print("Generating genome comparison and Venn diagram...")
        genecount_file = os.path.join(orthofinder_results, "Orthogroups", "Orthogroups.GeneCount.tsv")
        
        if os.path.exists(genecount_file):
            try:
                stats = create_venn_diagram(genecount_file)
                print("\nGene Distribution Statistics:")
                print("----------------------------")
                print("\nUnique genes per strain:")
                for strain, count in stats['unique'].items():
                    print(f"{strain}: {count}")
                print("\nShared genes:")
                for pair, count in stats['shared'].items():
                    print(f"{pair}: {count}")
            except Exception as e:
                print(f"Error generating Venn diagram: {str(e)}")
        else:
            print(f"Gene count file not found: {genecount_file}")

    files = glob.glob("Protein_files_for_orthofinder/OrthoFinder/Results_Oct27/Orthogroup_Sequences/*.fa")

    for file_name in files[0:10]:
       Phylo_tree (input_file=file_name, output_file=file_name[:-3])

    # 최종 결과 요약
    print("\nPipeline Summary:")
    print("----------------")
    for strain, results in annotation_results.items():
        print(f"\n{strain}:")
        print(f"  Assembly: {contig_files[strain]}")
        print(f"  Annotation summary: {results['txt']}")
        print(f"  Protein sequences: {results['faa']}")

    print(f"\nOrthoFinder Results:")
    print(f"  Results directory: {orthofinder_results}")
    print(f"  Venn diagram: {venn_diagram_file}")

    # 최종 결과를 포함하는 딕셔너리 반환
    pipeline_results = {
        'assembly_results': contig_files,
        'annotation_results': annotation_results,
        'orthofinder_results': orthofinder_results,
        'venn_diagram': venn_diagram_file
    }

    return pipeline_results

if __name__ == "__main__":
    # 명령줄 인자로부터 SRA ID 목록을 가져옵니다.
    #sra_ids = sys.argv[1:]
    
    #if not sra_ids:
        #sys.exit("Please provide SRA IDs as command line arguments")

    results = main()
    print("\nPipeline completed successfully")
    
    # 결과 경로들 출력
    print("\nResult Paths:")
    print("-------------")
    print(f"Assembly results: {results['assembly_results']}")
    print(f"Annotation results: {results['annotation_results']}")
    print(f"OrthoFinder results: {results['orthofinder_results']}")
