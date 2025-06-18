# __init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config

# Create the database extension object outside the factory
db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    
    # Load configuration from the config.py file
    app.config.from_object(config.Config)

    # Initialize extensions with the app
    db.init_app(app)

    # --- Register error handlers ---
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        # In a real app, you'd log the error here.
        db.session.rollback() # Rollback the session in case of a DB error
        return render_template('500.html'), 500
    # --- End of error handlers ---

    with app.app_context():
        # Import and register blueprints
        from . import routes
        app.register_blueprint(routes.bp)
        
        # Ensure models are known to SQLAlchemy before creating tables
        from . import models
        # NEW: Ensure the repository is imported within the app context
        from . import repository
        
        # Create database tables for our models
        db.create_all()

        return app