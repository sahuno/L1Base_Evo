#Download L1 from L1Base 
import requests
import argparse

# # python scripts/getTableL1Base.py --species human --id_limit 10
# python scripts/getTableL1Base.py --species mouse --id_limit 10
# Add argparse to make IDLimit configurable
parser = argparse.ArgumentParser(description="Download L1 data from L1Base")
parser.add_argument("--id_limit", type=int, default=2811, help="Limit for the ID query parameter; 2811+1 for mouse, 146+1 for human")
parser.add_argument("--species", type=str, choices=["human", "mouse"], required=True, help="Species to query: 'human' or 'mouse'")
args = parser.parse_args()

# Use the argument value for IDLimit
IDLimit = args.id_limit

# Determine the URL based on the species argument
if args.species == "human":
    url = f"http://l1base.charite.de/exportall.php?DBN=hsflil1_8438&START=0&NUM=50&SORT=0&f0=0&c0=l&v0={IDLimit}&b0=a"
elif args.species == "mouse":
    url = f"http://l1base.charite.de/exportall.php?DBN=mmflil1_8438&START=0&NUM=50&SORT=0&f0=0&c0=l&v0={IDLimit}&b0=a"

# The form fields according to the HTML:
#  - "format": "3" corresponds to CSV (options: 1 = Fasta, 2 = GenBank, 3 = CSV)
#  - "dest": "1" corresponds to saving as a file (option "1: File", "2: Window")
payload = {
    "format": "3",
    "dest": "1"
}

# Send a POST request to the export URL with the form data
response = requests.post(url, data=payload)
response.raise_for_status()  # Check that the request was successful

# Update the CSV filename to reflect species and ID limit
csv_filename = f"l1bbase_data_export_{args.species}_{IDLimit}.csv"
with open(csv_filename, "wb") as f:
    f.write(response.content)

print(f"CSV export downloaded and saved as '{csv_filename}'.")