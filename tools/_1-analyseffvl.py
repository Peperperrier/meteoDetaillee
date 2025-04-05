import json
from bs4 import BeautifulSoup
import re

def extract_site_id(href_text):
    """Extrait l'ID d'un site à partir du lien href"""
    match = re.search(r'/terrain/(\d+)', href_text)
    if match:
        return match.group(1)
    return None

def parse_html_to_json(html_file_path):
    """Analyse un fichier HTML et extrait les informations des terrains en JSON"""
    
    # Lire le fichier HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Rechercher toutes les lignes de tableau (tr) qui contiennent les données
    # On cherche spécifiquement les lignes contenant un lien vers /terrain/
    sites_data = []
    
    # Trouver tous les liens contenant "/terrain/"
    terrain_links = soup.find_all('a', href=re.compile(r'/terrain/\d+'))
    
    for link in terrain_links:
        # Remonter jusqu'à la ligne du tableau (tr)
        tr = link.find_parent('tr')
        if tr:
            # Récupérer toutes les cellules (td) de cette ligne
            tds = tr.find_all('td')
            
            if len(tds) >= 5:
                # Extraire les données de chaque cellule
                site_link = tds[0].find('a')
                site_name = site_link.text.strip() if site_link else ""
                site_id = extract_site_id(site_link['href']) if site_link and 'href' in site_link.attrs else ""
                
                # Extraire le nom entre crochets si présent
                match = re.search(r'(.*?)\s*\[(.*?)\]', site_name)
                if match:
                    site_name = match.group(1).strip()
                    site_code = match.group(2).strip()
                else:
                    site_code = site_id

                # Créer un dictionnaire avec les données
                site_data = {
                    "id": site_id,
                    "nom": site_name,
                    "code": site_code,
                    "commune": tds[1].text.strip() if len(tds) > 1 else "",
                    "code_postal": tds[2].text.strip() if len(tds) > 2 else "",
                    "activite": tds[3].text.strip() if len(tds) > 3 else "",
                    "statut": tds[4].text.strip() if len(tds) > 4 else ""
                }
                
                sites_data.append(site_data)
    
    # Convertir la liste de dictionnaires en JSON
    json_data = json.dumps(sites_data, ensure_ascii=False, indent=4)
    
    return json_data

def main():
    # Chemin vers le fichier HTML récupéré
    html_file_path = "_0-reponse_ffvl.html"  # Utiliser le fichier sauvegardé précédemment
    
    try:
        # Extraire les données et les convertir en JSON
        json_data = parse_html_to_json(html_file_path)
        
        # Enregistrer le JSON dans un fichier
        with open("sites_ffvl.json", "w", encoding="utf-8") as json_file:
            json_file.write(json_data)
        
        print("Conversion HTML vers JSON réussie!")
        print("Les données ont été enregistrées dans 'sites_ffvl.json'")
        
        # Afficher un exemple des données extraites
        sites = json.loads(json_data)
        if sites:
            print(f"\nExtraction réussie: {len(sites)} site(s) trouvé(s)")
            print("\nExemple du premier site extrait:")
            print(json.dumps(sites[0], ensure_ascii=False, indent=2))
    
    except Exception as e:
        print(f"Une erreur s'est produite lors de la conversion: {e}")

if __name__ == "__main__":
    main()