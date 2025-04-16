from bs4 import BeautifulSoup
import json
import time

def extract_active_balises(html_content):
    # Parse the HTML content
    with open(html_content, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    # Find the table containing the balise data
    table = soup.find('table', {'border': '1', 'cellspacing': '0', 'cellpadding': '1'})
    if not table:
        print("❌ Table not found in the HTML content.")
        time.sleep(10)
        return []
    
    # Initialize the result list
    result = []
    
    # Iterate through each row in the table (skip the header row)
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) < 9:
            continue
            
        # Check if the row has a green background (#00FF00) indicating active status
        if cells[0].get('bgcolor') == '#00FF00':
            # Extract the URL and name
            url_cell = cells[1].find('a', href=True)
            name_cell = cells[3].find('a', href=True)
            
            if url_cell and name_cell:
                url = url_cell['href']
                name = name_cell.text.strip()
                result.append({
                    'url': url,
                    'nom': name
                })
    
    return result

# Example usage with the provided HTML
# html_content = '''(your HTML content here)'''
# active_balises = extract_active_balises(html_content)
# print(active_balises)
# Exemple d'utilisation
html_content = "./_4-response.html"
output_json_file = "./balises.json"

# Extraire les balises et les sites
balises_and_sites = extract_active_balises(html_content)

# Enregistrer les résultats dans un fichier JSON
with open(output_json_file, "w", encoding="utf-8") as f:
    json.dump(balises_and_sites, f, ensure_ascii=False, indent=4)

print(f"✅ Les résultats ont été enregistrés dans le fichier : {output_json_file}")