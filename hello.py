import pigpio
import sqlite3
import lxml

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from os import system

system("sudo pigpiod")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ver.bai.tas.unt.int.ell.ige.nda.utr.esm.agi.sva.lea.tqu.amp.ere.at'

bootstrap = Bootstrap(app)
moment = Moment(app)

pi = pigpio.pi()


class NameForm(FlaskForm):
    name = StringField('Test field', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/on')
def on_light():
    pi.write(6,1)
    return render_template('index.html')

@app.route('/off')
def off_light():
    pi.write(6,0)


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


app.run()