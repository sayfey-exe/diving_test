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

from flask import (
    Flask, render_template, abort, request, jsonify, session,
    redirect, url_for, flash,
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user,
)

from data.content import CHAPITRES, ASTUCES
from data.questions import QUESTION_BANK, QUESTION_BY_ID
from data.exercices import EXERCICES, NOTE_TABLES
from models import db, User, TestResult, ChapterStudy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "plongee-n2-dev-secret-change-me")

# Base de données : PostgreSQL en production (DATABASE_URL), SQLite en local.
db_url = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "diving.db"))
if db_url.startswith("postgres://"):  # compat anciens schémas Heroku/Render
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "connexion"
login_manager.login_message = "Connecte-toi pour accéder à ton espace personnel."

NB_QUESTIONS_TEST = 40
DUREE_EXAMEN_MIN = 40  # minutes pour le mode examen

CHAPITRE_BY_SLUG = {c["slug"]: c for c in CHAPITRES}


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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
    )


@app.route("/astuces")
def astuces():
    return render_template("astuces.html", astuces=ASTUCES)


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

    # Statistiques synthétiques
    stats = {
        "nb_tests": len(results),
        "nb_chap_etudies": len(studied),
        "nb_chap_total": len(CHAPITRES),
        "meilleure_note": max((r.note20 for r in results), default=None),
        "moyenne": round(sum(r.note20 for r in results) / len(results), 1) if results else None,
    }
    return render_template(
        "profil.html",
        results=results,
        studied=studied,
        chapitres=CHAPITRES,
        stats=stats,
    )


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


# ---------------------------------------------------------------------------
# Tests (blanc / examen)
# ---------------------------------------------------------------------------

import random  # noqa: E402  (après config pour rester lisible)


def _tirer_questions(n):
    n = min(n, len(QUESTION_BANK))
    return random.sample(QUESTION_BANK, n)


def _questions_pour_client(questions):
    return [
        {
            "id": q["id"],
            "q": q["q"],
            "options": q["options"],
            "chapitre_titre": q["chapitre_titre"],
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
        choix = reponses.get(qid)
        try:
            choix = int(choix)
        except (TypeError, ValueError):
            choix = None
        juste = (choix == q["correct"])
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
            "choix": choix,
            "juste": juste,
            "chapitre_titre": q["chapitre_titre"],
            "chapitre_slug": q["chapitre_slug"],
        }
        if mode == "blanc":
            detail["correct"] = q["correct"]
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

@app.context_processor
def inject_globals():
    return {"chapitres_nav": CHAPITRES}


@app.errorhandler(404)
def page_introuvable(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
