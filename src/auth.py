from flask import Blueprint, render_template, request, redirect, url_for, session
from . import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return render_template("dashboard.html")
        except Exception as e:
            print(e)
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return render_template("dashboard.html")
        except Exception as e:
            print(e)
    return render_template('login.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    print("You have logged out")
    return redirect(url_for('auth.login'))
