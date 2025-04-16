import os
import json

def merge_json_files(input_folder, output_file):
    """
    Fusionne tous les fichiers JSON d'un dossier en un seul fichier JSON.
    Seuls les fichiers dont le nom commence par "sites_ffvl" sont pris en compte.
    
    :param input_folder: Chemin du dossier contenant les fichiers JSON.
    :param output_file: Chemin du fichier JSON de sortie.
    """
    merged_data = []  # Liste pour stocker tous les sites

    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(input_folder):
        # Vérifier si le fichier est un JSON et commence par "sites_ffvl"
        if filename.startswith("sites_ffvl") and filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            try:
                # Charger le contenu du fichier JSON
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):  # Si le fichier contient une liste
                        merged_data.extend(data)
                    elif isinstance(data, dict):  # Si le fichier contient un dictionnaire
                        merged_data.append(data)
                    print(f"✅ Fichier chargé : {filename}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename} : {e}")

    # Écrire les données fusionnées dans le fichier de sortie
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Données fusionnées enregistrées dans : {output_file}")
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier de sortie : {e}")

# Chemin du dossier contenant les fichiers JSON
input_folder = "."

# Chemin du fichier JSON de sortie
output_file = "../balise-tools/merged_sites.json"

# Appeler la fonction pour fusionner les fichiers
merge_json_files(input_folder, output_file)