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

## Prérequis

- **Python 3.9 ou supérieur** (vérifier avec `python3 --version`).
- **pip** (installé avec Python).
- Un navigateur web récent.

Aucune base de données ni service externe n'est nécessaire.

## Installation

### 1. Récupérer le projet

```bash
git clone <url-du-depot>
cd diving_test
```

> Si vous avez déjà les fichiers en local, placez-vous simplement dans le
> dossier `diving_test`.

### 2. Créer un environnement virtuel (recommandé)

Cela isole les dépendances du projet du reste de votre système.

**Linux / macOS :**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell) :**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Une fois activé, votre invite de commande affiche `(.venv)` au début.

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Puis ouvrir **http://localhost:5000** dans un navigateur.

Pour **arrêter** l'application : `Ctrl + C` dans le terminal.

Pour **quitter** l'environnement virtuel : `deactivate`.

### Options (variables d'environnement)

| Variable     | Rôle                                   | Défaut |
|--------------|----------------------------------------|--------|
| `PORT`       | Port d'écoute du serveur               | `5000` |
| `SECRET_KEY` | Clé de session Flask (à définir en prod)| valeur de dev |

Exemple pour changer le port :

```bash
# Linux / macOS
PORT=8080 python app.py

# Windows (PowerShell)
$env:PORT=8080; python app.py
```

## Résolution de problèmes

- **`python` introuvable** : essayez `python3` à la place (ou installez Python
  depuis [python.org](https://www.python.org/downloads/)).
- **Le port 5000 est déjà utilisé** : lancez avec un autre port, par ex.
  `PORT=8080 python app.py`.
- **`ModuleNotFoundError: No module named 'flask'`** : l'environnement virtuel
  n'est pas activé ou les dépendances ne sont pas installées — refaites les
  étapes 2 et 3.
- **Sous Windows, l'activation est bloquée** (`Activate.ps1`) : autorisez les
  scripts dans la session avec
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, puis relancez
  la commande d'activation.

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
