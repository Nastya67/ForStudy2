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


class Vhod(FlaskForm):
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.StringField('Password', validators=[Required()])
    submit = wtforms.SubmitField('OK')

class Reg(FlaskForm):
    name = wtforms.StringField("Name", validators=[Required()])
    surname = wtforms.StringField("Surname", validators=[Required()])
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.PasswordField("Your password", validators=[Required()])
    password2 = wtforms.PasswordField("Repeat your password", validators=[Required(),
    EqualTo('password', message='wrong password')])
    bday = wtforms.SelectField('Day', choices=[(str(i), i) for i in range(1, 32)])
    bmonth = wtforms.SelectField('Month', choices=[(str(i), i) for i in range(1,13)])
    byear = wtforms.SelectField('Year', choices=[(str(i), i) for i in range(1916, 2016)])
    submit = wtforms.SubmitField('OK')

class Search_follower(FlaskForm):
    nameFollower = wtforms.StringField("Name Follower")
    submit = wtforms.SubmitField('Find')

class Add_foto(FlaskForm):
    foto = wtforms.FileField("Avatar")
    submit = wtforms.SubmitField('Change Photo')

class Create_point(FlaskForm):
    Text = wtforms.TextField('Text')
    submit = wtforms.SubmitField('Create new pointer')

class Log_out(FlaskForm):
    logout = wtforms.SubmitField("Log out")


UPLOAD_FOLDER = r'D:\Nastya\Учеба\2курс\ОВП\ForStudy2\Курсовая\static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
WTF_CSRF_SECRET_KEY = 'qpwoeiruty'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
csrf = CsrfProtect()
csrf.init_app(app)
count = 100
alfas = 'QWERTYUIOPASDFGHJKLZXCVBNM'
alfa_count1 = 0
alfa_count2 = 0
alfa_count3 = 0

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/api/<id>", methods=['GET', 'POST'])
def api_index(id):
    if request.method == 'GET':
        if session['name']:
            resp = {'name': session['name'], 'surname': session['surname']}
            resp['birthday'] = session['birthday']
            return json.dumps(resp)
        else:
            return "log in, please"
    elif request.method == 'POST' and (id == session.get('id') or session.get('roles') == 2):
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            update_photo(id, filename)
            session['userphoto'] = filename
            return 'ok'
        return 'Ok'


@app.route("/<id>", methods=['GET', 'POST'])
def index(id):
    form = {}
    form["Add_foto"] = Add_foto()
    form["Create_point"] = Create_point()
    form["Log_out"] = Log_out()
    if request.method == 'GET':
        if(id == session.get('id')):
            return render_template('userStr.html', user_data = session, form = form, authorization = session.get('id'))
        else:
            user = get_user_info(id)
            if(user):
                if session.get('roles') == 2:
                    return render_template('userStr.html', user_data = user, form = form, authorization = bool(session.get('id')))
                return render_template('userStr.html', user_data = user, authorization = session.get('id'))
            else:
                return "User does not exist"
    elif request.method == 'POST' and request.form.get('Logout') and session.get("id"):
        del session['name']
        del session['surname']
        del session['id']
        del session['birthday']
        del session['roles']
        return redirect(url_for('vhod'))
    elif request.method == 'POST' and (id == session['id'] or session.get('roles') == 2):
        if form["Add_foto"].validate_on_submit() and 'photo' in request.files:
            file = request.files['photo']
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                update_photo(id, filename)
                session['userphoto'] = filename
                return redirect(request.url)
            else:
                print('Invalid format')
                return redirect(request.url)
        elif request.form.get('friends'):
            return redirect(url_for("followers", id = id))
        else:
            latlng = request.data.decode('utf-8')
            ll3 = latlng[1:-1].partition(", ")
            new_post(session['id'], float(ll3[0]), float(ll3[2]))
            return flask.make_response("Ok")

    else:
        return "you can't to do this"

@app.route("/<id>/followers", methods=["GET", "POST"])
def followers(id):
    form = Search_follower()
    if request.method == 'GET':
        user_list = get_list_follower(id)
        return render_template("friend.html", friends = user_list, form = form)
    elif request.method == 'POST':
        return []

@app.route("/", methods=['GET', 'POST'])
def vhod():
    form = Vhod()

    if form.validate_on_submit():
        user = select_where_log(form.login.data)
        if(hashlib.md5(form.password.data.encode('utf8')).hexdigest() == user['password']):
            user_inf = get_user_info(user['iduser'])
            session['id'] = user_inf['iduser']
            session['name'] = user_inf['name']
            session['surname'] = user_inf['surname']
            session['userphoto'] = user_inf['userphoto']
            session['birthday'] = '%s-%s-%s' %(str(user_inf['bday']),
            str(user_inf['bmonth']), str(user_inf['byear']))
            session['posts'] = select_posts(session['id'])
            session['roles'] = user_inf['roles']
        else:
            return redirect(url_for("vhod"))
        return redirect(url_for('index', id = user_inf['iduser']))
    return render_template('vhod.html', form = form)

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    form = Reg()
    if form.validate_on_submit():
        id = id_generator(6, alfas)
        save_log(id, form.login.data, form.password.data)
        save_info(id, form)
        session['name'] = form.name.data
        session['surname'] = form.surname.data


        return redirect(url_for('index', id = id))
    return render_template("reg.html", form = form)
    return redirect(url_for('vhod'))

def new_post(id, lat, lng):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        ins = db.prepare("INSERT INTO posts (idpost, iduser, longitude, latitude, chocolate) "
        "VALUES ($1, $2, $3, $4, $5);")
        postid = id_generator(3, alfas)
        ins(postid, id, lng, lat, 0)

def select_posts(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM posts WHERE iduser = $1")
        posts = sel(id)
    if posts:
        return posts
    return 0


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def save_log(id, login, password):
     with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
         ins = db.prepare("INSERT INTO logpass VALUES ($1, $2, $3)")
         ins(id, hashlib.md5(password.encode('utf8')).hexdigest(), login.lower())

def get_list_follower(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT (iduser, name, surname, userphoto) FROM"
        " friendlist INNER JOIN users on id2=iduser WHERE id1 = $1;")
        users = sel(id)
    if users:
        return users
    return []

def select_where_log(login):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM logpass WHERE login = $1")
        users = sel(login.lower())
    if users:
        return users[0]
    return 0

def update_photo(id, foto):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        upd = db.prepare("UPDATE users SET userphoto=$1 WHERE iduser=$2")
        upd(foto, id)
    return 0

def get_user_info(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        sel = db.prepare("SELECT * FROM users WHERE iduser = $1")
        users = sel(id)
    if users:
        return users[0]
    return 0

def save_info(id, form):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        ins = db.prepare("INSERT INTO users (iduser, name, surname, bday, "
        "bmonth, byear, roles) VALUES ($1, $2, $3, $4, $5, $6, $7)")
        ins(id, form.name.data, form.surname.data, int(form.bday.data), int(form.bmonth.data),
        int(form.byear.data), 1)




if __name__ == "__main__":
    app.run(debug=True)
