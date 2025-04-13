import re

# Define the input and output file paths
input_file = '$HOME/Downloads/hg38.fa.out'
output_file = '$HOME/Downloads/L1PA1_to_L1PA8.txt'

# Define the patterns to filter
patterns = re.compile(r'L1PA[1-8](?!\d)')

# Open the input file and filter lines
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if patterns.search(line):
            outfile.write(line)

print(f"Filtered lines saved to {output_file}")