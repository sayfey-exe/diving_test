# -*- coding: utf-8 -*-
"""
Contenu pédagogique de l'application de révision Niveau 2 (FFESSM / MN90).

Source : "Plongeur autonome Niveau II - Cours théorique" (MPS, 2011).

Chaque chapitre contient :
  - un résumé structuré (sections + points clés)
  - une liste "essentiel" (à retenir)
  - 3 questions d'auto-évaluation (QCM avec correction)
"""

CHAPITRES = [
    # ------------------------------------------------------------------ 1
    {
        "num": 1,
        "slug": "pression",
        "title": "La pression",
        "icon": "🌊",
        "accroche": "Tout part de là : comprendre les pressions, c'est comprendre la plongée.",
        "resume": [
            {
                "titre": "Définition",
                "points": [
                    "Une pression est le résultat d'une <strong>force appliquée sur une surface</strong>.",
                ],
            },
            {
                "titre": "Les pressions en plongée",
                "points": [
                    "<strong>Pression atmosphérique (Patm)</strong> : pression de l'air au-dessus de nous. Au niveau de la mer, on prend 1 ATM ≈ 1 bar.",
                    "<strong>Pression hydrostatique / relative (Phyd)</strong> : pression exercée par l'eau. Approximation plongée : <strong>+1 bar tous les 10 m</strong>.",
                    "<strong>Pression absolue (Pabs)</strong> : pression totale subie par le plongeur. <strong>Pabs = Patm + Phyd</strong>.",
                ],
            },
            {
                "titre": "À mémoriser : le tableau des pressions",
                "table": {
                    "head": ["Profondeur", "Patm", "Phyd", "Pabs"],
                    "rows": [
                        ["0 m", "1 b", "0 b", "1 b"],
                        ["10 m", "1 b", "1 b", "2 b"],
                        ["15 m", "1 b", "1,5 b", "2,5 b"],
                        ["20 m", "1 b", "2 b", "3 b"],
                        ["30 m", "1 b", "3 b", "4 b"],
                    ],
                },
            },
        ],
        "essentiel": [
            "Pabs = 1 + (profondeur ÷ 10).",
            "À 20 m → 3 bar absolus, à 40 m → 5 bar absolus.",
            "La pression hydrostatique augmente de 1 bar tous les 10 m.",
        ],
        "questions": [
            {
                "q": "Quelle est la pression absolue à 20 m de profondeur ?",
                "options": ["2 bar", "3 bar", "4 bar", "2,5 bar"],
                "correct": 1,
                "explication": "Pabs = Patm + Phyd = 1 + 20/10 = 1 + 2 = 3 bar.",
            },
            {
                "q": "À 25 m, quelle est la pression hydrostatique (relative) ?",
                "options": ["2 bar", "2,5 bar", "3,5 bar", "1,5 bar"],
                "correct": 1,
                "explication": "Phyd = profondeur / 10 = 25/10 = 2,5 bar. La pression absolue serait elle de 3,5 bar.",
            },
            {
                "q": "La pression absolue correspond à :",
                "options": [
                    "La pression de l'eau seule",
                    "La pression de l'air seule",
                    "Patm + Phyd",
                    "Phyd − Patm",
                ],
                "correct": 2,
                "explication": "Pabs = Patm + Phyd : c'est la pression totale subie par le plongeur.",
            },
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "num": 2,
        "slug": "archimede",
        "title": "Principe d'Archimède",
        "icon": "⚖️",
        "accroche": "Pourquoi flotte-t-on ou coule-t-on ? La poussée d'Archimède explique tout.",
        "resume": [
            {
                "titre": "Le principe",
                "points": [
                    "Tout corps plongé dans un liquide subit une <strong>poussée verticale dirigée de bas en haut</strong>, égale au <strong>poids du volume de liquide déplacé</strong>.",
                    "La poussée d'Archimède <strong>ne varie pas avec la profondeur</strong> : elle est constante.",
                ],
            },
            {
                "titre": "Poids apparent",
                "points": [
                    "<strong>P apparent = P réel − poussée d'Archimède</strong>.",
                    "Dans l'eau, un corps « pèse » moins lourd qu'en surface.",
                ],
            },
            {
                "titre": "Flottabilité",
                "points": [
                    "Flottabilité <strong>positive</strong> (l'objet remonte) → poids apparent < 0.",
                    "Flottabilité <strong>négative</strong> (l'objet coule) → poids apparent > 0.",
                    "Flottabilité <strong>nulle</strong> (équilibre) → poids apparent = 0.",
                ],
            },
            {
                "titre": "Exemple type",
                "points": [
                    "Bouteille de 18 kg, volume 13 L. Poussée = 13 kg (13 dm³ d'eau). "
                    "P apparent = 18 − 13 = <strong>5 kg > 0 → la bouteille coule</strong>.",
                ],
            },
        ],
        "essentiel": [
            "Poussée d'Archimède = poids du volume d'eau déplacé, constante avec la profondeur.",
            "P apparent = P réel − poussée.",
            "Poids apparent < 0 → ça flotte ; > 0 → ça coule ; = 0 → équilibre.",
        ],
        "questions": [
            {
                "q": "La poussée d'Archimède en fonction de la profondeur :",
                "options": [
                    "Augmente avec la profondeur",
                    "Diminue avec la profondeur",
                    "Est constante",
                    "S'annule à 10 m",
                ],
                "correct": 2,
                "explication": "La poussée d'Archimède est constante : elle ne dépend pas de la profondeur.",
            },
            {
                "q": "Un objet a une flottabilité positive. Cela signifie que :",
                "options": [
                    "Il coule, poids apparent > 0",
                    "Il remonte, poids apparent < 0",
                    "Il est en équilibre, poids apparent = 0",
                    "Sa poussée est nulle",
                ],
                "correct": 1,
                "explication": "Flottabilité positive = l'objet remonte = poids apparent < 0.",
            },
            {
                "q": "Bouteille de 18 kg pour 13 L. Quel est son poids apparent dans l'eau ?",
                "options": ["31 kg", "5 kg", "13 kg", "0 kg"],
                "correct": 1,
                "explication": "Poussée = 13 kg. P apparent = 18 − 13 = 5 kg (> 0 → elle coule).",
            },
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "num": 3,
        "slug": "boyle-mariotte",
        "title": "Loi de Boyle-Mariotte",
        "icon": "🎈",
        "accroche": "La loi qui relie pression et volume — et qui explique les barotraumatismes.",
        "resume": [
            {
                "titre": "La loi",
                "points": [
                    "À <strong>température constante</strong>, le volume d'un gaz est <strong>inversement proportionnel à la pression</strong>.",
                    "<strong>P1 × V1 = P2 × V2 = constante</strong>.",
                ],
            },
            {
                "titre": "Applications à la plongée",
                "points": [
                    "Les variations de pression modifient les volumes d'air (mécaniques et anatomiques).",
                    "C'est l'origine des <strong>barotraumatismes</strong>, évitables avec les bonnes précautions.",
                    "C'est <strong>près de la surface</strong> que les variations de volume sont les plus importantes.",
                ],
            },
            {
                "titre": "Exemple type",
                "points": [
                    "À 30 m (4 bar), on gonfle la bouée avec 2 L. Sans purger à la remontée : "
                    "4 × 2 = 1 × V2 → <strong>V2 = 8 L</strong> en surface.",
                ],
            },
        ],
        "essentiel": [
            "P1 × V1 = P2 × V2.",
            "Quand la pression augmente, le volume diminue (et inversement).",
            "Les plus fortes variations de volume sont près de la surface.",
        ],
        "questions": [
            {
                "q": "Que dit la loi de Boyle-Mariotte ?",
                "options": [
                    "Le volume est proportionnel à la pression",
                    "À température constante, P × V = constante",
                    "La pression augmente avec la température seulement",
                    "Le volume ne dépend pas de la pression",
                ],
                "correct": 1,
                "explication": "À température constante, P1×V1 = P2×V2 : le volume est inversement proportionnel à la pression.",
            },
            {
                "q": "À 30 m (4 bar) une bouée contient 2 L. Quel volume en surface si on ne purge pas ?",
                "options": ["2 L", "4 L", "8 L", "0,5 L"],
                "correct": 2,
                "explication": "P1×V1 = P2×V2 → 4×2 = 1×V2 → V2 = 8 L.",
            },
            {
                "q": "Où les variations de volume d'un gaz sont-elles les plus importantes ?",
                "options": [
                    "En profondeur (au-delà de 30 m)",
                    "Près de la surface",
                    "Au palier de 3 m uniquement",
                    "Elles sont identiques partout",
                ],
                "correct": 1,
                "explication": "Près de la surface, une même variation de profondeur fait varier le volume bien davantage.",
            },
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "num": 4,
        "slug": "autonomie",
        "title": "Calcul d'autonomie",
        "icon": "⏱️",
        "accroche": "Savoir combien de temps il reste d'air : un calcul vital pour l'autonomie.",
        "resume": [
            {
                "titre": "À quoi ça sert",
                "points": [
                    "Estimer une limite ou un besoin selon : quantité d'air, profondeur, temps, consommation.",
                ],
            },
            {
                "titre": "Méthodologie",
                "points": [
                    "1. Calculer la quantité d'air totale (capacité × pression).",
                    "2. Calculer la quantité d'air consommable (en gardant la réserve, ex. 50 bar).",
                    "3. Calculer la consommation à la profondeur : conso surface × Pabs.",
                    "4. En déduire le temps : air consommable ÷ consommation.",
                ],
            },
            {
                "titre": "Exemple type",
                "points": [
                    "Bloc 12 L à 200 b, 30 m, conso surface 20 L/min, réserve 50 b.",
                    "Air total = 12 × 200 = 2400 L. Air consommable = 2400 − 12×50 = 1800 L.",
                    "Conso à 30 m (4 b) = 20 × 4 = 80 L/min.",
                    "Temps = 1800 ÷ 80 = <strong>22,5 min</strong>.",
                ],
            },
        ],
        "essentiel": [
            "Quantité d'air = Volume du bloc × Pression.",
            "Consommation à la profondeur = consommation en surface × Pabs.",
            "On garde toujours la réserve (souvent 50 bar) dans le calcul.",
        ],
        "questions": [
            {
                "q": "Un plongeur respire 20 L/min en surface. Quelle est sa consommation à 30 m ?",
                "options": ["20 L/min", "40 L/min", "60 L/min", "80 L/min"],
                "correct": 3,
                "explication": "À 30 m, Pabs = 4 bar. Conso = 20 × 4 = 80 L/min.",
            },
            {
                "q": "Quelle quantité d'air contient un bloc de 12 L gonflé à 200 bar ?",
                "options": ["1200 L", "2400 L", "240 L", "200 L"],
                "correct": 1,
                "explication": "Quantité d'air = 12 × 200 = 2400 litres d'air détendu.",
            },
            {
                "q": "Dans un calcul d'autonomie, la réserve de sécurité :",
                "options": [
                    "Est ignorée dans le calcul",
                    "Est conservée (souvent 50 bar) et donc soustraite de l'air utilisable",
                    "Vaut toujours 100 bar",
                    "Est ajoutée à l'air consommable",
                ],
                "correct": 1,
                "explication": "On retire la réserve (ex. 50 bar) de l'air disponible : on ne plonge pas dessus.",
            },
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "num": 5,
        "slug": "barotraumatismes",
        "title": "Les barotraumatismes",
        "icon": "👂",
        "accroche": "Des accidents mécaniques liés à la pression, faciles à prévenir.",
        "images": [
            {"src": "oreille.png", "alt": "Anatomie de l'oreille",
             "caption": "Anatomie de l'oreille : externe, moyenne et interne."},
            {"src": "sinus.png", "alt": "Les sinus de la face",
             "caption": "Les sinus (frontal, ethmoïdal, maxillaire)."},
            {"src": "appareil-respiratoire.png", "alt": "Appareil respiratoire",
             "caption": "L'appareil respiratoire (surpression pulmonaire)."},
        ],
        "resume": [
            {
                "titre": "Mécanisme général",
                "points": [
                    "Dus aux <strong>déséquilibres de pression dans les espaces aériens anatomiques</strong>.",
                    "Liés à la loi de <strong>Boyle-Mariotte</strong>.",
                    "Les différences de pression sont les plus importantes <strong>près de la surface</strong>.",
                    "Ils sont <strong>indépendants de la durée et de la profondeur</strong> de la plongée.",
                ],
            },
            {
                "titre": "Les principaux barotraumatismes",
                "table": {
                    "head": ["Accident", "À la descente", "À la remontée"],
                    "rows": [
                        ["Oreilles", "✔", "✔"],
                        ["Sinus", "✔", "✔"],
                        ["Plaquage du masque", "✔", ""],
                        ["Dents", "", "✔"],
                        ["Estomac / intestins", "", "✔"],
                        ["Surpression pulmonaire", "", "✔"],
                    ],
                },
            },
            {
                "titre": "Points clés",
                "points": [
                    "<strong>Oreilles</strong> : équilibrer dès la tête sous l'eau, ne pas forcer. <strong>Pas de Valsalva à la remontée !</strong>",
                    "<strong>Plaquage du masque</strong> : souffler par le nez dans le masque à la descente.",
                    "<strong>Surpression pulmonaire</strong> : le plus grave mais le plus facile à éviter → <strong>ne jamais bloquer son expiration à la remontée</strong>. Entre 10 m et 0 m, le volume est multiplié par 2.",
                ],
            },
        ],
        "essentiel": [
            "Seul le plaquage du masque ne survient qu'à la descente ; dents, estomac et surpression pulmonaire seulement à la remontée.",
            "Pas de Valsalva à la remontée.",
            "Surpression pulmonaire : expirer normalement à la remontée, ne jamais bloquer sa respiration.",
        ],
        "questions": [
            {
                "q": "Quel barotraumatisme survient uniquement à la descente ?",
                "options": [
                    "La surpression pulmonaire",
                    "Le plaquage du masque",
                    "Les dents",
                    "L'estomac",
                ],
                "correct": 1,
                "explication": "Le plaquage du masque est le seul accident purement de descente ; les autres cités sont à la remontée.",
            },
            {
                "q": "Comment éviter la surpression pulmonaire ?",
                "options": [
                    "Faire un Valsalva à la remontée",
                    "Bloquer sa respiration en remontant",
                    "Expirer normalement, ne pas bloquer son air à la remontée",
                    "Descendre lentement",
                ],
                "correct": 2,
                "explication": "Il faut expirer normalement à la remontée : ne jamais bloquer son expiration.",
            },
            {
                "q": "À propos du Valsalva :",
                "options": [
                    "Il faut le faire à la remontée",
                    "Il ne faut jamais le faire à la remontée",
                    "Il est interdit à la descente",
                    "Il sert à équilibrer l'estomac",
                ],
                "correct": 1,
                "explication": "Attention : PAS de Valsalva à la remontée (risque pour l'oreille interne).",
            },
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "num": 6,
        "slug": "henry",
        "title": "Loi de Henry",
        "icon": "🫧",
        "accroche": "Comment l'azote se dissout dans le corps — la base des accidents de décompression.",
        "resume": [
            {
                "titre": "La loi",
                "points": [
                    "À température constante et à saturation, la <strong>quantité de gaz dissoute dans un liquide est proportionnelle à la pression</strong> exercée sur ce liquide.",
                    "Plus la pression augmente, plus la quantité de gaz dissous augmente.",
                ],
            },
            {
                "titre": "Les 3 états de dissolution",
                "points": [
                    "<strong>Saturation</strong> : équilibre, P = T (T = tension du gaz dissous).",
                    "<strong>Sous-saturation</strong> (descente) : la pression augmente vite, l'azote se dissout lentement → P > T.",
                    "<strong>Sur-saturation</strong> (remontée) : la pression diminue vite, l'azote s'élimine lentement → P < T.",
                    "<strong>Sursaturation critique</strong> (T ≫ P) : dégazage anarchique → grosses bulles → accident.",
                ],
            },
            {
                "titre": "En plongée",
                "points": [
                    "Le gaz concerné est l'<strong>azote (N2)</strong> ; le liquide est l'ensemble du corps humain (≈ 70 % d'eau).",
                    "Facteurs de dissolution : pression, temps, nature du gaz/liquide, surface d'échange, <strong>agitation</strong>, température.",
                ],
            },
        ],
        "essentiel": [
            "Descente = sous-saturation (P > T) ; remontée = sur-saturation (P < T).",
            "Le gaz qui pose problème est l'azote (N2).",
            "Plus le plongeur est agité, plus l'azote se dissout : rester calme.",
        ],
        "questions": [
            {
                "q": "Quel gaz est responsable des accidents de décompression ?",
                "options": ["L'oxygène (O2)", "Le gaz carbonique (CO2)", "L'azote (N2)", "L'hélium"],
                "correct": 2,
                "explication": "C'est l'azote : il ne participe pas au métabolisme et se dissout/dégaze selon la pression.",
            },
            {
                "q": "À la remontée, dans quel état de dissolution se trouve-t-on ?",
                "options": [
                    "Saturation (P = T)",
                    "Sous-saturation (P > T)",
                    "Sur-saturation (P < T)",
                    "Aucun",
                ],
                "correct": 2,
                "explication": "À la remontée la pression chute vite alors que l'azote s'élimine lentement : sur-saturation, P < T.",
            },
            {
                "q": "Quel facteur augmente la dissolution de l'azote dans le corps ?",
                "options": [
                    "Rester parfaitement immobile",
                    "L'agitation du plongeur",
                    "Une eau très chaude uniquement",
                    "Une plongée très courte",
                ],
                "correct": 1,
                "explication": "Plus un plongeur est agité, plus les gaz se dissolvent : il faut rester calme et économe.",
            },
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "num": 7,
        "slug": "add",
        "title": "Les accidents de décompression (ADD)",
        "icon": "🩸",
        "accroche": "Le risque majeur de la plongée à l'air — mécanisme, symptômes, traitement, prévention.",
        "images": [
            {"src": "circulation-sanguine.png", "alt": "Circulation sanguine",
             "caption": "La circulation sanguine : les bulles d'azote diffusent dans tout l'organisme."},
        ],
        "resume": [
            {
                "titre": "Mécanisme",
                "points": [
                    "Le corps est partagé en <strong>compartiments</strong> qui se saturent/désaturent à des vitesses différentes.",
                    "En cas de dépassement de la sursaturation critique, l'azote forme des <strong>bulles</strong> qui bloquent la micro-circulation.",
                    "Les bulles grossissent à la remontée (Boyle-Mariotte) jusqu'à bloquer la circulation.",
                ],
            },
            {
                "titre": "Symptômes (souvent < 1 h, parfois jusqu'à 12 h après)",
                "points": [
                    "<strong>Les puces</strong> : fourmillements, plaques rouges (peau).",
                    "<strong>Les moutons</strong> : cloques, sensation de neige crépitante (tissus sous-cutanés).",
                    "<strong>Ostéo-articulaires</strong> : douleurs aux articulations (surtout pros).",
                    "<strong>Neurologiques</strong> : fourmillements/fatigue des jambes, troubles moteurs, visuels, paralysie.",
                    "<strong>Cochléo-vestibulaires</strong> : vertiges, nausées, acouphènes (oreille interne).",
                ],
            },
            {
                "titre": "Traitement",
                "points": [
                    "<strong>Oxygénothérapie</strong> (O2 à 100 %).",
                    "<strong>Aspirine 0,5 g</strong> (sauf allergie, à proposer).",
                    "Faire boire (vérifier que la victime peut uriner), prévenir l'état de choc.",
                    "Relever les paramètres de plongée, évacuer vite vers un <strong>caisson hyperbare</strong>.",
                ],
            },
            {
                "titre": "Prévention",
                "points": [
                    "Respecter vitesse de remontée et paliers ; maîtriser son autonomie en air.",
                    "Pas d'apnée ni d'effort après la plongée.",
                    "<strong>Pas d'avion ni d'altitude dans les 12 à 24 h</strong>.",
                    "Attention au froid, à la fatigue, à l'effort, à l'anxiété, à l'hypoglycémie (facteurs favorisants).",
                ],
            },
        ],
        "essentiel": [
            "La plupart des ADD se déclarent dans l'heure, mais c'est possible jusqu'à 12 h après.",
            "Traitement : O2 + aspirine 0,5 g + faire boire + caisson hyperbare.",
            "Pas d'avion dans les 12 à 24 h suivant une plongée.",
        ],
        "questions": [
            {
                "q": "Dans quel délai se déclarent le plus souvent les ADD ?",
                "options": [
                    "Immédiatement uniquement",
                    "Au maximum 1 h après (parfois jusqu'à 12 h)",
                    "Toujours après 24 h",
                    "Une semaine après",
                ],
                "correct": 1,
                "explication": "La plupart se déclarent dans l'heure ; certains peuvent survenir jusqu'à 12 h après la plongée.",
            },
            {
                "q": "Quel est le traitement de première intention d'un ADD ?",
                "options": [
                    "Faire redescendre la victime",
                    "Oxygénothérapie, aspirine 0,5 g, faire boire, caisson",
                    "Donner à manger et laisser se reposer",
                    "Faire un Valsalva",
                ],
                "correct": 1,
                "explication": "O2 à 100 %, aspirine 0,5 g (sauf allergie), faire boire, évacuation vers un caisson hyperbare.",
            },
            {
                "q": "Combien de temps faut-il attendre avant de prendre l'avion après une plongée ?",
                "options": ["1 h", "6 h", "12 à 24 h", "48 h minimum"],
                "correct": 2,
                "explication": "Il ne faut pas prendre l'avion ni aller en altitude dans les 12 à 24 h suivant la plongée.",
            },
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "num": 8,
        "slug": "dalton",
        "title": "Règles de Dalton",
        "icon": "🧪",
        "accroche": "Les pressions partielles : indispensables pour comprendre la toxicité des gaz.",
        "resume": [
            {
                "titre": "La loi",
                "points": [
                    "La pression d'un mélange gazeux est égale à la <strong>somme des pressions partielles</strong> de chaque gaz.",
                    "<strong>Pression partielle (Ppa) = Pression totale × pourcentage du gaz</strong>.",
                    "L'air est composé d'environ <strong>20 % d'O2 et 80 % de N2</strong>.",
                ],
            },
            {
                "titre": "Exemples",
                "points": [
                    "En surface (1 bar) : PpO2 = 0,2 bar ; PpN2 = 0,8 bar.",
                    "À 30 m (4 bar) : PpO2 = 0,8 bar ; PpN2 = 3,2 bar.",
                ],
            },
        ],
        "essentiel": [
            "Ppa = Ptotale × % du gaz.",
            "Air ≈ 20 % O2 + 80 % N2.",
            "La pression partielle augmente avec la profondeur → toxicité possible.",
        ],
        "questions": [
            {
                "q": "Quelle est la pression partielle d'oxygène en surface (air) ?",
                "options": ["0,8 bar", "0,2 bar", "1 bar", "0,04 bar"],
                "correct": 1,
                "explication": "PpO2 = 1 × 20 % = 0,2 bar en surface.",
            },
            {
                "q": "Quelle est la pression partielle d'azote à 30 m ?",
                "options": ["0,8 bar", "1,6 bar", "3,2 bar", "4 bar"],
                "correct": 2,
                "explication": "À 30 m, Pabs = 4 bar. PpN2 = 4 × 80 % = 3,2 bar.",
            },
            {
                "q": "Comment calcule-t-on la pression partielle d'un gaz ?",
                "options": [
                    "Ptotale ÷ pourcentage du gaz",
                    "Ptotale × pourcentage du gaz",
                    "Pourcentage ÷ profondeur",
                    "Ptotale + pourcentage",
                ],
                "correct": 1,
                "explication": "Ppa = Pression totale × concentration (pourcentage) du gaz dans le mélange.",
            },
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "num": 9,
        "slug": "toxicite-gaz",
        "title": "Accidents dus à la toxicité des gaz",
        "icon": "😵",
        "accroche": "Essoufflement, narcose, toxicité de l'oxygène : trois pièges des profondeurs.",
        "resume": [
            {
                "titre": "L'essoufflement (intoxication au CO2)",
                "points": [
                    "Excès de gaz carbonique, souvent après un effort. L'expiration devient insuffisante → cercle vicieux.",
                    "Peut aller jusqu'à la syncope hypercapnique (rendez-vous syncopal des 7 m).",
                    "<strong>CAT</strong> : arrêter l'effort, favoriser l'<strong>expiration</strong>, remonter de quelques mètres, prévenir la palanquée.",
                    "<strong>À 40 m, on ne récupère pas d'un essoufflement → on remonte.</strong>",
                ],
            },
            {
                "titre": "La narcose (ivresse des profondeurs)",
                "points": [
                    "Due à l'élévation de la <strong>pression partielle d'azote</strong> (et probablement du CO2).",
                    "Possible dès 30 m, fréquente à partir de 40 m. Symptômes : comportement incohérent, désorientation, perte de la notion du temps.",
                    "<strong>Traitement</strong> : remonter au-dessus de 35 m → les symptômes disparaissent.",
                ],
            },
            {
                "titre": "Toxicité de l'oxygène",
                "points": [
                    "L'O2 devient dangereux à partir d'une <strong>Pp d'environ 1,6 bar</strong> (≈ 66 m à l'air).",
                    "Concerne surtout les Niveaux 3 et les plongeurs Nitrox.",
                ],
            },
        ],
        "essentiel": [
            "Essoufflement = intoxication au CO2 → favoriser l'expiration.",
            "Narcose = azote → le traitement est de remonter.",
            "O2 toxique à partir de ≈ 1,6 bar de pression partielle.",
        ],
        "questions": [
            {
                "q": "L'essoufflement est une intoxication à quel gaz ?",
                "options": ["L'azote (N2)", "L'oxygène (O2)", "Le gaz carbonique (CO2)", "L'hélium"],
                "correct": 2,
                "explication": "L'essoufflement est une intoxication au CO2 (gaz carbonique) : il faut favoriser l'expiration.",
            },
            {
                "q": "Quel est le traitement radical de la narcose ?",
                "options": [
                    "Descendre plus profond",
                    "Remonter au-dessus de 35 m",
                    "Respirer plus vite",
                    "Faire un palier de 10 min",
                ],
                "correct": 1,
                "explication": "La narcose disparaît en remontant : au-dessus de 35 m la Pp d'azote diminue suffisamment.",
            },
            {
                "q": "À partir de quelle pression partielle l'oxygène devient-il dangereux ?",
                "options": ["0,2 bar", "1,6 bar", "0,8 bar", "3,2 bar"],
                "correct": 1,
                "explication": "L'O2 est considéré dangereux à partir d'environ 1,6 bar (≈ 66 m à l'air).",
            },
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "num": 10,
        "slug": "noyade",
        "title": "La noyade",
        "icon": "🆘",
        "accroche": "Reconnaître et réagir : la noyade peut conclure de nombreux accidents de plongée.",
        "resume": [
            {
                "titre": "Définitions",
                "points": [
                    "Environ <strong>140 000 décès par an</strong> dans le monde, surtout chez les jeunes adultes.",
                    "<strong>Noyades primaires</strong> : la noyade proprement dite (épuisement, chute, incapacité technique).",
                    "<strong>Noyades secondaires</strong> : succèdent à une syncope ou une perte de connaissance en milieu irrespirable.",
                ],
            },
            {
                "titre": "En plongée",
                "points": [
                    "En apnée : <strong>syncope des 7 m</strong> après hyperventilation, syncope sur douleur d'un barotraumatisme.",
                    "En scaphandre : défaillance matériel, ADD, narcose, intoxication O2, surpression pulmonaire.",
                ],
            },
            {
                "titre": "Conduite à tenir",
                "points": [
                    "Extraire du milieu en <strong>maintenant le détendeur en bouche</strong>, faire le signe de détresse.",
                    "Appeler les secours spécialisés, réchauffer et rassurer.",
                    "Selon le cas : oxygène, bouche-à-bouche, PLS, massage cardiaque externe.",
                ],
            },
        ],
        "essentiel": [
            "Syncope des 7 m = liée à l'hyperventilation en apnée.",
            "Toujours maintenir le détendeur en bouche en remontant la victime.",
            "Noyade secondaire = consécutive à une syncope / perte de connaissance.",
        ],
        "questions": [
            {
                "q": "La syncope des 7 mètres en apnée est favorisée par :",
                "options": [
                    "Une descente trop lente",
                    "L'hyperventilation avant l'apnée",
                    "Un palier trop long",
                    "Le froid uniquement",
                ],
                "correct": 1,
                "explication": "L'hyperventilation retarde l'envie de respirer et peut provoquer une syncope vers 7 m à la remontée.",
            },
            {
                "q": "En remontant une victime de noyade, il faut :",
                "options": [
                    "Lui retirer le détendeur",
                    "Maintenir le détendeur en bouche",
                    "La faire redescendre",
                    "Lui faire un Valsalva",
                ],
                "correct": 1,
                "explication": "On maintient le détendeur en bouche pendant l'extraction du milieu.",
            },
            {
                "q": "Une noyade secondaire :",
                "options": [
                    "Est la noyade par épuisement",
                    "Succède à une syncope ou perte de connaissance",
                    "Ne concerne que les non-nageurs",
                    "Survient toujours en surface",
                ],
                "correct": 1,
                "explication": "La noyade secondaire fait suite à une syncope/perte de connaissance en milieu irrespirable.",
            },
        ],
    },
    # ------------------------------------------------------------------ 11
    {
        "num": 11,
        "slug": "tables-mn90-1",
        "title": "Les tables MN90 — 1ère partie",
        "icon": "📊",
        "accroche": "Le protocole de décompression de référence pour le passage du Niveau 2.",
        "images": [
            {"src": "profil-plongee.png", "alt": "Profil de plongée et lecture de table",
             "caption": "Profil d'une plongée simple et lecture de la table MN90 (P, durée, palier, DTR, GPS)."},
            {"src": "courbe-securite.png", "alt": "Courbe de sécurité MN90",
             "caption": "La courbe de sécurité : zone de plongées sans palier (1ère plongée du jour)."},
            {"src": "table-mn90.png", "alt": "Table MN90 FFESSM",
             "caption": "La table MN90 (FFESSM) — à utiliser pour les exercices."},
        ],
        "resume": [
            {
                "titre": "Présentation",
                "points": [
                    "<strong>MN90 = Marine Nationale, 1990</strong>. Adoptées par la FFESSM pour les brevets.",
                    "Vitesse de remontée : 15 à 17 m/min (≈ 1 m toutes les 4 s), <strong>fixée à 15 m/min</strong> pour les exercices.",
                    "Entre les paliers : 6 m/min (30 s par tranche de 3 m).",
                    "Paliers de décompression de <strong>3 en 3 m</strong>.",
                ],
            },
            {
                "titre": "Conditions d'utilisation",
                "points": [
                    "Plongées à l'air, au niveau de la mer (max 300 m d'altitude), 60 m maxi.",
                    "2 plongées maximum par 24 h, effort modéré, plongeur entraîné.",
                ],
            },
            {
                "titre": "Paramètres",
                "points": [
                    "<strong>P</strong> = profondeur <strong>maximale</strong> atteinte (même brièvement). Si absente de la table → valeur immédiatement supérieure.",
                    "<strong>DP</strong> = durée de plongée, de l'immersion (HI) au début de remontée (HR), arrondie à la minute supérieure.",
                    "La table donne : profondeur et durée des paliers + le <strong>GPS</strong> (groupe de plongée successive).",
                    "<strong>DTR</strong> = durée totale de remontée.",
                ],
            },
            {
                "titre": "Cas particuliers",
                "points": [
                    "<strong>Courbe de sécurité</strong> : pas de palier obligatoire (1ère plongée du jour). Palier de sécurité recommandé : 3 min à 3 m.",
                    "<strong>Remontée lente</strong> (< 15 m/min) : intégrer la durée de remontée à la DP.",
                    "<strong>Remontée rapide</strong> (> 17 m/min) : redescendre à mi-profondeur en < 3 min, palier de 5 min, puis au moins 2 min à 3 m.",
                    "<strong>Palier interrompu</strong> : y redescendre en < 3 min et le refaire entièrement.",
                ],
            },
        ],
        "essentiel": [
            "MN90 = Marine Nationale 1990 ; vitesse conventionnelle de remontée = 15 m/min.",
            "La profondeur à retenir est la profondeur MAXIMALE atteinte.",
            "Valeur absente de la table → on prend la valeur immédiatement supérieure (jamais d'interpolation).",
        ],
        "questions": [
            {
                "q": "Que signifie « MN90 » ?",
                "options": [
                    "Modèle Numérique 1990",
                    "Marine Nationale 1990",
                    "Mélange Nitrox 90 %",
                    "Manuel Niveau 90",
                ],
                "correct": 1,
                "explication": "MN90 = Marine Nationale, tables utilisées à partir de 1990.",
            },
            {
                "q": "Quelle vitesse de remontée est utilisée par convention pour les exercices ?",
                "options": ["6 m/min", "10 m/min", "15 m/min", "20 m/min"],
                "correct": 2,
                "explication": "La vitesse de remontée est fixée par convention à 15 m/min (entre les paliers : 6 m/min).",
            },
            {
                "q": "Quelle profondeur retient-on pour entrer dans les tables ?",
                "options": [
                    "La profondeur moyenne de la plongée",
                    "La profondeur maximale atteinte",
                    "La profondeur du palier",
                    "La profondeur de fin de plongée",
                ],
                "correct": 1,
                "explication": "On retient toujours la profondeur maximale atteinte, même si elle n'a duré que quelques secondes.",
            },
        ],
    },
    # ------------------------------------------------------------------ 12
    {
        "num": 12,
        "slug": "tables-mn90-2",
        "title": "Les tables MN90 — 2ème partie",
        "icon": "📈",
        "accroche": "Plongées consécutives et successives : gérer l'azote résiduel entre deux plongées.",
        "resume": [
            {
                "titre": "L'intervalle de surface (IS)",
                "points": [
                    "IS = temps entre l'arrivée en surface de la 1ère plongée et l'immersion de la 2ème.",
                    "2 plongées maximum par 24 h.",
                ],
            },
            {
                "titre": "Plongées CONSÉCUTIVES (IS < 15 min)",
                "points": [
                    "On considère une <strong>seule plongée</strong> : DP = somme des deux durées, P = profondeur maximale des deux plongées.",
                    "Cas à éviter (force majeure uniquement).",
                ],
            },
            {
                "titre": "Plongées SUCCESSIVES (15 min ≤ IS < 12 h)",
                "points": [
                    "Calculer la <strong>tension d'azote résiduel (TN2)</strong> via le <strong>tableau 1</strong> (selon GPS et IS).",
                    "Calculer la <strong>majoration</strong> via le <strong>tableau 2</strong> (selon TN2 et profondeur prévue).",
                    "La majoration = allongement fictif de la durée de la 2ème plongée → on l'ajoute à la DP pour calculer les paliers.",
                    "Le GPS codifie la quantité d'azote résiduel (lettres de A à P).",
                ],
            },
            {
                "titre": "Pièges et règles",
                "points": [
                    "<strong>Piège</strong> : la majoration ne compte PAS dans le calcul de l'heure de sortie.",
                    "La majoration est <strong>définitive</strong> : on ne la recalcule pas en cours de plongée.",
                    "IS absent du tableau 1 → valeur immédiatement <strong>inférieure</strong> (sécurité). Profondeur absente du tableau 2 → valeur supérieure.",
                ],
            },
        ],
        "essentiel": [
            "IS < 15 min → consécutives (une seule plongée). 15 min ≤ IS < 12 h → successives (majoration).",
            "Tableau 1 → azote résiduel ; tableau 2 → majoration.",
            "Piège classique : la majoration ne compte pas pour l'heure de sortie.",
        ],
        "questions": [
            {
                "q": "Deux plongées séparées de moins de 15 minutes sont :",
                "options": ["Successives", "Consécutives", "Indépendantes", "Interdites"],
                "correct": 1,
                "explication": "IS < 15 min → plongées consécutives : DP = somme des durées, P = profondeur max des deux.",
            },
            {
                "q": "Une plongée est dite « successive » quand l'intervalle de surface est :",
                "options": [
                    "Inférieur à 15 min",
                    "Entre 15 min et 12 h",
                    "Supérieur à 12 h",
                    "Supérieur à 24 h",
                ],
                "correct": 1,
                "explication": "Successive : 15 min ≤ IS < 12 h. Au-delà de 12 h, on considère une plongée simple.",
            },
            {
                "q": "La majoration intervient-elle dans le calcul de l'heure de sortie ?",
                "options": [
                    "Oui, on l'ajoute toujours",
                    "Non, c'est un piège classique",
                    "Seulement si IS < 1 h",
                    "Seulement au-delà de 40 m",
                ],
                "correct": 1,
                "explication": "Attention piège : la majoration sert à calculer les paliers, pas l'heure de sortie.",
            },
        ],
    },
    # ------------------------------------------------------------------ 13
    {
        "num": 13,
        "slug": "reglementation",
        "title": "Réglementation",
        "icon": "📋",
        "accroche": "Prérogatives, licence, assurance, certificat médical : le cadre légal du Niveau 2.",
        "resume": [
            {
                "titre": "Le Niveau 2",
                "points": [
                    "Candidature : titulaire du N1 FFESSM, licence en cours de validité, <strong>≥ 16 ans</strong>, certificat médical < 1 an.",
                    "Prérogatives : <strong>autonomie jusqu'à 20 m</strong> entre N2, ou <strong>encadré jusqu'à 40 m</strong>.",
                    "Autonomie = responsabilités partagées, pas de chef de palanquée.",
                ],
            },
            {
                "titre": "Équipement en autonomie (par plongeur)",
                "points": [
                    "Un gilet stabilisateur (gonflage au gaz comprimé).",
                    "Un moyen de contrôle : ordinateur OU tables + profondimètre + montre/timer.",
                    "De quoi donner de l'air sans échange d'embout (octopus ou 2 détendeurs).",
                ],
            },
            {
                "titre": "Licence, assurance, certificat médical",
                "points": [
                    "<strong>Licence FFESSM</strong> : validité 15 mois (loisir).",
                    "<strong>RC au tiers</strong> obligatoire (fournie avec la licence) ; individuelle facultative mais fortement conseillée.",
                    "Tout sinistre déclaré sous <strong>5 jours</strong> (AXA assistance + cabinet Lafont). La RC pénale n'est pas couverte.",
                    "<strong>Certificat médical</strong> de non-contre-indication, valable 1 an.",
                ],
            },
            {
                "titre": "Bouteilles",
                "points": [
                    "Tout récipient dont (Pression × Volume) > 80 litres est soumis à ré-épreuve.",
                ],
            },
        ],
        "essentiel": [
            "N2 : autonomie 20 m entre N2, encadré jusqu'à 40 m.",
            "Licence FFESSM valable 15 mois ; certificat médical valable 1 an.",
            "Sinistre à déclarer sous 5 jours.",
        ],
        "questions": [
            {
                "q": "Jusqu'à quelle profondeur un N2 peut-il plonger en autonomie (entre N2) ?",
                "options": ["10 m", "20 m", "40 m", "60 m"],
                "correct": 1,
                "explication": "En autonomie, le N2 plonge jusqu'à 20 m ; il peut aller à 40 m mais encadré par un guide de palanquée.",
            },
            {
                "q": "Quelle est la durée de validité de la licence FFESSM (loisir) ?",
                "options": ["12 mois", "15 mois", "24 mois", "1 saison"],
                "correct": 1,
                "explication": "La licence loisir est valable 15 mois (d'octobre à décembre de l'année suivante).",
            },
            {
                "q": "Dans quel délai un sinistre doit-il être déclaré ?",
                "options": ["24 h", "5 jours", "15 jours", "1 mois"],
                "correct": 1,
                "explication": "Tout sinistre doit être déclaré dans un délai maximum de 5 jours (cabinet Lafont).",
            },
        ],
    },
    # ------------------------------------------------------------------ 14
    {
        "num": 14,
        "slug": "comportement-securite",
        "title": "Comportement et sécurité",
        "icon": "🦺",
        "accroche": "Les bons réflexes avant, pendant et après la plongée.",
        "resume": [
            {
                "titre": "Généralités — ne pas plonger si…",
                "points": [
                    "Rhume ou sinusite, mauvaise forme physique ou psychologique, ou simplement pas envie.",
                    "Vous êtes le seul juge de votre état : ne vous laissez pas influencer.",
                ],
            },
            {
                "titre": "Avant la plongée",
                "points": [
                    "Vérifier la pression et le bon fonctionnement du matériel (contrôle mutuel possible).",
                    "Repérer l'équipement de sa palanquée, connaître le maniement du gilet des coéquipiers.",
                    "Écouter les directives du guide de palanquée / directeur de plongée ; en autonomie, planifier la plongée.",
                ],
            },
            {
                "titre": "Mise à l'eau et en plongée",
                "points": [
                    "Vérifier que la bouteille est ouverte : l'aiguille du manomètre <strong>ne bouge pas</strong> quand on respire.",
                    "Rester groupé, se surveiller, contrôler régulièrement sa consommation et ses paramètres de déco.",
                    "Gérer son orientation, être correctement lesté et équilibré.",
                ],
            },
            {
                "titre": "Fin de plongée et perte de palanquée",
                "points": [
                    "Respecter la vitesse de remontée et les paliers, faire un tour d'horizon.",
                    "Après : prévenir le DP au moindre symptôme, pas d'avion 12 h, pas d'apnée ni d'effort.",
                    "<strong>Perte de palanquée</strong> : 1 à 2 tours d'horizon (~1 min max), puis remonter doucement et attendre en surface.",
                ],
            },
        ],
        "essentiel": [
            "On ne plonge pas enrhumé, en méforme, ou sans envie.",
            "Bouteille ouverte = l'aiguille du manomètre ne bouge pas quand on respire.",
            "Perte de palanquée : on cherche ~1 min, puis on remonte doucement.",
        ],
        "questions": [
            {
                "q": "En cas de perte de la palanquée, que faire ?",
                "options": [
                    "Continuer la plongée seul",
                    "Chercher ~1 min (tours d'horizon) puis remonter doucement",
                    "Remonter immédiatement à vitesse rapide",
                    "Redescendre plus profond",
                ],
                "correct": 1,
                "explication": "On fait 1 à 2 tours d'horizon (~1 min), puis on remonte à une vitesse < petites bulles et on attend en surface.",
            },
            {
                "q": "Comment vérifier que la bouteille est bien ouverte ?",
                "options": [
                    "L'aiguille du manomètre chute quand on respire",
                    "L'aiguille du manomètre ne bouge pas quand on respire",
                    "On entend un sifflement",
                    "Le gilet se gonfle seul",
                ],
                "correct": 1,
                "explication": "Bouteille ouverte : en respirant sur le détendeur, l'aiguille du manomètre ne doit pas bouger.",
            },
            {
                "q": "Dans quel cas faut-il renoncer à plonger ?",
                "options": [
                    "S'il fait beau",
                    "En cas de rhume ou de sinusite",
                    "Si l'eau est à 20 °C",
                    "Si la palanquée est complète",
                ],
                "correct": 1,
                "explication": "On ne plonge pas enrhumé ni en sinusite (risque de barotraumatisme), ni en méforme, ni sans envie.",
            },
        ],
    },
    # ------------------------------------------------------------------ 15
    {
        "num": 15,
        "slug": "materiel",
        "title": "Le matériel",
        "icon": "🤿",
        "accroche": "Bouteilles, détendeurs, gilet, instruments : connaître et entretenir son équipement.",
        "images": [
            {"src": "detendeur.png", "alt": "Schéma d'un détendeur",
             "caption": "Le détendeur : 1er étage (HP→MP) et 2e étage (pression ambiante, à la demande)."},
            {"src": "gilet.png", "alt": "Gilet stabilisateur",
             "caption": "Le gilet stabilisateur (bouée de sécurité et de confort)."},
            {"src": "ordinateur.png", "alt": "Ordinateur de plongée",
             "caption": "L'ordinateur de plongée : calcul des paliers en temps réel."},
            {"src": "parachute.png", "alt": "Parachute de palier",
             "caption": "Le parachute de palier : repérage en surface."},
            {"src": "boussole.png", "alt": "Boussole de plongée",
             "caption": "La boussole : orientation sous l'eau."},
        ],
        "resume": [
            {
                "titre": "Les bouteilles",
                "points": [
                    "Contenances standards : 6, 9, 12, 15, 18 L ; pressions 200 ou 230 bar.",
                    "Acier (surtout en France) ou aluminium → le <strong>lestage doit être adapté</strong>.",
                ],
            },
            {
                "titre": "Les détendeurs",
                "points": [
                    "Rôle : fournir de l'air à la <strong>pression ambiante</strong>, sans effort, et <strong>à la demande</strong>.",
                    "<strong>1er étage</strong> (sur la bouteille) : détend la HP en moyenne pression (≈ 10 bar + Pabs).",
                    "<strong>2e étage</strong> : donne l'air à la demande, à la pression ambiante. Bouton de surpression pour purger.",
                    "Entretien : rincer à l'eau douce, sécher, ranger à l'abri ; révision quand nécessaire.",
                ],
            },
            {
                "titre": "Le gilet stabilisateur",
                "points": [
                    "Au minimum 2 mécanismes de gonflage (insufflateur + direct-system) et 3 purges (2 rapides + 1 lente).",
                    "<strong>La bouée n'est pas un moyen de compenser un sur-lestage.</strong>",
                ],
            },
            {
                "titre": "Instruments",
                "points": [
                    "<strong>Timer</strong> : temps, profondeur, vitesse (alarmes), mémoires ; à accompagner de tables.",
                    "<strong>Ordinateur</strong> : calcul en temps réel des paliers ; vitesse de remontée souvent plus lente (8 à 12 m/min).",
                    "Parachute de palier (repérage en surface), boussole (orientation).",
                ],
            },
        ],
        "essentiel": [
            "Détendeur : air à la pression ambiante, sans effort, à la demande.",
            "Le 1er étage détend la haute pression vers la moyenne pression.",
            "La bouée ne sert pas à compenser un sur-lestage.",
        ],
        "questions": [
            {
                "q": "Quel est le rôle d'un détendeur ?",
                "options": [
                    "Stocker l'air sous haute pression",
                    "Fournir de l'air à la pression ambiante, sans effort et à la demande",
                    "Mesurer la profondeur",
                    "Gonfler le gilet automatiquement",
                ],
                "correct": 1,
                "explication": "Le détendeur fournit de l'air à la pression ambiante, sans effort, uniquement à la demande.",
            },
            {
                "q": "La bouée (gilet stabilisateur) peut-elle compenser un sur-lestage ?",
                "options": [
                    "Oui, c'est son rôle principal",
                    "Non, elle ne doit pas servir à cela",
                    "Oui, jusqu'à 5 kg",
                    "Seulement en surface",
                ],
                "correct": 1,
                "explication": "La bouée n'est pas un moyen de compenser un sur-lestage : il faut être correctement lesté.",
            },
            {
                "q": "Le premier étage du détendeur détend la haute pression vers :",
                "options": [
                    "La pression ambiante directement",
                    "La moyenne pression (≈ 10 bar + Pabs)",
                    "La basse pression atmosphérique",
                    "La pression de la réserve",
                ],
                "correct": 1,
                "explication": "Le 1er étage détend la HP en moyenne pression (≈ 10 bar + Pabs) ; le 2e étage donne l'air à la demande.",
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Astuces / conseils pour réussir l'examen
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Les conseils de Pascal le Mérou (mascotte) — affichés derrière une ampoule
# 💡 dans chaque fiche de cours. Clé = numéro de chapitre.
# ---------------------------------------------------------------------------

PASCAL = {
    "nom": "Pascal le Mérou",
    "avatar_img": "pascal.png",   # image dans static/img/ (repli sur l'emoji si absente)
    "avatar_emoji": "🐟",
    "intro": "Salut, moi c'est Pascal le Mérou ! Voici mes points clés et mes pièges à "
             "éviter pour ce chapitre : tout l'essentiel à retenir, en un seul endroit. "
             "Clique sur mes ampoules 💡.",
}

# Conseils de Pascal : chaque entrée FUSIONNE l'essentiel à retenir et l'astuce
# (mémo, piège d'examen, application) — un seul point par idée, sans répétition.
HINTS = {
    1: [
        {"titre": "La formule magique de la pression",
         "texte": "Retiens <strong>Pabs = 1 + profondeur/10</strong> : avec ça tu réponds à "
                  "presque toutes les questions de pression. Ex : 20 m → 3 bar, 40 m → 5 bar."},
        {"titre": "Absolue vs hydrostatique (le piège)",
         "texte": "La pression <em>hydrostatique</em> (l'eau) augmente de 1 bar tous les 10 m. "
                  "La pression <em>absolue</em>, c'est toujours <strong>1 de plus</strong> (on "
                  "ajoute l'atmosphère). Beaucoup les confondent : pas toi !"},
    ],
    2: [
        {"titre": "Le poids apparent en un calcul",
         "texte": "<strong>1 litre = 1 kg de poussée.</strong> Poids apparent = poids réel − "
                  "volume (en litres). Négatif → ça remonte ; positif → ça coule ; nul → équilibre."},
        {"titre": "Le piège du bloc qui se vide",
         "texte": "La poussée d'Archimède est <strong>constante</strong> (indépendante de la "
                  "profondeur). Mais en fin de plongée, ton bloc allégé te rend plus léger → "
                  "flottabilité plus positive. Reste vigilant à la remontée."},
    ],
    3: [
        {"titre": "P × V = constante",
         "texte": "Si tu doutes, écris <strong>P1×V1 = P2×V2</strong> et remplace : infaillible. "
                  "Quand la pression augmente, le volume diminue."},
        {"titre": "Le danger est près de la surface",
         "texte": "Entre 10 m et 0 m, le volume <strong>double</strong> : c'est là que les "
                  "barotraumatismes guettent. Purge ta bouée doucement et n'oublie jamais d'expirer "
                  "à la remontée."},
    ],
    4: [
        {"titre": "La méthode d'autonomie sans erreur",
         "texte": "Dans l'ordre : (1) air <strong>consommable</strong> = (pression − réserve) × "
                  "volume, (2) conso à la profondeur = conso surface × Pabs, (3) temps = "
                  "consommable ÷ conso. La réserve (50 bar) se retire toujours."},
        {"titre": "×4 à 30 m",
         "texte": "À 30 m tu respires <strong>4 fois plus vite</strong> qu'en surface (Pabs = 4). "
                  "Multiplie toujours ta consommation par la pression absolue."},
    ],
    5: [
        {"titre": "Descente ou remontée ?",
         "texte": "Le seul accident qui n'arrive QU'à la descente, c'est le <strong>plaquage de "
                  "masque</strong> (souffle par le nez). Dents, estomac et surpression pulmonaire : "
                  "seulement à la remontée."},
        {"titre": "Jamais de Valsalva à la remontée",
         "texte": "Équilibre tes oreilles <strong>à la descente</strong>, sans forcer. À la "
                  "remontée, surtout pas de Valsalva : si une réponse le propose, c'est faux."},
        {"titre": "Surpression pulmonaire : la n°1 à éviter",
         "texte": "Le plus grave… mais le plus facile à éviter : <strong>expire normalement</strong> "
                  "à la remontée, ne bloque jamais ta respiration."},
    ],
    6: [
        {"titre": "L'azote : il entre, il sort",
         "texte": "Descente = l'azote se dissout (P&gt;T) ; remontée = il s'élimine (P&lt;T). Le gaz "
                  "qui pose problème, c'est l'<strong>azote</strong>."},
        {"titre": "Reste calme",
         "texte": "Plus tu t'agites, plus tu dissous d'azote. Une plongée tranquille = moins de "
                  "risque d'accident de décompression."},
    ],
    7: [
        {"titre": "Le traitement comme une comptine",
         "texte": "<strong>O2 à 100 %, aspirine 0,5 g, faire boire, caisson</strong> — et on alerte "
                  "les secours. On ne re-plonge jamais pour « recomprimer »."},
        {"titre": "Ça peut venir tard",
         "texte": "La plupart des ADD se déclarent dans l'heure, mais c'est possible jusqu'à "
                  "<strong>12 h après</strong>. Pas d'avion avant 12 à 24 h, pas d'effort ni "
                  "d'apnée après la plongée."},
    ],
    8: [
        {"titre": "Pression partielle = Ptotale × %",
         "texte": "Air = <strong>20 % O2, 80 % N2</strong>. Ppa = pression absolue × pourcentage. "
                  "Ex : à 40 m (5 bar), PpN2 = 5 × 0,8 = 4 bar."},
    ],
    9: [
        {"titre": "Essoufflement vs narcose (à ne jamais confondre)",
         "texte": "Essoufflement = trop de <strong>CO2</strong> → on EXPIRE et on s'arrête (à 40 m "
                  "on remonte). Narcose = trop d'<strong>azote</strong> → on REMONTE et tout "
                  "disparaît."},
    ],
    10: [
        {"titre": "Le réflexe qui sauve",
         "texte": "On remonte la victime en gardant le <strong>détendeur en bouche</strong>, on "
                  "alerte les secours, on réchauffe et on rassure. La syncope des 7 m vient de "
                  "l'hyperventilation en apnée."},
    ],
    11: [
        {"titre": "La méthode des tables",
         "texte": "Lis deux fois l'énoncé, fais un <strong>schéma clair</strong>, et si une valeur "
                  "manque, prends toujours la valeur <strong>immédiatement supérieure</strong> "
                  "(jamais d'interpolation). La profondeur retenue = la plus profonde atteinte."},
        {"titre": "Les vitesses à connaître par cœur",
         "texte": "<strong>15 m/min</strong> jusqu'au 1er palier, <strong>6 m/min</strong> entre les "
                  "paliers (plus lent). Paliers de 3 en 3 m ; palier de sécurité conseillé : "
                  "3 min à 3 m."},
    ],
    12: [
        {"titre": "Le piège préféré des examinateurs",
         "texte": "La <strong>majoration ne compte PAS</strong> pour l'heure de sortie, seulement "
                  "pour calculer les paliers. Tableau 1 → azote résiduel ; tableau 2 → majoration."},
        {"titre": "Consécutive ou successive ?",
         "texte": "IS &lt; 15 min = <strong>consécutive</strong> (une seule plongée : durées "
                  "additionnées, profondeur max). 15 min à 12 h = <strong>successive</strong> "
                  "(majoration). Intervalle absent du tableau 1 → valeur <strong>inférieure</strong> "
                  "(sécurité)."},
    ],
    13: [
        {"titre": "Les chiffres à retenir",
         "texte": "<strong>16 ans</strong>, licence <strong>15 mois</strong>, certificat médical "
                  "<strong>1 an</strong>, sinistre déclaré sous <strong>5 jours</strong>, bloc "
                  "ré-éprouvé si P×V &gt; 80 L."},
        {"titre": "Tes prérogatives",
         "texte": "Autonomie <strong>20 m</strong> entre N2, encadré jusqu'à <strong>40 m</strong>. "
                  "Mais attention : l'autonomie n'est pas l'encadrement — un N2 n'encadre personne."},
    ],
    14: [
        {"titre": "Tu es seul juge",
         "texte": "Enrhumé, fatigué ou pas envie → <strong>on ne plonge pas</strong>. Personne ne "
                  "décide à ta place."},
        {"titre": "Les bons réflexes",
         "texte": "Vérifie que ta bouteille est ouverte : l'aiguille du manomètre ne bouge pas "
                  "quand tu respires. Perte de palanquée : ~1 min de recherche, puis remontée lente."},
    ],
    15: [
        {"titre": "Le détendeur en 2 étages",
         "texte": "1er étage = HP → <strong>moyenne pression</strong> ; 2e étage = air <strong>à la "
                  "demande</strong>, à la pression ambiante. Rince-le à l'eau douce après chaque "
                  "plongée."},
        {"titre": "La bouée n'est pas du lestage",
         "texte": "Le gilet sert à s'équilibrer, <strong>jamais</strong> à compenser un sur-lestage. "
                  "Et l'ordinateur impose souvent une remontée plus lente (8–12 m/min) que les tables."},
    ],
}


# Ancien contenu « Astuces » — conservé pour mémoire mais remplacé par les
# conseils de Pascal le Mérou intégrés aux fiches (voir HINTS ci-dessus).
ASTUCES = [
    {
        "titre": "Méthode générale pour les QCM",
        "icon": "🎯",
        "conseils": [
            "Lisez <strong>deux fois</strong> chaque énoncé en entier avant de répondre.",
            "Repérez les mots-clés : « toujours », « jamais », « sauf », « uniquement » changent tout le sens.",
            "Éliminez d'abord les réponses manifestement fausses, puis tranchez entre les restantes.",
            "Ne restez jamais bloqué : passez la question (en test blanc) et revenez-y à la fin.",
            "Méfiez-vous des pièges : une réponse « trop évidente » mérite une seconde lecture.",
        ],
    },
    {
        "titre": "Les exercices de tables MN90",
        "icon": "📊",
        "conseils": [
            "Lisez <strong>deux fois</strong> l'énoncé en entier avant de commencer les calculs.",
            "Faites <strong>toujours un schéma clair et spacieux</strong> de la plongée.",
            "Utilisez toujours la même méthode et des codes couleurs (mètres vs minutes).",
            "Contrôlez votre lecture de table <strong>avant</strong> de faire le moindre calcul.",
            "Profondeur = profondeur MAX atteinte ; valeur absente → valeur immédiatement supérieure (jamais d'interpolation).",
            "Vérifiez toujours la <strong>plausibilité</strong> du résultat (un palier de 3 h, c'est suspect !).",
        ],
    },
    {
        "titre": "Pièges classiques à connaître",
        "icon": "⚠️",
        "conseils": [
            "La <strong>majoration ne compte pas</strong> pour l'heure de sortie (seulement pour les paliers).",
            "<strong>Pas de Valsalva à la remontée.</strong>",
            "La poussée d'Archimède est <strong>constante</strong> avec la profondeur.",
            "Les barotraumatismes sont <strong>indépendants</strong> de la durée et de la profondeur.",
            "Plongées consécutives (IS < 15 min) vs successives (15 min ≤ IS < 12 h) : ne pas confondre.",
            "Pour l'IS dans le tableau 1, on prend la valeur <strong>inférieure</strong> (sécurité) ; ailleurs, valeur supérieure.",
        ],
    },
    {
        "titre": "Calculs : les automatismes à avoir",
        "icon": "🧮",
        "conseils": [
            "Pabs = 1 + profondeur/10.",
            "Consommation à la profondeur = consommation surface × Pabs.",
            "Quantité d'air = volume du bloc × pression.",
            "Pression partielle = pression totale × pourcentage du gaz.",
            "Révisez les calculs d'horaires : 10h55 + 35 min = 11h30, etc.",
        ],
    },
    {
        "titre": "Le jour de l'examen",
        "icon": "🧠",
        "conseils": [
            "Gérez votre temps : repérez les questions rapides, gardez les calculs de tables pour la fin si besoin.",
            "Commencez par les questions sur lesquelles vous êtes sûr pour engranger des points et la confiance.",
            "Une question sans malus de mauvaise réponse : ne laissez jamais de blanc, tentez votre meilleure hypothèse.",
            "Relisez-vous : vérifiez les unités (mètres/minutes, bar) et l'ordre de grandeur.",
            "Reposez-vous la veille : la fatigue est l'ennemie de la concentration… comme en plongée.",
        ],
    },
]
