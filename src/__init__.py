from flask import Flask
import pyrebase
from flask_session import Session
from config import Config

firebaseConfig = {
    "apiKey": Config.FIREBASE_API_KEY,
    "authDomain": Config.FIREBASE_AUTH_DOMAIN,
    "databaseURL": Config.FIREBASE_DATABASE_URL,
    "projectId": Config.FIREBASE_PROJECT_ID,
    "storageBucket": Config.FIREBASE_STORAGE_BUCKET,
    "messagingSenderId": Config.FIREBASE_MESSAGING_SENDER_ID,
    "appId": Config.FIREBASE_APP_ID,
    "measurementId": Config.FIREBASE_MEASUREMENT_ID
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    Session(app)

    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    from.auth import auth_bp
    from.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app