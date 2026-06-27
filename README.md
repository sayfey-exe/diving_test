# 🤿 Plongée N2 — Application de révision

Application web (Flask) pour aider les élèves à réviser et à s'entraîner au
**brevet Plongeur Autonome Niveau II (FFESSM)**, d'après le cours théorique
MPS 2011 (tables MN90).

## Fonctionnalités

- **📚 Fiches de cours** — les 15 chapitres du programme résumés, avec
  *l'essentiel à retenir* et **3 questions d'auto-évaluation** (correction
  immédiate) à la fin de chaque fiche.
- **📝 Test blanc** — 40 QCM tirés au sort, navigation libre (on peut passer
  une question et y revenir), puis **correction détaillée** avec explication et
  renvoi au chapitre concerné.
- **⏱️ Test examen** — 40 QCM **chronométrés** (40 min), sans correction
  pendant l'épreuve ; score et bilan par chapitre à la fin.
- **💡 Astuces & méthode** — pièges classiques, méthode pour les QCM et les
  exercices de tables, bons réflexes le jour de l'examen.

## Programme couvert

Pression · Archimède · Boyle-Mariotte · Calcul d'autonomie · Barotraumatismes ·
Henry · Accidents de décompression · Dalton · Toxicité des gaz · Noyade ·
Tables MN90 (2 parties) · Réglementation · Comportement & sécurité · Matériel.

## Installation et lancement

```bash
# 1. (recommandé) créer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 2. installer les dépendances
pip install -r requirements.txt

# 3. lancer l'application
python app.py
```

Puis ouvrir **http://localhost:5000** dans un navigateur.

> Variable d'environnement optionnelle : `PORT` (port d'écoute, défaut 5000) et
> `SECRET_KEY` (clé de session Flask).

## Structure du projet

```
diving_test/
├── app.py                 # application Flask (routes)
├── requirements.txt
├── data/
│   ├── content.py         # les 15 fiches de cours + astuces
│   └── questions.py       # banque de questions des tests
├── templates/             # gabarits HTML (Jinja2)
└── static/                # CSS + JavaScript
```

## Avertissement

Outil **pédagogique d'entraînement**. En cas de doute, référez-vous toujours au
cours officiel, à vos moniteurs et aux tables MN90 de la FFESSM.
