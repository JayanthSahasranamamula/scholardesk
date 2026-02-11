from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=20)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")

from wtforms import TextAreaField


class NoteForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=100)]
    )

    subject = StringField(
        "Subject",
        validators=[DataRequired(), Length(max=50)]
    )

    tags = StringField(
        "Tags (comma separated)"
    )

    resource_link = StringField(
        "Resource Link"
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")
