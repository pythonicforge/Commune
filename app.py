from flask import Flask, render_template, request
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAdQcNW7aCV9gQ2Uf--IDO_Fd4w5yLFWNU",
    "authDomain": "commune-88a9c.firebaseapp.com",
    "databaseURL":"https://commune-88a9c-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "commune-88a9c",
    "storageBucket": "commune-88a9c.appspot.com",
    "messagingSenderId": "525975479363",
    "appId": "1:525975479363:web:bcf5bf5deea6b0bbd320f6",
    "measurementId": "G-N124PHM3FC"
}

app = Flask(__name__)
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route('/register')
def sign_up():
    return render_template('register.html')

@app.route('/submitOldUser', methods=['POST'])
def signUpDashboard():
    email = request.form['email']
    password = request.form['password']
    auth.create_user_with_email_and_password(email, password)
    return f"Hi {email}, you are signed up now"

@app.route('/submitNewUser', methods=['POST'])
def signInDashboard():
    email = request.form['email']
    password = request.form['password']
    auth.sign_in_with_email_and_password(email, password)
    return f"Hi {email}, you are logged in now"

@app.route('/login')
def sign_in():
    return render_template('login.html')

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)