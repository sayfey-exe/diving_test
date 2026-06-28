# -*- coding: utf-8 -*-
"""
Exercices d'entraînement, repris du cours théorique N2 (MPS 2011) et complétés.

Pour chaque chapitre concerné : une liste d'exercices {titre, enonce, correction}.

Note sur les exercices de tables MN90 : la correction détaille la *méthode*
complète (arrondis, calcul de DR / DTR / heure de sortie, classification des
plongées, majoration) et les valeurs calculables sûrement. La lecture finale du
palier et du GPS se fait sur la table MN90 officielle, affichée dans le
chapitre 11 — c'est précisément la compétence évaluée à l'examen. Vérifie
toujours tes paliers sur la table de référence.
"""

NOTE_TABLES = (
    "Pour ces exercices, garde la <strong>table MN90</strong> (affichée dans le "
    "chapitre 11) sous les yeux. La correction détaille la méthode ; lis le "
    "palier et le GPS directement sur la table à la profondeur et la durée "
    "indiquées. Rappel : profondeur ou durée absente → on prend la valeur "
    "<strong>immédiatement supérieure</strong> (jamais d'interpolation)."
)

EXERCICES = {
    # ---------------------------------------------------------------- Ch1 Pression
    1: [
        {
            "titre": "Pression absolue",
            "enonce": "Un plongeur descend à 33 m. Quelle est la pression absolue qu'il subit ?",
            "correction": (
                "Pabs = Patm + Phyd = 1 + 33/10 = 1 + 3,3 = <strong>4,3 bar</strong>."
            ),
        },
        {
            "titre": "Retrouver une profondeur",
            "enonce": "À quelle profondeur la pression absolue vaut-elle 3,5 bar ?",
            "correction": (
                "Phyd = Pabs − Patm = 3,5 − 1 = 2,5 bar. "
                "Profondeur = 2,5 × 10 = <strong>25 m</strong>."
            ),
        },
    ],
    # ---------------------------------------------------------------- Ch2 Archimède
    2: [
        {
            "titre": "Poids apparent d'une bouteille",
            "enonce": "Une bouteille pèse 18 kg pour un volume de 13 L. Quel est son poids "
                      "apparent dans l'eau de mer ? Coule-t-elle ?",
            "correction": (
                "Poussée d'Archimède = poids du volume d'eau déplacé = 13 kg "
                "(13 L = 13 dm³). Poids apparent = 18 − 13 = <strong>5 kg</strong>. "
                "Comme il est positif, <strong>la bouteille coule</strong>."
            ),
        },
        {
            "titre": "Lestage et équilibre",
            "enonce": "Un bloc a un poids apparent de +3 kg en fin de plongée. Que doit faire "
                      "le plongeur pour être en équilibre (flottabilité nulle) ?",
            "correction": (
                "Pour une flottabilité nulle, il faut un poids apparent = 0. Le plongeur doit "
                "donc ajouter de la flottabilité (gonfler légèrement son gilet) pour compenser "
                "ces +3 kg. <em>Remarque</em> : le gilet sert à s'équilibrer, pas à compenser "
                "un sur-lestage chronique."
            ),
        },
    ],
    # ---------------------------------------------------------------- Ch3 Boyle-Mariotte
    3: [
        {
            "titre": "Volume d'air à la remontée",
            "enonce": "À 30 m (4 bar), un plongeur gonfle sa bouée avec 2 L d'air. Il oublie "
                      "de purger à la remontée. Quel volume cet air occupe-t-il en surface ?",
            "correction": (
                "P1 × V1 = P2 × V2 → 4 × 2 = 1 × V2 → V2 = <strong>8 L</strong>. "
                "L'air a quadruplé : d'où le risque de remontée incontrôlée si on ne purge pas."
            ),
        },
        {
            "titre": "Compression à la descente",
            "enonce": "Un ballon souple contient 10 L d'air en surface. Quel sera son volume "
                      "à 20 m ?",
            "correction": (
                "À 20 m, Pabs = 3 bar. P1 × V1 = P2 × V2 → 1 × 10 = 3 × V2 → "
                "V2 = 10/3 ≈ <strong>3,3 L</strong>."
            ),
        },
    ],
    # ---------------------------------------------------------------- Ch4 Autonomie
    4: [
        {
            "titre": "Exercice du cours — temps avant réserve",
            "enonce": "Un plongeur dispose d'un bloc de 15 L gonflé à 200 bar. Il veut descendre "
                      "à 40 m et respire 20 L/min en surface. Réserve = 50 bar. Au bout de "
                      "combien de temps passe-t-il sur réserve ?",
            "correction": (
                "<strong>1. Air total</strong> : 15 × 200 = 3000 L.<br>"
                "<strong>2. Air consommable</strong> (on garde la réserve) : "
                "3000 − 15 × 50 = 3000 − 750 = 2250 L.<br>"
                "<strong>3. Consommation à 40 m</strong> (Pabs = 5 bar) : 20 × 5 = 100 L/min.<br>"
                "<strong>4. Temps</strong> : 2250 ÷ 100 = <strong>22,5 min</strong>."
            ),
        },
        {
            "titre": "Autonomie à 20 m",
            "enonce": "Bloc de 12 L à 200 bar, plongée à 20 m, consommation 18 L/min en surface, "
                      "réserve 50 bar. Quelle est l'autonomie avant la réserve ?",
            "correction": (
                "Air consommable = (200 − 50) × 12 = 150 × 12 = 1800 L.<br>"
                "Consommation à 20 m (Pabs = 3 bar) = 18 × 3 = 54 L/min.<br>"
                "Temps = 1800 ÷ 54 ≈ <strong>33 min</strong>."
            ),
        },
    ],
    # ---------------------------------------------------------------- Ch8 Dalton
    8: [
        {
            "titre": "Pressions partielles à 30 m",
            "enonce": "Pour de l'air (20 % O2, 80 % N2), calcule les pressions partielles "
                      "d'oxygène et d'azote à 30 m.",
            "correction": (
                "À 30 m, Pabs = 4 bar.<br>"
                "PpO2 = 4 × 0,20 = <strong>0,8 bar</strong>.<br>"
                "PpN2 = 4 × 0,80 = <strong>3,2 bar</strong>."
            ),
        },
        {
            "titre": "Profondeur de toxicité de l'O2",
            "enonce": "On considère l'oxygène dangereux à partir d'une pression partielle de "
                      "1,6 bar. À quelle profondeur cela correspond-il en plongée à l'air (21 % O2) ?",
            "correction": (
                "PpO2 = Pabs × 0,21 = 1,6 → Pabs = 1,6 ÷ 0,21 ≈ 7,6 bar → "
                "profondeur ≈ (7,6 − 1) × 10 ≈ <strong>66 m</strong>."
            ),
        },
    ],
    # ---------------------------------------------------------------- Ch11 Tables MN90 (1)
    11: [
        {
            "titre": "11.4 (a) — Plongée simple à 21 m / 45 min",
            "enonce": "Profondeur & durée de palier, GPS, pour une plongée à 21 m pendant 45 min ?",
            "correction": (
                "<strong>Profondeur</strong> : 21 m n'existe pas dans la table → on prend "
                "<strong>22 m</strong>. <strong>Durée</strong> : 45 min (existe).<br>"
                "→ Sur la table MN90, ligne 22 m / colonne 45 min : lis le "
                "<strong>palier à 3 m</strong> et le <strong>GPS</strong>."
            ),
        },
        {
            "titre": "11.4 (b) — Plongée simple à 25 m / 41 min",
            "enonce": "Profondeur & durée de palier, GPS, pour une plongée à 25 m pendant 41 min ?",
            "correction": (
                "<strong>Profondeur</strong> : 25 m (existe). <strong>Durée</strong> : 41 min "
                "n'existe pas → on prend <strong>45 min</strong>.<br>"
                "→ Table MN90, ligne 25 m / colonne 45 min : lis le palier à 3 m et le GPS."
            ),
        },
        {
            "titre": "11.4 (c) — HI = 14h45 / 34 m / 36 min",
            "enonce": "HI = 14h45, P = 34 m, DP = 36 min. Paliers ? Heure de sortie ? GPS ?",
            "correction": (
                "<strong>Profondeur</strong> : 34 m → <strong>35 m</strong>. "
                "<strong>Durée</strong> : 36 min → <strong>40 min</strong>.<br>"
                "Lis sur la table (35 m / 40 min) le palier à 3 m (appelons-le D<sub>pal</sub>), "
                "la <strong>DTR</strong> et le GPS.<br>"
                "<strong>Heure de sortie</strong> : HS = HI + DP + DTR = 14h45 + 36 min + DTR. "
                "<em>(On utilise la DP réelle, 36 min, pas l'arrondi.)</em>"
            ),
        },
        {
            "titre": "11.4 (d) — HI = 10h20 / 29 m / remontée à 10h53",
            "enonce": "HI = 10h20, P = 29 m, début de la remontée à 10h53. Paliers ? HS ? GPS ?",
            "correction": (
                "<strong>Durée de plongée</strong> : DP = 10h53 − 10h20 = <strong>33 min</strong>.<br>"
                "<strong>Profondeur</strong> : 29 m → <strong>30 m</strong>. "
                "<strong>Durée</strong> : 33 min → <strong>35 min</strong>.<br>"
                "Lis le palier, la DTR et le GPS sur la table (30 m / 35 min), puis "
                "HS = 10h53 + DTR."
            ),
        },
        {
            "titre": "11.6 — Remontée lente",
            "enonce": "HI = 11h00, P = 22 m. À 11h45 la palanquée remonte jusqu'à 17 m où elle "
                      "arrive à 11h50, puis remonte à la vitesse préconisée. Paliers ? GPS ? HS ?",
            "correction": (
                "La remontée de 22 m à 17 m (5 m) prend 5 min (11h45→11h50) : c'est une "
                "<strong>remontée lente</strong> (&lt; 15 m/min).<br>"
                "<strong>Règle</strong> : on intègre cette durée à la durée de plongée. "
                "DP = (11h45 − 11h00) + 5 min = 45 + 5 = <strong>50 min</strong>. P = 22 m.<br>"
                "Lis le palier et le GPS sur la table (22 m / 50 min).<br>"
                "<strong>Attention</strong> : on ne peut pas utiliser la colonne DTR de la "
                "table (on repart de 17 m, pas de 22 m). DR = (17 − 3)/15 ≈ 0,9 min ; "
                "DTR = DR + durée palier + 0,5 min. Puis HS = 11h50 + DTR."
            ),
        },
        {
            "titre": "11.7 — Remontée rapide",
            "enonce": "Immersion à 9h00 à 20 m, remontée rapide au bout de 30 min. Conduite à "
                      "tenir, paliers, GPS et HS ?",
            "correction": (
                "<strong>Conduite à tenir</strong> : redescendre à la mi-profondeur "
                "(20/2 = <strong>10 m</strong>) en moins de 3 min, y faire un palier de "
                "<strong>5 min</strong>, puis remonter (15 m/min) ; faire au minimum un palier "
                "de 2 min à 3 m même si la table n'en impose pas.<br>"
                "<strong>Durée de plongée retenue</strong> = de l'immersion à la fin du palier "
                "à mi-profondeur = 30 + 3 + 5 = <strong>38 min</strong> → arrondi à 40 min. "
                "P = 20 m.<br>"
                "Lis le palier et le GPS sur la table (20 m / 40 min), puis calcule HS."
            ),
        },
        {
            "titre": "11.8 — Palier interrompu",
            "enonce": "HI = 15h00, P = 37 m, DP = 25 min. Panne d'air au palier de 3 m après "
                      "10 min. Conduite à tenir, paliers, GPS et HS ?",
            "correction": (
                "<strong>Profondeur</strong> : 37 m → <strong>38 m</strong>. DP = 25 min.<br>"
                "<strong>Conduite à tenir</strong> : être redescendu au palier de 3 m en moins "
                "de 3 min et le <strong>refaire entièrement</strong> (on ne recommence que le "
                "palier interrompu et les suivants). Si c'est impossible (pas de bloc de "
                "secours), déclencher les secours et appliquer la procédure ADD à titre "
                "préventif.<br>"
                "Lis sur la table (38 m / 25 min) la durée totale du palier à 3 m et le GPS, "
                "puis HS = HI + DP + DTR + temps de redescente + palier refait."
            ),
        },
        {
            "titre": "11.9 — Exercice 1 : 9h50 / 23 m / 47 min",
            "enonce": "Immersion à 9h50, profondeur maxi 23 m, durée 47 min. Paliers, HS, GPS ?",
            "correction": (
                "P : 23 m → <strong>25 m</strong>. DP : 47 min → <strong>50 min</strong>.<br>"
                "Lis le palier à 3 m, la DTR et le GPS sur la table (25 m / 50 min). "
                "HS = 9h50 + 47 min + DTR."
            ),
        },
        {
            "titre": "11.9 — Exercice 3 : 9h00 / 22 m / remontée rapide",
            "enonce": "Immersion à 9h00, profondeur maxi 22 m. À 9h50 remontée depuis 22 m, "
                      "surface à 9h51. Paliers, HS, GPS ?",
            "correction": (
                "22 m en 1 min &gt; 17 m/min : <strong>remontée rapide</strong>. "
                "Mi-profondeur = 11 m → redescendre en &lt; 3 min, palier de 5 min, puis "
                "minimum 2 min à 3 m.<br>"
                "Durée retenue = 50 + 1 + 3 + 5 = <strong>59 min</strong> → 60 min. P = 22 m.<br>"
                "Lis le palier et le GPS sur la table (22 m / 60 min) ; calcule la DTR puis HS."
            ),
        },
    ],
    # ---------------------------------------------------------------- Ch12 Tables MN90 (2)
    12: [
        {
            "titre": "12.1 — Plongée consécutive",
            "enonce": "Une palanquée N2 s'immerge à 11h00 sur 20 m pendant 40 min. À 11h52, "
                      "deux plongeurs redescendent à 22 m pour récupérer un phare ; ils "
                      "remontent au bout de 6 min. Paliers, HS et GPS des deux plongées ?",
            "correction": (
                "<strong>1ère plongée</strong> : P = 20 m, DP = 40 min → lis palier/DTR/GPS sur "
                "la table, HS1 = 11h00 + 40 min + DTR1.<br>"
                "<strong>Intervalle</strong> : si HS1 ≈ 11h44, l'intervalle jusqu'à 11h52 est "
                "&lt; 15 min → ce sont des <strong>plongées consécutives</strong>.<br>"
                "<strong>Règle</strong> : on traite comme UNE seule plongée. "
                "P = profondeur maxi des deux = <strong>22 m</strong> ; "
                "DP = 40 + 6 = <strong>46 min</strong>.<br>"
                "Lis le palier et le GPS sur la table (22 m / 46 min → 50 min). "
                "On remonte depuis 22 m : la colonne DTR de la table est utilisable. "
                "HS2 = 11h52 + 6 min + DTR."
            ),
        },
        {
            "titre": "12.6 — Exercice 2 : successive avec GPS connu",
            "enonce": "Sortie de 1ère plongée à 9h00 avec GPS = D. 2ème plongée : début à "
                      "11h15, profondeur maxi 21 m, durée 14 min. Paliers et heure de sortie ?",
            "correction": (
                "<strong>Intervalle de surface</strong> : 11h15 − 9h00 = 2h15 → "
                "15 min ≤ IS &lt; 12h → <strong>plongée successive</strong>.<br>"
                "<strong>1. Azote résiduel</strong> : tableau 1, ligne GPS = D, colonne IS "
                "(2h15 → prendre 2h00, valeur inférieure par sécurité) → TN2.<br>"
                "<strong>2. Majoration</strong> : tableau 2, avec ce TN2 et P = 22 m (21→22) "
                "→ majoration M (en min).<br>"
                "<strong>3. Durée fictive</strong> = 14 + M → lis le palier sur la table "
                "(22 m / durée fictive arrondie).<br>"
                "<strong>Piège</strong> : la majoration ne compte PAS pour l'heure de sortie. "
                "HS = 11h15 + 14 min + DTR."
            ),
        },
        {
            "titre": "12.6 — Exercice 3 : plongée profonde + intervalle minimal",
            "enonce": "1ère plongée : immersion à 8h33, profondeur maxi 43 m, durée 41 min. "
                      "(1) Paliers et heure de sortie ? (2) Quel intervalle minimal pour faire "
                      "une 2ème plongée à 15 m pendant 20 min ?",
            "correction": (
                "<strong>(1)</strong> P = 43 m → <strong>45 m</strong>, DP = 41 min → 42 min "
                "(arrondi à la minute supérieure si besoin). Lis sur la table les paliers "
                "(souvent à 6 m et 3 m à cette profondeur), la DTR et le GPS. "
                "HS = 8h33 + 41 min + DTR.<br>"
                "<strong>(2)</strong> Méthode : pour la 2ème plongée planifiée à 15 m / 20 min, "
                "détermine la majoration maximale acceptable, puis via le tableau 2 le TN2 "
                "correspondant, puis via le tableau 1 (ligne GPS de la 1ère plongée) "
                "l'intervalle de surface minimal qui ramène à ce TN2."
            ),
        },
        {
            "titre": "12.6 — Exercice 6 : palier interrompu (35 m)",
            "enonce": "Plongée : immersion à 10h50, profondeur maxi 35 m, durée 30 min. Panne "
                      "d'air au bout de 5 min de palier à 3 m. Conduite à tenir, paliers, HS, GPS ?",
            "correction": (
                "P = 35 m, DP = 30 min. Lis sur la table (35 m / 30 min) la durée du palier à "
                "3 m, la DTR et le GPS.<br>"
                "<strong>Conduite à tenir</strong> : panne d'air pendant le palier → être "
                "redescendu au palier de 3 m en moins de 3 min et le <strong>refaire en "
                "entier</strong>. Si impossible : secours + procédure ADD préventive.<br>"
                "HS = 10h50 + 30 min + DTR + 3 min (redescente) + durée du palier refait."
            ),
        },
    ],
}
