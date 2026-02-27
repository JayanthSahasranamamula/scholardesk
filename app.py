from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Note, Tag
from forms import (
    RegistrationForm,
    LoginForm,
    NoteForm,
    UpdateProfileForm,
    ChangePasswordForm
)
from extensions import db, bcrypt, login_manager
from sqlalchemy import or_
import os

app = Flask(__name__)

# =====================
# Configuration
# =====================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key"
)

database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# =====================
# Initialise Extensions
# =====================

db.init_app(app)
bcrypt.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =====================
# Home
# =====================

@app.route("/")
def home():
    return render_template("index.html")


# =====================
# Notes (Search + Relational Tag Filtering)
# =====================

@app.route("/notes")
@login_required
def notes():

    search_query = request.args.get("q")
    subject_filter = request.args.get("subject")
    tag_filter = request.args.get("tag")

    query = Note.query.filter_by(user_id=current_user.id)

    if search_query:
        query = query.filter(
            or_(
                Note.title.ilike(f"%{search_query}%"),
                Note.content.ilike(f"%{search_query}%")
            )
        )

    if subject_filter:
        query = query.filter(
            Note.subject.ilike(f"%{subject_filter}%")
        )

    if tag_filter:
        query = query.join(Note.tags).filter(
            Tag.name.ilike(f"%{tag_filter.lower()}%")
        )

    filtered_notes = query.distinct().all()

    return render_template(
        "notes.html",
        notes=filtered_notes
    )


# =====================
# Authentication
# =====================

@app.route("/register", methods=["GET", "POST"])
def register():

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            registration_form.password.data
        ).decode("utf-8")

        new_user = User(
            username=registration_form.username.data,
            email=registration_form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created! You can now log in.", "success")

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=registration_form
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=login_form.email.data
        ).first()

        if existing_user and bcrypt.check_password_hash(
            existing_user.password,
            login_form.password.data
        ):

            login_user(existing_user)
            return redirect(url_for("home"))

        flash("Login failed. Check email and password.", "danger")

    return render_template(
        "login.html",
        form=login_form
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    update_form = UpdateProfileForm(
        obj=current_user
    )

    password_form = ChangePasswordForm()

    # Handle profile update
    if update_form.submit.data and update_form.validate_on_submit():

        current_user.username = update_form.username.data
        current_user.email = update_form.email.data

        db.session.commit()

        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    # Handle password change
    if password_form.submit.data and password_form.validate_on_submit():

        if bcrypt.check_password_hash(
            current_user.password,
            password_form.current_password.data
        ):

            new_hashed_password = bcrypt.generate_password_hash(
                password_form.new_password.data
            ).decode("utf-8")

            current_user.password = new_hashed_password
            db.session.commit()

            flash("Password updated successfully.", "success")
            return redirect(url_for("profile"))

        else:
            flash("Current password is incorrect.", "danger")

    return render_template(
        "profile.html",
        update_form=update_form,
        password_form=password_form
    )

@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():

    db.session.delete(current_user)
    db.session.commit()

    flash("Your account has been deleted.", "info")

    return redirect(url_for("home"))

# =====================
# Notes CRUD
# =====================

@app.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():

    note_form = NoteForm()

    if note_form.validate_on_submit():

        new_note = Note(
            title=note_form.title.data,
            content=note_form.content.data,
            subject=note_form.subject.data,
            resource_link=note_form.resource_link.data,
            user=current_user
        )

        # Process tags (many-to-many)
        tag_names = note_form.tags.data.split(",")

        for name in tag_names:
            clean_name = name.strip().lower()

            if clean_name:
                tag = Tag.query.filter_by(name=clean_name).first()

                if not tag:
                    tag = Tag(name=clean_name)
                    db.session.add(tag)

                new_note.tags.append(tag)

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("notes"))

    return render_template(
        "note_form.html",
        form=note_form,
        legend="New Note"
    )


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):

    existing_note = Note.query.get_or_404(note_id)

    if existing_note.user != current_user:
        return redirect(url_for("notes"))

    note_form = NoteForm(obj=existing_note)

    if note_form.validate_on_submit():

        existing_note.title = note_form.title.data
        existing_note.content = note_form.content.data
        existing_note.subject = note_form.subject.data
        existing_note.resource_link = note_form.resource_link.data

        # Clear existing tags
        existing_note.tags.clear()

        tag_names = note_form.tags.data.split(",")

        for name in tag_names:
            clean_name = name.strip().lower()

            if clean_name:
                tag = Tag.query.filter_by(name=clean_name).first()

                if not tag:
                    tag = Tag(name=clean_name)
                    db.session.add(tag)

                existing_note.tags.append(tag)

        db.session.commit()

        return redirect(url_for("notes"))

    # Prepopulate tags field as comma string
    note_form.tags.data = ", ".join(tag.name for tag in existing_note.tags)

    return render_template(
        "note_form.html",
        form=note_form,
        legend="Edit Note"
    )


@app.route("/notes/<int:note_id>/delete")
@login_required
def delete_note(note_id):

    existing_note = Note.query.get_or_404(note_id)

    if existing_note.user != current_user:
        return redirect(url_for("notes"))

    db.session.delete(existing_note)
    db.session.commit()

    return redirect(url_for("notes"))


# =====================
# API Endpoints
# =====================

@app.route("/api/user")
@login_required
def api_user():

    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    })


@app.route("/api/notes")
@login_required
def api_notes():

    user_notes = Note.query.filter_by(
        user_id=current_user.id
    ).all()

    serialized_notes = []

    for note in user_notes:
        serialized_notes.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "subject": note.subject,
            "tags": [tag.name for tag in note.tags],
            "resource_link": note.resource_link
        })

    return jsonify(serialized_notes)


# =====================
# Database Initialisation
# =====================

with app.app_context():
    db.create_all()