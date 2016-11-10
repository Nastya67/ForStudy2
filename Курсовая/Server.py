from flask import Flask, render_template
app = Flask(__name__)

import json

@app.route("/")
def index():
    return render_template('userStr.html')

@app.route("/user/<name>")
def user(name):
    return "<h1>Hello %s </h1>" %name


if __name__ == "__main__":
    app.run(debug=True)
