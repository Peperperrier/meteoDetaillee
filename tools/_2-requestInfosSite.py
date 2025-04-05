import json
import requests
from bs4 import BeautifulSoup
import time
import re

def get_orientation_from_wind_sector(wind_sector):
    """
    Convertit le code d'orientation du vent en nom complet
    """
    orientation_map = {
        'N': 'Nord',
        'NE': 'Nord-Est',
        'E': 'Est',
        'SE': 'Sud-Est',
        'S': 'Sud',
        'SO': 'Sud-Ouest',
        'O': 'Ouest',
        'NO': 'Nord-Ouest'
    }
    
    # Extraire la première orientation si plusieurs sont présentes
    if wind_sector:
        # Nettoyer la chaîne et diviser par les séparateurs potentiels
        cleaned = wind_sector.replace("secteurs_vent:", "").strip()
        # recherche si orientation contient des ";"
        if ";" in cleaned:
            orientations = re.split(r'[;,\s]+', cleaned)

        # Prendre la première orientation non vide
        for orientation in orientations:
            if orientation and orientation in orientation_map:
                return orientation_map[orientation]
    
    return None

def extract_data_from_site(site_id):
    """
    Récupère les détails d'un site à partir de son ID
    """
    url = f"https://federation.ffvl.fr/terrain/{site_id}"
    print(f"Récupération des données pour le site {site_id} à partir de {url}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération pour le site {site_id}: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Dictionnaire pour stocker les détails extraits
        details = {}
        
        # Recherche des coordonnées (Latitude, Longitude)
        coords_link = soup.find('a', href=lambda href: href and 'google.com/maps/preview?q=' in href)
        if coords_link:
            # Extraire les coordonnées du texte du lien
            coords_text = coords_link.get_text().strip()
            coords_match = re.search(r'(\d+\.\d+),\s*(\d+\.\d+)', coords_text)
            if coords_match:
                # Arrondir à 4 décimales
                details['latitude'] = round(float(coords_match.group(1)), 4)
                details['longitude'] = round(float(coords_match.group(2)), 4)
            # Alternativement, extraire de l'URL si le texte ne contient pas les coordonnées
            elif 'href' in coords_link.attrs:
                href = coords_link['href']
                coords_match = re.search(r'q=(\d+\.\d+),(\d+\.\d+)', href)
                if coords_match:
                    # Arrondir à 4 décimales
                    details['latitude'] = round(float(coords_match.group(1)), 4)
                    details['longitude'] = round(float(coords_match.group(2)), 4)
        
        # Recherche de l'altitude
        altitude_div = soup.find('div', id='edit-terrain-altitude')
        if altitude_div:
            alt_text = altitude_div.get_text().strip()
            alt_match = re.search(r'Altitude\s*:\s*(\d+)', alt_text)
            if alt_match:
                details['altitude'] = int(alt_match.group(1))
        
        # Recherche des secteurs de vent favorables
        wind_sectors = None
        
        # Tentative 1: recherche d'un élément avec un texte contenant "Secteurs de vent"
        for element in soup.find_all(['div', 'p', 'span']):
            text = element.get_text()
            if 'Secteurs de vent favorables' in text:
                wind_match = re.search(r'Secteurs de vent favorables\s*:\s*(.*?)(?:\n|$)', text)
                if wind_match:
                    wind_sectors = wind_match.group(1).strip()
                    break
        
        if wind_sectors:
            details['secteurs_vent'] = wind_sectors
        
        return details
        
    except Exception as e:
        print(f"Erreur lors de la récupération des détails pour le site {site_id}: {e}")
        return None

def main():
    # Charger le fichier JSON existant
    try:
        with open("sites_ffvl.json", "r", encoding="utf-8") as f:
            sites = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON: {e}")
        return
    
    print(f"Chargement de {len(sites)} sites depuis le fichier JSON.")
    
    # Parcourir chaque site et ajouter les détails supplémentaires
    for i, site in enumerate(sites):
        activite_type = site.get('activite')
        statut_type = site.get('statut')
        if (not 'parapente' in activite_type) or 'atterro' in activite_type or 'interdit' in statut_type or 'non praticable définitivement' in statut_type:
            print(f"Site #{i} n'est pas adapté au décollage en parapente.")
            # flush le site et passe au suivant
            site.clear()
            continue
        else:
            site_id = site.get('id')
            if not site_id:
                print(f"Site #{i} n'a pas d'ID, passage au suivant.")
                continue
            
            print(f"Traitement du site {i+1}/{len(sites)}: {site.get('nom', 'Sans nom')} (ID: {site_id})")
            
            # Récupérer les détails supplémentaires
            details = extract_data_from_site(site_id)
            # Mettre à jour le site avec les nouvelles informations
            site.update(details)
            # if details:
            #     # Mettre à jour le site avec les nouvelles informations
            #     site.update(details)
            #     # Ajouter l'orientation basée sur le premier secteur de vent
            #     if 'secteurs_vent' in details:
            #         orientation = get_orientation_from_wind_sector(details['secteurs_vent'])
            #         if orientation:
            #             site['orientation'] = orientation
            #             print(f"Détails ajoutés: {', '.join(details.keys())}, orientation")
            #         else:
            #             print(f"Détails ajoutés: {', '.join(details.keys())}")
            #     else:
            #         print(f"Détails ajoutés: {', '.join(details.keys())}")
                
            # Charger les données existantes dans le fichier JSON
            try:
                with open("sites_ffvl_details.json", "r", encoding="utf-8") as f:
                    existing_sites = json.load(f)
            except FileNotFoundError:
                existing_sites = []  # Si le fichier n'existe pas, initialisez une liste vide
            except json.JSONDecodeError:
                existing_sites = []  # Si le fichier est corrompu ou vide, initialisez une liste vide
            
            # Ajouter le site traité à la liste
            existing_sites.append(site)
            
            # Écrire la liste mise à jour dans le fichier JSON
            try:
                with open("sites_ffvl_details.json", "w", encoding="utf-8") as f:
                    json.dump(existing_sites, f, ensure_ascii=False, indent=4)
                print(f"✅ Site {site_id} mis à jour et enregistré dans 'sites_ffvl_details.json'")
            except Exception as e:
                print(f"Erreur lors de l'enregistrement du site {site_id} : {e}")

        
        # Pause pour ne pas surcharger le serveur
        if i < len(sites) - 1:  # Pas de pause après le dernier site
            time.sleep(1)
    
    print(f"\nTraitement terminé. Tous les sites ont été mis à jour.")
if __name__ == "__main__":
    main()