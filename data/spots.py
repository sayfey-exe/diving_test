# -*- coding: utf-8 -*-
"""
Catalogue des poissons et spots de plongée (carte interactive).

Les photos « officielles » des poissons sont dans static/img/. Les photos de la
communauté sont stockées en base (modèle SpotPhoto).
"""

# Catalogue des poissons (clé → nom, image de référence, description courte).
FISH = {
    "merou": {
        "nom": "Mérou brun",
        "image": "merou.jpeg",
        "desc": "L'emblème de la Méditerranée : curieux, massif et protégé. "
                "Il aime les tombants et les grottes.",
    },
    "barracuda": {
        "nom": "Barracuda",
        "image": "barracuda.jpg",
        "desc": "Prédateur élancé et argenté, souvent en banc immobile en pleine eau.",
    },
    "murene": {
        "nom": "Murène",
        "image": "murene.jpg",
        "desc": "Cachée dans les failles, la bouche ouverte pour respirer. "
                "Impressionnante mais craintive.",
    },
    "dorade": {
        "nom": "Dorade royale",
        "image": "dorade.jpg",
        "desc": "Reconnaissable au reflet doré entre les yeux ; fréquente les fonds sableux.",
    },
    "corb": {
        "nom": "Corb",
        "image": "corbes.jpg",
        "desc": "Poisson sombre aux reflets cuivrés, souvent immobile sous les surplombs.",
    },
    "araignee": {
        "nom": "Araignée de mer",
        "image": "araignee.jpg",
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
