from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/register')
def sign_up():
    return render_template('register.html')

@app.route('/login')
def sign_in():
    return render_template('login.html')

@app.route('/')
def main():
    return render_template('index.html')