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

    This function takes an exception object as input, which is assumed to contain an error response from an authentication system.
    The error response is expected to be a string representation of a dictionary. The function converts this string back into a dictionary,
    extracts the error code, and then uses this code to look up and return a corresponding user-friendly error message.

    Args:
    error (Exception): The original error response from the authentication system. The error response is assumed to be a string representation of a dictionary.

    Returns:
    str: A user-friendly error message. If the error code is not found in the ERROR_MESSAGES dictionary, the function returns a default message.

    Raises:
    Exception: If the error response cannot be converted into a dictionary, the function raises an exception.

    Note:
    The error response dictionary is expected to have a structure like this:
    {
        "error": {
            "message": "ERROR_CODE"
        }
    }
    """
    error_response = error.args[1]
    error_data = eval(error_response)
    error_code = error_data.get("error", {}).get("message", "")
    return ERROR_MESSAGES.get(error_code, 'An unknown error occurred. Please try again later.')

def no_cache(view):
    """
    Decorator function to prevent caching of views.

    This decorator wraps around a view function and adds HTTP headers to the response to prevent caching.
    The headers set are:
    - Cache-Control: no-store, no-cache, must-revalidate
    - Pragma: no-cache
    - Expires: 0

    Args:
    view (function): The view function to be decorated.

    Returns:
    function: The decorated view function with added HTTP headers to prevent caching.
    """
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
    """
    Handles the registration process for new users.

    This function processes POST requests to create a new user account using the provided email and password.
    It also handles GET requests to render the registration template.

    Parameters:
    None

    Returns:
    redirect: A Flask redirect response to the dashboard page if the user is successfully registered.
    render_template: A Flask render_template response to the registration page if the request method is GET or if the registration fails.

    Raises:
    Exception: If an error occurs during the registration process, it is caught and handled by the get_user_friendly_message function.
    """
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
    """
    Handles the login route. It processes POST requests to authenticate users and GET requests to render the login template.

    Parameters:
    None

    Returns:
    redirect: A Flask redirect response to the dashboard page if the user is successfully logged in.
    render_template: A Flask render_template response to the login page if the request method is GET or if the login fails.
    """
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
    """
    This function handles the dashboard route. It checks if the user is logged in by verifying the existence of the 'user' key in the session.
    If the user is not logged in, they are redirected to the login page. Otherwise, the dashboard page is rendered.

    Parameters:
    None

    Returns:
    redirect: A Flask redirect response to the login page if the user is not logged in.
    render_template: A Flask render_template response to the dashboard page if the user is logged in.
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@auth_bp.route('/logout')
@no_cache
def logout():
    """
    Logs out the user by removing the 'user' key from the session.
    Prints a message indicating that the user has logged out.
    Redirects the user to the login page.

    Parameters:
    None

    Returns:
    redirect: A Flask redirect response to the login page.
    """
    session.pop('user', None)
    print("You have logged out")
    return redirect(url_for('auth.login'))
