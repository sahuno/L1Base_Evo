import os
import argparse
import requests
from bs4 import BeautifulSoup

# # Get all mouse BEDs for NCBIm38
# python scripts/getBedFilesL1Base.py --species mouse

# # Get all BEDs for latest human genome
# python scripts/getBedFilesL1Base.py --species human


#NOTE:
# files with `*_rm.bed` suffix are repeat masked BED files


import os
import argparse
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://l1base.charite.de/l1base.php"
BED_BASE = "http://l1base.charite.de"

# Map species → label to look for in text
SPECIES_LABELS = {
    'mouse': 'Mus musculus',
    'human': 'Homo sapiens',
}

def get_bed_links(species):
    """Scrape L1Base2 page and find BED links for the specified species."""
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    species_label = SPECIES_LABELS[species]
    bed_links = []

    for section in soup.find_all('h3'):
        if species_label in section.get_text():
            for tag in section.find_all_next('a', href=True, limit=10):
                if 'BED Track' in tag.get_text():
                    href = tag['href']
                    if href.endswith('.bed') or 'track.php' in href:
                        bed_links.append(BED_BASE + '/' + href)
            break

    return bed_links

def download_links(links, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for url in links:
        filename = os.path.join(output_dir, os.path.basename(url))
        print(f"Downloading: {url}")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

def main():
    parser = argparse.ArgumentParser(description="Download L1Base2 BED files for Mouse or Human")
    parser.add_argument('--species', choices=['mouse', 'human'], required=True)
    args = parser.parse_args()

    print(f"Fetching BED file links for {args.species}...")
    links = get_bed_links(args.species)

    if not links:
        print("No BED links found.")
        return

    output_dir = f"l1base_{args.species}_bed_files"
    download_links(links, output_dir)
    print(f"Downloaded to: {output_dir}")

if __name__ == "__main__":
    main()