
from flask import Flask, request, session, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_homepage():
  """ Redirects to/register """

  return redirect("/register")

@app.route("/register", methods =['GET','POST'])
def register_form():
  """Produces a form for registering a new user"""

  form = RegisterUserForm()

  if form.validate_on_submit():
      data = {k: v for k, v in form.data.items() if k != "csrf_token"}
      new_user = User(**data)

      db.session.add(new_user)
      db.session.commit()

      session["user_id"] = new_user.id

      return redirect("/secret")

  else:
      return render_template("user_registration.html", form=form)

mxjung

    
