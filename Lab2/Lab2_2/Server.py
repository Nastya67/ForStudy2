from flask import Flask, render_template, request, redirect, url_for
import json
import postgresql
import random
from flask_wtf import FlaskForm
import wtforms
from flask_wtf.csrf import CsrfProtect
from werkzeug.utils import secure_filename
import os
import string

class Create(FlaskForm):
    name = wtforms.StringField("Name")
    author = wtforms.StringField("Author")
    size = wtforms.IntegerField("Size")
    edition = wtforms.IntegerField("Edition")
    date = wtforms.StringField("Date")
    #foto = wtforms.FileField("Title page")
    submit = wtforms.SubmitField('Create')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = r"D:\Nastya\Учеба\2курс\ОВП\ForStudy2\Lab2\Lab2_2\static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'qpwoeiruty'

ss = 'qwertyuiopasdfghjkl123456789zxcvbnm'

def request_args_get():
    date = request.args.get('date')
    name = request.args.get('name')
    author = request.args.get('author')
    size = request.args.get("size")
    edition = request.args.get('edition')
    return {"name":name, "author":author, "date":date, "edition":edition, "size":size}

def insert_book(form, photo):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/Lab2") as db:
        ins = db.prepare("INSERT INTO books VALUES ($1, $2, $3, $4, $5, $6, $7);")
        id = id_generator(3, "qwertyuiopasdfghjklzxcvbnm")
        ins(id, form.name.data, form.author.data,
        form.date.data, form.edition.data, form.size.data, photo)
    return id


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/book/<index>", methods=['GET', "POST"])
def one_book(index):
    if request.method == "GET":
        book = get_book_where(index)
        return render_template('book.html', book = book)
    if request.form.get("delete"):
        del_book_where(index)
        return redirect(url_for("List"))

@app.route("/list", methods=['GET', 'POST'])
def List():
    if request.args.get("find") and request.args.get("field_find"):
        books = get_all_books()
        res = []
        find_val = request.args.get("field_find")
        for book in books:
            if str(book["book_name"]).find(find_val) != -1:
                print(str(book))
                res.append(book)
        return render_template('list.html', books = res, find_val = find_val, page={"cur":0, "max":0})
    if request.method == 'GET':
        num = request.args.get('page')
        size = 4;
        if not num:
            return redirect("/list?page=0")
        books = get_list_books(int(num), size)
        return render_template('list.html', books = books['books'], page={'cur':int(num), 'max':books['size']/size})

@app.route("/new_book", methods=['GET', "POST"])
def new_book():
    form = Create()
    if request.method == "GET":
        return render_template("create.html", form = form)
    elif request.method =="POST" and form.validate_on_submit():
        file = request.files['photo']
        if file.filename == "":
            id = insert_book(form, "")
            return redirect(url_for("one_book", index = id))
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
    with postgresql.open("pq://postgres:poqwiueryt@localhost/Lab2") as db:
        sel = db.prepare(req)
        books = sel(val)
    if books:
        return books
    return 0

def generic_rand_id():
    i1 = random.randint(0, len(ss)-1)
    i2 = random.randint(0, len(ss)-1)
    i3 = random.randint(0, len(ss)-1)
    return ss[i1]+ss[i2]+ss[i3]

def del_book_where(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/Lab2") as db:
        dell = db.prepare("DELETE FROM Books WHERE book_id=$1;")
        dell(id)

def get_all_books():
    with postgresql.open("pq://postgres:poqwiueryt@localhost/Lab2") as db:
        sel = db.prepare("SELECT * FROM Books;")
        books = sel()
    if books:
        return books
    return 0

def get_list_books(num = 0, size = 4):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/Lab2") as db:
        sel = db.prepare("SELECT book_id, book_name, book_photo FROM Books;")
        books = sel()
    if books:
        res = {'books':books[num*size:num*size+size], 'size':len(books)}
        return res
    return 0

def get_book_where(id):
    with postgresql.open("pq://postgres:poqwiueryt@localhost/Lab2") as db:
        sel = db.prepare("SELECT * FROM Books WHERE book_id = $1;")
        books = sel(id)
    if books:
        return books[0]
    return 0

if __name__ == "__main__":
    app.run(debug=True)
