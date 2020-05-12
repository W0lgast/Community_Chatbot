from flask import Flask, render_template, request, session
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SelectField, SubmitField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

from util.message import message
import util.utilities as ut
import os

# Get password from gitignored file
with open("data/creds.txt") as f :
    PASSWORD = f.readline()


app = Flask(__name__)
loginMan = LoginManager(app)


# Arbitrary secret key for csrf
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
ADMIN = "kwmc_admin"
GENRES = [("m", "Music"),
          ("c", "Comedy"),
          ("t", "Theatre"),
          ("s", "Shows & Events"),
          ("e", "Exercise"),
          ("o", "Outdoors"),
          ("ca", "Cafe"),
          ("coo", "Cooking"),
          ("a", "Art")]

# Single user
class User(UserMixin):
    def __init__(self):
        #self.id = 1
        self.username = ADMIN
        self.password = generate_password_hash(PASSWORD, method='sha256')

    def get_id(self):
        return self.username

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


@loginMan.user_loader
def load_user(user_id):
    return User()


class LoginForm(FlaskForm):
    password = StringField('password', validators=[DataRequired()])
    username = HiddenField(ADMIN)
    submit = SubmitField('Log In')


class DataForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    url = StringField('url')
    genre = SelectField('genre', choices=GENRES)
    submit = SubmitField('send')


@app.route('/')
def home() :
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/data")
    form = LoginForm()
    user = load_user(request.values.get('username'))
    if user.check_password(password=form.password.data):
        login_user(user)
        return redirect('/data')

    return render_template('login.html', form=form)


@app.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    form = DataForm()
    if form.validate_on_submit():
        if request.method == "POST":
            print(request.form.title)
        render_template('success.html')

    return render_template('data.html', form=form)


# @loginMan.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash('You must be logged in to view that page.')
#     return redirect('/login')


@app.route('/submit', methods=('GET', 'POST'))
def submit():

    return render_template('data.html')



def main():
    # Disable debugger; otherwise allows arbitrary execution
    app.debug = False
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
    ut.exit(1)
