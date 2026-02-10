from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

from models import db, User
from forms import RegistrationForm, LoginForm


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
