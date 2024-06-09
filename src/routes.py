from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    """
    The main function is the entry point for the root URL ('/').
    It checks if a user is logged in by checking the 'user' key in the session.
    If a user is logged in, it renders the 'dashboard.html' template.
    If no user is logged in, it renders the 'index.html' template.

    Parameters:
    None

    Returns:
    render_template: A rendered HTML template based on the conditions.
    """
    if 'user' in session:
        return render_template("dashboard.html")
    return render_template('index.html')
