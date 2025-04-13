import requests
import pandas as pd
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup


# Define the URL for the results page (show.php is the script that displays query results)
url = "http://l1base.charite.de/show.php"

# Set parameters to specify the query for "ID equals 1"
params = {
    "DBN": "hsflil1_8438",  # Database identifier
    "START": "0",           # Start index (if applicable)
    "f0": "0",              # Field 0 corresponds to ID (as defined by the form's first select)
    "c0": "e",              # "e" stands for equals
    "v0": "1",              # The value we are searching for
    # The rest of the parameters (f1, c1, v1, etc.) can be left out if not needed
}

# Send GET request to show.php with these parameters
response = requests.get(url, params=params)

# Ensure the request succeeded
if response.status_code == 200:
    # Parse the returned HTML to extract data
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Attempt to find the result table
    table = soup.find("table")
    if table:
        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if tbody else table.find_all("tr")
        data_found = False
        for row in rows:
            # Process only rows that have <td> cells (data rows typically use <td>)
            cells = row.find_all("td")
            if cells:
                data_found = True
                # Print a list of cell texts
                row_data = [cell.get_text(strip=True) for cell in cells]
                print(row_data)
        if not data_found:
            print("No data rows were found for ID == 1. Possibly the record doesn't exist or it’s not returning any data.")
    else:
        print("No table found in the HTML; check if the structure of the page has changed.")
else:
    print("Error: Received status code", response.status_code)

print("\nscript")
print(rows)
print("End of script")