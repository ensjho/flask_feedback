"""Forms for feedback app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, TextField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


class RegisterUserForm(FlaskForm):
    """Form for registering users."""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)],
    )

    email = TextField(
        "Email",
        validators=[InputRequired(), Length(max=50)],
    )

    first_name = TextField(
        "first_name",
        validators=[InputRequired(),Length(max=30) ],
    )
    last_name = TextField(
        "last_name",
        validators=[InputRequired(),Length(max=30)],
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

class FeedbackForm(FlaskForm):
    """Form for feedbacks"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )

    content = TextAreaField(
        "Content",
        validators=[InputRequired(), Length(max=500)],
    )
