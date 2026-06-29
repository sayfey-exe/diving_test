# 🤿 Plongée N2 — Application de révision

Application web (Flask) pour aider les élèves à réviser et à s'entraîner au
**brevet Plongeur Autonome Niveau II (FFESSM)**, d'après le cours théorique
MPS 2011 (tables MN90).

## Fonctionnalités

- **📚 Fiches de cours** — les 15 chapitres du programme résumés, avec
  *l'essentiel à retenir* et **3 questions d'auto-évaluation** (correction
  immédiate) à la fin de chaque fiche.
- **📝 Test blanc** — 40 QCM **tirés au sort sans doublon** dans une banque de
  **plus de 400 questions**, navigation libre (on peut passer une question et y
  revenir), puis **correction détaillée** avec explication et renvoi au chapitre.
  Sous chaque question corrigée, une **zone de commentaire** permet de signaler
  une remarque ; ces retours sont enregistrés et consultables côté admin pour
  améliorer la banque.
- **⏱️ Test examen** — 40 QCM **chronométrés** (40 min), sans correction
  pendant l'épreuve ; score et bilan par chapitre à la fin.
- **🐟 Conseils de Pascal le Mérou** — la mascotte distille ses astuces (méthode,
  pièges classiques, calculs) cachées derrière des **icônes ampoule 💡** dans
  les fiches de cours.
- **🖼️ Images du cours** — les schémas du document (anatomie, détendeur,
  profils de plongée, table MN90…) sont intégrés aux fiches concernées.
- **✏️ Exercices corrigés** — les exercices du cours (autonomie, tables MN90…)
  avec leur correction (méthode détaillée + valeurs calculables).
- **👤 Comptes & statistiques** — création de compte et connexion, **suivi des
  chapitres étudiés** et **historique des résultats** (tests blancs et examens),
  avec note moyenne, meilleure note et **graphique d'évolution des scores**.
- **🏆 Classement** — comparaison à la **moyenne de la communauté** et classement
  des joueurs par note moyenne (esprit de compétition).
- **🛡️ Mode administrateur** — vue de tous les comptes et de leurs scores
  (réservé aux e-mails déclarés administrateurs).

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

## Comptes et base de données

Les comptes et les statistiques sont stockés dans une base de données configurée
via la variable d'environnement `DATABASE_URL` :

- **En local** : si `DATABASE_URL` n'est pas définie, l'application crée
  automatiquement un fichier **SQLite** (`diving.db`). Rien à installer.
- **En production** : définis `DATABASE_URL` vers une base **PostgreSQL**
  (recommandé). Les tables sont créées automatiquement au démarrage.

> ⚠️ **Persistance sur l'hébergement gratuit** : sur Render (offre gratuite), le
> disque est *éphémère* — une base SQLite serait effacée à chaque
> redéploiement. Pour conserver les comptes, **utilise une base PostgreSQL**
> (voir ci-dessous, le `render.yaml` en crée une automatiquement).

### Mode administrateur

Le mode admin (vue de tous les comptes et de leurs scores, page `/admin`) est
réservé aux comptes dont l'e-mail est listé dans la variable d'environnement
**`ADMIN_EMAILS`** (e-mails séparés par des virgules) :

```bash
# Linux / macOS — lancement local en admin
ADMIN_EMAILS="ton.email@exemple.fr" python app.py
```

Sur Render : onglet **Environment** du service web → ajoute la variable
`ADMIN_EMAILS` avec ton (tes) e-mail(s). Le lien **🛡️ Admin** apparaît alors
dans la barre de navigation pour ces comptes. Aucune migration de base n'est
nécessaire (le statut admin est déterminé par l'e-mail, pas stocké en base).

### Réinitialisation de mot de passe (envoi d'e-mail)

La page **« Mot de passe oublié ? »** envoie un **lien de réinitialisation**
(valable 1 h) à l'adresse du compte. Les mots de passe étant *hachés*, ils ne
sont jamais renvoyés en clair : on choisit un nouveau mot de passe via le lien.

L'envoi d'e-mail se configure avec des variables d'environnement SMTP :

| Variable        | Exemple                    | Rôle                              |
|-----------------|----------------------------|-----------------------------------|
| `MAIL_SERVER`   | `smtp.gmail.com`           | serveur SMTP                      |
| `MAIL_PORT`     | `587`                      | port (587 = TLS, 465 = SSL)       |
| `MAIL_USERNAME` | `ton.email@gmail.com`      | identifiant SMTP                  |
| `MAIL_PASSWORD` | *(mot de passe d'application)* | mot de passe SMTP             |
| `MAIL_SENDER`   | `Plongée N2 <…@gmail.com>` | expéditeur affiché (optionnel)    |
| `MAIL_USE_SSL`  | `false`                    | `true` pour le port 465           |

> Avec Gmail, crée un **« mot de passe d'application »** (compte Google →
> Sécurité → validation en 2 étapes) plutôt que ton mot de passe principal.
> Sans ces variables, l'e-mail n'est pas envoyé ; en local (mode debug), le
> lien de réinitialisation s'affiche directement à l'écran pour tester.

> ℹ️ **Rappel important** : si « l'application ne se souvient plus des comptes »,
> c'est presque toujours que la base **SQLite éphémère** est utilisée en
> production (voir l'avertissement au démarrage dans les logs). Branche une base
> **PostgreSQL** via `DATABASE_URL` pour que les comptes persistent.

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
     build, démarrage, clé `SECRET_KEY` générée **et une base PostgreSQL
     gratuite** reliée via `DATABASE_URL` pour les comptes).
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
├── app.py                 # application Flask (routes, auth, suivi)
├── models.py              # modèles SQLAlchemy (User, TestResult, ChapterStudy)
├── requirements.txt       # dépendances (Flask, SQLAlchemy, Login, gunicorn…)
├── Procfile               # commande de démarrage en production (gunicorn)
├── render.yaml            # déploiement Render (web + base PostgreSQL)
├── data/
│   ├── content.py         # les 15 fiches de cours + astuces + images
│   ├── questions.py       # banque de questions des tests
│   └── exercices.py       # exercices corrigés par chapitre
├── templates/             # gabarits HTML (Jinja2)
└── static/
    ├── style.css
    ├── *.js
    └── img/               # schémas extraits du cours
```

## Crédits & sources

Contenu pédagogique d'après le **cours théorique Plongeur Niveau II (MPS, 2011)**
de la FFESSM. Les schémas intégrés aux fiches proviennent de ce document et
conservent leurs attributions d'origine (notamment *Alain Foret — Illustra-Pack*,
*infovisual.info*, et la **table MN90 — FFESSM**). Application destinée à un
usage **pédagogique et personnel** de révision.

## Avertissement

Outil **pédagogique d'entraînement**. En cas de doute, référez-vous toujours au
cours officiel, à vos moniteurs et aux tables MN90 de la FFESSM.
