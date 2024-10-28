from flask import Flask
from src.config import Config
from src.models import db
from src.routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    init_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)