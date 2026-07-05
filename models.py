# -*- coding: utf-8 -*-
"""Modèles de données : utilisateurs, résultats de tests, chapitres étudiés."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    pseudo = db.Column(db.String(80), nullable=False)
    # Nullable : les comptes créés via Google/Facebook n'ont pas de mot de passe.
    password_hash = db.Column(db.String(255), nullable=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    oauth_provider = db.Column(db.String(20))   # "google" | "facebook" | None
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Profil public / social
    bio = db.Column(db.Text)
    niveau = db.Column(db.String(40))           # ex. N1, N2, N3, Guide de palanquée…
    ville = db.Column(db.String(80))            # ville / région du plongeur
    profile_public = db.Column(db.Boolean, default=True, nullable=False)

    results = db.relationship(
        "TestResult", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    studies = db.relationship(
        "ChapterStudy", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def has_password(self):
        return bool(self.password_hash)


class TestResult(db.Model):
    __tablename__ = "test_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    mode = db.Column(db.String(20), nullable=False)       # "blanc" | "examen"
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    note20 = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class QuestionComment(db.Model):
    """Remarque d'un utilisateur sur une question (pour améliorer la banque)."""
    __tablename__ = "question_comments"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(40), nullable=False, index=True)
    question_text = db.Column(db.Text)            # libellé au moment du commentaire
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    pseudo = db.Column(db.String(80))             # pseudo (ou « Anonyme »)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Spot(db.Model):
    """Spot de plongée (pré-défini ou ajouté par un utilisateur)."""
    __tablename__ = "spots"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False, index=True)
    nom = db.Column(db.String(120), nullable=False)
    lieu = db.Column(db.String(160))
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    profondeur = db.Column(db.String(40))
    description = db.Column(db.Text)
    poissons = db.Column(db.String(400))            # clés de poissons, séparées par des virgules
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    pseudo = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def fish_keys(self):
        return [k for k in (self.poissons or "").split(",") if k]

    @property
    def user_created(self):
        return self.created_by is not None


class SpotComment(db.Model):
    """Commentaire d'un utilisateur sur un spot."""
    __tablename__ = "spot_comments"

    id = db.Column(db.Integer, primary_key=True)
    spot_key = db.Column(db.String(80), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    pseudo = db.Column(db.String(80))
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SpotPhoto(db.Model):
    """Photo de poisson ajoutée par un utilisateur sur un spot de plongée."""
    __tablename__ = "spot_photos"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.String(60), nullable=False, index=True)
    fish_key = db.Column(db.String(40))          # poisson identifié (optionnel)
    caption = db.Column(db.String(300))
    mimetype = db.Column(db.String(40), default="image/jpeg")
    data = db.Column(db.LargeBinary, nullable=False)   # image redimensionnée
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    pseudo = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Species(db.Model):
    """Espèce du guide de la vie sous-marine (poisson, invertébré, végétal…).

    Les espèces de référence (source="seed") sont validées d'office. La
    communauté et la reconnaissance automatique des photos peuvent proposer de
    nouvelles espèces : elles restent `validated=False` jusqu'à validation admin.
    """
    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(60), unique=True, nullable=False, index=True)
    nom = db.Column(db.String(120), nullable=False)
    nom_scientifique = db.Column(db.String(160))
    categorie = db.Column(db.String(40), default="poisson")
    description = db.Column(db.Text)
    habitat = db.Column(db.String(200))
    taille = db.Column(db.String(80))
    image = db.Column(db.String(120))                  # fichier static/img (référence)
    photo_id = db.Column(db.Integer)                   # à défaut, photo communautaire illustrante
    # Photo de référence téléversée par un admin (prioritaire). Différée pour ne
    # pas charger le blob à chaque listing du catalogue.
    image_mimetype = db.Column(db.String(40))
    image_data = deferred(db.Column(db.LargeBinary))
    signal_key = db.Column(db.String(60))              # signe de plongée associé (data/signals)
    validated = db.Column(db.Boolean, default=True, index=True)
    source = db.Column(db.String(40), default="seed")  # seed | communauté | reconnaissance
    confidence = db.Column(db.Float)                   # confiance de reconnaissance (0–1)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    pseudo = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def desc(self):            # compat templates historiques (fish[k].desc)
        return self.description


class DiveLog(db.Model):
    """Entrée du carnet de plongée d'un utilisateur."""
    __tablename__ = "dive_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    date = db.Column(db.Date)
    spot_key = db.Column(db.String(80))       # lien facultatif vers un Spot de la carte
    spot_nom = db.Column(db.String(160))      # nom libre du site
    profondeur_max = db.Column(db.Float)      # mètres
    duree_min = db.Column(db.Integer)         # minutes
    temp_eau = db.Column(db.Float)            # °C
    visibilite = db.Column(db.String(40))
    binome = db.Column(db.String(120))
    lestage = db.Column(db.String(40))
    gaz = db.Column(db.String(40))            # air, nitrox 32…
    ressenti = db.Column(db.Integer)          # 1 à 5
    notes = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True, nullable=False)  # visible dans le fil
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Follow(db.Model):
    """Relation d'abonnement : follower_id suit followed_id."""
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("follower_id", "followed_id", name="uq_follow"),
    )


class ChapterStudy(db.Model):
    __tablename__ = "chapter_studies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    chapter_slug = db.Column(db.String(80), nullable=False)
    studied_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "chapter_slug", name="uq_user_chapter"),
    )
