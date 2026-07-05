# -*- coding: utf-8 -*-
"""
Palanquée — La plongée pour tous (théorie, entraînement et communauté).

Application web Flask ouverte à tous les plongeurs, quel que soit leur niveau :
  - des fiches de théorie (résumé par thème, images, exercices corrigés et
    3 questions d'auto-évaluation) suivant le programme FFESSM / tables MN90
  - un quiz d'entraînement (QCM avec correction détaillée, navigation libre)
  - un mode examen (QCM chronométrés, sans correction)
  - une carte communautaire des spots avec photos et poissons observés
  - un compte personnel : suivi des fiches vues et historique des scores
"""

import os
import io
import ssl
import secrets
import smtplib
import logging
from email.message import EmailMessage

from flask import (
    Flask, render_template, abort, request, jsonify, session,
    redirect, url_for, flash, Response,
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user,
)
from functools import wraps
from sqlalchemy import func, inspect as sa_inspect, text
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from authlib.integrations.flask_client import OAuth

from data.content import CHAPITRES, HINTS, PASCAL
from data.questions import QUESTION_BANK, QUESTION_BY_ID
from data.exercices import EXERCICES, NOTE_TABLES
from data.spots import SPOTS, FISH
from data.signals import SIGNALS, SIGNAL_BY_KEY
from models import (
    db, User, TestResult, ChapterStudy, QuestionComment,
    Spot, SpotComment, SpotPhoto, Species, DiveLog,
)
import recognition

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "plongee-n2-dev-secret-change-me")

# Base de données : PostgreSQL en production (DATABASE_URL), SQLite en local.
db_url = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "diving.db"))
if db_url.startswith("postgres://"):  # compat anciens schémas Heroku/Render
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 Mo max par upload

# Journal de démarrage : indique clairement la base utilisée. Sur un hébergeur
# au disque éphémère (ex. Render gratuit), SQLite est REMIS À ZÉRO à chaque
# redémarrage → les comptes disparaissent. Il faut alors une base PostgreSQL.
logging.basicConfig(level=logging.INFO)
if db_url.startswith("sqlite"):
    app.logger.warning(
        "Base SQLITE utilisée (%s). En production sur disque éphémère, les "
        "comptes seront perdus à chaque redémarrage : définis DATABASE_URL "
        "vers une base PostgreSQL.", db_url,
    )
else:
    app.logger.info("Base de données : %s", db_url.split("@")[-1])

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "connexion"
login_manager.login_message = "Connecte-toi pour accéder à ton espace personnel."

# --- Connexion via Google / Facebook (OAuth 2) ---
# Activée seulement si les identifiants sont fournis en variables d'environnement.
oauth = OAuth(app)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
FACEBOOK_CLIENT_ID = os.environ.get("FACEBOOK_CLIENT_ID")
FACEBOOK_CLIENT_SECRET = os.environ.get("FACEBOOK_CLIENT_SECRET")

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET:
    oauth.register(
        name="facebook",
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url="https://graph.facebook.com/v18.0/oauth/access_token",
        authorize_url="https://www.facebook.com/v18.0/dialog/oauth",
        api_base_url="https://graph.facebook.com/v18.0/",
        client_kwargs={"scope": "email public_profile"},
    )


def configured_oauth_providers():
    """Liste [(clé, libellé)] des fournisseurs OAuth configurés."""
    provs = []
    if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
        provs.append(("google", "Google"))
    if FACEBOOK_CLIENT_ID and FACEBOOK_CLIENT_SECRET:
        provs.append(("facebook", "Facebook"))
    return provs


NB_QUESTIONS_TEST = 40
DUREE_EXAMEN_MIN = 40  # minutes pour le mode examen

# Comptes administrateurs : liste d'e-mails dans la variable ADMIN_EMAILS
# (séparés par des virgules). Pas de migration de base nécessaire.
ADMIN_EMAILS = {
    e.strip().lower()
    for e in os.environ.get("ADMIN_EMAILS", "").split(",")
    if e.strip()
}

CHAPITRE_BY_SLUG = {c["slug"]: c for c in CHAPITRES}

# Envoi d'e-mails (réinitialisation de mot de passe). Configuré via variables
# d'environnement ; si non configuré, le lien est journalisé côté serveur.
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_SENDER = os.environ.get("MAIL_SENDER", MAIL_USERNAME or "no-reply@plongee-n2")
# SSL implicite (port 465) : activé explicitement, ou déduit du port 465.
MAIL_USE_SSL = (os.environ.get("MAIL_USE_SSL", "").lower() in ("1", "true", "yes")
                or MAIL_PORT == 465)
MAIL_TIMEOUT = int(os.environ.get("MAIL_TIMEOUT", "15"))

reset_serializer = URLSafeTimedSerializer(app.secret_key, salt="password-reset")
verify_serializer = URLSafeTimedSerializer(app.secret_key, salt="email-verify")
RESET_MAX_AGE = 3600           # 1 heure
VERIFY_MAX_AGE = 7 * 24 * 3600  # 7 jours


def mail_configured():
    return bool(MAIL_SERVER and MAIL_USERNAME and MAIL_PASSWORD)


def send_email(destinataire, sujet, corps):
    """Envoie un e-mail. Retourne (True, None) si envoyé, sinon (False, message)."""
    if not mail_configured():
        manque = [n for n, v in (("MAIL_SERVER", MAIL_SERVER),
                                 ("MAIL_USERNAME", MAIL_USERNAME),
                                 ("MAIL_PASSWORD", MAIL_PASSWORD)) if not v]
        app.logger.warning(
            "E-mail non configuré (variables manquantes : %s). Message destiné à "
            "%s NON envoyé. Contenu :\n%s", ", ".join(manque), destinataire, corps,
        )
        return False, "e-mail non configuré (%s manquant)" % ", ".join(manque)
    msg = EmailMessage()
    msg["Subject"] = sujet
    msg["From"] = MAIL_SENDER
    msg["To"] = destinataire
    msg.set_content(corps)
    try:
        ctx = ssl.create_default_context()
        if MAIL_USE_SSL:
            with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=ctx,
                                  timeout=MAIL_TIMEOUT) as s:
                s.login(MAIL_USERNAME, MAIL_PASSWORD)
                s.send_message(msg)
        else:
            with smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=MAIL_TIMEOUT) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.login(MAIL_USERNAME, MAIL_PASSWORD)
                s.send_message(msg)
        app.logger.info("E-mail « %s » envoyé à %s.", sujet, destinataire)
        return True, None
    except Exception as exc:  # noqa: BLE001 (on journalise toute erreur SMTP)
        app.logger.error("Échec d'envoi d'e-mail à %s : %s", destinataire, exc)
        return False, str(exc)


if not mail_configured():
    app.logger.warning(
        "E-mails NON configurés : la confirmation d'adresse et la réinitialisation "
        "de mot de passe ne seront PAS envoyées. Définis MAIL_SERVER, MAIL_USERNAME "
        "et MAIL_PASSWORD (voir README, section « envoi d'e-mail »)."
    )


def send_verification_email(user):
    """Envoie l'e-mail de confirmation d'adresse. Retourne (ok, erreur)."""
    token = verify_serializer.dumps(user.email)
    lien = url_for("verifier_email", token=token, _external=True)
    corps = (
        "Bonjour %s,\n\n"
        "Bienvenue sur Palanquée ! Confirme ton adresse e-mail en cliquant sur "
        "ce lien (valable 7 jours) :\n\n%s\n\n"
        "Si tu n'es pas à l'origine de cette inscription, ignore cet e-mail."
        % (user.pseudo, lien)
    )
    return send_email(user.email, "Confirme ton adresse — Palanquée", corps)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def is_admin(user=None):
    user = user or current_user
    return (
        getattr(user, "is_authenticated", False)
        and (user.email or "").lower() in ADMIN_EMAILS
    )


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not is_admin():
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def _seed_spots():
    """Insère les spots pré-définis dans la base si elle est vide."""
    if Spot.query.count() == 0:
        for s in SPOTS:
            db.session.add(Spot(
                key=s["id"], nom=s["nom"], lieu=s["lieu"], lat=s["lat"], lon=s["lon"],
                profondeur=s["profondeur"], description=s["desc"],
                poissons=",".join(s["poissons"]),
            ))
        db.session.commit()


def _seed_species():
    """Insère les espèces de référence dans le catalogue si vide."""
    if Species.query.count() == 0:
        for key, f in FISH.items():
            db.session.add(Species(
                key=key, nom=f["nom"], nom_scientifique=f.get("nom_scientifique"),
                categorie=f.get("categorie", "poisson"), description=f["desc"],
                habitat=f.get("habitat"), taille=f.get("taille"),
                image=f.get("image"), signal_key=f.get("signal"),
                validated=True, source="seed",
            ))
        db.session.commit()


CATEGORY_EMOJI = {
    "poisson": "🐟", "invertébré": "🦀", "mollusque": "🐙", "crustacé": "🦞",
    "végétal": "🌿", "reptile": "🐢", "mammifère": "🐬", "autre": "🌊",
}


def species_map(validated_only=True):
    """Dictionnaire {clé: Species} pour les templates (remplace l'ancien FISH)."""
    q = Species.query
    if validated_only:
        q = q.filter_by(validated=True)
    return {s.key: s for s in q.order_by(Species.nom.asc()).all()}


def species_photo_url(sp):
    """URL d'illustration d'une espèce : image de référence, sinon photo taguée."""
    img = getattr(sp, "image", None)
    if img:
        return url_for("static", filename="img/" + img)
    pid = getattr(sp, "photo_id", None)
    if pid:
        return url_for("spot_photo", photo_id=pid)
    return ""


def _migrate_schema():
    """Ajoute les colonnes récentes aux bases existantes (create_all n'ALTER pas)."""
    insp = sa_inspect(db.engine)
    if "users" not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns("users")}
    dialect = db.engine.dialect.name
    bool_default = "FALSE" if dialect == "postgresql" else "0"
    stmts = []
    if "email_verified" not in cols:
        stmts.append("ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL "
                     "DEFAULT %s" % bool_default)
    if "oauth_provider" not in cols:
        stmts.append("ALTER TABLE users ADD COLUMN oauth_provider VARCHAR(20)")
    # Les comptes OAuth n'ont pas de mot de passe : la colonne doit être nullable.
    if dialect == "postgresql":
        stmts.append("ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL")
    for s in stmts:
        try:
            db.session.execute(text(s))
            db.session.commit()
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            app.logger.info("Migration ignorée (%s) : %s", s.split(" ADD")[0], exc)


with app.app_context():
    db.create_all()
    _migrate_schema()
    _seed_spots()
    _seed_species()


# ---------------------------------------------------------------------------
# Pages "contenu"
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template(
        "index.html",
        chapitres=CHAPITRES,
        nb_questions=len(QUESTION_BANK),
        nb_test=NB_QUESTIONS_TEST,
    )


@app.route("/apprendre")
def apprendre():
    """Espace unique : réviser la théorie ET s'entraîner (tests)."""
    studied = _studied_slugs()
    return render_template(
        "apprendre.html",
        chapitres=CHAPITRES,
        studied=studied,
        nb_questions=len(QUESTION_BANK),
        nb_test=NB_QUESTIONS_TEST,
        duree_min=DUREE_EXAMEN_MIN,
    )


@app.route("/cours")
def cours():
    # Ancien onglet « Cours » : désormais fusionné avec les tests.
    return redirect(url_for("apprendre"))


@app.route("/cours/<slug>")
def chapitre(slug):
    chap = CHAPITRE_BY_SLUG.get(slug)
    if not chap:
        abort(404)
    idx = CHAPITRES.index(chap)
    precedent = CHAPITRES[idx - 1] if idx > 0 else None
    suivant = CHAPITRES[idx + 1] if idx < len(CHAPITRES) - 1 else None

    # Suivi : on enregistre la consultation du chapitre pour l'utilisateur connecté.
    if current_user.is_authenticated:
        _marquer_etudie(slug)

    return render_template(
        "chapitre.html",
        chap=chap,
        precedent=precedent,
        suivant=suivant,
        exercices=EXERCICES.get(chap["num"], []),
        note_tables=NOTE_TABLES,
        hints=HINTS.get(chap["num"], []),
        pascal=PASCAL,
    )


# ---------------------------------------------------------------------------
# Spots de plongée (carte + banque de photos communautaire)
# ---------------------------------------------------------------------------

def _spot_photo_counts():
    rows = (db.session.query(SpotPhoto.spot_id, func.count(SpotPhoto.id))
            .group_by(SpotPhoto.spot_id).all())
    return {sid: n for sid, n in rows}


def _slugify(text):
    import re
    import unicodedata
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "spot"


@app.route("/spots")
def spots():
    all_spots = Spot.query.order_by(Spot.created_at.asc()).all()
    counts = _spot_photo_counts()
    spots_json = [
        {"key": s.key, "nom": s.nom, "lieu": s.lieu, "lat": s.lat, "lon": s.lon,
         "nb_poissons": len(s.fish_keys), "nb_photos": counts.get(s.key, 0),
         "user": s.user_created}
        for s in all_spots
    ]
    return render_template("spots.html", spots=all_spots, spots_json=spots_json,
                           counts=counts, fish=species_map())


@app.route("/spots/<key>")
def spot(key):
    s = Spot.query.filter_by(key=key).first()
    if not s:
        abort(404)
    smap = species_map()
    poissons = [smap[k] for k in s.fish_keys if k in smap]
    photos = (SpotPhoto.query.filter_by(spot_id=key)
              .order_by(SpotPhoto.created_at.desc()).all())
    comments = (SpotComment.query.filter_by(spot_key=key)
                .order_by(SpotComment.created_at.asc()).all())
    return render_template("spot.html", spot=s, poissons=poissons, photos=photos,
                           comments=comments, fish=smap)


@app.route("/spots/add", methods=["POST"])
@login_required
def spot_add():
    nom = (request.form.get("nom") or "").strip()
    try:
        lat = float(request.form.get("lat"))
        lon = float(request.form.get("lon"))
    except (TypeError, ValueError):
        lat = lon = None
    if not nom or lat is None or lon is None or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        flash("Donne un nom et clique sur la carte pour placer ton spot.", "error")
        return redirect(url_for("spots"))

    valid_keys = set(species_map().keys())
    poissons = [k for k in request.form.getlist("poissons") if k in valid_keys]
    key = base = _slugify(nom)
    i = 2
    while Spot.query.filter_by(key=key).first():
        key = "%s-%d" % (base, i)
        i += 1
    db.session.add(Spot(
        key=key, nom=nom[:120], lieu=(request.form.get("lieu") or "").strip()[:160],
        lat=lat, lon=lon, profondeur=(request.form.get("profondeur") or "").strip()[:40],
        description=(request.form.get("desc") or "").strip()[:1000],
        poissons=",".join(poissons), created_by=current_user.id, pseudo=current_user.pseudo,
    ))
    db.session.commit()
    flash("Merci ! Ton spot a été ajouté à la carte. 🗺️", "success")
    return redirect(url_for("spot", key=key))


@app.route("/spots/<key>/comment", methods=["POST"])
@login_required
def spot_comment_add(key):
    s = Spot.query.filter_by(key=key).first()
    if not s:
        abort(404)
    texte = (request.form.get("comment") or "").strip()[:1000]
    if texte:
        db.session.add(SpotComment(
            spot_key=key, user_id=current_user.id,
            pseudo=current_user.pseudo, comment=texte,
        ))
        db.session.commit()
        flash("Ton commentaire a été publié.", "success")
    return redirect(url_for("spot", key=key))


@app.route("/spots/<key>/photo", methods=["POST"])
@login_required
def spot_photo_upload(key):
    s = Spot.query.filter_by(key=key).first()
    if not s:
        abort(404)
    file = request.files.get("photo")
    if not file or not file.filename:
        flash("Choisis une photo à envoyer.", "error")
        return redirect(url_for("spot", key=key))
    try:
        from PIL import Image
        img = Image.open(file.stream)
        img = img.convert("RGB")
        img.thumbnail((1280, 1280))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82, optimize=True)
        data = buf.getvalue()
    except Exception:
        flash("Fichier image invalide (formats acceptés : JPEG, PNG…).", "error")
        return redirect(url_for("spot", key=key))

    smap = species_map()
    fish_key = request.form.get("fish_key") or None
    if fish_key not in smap:
        fish_key = None
    proposed = (request.form.get("nouvelle_espece") or "").strip()[:120]
    caption = (request.form.get("caption") or "").strip()[:300]

    photo = SpotPhoto(
        spot_id=key, fish_key=fish_key, caption=caption,
        mimetype="image/jpeg", data=data,
        user_id=current_user.id, pseudo=current_user.pseudo,
    )
    db.session.add(photo)
    db.session.commit()  # commit pour disposer de photo.id (illustration d'espèce)

    msg = "Merci ! Ta photo a été ajoutée à la banque du spot. 🐟"

    if not fish_key:
        # 1) L'utilisateur propose lui-même une nouvelle espèce.
        if proposed:
            sp = _register_species(proposed, photo, source="communauté")
            photo.fish_key = sp.key
            db.session.commit()
            msg += (" Ton espèce « %s » a été proposée et sera visible après "
                    "validation." % sp.nom)
        else:
            # 2) Reconnaissance automatique (si un backend est configuré).
            suggestion = recognition.identify(
                data, "image/jpeg", known=[s.nom for s in smap.values()])
            if suggestion and suggestion["confiance"] >= recognition.min_confidence():
                match = _match_species(suggestion["nom"], smap)
                if match:
                    photo.fish_key = match.key
                    db.session.commit()
                    msg += (" 🤖 Reconnaissance : %s (confiance %.0f%%) — "
                            "photo classée automatiquement."
                            % (match.nom, 100 * suggestion["confiance"]))
                else:
                    sp = _register_species(
                        suggestion["nom"], photo, source="reconnaissance",
                        nom_scientifique=suggestion.get("nom_scientifique"),
                        categorie=suggestion.get("categorie"),
                        confidence=suggestion["confiance"],
                    )
                    photo.fish_key = sp.key
                    db.session.commit()
                    msg += (" 🤖 Reconnaissance : %s (confiance %.0f%%) — nouvelle "
                            "espèce proposée, en attente de validation."
                            % (sp.nom, 100 * suggestion["confiance"]))

    flash(msg, "success")
    return redirect(url_for("spot", key=key))


def _match_species(nom, smap):
    """Rapproche un nom proposé d'une espèce existante (comparaison souple)."""
    cible = _slugify(nom)
    for sp in smap.values():
        if _slugify(sp.nom) == cible or (
                sp.nom_scientifique and _slugify(sp.nom_scientifique) == cible):
            return sp
    return None


def _register_species(nom, photo, source, nom_scientifique=None,
                      categorie=None, confidence=None):
    """Crée (ou retrouve) une espèce proposée, en attente de validation."""
    base = _slugify(nom)
    existing = Species.query.filter_by(key=base).first()
    if existing:
        return existing
    key = base
    i = 2
    while Species.query.filter_by(key=key).first():
        key = "%s-%d" % (base, i)
        i += 1
    sp = Species(
        key=key, nom=nom[:120], nom_scientifique=nom_scientifique,
        categorie=(categorie or "autre")[:40], photo_id=photo.id,
        validated=False, source=source, confidence=confidence,
        created_by=current_user.id if current_user.is_authenticated else None,
        pseudo=current_user.pseudo if current_user.is_authenticated else None,
    )
    db.session.add(sp)
    db.session.commit()
    return sp


@app.route("/spot-photo/<int:photo_id>")
def spot_photo(photo_id):
    p = db.session.get(SpotPhoto, photo_id)
    if not p:
        abort(404)
    return Response(p.data, mimetype=p.mimetype or "image/jpeg",
                    headers={"Cache-Control": "public, max-age=86400"})


def _photos_by_species():
    photos = (SpotPhoto.query.filter(SpotPhoto.fish_key.isnot(None))
              .order_by(SpotPhoto.created_at.desc()).all())
    by_fish = {}
    for p in photos:
        by_fish.setdefault(p.fish_key, []).append(p)
    return by_fish


@app.route("/poissons")
@app.route("/vie-sous-marine")
def poissons():
    """Guide de la vie sous-marine, enrichi par les photos taguées et la
    reconnaissance automatique. Regroupé par catégorie."""
    species = (Species.query.filter_by(validated=True)
               .order_by(Species.categorie.asc(), Species.nom.asc()).all())
    by_fish = _photos_by_species()
    par_categorie = {}
    for sp in species:
        par_categorie.setdefault(sp.categorie or "autre", []).append(sp)
    nb_attente = Species.query.filter_by(validated=False).count() if is_admin() else 0
    return render_template(
        "poissons.html", par_categorie=par_categorie, by_fish=by_fish,
        nb_especes=len(species), nb_attente=nb_attente,
    )


@app.route("/signes")
def signes():
    """Mémo des signes de plongée, regroupés par catégorie."""
    ordre = ["communication", "securite", "faune"]
    titres = {
        "communication": "💬 Communication de base",
        "securite": "🚨 Sécurité & détresse",
        "faune": "🐟 Faune (indicatifs)",
    }
    par_cat = {c: [] for c in ordre}
    for s in SIGNALS:
        par_cat.setdefault(s["categorie"], []).append(s)
    return render_template("signes.html", par_cat=par_cat, ordre=ordre, titres=titres)


@app.route("/espece/<key>")
def espece(key):
    sp = Species.query.filter_by(key=key).first()
    if not sp or (not sp.validated and not is_admin()):
        abort(404)
    photos = (SpotPhoto.query.filter_by(fish_key=key)
              .order_by(SpotPhoto.created_at.desc()).all())
    signal = SIGNAL_BY_KEY.get(sp.signal_key) if sp.signal_key else None
    # Spots où l'espèce est renseignée.
    spots_ici = [s for s in Spot.query.all() if key in s.fish_keys]
    return render_template("espece.html", sp=sp, photos=photos, signal=signal,
                           spots_ici=spots_ici)


# --- Modération (admins uniquement) ---

@app.route("/admin/photo/<int:photo_id>/delete", methods=["POST"])
@admin_required
def admin_delete_photo(photo_id):
    p = db.session.get(SpotPhoto, photo_id)
    dest = url_for("spots")
    if p:
        dest = url_for("spot", key=p.spot_id)
        db.session.delete(p)
        db.session.commit()
        flash("Photo supprimée.", "success")
    return redirect(dest)


@app.route("/admin/spot-comment/<int:cid>/delete", methods=["POST"])
@admin_required
def admin_delete_spot_comment(cid):
    c = db.session.get(SpotComment, cid)
    dest = url_for("spots")
    if c:
        dest = url_for("spot", key=c.spot_key)
        db.session.delete(c)
        db.session.commit()
        flash("Commentaire supprimé.", "success")
    return redirect(dest)


@app.route("/admin/spot/<key>/delete", methods=["POST"])
@admin_required
def admin_delete_spot(key):
    s = Spot.query.filter_by(key=key).first()
    if s:
        SpotPhoto.query.filter_by(spot_id=key).delete()
        SpotComment.query.filter_by(spot_key=key).delete()
        db.session.delete(s)
        db.session.commit()
        flash("Spot supprimé.", "success")
    return redirect(url_for("spots"))


@app.route("/admin/especes")
@admin_required
def admin_especes():
    en_attente = (Species.query.filter_by(validated=False)
                  .order_by(Species.created_at.desc()).all())
    validees = (Species.query.filter_by(validated=True)
                .order_by(Species.nom.asc()).all())
    return render_template("admin_especes.html", en_attente=en_attente,
                           validees=validees, signals=SIGNALS)


@app.route("/admin/espece/<key>/valider", methods=["POST"])
@admin_required
def admin_valider_espece(key):
    sp = Species.query.filter_by(key=key).first()
    if sp:
        sp.validated = True
        # Champs éventuellement complétés par l'admin lors de la validation.
        for champ in ("categorie", "habitat", "taille", "nom_scientifique"):
            val = (request.form.get(champ) or "").strip()
            if val:
                setattr(sp, champ, val[:200])
        signal_key = request.form.get("signal_key") or None
        if signal_key in SIGNAL_BY_KEY:
            sp.signal_key = signal_key
        db.session.commit()
        flash("Espèce « %s » validée et ajoutée au guide." % sp.nom, "success")
    return redirect(url_for("admin_especes"))


@app.route("/admin/espece/<key>/signal", methods=["POST"])
@admin_required
def admin_espece_signal(key):
    sp = Species.query.filter_by(key=key).first()
    if sp:
        signal_key = request.form.get("signal_key") or None
        sp.signal_key = signal_key if signal_key in SIGNAL_BY_KEY else None
        db.session.commit()
        flash("Signe de plongée mis à jour pour « %s ». " % sp.nom, "success")
    return redirect(url_for("admin_especes"))


@app.route("/admin/espece/<key>/supprimer", methods=["POST"])
@admin_required
def admin_supprimer_espece(key):
    sp = Species.query.filter_by(key=key).first()
    if sp and sp.source != "seed":
        db.session.delete(sp)
        db.session.commit()
        flash("Espèce supprimée.", "success")
    else:
        flash("Les espèces de référence ne peuvent pas être supprimées.", "error")
    return redirect(url_for("admin_especes"))


@app.route("/admin/question-comment/<int:cid>/delete", methods=["POST"])
@admin_required
def admin_delete_question_comment(cid):
    c = db.session.get(QuestionComment, cid)
    if c:
        db.session.delete(c)
        db.session.commit()
        flash("Remarque supprimée.", "success")
    return redirect(url_for("admin_commentaires"))


# ---------------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------------

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for("profil"))
    if request.method == "POST":
        pseudo = (request.form.get("pseudo") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        password2 = request.form.get("password2") or ""

        erreurs = []
        if len(pseudo) < 2:
            erreurs.append("Le pseudo doit faire au moins 2 caractères.")
        if "@" not in email or "." not in email:
            erreurs.append("Adresse e-mail invalide.")
        if len(password) < 6:
            erreurs.append("Le mot de passe doit faire au moins 6 caractères.")
        if password != password2:
            erreurs.append("Les deux mots de passe ne correspondent pas.")
        if User.query.filter_by(email=email).first():
            erreurs.append("Un compte existe déjà avec cet e-mail.")

        if erreurs:
            for e in erreurs:
                flash(e, "error")
            return render_template("inscription.html", pseudo=pseudo, email=email)

        user = User(email=email, pseudo=pseudo, email_verified=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        ok, err = send_verification_email(user)
        if ok:
            flash("Bienvenue %s ! Un e-mail de confirmation vient d'être envoyé à "
                  "%s." % (pseudo, email), "success")
        elif app.debug:
            token = verify_serializer.dumps(user.email)
            lien = url_for("verifier_email", token=token, _external=True)
            flash("Compte créé. E-mail non configuré (mode test) — lien de "
                  "confirmation : %s" % lien, "success")
        else:
            flash("Bienvenue %s ! Ton compte est créé. (L'e-mail de confirmation "
                  "n'a pas pu être envoyé — tu pourras le renvoyer depuis ton "
                  "profil.)" % pseudo, "success")
        return redirect(url_for("profil"))

    return render_template("inscription.html", providers=configured_oauth_providers())


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for("profil"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Content de te revoir, %s !" % user.pseudo, "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("profil"))
        flash("E-mail ou mot de passe incorrect.", "error")
        return render_template("connexion.html", email=email,
                               providers=configured_oauth_providers())
    return render_template("connexion.html", providers=configured_oauth_providers())


@app.route("/mot-de-passe-oublie", methods=["GET", "POST"])
def mot_de_passe_oublie():
    if current_user.is_authenticated:
        return redirect(url_for("profil"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            token = reset_serializer.dumps(user.email)
            lien = url_for("reinitialiser", token=token, _external=True)
            corps = (
                "Bonjour %s,\n\n"
                "Tu as demandé à réinitialiser ton mot de passe sur Palanquée.\n"
                "Clique sur ce lien (valable 1 heure) pour choisir un nouveau "
                "mot de passe :\n\n%s\n\n"
                "Si tu n'es pas à l'origine de cette demande, ignore cet e-mail."
                % (user.pseudo, lien)
            )
            envoye, err = send_email(
                user.email,
                "Réinitialisation de ton mot de passe — Palanquée",
                corps,
            )
            # En local (debug) sans SMTP configuré, on affiche le lien pour tester.
            if not envoye and app.debug:
                flash("E-mail non configuré (mode test) — lien de "
                      "réinitialisation : %s" % lien, "success")
        # Message neutre dans tous les cas (évite de révéler quels e-mails existent).
        flash("Si un compte existe avec cet e-mail, un lien de réinitialisation "
              "vient d'être envoyé.", "success")
        return redirect(url_for("connexion"))
    return render_template("mot_de_passe_oublie.html")


@app.route("/reinitialiser/<token>", methods=["GET", "POST"])
def reinitialiser(token):
    try:
        email = reset_serializer.loads(token, max_age=RESET_MAX_AGE)
    except SignatureExpired:
        flash("Ce lien de réinitialisation a expiré. Refais une demande.", "error")
        return redirect(url_for("mot_de_passe_oublie"))
    except BadSignature:
        flash("Lien de réinitialisation invalide.", "error")
        return redirect(url_for("mot_de_passe_oublie"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Compte introuvable.", "error")
        return redirect(url_for("connexion"))

    if request.method == "POST":
        password = request.form.get("password") or ""
        password2 = request.form.get("password2") or ""
        if len(password) < 6:
            flash("Le mot de passe doit faire au moins 6 caractères.", "error")
        elif password != password2:
            flash("Les deux mots de passe ne correspondent pas.", "error")
        else:
            user.set_password(password)
            db.session.commit()
            flash("Mot de passe mis à jour ! Tu peux te connecter.", "success")
            return redirect(url_for("connexion"))
    return render_template("reinitialiser.html", token=token)


@app.route("/verifier/<token>")
def verifier_email(token):
    try:
        email = verify_serializer.loads(token, max_age=VERIFY_MAX_AGE)
    except SignatureExpired:
        flash("Ce lien de confirmation a expiré. Renvoie-en un depuis ton profil.", "error")
        return redirect(url_for("profil") if current_user.is_authenticated else url_for("connexion"))
    except BadSignature:
        flash("Lien de confirmation invalide.", "error")
        return redirect(url_for("connexion"))

    user = User.query.filter_by(email=email).first()
    if user and not user.email_verified:
        user.email_verified = True
        db.session.commit()
        flash("Ton adresse e-mail est confirmée ! ✅", "success")
    elif user:
        flash("Ton adresse était déjà confirmée.", "success")
    return redirect(url_for("profil") if current_user.is_authenticated else url_for("connexion"))


@app.route("/renvoyer-verification")
@login_required
def renvoyer_verification():
    if current_user.email_verified:
        flash("Ton adresse est déjà confirmée.", "success")
        return redirect(url_for("profil"))
    ok, err = send_verification_email(current_user)
    if ok:
        flash("E-mail de confirmation renvoyé à %s." % current_user.email, "success")
    elif app.debug:
        token = verify_serializer.dumps(current_user.email)
        lien = url_for("verifier_email", token=token, _external=True)
        flash("E-mail non configuré (mode test) — lien : %s" % lien, "success")
    else:
        flash("Envoi impossible pour le moment (%s). Réessaie plus tard." % err, "error")
    return redirect(url_for("profil"))


@app.route("/connexion/<provider>")
def oauth_login(provider):
    client = oauth.create_client(provider)
    if client is None:
        flash("La connexion via %s n'est pas disponible." % provider.capitalize(), "error")
        return redirect(url_for("connexion"))
    redirect_uri = url_for("oauth_callback", provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)


@app.route("/connexion/<provider>/callback")
def oauth_callback(provider):
    client = oauth.create_client(provider)
    if client is None:
        abort(404)
    try:
        token = client.authorize_access_token()
    except Exception as exc:  # noqa: BLE001
        app.logger.warning("Échec OAuth %s : %s", provider, exc)
        flash("La connexion via %s a échoué. Réessaie." % provider.capitalize(), "error")
        return redirect(url_for("connexion"))

    email = name = None
    if provider == "google":
        info = token.get("userinfo")
        if not info:
            try:
                info = client.userinfo()
            except Exception:  # noqa: BLE001
                info = {}
        email = info.get("email")
        name = info.get("name") or info.get("given_name")
    else:  # facebook
        try:
            info = client.get("me?fields=id,name,email").json()
        except Exception:  # noqa: BLE001
            info = {}
        email = info.get("email")
        name = info.get("name")

    if not email:
        flash("Impossible de récupérer ton adresse e-mail depuis %s. "
              "Vérifie que tu autorises le partage de l'e-mail." % provider.capitalize(), "error")
        return redirect(url_for("connexion"))

    email = email.strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            email=email, pseudo=(name or email.split("@")[0])[:80],
            email_verified=True, oauth_provider=provider,
        )
        db.session.add(user)
        db.session.commit()
        flash("Compte créé via %s. Bienvenue %s !" % (provider.capitalize(), user.pseudo), "success")
    else:
        if not user.email_verified:
            user.email_verified = True  # e-mail garanti par le fournisseur
        if not user.oauth_provider:
            user.oauth_provider = provider
        db.session.commit()
        flash("Content de te revoir, %s !" % user.pseudo, "success")
    login_user(user)
    return redirect(url_for("profil"))


@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    flash("Tu es déconnecté. À bientôt !", "success")
    return redirect(url_for("index"))


@app.route("/profil")
@login_required
def profil():
    results = (
        TestResult.query.filter_by(user_id=current_user.id)
        .order_by(TestResult.created_at.desc())
        .all()
    )
    studied = _studied_slugs()
    moyenne = round(sum(r.note20 for r in results) / len(results), 1) if results else None

    # Statistiques synthétiques
    stats = {
        "nb_tests": len(results),
        "nb_chap_etudies": len(studied),
        "nb_chap_total": len(CHAPITRES),
        "meilleure_note": max((r.note20 for r in results), default=None),
        "moyenne": moyenne,
    }

    # Données du graphique d'évolution (ordre chronologique).
    chart = [
        {
            "date": r.created_at.strftime("%d/%m"),
            "note": r.note20,
            "mode": r.mode,
        }
        for r in reversed(results)
    ]

    # Comparaison à la communauté.
    global_avg, nb_joueurs = _global_average()

    return render_template(
        "profil.html",
        results=results,
        studied=studied,
        chapitres=CHAPITRES,
        stats=stats,
        chart=chart,
        global_avg=global_avg,
        nb_joueurs=nb_joueurs,
    )


@app.route("/profil/modifier", methods=["GET", "POST"])
@login_required
def profil_modifier():
    user = current_user
    if request.method == "POST":
        action = request.form.get("action")

        if action == "infos":
            pseudo = (request.form.get("pseudo") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            erreurs = []
            if len(pseudo) < 2:
                erreurs.append("Le pseudo doit faire au moins 2 caractères.")
            if "@" not in email or "." not in email:
                erreurs.append("Adresse e-mail invalide.")
            autre = User.query.filter_by(email=email).first()
            if autre and autre.id != user.id:
                erreurs.append("Cet e-mail est déjà utilisé par un autre compte.")
            if erreurs:
                for e in erreurs:
                    flash(e, "error")
                return redirect(url_for("profil_modifier"))

            user.pseudo = pseudo
            if email != user.email:
                user.email = email
                user.email_verified = False
                db.session.commit()
                ok, err = send_verification_email(user)
                if ok:
                    flash("Informations mises à jour. Un e-mail de confirmation a été "
                          "envoyé à ta nouvelle adresse.", "success")
                elif app.debug:
                    token = verify_serializer.dumps(user.email)
                    flash("Infos mises à jour. E-mail non configuré (test) — lien : %s"
                          % url_for("verifier_email", token=token, _external=True), "success")
                else:
                    flash("Informations mises à jour. (E-mail de confirmation non "
                          "envoyé — renvoie-le depuis ton profil.)", "success")
            else:
                db.session.commit()
                flash("Informations mises à jour.", "success")
            return redirect(url_for("profil"))

        if action == "password":
            actuel = request.form.get("actuel") or ""
            nouveau = request.form.get("nouveau") or ""
            nouveau2 = request.form.get("nouveau2") or ""
            if user.has_password and not user.check_password(actuel):
                flash("Ton mot de passe actuel est incorrect.", "error")
            elif len(nouveau) < 6:
                flash("Le nouveau mot de passe doit faire au moins 6 caractères.", "error")
            elif nouveau != nouveau2:
                flash("Les deux mots de passe ne correspondent pas.", "error")
            else:
                user.set_password(nouveau)
                db.session.commit()
                flash("Mot de passe mis à jour.", "success")
            return redirect(url_for("profil_modifier"))

    return render_template("profil_modifier.html", user=user)


def _num(val, cast):
    try:
        v = (val or "").strip()
        return cast(v) if v != "" else None
    except (TypeError, ValueError):
        return None


@app.route("/carnet")
@login_required
def carnet():
    """Carnet de plongée personnel : liste des plongées et statistiques."""
    logs = (DiveLog.query.filter_by(user_id=current_user.id)
            .order_by(DiveLog.date.desc(), DiveLog.id.desc()).all())
    total_min = sum(l.duree_min or 0 for l in logs)
    profs = [l.profondeur_max for l in logs if l.profondeur_max]
    spots_visites = {(l.spot_key or l.spot_nom) for l in logs if (l.spot_key or l.spot_nom)}
    stats = {
        "nb": len(logs),
        "temps_total_h": round(total_min / 60, 1) if total_min else 0,
        "prof_max": max(profs) if profs else None,
        "prof_moy": round(sum(profs) / len(profs), 1) if profs else None,
        "nb_spots": len(spots_visites),
    }
    spots = Spot.query.order_by(Spot.nom.asc()).all()
    prefill = request.args.get("spot") or ""
    return render_template("carnet.html", logs=logs, stats=stats, spots=spots,
                           prefill_spot=prefill)


@app.route("/carnet/ajouter", methods=["POST"])
@login_required
def carnet_ajouter():
    from datetime import datetime
    d = None
    raw_date = (request.form.get("date") or "").strip()
    if raw_date:
        try:
            d = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            d = None

    spot_key = (request.form.get("spot_key") or "").strip() or None
    spot_nom = (request.form.get("spot_nom") or "").strip()[:160]
    if spot_key:
        s = Spot.query.filter_by(key=spot_key).first()
        if s and not spot_nom:
            spot_nom = s.nom
        if not s:
            spot_key = None

    ressenti = _num(request.form.get("ressenti"), int)
    if ressenti is not None:
        ressenti = max(1, min(5, ressenti))

    log = DiveLog(
        user_id=current_user.id, date=d, spot_key=spot_key, spot_nom=spot_nom or None,
        profondeur_max=_num(request.form.get("profondeur_max"), float),
        duree_min=_num(request.form.get("duree_min"), int),
        temp_eau=_num(request.form.get("temp_eau"), float),
        visibilite=(request.form.get("visibilite") or "").strip()[:40] or None,
        binome=(request.form.get("binome") or "").strip()[:120] or None,
        lestage=(request.form.get("lestage") or "").strip()[:40] or None,
        gaz=(request.form.get("gaz") or "").strip()[:40] or None,
        ressenti=ressenti,
        notes=(request.form.get("notes") or "").strip()[:2000] or None,
    )
    db.session.add(log)
    db.session.commit()
    flash("Plongée ajoutée à ton carnet. 🤿", "success")
    return redirect(url_for("carnet"))


@app.route("/carnet/<int:log_id>/supprimer", methods=["POST"])
@login_required
def carnet_supprimer(log_id):
    log = db.session.get(DiveLog, log_id)
    if log and log.user_id == current_user.id:
        db.session.delete(log)
        db.session.commit()
        flash("Plongée supprimée du carnet.", "success")
    return redirect(url_for("carnet"))


@app.route("/classement")
def classement():
    """Classement de la communauté par note moyenne (compétition)."""
    rows = _leaderboard()
    global_avg, nb_joueurs = _global_average()
    mon_rang = None
    if current_user.is_authenticated:
        for i, r in enumerate(rows, start=1):
            if r["user_id"] == current_user.id:
                mon_rang = i
                break
    return render_template(
        "classement.html",
        rows=rows,
        global_avg=global_avg,
        nb_joueurs=nb_joueurs,
        mon_rang=mon_rang,
        current_uid=current_user.id if current_user.is_authenticated else None,
    )


@app.route("/admin")
@admin_required
def admin():
    """Tableau de bord administrateur : tous les comptes et leurs scores."""
    rows = _user_aggregates()
    global_avg, nb_joueurs = _global_average()
    totaux = {
        "nb_comptes": User.query.count(),
        "nb_tests": TestResult.query.count(),
        "global_avg": global_avg,
    }
    nb_comment = QuestionComment.query.count()
    nb_especes_attente = Species.query.filter_by(validated=False).count()
    return render_template("admin.html", rows=rows, totaux=totaux,
                           nb_comment=nb_comment, nb_especes_attente=nb_especes_attente,
                           mail_ok=mail_configured(), mail_server=MAIL_SERVER)


@app.route("/admin/test-email", methods=["POST"])
@admin_required
def admin_test_email():
    dest = (request.form.get("dest") or "").strip() or current_user.email
    ok, err = send_email(
        dest, "Test d'envoi — Palanquée",
        "Ceci est un e-mail de test envoyé depuis l'administration de Palanquée. "
        "Si tu le reçois, la configuration SMTP fonctionne. ✅",
    )
    if ok:
        flash("E-mail de test envoyé à %s. Vérifie ta boîte (et les spams)." % dest, "success")
    else:
        flash("Échec de l'envoi : %s" % err, "error")
    return redirect(url_for("admin"))


@app.route("/admin/commentaires")
@admin_required
def admin_commentaires():
    comments = (
        QuestionComment.query.order_by(QuestionComment.created_at.desc()).all()
    )
    return render_template("commentaires.html", comments=comments)


# ---------------------------------------------------------------------------
# Helpers suivi
# ---------------------------------------------------------------------------

def _studied_slugs():
    """Ensemble des slugs de chapitres étudiés par l'utilisateur connecté."""
    if not current_user.is_authenticated:
        return set()
    rows = ChapterStudy.query.filter_by(user_id=current_user.id).all()
    return {r.chapter_slug for r in rows}


def _marquer_etudie(slug):
    existe = ChapterStudy.query.filter_by(
        user_id=current_user.id, chapter_slug=slug
    ).first()
    if not existe:
        db.session.add(ChapterStudy(user_id=current_user.id, chapter_slug=slug))
        db.session.commit()


def _global_average():
    """Moyenne globale des notes (tous comptes) et nombre de joueurs ayant testé."""
    avg = db.session.query(func.avg(TestResult.note20)).scalar()
    nb_joueurs = db.session.query(
        func.count(func.distinct(TestResult.user_id))
    ).scalar() or 0
    return (round(avg, 1) if avg is not None else None), nb_joueurs


def _user_aggregates():
    """Agrégats par utilisateur : nb tests, moyenne, meilleure note, dernière activité."""
    rows = (
        db.session.query(
            User.id, User.pseudo, User.email, User.created_at,
            func.count(TestResult.id).label("nb"),
            func.avg(TestResult.note20).label("moy"),
            func.max(TestResult.note20).label("best"),
            func.max(TestResult.created_at).label("last"),
        )
        .outerjoin(TestResult, TestResult.user_id == User.id)
        .group_by(User.id)
        .all()
    )
    result = []
    for r in rows:
        result.append({
            "user_id": r.id,
            "pseudo": r.pseudo,
            "email": r.email,
            "created_at": r.created_at,
            "nb_tests": r.nb or 0,
            "moyenne": round(r.moy, 1) if r.moy is not None else None,
            "meilleure": round(r.best, 1) if r.best is not None else None,
            "derniere": r.last,
            "is_admin": (r.email or "").lower() in ADMIN_EMAILS,
        })
    return result


def _leaderboard():
    """Classement des joueurs ayant passé au moins un test, par note moyenne."""
    rows = [r for r in _user_aggregates() if r["nb_tests"] > 0]
    rows.sort(key=lambda r: (r["moyenne"], r["meilleure"]), reverse=True)
    return rows


# ---------------------------------------------------------------------------
# Tests (blanc / examen)
# ---------------------------------------------------------------------------

import random  # noqa: E402  (après config pour rester lisible)


RATIO_MULTI = 0.25  # au moins 1/4 de questions à choix multiples par test


def _balanced_pick(pool, k):
    """Choisit k questions du pool en rotation sur les chapitres (diversité)."""
    if k <= 0 or not pool:
        return []
    par_chap = {}
    for q in pool:
        par_chap.setdefault(q["chapitre"], []).append(q)
    for lst in par_chap.values():
        random.shuffle(lst)
    chapitres = list(par_chap.keys())
    random.shuffle(chapitres)
    chosen, pos = [], {c: 0 for c in chapitres}
    progressed = True
    while len(chosen) < k and progressed:
        progressed = False
        for c in chapitres:
            if pos[c] < len(par_chap[c]):
                chosen.append(par_chap[c][pos[c]])
                pos[c] += 1
                progressed = True
                if len(chosen) >= k:
                    break
    return chosen


def _tirer_questions(n):
    """Tire n questions distinctes : thèmes équilibrés et au moins 1/4 de QCM
    à choix multiples (plusieurs bonnes réponses)."""
    n = min(n, len(QUESTION_BANK))
    multi_pool = [q for q in QUESTION_BANK if q["multi"]]
    single_pool = [q for q in QUESTION_BANK if not q["multi"]]

    quota_multi = min(len(multi_pool), -(-n // 4))  # arrondi supérieur de n/4
    chosen = _balanced_pick(multi_pool, quota_multi)
    chosen += _balanced_pick(single_pool, n - len(chosen))

    # Filet de sécurité si une catégorie manque de questions.
    if len(chosen) < n:
        used = {q["id"] for q in chosen}
        reste = [q for q in QUESTION_BANK if q["id"] not in used]
        random.shuffle(reste)
        chosen += reste[: n - len(chosen)]

    random.shuffle(chosen)  # mélange l'ordre final (thèmes et types)
    return chosen[:n]


def _questions_pour_client(questions):
    # On envoie le type (multi) mais jamais les bonnes réponses.
    return [
        {
            "id": q["id"],
            "q": q["q"],
            "options": q["options"],
            "chapitre_titre": q["chapitre_titre"],
            "multi": q["multi"],
        }
        for q in questions
    ]


@app.route("/test/<mode>")
def test(mode):
    if mode not in ("blanc", "examen"):
        abort(404)
    questions = _tirer_questions(NB_QUESTIONS_TEST)
    session["test_ids"] = [q["id"] for q in questions]
    session["test_mode"] = mode
    return render_template(
        "test.html",
        mode=mode,
        questions=_questions_pour_client(questions),
        nb_questions=len(questions),
        duree_min=DUREE_EXAMEN_MIN,
    )


@app.route("/test/<mode>/submit", methods=["POST"])
def test_submit(mode):
    if mode not in ("blanc", "examen"):
        abort(404)
    data = request.get_json(silent=True) or {}
    reponses = data.get("reponses", {})

    ids = session.get("test_ids")
    if not ids:
        return jsonify({"error": "Session de test expirée. Relancez le test."}), 400

    score = 0
    par_chapitre = {}
    details = []

    for qid in ids:
        q = QUESTION_BY_ID.get(qid)
        if not q:
            continue
        # La réponse peut être un entier (réponse unique) ou une liste (multi).
        raw = reponses.get(qid)
        if isinstance(raw, (list, tuple)):
            choix = set()
            for x in raw:
                try:
                    choix.add(int(x))
                except (TypeError, ValueError):
                    pass
        elif raw is None or raw == "":
            choix = set()
        else:
            try:
                choix = {int(raw)}
            except (TypeError, ValueError):
                choix = set()

        corrects = set(q["corrects"])
        juste = (choix == corrects)
        if juste:
            score += 1

        chap = q["chapitre_titre"]
        s = par_chapitre.setdefault(chap, {"ok": 0, "total": 0})
        s["total"] += 1
        if juste:
            s["ok"] += 1

        detail = {
            "id": qid,
            "q": q["q"],
            "options": q["options"],
            "choix": sorted(choix),
            "multi": q["multi"],
            "juste": juste,
            "chapitre_titre": q["chapitre_titre"],
            "chapitre_slug": q["chapitre_slug"],
        }
        if mode == "blanc":
            detail["corrects"] = q["corrects"]
            detail["explication"] = q["explication"]
        details.append(detail)

    total = len(ids)
    note20 = round(score / total * 20, 1) if total else 0

    # Sauvegarde du résultat pour l'utilisateur connecté.
    saved = False
    if current_user.is_authenticated:
        db.session.add(TestResult(
            user_id=current_user.id, mode=mode,
            score=score, total=total, note20=note20,
        ))
        db.session.commit()
        saved = True

    resultat = {
        "mode": mode,
        "score": score,
        "total": total,
        "note20": note20,
        "par_chapitre": par_chapitre,
        "saved": saved,
        "authenticated": current_user.is_authenticated,
    }
    if mode == "blanc":
        resultat["details"] = details

    return jsonify(resultat)


# ---------------------------------------------------------------------------
# Divers
# ---------------------------------------------------------------------------

@app.route("/question/<qid>/commentaire", methods=["POST"])
def commentaire_question(qid):
    """Enregistre une remarque d'utilisateur sur une question (test blanc)."""
    q = QUESTION_BY_ID.get(qid)
    if not q:
        return jsonify({"error": "Question inconnue."}), 404
    data = request.get_json(silent=True) or {}
    texte = (data.get("comment") or "").strip()
    if not texte:
        return jsonify({"error": "Commentaire vide."}), 400
    texte = texte[:1000]
    db.session.add(QuestionComment(
        question_id=qid,
        question_text=q["q"],
        user_id=current_user.id if current_user.is_authenticated else None,
        pseudo=current_user.pseudo if current_user.is_authenticated else "Anonyme",
        comment=texte,
    ))
    db.session.commit()
    return jsonify({"ok": True})


@app.context_processor
def inject_globals():
    return {
        "chapitres_nav": CHAPITRES,
        "user_is_admin": is_admin(),
        "species_photo_url": species_photo_url,
        "species_emoji": lambda cat: CATEGORY_EMOJI.get(cat, "🌊"),
        "signal_by_key": SIGNAL_BY_KEY,
    }


@app.errorhandler(404)
def page_introuvable(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def acces_refuse(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
