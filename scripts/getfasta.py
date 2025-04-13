# -*- coding: utf-8 -*-
# $HOME/miniforge3/envs/l1base/bin/python ${HOME}/sta/L1Base_Evo/scripts/getfasta.py

##!/usr/bin/env python


import requests
from bs4 import BeautifulSoup

# Build the full URL for the first 10 IDs
export_url = (
    "http://l1base.charite.de/exportall.php?DBN=hsflil1_8438&START=0&NUM=50&SORT=0&"
    "f0=0&c0=l&v0=11&b0=a"
)

# Prepare the POST data for FASTA format output.
post_data = {
    "format": "1",  # FASTA format
    "dest": "2"     # Window; direct output in response
}

# Send the POST request
response = requests.post(export_url, data=post_data)


if response.status_code == 200:
    html_content = response.text
    # Use BeautifulSoup to parse the HTML response.
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <pre> tags (the export window typically encloses FASTA text within <pre> elements).
    pre_tags = soup.find_all("pre")
    if pre_tags:
        # Pick the inner-most <pre> block (normally the last one).
        fasta_text = pre_tags[-1].get_text()
        # Remove any extraneous characters by locating the first ">" which should mark the FASTA header.
        header_index = fasta_text.find('>')
        if header_index != -1:
            fasta_text = fasta_text[header_index:]
        # Save the cleaned FASTA sequences to a file.
        with open("data/first10_ids_clean.fasta", "w") as f:
            f.write(fasta_text)
        print("Clean FASTA sequences for the first 10 IDs have been saved in 'first10_ids_clean.fasta'.")
    else:
        print("Error: Could not find the <pre> tag in the response, check the exported content.")
else:
    print("Error: Received status code", response.status_code)