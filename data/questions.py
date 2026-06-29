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


# Questions issues des EXERCICES du cours (calculs + méthode des tables MN90).
# Les exercices de calcul sont chiffrés ; les exercices de tables portent sur la
# méthode (valeurs à retenir, classification, tableaux), toujours vérifiables.
EXERCICE_QUESTIONS = [
    # --- Calcul d'autonomie (ch.4)
    {
        "chapitre": 4,
        "q": "Bloc de 15 L à 200 bar, plongée à 40 m, consommation 20 L/min en surface, "
             "réserve 50 bar. Au bout de combien de temps passe-t-on sur réserve ?",
        "options": ["18 min", "22,5 min", "30 min", "45 min"],
        "correct": 1,
        "explication": "Air consommable = (200−50)×15 = 2250 L ; conso à 40 m = 20×5 = 100 L/min ; "
                       "2250 ÷ 100 = 22,5 min.",
    },
    {
        "chapitre": 4,
        "q": "Bloc de 12 L à 200 bar, plongée à 20 m, consommation 18 L/min, réserve 50 bar. "
             "Quelle est l'autonomie avant la réserve ?",
        "options": ["18 min", "≈ 25 min", "≈ 33 min", "≈ 50 min"],
        "correct": 2,
        "explication": "Air consommable = (200−50)×12 = 1800 L ; conso à 20 m = 18×3 = 54 L/min ; "
                       "1800 ÷ 54 ≈ 33 min.",
    },
    # --- Pression (ch.1)
    {
        "chapitre": 1,
        "q": "Quelle est la pression absolue à 33 m de profondeur ?",
        "options": ["3,3 bar", "4 bar", "4,3 bar", "5 bar"],
        "correct": 2,
        "explication": "Pabs = 1 + 33/10 = 4,3 bar.",
    },
    {
        "chapitre": 1,
        "q": "À quelle profondeur la pression absolue vaut-elle 3,5 bar ?",
        "options": ["15 m", "25 m", "35 m", "2,5 m"],
        "correct": 1,
        "explication": "Phyd = 3,5 − 1 = 2,5 bar → profondeur = 25 m.",
    },
    # --- Boyle-Mariotte (ch.3)
    {
        "chapitre": 3,
        "q": "Un ballon souple contient 10 L d'air en surface. Quel sera son volume à 20 m ?",
        "options": ["10 L", "≈ 3,3 L", "5 L", "30 L"],
        "correct": 1,
        "explication": "1×10 = 3×V2 → V2 = 10/3 ≈ 3,3 L (Pabs = 3 bar à 20 m).",
    },
    # --- Dalton (ch.8)
    {
        "chapitre": 8,
        "q": "En plongée à l'air (21 % d'O2), à quelle profondeur la PpO2 atteint-elle 1,6 bar ?",
        "options": ["environ 40 m", "environ 50 m", "environ 66 m", "environ 80 m"],
        "correct": 2,
        "explication": "Pabs = 1,6 / 0,21 ≈ 7,6 bar → profondeur ≈ (7,6−1)×10 ≈ 66 m.",
    },
    # --- Tables MN90 partie 1 (ch.11) : méthode
    {
        "chapitre": 11,
        "q": "Pour une plongée à 21 m, quelle profondeur retient-on pour entrer dans la table MN90 ?",
        "options": ["20 m", "21 m", "22 m", "25 m"],
        "correct": 2,
        "explication": "21 m n'existe pas dans la table → on prend la valeur immédiatement supérieure : 22 m.",
    },
    {
        "chapitre": 11,
        "q": "Pour une plongée à 34 m, quelle profondeur retient-on dans la table MN90 ?",
        "options": ["30 m", "34 m", "35 m", "40 m"],
        "correct": 2,
        "explication": "34 m n'existe pas → valeur immédiatement supérieure : 35 m.",
    },
    {
        "chapitre": 11,
        "q": "Une durée de plongée de 41 min n'existe pas dans la table. Quelle durée retient-on ?",
        "options": ["40 min", "41 min", "45 min", "On interpole"],
        "correct": 2,
        "explication": "On prend la durée immédiatement supérieure : 45 min (jamais d'interpolation).",
    },
    {
        "chapitre": 11,
        "q": "Remontée rapide depuis 20 m : à quelle profondeur faut-il redescendre, et pour quel palier ?",
        "options": [
            "À 10 m, palier de 5 min",
            "À 3 m, palier de 2 min",
            "À 15 m, palier de 3 min",
            "On ne redescend pas",
        ],
        "correct": 0,
        "explication": "On redescend à la mi-profondeur (10 m) en moins de 3 min pour un palier de 5 min, "
                       "puis au moins 2 min à 3 m.",
    },
    {
        "chapitre": 11,
        "q": "Lors d'une remontée lente (ex. de 22 à 17 m en 5 min), que fait-on de cette durée ?",
        "options": [
            "On l'ignore",
            "On l'intègre à la durée de plongée (DP)",
            "On la retire de la DP",
            "On la compte comme un palier",
        ],
        "correct": 1,
        "explication": "La durée de la remontée lente s'ajoute à la durée de plongée pour le calcul des paliers.",
    },
    {
        "chapitre": 11,
        "q": "Palier interrompu : quelle est la conduite à tenir ?",
        "options": [
            "Remonter directement en surface",
            "Refaire seulement la moitié du palier",
            "Redescendre au palier en moins de 3 min et le refaire entièrement",
            "Attendre 15 min puis redescendre",
        ],
        "correct": 2,
        "explication": "On doit être redescendu au palier en moins de 3 min et le refaire en entier "
                       "(ainsi que les suivants).",
    },
    # --- Tables MN90 partie 2 (ch.12) : méthode
    {
        "chapitre": 12,
        "q": "Plongée successive : avec quel tableau calcule-t-on l'azote résiduel ?",
        "options": ["Le tableau 1", "Le tableau 2", "Le tableau IV", "La courbe de sécurité"],
        "correct": 0,
        "explication": "Le tableau 1 donne l'azote résiduel (selon le GPS et l'intervalle de surface).",
    },
    {
        "chapitre": 12,
        "q": "Plongée successive : avec quel tableau calcule-t-on la majoration ?",
        "options": ["Le tableau 1", "Le tableau 2", "Le tableau III", "La courbe de sécurité"],
        "correct": 1,
        "explication": "Le tableau 2 donne la majoration (selon l'azote résiduel et la profondeur prévue).",
    },
    {
        "chapitre": 12,
        "q": "Une 1ère plongée se termine à 9h00, la 2ème commence à 11h15. Ces plongées sont :",
        "options": ["Consécutives", "Successives", "Isolées", "Interdites"],
        "correct": 1,
        "explication": "Intervalle de 2h15 → 15 min ≤ IS < 12 h → plongées successives.",
    },
    {
        "chapitre": 12,
        "q": "L'intervalle de surface (2h15) n'existe pas dans le tableau 1. Quelle valeur prend-on ?",
        "options": [
            "La valeur immédiatement supérieure",
            "La valeur immédiatement inférieure (sécurité)",
            "La moyenne des deux",
            "Zéro",
        ],
        "correct": 1,
        "explication": "Pour l'intervalle dans le tableau 1, on prend la valeur inférieure → plus d'azote "
                       "résiduel → principe de sécurité.",
    },
]


# ===========================================================================
# Questions FACTUELLES supplémentaires (connaissances du cours), par chapitre
# ===========================================================================
FACTUELLES = [
    # --- 1. Pression
    {"chapitre": 1, "q": "1 bar correspond environ à la pression d'une colonne d'eau de mer de :",
     "options": ["1 m", "5 m", "10 m", "20 m"], "correct": 2,
     "explication": "On compte +1 bar tous les 10 m d'eau."},
    {"chapitre": 1, "q": "À la surface, la pression absolue vaut :",
     "options": ["0 bar", "1 bar", "2 bar", "10 bar"], "correct": 1,
     "explication": "Pabs = Patm = 1 bar en surface (Phyd = 0)."},
    {"chapitre": 1, "q": "Quand on descend, la pression absolue :",
     "options": ["diminue", "augmente", "reste constante", "s'annule"], "correct": 1,
     "explication": "Elle augmente de 1 bar tous les 10 m."},
    {"chapitre": 1, "q": "La pression atmosphérique sous l'eau :",
     "options": ["disparaît", "s'ajoute à la pression de l'eau (pression absolue)",
                 "double à 10 m", "ne compte pas"], "correct": 1,
     "explication": "Pabs = Patm + Phyd : la pression atmosphérique s'ajoute toujours."},
    {"chapitre": 1, "q": "La pression est définie comme :",
     "options": ["une force sur une surface", "un volume sur un temps",
                 "une masse sur une longueur", "une vitesse"], "correct": 0,
     "explication": "Une pression = résultat d'une force appliquée sur une surface."},
    {"chapitre": 1, "q": "À 45 m, la pression absolue vaut :",
     "options": ["4,5 bar", "5,5 bar", "5 bar", "4 bar"], "correct": 1,
     "explication": "Pabs = 1 + 45/10 = 5,5 bar."},
    # --- 2. Archimède
    {"chapitre": 2, "q": "La poussée d'Archimède est dirigée :",
     "options": ["de haut en bas", "de bas en haut (verticalement)",
                 "horizontalement", "vers le fond"], "correct": 1,
     "explication": "C'est une poussée verticale dirigée de bas en haut."},
    {"chapitre": 2, "q": "1 litre d'eau de mer déplacé crée une poussée d'environ :",
     "options": ["0,1 kg", "1 kg", "10 kg", "0,5 kg"], "correct": 1,
     "explication": "1 L d'eau ≈ 1 kg → 1 kg de poussée."},
    {"chapitre": 2, "q": "Un objet dont le poids apparent est négatif :",
     "options": ["coule", "remonte", "reste immobile", "se dissout"], "correct": 1,
     "explication": "Poids apparent < 0 → flottabilité positive → l'objet remonte."},
    {"chapitre": 2, "q": "Ajouter du plomb au lestage rend la flottabilité :",
     "options": ["plus positive", "plus négative", "nulle", "inchangée"], "correct": 1,
     "explication": "Plus de poids → poids apparent plus grand → flottabilité plus négative."},
    {"chapitre": 2, "q": "Un plongeur en équilibre (flottabilité nulle) a un poids apparent :",
     "options": ["positif", "négatif", "nul", "infini"], "correct": 2,
     "explication": "Flottabilité nulle ↔ poids apparent = 0."},
    {"chapitre": 2, "q": "La poussée d'Archimède dépend-elle de la profondeur ?",
     "options": ["oui, elle augmente", "oui, elle diminue", "non, elle est constante",
                 "seulement après 30 m"], "correct": 2,
     "explication": "Elle est constante : elle ne dépend que du volume déplacé."},
    # --- 3. Boyle-Mariotte
    {"chapitre": 3, "q": "À température constante, si la pression double, le volume :",
     "options": ["double", "est divisé par 2", "ne change pas", "est multiplié par 4"], "correct": 1,
     "explication": "Volume et pression sont inversement proportionnels."},
    {"chapitre": 3, "q": "La loi de Boyle-Mariotte suppose une température :",
     "options": ["croissante", "constante", "décroissante", "nulle"], "correct": 1,
     "explication": "P×V = constante à température constante."},
    {"chapitre": 3, "q": "En remontant, le volume d'air d'un espace souple :",
     "options": ["augmente", "diminue", "ne change pas", "se liquéfie"], "correct": 0,
     "explication": "La pression diminue → le volume augmente."},
    {"chapitre": 3, "q": "Entre 10 m et la surface, le volume d'un gaz est :",
     "options": ["multiplié par 2", "divisé par 2", "inchangé", "multiplié par 4"], "correct": 0,
     "explication": "La pression passe de 2 à 1 bar → le volume double."},
    {"chapitre": 3, "q": "P1×V1 = P2×V2 traduit que P et V sont :",
     "options": ["proportionnels", "inversement proportionnels", "indépendants", "égaux"], "correct": 1,
     "explication": "Le produit P×V reste constant."},
    {"chapitre": 3, "q": "Les barotraumatismes découlent surtout de la loi de :",
     "options": ["Henry", "Dalton", "Boyle-Mariotte", "Archimède"], "correct": 2,
     "explication": "Ce sont des variations de volume d'air → Boyle-Mariotte."},
    # --- 4. Autonomie
    {"chapitre": 4, "q": "La quantité d'air d'un bloc (en litres) se calcule par :",
     "options": ["volume + pression", "volume × pression", "pression / volume", "volume − réserve"],
     "correct": 1, "explication": "Quantité d'air = volume du bloc × pression."},
    {"chapitre": 4, "q": "Un bloc de 15 L à 230 bar contient :",
     "options": ["3450 L", "3000 L", "245 L", "1725 L"], "correct": 0,
     "explication": "15 × 230 = 3450 L d'air détendu."},
    {"chapitre": 4, "q": "La consommation à 30 m par rapport à la surface est :",
     "options": ["identique", "doublée", "multipliée par 3", "multipliée par 4"], "correct": 3,
     "explication": "À 30 m, Pabs = 4 bar → consommation × 4."},
    {"chapitre": 4, "q": "La pression de réserve usuelle est de :",
     "options": ["10 bar", "30 bar", "50 bar", "100 bar"], "correct": 2,
     "explication": "On garde en général 50 bar de réserve."},
    {"chapitre": 4, "q": "À durée et conso égales, plus on plonge profond, l'autonomie :",
     "options": ["augmente", "diminue", "ne change pas", "double"], "correct": 1,
     "explication": "La consommation augmente avec la pression → autonomie réduite."},
    # --- 5. Barotraumatismes
    {"chapitre": 5, "q": "L'équilibrage des oreilles se fait surtout :",
     "options": ["à la descente", "à la remontée", "en surface", "au palier"], "correct": 0,
     "explication": "On équilibre dès la tête sous l'eau, à la descente (jamais Valsalva à la remontée)."},
    {"chapitre": 5, "q": "Un rhume ou une sinusite :",
     "options": ["n'a aucun effet", "contre-indique la plongée", "facilite l'équilibrage",
                 "n'agit que sur les dents"], "correct": 1,
     "explication": "Enrhumé/sinusite : on ne plonge pas (risque de barotraumatisme)."},
    {"chapitre": 5, "q": "Le barotraumatisme des dents survient plutôt :",
     "options": ["à la descente", "à la remontée", "en surface", "au palier"], "correct": 1,
     "explication": "L'air piégé sous une dent se dilate à la remontée."},
    {"chapitre": 5, "q": "Le plaquage de masque se prévient en :",
     "options": ["soufflant par le nez à la descente", "bloquant sa respiration",
                 "faisant un Valsalva", "serrant la sangle"], "correct": 0,
     "explication": "On souffle de l'air par le nez dans le masque à la descente."},
    {"chapitre": 5, "q": "La surpression pulmonaire est surtout à risque :",
     "options": ["en profondeur", "près de la surface (10 m → 0 m)", "au fond", "au palier de 6 m"],
     "correct": 1, "explication": "Entre 10 m et 0 m le volume double : c'est là que le risque est maximal."},
    {"chapitre": 5, "q": "Les barotraumatismes dépendent-ils de la durée de plongée ?",
     "options": ["oui", "non, ils en sont indépendants", "seulement après 1 h", "uniquement au-delà de 30 m"],
     "correct": 1, "explication": "Ils sont indépendants de la durée et de la profondeur."},
    # --- 6. Henry
    {"chapitre": 6, "q": "À saturation, la pression du gaz et la tension dans le liquide sont :",
     "options": ["P > T", "P < T", "P = T", "P = 0"], "correct": 2,
     "explication": "Saturation = équilibre : P = T."},
    {"chapitre": 6, "q": "À la descente, l'azote :",
     "options": ["s'élimine", "se dissout dans les tissus", "ne bouge pas", "devient liquide"], "correct": 1,
     "explication": "La pression augmente → l'azote se dissout (sous-saturation, P > T)."},
    {"chapitre": 6, "q": "Plus la pression augmente, la quantité de gaz dissous :",
     "options": ["diminue", "augmente", "reste constante", "s'annule"], "correct": 1,
     "explication": "Loi de Henry : quantité dissoute ∝ pression."},
    {"chapitre": 6, "q": "La sursaturation critique provoque :",
     "options": ["une dissolution lente", "un dégazage anarchique (grosses bulles)",
                 "une saturation", "rien"], "correct": 1,
     "explication": "Quand T ≫ P, l'azote dégaze en grosses bulles → accident."},
    {"chapitre": 6, "q": "Le liquide considéré par la loi de Henry en plongée est :",
     "options": ["l'eau de mer", "le sang seul", "l'ensemble du corps (≈70 % d'eau)", "l'air des poumons"],
     "correct": 2, "explication": "Le corps humain, composé majoritairement d'eau."},
    # --- 7. ADD
    {"chapitre": 7, "q": "Pour décrire l'ADD, le corps est modélisé en :",
     "options": ["organes", "compartiments", "couches", "membranes"], "correct": 1,
     "explication": "Des compartiments qui saturent/désaturent à des vitesses différentes."},
    {"chapitre": 7, "q": "Les « puces » correspondent à une atteinte :",
     "options": ["osseuse", "cutanée", "neurologique", "de l'oreille interne"], "correct": 1,
     "explication": "Fourmillements et plaques rouges sur la peau."},
    {"chapitre": 7, "q": "Devant un ADD suspecté, on administre de l'oxygène :",
     "options": ["à 21 %", "à 50 %", "à 100 %", "pas du tout"], "correct": 2,
     "explication": "Oxygénothérapie normobare à 100 %."},
    {"chapitre": 7, "q": "Un palier obligatoire de 3 m peut être réalisé à :",
     "options": ["2,5 m", "4 m mais jamais 2,5 m", "1 m", "n'importe quelle profondeur"], "correct": 1,
     "explication": "On peut le faire à 4 m, en aucun cas à 2,5 m."},
    {"chapitre": 7, "q": "Quel facteur NE favorise PAS un ADD ?",
     "options": ["le froid", "l'effort", "le repos et le calme", "la fatigue"], "correct": 2,
     "explication": "Froid, effort, fatigue, anxiété favorisent l'ADD ; le calme le limite."},
    {"chapitre": 7, "q": "Les accidents neurologiques de l'ADD peuvent donner :",
     "options": ["des fourmillements/paralysie des jambes", "une simple soif",
                 "une faim intense", "une meilleure vision"], "correct": 0,
     "explication": "Troubles moteurs, fourmillements, voire paraplégie."},
    # --- 8. Dalton
    {"chapitre": 8, "q": "La pression d'un mélange gazeux est égale à :",
     "options": ["la pression du gaz majoritaire", "la somme des pressions partielles",
                 "la moyenne des pressions", "la pression de l'oxygène"], "correct": 1,
     "explication": "Loi de Dalton : Ptotale = somme des pressions partielles."},
    {"chapitre": 8, "q": "La pression partielle d'un gaz dépend :",
     "options": ["de la température seule", "de la pression totale et du pourcentage du gaz",
                 "du volume du bloc", "de la profondeur seule"], "correct": 1,
     "explication": "Ppa = Pression totale × pourcentage du gaz."},
    {"chapitre": 8, "q": "À 40 m, la pression partielle d'azote (air) vaut :",
     "options": ["3,2 bar", "4 bar", "1 bar", "0,8 bar"], "correct": 1,
     "explication": "Pabs = 5 bar à 40 m ; PpN2 = 5 × 0,8 = 4 bar."},
    {"chapitre": 8, "q": "Dans l'air, l'oxygène représente environ :",
     "options": ["80 %", "50 %", "20 %", "100 %"], "correct": 2,
     "explication": "Air ≈ 20 % O2 et 80 % N2."},
    {"chapitre": 8, "q": "La narcose est liée à la pression partielle de :",
     "options": ["l'oxygène", "l'azote", "l'hélium", "la vapeur d'eau"], "correct": 1,
     "explication": "Élévation de la PpN2 (et probablement du CO2)."},
    # --- 9. Toxicité des gaz
    {"chapitre": 9, "q": "L'essoufflement est dû à une accumulation de :",
     "options": ["azote", "oxygène", "gaz carbonique (CO2)", "hélium"], "correct": 2,
     "explication": "Intoxication au CO2."},
    {"chapitre": 9, "q": "Devant un essoufflement, on favorise :",
     "options": ["l'inspiration", "l'expiration", "l'apnée", "l'accélération du rythme"], "correct": 1,
     "explication": "Arrêt de l'effort et expiration favorisée."},
    {"chapitre": 9, "q": "La narcose apparaît souvent à partir de :",
     "options": ["10 m", "20 m", "40 m", "60 m"], "correct": 2,
     "explication": "Possible dès 30 m, fréquente à partir de 40 m."},
    {"chapitre": 9, "q": "Le « rendez-vous syncopal des 7 m » concerne :",
     "options": ["la plongée bouteille profonde", "l'apnée après hyperventilation",
                 "le palier de 3 m", "la narcose"], "correct": 1,
     "explication": "Syncope hypoxique en fin d'apnée, favorisée par l'hyperventilation."},
    {"chapitre": 9, "q": "À 40 m, en cas d'essoufflement, il faut :",
     "options": ["récupérer sur place", "descendre", "remonter", "accélérer la respiration"], "correct": 2,
     "explication": "À 40 m on ne récupère pas d'un essoufflement : on remonte."},
    {"chapitre": 9, "q": "La toxicité de l'oxygène concerne surtout :",
     "options": ["tous les plongeurs dès 10 m", "les N3 et plongeurs Nitrox",
                 "uniquement les apnéistes", "personne"], "correct": 1,
     "explication": "Dangereuse vers 1,6 bar de PpO2 (≈ 66 m à l'air) : surtout N3 et Nitrox."},
    # --- 10. Noyade
    {"chapitre": 10, "q": "En remontant une victime, on maintient :",
     "options": ["le masque enlevé", "le détendeur en bouche", "la tête sous l'eau", "les bras levés"],
     "correct": 1, "explication": "On maintient le détendeur en bouche pendant l'extraction."},
    {"chapitre": 10, "q": "Une noyade secondaire fait suite à :",
     "options": ["un épuisement", "une syncope ou perte de connaissance",
                 "un bon palier", "une plongée courte"], "correct": 1,
     "explication": "Elle succède à une syncope/perte de connaissance en milieu irrespirable."},
    {"chapitre": 10, "q": "Après extraction d'une victime, on :",
     "options": ["la laisse seule", "alerte les secours, réchauffe et rassure",
                 "la fait replonger", "attend 1 h"], "correct": 1,
     "explication": "Signe de détresse, appel des secours, réchauffer et rassurer."},
    {"chapitre": 10, "q": "L'hyperventilation avant une apnée :",
     "options": ["est recommandée", "favorise la syncope", "n'a aucun effet", "réchauffe le corps"],
     "correct": 1, "explication": "Elle retarde l'envie de respirer et favorise la syncope."},
    # --- 11. Tables MN90 (1)
    {"chapitre": 11, "q": "La vitesse de remontée entre deux paliers est de :",
     "options": ["6 m/min", "15 m/min", "10 m/min", "17 m/min"], "correct": 0,
     "explication": "Entre paliers : 6 m/min (≈ 30 s par tranche de 3 m)."},
    {"chapitre": 11, "q": "Les paliers de décompression se font tous les :",
     "options": ["2 m", "3 m", "5 m", "6 m"], "correct": 1,
     "explication": "De 3 en 3 mètres."},
    {"chapitre": 11, "q": "Si la profondeur n'existe pas dans la table, on prend :",
     "options": ["la valeur inférieure", "la valeur immédiatement supérieure",
                 "la moyenne", "on interpole"], "correct": 1,
     "explication": "Valeur immédiatement supérieure ; l'interpolation est interdite."},
    {"chapitre": 11, "q": "Le palier de sécurité recommandé est de :",
     "options": ["3 min à 3 m", "5 min à 5 m", "1 min à 6 m", "10 min à 3 m"], "correct": 0,
     "explication": "Palier de principe : 3 min à 3 m."},
    {"chapitre": 11, "q": "Les tables MN90 sont prévues pour des plongées :",
     "options": ["au Nitrox", "à l'air", "à l'oxygène pur", "au Trimix"], "correct": 1,
     "explication": "Plongées à l'air, au niveau de la mer, 2 plongées max/24 h."},
    {"chapitre": 11, "q": "La courbe de sécurité n'est valable que pour :",
     "options": ["la 1ère plongée du jour", "la 2e plongée", "les plongées de nuit",
                 "les plongées profondes"], "correct": 0,
     "explication": "Elle ne s'applique qu'à la première plongée de la journée."},
    {"chapitre": 11, "q": "MN90 a été élaborée par :",
     "options": ["la PADI", "la Marine Nationale", "la CMAS", "la Royal Navy"], "correct": 1,
     "explication": "Marine Nationale, utilisée à partir de 1990."},
    # --- 12. Tables MN90 (2)
    {"chapitre": 12, "q": "Deux plongées séparées de moins de 15 min sont :",
     "options": ["successives", "consécutives", "isolées", "interdites"], "correct": 1,
     "explication": "IS < 15 min → consécutives (une seule plongée)."},
    {"chapitre": 12, "q": "L'azote résiduel se lit dans :",
     "options": ["le tableau 1", "le tableau 2", "le tableau IV", "la courbe de sécurité"], "correct": 0,
     "explication": "Tableau 1 : azote résiduel selon GPS et intervalle de surface."},
    {"chapitre": 12, "q": "La majoration se lit dans :",
     "options": ["le tableau 1", "le tableau 2", "le tableau III", "la courbe"], "correct": 1,
     "explication": "Tableau 2 : majoration selon azote résiduel et profondeur prévue."},
    {"chapitre": 12, "q": "La majoration s'ajoute :",
     "options": ["à l'heure de sortie", "à la durée de la 2e plongée (pour les paliers)",
                 "à la profondeur", "à l'intervalle de surface"], "correct": 1,
     "explication": "C'est un allongement fictif de la durée de la 2e plongée."},
    {"chapitre": 12, "q": "Au-delà de 12 h entre deux plongées, on considère :",
     "options": ["une plongée successive", "une plongée consécutive",
                 "une plongée simple (isolée)", "deux plongées interdites"], "correct": 2,
     "explication": "12 h = désaturation quasi complète → plongée simple."},
    {"chapitre": 12, "q": "La lettre GPS indique :",
     "options": ["la profondeur du palier", "l'azote résiduel dans l'organisme",
                 "la vitesse de remontée", "l'heure de sortie"], "correct": 1,
     "explication": "Le GPS code la quantité d'azote dissous restant."},
    # --- 13. Réglementation
    {"chapitre": 13, "q": "Un N2 encadré par un guide de palanquée peut aller jusqu'à :",
     "options": ["20 m", "40 m", "60 m", "12 m"], "correct": 1,
     "explication": "Encadré jusqu'à 40 m ; en autonomie entre N2 jusqu'à 20 m."},
    {"chapitre": 13, "q": "Âge minimum pour le Niveau 2 :",
     "options": ["12 ans", "14 ans", "16 ans", "18 ans"], "correct": 2,
     "explication": "Au moins 16 ans (autorisation parentale si mineur)."},
    {"chapitre": 13, "q": "Le certificat médical de non-contre-indication est valable :",
     "options": ["6 mois", "1 an", "2 ans", "5 ans"], "correct": 1,
     "explication": "Validité d'un an."},
    {"chapitre": 13, "q": "La RC (responsabilité civile) au tiers est :",
     "options": ["facultative", "obligatoire et fournie avec la licence",
                 "réservée aux compétiteurs", "inutile"], "correct": 1,
     "explication": "Obligatoire, fournie avec la licence FFESSM."},
    {"chapitre": 13, "q": "En autonomie, chaque plongeur doit pouvoir donner de l'air via :",
     "options": ["un seul détendeur", "un octopus ou 2 détendeurs",
                 "le gilet", "le parachute"], "correct": 1,
     "explication": "Octopus ou 2 détendeurs : donner de l'air sans échange d'embout."},
    {"chapitre": 13, "q": "La licence FFESSM (loisir) est valable :",
     "options": ["12 mois", "15 mois", "24 mois", "1 saison"], "correct": 1,
     "explication": "15 mois (d'octobre à décembre de l'année suivante)."},
    # --- 14. Comportement et sécurité
    {"chapitre": 14, "q": "On ne plonge pas si :",
     "options": ["il fait beau", "on est enrhumé", "l'eau est à 20 °C", "la palanquée est complète"],
     "correct": 1, "explication": "Rhume/sinusite, méforme ou absence d'envie : on ne plonge pas."},
    {"chapitre": 14, "q": "Bouteille bien ouverte : en respirant, l'aiguille du manomètre :",
     "options": ["chute", "ne bouge pas", "monte", "clignote"], "correct": 1,
     "explication": "Si elle bouge à l'inspiration, la bouteille n'est pas (assez) ouverte."},
    {"chapitre": 14, "q": "En cas de perte de palanquée :",
     "options": ["continuer seul", "chercher ~1 min puis remonter doucement",
                 "remonter vite", "redescendre"], "correct": 1,
     "explication": "1 à 2 tours d'horizon (~1 min) puis remontée lente et attente en surface."},
    {"chapitre": 14, "q": "Après la plongée, on évite l'avion pendant :",
     "options": ["1 h", "6 h", "au moins 12 h", "30 min"], "correct": 2,
     "explication": "Pas d'avion ni d'altitude dans les 12 à 24 h."},
    {"chapitre": 14, "q": "Le seul juge de son aptitude à plonger ce jour-là est :",
     "options": ["le moniteur", "le binôme", "soi-même", "le club"], "correct": 2,
     "explication": "Vous êtes seul apte à juger de votre état ; ne pas se laisser influencer."},
    # --- 15. Matériel
    {"chapitre": 15, "q": "Le 1er étage du détendeur détend la haute pression vers :",
     "options": ["la pression ambiante", "la moyenne pression (≈10 bar + Pabs)",
                 "la basse pression", "la réserve"], "correct": 1,
     "explication": "1er étage : HP → moyenne pression."},
    {"chapitre": 15, "q": "Le 2e étage du détendeur délivre l'air :",
     "options": ["en continu", "à la demande, à la pression ambiante",
                 "sous haute pression", "uniquement en surface"], "correct": 1,
     "explication": "À la demande et à la pression ambiante."},
    {"chapitre": 15, "q": "Un gilet stabilisateur comporte au minimum :",
     "options": ["1 purge", "2 purges", "3 purges", "5 purges"], "correct": 2,
     "explication": "3 purges (2 rapides + 1 lente) et 2 mécanismes de gonflage."},
    {"chapitre": 15, "q": "La bouée (gilet) sert à :",
     "options": ["compenser un sur-lestage", "s'équilibrer et se maintenir en surface",
                 "remplacer le lestage", "respirer"], "correct": 1,
     "explication": "Elle ne doit pas compenser un sur-lestage."},
    {"chapitre": 15, "q": "Après la plongée, le détendeur doit être :",
     "options": ["laissé tel quel", "rincé à l'eau douce et séché",
                 "graissé à chaque fois", "démonté"], "correct": 1,
     "explication": "Rinçage à l'eau douce, séchage, rangement à l'abri."},
    {"chapitre": 15, "q": "Le parachute de palier sert à :",
     "options": ["descendre plus vite", "se faire repérer en surface",
                 "respirer au palier", "mesurer la profondeur"], "correct": 1,
     "explication": "Repérage en surface et cohésion de la palanquée au palier."},
    {"chapitre": 15, "q": "Les contenances standards des bouteilles sont :",
     "options": ["5-10-15-20 L", "6-9-12-15-18 L", "8-16-24 L", "10-12-14 L"], "correct": 1,
     "explication": "6, 9, 12, 15 et 18 litres (200 ou 230 bar)."},
]


# ===========================================================================
# Questions à CHOIX MULTIPLES (plusieurs bonnes réponses) — clé "corrects"
# ===========================================================================
MULTI = [
    # --- 1. Pression
    {"chapitre": 1, "q": "Parmi ces affirmations sur la pression, lesquelles sont exactes ?",
     "options": ["Pabs = Patm + Phyd", "La pression hydrostatique augmente de 1 bar tous les 10 m",
                 "La pression atmosphérique vaut 0 bar en surface", "À 20 m, la Pabs vaut 3 bar"],
     "corrects": [0, 1, 3],
     "explication": "La Patm vaut 1 bar (pas 0) en surface ; les autres affirmations sont exactes."},
    {"chapitre": 1, "q": "Quelles grandeurs composent la pression absolue ?",
     "options": ["la pression atmosphérique", "la pression hydrostatique",
                 "la pression partielle d'oxygène", "la poussée d'Archimède"],
     "corrects": [0, 1],
     "explication": "Pabs = pression atmosphérique + pression hydrostatique."},
    # --- 2. Archimède
    {"chapitre": 2, "q": "Quelles affirmations sur Archimède sont correctes ?",
     "options": ["Poids apparent = poids réel − poussée", "La poussée est constante avec la profondeur",
                 "Flottabilité positive → l'objet coule", "1 L d'eau déplacé ≈ 1 kg de poussée"],
     "corrects": [0, 1, 3],
     "explication": "Flottabilité positive → l'objet REMONTE (poids apparent < 0)."},
    {"chapitre": 2, "q": "Un objet a une flottabilité négative. Lesquelles sont vraies ?",
     "options": ["il coule", "son poids apparent est positif", "il remonte", "son poids apparent est nul"],
     "corrects": [0, 1],
     "explication": "Flottabilité négative ↔ poids apparent > 0 ↔ l'objet coule."},
    # --- 3. Boyle-Mariotte
    {"chapitre": 3, "q": "Concernant la loi de Boyle-Mariotte, lesquelles sont vraies ?",
     "options": ["P × V est constant (à T constante)", "le volume augmente à la remontée",
                 "les variations de volume sont maximales près de la surface",
                 "le volume augmente quand la pression augmente"],
     "corrects": [0, 1, 2],
     "explication": "Quand la pression augmente, le volume DIMINUE (inversement proportionnels)."},
    # --- 4. Autonomie
    {"chapitre": 4, "q": "Pour un calcul d'autonomie, de quoi a-t-on besoin ?",
     "options": ["le volume du bloc", "la pression du bloc", "la profondeur et la consommation",
                 "la température de l'eau"],
     "corrects": [0, 1, 2],
     "explication": "Volume, pression, profondeur et consommation suffisent."},
    {"chapitre": 4, "q": "Quelles étapes interviennent dans le calcul d'autonomie ?",
     "options": ["calculer l'air consommable", "tenir compte de la réserve",
                 "multiplier la consommation par la pression absolue", "ignorer la profondeur"],
     "corrects": [0, 1, 2],
     "explication": "On garde la réserve et on tient compte de la profondeur (× Pabs)."},
    # --- 5. Barotraumatismes
    {"chapitre": 5, "q": "Quels barotraumatismes peuvent survenir à la remontée ?",
     "options": ["les dents", "l'estomac et les intestins", "le plaquage du masque",
                 "la surpression pulmonaire"],
     "corrects": [0, 1, 3],
     "explication": "Le plaquage du masque ne survient qu'à la descente."},
    {"chapitre": 5, "q": "Quels accidents peuvent survenir à la descente ?",
     "options": ["le plaquage du masque", "les oreilles", "les sinus", "la surpression pulmonaire"],
     "corrects": [0, 1, 2],
     "explication": "La surpression pulmonaire est un accident de remontée."},
    {"chapitre": 5, "q": "Comment prévenir la surpression pulmonaire ?",
     "options": ["expirer à la remontée", "ne jamais bloquer sa respiration",
                 "faire un Valsalva à la remontée", "être prudent lors des remontées à 2 sur un embout"],
     "corrects": [0, 1, 3],
     "explication": "Pas de Valsalva à la remontée : il faut expirer et ne pas bloquer son air."},
    # --- 6. Henry
    {"chapitre": 6, "q": "Quels facteurs influencent la dissolution des gaz dans le corps ?",
     "options": ["la pression", "le temps", "l'agitation du plongeur", "la couleur de la combinaison"],
     "corrects": [0, 1, 2],
     "explication": "Pression, temps, agitation, température… influencent la dissolution."},
    {"chapitre": 6, "q": "À propos des états de dissolution, lesquels sont corrects ?",
     "options": ["descente = sous-saturation (P > T)", "remontée = sur-saturation (P < T)",
                 "saturation : P = T", "remontée : P > T"],
     "corrects": [0, 1, 2],
     "explication": "À la remontée, P < T (sur-saturation)."},
    # --- 7. ADD
    {"chapitre": 7, "q": "Lesquels sont des types/symptômes d'accident de décompression ?",
     "options": ["les puces", "les moutons", "les accidents neurologiques", "le plaquage du masque"],
     "corrects": [0, 1, 2],
     "explication": "Le plaquage du masque est un barotraumatisme, pas un ADD."},
    {"chapitre": 7, "q": "Que comprend le traitement d'un ADD ?",
     "options": ["oxygène à 100 %", "aspirine 0,5 g", "faire boire", "faire redescendre la victime"],
     "corrects": [0, 1, 2],
     "explication": "On ne fait pas redescendre la victime : O2, aspirine, boire, caisson."},
    {"chapitre": 7, "q": "Quels facteurs favorisent un ADD ?",
     "options": ["le froid", "l'effort", "la fatigue", "le repos et le calme"],
     "corrects": [0, 1, 2],
     "explication": "Froid, effort, fatigue, anxiété, hypoglycémie favorisent l'ADD."},
    {"chapitre": 7, "q": "Quelles mesures préviennent l'ADD ?",
     "options": ["respecter la vitesse de remontée", "respecter les paliers",
                 "pas d'avion pendant 12 à 24 h", "faire une apnée juste après la plongée"],
     "corrects": [0, 1, 2],
     "explication": "Pas d'apnée ni d'effort après la plongée."},
    # --- 8. Dalton
    {"chapitre": 8, "q": "Concernant la loi de Dalton, lesquelles sont vraies ?",
     "options": ["Ptotale = somme des pressions partielles", "Ppa = Ptotale × pourcentage du gaz",
                 "l'air ≈ 20 % O2 et 80 % N2", "la pression partielle diminue avec la profondeur"],
     "corrects": [0, 1, 2],
     "explication": "La pression partielle AUGMENTE avec la profondeur."},
    # --- 9. Toxicité des gaz
    {"chapitre": 9, "q": "Quels sont des symptômes d'essoufflement ?",
     "options": ["accélération du rythme ventilatoire", "maux de tête", "palpitations",
                 "sensation de pleine forme"],
     "corrects": [0, 1, 2],
     "explication": "Essoufflement : accélération ventilatoire, maux de tête, palpitations, panique…"},
    {"chapitre": 9, "q": "Quelles peuvent être des causes d'essoufflement ?",
     "options": ["l'effort", "le froid", "un matériel mal adapté", "une excellente technique de palmage"],
     "corrects": [0, 1, 2],
     "explication": "Effort, froid, émotion, matériel défectueux, profondeur… favorisent l'essoufflement."},
    {"chapitre": 9, "q": "À propos de la narcose, lesquelles sont vraies ?",
     "options": ["elle est due à l'azote", "elle apparaît souvent dès 40 m",
                 "elle se traite en remontant", "elle laisse des séquelles définitives"],
     "corrects": [0, 1, 2],
     "explication": "Les symptômes disparaissent en remontant, sans séquelle."},
    # --- 10. Noyade
    {"chapitre": 10, "q": "Quelle est la conduite à tenir face à une noyade ?",
     "options": ["extraire du milieu", "maintenir le détendeur en bouche", "appeler les secours",
                 "laisser la victime dans l'eau"],
     "corrects": [0, 1, 2],
     "explication": "On extrait la victime (détendeur en bouche) et on alerte les secours."},
    # --- 11. Tables MN90 (1)
    {"chapitre": 11, "q": "Quelles sont des conditions d'utilisation des tables MN90 ?",
     "options": ["plongées à l'air", "2 plongées maximum par 24 h", "profondeur maxi 60 m",
                 "plongées au Nitrox"],
     "corrects": [0, 1, 2],
     "explication": "Les MN90 sont prévues pour des plongées à l'air."},
    {"chapitre": 11, "q": "Concernant les vitesses et paliers MN90 :",
     "options": ["15 m/min à la remontée", "6 m/min entre les paliers", "paliers de 3 en 3 m",
                 "interpolation autorisée"],
     "corrects": [0, 1, 2],
     "explication": "L'interpolation est interdite : on prend la valeur supérieure."},
    {"chapitre": 11, "q": "Quels cas particuliers la table MN90 permet-elle de gérer ?",
     "options": ["la remontée lente", "la remontée rapide", "le palier interrompu",
                 "le palier anticipé à 1 m"],
     "corrects": [0, 1, 2],
     "explication": "Remontée lente, remontée rapide et palier interrompu ont des procédures."},
    # --- 12. Tables MN90 (2)
    {"chapitre": 12, "q": "Pour une plongée successive (15 min ≤ IS < 12 h), il faut :",
     "options": ["calculer l'azote résiduel (tableau 1)", "calculer la majoration (tableau 2)",
                 "ajouter la majoration à la durée de plongée",
                 "compter la majoration dans l'heure de sortie"],
     "corrects": [0, 1, 2],
     "explication": "Piège : la majoration ne compte pas dans l'heure de sortie."},
    {"chapitre": 12, "q": "Concernant les plongées consécutives (IS < 15 min) :",
     "options": ["on prend la profondeur max des deux plongées", "DP = somme des deux durées",
                 "on traite comme une seule plongée", "on calcule une majoration"],
     "corrects": [0, 1, 2],
     "explication": "Pas de majoration : on additionne les durées et on prend la profondeur max."},
    # --- 13. Réglementation
    {"chapitre": 13, "q": "Quelles sont des conditions pour passer le Niveau 2 ?",
     "options": ["être titulaire du N1 (ou équivalent)", "avoir une licence FFESSM valide",
                 "avoir 18 ans obligatoirement", "avoir un certificat médical de moins d'un an"],
     "corrects": [0, 1, 3],
     "explication": "L'âge minimum est 16 ans (pas 18)."},
    {"chapitre": 13, "q": "Quel équipement est requis pour plonger en autonomie ?",
     "options": ["un gilet stabilisateur", "un moyen de contrôle (ordinateur ou tables)",
                 "un octopus ou 2 détendeurs", "un fusil de chasse sous-marine"],
     "corrects": [0, 1, 2],
     "explication": "Gilet, moyen de contrôle et de quoi donner de l'air sans échange d'embout."},
    {"chapitre": 13, "q": "Quels diplômes/qualifications sont accessibles après le N2 ?",
     "options": ["Niveau 3", "Plongeur Nitrox", "Initiateur", "Niveau 4 (encadrement)"],
     "corrects": [0, 1, 2],
     "explication": "Le Niveau 4 n'est plus accessible après le N2 depuis septembre 2011."},
    # --- 14. Comportement et sécurité
    {"chapitre": 14, "q": "Avant la plongée, que doit-on faire ?",
     "options": ["vérifier la pression du bloc", "vérifier le bon fonctionnement du matériel",
                 "repérer l'équipement de sa palanquée", "ignorer le briefing du directeur de plongée"],
     "corrects": [0, 1, 2],
     "explication": "On écoute toujours le briefing du directeur de plongée."},
    {"chapitre": 14, "q": "Dans quels cas ne faut-il PAS plonger ?",
     "options": ["en cas de rhume", "si l'on n'est pas en forme", "si l'on n'a pas envie",
                 "si l'eau est claire"],
     "corrects": [0, 1, 2],
     "explication": "Rhume, méforme ou absence d'envie : on ne plonge pas."},
    # --- 15. Matériel
    {"chapitre": 15, "q": "Un détendeur doit fournir de l'air :",
     "options": ["à la pression ambiante", "sans effort", "à la demande",
                 "en débit continu permanent"],
     "corrects": [0, 1, 2],
     "explication": "À la pression ambiante, sans effort et uniquement à la demande."},
    {"chapitre": 15, "q": "Un gilet stabilisateur comporte :",
     "options": ["au moins 2 mécanismes de gonflage", "au moins 3 purges", "un insufflateur",
                 "un détendeur haute pression"],
     "corrects": [0, 1, 2],
     "explication": "2 mécanismes de gonflage (insufflateur + direct-system) et 3 purges minimum."},
    {"chapitre": 15, "q": "Quels instruments servent à gérer ses paramètres de plongée ?",
     "options": ["le timer", "l'ordinateur", "le profondimètre", "l'arbalète"],
     "corrects": [0, 1, 2],
     "explication": "Timer, ordinateur, profondimètre/montre : pour temps, profondeur, vitesse, paliers."},
]


# ===========================================================================
# Générateurs de questions de CALCUL (réponses calculées → fiables)
# ===========================================================================

def _fmt(x, unit=""):
    """Formate un nombre à la française (virgule décimale, sans .0 inutile)."""
    x = round(float(x), 2)
    if abs(x - round(x)) < 1e-9:
        s = str(int(round(x)))
    else:
        s = ("%.2f" % x).rstrip("0").rstrip(".").replace(".", ",")
    return (s + " " + unit) if unit else s


def _numq(qid, chap_num, text, answer, distractors, unit, explication):
    """Construit une question numérique : 4 options distinctes, bon index calculé."""
    answer = round(float(answer), 2)
    vals = [answer]
    for d in distractors:
        d = round(float(d), 2)
        if all(abs(d - v) > 1e-6 for v in vals):
            vals.append(d)
        if len(vals) == 4:
            break
    pad = 1
    while len(vals) < 4:
        cand = round(answer + pad, 2)
        if cand > 0 and all(abs(cand - v) > 1e-6 for v in vals):
            vals.append(cand)
        pad += 1
    vals_sorted = sorted(vals)
    options = [_fmt(v, unit) for v in vals_sorted]
    correct = min(range(len(vals_sorted)), key=lambda i: abs(vals_sorted[i] - answer))
    return {"id": qid, "chapitre": chap_num, "q": text,
            "options": options, "correct": correct, "explication": explication}


# Contextes variés (scénarios) pour rendre les énoncés moins répétitifs.
_SCN = [
    "À {d} m de profondeur,",
    "Un plongeur explore une épave à {d} m :",
    "Au pied d'un tombant à {d} m,",
    "Pendant une plongée à {d} m,",
    "Pascal le Mérou nage à {d} m :",
    "Sur un fond de {d} m,",
    "Le long du récif à {d} m,",
    "Un binôme descend à {d} m :",
]


def _scn(i, d):
    return _SCN[i % len(_SCN)].format(d=d)


def _gen_pression():
    out = []
    depths = [5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 28, 30, 32,
              34, 35, 38, 40, 42, 44, 45, 48, 50, 52, 55, 58]
    for i, d in enumerate(depths):
        pabs, phyd = 1 + d / 10, d / 10
        if i % 3 == 0:
            out.append(_numq(f"gpa{i}", 1,
                f"{_scn(i, d)} quelle est la pression absolue subie par le plongeur ?",
                pabs, [phyd, pabs + 1, 1 + d / 100, pabs + 2], "bar",
                f"Pabs = 1 + {d}/10 = {_fmt(pabs)} bar."))
        elif i % 3 == 1:
            out.append(_numq(f"gph{i}", 1,
                f"{_scn(i, d)} quelle est la pression hydrostatique (celle de l'eau seule) ?",
                phyd, [pabs, phyd + 1, d / 100, phyd + 2], "bar",
                f"Phyd = {d}/10 = {_fmt(phyd)} bar (Pabs = {_fmt(pabs)} bar)."))
        else:
            out.append(_numq(f"gpx{i}", 1,
                f"{_scn(i, d)} la pression absolue représente combien de fois celle de la surface ?",
                pabs, [phyd, pabs + 1, pabs - 1 if pabs > 1.1 else pabs + 2, pabs + 0.5], "fois",
                f"Pabs / Psurface = {_fmt(pabs)} / 1 = {_fmt(pabs)} fois la pression de surface."))
    for j, p in enumerate([2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]):
        d = (p - 1) * 10
        out.append(_numq(f"gpd{j}", 1,
            f"À quelle profondeur la pression absolue vaut-elle {_fmt(p)} bar ?",
            d, [p * 10, d + 5, d - 5 if d > 5 else d + 10, d + 10], "m",
            f"Phyd = {_fmt(p)} − 1 = {_fmt(p - 1)} bar → profondeur = {_fmt(d)} m."))
    for j, (a, b) in enumerate([(10, 30), (0, 20), (15, 40), (20, 50), (5, 25), (12, 42), (8, 38)]):
        g = (b - a) / 10
        out.append(_numq(f"gpg{j}", 1,
            f"De combien de bar la pression augmente-t-elle entre {a} m et {b} m ?",
            g, [g + 1, g - 1 if g > 1 else g + 2, b - a, g + 0.5], "bar",
            f"Variation = ({b} − {a}) / 10 = {_fmt(g)} bar."))
    return out


def _gen_boyle():
    out = []
    objs_up = ["la bouée d'un plongeur", "un parachute de palier", "un sac de relevage"]
    i = 0
    for V in [1, 2, 3, 4, 5, 6]:
        for d in [10, 20, 30, 40, 50]:
            pabs = 1 + d / 10
            surf = V * pabs
            obj = objs_up[i % len(objs_up)]
            out.append(_numq(f"gba{i}", 3,
                f"À {d} m, {obj} contient {V} L d'air. Sans purger à la remontée, quel volume "
                f"cela représente-t-il en surface ?",
                surf, [V * (pabs - 1), V * (pabs + 1), V, V / pabs], "L",
                f"P1×V1 = P2×V2 → {_fmt(pabs)}×{V} = 1×V → V = {_fmt(surf)} L."))
            i += 1
    objs_dn = ["Un ballon souple", "Une bouée", "Un sac plastique fermé", "Une poche d'air"]
    for k, (V0, d) in enumerate([(6, 10), (12, 10), (6, 20), (12, 20), (9, 20), (12, 30),
                                 (6, 30), (8, 30), (12, 40), (8, 40), (15, 20), (18, 20),
                                 (10, 10), (20, 30), (24, 40)]):
        pabs = 1 + d / 10
        vv = V0 / pabs
        obj = objs_dn[k % len(objs_dn)]
        out.append(_numq(f"gbd{k}", 3,
            f"{obj} de {V0} L (en surface) est descendu à {d} m. Quel est alors son volume ?",
            vv, [V0, V0 * pabs, V0 / (pabs - 1) if pabs > 1.1 else V0 + 1, vv + 1], "L",
            f"1×{V0} = {_fmt(pabs)}×V → V = {_fmt(vv)} L."))
    for k, ratio in enumerate([2, 3, 4, 5, 6]):
        d = (ratio - 1) * 10
        out.append(_numq(f"gbr{k}", 3,
            f"À quelle profondeur le volume d'un gaz est-il divisé par {ratio} par rapport "
            f"à la surface ?",
            d, [d + 10, d - 10 if d > 10 else d + 20, ratio * 10, d + 5], "m",
            f"Volume ÷ {ratio} ⇔ pression × {ratio} ⇔ Pabs = {ratio} bar ⇔ {_fmt(d)} m."))
    return out


def _gen_autonomie():
    out = []
    combos = []
    for Vb in [10, 12, 15]:
        for P in [200, 230]:
            for d in [10, 20, 30, 40]:
                for C in [15, 18, 20, 22]:
                    combos.append((Vb, P, d, C))
    intros = [
        "Bloc de {Vb} L à {P} bar, plongée à {d} m, consommation {C} L/min en surface "
        "(réserve 50 bar).",
        "Avec un bloc de {Vb} L gonflé à {P} bar, à {d} m, en respirant {C} L/min en surface "
        "(réserve 50 bar).",
        "Un plongeur (qui consomme {C} L/min en surface) part à {d} m avec un bloc {Vb} L / "
        "{P} bar (réserve 50 bar).",
        "Pour une plongée à {d} m : bloc {Vb} L / {P} bar, consommation {C} L/min, réserve 50 bar.",
    ]
    for idx, (Vb, P, d, C) in enumerate(combos):
        pabs = 1 + d / 10
        t = (P - 50) * Vb / (C * pabs)
        intro = intros[idx % len(intros)].format(Vb=Vb, P=P, d=d, C=C)
        out.append(_numq(f"gau{idx}", 4,
            intro + " Au bout de combien de temps passe-t-on sur la réserve ?",
            t, [P * Vb / (C * pabs), (P - 50) * Vb / C, (P - 50) * Vb / (C * max(d / 10, 1)), t + 5],
            "min",
            f"Air consommable = ({P}−50)×{Vb} = {int((P - 50) * Vb)} L ; conso à {d} m = "
            f"{C}×{_fmt(pabs)} = {_fmt(C * pabs)} L/min ; {int((P - 50) * Vb)} ÷ "
            f"{_fmt(C * pabs)} = {_fmt(t)} min."))
    return out


def _gen_dalton():
    out = []
    for i, d in enumerate([0, 10, 20, 30, 40, 50, 15, 25, 35, 45]):
        pabs = 1 + d / 10
        po2, pn2 = pabs * 0.2, pabs * 0.8
        if i % 2 == 0:
            out.append(_numq(f"gdo{i}", 8,
                f"En plongée à l'air à {d} m, quelle est la pression partielle d'oxygène ?",
                po2, [pn2, pabs * 0.21, pabs * 0.16, po2 + 0.2], "bar",
                f"PpO2 = {_fmt(pabs)} × 0,20 = {_fmt(po2)} bar."))
        else:
            out.append(_numq(f"gdn{i}", 8,
                f"En plongée à l'air à {d} m, quelle est la pression partielle d'azote ?",
                pn2, [po2, pabs * 0.79, pn2 + 0.8, pabs * 0.7], "bar",
                f"PpN2 = {_fmt(pabs)} × 0,80 = {_fmt(pn2)} bar."))
    for k, d in enumerate([12, 18, 28, 38, 48]):
        pabs = 1 + d / 10
        po2 = pabs * 0.2
        out.append(_numq(f"gdo2{k}", 8,
            f"Un plongeur est à {d} m (air) : quelle est la pression partielle d'oxygène ?",
            po2, [pabs * 0.8, pabs * 0.21, po2 + 0.2, pabs * 0.16], "bar",
            f"PpO2 = {_fmt(pabs)} × 0,20 = {_fmt(po2)} bar."))
    return out


def _gen_archimede():
    out = []
    objs = ["Un bloc", "Une statuette remontée d'une épave", "Un objet",
            "Une ancre", "Un lest", "Une caisse étanche"]
    i = 0
    for W in [10, 12, 15, 18, 20, 24, 16, 22]:
        for Vol in [8, 10, 12, 13, 15]:
            pa = W - Vol
            verdict = "il coule" if pa > 0 else ("il remonte" if pa < 0 else "équilibre")
            obj = objs[i % len(objs)]
            out.append(_numq(f"gar{i}", 2,
                f"{obj} pèse {W} kg pour un volume de {Vol} L (eau de mer). "
                f"Quel est son poids apparent ?",
                pa, [W + Vol, Vol - W, 2 * W - Vol, pa - 2], "kg",
                f"Poussée = {Vol} kg ; poids apparent = {W} − {Vol} = {_fmt(pa)} kg ({verdict})."))
            i += 1
    return out


def _generate_all():
    questions = []
    for gen in (_gen_pression, _gen_boyle, _gen_autonomie, _gen_dalton, _gen_archimede):
        questions.extend(gen())
    return questions


# ===========================================================================
# Construction de la banque complète
# ===========================================================================

_CHAP_BY_NUM = {c["num"]: c for c in CHAPITRES}


def _attach(q, qid):
    chap = _CHAP_BY_NUM[q["chapitre"]]
    if "corrects" in q:                       # question à choix multiples
        multi = True
        corrects = sorted(set(q["corrects"]))
    else:                                      # question à réponse unique
        multi = False
        corrects = [q["correct"]]
    return {
        "id": qid,
        "chapitre": q["chapitre"],
        "chapitre_titre": chap["title"],
        "chapitre_slug": chap["slug"],
        "q": q["q"],
        "options": q["options"],
        "multi": multi,
        "corrects": corrects,
        "explication": q["explication"],
    }


def build_question_bank():
    """Banque complète : fiches + supplémentaires + exercices + factuelles + multi + calculs."""
    bank = []
    # 1) Questions des fiches de cours
    for chap in CHAPITRES:
        for i, q in enumerate(chap["questions"]):
            bank.append(_attach({**q, "chapitre": chap["num"]}, f"c{chap['num']}q{i}"))
    # 2) Listes manuelles (réponse unique + choix multiples)
    for prefix, source in (("s", QUESTIONS_SUPP), ("e", EXERCICE_QUESTIONS),
                           ("f", FACTUELLES), ("m", MULTI)):
        for i, q in enumerate(source):
            bank.append(_attach(q, f"{prefix}{i}"))
    # 3) Questions de calcul générées (id déjà unique)
    for q in _generate_all():
        bank.append(_attach(q, q["id"]))
    return bank


QUESTION_BANK = build_question_bank()
QUESTION_BY_ID = {q["id"]: q for q in QUESTION_BANK}

# Garde-fous : banque ≥ 400 questions, IDs uniques, et assez de questions à
# choix multiples pour garantir le quota d'au moins 10 par test de 40.
assert len(QUESTION_BANK) >= 400, "Banque insuffisante : %d questions" % len(QUESTION_BANK)
assert len(QUESTION_BY_ID) == len(QUESTION_BANK), "IDs de questions dupliqués !"
_NB_MULTI = sum(1 for q in QUESTION_BANK if q["multi"])
assert _NB_MULTI >= 10, "Pas assez de questions à choix multiples : %d" % _NB_MULTI
