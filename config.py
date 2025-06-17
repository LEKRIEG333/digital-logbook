# config.py

import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_development')
    # This line constructs the database path safely, regardless of the OS.
    # It looks for a DATABASE_URL environment variable first (for production)
    # and falls back to our local sqlite DB in the 'instance' folder.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'logbook.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False