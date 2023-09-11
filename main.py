import requests
from bs4 import BeautifulSoup
import json

url = 'https://genshin.honeyhunterworld.com/lisa_006/?lang=EN'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main table by its class name
main_table = soup.find('table', class_='genshin_table main_table')
additional_table = soup.find('table', class_='genshin_table stat_table')  # Add this line to find the additional table
data = []

# Iterate over the rows in the main table
for row in main_table.find_all('tr'):
    # Get all cells in the row
    cells = row.find_all('td')
    if len(cells) == 2:  # Check if the row has exactly two cells (name and value)
        # Extract data from the cells
        name = cells[0].text.strip()
        value = cells[1].text.strip()
        data.append({name: value})

# Extract data from the additional table
additional_data = []
for row in additional_table.find_all('tr'):
    # Get all cells in the row
    cells = row.find_all('td')
    if len(cells) == 9:  # Check if the row has exactly nine cells
        # Extract data from the cells
        level = cells[0].text.strip()
        hp = cells[1].text.strip()
        atk = cells[2].text.strip()
        defense = cells[3].text.strip()
        crit_rate = cells[4].text.strip()
        crit_dmg = cells[5].text.strip()
        bonus_em = cells[6].text.strip()
        materials = cells[7].text.strip()
        total_materials = cells[8].text.strip()

        additional_data.append({
            'Level': level,
            'HP': hp,
            'Attack': atk,
            'Defense': defense,
            'CritRate%': crit_rate,
            'CritDMG%': crit_dmg,
            'Bonus EM': bonus_em,
            'Materials': materials,
            'Total Materials': total_materials
        })

# Combine both sets of data into a single dictionary
result_data = {
    'Main Table': data,
    'Additional Table': additional_data
}

# Save the data as JSON
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=4)

print('Data saved as JSON.')
