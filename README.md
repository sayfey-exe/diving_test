# 🤿 Palanquée — La plongée pour tous

Application web (Flask) ouverte à **tous les plongeurs, quel que soit leur
niveau** : réviser la théorie, s'entraîner avec des quiz, et explorer une carte
communautaire de spots. Le contenu théorique suit le programme **FFESSM**
(cours MPS 2011, tables MN90) — idéal pour préparer un brevet comme pour
entretenir ses connaissances.

L'onglet **« Réviser & se tester »** regroupe en un seul endroit les fiches de
théorie et les quiz (entraînement corrigé ou mode examen chronométré).

## Fonctionnalités

L'onglet **« 🎓 Réviser »** regroupe la théorie et les quiz. Les autres onglets
(**Spots**, **Vie sous-marine**, **Signes**, **Carnet**) sont des outils utiles
à **tous les plongeurs**, quel que soit leur niveau.

- **📚 Fiches de théorie** — les 15 chapitres du programme résumés, avec
  *l'essentiel à retenir* et **3 questions d'auto-évaluation** (correction
  immédiate) à la fin de chaque fiche.
- **📝 Quiz d'entraînement** — 40 QCM **tirés au sort sans doublon** dans une banque de
  **plus de 400 questions** d'un **niveau un peu plus exigeant que l'examen**
  (calculs multi-étapes, pièges classiques, mises en situation, distracteurs
  subtils), avec un **tirage équilibré par thème** (chaque test couvre les 15
  chapitres) et **au moins 1/4 de questions à choix multiples**. Navigation
  libre, puis **correction détaillée** avec explication et renvoi au chapitre.
  Sous chaque question corrigée, une **zone de commentaire** permet de signaler
  une remarque ; ces retours sont enregistrés et consultables côté admin pour
  améliorer la banque.
- **⏱️ Mode examen** — 40 QCM **chronométrés** (40 min), sans correction
  pendant l'épreuve ; score et bilan par thème à la fin.
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
- **🗺️ Spots de plongée** — une **carte interactive** (Leaflet + OpenStreetMap)
  des spots ; chaque spot liste les **poissons observables**, une **banque de
  photos communautaire** (upload redimensionné, stocké en base) et des
  **commentaires**. Les utilisateurs connectés peuvent **ajouter un spot en
  cliquant sur la carte**, et chaque photo taguée par espèce **enrichit le
  guide de la vie sous-marine**. Les **administrateurs** peuvent
  supprimer photos, commentaires et spots proposés par la communauté.
- **🐟 Guide de la vie sous-marine** (`/vie-sous-marine`) — un **catalogue
  d'espèces** (regroupé par catégorie : poissons, invertébrés, mollusques,
  végétaux…), avec fiche détaillée (habitat, taille, nom scientifique), le
  **signe de plongée** associé quand il existe, et la galerie des photos de la
  communauté. Le catalogue **s'enrichit tout seul** : chaque photo peut être
  taguée à une espèce, un plongeur peut **proposer une nouvelle espèce**, et une
  **reconnaissance automatique** (optionnelle, voir plus bas) peut identifier
  l'espèce sur la photo. Toute **nouvelle espèce** reste *en attente de
  validation* par un administrateur avant d'apparaître publiquement.
- **🤿 Mémo des signes de plongée** (`/signes`) — aide-mémoire des signes de
  **communication**, de **sécurité/détresse** et de **faune** (indicatifs).
- **📖 Carnet de plongée** (`/carnet`) — journal personnel des plongées (date,
  site — relié à la carte des spots —, profondeur, durée, température, binôme,
  lestage, gaz, ressenti, notes) avec **statistiques** (nombre de plongées,
  temps cumulé, profondeur max, sites visités).
- **🏆 Classement** — comparaison à la **moyenne de la communauté** et classement
  des joueurs par note moyenne (esprit de compétition).
- **🛡️ Mode administrateur** — vue de tous les comptes et de leurs scores, et
  **modération** (remarques, photos, spots, commentaires, **validation des
  espèces** proposées et attribution des signes de plongée).

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

#### Reconnaissance automatique des espèces (optionnelle)

La reconnaissance des espèces sur les photos est **désactivée par défaut** :
sans configuration, l'utilisateur choisit ou propose l'espèce à la main, et
un administrateur valide les nouvelles propositions.

Pour l'activer, on branche l'API vision de Claude via ces variables :

| Variable                | Rôle                                              | Défaut |
|-------------------------|---------------------------------------------------|--------|
| `ANTHROPIC_API_KEY`     | Clé API (active la reconnaissance)                | *(vide)* |
| `VISION_ENABLED`        | `0` pour désactiver même si une clé est présente  | `1` |
| `VISION_MODEL`          | Modèle vision utilisé                             | `claude-3-5-sonnet-latest` |
| `VISION_MIN_CONFIDENCE` | Seuil de confiance (0–1) pour accepter une propal | `0.55` |

Le résultat n'est **jamais** publié sans contrôle : une espèce reconnue mais
absente du catalogue est créée *en attente de validation* (l'admin la valide
depuis **🛡️ Admin → Espèces**), et l'utilisateur peut toujours corriger. Sans
clé, `recognition.identify()` renvoie simplement `None`.

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

### E-mails : confirmation d'adresse & mot de passe oublié

Deux e-mails sont envoyés par l'application :

- **Confirmation d'adresse** — à la création d'un compte (et si l'on change
  d'e-mail). Un bandeau invite à confirmer tant que ce n'est pas fait ; le lien
  est valable 7 jours et peut être **renvoyé depuis le profil**.
- **Mot de passe oublié** — un **lien de réinitialisation** (valable 1 h). Les
  mots de passe étant *hachés*, ils ne sont jamais renvoyés en clair.

L'envoi se configure avec des variables d'environnement SMTP :

| Variable        | Exemple                       | Rôle                                    |
|-----------------|-------------------------------|-----------------------------------------|
| `MAIL_SERVER`   | `smtp.gmail.com`              | serveur SMTP                            |
| `MAIL_PORT`     | `587`                         | port (587 = TLS/STARTTLS, 465 = SSL)    |
| `MAIL_USERNAME` | `ton.email@gmail.com`         | identifiant SMTP                        |
| `MAIL_PASSWORD` | *(mot de passe d'application)*| mot de passe SMTP                       |
| `MAIL_SENDER`   | `Palanquée <…@gmail.com>`     | expéditeur affiché (optionnel)          |
| `MAIL_USE_SSL`  | `false`                       | `true` pour le port 465 (auto si port=465) |

#### ⚠️ « Je ne reçois aucun e-mail » — checklist

C'est presque toujours un **problème de configuration SMTP**, pas de code :

1. **Les variables `MAIL_*` sont-elles définies ?** Sans elles, *rien n'est
   envoyé* (l'app le journalise : `E-mail non configuré…`). Sur Render :
   onglet **Environment** du service → ajoute les 3 variables au minimum
   (`MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`), puis **redeploy**.
2. **Gmail** : le mot de passe classique **ne marche pas**. Il faut :
   active la **validation en 2 étapes** sur ton compte Google, puis crée un
   **« mot de passe d'application »** (Google → Sécurité → Mots de passe des
   applications) et mets *ce* code de 16 caractères dans `MAIL_PASSWORD`.
   Utilise `MAIL_SERVER=smtp.gmail.com` et `MAIL_PORT=587`.
3. **Teste l'envoi** : connecte-toi en admin → page **🛡️ Admin** → section
   **« 📧 Envoi d'e-mails »** → *Envoyer un e-mail de test*. Le résultat (succès
   ou **message d'erreur SMTP exact**) s'affiche immédiatement.
4. **Regarde les spams** et vérifie que `MAIL_SENDER` correspond bien au compte
   `MAIL_USERNAME` (certains fournisseurs rejettent un expéditeur différent).
5. En **local (mode debug)** sans SMTP, les liens de confirmation / de
   réinitialisation s'affichent directement à l'écran pour pouvoir tester.

> 💡 Alternative simple si Gmail pose problème : un service d'e-mail
> transactionnel gratuit (Brevo/Sendinblue, Mailjet, Resend…) fournit un hôte
> SMTP et des identifiants dédiés à mettre dans ces mêmes variables.

### Connexion Google / Facebook (optionnelle)

Des boutons **« Continuer avec Google / Facebook »** apparaissent sur les pages
de connexion et d'inscription **dès que les identifiants OAuth sont fournis**
(sinon ils sont masqués). Un compte créé par ce biais a son adresse
**automatiquement confirmée**.

| Variable                 | Où l'obtenir                                             |
|--------------------------|---------------------------------------------------------|
| `GOOGLE_CLIENT_ID`       | [Google Cloud Console](https://console.cloud.google.com/) → *APIs & Services* → *Credentials* → *OAuth client ID* (type « Web ») |
| `GOOGLE_CLIENT_SECRET`   | idem                                                    |
| `FACEBOOK_CLIENT_ID`     | [Facebook for Developers](https://developers.facebook.com/) → une app → *Facebook Login* |
| `FACEBOOK_CLIENT_SECRET` | idem                                                    |

**URL de redirection (callback)** à déclarer chez le fournisseur — exactement :

```
https://TON-DOMAINE/connexion/google/callback
https://TON-DOMAINE/connexion/facebook/callback
```

(en local : `http://localhost:5000/connexion/google/callback`). Pense à activer
le partage de l'**e-mail** dans les autorisations de l'app OAuth, sinon la
connexion échoue faute d'adresse.

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
