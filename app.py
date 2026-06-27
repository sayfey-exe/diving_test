# -*- coding: utf-8 -*-
"""
Plongée N2 — Application de révision (FFESSM / tables MN90).

Application web Flask permettant aux élèves Niveau 2 de réviser :
  - des fiches de cours (résumé par chapitre + 3 questions d'auto-évaluation)
  - un "test blanc" (40 QCM avec correction détaillée, navigation libre)
  - un "test examen" (40 QCM chronométrés, sans correction)
  - des astuces pour réussir l'examen
"""

import os
import random

from flask import (
    Flask, render_template, abort, request, jsonify, session, url_for, redirect
)

from data.content import CHAPITRES, ASTUCES
from data.questions import QUESTION_BANK, QUESTION_BY_ID

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "plongee-n2-dev-secret-change-me")

NB_QUESTIONS_TEST = 40
DUREE_EXAMEN_MIN = 40  # minutes pour le mode examen

CHAPITRE_BY_SLUG = {c["slug"]: c for c in CHAPITRES}


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
    return render_template("cours.html", chapitres=CHAPITRES)


@app.route("/cours/<slug>")
def chapitre(slug):
    chap = CHAPITRE_BY_SLUG.get(slug)
    if not chap:
        abort(404)
    idx = CHAPITRES.index(chap)
    precedent = CHAPITRES[idx - 1] if idx > 0 else None
    suivant = CHAPITRES[idx + 1] if idx < len(CHAPITRES) - 1 else None
    return render_template(
        "chapitre.html", chap=chap, precedent=precedent, suivant=suivant
    )


@app.route("/astuces")
def astuces():
    return render_template("astuces.html", astuces=ASTUCES)


# ---------------------------------------------------------------------------
# Tests (blanc / examen)
# ---------------------------------------------------------------------------

def _tirer_questions(n):
    """Tire n questions aléatoires distinctes de la banque."""
    n = min(n, len(QUESTION_BANK))
    return random.sample(QUESTION_BANK, n)


def _questions_pour_client(questions):
    """Version des questions envoyée au navigateur : sans la bonne réponse."""
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
    # On mémorise les IDs servis pour scorer côté serveur (anti-triche pour l'examen).
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
    reponses = data.get("reponses", {})  # {question_id: index_choisi}

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
        stats = par_chapitre.setdefault(chap, {"ok": 0, "total": 0})
        stats["total"] += 1
        if juste:
            stats["ok"] += 1

        detail = {
            "id": qid,
            "q": q["q"],
            "options": q["options"],
            "choix": choix,
            "juste": juste,
            "chapitre_titre": q["chapitre_titre"],
            "chapitre_slug": q["chapitre_slug"],
        }
        # On ne révèle la correction que pour le test blanc.
        if mode == "blanc":
            detail["correct"] = q["correct"]
            detail["explication"] = q["explication"]
        details.append(detail)

    total = len(ids)
    note20 = round(score / total * 20, 1) if total else 0

    resultat = {
        "mode": mode,
        "score": score,
        "total": total,
        "note20": note20,
        "par_chapitre": par_chapitre,
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
