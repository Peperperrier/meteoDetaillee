import json
import math

# Table de correspondance des orientations cardinales en degrés
ORIENTATION_TO_DEGREES = {
    "N": 0,
    "NE": 45,
    "E": 90,
    "SE": 135,
    "S": 180,
    "SO": 225,
    "O": 270,
    "NO": 315
}

# Table inverse pour convertir des degrés en orientations cardinales
DEGREES_TO_ORIENTATION = {v: k for k, v in ORIENTATION_TO_DEGREES.items()}

def get_average_orientation(orientations):
    """
    Calcule la moyenne des orientations cardinales.
    :param orientations: Liste des orientations (ex: ["N", "SE", "S", "SO", "O", "NO"])
    :return: Orientation moyenne (ex: "S")
    """
    if not orientations:
        return None

    # Convertir les orientations en radians
    radians = [math.radians(ORIENTATION_TO_DEGREES[orientation]) for orientation in orientations if orientation in ORIENTATION_TO_DEGREES]

    # Calculer les moyennes des coordonnées x et y sur le cercle trigonométrique
    x = sum(math.cos(r) for r in radians) / len(radians)
    y = sum(math.sin(r) for r in radians) / len(radians)

    # Calculer l'angle moyen en radians
    average_radians = math.atan2(y, x)

    # Convertir l'angle moyen en degrés
    average_degrees = math.degrees(average_radians) % 360

    # Trouver l'orientation cardinale la plus proche
    closest_orientation = min(DEGREES_TO_ORIENTATION.keys(), key=lambda d: abs(d - average_degrees))
    return DEGREES_TO_ORIENTATION[closest_orientation]

def extract_orientation(secteurs_vent):
    """
    Extrait l'orientation à partir du champ 'secteurs_vent'.
    Récupère uniquement les données avant 'Secteurs de vent défavorables'.
    """
    if not secteurs_vent:
        return None

    # Diviser le texte au niveau de "Secteurs de vent défavorables"
    parts = secteurs_vent.split("Secteurs de vent défavorables")
    if len(parts) > 0:
        # Retourner la partie avant "Secteurs de vent défavorables", en supprimant les espaces inutiles
        return parts[0].strip()
    return None

# Charger les données JSON
with open("sites_ffvl_details.json", "r", encoding="utf-8") as f:
    sites = json.load(f)

# Ajouter le champ 'orientation' à chaque site
for site in sites:
    secteurs_vent = site.get("secteurs_vent", "")
    orientation = extract_orientation(secteurs_vent)
    site["orientation_all"] = orientation
    # recherche uniquement si ne contient pas "non" dans orientation    
    if not (orientation and "non" not in orientation.lower()):
        site["orientation"] = None
    else:
        if "orientation_all" in site:
            orientations = site["orientation_all"].split(";")
            site["orientation"] = get_average_orientation(orientations)

        # Concaténer l'orientation moyenne au champ 'nom'
        if site["orientation"]:
            site["nom"] = f"{site['nom']} ({site['orientation']})"
        
# Sauvegarder les données mises à jour
with open("sites_ffvl_details.json", "w", encoding="utf-8") as f:
    json.dump(sites, f, ensure_ascii=False, indent=4)

print("Les données ont été mises à jour avec la moyenne des orientations.")