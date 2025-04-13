#!/usr/bin/env python3

# python scripts/build_phylogeny.py --unaligned mouse_flActiveLine1.fasta --plot
# python scripts/build_phylogeny.py --alignment mouse_flActiveLine1.aln --clustering upgma -o mytree.nwk --plot
# python scripts/build_phylogeny.py --unaligned scripts/first10_ids_clean.fasta --clustering upgma -o mytree.nwk --plot


import argparse
import subprocess
import os
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import matplotlib.pyplot as plt

def run_mafft(unaligned_file, alignment_file):
    """Run MAFFT with the '--auto' option to generate an alignment."""
    cmd = f"mafft --auto {unaligned_file} > {alignment_file}"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"MAFFT alignment generated: {alignment_file}")
    except subprocess.CalledProcessError as e:
        print("Error running MAFFT:", e)
        exit(1)

def build_tree(alignment_file, model, clustering_method):
    """Read the alignment file, compute distance, and build a phylogenetic tree."""
    alignment = AlignIO.read(alignment_file, "fasta")
    print("Alignment loaded from:", alignment_file)
    
    # Calculate the distance matrix
    calculator = DistanceCalculator(model)
    dm = calculator.get_distance(alignment)
    print("\nDistance Matrix:")
    print(dm)
    
    # Build tree using chosen method
    constructor = DistanceTreeConstructor()
    if clustering_method == "nj":
        tree = constructor.nj(dm)
    elif clustering_method == "upgma":
        tree = constructor.upgma(dm)
    else:
        print("Unsupported clustering method:", clustering_method)
        exit(1)
    
    tree.root_at_midpoint()
    return tree

def main():
    parser = argparse.ArgumentParser(
        description="Run MAFFT (optional) and build a phylogenetic tree from a FASTA alignment."
    )
    # Input options: Provide either an unaligned FASTA or an alignment file.
    parser.add_argument("-u", "--unaligned", help="Input unaligned FASTA file (will run MAFFT) if --alignment is not provided.")
    parser.add_argument("-a", "--alignment", help="Input alignment FASTA file (pre-aligned). If omitted, --unaligned is used and MAFFT will be run.")
    parser.add_argument("-o", "--output", default="tree.nwk", help="Output Newick tree file (default: tree.nwk).")
    parser.add_argument("-c", "--clustering", choices=["nj", "upgma"], default="nj",
                        help="Clustering method: 'nj' (Neighbor-Joining, default) or 'upgma'.")
    parser.add_argument("-m", "--model", default="identity", help="Distance model (default: identity).")
    parser.add_argument("--plot", action="store_true", help="Display the tree graphically.")
    
    args = parser.parse_args()
    
    # Determine the alignment file to use.
    alignment_file = args.alignment
    if not alignment_file:
        # If no alignment file provided, use the unaligned file with MAFFT.
        if not args.unaligned:
            parser.error("You must provide either an unaligned FASTA (--unaligned) or a pre-aligned FASTA (--alignment).")
        # Create a default alignment file name by appending .aln to unaligned file name
        alignment_file = os.path.splitext(args.unaligned)[0] + ".aln"
        run_mafft(args.unaligned, alignment_file)
    
    # Build the phylogenetic tree from the alignment file.
    tree = build_tree(alignment_file, args.model, args.clustering)
    
    # Print an ASCII representation of the tree.
    print("\nPhylogenetic Tree (ASCII):")
    Phylo.draw_ascii(tree)
    
    # Optionally, display the tree graphically.
    if args.plot:
        fig = plt.figure(figsize=(10, 5))
        axes = fig.add_subplot(1, 1, 1)
        Phylo.draw(tree, do_show=False, axes=axes)
        plt.title(f"Phylogenetic Tree ({args.clustering.upper()})")
        plt.xlabel("Branch Length")
        plt.savefig("phylogenetic_tree.png", dpi=300)
    
    # Save the tree in Newick format.
    Phylo.write(tree, args.output, "newick")
    print(f"\nTree saved as '{args.output}'")

if __name__ == '__main__':
    main()