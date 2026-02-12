from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from models import User, Note
from forms import RegistrationForm, LoginForm, NoteForm
from extensions import db, bcrypt, login_manager


app = Flask(__name__)

# =====================
# Configuration
# =====================

app.config["SECRET_KEY"] = "dev-secret-key"
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
# Main Routes
# =====================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/notes")
@login_required
def notes():
    user_notes = Note.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "notes.html",
        notes=user_notes
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
            tags=note_form.tags.data,
            resource_link=note_form.resource_link.data,
            user=current_user
        )

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
        existing_note.tags = note_form.tags.data
        existing_note.resource_link = note_form.resource_link.data

        db.session.commit()

        return redirect(url_for("notes"))

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

    current_user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

    return jsonify(current_user_data)


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
            "tags": note.tags,
            "resource_link": note.resource_link
        })

    return jsonify(serialized_notes)


# =====================
# App Runner
# =====================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)