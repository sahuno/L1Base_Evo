#!/bin/bash
# Filter lines containing 'L1MdA' from the mm10.fa.out file and convert to BED format
mm10_file_path="${HOME}/Downloads/mm10.fa.out"
output_file="filtered_L1Md_A.bed"
grep -i "L1MdA" "$mm10_file_path" | awk '{print $5"\t"$6"\t"$7"\t"$10"\t"$9"\t"$11}' > "$output_file"
echo "Filtered lines containing 'L1MdA' have been converted to BED format and saved to $output_file"

# awk '/L1MdT/ {print $10}' ${HOME}Downloads/mm10.fa.out | sort | uniq | wc -l

# awk '/L1MdA/ {print $10}' ${HOME}/Downloads/mm10.fa.out | sort | uniq | wc -l
