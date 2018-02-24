from Engine import Engine
from reinitdb import rebuildDb
from os import system

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ver.bai.tas.unt.int.ell.ige.nda.utr.esm.agi.sva.lea.tqu.amp.ere.at'
bootstrap = Bootstrap(app)
moment = Moment(app)

engine = Engine()

from Switch import Switch

class NameForm(FlaskForm):
    gpio = StringField('Toggle GPIO', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/on')
def on_light():
    engine.gpioList[2].setState(Switch.e_state.On)
    return render_template('index.html', form=NameForm(), name=None)

@app.route('/off')
def off_light():
    engine.gpioList[2].setState(Switch.e_state.Off)
    return render_template('index.html', form=NameForm(), name=None)

@app.route('/setgpio')
def set_gpio():
    gpioNum = request.args.get('gpioNum')
    value = request.args.get('value')
    for gpio in engine.gpioList:
        if gpio.getGpio() == int(gpioNum):
            gpio.setState(value)
    return render_template('index.html', form=NameForm(), name=None)

@app.route('/setpwm')
def set_pwm():
    gpioNum = int(request.args.get('gpioNum'))
    value = int(request.args.get('value'))
    for gpio in engine.gpioList:
        if gpio.getGpio() == gpioNum:
            gpio.setDutyCycle(value)
    return render_template('index.html', form=NameForm(), name=None)



@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

def main():
    system("sudo pigpiod")
    rebuildDb()
    engine.start()
    #engine.join()



    app.run()

if __name__ == "__main__":
    main()