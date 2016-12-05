from flask import Flask, render_template, request, redirect, url_for
import json
import postgresql
app = Flask(__name__)

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

@app.route('/api/list')
def api_list():
    name = request.args.get('name')
    books_pg = get_all_books()
    book = []
    for b in books_pg:
        book.append(list(b))
    for b in book:
        b[3] = str(b[3])
    return json.dumps(book)

@app.route('/api/book/<index>')
def api_book(index):
    book = get_book_where(index)
    book = list(book)
    book[3] = str(book[3])
    return json.dumps(book)

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
