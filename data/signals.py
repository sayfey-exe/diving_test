# -*- coding: utf-8 -*-
"""
Mémo des signes de plongée (communication, sécurité, faune).

Les signes de communication et de sécurité sont standardisés (FFESSM / CMAS).
Les signes de faune sont indicatifs : ils varient selon les clubs et les régions.
Faute d'illustrations libres de droits, chaque signe est décrit par un texte
clair et une émoji d'appui — l'idée est de mémoriser le geste, pas de le montrer.
"""

# categorie : "communication" | "securite" | "faune"
SIGNALS = [
    # --- Communication de base (obligatoires à connaître) ---
    {"key": "ok", "nom": "OK / tout va bien", "categorie": "communication", "emoji": "👌",
     "description": "Pouce et index joints en cercle, les autres doigts tendus. "
                    "C'est une question ET une réponse : on répond toujours par OK."},
    {"key": "probleme", "nom": "Ça ne va pas / il y a un problème", "categorie": "communication", "emoji": "🤚",
     "description": "Main à plat, paume vers le bas, basculée d'un côté puis de l'autre. "
                    "On désigne ensuite l'origine du souci (oreille, air…)."},
    {"key": "monter", "nom": "Je monte / on remonte", "categorie": "communication", "emoji": "👍",
     "description": "Pouce tendu vers le haut. Signe de commandement : on remonte."},
    {"key": "descendre", "nom": "Je descends / on descend", "categorie": "communication", "emoji": "👎",
     "description": "Pouce tendu vers le bas."},
    {"key": "stop", "nom": "Stop / on ne bouge plus", "categorie": "communication", "emoji": "✋",
     "description": "Main ouverte, paume tournée vers le binôme."},
    {"key": "niveau", "nom": "On reste à ce niveau", "categorie": "communication", "emoji": "➖",
     "description": "Main à plat, horizontale, stabilisée : on maintient la profondeur."},
    {"key": "venir", "nom": "Viens / suis-moi", "categorie": "communication", "emoji": "🫴",
     "description": "Main qui se replie vers soi, ou on se désigne puis on pointe la direction."},
    {"key": "direction", "nom": "On va par là", "categorie": "communication", "emoji": "👉",
     "description": "Bras et index tendus dans la direction choisie."},

    # --- Sécurité / détresse (à reconnaître immédiatement) ---
    {"key": "panne-air", "nom": "Je n'ai plus d'air / panne d'air", "categorie": "securite", "emoji": "🚨",
     "description": "Main qui tranche la gorge en va-et-vient. Urgence : on donne son "
                    "octopus (détendeur de secours) au binôme."},
    {"key": "reserve", "nom": "Je suis sur réserve", "categorie": "securite", "emoji": "✊",
     "description": "Poing fermé posé sur la poitrine. Il faut envisager la remontée."},
    {"key": "essouffle", "nom": "Je suis essoufflé", "categorie": "securite", "emoji": "😮‍💨",
     "description": "Main ouverte devant la poitrine, qui s'ouvre et se ferme au rythme "
                    "de la respiration. On s'arrête, on se ventile, on remonte doucement."},
    {"key": "froid", "nom": "J'ai froid", "categorie": "securite", "emoji": "🥶",
     "description": "Bras croisés sur la poitrine, mains se frictionnant les épaules."},
    {"key": "oreilles", "nom": "Problème d'oreilles", "categorie": "securite", "emoji": "👂",
     "description": "Main portée près de l'oreille. On arrête la descente, on remonte "
                    "un peu et on rééquilibre."},
    {"key": "vertige", "nom": "Ça tourne / vertige", "categorie": "securite", "emoji": "😵‍💫",
     "description": "Index tournant près de la tempe. Signe de vertige ou de narcose."},
    {"key": "detresse-surface", "nom": "Détresse en surface", "categorie": "securite", "emoji": "🆘",
     "description": "Un bras tendu vers le haut, agité de grands gestes. Appel au secours "
                    "depuis la surface."},
    {"key": "ok-surface", "nom": "OK surface", "categorie": "securite", "emoji": "🙆",
     "description": "Grand cercle formé au-dessus de la tête avec les bras (ou une main "
                    "posée sur la tête) : tout va bien, vu de loin."},

    # --- Faune (indicatifs, varient selon les clubs) ---
    {"key": "requin", "nom": "Requin", "categorie": "faune", "emoji": "🦈",
     "description": "Main posée verticalement sur le sommet du crâne, imitant l'aileron."},
    {"key": "raie", "nom": "Raie / mante", "categorie": "faune", "emoji": "🐟",
     "description": "Bras écartés ondulant lentement comme des ailes."},
    {"key": "tortue", "nom": "Tortue", "categorie": "faune", "emoji": "🐢",
     "description": "Une main posée sur le dos de l'autre (la carapace), les pouces "
                    "battant comme des nageoires."},
    {"key": "poulpe", "nom": "Poulpe / pieuvre", "categorie": "faune", "emoji": "🐙",
     "description": "Doigts pendants qui ondulent, imitant les tentacules."},
    {"key": "merou", "nom": "Mérou", "categorie": "faune", "emoji": "🐟",
     "description": "Main ouverte devant la bouche imitant les grosses lèvres du mérou "
                    "(signe indicatif, souvent propre au club)."},
    {"key": "murene", "nom": "Murène", "categorie": "faune", "emoji": "🐍",
     "description": "Main dont les doigts s'ouvrent et se ferment, imitant la gueule "
                    "qui s'ouvre et se referme."},
    {"key": "meduse", "nom": "Méduse (attention)", "categorie": "faune", "emoji": "🎐",
     "description": "Main en cloche, doigts pendants, avec un signe de prudence : "
                    "ne pas toucher, ça urtique."},
    {"key": "langouste", "nom": "Langouste", "categorie": "faune", "emoji": "🦞",
     "description": "Deux doigts pointés depuis le front, imitant les longues antennes."},
]

SIGNAL_BY_KEY = {s["key"]: s for s in SIGNALS}
