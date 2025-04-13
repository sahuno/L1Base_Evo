import os
import argparse
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://l1base.charite.de/l1base.php"
BED_BASE = "http://l1base.charite.de"

def get_bed_links(species, genome_version, bed_type):
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = []
    
    # Iterate over all anchor tags with "BED Track" in the text
    for a in soup.find_all('a', string=lambda s: s and "BED Track" in s):
        href = a.get('href', '')
        # Only consider valid BED file URLs
        if not (href.startswith('/BED/') and href.endswith('.bed')):
            continue
        
        # Ensure the file name contains the genome build number (e.g. "_8438" or "_3835")
        if f"_{genome_version}" not in href:
            continue
        
        # Try to get context from the nearest table row; if not available, fallback to nearest header
        tr = a.find_parent("tr")
        if tr:
            context_text = tr.get_text(" ", strip=True).lower()
        else:
            header_tag = a.find_previous(lambda tag: tag.name in ['h3','h4','h5'])
            if header_tag:
                context_text = header_tag.get_text(strip=True).lower()
            else:
                continue

        # Check for species match based on context text
        if species.lower() == "human":
            if "human" not in context_text and "homo" not in context_text:
                continue
        elif species.lower() == "mouse":
            if "mouse" not in context_text and "mus" not in context_text:
                continue

        # Check for genome build in context text, if possible
        if genome_version == "8438":
            if ("ens84.38" not in context_text) and ("ens84" not in context_text):
                continue
        elif genome_version == "3835":
            if ("ens38.35" not in context_text) and ("ens38" not in context_text):
                continue

        # Apply BED type filtering
        if bed_type == "masked" and "_rm" not in href:
            continue
        if bed_type == "unmasked" and "_rm" in href:
            continue
        
        full_url = BED_BASE + href
        links.append(full_url)
    return links

def download_links(links, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for url in links:
        filename = os.path.join(output_dir, os.path.basename(url))
        print(f"Downloading: {url}")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

def main():
    parser = argparse.ArgumentParser(description="Download filtered L1Base2 BED files")
    parser.add_argument('--species', choices=['mouse', 'human'], required=True,
                        help="Which species to fetch from L1Base2")
    parser.add_argument('--build', choices=['8438', '3835'], required=True,
                        help="Genome build version (8438 for NCBIm38, 3835 for NCBIm35)")
    parser.add_argument('--bedtype', choices=['all', 'masked', 'unmasked'], default='all',
                        help="Type of BED file: 'all', 'masked' (_rm), or 'unmasked'")
    args = parser.parse_args()
    
    print(f"\nFetching {args.bedtype} BED files for {args.species} (build: {args.build})...")
    links = get_bed_links(args.species, args.build, args.bedtype)
    
    if not links:
        print("No BED links found for the selected filters.")
        return
    
    output_dir = f"l1base_{args.species}_build{args.build}_{args.bedtype}"
    download_links(links, output_dir)
    print(f"\nDownloaded {len(links)} files to: {output_dir}\n")

if __name__ == '__main__':
    main()