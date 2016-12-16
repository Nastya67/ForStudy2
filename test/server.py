import flask
from flask import Flask, flash, render_template, redirect, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
import wtforms
from wtforms.validators import Required, EqualTo
import json
from flask import request
import postgresql
import random
import string
import base64
import hashlib
from werkzeug.utils import secure_filename
import os
import binascii

class Log_out(FlaskForm):
    logout = wtforms.SubmitField("Log out", name = "first")

class Vhod(FlaskForm):
    submit = wtforms.SubmitField('OK')

class Reg(FlaskForm):
    submit = wtforms.SubmitField('OK')

WTF_CSRF_SECRET_KEY = 'qpwoeiruty'

app = Flask(__name__)
app.secret_key = 'qpwoeiruty'
csrf = CsrfProtect(app)

@app.route("/<id>", methods=['GET', 'POST'])
def index(id):
    form = []
    form1 = Log_out()
    form2 = Reg()
    form3 = Vhod()
    if request.method == 'GET':
        return render_template("str.html", form1 = form1,
        form2= form2)
    elif request.method == "POST":
        if form1.validate_on_submit() and request.form.get("first"):
            return"23"
        if form2.validate_on_submit():
            return"1"
        if form3.validate_on_submit():
            return"2"

if __name__ == "__main__":
    app.run(debug=True)
