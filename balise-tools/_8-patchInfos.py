import json

def apply_corrections(sites_file, corrections_file, output_file):
    """
    Applique des corrections aux noms et orientations des sites dans un fichier JSON.
    
    :param sites_file: Chemin du fichier JSON contenant les sites (merged_sites_with_balises.json).
    :param corrections_file: Chemin du fichier JSON contenant les corrections (corrections.json).
    :param output_file: Chemin du fichier JSON de sortie avec les corrections appliquées.
    """
    # Charger les fichiers JSON
    with open(sites_file, "r", encoding="utf-8") as f:
        sites = json.load(f)
    
    with open(corrections_file, "r", encoding="utf-8") as f:
        corrections = json.load(f)
    
    # Appliquer les corrections
    for correction in corrections:
        nom_actuel = correction.get("nom_actuel")
        nouveau_nom = correction.get("nouveau_nom")
        nouvelle_orientation = correction.get("nouvelle_orientation")
        
        # Rechercher le site correspondant
        for site in sites:
            if site.get("nom") == nom_actuel:
                # Appliquer les corrections
                if nouveau_nom:
                    site["nom"] = nouveau_nom
                if nouvelle_orientation:
                    site["orientation"] = nouvelle_orientation
                print(f"✅ Correction appliquée : {nom_actuel} -> {nouveau_nom}, Orientation : {nouvelle_orientation}")
                break
        else:
            print(f"⚠️ Site non trouvé : {nom_actuel}")
    
    # Sauvegarder les sites corrigés dans le fichier de sortie
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Les corrections ont été appliquées et enregistrées dans : {output_file}")


# Chemins des fichiers
sites_file = "./merged_sites_with_balises.json"
corrections_file = "./corrections.json"
output_file = "./merged_sites_with_balises_corrected.json"

# Appliquer les corrections
apply_corrections(sites_file, corrections_file, output_file)