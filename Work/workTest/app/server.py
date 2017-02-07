from flask import Flask, render_template, request, redirect, url_for, session
import json
import postgresql
import random
from flask_wtf import FlaskForm
import wtforms
from flask_wtf.csrf import CsrfProtect
from werkzeug.utils import secure_filename
import os
import string
import hashlib
from wtforms.validators import Required, EqualTo

class Log_in(FlaskForm):
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.PasswordField("Password", validators=[Required()])
    submit = wtforms.SubmitField('Log in')

class Sign_up(FlaskForm):
    name = wtforms.StringField("Name")
    surname = wtforms.StringField("Surname")
    login = wtforms.StringField("Login")
    password1 = wtforms.PasswordField("Password")
    password2 = wtforms.PasswordField("Confirm password", validators=[Required(),
    EqualTo('password1', message='Wrong password')])
    submit = wtforms.SubmitField('Sign up')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'
csrf = CsrfProtect()
csrf.init_app(app)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def reset_sesion():
    if session.get('id'):
        del session['name']
        del session['surname']
        del session['id']


def init_session(user_inf):
    session['id'] = user_inf[0]
    session['name'] = user_inf[1]
    session['surname'] = user_inf[2]

def chek_pass(login, password):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT * FROM LogPass WHERE userLog=$1;")
        user = sel(login.lower())
        if user:
            if user[0][2] == hashlib.md5(password.encode('utf8')).hexdigest():
                return user[0][0]
        return False


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("log_in"))

@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    reset_sesion()
    form = Log_in()
    if request.method == "GET":
        return render_template("log_in.html", form=form)
    if form.validate_on_submit():
        userId  = chek_pass(form.login.data, form.password.data)
        if  not userId:
            return render_template("log_in.html", form=form, error = "Wrong password")
        res = get_user_info(userId)
        if res:
            init_session(res)
            return redirect(url_for("user_profile", id = userId))
        return "Some Error. Please try again"
    return redirect(request.url)

@app.route("/<id>", methods=["GET", "POST"])
def user_profile(id):
    if request.method == "GET":
        return render_template("main.html", user = session, interests=get_interestsUser(id))
    elif request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        if data.get('action') == "get list":
            return json.dumps(get_interests()), 200
        elif data.get('action') == "new item":
            new_interest(id, data.get("interest"))
            return "OK", 200
        elif data.get('action') == "delete":
            remove_interest(id, data.get("interest"))
            return "OK", 200
    return "Not found", 404

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = Sign_up()
    if request.method == "GET":
        return render_template("sign_up.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            userId = id_generator()
            save_log(userId, form.login.data, form.password1.data)
            save_info(userId, form)
        return redirect(url_for("log_in"))

def save_log(id, login, password):
     with postgresql.open(os.environ['URL_DATABASE']) as db:
         ins = db.prepare("INSERT INTO LogPass VALUES ($1, $2, $3)")
         ins(id, login.lower(), hashlib.md5(password.encode('utf8')).hexdigest())

def save_info(id, form):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        ins = db.prepare("INSERT INTO UserInfo VALUES ($1, $2, $3)")
        ins(id, form.name.data, form.surname.data)

def remove_interest(userid, intereststr):
    iid = ""
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT interestId FROM Interest WHERE interestName = $1")
        iid = sel(intereststr)
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("DELETE FROM UserInterest WHERE userId = $1 and interestId = $2")
        users = sel(userid, iid[0][0])


def get_user_info(id):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT * FROM UserInfo WHERE userId = $1")
        users = sel(id)
    if users:
        return users[0]
    return {}

def get_interests():
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT * FROM Interest")
        interests = sel()
    if interests:
        return interests
    return {}

def new_interest(userid, interest):
    idInterest = id_generator()
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT * FROM Interest WHERE interestname = $1")
        interests = sel(interest)
    if not interests:
        with postgresql.open(os.environ['URL_DATABASE']) as db:
            sel = db.prepare("INSERT INTO Interest VALUES ($1, $2, $3)")
            interests = sel(idInterest, interest, 0)
    else:
        idInterest = interests[0][0]
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("INSERT INTO UserInterest VALUES ($1, $2)")
        interests = sel(userid, idInterest)

def get_interestsUser(id):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT interestname FROM userinterest NATURAL JOIN interest WHERE userid = $1")
        interests = sel(id)
    if interests:
        li = []
        for i in interests:
            li.append(i[0])
        return li
    return {}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ['PORT']), debug=True)
