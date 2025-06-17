# __init__.py

from flask import Flask, render_template # NEW: Import render_template
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config.Config)
    db.init_app(app)

    # --- NEW: Register error handlers ---
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        # In a real app, you'd log the error here.
        # For now, we just show the page.
        db.session.rollback() # Rollback the session in case of a DB error
        return render_template('500.html'), 500
    # --- End of new code ---

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
        
        from . import models
        db.create_all()

        return app