
from flask import Flask, request, session, render_template, redirect
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

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
    # breakpoint()

    if "user_username" not in session or session["user_username"] != username:
        return redirect('/')

    user = User.query.get_or_404(username)
    feedbacks = user.feedbacks
    return render_template('user_information.html', user=user, feedbacks=feedbacks)


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


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete the user from the db and redirect to "/" """

    if "user_username" not in session or session["user_username"] != username:
        return redirect('/')

    # Make sure to delete feedbacks first, since feedbacks are tied to users (ForeignKey)
    user = User.query.get_or_404(username)
    Feedback.query.filter(Feedback.username == username).delete()

    db.session.delete(user)

    db.session.commit()
    session.pop("user_username")

    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def feedback_form(username):
    """Display a form to add feedback."""

    if "user_username" not in session or session["user_username"] != username:
        return redirect('/')

    user = User.query.get_or_404(username)
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{user.username}")

    return render_template("new_feedback.html", form=form, user=user)


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Update the feedback from the db"""
    
    feedback = Feedback.query.get_or_404(feedback_id)
    if "user_username" not in session or session["user_username"] != feedback.user.username:
        return redirect('/')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.user.username}")

    return render_template("update_feedback.html", feedback=feedback, form=form)


@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete the feedback from the db and redirect to "/" """
    feedback = Feedback.query.get_or_404(feedback_id)

    if "user_username" not in session or session["user_username"] != feedback.user.username:
        return redirect('/')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.user.username}")