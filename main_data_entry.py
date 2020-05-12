from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from util.message import message
import util.utilities as ut


app = Flask(__name__)

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('data.html', form=form)




# def event_form() :
#
#     message.logDebug("Form launched", "main::main")
#
#     return app


def main():
    '''
    This will run the specified components
    '''
    # app = event_form()

    # Debugger allows arbitrary execution
    app.debug = False
    app.run(host='0.0.0.0')


    #app.start()
    # login_manager = LoginManager()
    # login_manager.init_app(app)


if __name__ == "__main__":
    main()
    ut.exit(1)
