from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
import functools
from . import auth

auth_bp = Blueprint('auth', __name__)

# Define user-friendly error messages
ERROR_MESSAGES = {
    'EMAIL_NOT_FOUND': 'No account found with this email.',
    'INVALID_PASSWORD': 'The password you entered is incorrect.',
    'USER_DISABLED': 'This account has been disabled by an administrator.',
    'EMAIL_EXISTS': 'This email is already registered.',
    'INVALID_EMAIL': 'The email address is badly formatted.',
    'WEAK_PASSWORD': 'The password is too weak.',
    'INVALID_LOGIN_CREDENTIALS': 'Invalid login credentials. Please try again.',
}

def get_user_friendly_message(error):
    """
    Extract a user-friendly message from an error response.

    Args:
    error (Exception): The original error response from the authentication system.

    Returns:
    str: A user-friendly error message.
    """
    error_response = error.args[1]
    error_data = eval(error_response)  # Convert the string representation of the dictionary back to a dictionary
    error_code = error_data.get("error", {}).get("message", "")
    return ERROR_MESSAGES.get(error_code, 'An unknown error occurred. Please try again later.')

def no_cache(view):
    @functools.wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache_view

@auth_bp.route('/register', methods=['GET', 'POST'])
@no_cache
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('auth.dashboard'))
        except Exception as e:
            error_message = get_user_friendly_message(e)
            flash(error_message)
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@no_cache
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('auth.dashboard'))
        except Exception as e:
            error_message = get_user_friendly_message(e)
            flash(error_message)
    return render_template('login.html')

@auth_bp.route('/dashboard')
@no_cache
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@auth_bp.route('/logout')
@no_cache
def logout():
    session.pop('user', None)
    print("You have logged out")
    return redirect(url_for('auth.login'))
