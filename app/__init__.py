# __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the database extension object outside the factory
db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # --- DATABASE CONFIGURATION ---
    # We now use an absolute path to avoid any ambiguity.
    # app.instance_path is a special Flask attribute that points to the 'instance' folder.
    db_path = os.path.join(app.instance_path, 'logbook.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # The folder already exists.

    # Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        # Import the blueprint
        from . import routes
        
        # Register the blueprint with the app
        app.register_blueprint(routes.bp)
        
        # Import models here to ensure they are known to SQLAlchemy
        from . import models
        
        # Create database tables for our models
        db.create_all()

        return app