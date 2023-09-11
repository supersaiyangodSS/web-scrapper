import requests
from bs4 import BeautifulSoup
import json

url = 'https://genshin.honeyhunterworld.com/lisa_006/?lang=EN'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables on the page
tables = soup.find_all('table')
data = {}

# Iterate over all tables
for idx, table in enumerate(tables):
    table_data = []
    headers = []

    # Extract table headers if the table has a thead element
    header_row = table.find('thead')
    if header_row:
        header_row = header_row.find('tr')
        header_cells = header_row.find_all('td')
        headers = [cell.text.strip() for cell in header_cells]

    # Find the table body (tbody) if it exists
    body = table.find('tbody')

    if body:
        # Iterate over the rows in the table body
        body_rows = body.find_all('tr')
        for body_row in body_rows:
            cells = body_row.find_all('td')
            row_data = {}

            # Check if the number of cells matches the number of headers
            if len(cells) == len(headers):
                for i in range(len(cells)):
                    name = headers[i]
                    value = cells[i].text.strip()
                    row_data[name] = value

                table_data.append(row_data)

    # Add the table data to the JSON with a key based on the table index
    data[f'Table_{idx + 1}'] = table_data

# Save the data as JSON
with open('tables_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print('Data saved as JSON.')
