# -*- coding: utf-8 -*-
"""
Reconnaissance automatique d'espèces sur les photos de la communauté.

Le backend est *enfichable* et **désactivé par défaut** : sans configuration,
`identify()` renvoie None et l'utilisateur choisit / propose l'espèce à la main.

Backend « vision » (optionnel, activé en production) :
  - Défini une clé ANTHROPIC_API_KEY dans l'environnement.
  - On interroge alors l'API Messages de Claude (capacité vision) pour proposer
    une espèce à partir de l'image.
Le résultat n'est **jamais** accepté aveuglément : une espèce nouvelle reste
« en attente de validation » par un administrateur (Species.validated=False),
et l'utilisateur peut toujours corriger la proposition.

Variables d'environnement :
  ANTHROPIC_API_KEY   clé API (active la reconnaissance)
  VISION_ENABLED      "0" pour désactiver même si une clé est présente
  VISION_MODEL        modèle vision à utiliser (défaut : claude-3-5-sonnet-latest)
  VISION_MIN_CONFIDENCE  seuil de confiance (défaut : 0.55)
"""

import os
import io
import json
import base64
import logging
import urllib.request

log = logging.getLogger(__name__)

API_URL = "https://api.anthropic.com/v1/messages"
_TIMEOUT = 20  # secondes


def enabled():
    """La reconnaissance automatique est-elle configurée et active ?"""
    if os.environ.get("VISION_ENABLED", "1").lower() in ("0", "false", "no"):
        return False
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def min_confidence():
    try:
        return float(os.environ.get("VISION_MIN_CONFIDENCE", "0.55"))
    except ValueError:
        return 0.55


def status():
    """État de la reconnaissance, pour l'affichage (admin & UI)."""
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    disabled_flag = os.environ.get("VISION_ENABLED", "1").lower() in ("0", "false", "no")
    if not has_key:
        raison = ("Aucune clé ANTHROPIC_API_KEY définie : la reconnaissance "
                  "automatique est désactivée.")
    elif disabled_flag:
        raison = "Désactivée via VISION_ENABLED=0."
    else:
        raison = "Activée."
    return {
        "enabled": enabled(),
        "has_key": has_key,
        "model": os.environ.get("VISION_MODEL", "claude-3-5-sonnet-latest"),
        "min_confidence": min_confidence(),
        "reason": raison,
    }


def identify(image_bytes, mimetype="image/jpeg", known=None):
    """Propose une espèce pour une image.

    Retourne un dict {nom, nom_scientifique, categorie, confiance} ou None
    (backend indisponible, erreur, ou rien de reconnaissable).
    `known` : liste de noms d'espèces déjà au catalogue (aide au rapprochement).
    """
    if not enabled():
        return None
    try:
        return _identify_anthropic(image_bytes, mimetype, known or [])
    except Exception as exc:  # noqa: BLE001 — on ne casse jamais l'upload
        log.warning("Reconnaissance d'espèce indisponible : %s", exc)
        return None


def _identify_anthropic(image_bytes, mimetype, known):
    api_key = os.environ["ANTHROPIC_API_KEY"]
    model = os.environ.get("VISION_MODEL", "claude-3-5-sonnet-latest")

    b64 = base64.b64encode(image_bytes).decode("ascii")
    media_type = mimetype if mimetype in (
        "image/jpeg", "image/png", "image/webp", "image/gif") else "image/jpeg"

    liste = ", ".join(known) if known else "(catalogue vide)"
    consigne = (
        "Tu es un biologiste marin. Identifie l'espèce principale (animal ou "
        "végétal) visible sur cette photo sous-marine. Réponds UNIQUEMENT par un "
        "objet JSON, sans texte autour, au format :\n"
        '{\"nom\": \"nom commun en français\", \"nom_scientifique\": \"latin\", '
        '\"categorie\": \"poisson|invertébré|mollusque|crustacé|végétal|reptile|'
        'mammifère|autre\", \"confiance\": 0.0}\n'
        "La confiance est entre 0 et 1. Si ce n'est pas identifiable, mets "
        "confiance à 0. Si l'espèce correspond à l'une de celles déjà connues, "
        "reprends exactement le même nom. Espèces déjà connues : " + liste
    )

    payload = {
        "model": model,
        "max_tokens": 300,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64", "media_type": media_type, "data": b64}},
                {"type": "text", "text": consigne},
            ],
        }],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, method="POST", headers={
        "content-type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    })
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    # La réponse Messages : { content: [ { type: "text", text: "..." } ] }
    text = ""
    for block in body.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
    parsed = _extract_json(text)
    if not parsed:
        return None
    try:
        conf = float(parsed.get("confiance", 0) or 0)
    except (TypeError, ValueError):
        conf = 0.0
    nom = (parsed.get("nom") or "").strip()
    if not nom or conf <= 0:
        return None
    return {
        "nom": nom[:120],
        "nom_scientifique": (parsed.get("nom_scientifique") or "").strip()[:160] or None,
        "categorie": (parsed.get("categorie") or "autre").strip()[:40],
        "confiance": max(0.0, min(1.0, conf)),
    }


def _extract_json(text):
    """Extrait le premier objet JSON d'une chaîne (robuste aux ``` et au bruit)."""
    if not text:
        return None
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None
