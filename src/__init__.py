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

    from .auth import auth_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
