from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    if 'user' in session:
        return render_template("dashboard.html")
    return render_template('index.html')
