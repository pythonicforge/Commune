from flask import Blueprint, render_template, request, redirect, url_for, session
from . import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function handles the registration process.
    It accepts POST requests with email and password data.
    Upon successful registration, it logs in the user and redirects to the dashboard.
    If an error occurs during registration, it prints the error message.

    Parameters:
    None

    Returns:
    render_template('register.html') if the request method is not POST
    render_template('dashboard.html') if the registration is successful
    """
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
    """
    This function handles the login process.
    It accepts POST requests with email and password data.
    Upon successful login, it logs in the user and redirects to the dashboard.
    If an error occurs during login, it prints the error message.

    Parameters:
    None

    Returns:
    render_template('login.html') if the request method is not POST
    render_template('dashboard.html') if the login is successful
    """
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
    """
    This function handles the dashboard route.
    It checks if the user is logged in by verifying the existence of 'user' in the session.
    If the user is not logged in, it redirects them to the login page.
    If the user is logged in, it renders the dashboard template.

    Parameters:
    None

    Returns:
    redirect(url_for('auth.login')) if the user is not logged in
    render_template('dashboard.html') if the user is logged in
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@auth_bp.route('/logout')
def logout():
    """
    This function handles the logout process.
    It removes the 'user' key from the session to log out the user.
    It prints a message indicating that the user has logged out.
    Finally, it redirects the user to the login page.

    Parameters:
    None

    Returns:
    redirect(url_for('auth.login')) - Redirects the user to the login page after logging out.
    """
    session.pop('user', None)
    print("You have logged out")
    return redirect(url_for('auth.login'))
