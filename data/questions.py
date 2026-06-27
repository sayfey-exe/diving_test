# -*- coding: utf-8 -*-
"""
Banque de questions pour les modes "test blanc" et "test examen".

La banque est construite à partir :
  - des 3 questions de chaque fiche (45 questions)
  - de questions supplémentaires définies ci-dessous

Chaque question : {id, chapitre, q, options, correct, explication}
"""

from .content import CHAPITRES


# Questions supplémentaires (au-delà des 3 questions par fiche), pour donner
# de la variété aux tests de 40 questions.
QUESTIONS_SUPP = [
    # --- 1. Pression
    {
        "chapitre": 1,
        "q": "Quelle est la pression absolue à 40 m de profondeur ?",
        "options": ["4 bar", "5 bar", "6 bar", "4,5 bar"],
        "correct": 1,
        "explication": "Pabs = 1 + 40/10 = 5 bar.",
    },
    {
        "chapitre": 1,
        "q": "La pression atmosphérique au niveau de la mer vaut environ :",
        "options": ["0 bar", "1 bar", "2 bar", "10 bar"],
        "correct": 1,
        "explication": "Au niveau de la mer, on prend 1 ATM ≈ 1 bar.",
    },
    # --- 2. Archimède
    {
        "chapitre": 2,
        "q": "Un plongeur a un poids apparent nul. Il est :",
        "options": ["En train de couler", "En train de remonter", "En équilibre (flottabilité nulle)", "Sur-lesté"],
        "correct": 2,
        "explication": "Poids apparent = 0 → flottabilité nulle → équilibre.",
    },
    {
        "chapitre": 2,
        "q": "La poussée d'Archimède est égale :",
        "options": [
            "Au poids du corps immergé",
            "Au poids du volume de liquide déplacé",
            "À la moitié du poids réel",
            "À la pression absolue",
        ],
        "correct": 1,
        "explication": "Poussée d'Archimède = poids du volume de liquide déplacé.",
    },
    # --- 3. Boyle-Mariotte
    {
        "chapitre": 3,
        "q": "Un ballon de 6 L plein d'air à 40 m (5 bar) remonte fermé en surface. Son volume devient :",
        "options": ["6 L", "12 L", "30 L", "1,2 L"],
        "correct": 2,
        "explication": "P1×V1 = P2×V2 → 5×6 = 1×V2 → V2 = 30 L.",
    },
    {
        "chapitre": 3,
        "q": "Les barotraumatismes sont une conséquence directe de quelle loi ?",
        "options": ["Henry", "Dalton", "Boyle-Mariotte", "Archimède"],
        "correct": 2,
        "explication": "Les variations de volume d'air sont régies par Boyle-Mariotte.",
    },
    # --- 4. Autonomie
    {
        "chapitre": 4,
        "q": "Bloc 15 L à 200 b, plongée à 40 m, conso 20 L/min. Quelle est la consommation à 40 m ?",
        "options": ["20 L/min", "60 L/min", "100 L/min", "80 L/min"],
        "correct": 2,
        "explication": "À 40 m, Pabs = 5 bar. Conso = 20 × 5 = 100 L/min.",
    },
    {
        "chapitre": 4,
        "q": "Pour calculer la durée d'autonomie, l'air consommable est :",
        "options": [
            "L'air total, réserve comprise",
            "L'air total moins la réserve",
            "La moitié de l'air total",
            "La pression du bloc",
        ],
        "correct": 1,
        "explication": "On retire la réserve (ex. 50 b × volume) de la quantité d'air totale.",
    },
    # --- 5. Barotraumatismes
    {
        "chapitre": 5,
        "q": "Quel est le barotraumatisme le plus grave ?",
        "options": ["Le plaquage du masque", "Les dents", "La surpression pulmonaire", "L'estomac"],
        "correct": 2,
        "explication": "La surpression pulmonaire est le plus grave, mais aussi le plus facile à éviter.",
    },
    {
        "chapitre": 5,
        "q": "Pour prévenir le plaquage du masque, à la descente il faut :",
        "options": [
            "Faire un Valsalva",
            "Souffler par le nez dans le masque",
            "Retenir sa respiration",
            "Remonter de quelques mètres",
        ],
        "correct": 1,
        "explication": "On souffle de l'air par le nez dans le masque pour compenser la dépression.",
    },
    {
        "chapitre": 5,
        "q": "Les barotraumatismes dépendent-ils de la profondeur et de la durée de plongée ?",
        "options": [
            "Oui, des deux",
            "Non, ils en sont indépendants",
            "Seulement de la profondeur",
            "Seulement de la durée",
        ],
        "correct": 1,
        "explication": "Ils sont indépendants de la durée et de la profondeur ; c'est près de la surface que le risque est le plus fort.",
    },
    # --- 6. Henry
    {
        "chapitre": 6,
        "q": "À la descente, l'état de dissolution est :",
        "options": ["Saturation (P = T)", "Sous-saturation (P > T)", "Sur-saturation (P < T)", "Sursaturation critique"],
        "correct": 1,
        "explication": "À la descente, la pression augmente vite et l'azote se dissout lentement : P > T.",
    },
    {
        "chapitre": 6,
        "q": "La sursaturation critique provoque :",
        "options": [
            "Une meilleure élimination de l'azote",
            "Un dégazage anarchique sous forme de grosses bulles",
            "Une saturation immédiate",
            "Aucune conséquence",
        ],
        "correct": 1,
        "explication": "Quand T ≫ P, l'azote dégaze de façon anarchique en grosses bulles : c'est l'origine de l'ADD.",
    },
    # --- 7. ADD
    {
        "chapitre": 7,
        "q": "Parmi ces symptômes d'ADD, lesquels sont cutanés ?",
        "options": [
            "Les puces et les moutons",
            "Les acouphènes",
            "La paraplégie",
            "Les troubles visuels",
        ],
        "correct": 0,
        "explication": "Les puces (fourmillements, plaques rouges) et les moutons (cloques) sont les atteintes cutanées/sous-cutanées.",
    },
    {
        "chapitre": 7,
        "q": "Quel facteur favorise un accident de décompression ?",
        "options": ["La chaleur", "Le repos complet", "Le froid et l'effort", "Une plongée peu profonde"],
        "correct": 2,
        "explication": "Froid, effort, fatigue, anxiété, hypoglycémie sont des facteurs favorisants.",
    },
    {
        "chapitre": 7,
        "q": "Quelle dose d'aspirine donne-t-on en cas d'ADD (sauf allergie) ?",
        "options": ["0,5 g", "1 g", "2 g", "5 g"],
        "correct": 0,
        "explication": "On propose 0,5 g d'aspirine (sauf allergie), en complément de l'oxygénothérapie.",
    },
    # --- 8. Dalton
    {
        "chapitre": 8,
        "q": "À 30 m, quelle est la pression partielle d'oxygène (air) ?",
        "options": ["0,2 bar", "0,8 bar", "1,6 bar", "3,2 bar"],
        "correct": 1,
        "explication": "À 30 m, Pabs = 4 bar. PpO2 = 4 × 20 % = 0,8 bar.",
    },
    {
        "chapitre": 8,
        "q": "La composition de l'air retenue en plongée est approximativement :",
        "options": ["50 % O2 / 50 % N2", "20 % O2 / 80 % N2", "80 % O2 / 20 % N2", "100 % O2"],
        "correct": 1,
        "explication": "On retient environ 20 % d'oxygène et 80 % d'azote.",
    },
    # --- 9. Toxicité des gaz
    {
        "chapitre": 9,
        "q": "À 40 m, en cas d'essoufflement, que faut-il faire ?",
        "options": [
            "Récupérer sur place",
            "Descendre un peu",
            "Remonter (on ne récupère pas d'un essoufflement à 40 m)",
            "Accélérer la respiration",
        ],
        "correct": 2,
        "explication": "À 40 m on ne récupère pas d'un essoufflement : on remonte.",
    },
    {
        "chapitre": 9,
        "q": "La narcose est principalement due à :",
        "options": [
            "La pression partielle d'azote",
            "Le manque d'oxygène",
            "L'excès d'eau dans les poumons",
            "Le froid",
        ],
        "correct": 0,
        "explication": "La narcose (ivresse des profondeurs) est due à l'élévation de la Pp d'azote (et probablement du CO2).",
    },
    # --- 10. Noyade
    {
        "chapitre": 10,
        "q": "Dans tous les cas de noyade, la première action est :",
        "options": [
            "Donner à boire",
            "Extraire du milieu et alerter les secours",
            "Faire un massage cardiaque systématique",
            "Faire redescendre la victime",
        ],
        "correct": 1,
        "explication": "On extrait du milieu (détendeur en bouche), signe de détresse, appel des secours, réchauffer/rassurer.",
    },
    # --- 11. Tables MN90 1
    {
        "chapitre": 11,
        "q": "Les paliers de décompression se font tous les :",
        "options": ["2 m", "3 m", "5 m", "10 m"],
        "correct": 1,
        "explication": "Les paliers se font de 3 en 3 mètres.",
    },
    {
        "chapitre": 11,
        "q": "Le palier de sécurité recommandé est de :",
        "options": ["3 min à 3 m", "5 min à 5 m", "1 min à 3 m", "10 min à 3 m"],
        "correct": 0,
        "explication": "Le palier de sécurité (de principe) est de 3 minutes à 3 mètres, recommandé même dans la courbe de sécurité.",
    },
    {
        "chapitre": 11,
        "q": "Combien de plongées au maximum les tables MN90 autorisent-elles par 24 h ?",
        "options": ["1", "2", "3", "Illimité"],
        "correct": 1,
        "explication": "Les tables MN90 sont prévues pour 2 plongées au maximum par 24 heures.",
    },
    {
        "chapitre": 11,
        "q": "Si une valeur de profondeur n'existe pas dans la table, on prend :",
        "options": [
            "La valeur inférieure",
            "La valeur immédiatement supérieure",
            "La moyenne des deux",
            "On interpole",
        ],
        "correct": 1,
        "explication": "On prend la valeur immédiatement supérieure : l'interpolation est interdite.",
    },
    # --- 12. Tables MN90 2
    {
        "chapitre": 12,
        "q": "Quel tableau des tables MN90 donne la majoration ?",
        "options": ["Le tableau 1", "Le tableau 2", "Le tableau 3", "Le tableau IV"],
        "correct": 1,
        "explication": "Le tableau 1 donne l'azote résiduel, le tableau 2 donne la majoration.",
    },
    {
        "chapitre": 12,
        "q": "La lettre GPS code :",
        "options": [
            "La profondeur du palier",
            "La quantité d'azote résiduel dans l'organisme",
            "La vitesse de remontée",
            "L'heure de sortie",
        ],
        "correct": 1,
        "explication": "Le GPS (groupe de plongée successive) codifie la quantité d'azote dissous restant après la plongée.",
    },
    # --- 13. Réglementation
    {
        "chapitre": 13,
        "q": "À partir de quel âge peut-on être titulaire du Niveau 2 ?",
        "options": ["12 ans", "14 ans", "16 ans", "18 ans"],
        "correct": 2,
        "explication": "Il faut être âgé d'au moins 16 ans (autorisation du responsable légal pour les mineurs).",
    },
    {
        "chapitre": 13,
        "q": "Un bloc de plongée est soumis à ré-épreuve quand le produit (Pression × Volume) dépasse :",
        "options": ["50 litres", "80 litres", "100 litres", "200 litres"],
        "correct": 1,
        "explication": "Tout récipient dont P × V excède 80 litres est soumis à ré-épreuve.",
    },
    {
        "chapitre": 13,
        "q": "L'assurance responsabilité civile au tiers est :",
        "options": [
            "Facultative",
            "Obligatoire et fournie avec la licence",
            "Réservée aux compétiteurs",
            "Payante en supplément obligatoire",
        ],
        "correct": 1,
        "explication": "La RC au tiers est obligatoire et fournie avec la licence FFESSM ; l'individuelle est facultative mais conseillée.",
    },
    # --- 14. Comportement / sécurité
    {
        "chapitre": 14,
        "q": "Après une plongée, dans combien de temps peut-on prendre l'avion ?",
        "options": ["Immédiatement", "Après 1 h", "Pas avant 12 h", "Pas avant 48 h"],
        "correct": 2,
        "explication": "On ne prend pas l'avion dans les 12 h (12 à 24 h) qui suivent une plongée.",
    },
    {
        "chapitre": 14,
        "q": "Au moindre symptôme d'accident après la plongée, il faut :",
        "options": [
            "Attendre de voir si ça passe",
            "Prévenir immédiatement le directeur de plongée",
            "Replonger pour faire un palier",
            "Prendre un repas",
        ],
        "correct": 1,
        "explication": "Tout symptôme suspect (fatigue intense, fourmillements…) impose de prévenir immédiatement le DP.",
    },
    # --- 15. Matériel
    {
        "chapitre": 15,
        "q": "Quelles sont les contenances standards des bouteilles ?",
        "options": [
            "5 - 10 - 15 - 20 L",
            "6 - 9 - 12 - 15 - 18 L",
            "8 - 16 - 24 L",
            "10 - 12 - 14 L",
        ],
        "correct": 1,
        "explication": "Les contenances standards sont 6, 9, 12, 15 et 18 litres.",
    },
    {
        "chapitre": 15,
        "q": "La vitesse de remontée préconisée par les ordinateurs est généralement :",
        "options": [
            "Plus rapide que les tables (20 m/min)",
            "Identique aux tables (15 m/min)",
            "Plus lente que les tables (8 à 12 m/min)",
            "Sans importance",
        ],
        "correct": 2,
        "explication": "Les ordinateurs imposent souvent une remontée plus lente (8 à 12 m/min) que les 15 m/min des tables.",
    },
    {
        "chapitre": 15,
        "q": "Combien de purges comporte au minimum un gilet stabilisateur ?",
        "options": ["1", "2", "3", "4"],
        "correct": 2,
        "explication": "Le gilet comporte au minimum 3 purges (2 rapides + 1 lente) et 2 mécanismes de gonflage.",
    },
]


def _chapitre_titre(num):
    for c in CHAPITRES:
        if c["num"] == num:
            return c["title"]
    return ""


def build_question_bank():
    """Construit la banque complète : questions des fiches + questions supplémentaires."""
    bank = []
    # 1) Questions issues des fiches
    for chap in CHAPITRES:
        for i, q in enumerate(chap["questions"]):
            bank.append({
                "id": f"c{chap['num']}q{i}",
                "chapitre": chap["num"],
                "chapitre_titre": chap["title"],
                "chapitre_slug": chap["slug"],
                "q": q["q"],
                "options": q["options"],
                "correct": q["correct"],
                "explication": q["explication"],
            })
    # 2) Questions supplémentaires
    for i, q in enumerate(QUESTIONS_SUPP):
        num = q["chapitre"]
        chap = next(c for c in CHAPITRES if c["num"] == num)
        bank.append({
            "id": f"s{i}",
            "chapitre": num,
            "chapitre_titre": chap["title"],
            "chapitre_slug": chap["slug"],
            "q": q["q"],
            "options": q["options"],
            "correct": q["correct"],
            "explication": q["explication"],
        })
    return bank


QUESTION_BANK = build_question_bank()
QUESTION_BY_ID = {q["id"]: q for q in QUESTION_BANK}
