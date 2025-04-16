import json
import re
import time
def add_balises_to_sites(sites_file, balises_file, output_file):
    """
    Ajoute les balises disponibles aux sites dans le fichier merged_sites.json.
    
    :param sites_file: Chemin du fichier JSON contenant les sites (merged_sites.json).
    :param balises_file: Chemin du fichier JSON contenant les balises (balises_example.json).
    :param output_file: Chemin du fichier JSON de sortie avec les balises ajoutées.
    """
    # Charger les fichiers JSON
    with open(sites_file, "r", encoding="utf-8") as f:
        sites = json.load(f)
    
    with open(balises_file, "r", encoding="utf-8") as f:
        balises = json.load(f)
    
    # Parcourir chaque site et vérifier si une balise correspond
    for site in sites:
        site_name = site.get("nom", "").lower().replace("-", " ").replace("saint", "st").replace("é", "e")
        print(f"Traitement du site : {site_name}")

        # Conserver les balises existantes si présentes
        existing_balises = site.get("balise", [])
        if isinstance(existing_balises, str):  # Si c'est une seule balise sous forme de string
            existing_balises = [existing_balises]
        site["balise"] = existing_balises.copy()  # Initialiser avec les balises existantes
        
        for balise in balises:
            balise_name = balise.get("nom", "").lower().replace("-", " ").replace("saint", "st").replace("é", "e")
            if balise_name in site_name:
                print(f"✅balise trouvée: {balise_name}")
                if balise["url"] not in site["balise"]:  # Éviter les doublons
                    site["balise"].append(balise["url"])
        
        # Supprimer le champ "balise" uniquement si aucune balise n'est présente
        if not site["balise"]:
            del site["balise"]
        else:
            # Ajouter l'émoji au nom du site s'il a au moins une balise
            if not site["nom"].endswith("🚩"):  # Éviter d'ajouter l'émoji plusieurs fois
                site["nom"] = f"{site['nom']} 🚩"

    # Vérifier et remplacer les URLs spécifiques
    replace_specific_url(sites)
    
    # Sauvegarder les sites mis à jour dans le fichier de sortie
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Les balises ont été ajoutées et enregistrées dans : {output_file}")


def replace_specific_url(sites):
    """
    Vérifie et remplace les URLs qui commencent par "https://intranet.ffvl.fr/structure/"
    en les transformant en "https://www.balisemeteo.com/balise.php?idBalise=" tout en
    conservant uniquement le dernier chiffre.
    
    :param sites: Liste des sites contenant les balises.
    """
    for site in sites:
        if "balise" in site:
            # Remplacer les URLs qui correspondent au modèle
            updated_balises = []
            for url in site["balise"]:
                if url.startswith("https://intranet.ffvl.fr/structure/"):
                    # Extraire le dernier chiffre de l'URL
                    match = re.search(r"/(\d+)$", url)
                    if match:
                        balise_id = match.group(1)
                        # Construire la nouvelle URL
                        new_url = f"https://www.balisemeteo.com/balise.php?idBalise={balise_id}"
                        updated_balises.append(new_url)
                    else:
                        updated_balises.append(url)  # Conserver l'URL d'origine si aucun ID trouvé
                else:
                    updated_balises.append(url)  # Conserver l'URL d'origine si elle ne correspond pas
            site["balise"] = updated_balises


# Chemins des fichiers
sites_file = "./merged_sites.json"
balises_file = "./balises_full.json"
output_file = "./merged_sites_with_balises.json"

# Ajouter les balises aux sites
add_balises_to_sites(sites_file, balises_file, output_file)