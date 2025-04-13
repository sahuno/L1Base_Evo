# python scripts/testgetBed.py --species human --build 8438 --bedtype all


# python scripts/testgetBed.py --species mouse --build 8438 --bedtype all


import os
import argparse
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://l1base.charite.de/l1base.php"
BED_BASE = "http://l1base.charite.de"

SPECIES_NAME_MAP = {
    'human': "Homo sapiens",
    'mouse': "Mus musculus",
}

BUILD_STRING_MAP = {
    # We match these within parentheses, e.g. (Ens84.38)
    '8438': "Ens84.38",
    '3835': "Ens38.35",
}

def parse_section(species, build_str, bed_type, container):
    """
    From a container (the part of the DOM after <h3> for the species),
    find all dataset headings that mention build_str, then collect
    anchor tags that say "BED Track".
    """
    bed_links = []

    # We move through siblings of the <h3> block until we hit the next <h3> (or page end)
    for sibling in container.find_all_next():
        # Stop if we've reached the next <h3> block (another species, basically)
        if sibling.name == 'h3':
            break

        # We're only interested in headings/datasets that mention e.g. "Ens84.38" or "Ens38.35"
        if sibling.name in ['h4', 'h5']:
            heading_text = sibling.get_text(strip=True)
            if build_str not in heading_text:
                continue

            # Collect BED Track links in the content that follows,
            # stopping if we see another heading (h4/h5) or an h3 for the next species
            node = sibling
            while True:
                node = node.next_sibling
                if not node:
                    break
                if hasattr(node, 'name'):
                    # If we see another heading, break
                    if node.name in ['h4','h5','h3']:
                        break
                    # If it's an <a> "BED Track"
                    if node.name == 'a' and 'BED Track' in node.get_text():
                        href = node.get('href', '')
                        # Confirm format
                        if href.startswith('/BED/') and href.endswith('.bed'):
                            # Filter by bed type
                            if bed_type == 'masked' and '_rm' not in href:
                                continue
                            if bed_type == 'unmasked' and '_rm' in href:
                                continue
                            bed_links.append(BED_BASE + href)
                # If it's just text or something else, keep going

    return bed_links

def get_bed_links(species, genome_version, bed_type):
    """
    1. Find the <h3> that says e.g. "Homo sapiens (Human)" or "Mus musculus (Mouse)"
    2. From there, parse the next siblings until the next <h3>,
       collecting all appropriate bed links for the requested build & type.
    """
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    species_string = SPECIES_NAME_MAP[species]
    build_str = BUILD_STRING_MAP[genome_version]  # e.g. "Ens84.38"

    # Find the h3 that includes the species string
    #  e.g. <h3>Homo sapiens (Human)</h3>
    h3 = soup.find('h3', string=lambda t: t and species_string in t)
    if not h3:
        return []

    # Now parse from that h3 downwards
    bed_links = parse_section(species, build_str, bed_type, h3)
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
    parser = argparse.ArgumentParser(description="Download filtered L1Base2 BED files")
    parser.add_argument('--species', choices=['mouse', 'human'], required=True,
                        help="Which species to fetch from L1Base2")
    parser.add_argument('--build', choices=['8438', '3835'], required=True,
                        help="Genome build version (8438 for NCBIm38, 3835 for NCBIm35)")
    parser.add_argument('--bedtype', choices=['all', 'masked', 'unmasked'], default='all',
                        help="Type of BED file: 'all', 'masked' (_rm), or 'unmasked'")
    args = parser.parse_args()

    print(f"\n📥 Fetching {args.bedtype} BED files for {args.species} (build: {args.build})...")
    links = get_bed_links(args.species, args.build, args.bedtype)

    if not links:
        print("❌ No BED links found for the selected filters.")
        return

    output_dir = f"l1base_{args.species}_build{args.build}_{args.bedtype}"
    download_links(links, output_dir)
    print(f"\n✅ Downloaded {len(links)} files to: {output_dir}\n")

if __name__ == '__main__':
    main()