import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a request to the website
url = "https://www.fantasypros.com/nfl/stats/qb.php"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the webpage.")
else:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Locate the table containing the data
table = soup.find("table", {"id": "data"})

# Extract the headers from the table
headers = [th.text for th in table.find("thead").find_all("th")]

# Extract the rows from the table body
rows = []
for tr in table.find("tbody").find_all("tr"):
    row = [td.text.strip() for td in tr.find_all("td")]
    rows.append(row)

# Create a DataFrame from the extracted data
df = pd.DataFrame(rows, columns=headers)

# Display or save the data
print(df.head())  # Print the first few rows

# Optional: Save to a CSV file
df.to_csv("quarterback_stats.csv", index=False)
print("Data saved to 'quarterback_stats.csv'")
