import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_balise_data(department):
    """Fetch balise data from balisemeteo.com for a specific department."""
    url = f"https://www.balisemeteo.com/depart.php?dept={department}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Erreur lors de la récupération des données pour le département {department}: {e}")
        return None

def extract_active_balises(html_content):
    """Extract active balises from HTML content."""
    # Si html_content est une chaîne de caractères, pas besoin d'ouvrir un fichier
    if isinstance(html_content, str):
        soup = BeautifulSoup(html_content, "html.parser")
    else:
        # Ancien comportement pour les fichiers
        with open(html_content, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    
    # ... reste du code existant pour extract_active_balises ...
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

def process_department(department):
    """Process a single department and save its data"""
    print(f"📍 Traitement du département {department}")
    output_json_file = f"./balises_{department}.json"
    
    # Récupérer les données depuis le site web
    html_content = fetch_balise_data(department)
    
    if html_content:
        # Extraire les balises et les sites
        balises_and_sites = extract_active_balises(html_content)
        
        # Enregistrer les résultats dans un fichier JSON
        with open(output_json_file, "w", encoding="utf-8") as f:
            json.dump(balises_and_sites, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Résultats enregistrés dans : {output_json_file}")
        return True
    return False

# Programme principal
departments = ["07", "43", "42", "48", "15", "63", "69", "26"]  # Liste des départements à traiter
successful_depts = []
failed_depts = []

for dept in departments:
    if process_department(dept):
        successful_depts.append(dept)
    else:
        failed_depts.append(dept)
    time.sleep(1)  # Pause d'une seconde entre chaque requête pour éviter la surcharge du serveur

# Afficher le résumé
print("\n📊 Résumé du traitement :")
print(f"✅ Départements traités avec succès ({len(successful_depts)}): {', '.join(successful_depts)}")
if failed_depts:
    print(f"❌ Départements en échec ({len(failed_depts)}): {', '.join(failed_depts)}")

