# -*- coding: utf-8 -*-
"""
Catalogue des poissons et spots de plongée (carte interactive).

Les photos « officielles » des poissons sont dans static/img/. Les photos de la
communauté sont stockées en base (modèle SpotPhoto).
"""

# Catalogue des espèces de référence (clé → fiche). Ces espèces sont « validées »
# d'office (source=seed). La communauté et la reconnaissance automatique peuvent
# enrichir ce catalogue avec de nouvelles espèces (voir modèle Species).
# `signal` = clé d'un signe de plongée (voir data/signals.py) quand il en existe un.
FISH = {
    "merou": {
        "nom": "Mérou brun",
        "nom_scientifique": "Epinephelus marginatus",
        "image": "merou.jpeg",
        "categorie": "poisson",
        "habitat": "Tombants rocheux, grottes et failles, 5–50 m",
        "taille": "Jusqu'à 1,5 m et 60 kg",
        "signal": "merou",
        "desc": "L'emblème de la Méditerranée : curieux, massif et protégé. "
                "Il aime les tombants et les grottes.",
    },
    "barracuda": {
        "nom": "Barracuda",
        "nom_scientifique": "Sphyraena viridensis",
        "image": "barracuda.jpg",
        "categorie": "poisson",
        "habitat": "Pleine eau, souvent en banc près des secs et tombants",
        "taille": "60 cm à 1,2 m",
        "signal": None,
        "desc": "Prédateur élancé et argenté, souvent en banc immobile en pleine eau.",
    },
    "murene": {
        "nom": "Murène",
        "nom_scientifique": "Muraena helena",
        "image": "murene.jpg",
        "categorie": "poisson",
        "habitat": "Failles et trous rocheux, 3–40 m",
        "taille": "80 cm à 1,3 m",
        "signal": "murene",
        "desc": "Cachée dans les failles, la bouche ouverte pour respirer. "
                "Impressionnante mais craintive.",
    },
    "dorade": {
        "nom": "Dorade royale",
        "nom_scientifique": "Sparus aurata",
        "image": "dorade.jpg",
        "categorie": "poisson",
        "habitat": "Fonds sableux et herbiers, 5–30 m",
        "taille": "30 à 60 cm",
        "signal": None,
        "desc": "Reconnaissable au reflet doré entre les yeux ; fréquente les fonds sableux.",
    },
    "corb": {
        "nom": "Corb",
        "nom_scientifique": "Sciaena umbra",
        "image": "corbes.jpg",
        "categorie": "poisson",
        "habitat": "Surplombs et entrées de grottes, 5–35 m",
        "taille": "30 à 50 cm",
        "signal": None,
        "desc": "Poisson sombre aux reflets cuivrés, souvent immobile sous les surplombs.",
    },
    "araignee": {
        "nom": "Araignée de mer",
        "nom_scientifique": "Maja squinado",
        "image": "araignee.jpg",
        "categorie": "invertébré",
        "habitat": "Fonds rocheux et herbiers de posidonie, 5–50 m",
        "taille": "Carapace jusqu'à 20 cm",
        "signal": None,
        "desc": "Grand crabe aux longues pattes, sur les fonds rocheux et les herbiers.",
    },
}

# Spots de plongée (coordonnées approximatives). Le premier sert de spot de
# référence : les photos fournies proviennent de Morsiglia (Cap Corse).
SPOTS = [
    {
        "id": "morsiglia",
        "nom": "Morsiglia",
        "lieu": "Cap Corse, Haute-Corse",
        "lat": 42.9850, "lon": 9.3550,
        "profondeur": "5 – 40 m",
        "desc": "Spot sauvage du nord du Cap Corse : tombants, herbiers de posidonie "
                "et faune méditerranéenne emblématique.",
        "poissons": ["merou", "barracuda", "murene", "dorade", "corb", "araignee"],
    },
    {
        "id": "port-cros",
        "nom": "Parc national de Port-Cros",
        "lieu": "Îles d'Hyères, France",
        "lat": 43.0092, "lon": 6.3906,
        "profondeur": "5 – 40 m",
        "desc": "Réserve marine mythique, réputée pour ses mérous curieux qui viennent "
                "à la rencontre des plongeurs.",
        "poissons": ["merou", "barracuda", "corb", "murene", "dorade"],
    },
    {
        "id": "medes",
        "nom": "Îles Medes",
        "lieu": "Costa Brava, Espagne",
        "lat": 42.0468, "lon": 3.2237,
        "profondeur": "6 – 35 m",
        "desc": "Réserve protégée aux tombants et grottes riches en vie.",
        "poissons": ["merou", "murene", "corb", "dorade"],
    },
    {
        "id": "scandola",
        "nom": "Réserve de Scandola",
        "lieu": "Corse, France",
        "lat": 42.3667, "lon": 8.5667,
        "profondeur": "5 – 40 m",
        "desc": "Falaises rouges classées à l'UNESCO et faune méditerranéenne abondante.",
        "poissons": ["merou", "murene", "corb", "barracuda"],
    },
    {
        "id": "calanques",
        "nom": "Calanques de Marseille",
        "lieu": "Bouches-du-Rhône, France",
        "lat": 43.2119, "lon": 5.4487,
        "profondeur": "8 – 40 m",
        "desc": "Tombants et secs spectaculaires à quelques minutes de la ville.",
        "poissons": ["dorade", "barracuda", "murene", "araignee"],
    },
    {
        "id": "lavezzi",
        "nom": "Îles Lavezzi",
        "lieu": "Bonifacio, Corse",
        "lat": 41.3419, "lon": 9.2558,
        "profondeur": "5 – 30 m",
        "desc": "Chaos granitiques et eaux translucides, idéal pour l'exploration.",
        "poissons": ["merou", "barracuda", "dorade", "araignee"],
    },
    {
        "id": "cap-creus",
        "nom": "Cap de Creus",
        "lieu": "Catalogne, Espagne",
        "lat": 42.3190, "lon": 3.3200,
        "profondeur": "6 – 35 m",
        "desc": "Pointe sauvage battue par la tramontane, tombants et posidonies.",
        "poissons": ["dorade", "barracuda", "araignee", "corb"],
    },
]

SPOT_BY_ID = {s["id"]: s for s in SPOTS}
