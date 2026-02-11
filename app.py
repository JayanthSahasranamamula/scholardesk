from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Note
from forms import RegistrationForm, LoginForm, NoteForm
from flask_login import current_user


app = Flask(__name__)

# Config
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Init
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes

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

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created! You can now log in.", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("home"))

        else:
            flash("Login failed. Check email and password.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():

    form = NoteForm()

    if form.validate_on_submit():

        note = Note(
    title=form.title.data,
    content=form.content.data,
    subject=form.subject.data,
    tags=form.tags.data,
    resource_link=form.resource_link.data,
    user=current_user
)


        db.session.add(note)
        db.session.commit()

        return redirect(url_for("notes"))

    return render_template(
        "note_form.html",
        form=form,
        legend="New Note"
    )

@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):

    note = Note.query.get_or_404(note_id)

    if note.user != current_user:
        return redirect(url_for("notes"))

    form = NoteForm(obj=note)

    if form.validate_on_submit():

        note.title = form.title.data
        note.content = form.content.data
        note.subject = form.subject.data
        note.tags = form.tags.data
        note.resource_link = form.resource_link.data

        db.session.commit()

        return redirect(url_for("notes"))

    return render_template(
        "note_form.html",
        form=form,
        legend="Edit Note"
    )


@app.route("/notes/<int:note_id>/delete")
@login_required
def delete_note(note_id):

    note = Note.query.get_or_404(note_id)

    if note.user != current_user:
        return redirect(url_for("notes"))

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("notes"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
