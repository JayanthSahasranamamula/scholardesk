from extensions import db
from flask_login import UserMixin
from datetime import datetime

# Association table
note_tags = db.Table(
    "note_tags",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    notes = db.relationship(
        "Note",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    resource_link = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tags = db.relationship(
        "Tag",
        secondary=note_tags,
        backref=db.backref("notes", lazy="dynamic")
    )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)