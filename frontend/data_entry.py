import flask
from flask_login import login_user, LoginManager, login_required
from urllib.parse import urlparse, urljoin
from flask import request, Flask, render_template

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField, URLField
from wtforms.validators import DataRequired

PORT = 8421
PASSWORD = "speech_was_nothing"

app = Flask(__name__)
login = LoginManager(app)


class MyForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    venue = StringField('venue', validators=[DataRequired()])
    date = DateField("startDate", validators=[DataRequired()])
    description = StringField("description")
    linkToImage = URLField("image")


# Only user
class User() :
    username = "KWMC"
    password = PASSWORD


@app.route('/')
@login_required
def data():
    return 'data'


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        login_user(User())

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
