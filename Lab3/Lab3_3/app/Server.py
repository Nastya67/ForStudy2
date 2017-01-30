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
from wtforms.validators import Required, EqualTo

class Create(FlaskForm):
    name = wtforms.StringField("Name")
    author = wtforms.StringField("Author")
    size = wtforms.IntegerField("Size")
    edition = wtforms.IntegerField("Edition")
    date = wtforms.StringField("Date")
    submit = wtforms.SubmitField('Create')

class Sign_up(FlaskForm):
    name = wtforms.StringField("Name")
    surname = wtforms.StringField("Surname")
    login = wtforms.StringField("Login")
    password1 = wtforms.PasswordField("Password")
    password2 = wtforms.PasswordField("Confirm password", validators=[Required(),
    EqualTo('password1', message='Wrong password')])
    submit = wtforms.SubmitField('Sign up')

class Log_in(FlaskForm):
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.PasswordField("Password", validators=[Required()])
    submit = wtforms.SubmitField('Log in')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = r"D:\Nastya\Учеба\2курс\ОВП\ForStudy2\Lab3\Lab3_1\static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'qpwoeiruty'


def request_args_get():
    date = request.args.get('date')
    name = request.args.get('name')
    author = request.args.get('author')
    size = request.args.get("size")
    edition = request.args.get('edition')
    return {"name":name, "author":author, "date":date, "edition":edition, "size":size}

def insert_book(form, photo):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        ins = db.prepare("INSERT INTO books VALUES ($1, $2, $3, $4, $5, $6, $7);")
        id = id_generator(3, "qwertyuiopasdfghjklzxcvbnm")
        ins(id, form.name.data, form.author.data,
        form.date.data, form.edition.data, form.size.data, photo)
    return id

def new_user(form):
    id = id_generator(4, "qwertyuiopasdfghjklzxcvbnm")
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        ins_users = db.prepare("INSERT INTO users VALUES ($1, $2, $3);")
        ins_users(id, form.login.data, form.password1.data)
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        ins = db.prepare("INSERT INTO user_info VALUES ($1, $2, $3, $4);")
        ins(id, form.name.data, form.surname.data, False)
    return id

def get_user(login):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT user_id FROM users WHERE user_login=$1;")
        user_id = sel(login)
        if user_id:
            sel2 = db.prepare("SELECT * FROM user_info WHERE user_id=$1;")
            user_info = sel2(user_id[0][0])
            if user_info:
                res = {'user_id':user_info[0]['user_id'],
                'user_name':user_info[0]['user_name'],
                'user_surname':user_info[0]['user_surname'],
                'user_status':user_info[0]['user_status']}
                return res
    return None

def chek_pass(login, password):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT user_password FROM users WHERE user_login=$1;")
        user_pass = sel(login)
        if user_pass:
            if user_pass[0][0] == password:
                return True
        return False

def get_user_list():
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT user_name, user_surname FROM user_info;")
        return sel()


def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def init_session(res):
    session['name'] = res['user_name']
    session['surname'] = res['user_surname']
    session['id'] = res['user_id']
    session['admin'] = res['user_status']

def reset_sesion():
    if session.get('id'):
        del session['name']
        del session['surname']
        del session['id']
        del session['admin']

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html', user = session)

@app.route("/users")
def users():
    if session.get('admin'):
        user_list = get_user_list()
        return render_template("user_list.html", user_list = user_list)
    return redirect("/home")

@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    reset_sesion()
    form = Log_in()
    if request.method == "GET":
        return render_template("log_in.html", form=form)
    if form.validate_on_submit():
        if  not chek_pass(form.login.data, form.password.data):
            return render_template("log_in.html", form=form, error = "Wrong password")
        res = get_user(form.login.data)
        if res:
            init_session(res)
            return redirect(url_for("home"))
        return "Some Error. Please try again"
    return redirect(request.url)

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    reset_sesion()
    form = Sign_up()
    if request.method == "GET":
        return render_template("sign_up.html", form=form)
    if form.validate_on_submit():
        id_user = new_user(form)
        res = get_user(form.login.data)
        if res:
            init_session(res)
            return redirect(url_for("home"))
        return "Some Error. Please try again"
    return redirect(request.url)

@app.route("/book/<index>", methods=['GET', "POST"])
def one_book(index):
    if not session.get('id'):
        return redirect("/log_in")
    if request.method == "GET":
        book = get_book_where(index)
        return render_template('book.html', book = book, user = session)
    if request.form.get("delete"):
        del_book_where(index)
        return redirect(url_for("List"))
    return redirect(request.url)

@app.route("/list", methods=['GET', 'POST'])
def List():
    if not session.get('id'):
        return redirect("/log_in")
    if request.args.get("find") and request.args.get("field_find"):
        books = get_all_books()
        res = []
        find_val = request.args.get("field_find")
        for book in books:
            if str(book["book_name"]).find(find_val) != -1:
                print(str(book))
                res.append(book)
        return render_template('list.html', books = res, find_val = find_val,
        page={"cur":0, "max":0}, user = session)
    if request.method == 'GET':
        num = request.args.get('page')
        size = 4;
        if not num:
            return redirect("/list?page=0")
        books = get_list_books(int(num), size)
        if(books):
            return render_template('list.html', books = books.get('books'),
            page={'cur':int(num), 'max':books.get('size')/size}, user = session)
        return render_template('list.html', books = 0,
        page={'cur':int(num), 'max':0}, user = session)

@app.route("/new_book", methods=['GET', "POST"])
def new_book():
    if not session.get('id'):
        return redirect("/log_in")
    form = Create()
    if request.method == "GET":
        return render_template("create.html", form = form, user = session)
    elif request.method =="POST" and form.validate_on_submit():
        file = request.files['photo']
        if file.filename == "":
            id = insert_book(form, "")
            return redirect(url_for("one_book", index = id))
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            id = insert_book(form, filename)
            return redirect(url_for("one_book", index = id))
    return "Error"

@app.route('/api/list', methods=['GET', 'POST', 'DELETE'])
def api_list():
    args = request_args_get()
    if request.method == 'GET':
        line = "SELECT * FROM Books WHERE"
        i = 1
        list_val = []
        for key in args.keys():
            if args[key] != None:
                list_val.append(args[key])
                line += " {0} = ${1} AND ".format("book_"+key, i)
                i +=1
        if i > 1:
            line = line[:-4]
        else:
            line = line[:6]
        books = get_book_filter(line, list_val)
        return books

@app.route('/api/book/<index>', methods=['GET', 'DELETE', 'POST'])
def api_book(index):
    if request.method == 'GET':
        book = get_book_where(index)
        book = list(book)
        book[3] = str(book[3])
        return json.dumps(book)
    elif request.method == 'DELETE':
        del_book_where(index)
        return "OK"
    elif request.method == 'POST':
        return "0"

def get_book_filter(req, val):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare(req)
        books = sel(val)
    if books:
        return books
    return 0

def del_book_where(id):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        dell = db.prepare("DELETE FROM Books WHERE book_id=$1;")
        dell(id)

def get_all_books():
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT * FROM Books;")
        books = sel()
    if books:
        return books
    return {}

def get_list_books(num = 0, size = 4):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT book_id, book_name, book_photo FROM Books;")
        books = sel()
    if books:
        res = {'books':books[num*size:num*size+size], 'size':len(books)}
        return res
    return {}

def get_book_where(id):
    with postgresql.open(os.environ['URL_DATABASE']) as db:
        sel = db.prepare("SELECT * FROM Books WHERE book_id = $1;")
        books = sel(id)
    if books:
        return books[0]
    return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ['PORT']), debug=True)
