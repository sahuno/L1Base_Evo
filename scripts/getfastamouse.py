import requests
from bs4 import BeautifulSoup

# Build the export URL for mouse LINE-1 repeats.
# In this case, we use the query string parameters that specify:
#   DBN = mmflil1_8438         (mouse database)
#   START = 0                  (starting at the first record)
#   NUM = 50                   (50 entries per page; adjust as needed)
#   SORT = 0                   (sort by ID)
#   f0=0, c0=e, v0=, b0=a       (filter for ID equals blank, which means no filter; 
#                              if the text field is left empty, v0 remains empty)
export_url = (
    "http://l1base.charite.de/exportall.php?"
    "DBN=mmflil1_8438&START=0&NUM=50&SORT=0&f0=0&c0=e&v0=&b0=a"
)

# Prepare the POST data.
# "format": "1" requests FASTA output.
# "dest": "2" indicates that the export should be returned in the response (as opposed to triggering a file download).
post_data = {
    "format": "1",
    "dest": "2"
}

# Send the POST request to obtain the export.
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
        with open("mouse_flActiveLine1.fasta", "w") as f:
            f.write(fasta_text)
        print("FASTA sequences for mouse LINE-1 repeats have been saved as 'mouse_line1.fasta'.")
    else:
        print("Error: Could not find the <pre> tag in the response, check the exported content.")
else:
    print("Error: Received status code", response.status_code)