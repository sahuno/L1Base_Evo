# mafft first10_ids_clean.fasta > first10_ids_clean.aln


from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import matplotlib.pyplot as plt

# Read the alignment
alignment = AlignIO.read("first10_ids_clean.aln", "fasta")

# Calculate a distance matrix (using the 'identity' model)
calculator = DistanceCalculator('identity')
dm = calculator.get_distance(alignment)
print("Distance Matrix:")
print(dm)

# Construct a Neighbor-Joining tree from the distance matrix
constructor = DistanceTreeConstructor()
nj_tree = constructor.nj(dm)
nj_tree.root_at_midpoint()

# Print an ASCII representation of the tree
print("\nNeighbor-Joining Phylogenetic Tree (ASCII):")
Phylo.draw_ascii(nj_tree)

# Optionally, display the tree graphically
fig = plt.figure(figsize=(10, 5))
axes = fig.add_subplot(1, 1, 1)
Phylo.draw(nj_tree, do_show=False, axes=axes)
plt.title("Neighbor-Joining Phylogenetic Tree")
plt.show()

# Save the tree in Newick format for future use
Phylo.write(nj_tree, "first10_ids_tree.nwk", "newick")
print("Tree saved as 'first10_ids_tree.nwk'")