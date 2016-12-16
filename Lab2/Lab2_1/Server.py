from flask import Flask, render_template, request, redirect, url_for
import json
import postgresql
import random
app = Flask(__name__)

ss = 'qwertyuiopasdfghjkl123456789zxcvbnm'

def request_args_get():
    date = request.args.get('date')
    name = request.args.get('name')
    author = request.args.get('author')
    size = request.args.get("size")
    edition = request.args.get('edition')
    return {"name":name, "author":author, "date":date, "edition":edition, "size":size}

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/book/<index>")
def one_book(index):
    book = get_book_where(index)
    return render_template('book.html', book = book)

@app.route("/list")
def List():
    num = request.args.get('page')
    size = 4;
    if not num:
        return redirect("/list?page=0")
    books = get_list_books(int(num), size)
    return render_template('list.html', books = books['books'], page={'cur':int(num), 'max':books['size']/size})

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
    print("Start")
    app.run(debug=True)
