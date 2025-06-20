import json

def apply_corrections(sites_file, corrections_file, output_file):
    """
    Applique des corrections aux noms et orientations des sites dans un fichier JSON.
    Permet également de supprimer des sites si le paramètre "supprimer" est défini sur True.
    
    :param sites_file: Chemin du fichier JSON contenant les sites (merged_sites_with_balises.json).
    :param corrections_file: Chemin du fichier JSON contenant les corrections (corrections.json).
    :param output_file: Chemin du fichier JSON de sortie avec les corrections appliquées.
    """
    # Charger les fichiers JSON
    with open(sites_file, "r", encoding="utf-8") as f:
        sites = json.load(f)
    
    with open(corrections_file, "r", encoding="utf-8") as f:
        corrections = json.load(f)
    
    # Liste pour stocker les sites à conserver
    updated_sites = []

    # Appliquer les corrections
    for site in sites:
        # Vérifier si le site doit être corrigé ou supprimé
        site_modified = False
        for correction in corrections:
            nom_actuel = correction.get("nom_actuel", "").lower()  # Convertir en minuscule pour éviter les problèmes de casse
            nouveau_nom = correction.get("nouveau_nom")
            nouvelle_orientation = correction.get("nouvelle_orientation")
            supprimer = correction.get("supprimer", False)  # Par défaut, ne pas supprimer
            
            if site.get("nom", "").lower() == nom_actuel:  # Comparer les noms en minuscule
                if supprimer:
                    print(f"🗑️ Site supprimé : {nom_actuel}")
                    site_modified = True  # Marquer le site comme modifié pour ne pas l'ajouter
                    break  # Ne pas ajouter ce site à la liste mise à jour
                if nouveau_nom:
                    site["nom"] = nouveau_nom
                if nouvelle_orientation:
                    site["orientation"] = nouvelle_orientation
                print(f"✅ Correction appliquée : {nom_actuel} -> {nouveau_nom}, Orientation : {nouvelle_orientation}")
                site_modified = True  # Marquer le site comme modifié
                break
        
        # Ajouter le site corrigé ou non modifié à la liste mise à jour
        if not site_modified or not supprimer:
            updated_sites.append(site)
    
    # Sauvegarder les sites corrigés dans le fichier de sortie
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(updated_sites, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Les corrections ont été appliquées et enregistrées dans : {output_file}")


# Chemins des fichiers
sites_file = "./merged_sites_with_balises.json"
corrections_file = "./corrections.json"
output_file = "./merged_sites_with_balises_corrected.json"

# Appliquer les corrections
apply_corrections(sites_file, corrections_file, output_file)