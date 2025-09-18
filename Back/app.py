from flask import Flask
from src.config.config import Config
from src.routes import register_routes
from src.config.database import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Import models here to make sure they are registered with SQLAlchemy
    from src import models

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)