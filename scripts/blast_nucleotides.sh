databaseFasta=$HOME/sta/L1Base_Evo/data/first10_ids_clean.fasta
baseName=`basename -s .fasta $databaseFasta`
#sed '/^>/ {s/,.*//; s/[[:space:]]*$//}' ${databaseFasta} > data/${baseName}_cleanHeader.fasta

sed -e '/^>/ s/,.*//' -e '/^>/ s/[[:space:]]*$//' ${databaseFasta} > data/${baseName}_cleanHeader.fasta

makeblastdb -in data/${baseName}_cleanHeader.fasta \
            -dbtype nucl \
            -parse_seqids \
            -out data/db/${baseName}_cleanHeader_db

# makeblastdb -in ${databaseFasta} \
#             -dbtype nucl \
#             -parse_seqids \
#             -out ${baseName}_db


# blastn -query short_query.fasta \
#        -db human_reference_db \
#        -out blast_results.txt \
#        -outfmt 6



#        rand=$HOME/sta/L1Base_Evo/data/randomHg38Sequences.fasta
