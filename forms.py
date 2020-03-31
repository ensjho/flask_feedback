"""Forms for feedback app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, TextField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


class RegisterUserForm(FlaskForm):
    """Form for registering users."""
    username = StringField(
        "Username",
        validators=[InputRequired()],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )

    email = TextField(
        "Email",
        validators=[InputRequired()],
    )

    first_name = TextField(
        "first_name",
        validators=[InputRequired()],
    )
    last_name = TextField(
        "last_name",
        validators=[InputRequired()],
    )


class LoginUserForm(FlaskForm):
    """Form for logging in User"""

    username = StringField(
        "Username",
        validators=[InputRequired()],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )
