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

arr_foto = {}

@app.route("/<id>", methods=['GET', 'POST'])
def index(id):
    form = []
    form.append(Add_foto())
    form.append(Create_point())
    user_inf = get_user_info(id)
    session['name'] = user_inf['name']
    session['surname'] = user_inf['surname']
    if request.method == 'GET':
        return render_template('userStr.html', user_data = session, form = form)
    else:
        if form[0].validate_on_submit():
            arr_foto = {}
            arr_foto[id] = form.foto.data
            return render_template('userStr.html', user_data = session, form = form, foto = arr_foto[id])
        elif form[1].validate_on_submit():
            a = []
        print(request.data)
        return 'Ok'

@app.route("/", methods=['GET', 'POST'])
def vhod():
    form = Vhod()
    print(form.errors)
    if form.validate_on_submit():
        user = select_where_log(form.login.data)
        if(hashlib.md5(form.password.data.encode('utf8')).hexdigest() == user['password']):
            user_inf = get_user_info(user['iduser'])
            session['name'] = user_inf['name']
            session['surname'] = user_inf['surname']
        else:
            return 'Ne OK'
        return redirect(url_for('index', id = user_inf['iduser']))
    return render_template('vhod.html', form = form, user_data = session)

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    form = Reg()
    if form.validate_on_submit() and (form.password.data == form.password2.data):
        id = constr_id()
        save_log(id, form.login.data, form.password.data)
        save_info(id, form)
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        return redirect(url_for('index', id = id))
    return render_template('reg.html', form = form)

def save_log(id, login, password):
     with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
         ins = db.prepare("INSERT INTO logpass VALUES ($1, $2, $3)")
         ins(id, hashlib.md5(password.encode('utf8')).hexdigest(), login.lower())

def select_where_log(login):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM logpass WHERE login = $1")
        users = sel(login.lower())
    return users[0]

def get_user_info(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM users WHERE iduser = $1")
        users = sel(id)
    return users[0]

def save_info(id, form):
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
