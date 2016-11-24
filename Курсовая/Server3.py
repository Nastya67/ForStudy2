from flask import Flask, render_template, redirect, session, url_for
from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Required
import json
from flask import request
import postgresql
import random
from base64 import b64decode
import hashlib

class Vhod(FlaskForm):
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.StringField('Password', validators=[Required()])
    submit = wtforms.SubmitField('OK')

class Reg(FlaskForm):
    name = wtforms.StringField("Name", validators=[Required()])
    surname = wtforms.StringField("Surname", validators=[Required()])
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.PasswordField("Your password", validators=[Required()])
    password2 = wtforms.PasswordField("Repeat your password", validators=[Required()])
    bday = wtforms.SelectField('Day', choices=[(str(i), i) for i in range(1, 32)])
    bmonth = wtforms.SelectField('Month', choices=[(str(i), i) for i in range(1,13)])
    byear = wtforms.SelectField('Year', choices=[(str(i), i) for i in range(1916, 2016)])
    submit = wtforms.SubmitField('OK')

class Add_foto(FlaskForm):
    foto = wtforms.FileField("Avatar")
    submit = wtforms.SubmitField('Change Photo')

class Create_point(FlaskForm):
    Text = wtforms.TextField('Text')
    submit = wtforms.SubmitField('Create new popinter')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'
count = 100
alfas = 'QWERTYUIOPASDFGHJKLZXCVBNM'
alfa_count1 = 0
alfa_count2 = 0
alfa_count3 = 0

@app.route("/api/<id>")
def api_index_id(id):
    user_inf = select_from_users_where_id(id)


def insert_into_logpass(id, login, password):
     with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
         ins = db.prepare("INSERT INTO logpass VALUES ($1, $2, $3)")
         ins(id, hashlib.md5(password.encode('utf8')).hexdigest(), login.lower())

def select_from_logpass_where_log(login):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM logpass WHERE login = $1")
        users = sel(login.lower())
    return users[0]

def select_from_users_where_id(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM users WHERE iduser = $1")
        users = sel(id)
    return users[0]

def insert_into_users(id, form):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        ins = db.prepare("INSERT INTO users VALUES ($1, $2, $3, $4, $5, $6, $7)")
        ins(id, form.name.data, form.surname.data, int(form.bday.data), int(form.bmonth.data),
        int(form.byear.data), 1)

def constr_id():
    global count, alfas, alfa_count1, alfa_count2, alfa_count3
    id = str(count) + alfas[alfa_count1] + alfas[alfa_count2] + alfas[alfa_count3]
    alfa_count3 +=1
    if alfa_count3 == len(alfas):
        alfa_count3 = 0
        alfa_count2 +=1
        if alfa_count2 == len(alfas):
            alfa_count2 = 0
            alfa_count1 +=1
            if alfa_count1 == len(alfas):
                alfa_count1 = 0
                count +=1
    return id


if __name__ == "__main__":
    app.run(debug=True)
