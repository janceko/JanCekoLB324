import os
from dotenv import load_dotenv
from flask import Flask
from src.config import Config
from src.models import db
from src.routes import init_routes

# Lade Umgebungsvariablen aus einer .env-Datei
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'standard_geheimer_schluessel')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Konfiguration aus der Config-Klasse laden
    db.init_app(app)  # Initialisiere die Datenbank
    with app.app_context():
        db.create_all()  # Erstelle alle Datenbanktabellen, falls sie nicht existieren
    init_routes(app)  # Initialisiere die Routen
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

