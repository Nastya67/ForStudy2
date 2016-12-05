from flask import Flask, flash, render_template, redirect, session, url_for
from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Required
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
    submit = wtforms.SubmitField('Create new pointer')


UPLOAD_FOLDER = r'D:\Nastya\Учеба\2курс\ОВП\ForStudy2\Курсовая\static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    elif request.method == 'POST' and id == session.get('id'):
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
    form = []
    form.append(Add_foto())
    form.append(Create_point())
    if request.method == 'GET':
        if(id == session.get('id')):
            return render_template('userStr.html', user_data = session, form = form)
        else:
            user = get_user_info(id)
            if(user):
                return render_template('userStr.html', user_data = user)
            else:
                return "User does not exist"
    elif request.method == 'POST' and id == session['id']:
        if form[0].validate_on_submit():
            if 'photo' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['photo']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                update_photo(id, filename)
                session['userphoto'] = filename
                return render_template('userStr.html', user_data = session, form = form)
            else:
                flash('Invalid format')
                return redirect(request.url)
        elif request.form.get('Logout'):
            del session['name']
            del session['surname']
            del session['id']
            del session['birthday']
            return redirect(url_for('vhod'))

        print(request.data)
        latlng = request.data.decode('utf-8')
        
        return 'Ok'

    else:
        return "you can't to do this"

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

        else:
            return redirect(url_for("vhod"))
        return redirect(url_for('index', id = user_inf['iduser']))
    return render_template('vhod.html', form = form)

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
    return redirect(url_for('vhod'))

def new_post(id, lat, lng):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
        ins = db.prepare("INSERT INTO posts (idpost, iduser, longitude, latitude)"
        "VALUES ($1, $2, $3, $4)")
        postid = x.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
        print(postid)
        ins(postid, id, lng, lat)


def save_log(id, login, password):
     with postgresql.open("pq://postgres:poqwiueryt@localhost/CorseWork") as db:
         ins = db.prepare("INSERT INTO logpass VALUES ($1, $2, $3)")
         ins(id, hashlib.md5(password.encode('utf8')).hexdigest(), login.lower())

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
