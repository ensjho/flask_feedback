
from flask import Flask, request, session, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():
    """ Redirects to/register """

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def register_form():
    """Produces a form for registering a new user"""

    form = RegisterUserForm()

    if form.validate_on_submit():
        # data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        # new_user = User(**data)

        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_username"] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("user_registration.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_form():
    """Produces a form for login user"""

    form = LoginUserForm()

    if form.validate_on_submit():
        # data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user_name = form.username.data
        user_password = form.password.data

        user = User.authenticate(user_name, user_password)

        if user:
            session["user_username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")
            # return redirect('/secret')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("user_login.html", form=form)


@app.route("/users/<username>")
def user_login(username):

    # if "user_username" in session and session["user_username"] == username:
    #     user = User.query.get_or_404(username)
    #     return render_template('user_information.html', user=user)

    if "user_username" not in session or session["user_username"] != username:
        return redirect('/')

    user = User.query.get_or_404(username)
    return render_template('user_information.html', user=user)


@app.route("/secret")
def secret_form():
    """Produces a form for secret page"""

    if "user_username" not in session:
        return redirect('/')
    return render_template('secret.html')


@app.route("/logout")
def logout_form():
    """Logs user out and redirects to homepage"""

    session.pop("user_username")

    return redirect('/')
