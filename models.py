# -*- coding: utf-8 -*-
"""Modèles de données : utilisateurs, résultats de tests, chapitres étudiés."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    pseudo = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship(
        "TestResult", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    studies = db.relationship(
        "ChapterStudy", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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


class ChapterStudy(db.Model):
    __tablename__ = "chapter_studies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    chapter_slug = db.Column(db.String(80), nullable=False)
    studied_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "chapter_slug", name="uq_user_chapter"),
    )
