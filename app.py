# -*- coding: utf-8 -*-
"""
Plongée N2 — Application de révision (FFESSM / tables MN90).

Application web Flask permettant aux élèves Niveau 2 de réviser :
  - des fiches de cours (résumé par chapitre, images, exercices corrigés
    et 3 questions d'auto-évaluation)
  - un "test blanc" (40 QCM avec correction détaillée, navigation libre)
  - un "test examen" (40 QCM chronométrés, sans correction)
  - des astuces pour réussir l'examen
  - un compte personnel : suivi des chapitres étudiés et historique des tests
"""

import os
import ssl
import smtplib
import logging
from email.message import EmailMessage

from flask import (
    Flask, render_template, abort, request, jsonify, session,
    redirect, url_for, flash,
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user,
)
from functools import wraps
from sqlalchemy import func
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from data.content import CHAPITRES, HINTS, PASCAL
from data.questions import QUESTION_BANK, QUESTION_BY_ID
from data.exercices import EXERCICES, NOTE_TABLES
from models import db, User, TestResult, ChapterStudy, QuestionComment

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "plongee-n2-dev-secret-change-me")

# Base de données : PostgreSQL en production (DATABASE_URL), SQLite en local.
db_url = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "diving.db"))
if db_url.startswith("postgres://"):  # compat anciens schémas Heroku/Render
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "").lower() in ("1", "true", "yes")

reset_serializer = URLSafeTimedSerializer(app.secret_key, salt="password-reset")
RESET_MAX_AGE = 3600  # 1 heure


def mail_configured():
    return bool(MAIL_SERVER and MAIL_USERNAME and MAIL_PASSWORD)


def send_email(destinataire, sujet, corps):
    """Envoie un e-mail. Retourne True si envoyé, False sinon (et journalise)."""
    if not mail_configured():
        app.logger.warning(
            "E-mail non configuré (MAIL_SERVER/MAIL_USERNAME/MAIL_PASSWORD). "
            "Message destiné à %s NON envoyé. Contenu :\n%s", destinataire, corps,
        )
        return False
    msg = EmailMessage()
    msg["Subject"] = sujet
    msg["From"] = MAIL_SENDER
    msg["To"] = destinataire
    msg.set_content(corps)
    try:
        ctx = ssl.create_default_context()
        if MAIL_USE_SSL:
            with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=ctx) as s:
                s.login(MAIL_USERNAME, MAIL_PASSWORD)
                s.send_message(msg)
        else:
            with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as s:
                s.starttls(context=ctx)
                s.login(MAIL_USERNAME, MAIL_PASSWORD)
                s.send_message(msg)
        return True
    except Exception as exc:  # noqa: BLE001 (on journalise toute erreur SMTP)
        app.logger.error("Échec d'envoi d'e-mail à %s : %s", destinataire, exc)
        return False


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


with app.app_context():
    db.create_all()


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


@app.route("/cours")
def cours():
    studied = _studied_slugs()
    return render_template("cours.html", chapitres=CHAPITRES, studied=studied)


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

        user = User(email=email, pseudo=pseudo)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Bienvenue %s ! Ton compte est créé." % pseudo, "success")
        return redirect(url_for("profil"))

    return render_template("inscription.html")


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
        return render_template("connexion.html", email=email)
    return render_template("connexion.html")


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
                "Tu as demandé à réinitialiser ton mot de passe sur Plongée N2.\n"
                "Clique sur ce lien (valable 1 heure) pour choisir un nouveau "
                "mot de passe :\n\n%s\n\n"
                "Si tu n'es pas à l'origine de cette demande, ignore cet e-mail."
                % (user.pseudo, lien)
            )
            envoye = send_email(
                user.email,
                "Réinitialisation de ton mot de passe — Plongée N2",
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
    return render_template("admin.html", rows=rows, totaux=totaux, nb_comment=nb_comment)


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
    return {"chapitres_nav": CHAPITRES, "user_is_admin": is_admin()}


@app.errorhandler(404)
def page_introuvable(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def acces_refuse(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
