# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config # Import the new config file

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    
    # Load configuration from the config.py file
    app.config.from_object(config.Config)

    # Initialize extensions with the app
    db.init_app(app)

    with app.app_context():
        # Import and register blueprints
        from . import routes
        app.register_blueprint(routes.bp)
        
        # Ensure models are known to SQLAlchemy before creating tables
        from . import models
        
        # Create database tables for our models
        db.create_all()

        return app