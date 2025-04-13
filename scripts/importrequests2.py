import requests
from bs4 import BeautifulSoup
import pandas as pd

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

if response.status_code == 200:
    # Parse the returned HTML to extract data
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Attempt to find the result table
    table = soup.find("table")
    if table:
        # Extract rows from <thead> if available (usually for headers) and <tbody> (for data)
        header = []
        if table.find("thead"):
            header_row = table.find("thead").find("tr")
            if header_row:
                header = [cell.get_text(strip=True) for cell in header_row.find_all(["th", "td"])]
                
        # Otherwise, assume the first <tr> is the header
        rows = table.find_all("tr")
        if not header and rows:
            header = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]
            data_rows_html = rows[1:]
        else:
            data_rows_html = table.find("tbody").find_all("tr") if table.find("tbody") else rows

        data = []
        for row in data_rows_html:
            # Process rows that have cells (<td> or <th>)
            cells = row.find_all(["td", "th"])
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells]
                # Avoid adding the header row twice if it's already been captured
                if row_data != header:
                    data.append(row_data)
        
        if header and data:
            # Create a DataFrame from the header and the data rows
            df = pd.DataFrame(data, columns=header)
            # Render the DataFrame as a Markdown table (requires the 'tabulate' package)
            print(df.to_markdown(index=False))
            # Alternatively, you can just display the DataFrame with:
            # print(df)
        else:
            print("No data rows were found for ID == 1. Possibly the record doesn't exist or the structure changed.")
    else:
        print("No table found in the HTML; check if the structure of the page has changed.")
else:
    print("Error: Received status code", response.status_code)