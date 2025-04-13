# author: samuel ahuno
# purpose: lineages of active line1 in l1Base.
# goals: 
1. are all the ative human line1 L1PA1(L1HS)?
2. how does repeat masker LINE1 relae to this? 
3. can you find the evolutionary age of active line1?


## install softwares
`$ mamba env create -f environment.yml`

## Run
```
#get fasta files from L1Base
python scripts/getfastamouse.py

# build multiple sequecne alignmenet and phylogeny2
python scripts/build_phylogeny.py --unaligned mouse_flActiveLine1.fasta --plot
```
