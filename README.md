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

## Déploiement en ligne (gratuit)

L'application est prête pour la production : elle se lance avec le serveur
**gunicorn** via le point d'entrée `app:app` (voir le `Procfile`).

### Option A — Render (recommandé, déploiement depuis GitHub)

[Render](https://render.com) propose un hébergement gratuit pour les services
web et redéploie automatiquement à chaque `git push`.

1. Pousser le projet sur un dépôt **GitHub** (public ou privé).
2. Créer un compte sur [render.com](https://render.com) et le connecter à GitHub.
3. Cliquer sur **New → Web Service**, sélectionner le dépôt et **la branche**
   à déployer, puis renseigner :
   - **Build Command** = `pip install -r requirements.txt`
   - **Start Command** = `gunicorn app:app --bind 0.0.0.0:$PORT`
   - (le fichier `render.yaml` fourni permet aussi un déploiement
     **New → Blueprint** en un clic, qui configure tout automatiquement —
     build, démarrage, clé `SECRET_KEY` générée).
4. Valider : l'app est en ligne sous une URL en `…onrender.com`.

> ⚠️ **Important** : la commande de démarrage doit écouter sur le port fourni
> par l'hébergeur via `$PORT` (`--bind 0.0.0.0:$PORT`). Sans cela, Render
> n'ouvre aucun port et le déploiement échoue.

> ⓘ Sur l'offre gratuite, le service se met en veille après ~15 min d'inactivité ;
> la première visite suivante prend quelques dizaines de secondes à « réveiller ».

### Option B — PythonAnywhere (sans carte bancaire)

[PythonAnywhere](https://www.pythonanywhere.com) a une offre gratuite adaptée à
Flask, sans carte bancaire.

1. Créer un compte gratuit (« Beginner »).
2. Onglet **Files** : uploader le projet (ou le cloner via une console Bash :
   `git clone <url-du-depot>`).
3. Onglet **Web → Add a new web app → Manual configuration → Python 3.x**.
4. Dans **Virtualenv**, créer/installer les dépendances :
   `pip install -r requirements.txt`.
5. Éditer le fichier **WSGI** proposé pour qu'il importe l'app :

   ```python
   import sys
   path = "/home/<votre_user>/diving_test"
   if path not in sys.path:
       sys.path.insert(0, path)
   from app import app as application   # PythonAnywhere attend « application »
   ```

6. Cliquer sur **Reload**. L'app est en ligne sous `…pythonanywhere.com`.

### Autres plateformes compatibles

Le `Procfile` (`web: gunicorn app:app`) rend l'app déployable telle quelle sur
**Railway**, **Koyeb**, **Fly.io**, etc. Pensez à définir la variable
d'environnement `SECRET_KEY` sur ces plateformes.

## Structure du projet

```
diving_test/
├── app.py                 # application Flask (routes)
├── requirements.txt       # dépendances (Flask, gunicorn)
├── Procfile               # commande de démarrage en production (gunicorn)
├── render.yaml            # configuration de déploiement Render
├── data/
│   ├── content.py         # les 15 fiches de cours + astuces
│   └── questions.py       # banque de questions des tests
├── templates/             # gabarits HTML (Jinja2)
└── static/                # CSS + JavaScript
```

## Avertissement

Outil **pédagogique d'entraînement**. En cas de doute, référez-vous toujours au
cours officiel, à vos moniteurs et aux tables MN90 de la FFESSM.
