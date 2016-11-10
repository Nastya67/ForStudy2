from flask import Flask, render_template
import json
app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():    
    return render_template('home.html')
    

@app.route("/book/<index>")
def one_book(index):
    book = read_json("Books.json")
    return render_template('book.html', book = book, i = int(index))

@app.route("/list")
def List():
    book = read_json("Books.json")
    return render_template('list.html', books = book)

def read_json(name):
    book_txt = open(name).read()
    book = json.loads(book_txt)
    return book
def read_file(name):
    txt = open(name).read()
    return txt

if __name__ == "__main__":
    print("Start")
    app.run(debug=True)


    
