# routes.py

# --- IMPORTS ---
# We need functions from Flask to handle requests, templates, and redirects.
from flask import Blueprint, render_template, request, redirect, url_for

# We need access to our database (db) and our data model (LogEntry).
from app import db
from app.models import LogEntry


# --- BLUEPRINT SETUP ---
# A Blueprint is a way to organize a group of related views and other code.
# Instead of registering views with the application directly, they are
# registered with a blueprint. Then, the blueprint is registered with the
# application when it is available in the factory function.
bp = Blueprint('main', __name__)


# --- ROUTES ---

# This is the main homepage route.
@bp.route('/')
@bp.route('/index')
def index():
    # This is the READ part of CRUD.
    # We query the database for all LogEntry objects.
    # We order them by the timestamp in descending order (newest first).
    # .all() executes the query and returns a list of all results.
    entries = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    
    # We pass this list of 'entries' to our template. The template will
    # then use a for-loop to display each one.
    return render_template('index.html', entries=entries)


# This route is specifically for handling the form submission.
# It only accepts POST requests, which is what HTML forms send.
@bp.route('/add', methods=['POST'])
def add_entry():
    # This is the CREATE part of CRUD.
    
    # 1. Get the data from the submitted form.
    # The key 'entry_text' must match the 'name' attribute of the <textarea> in our HTML.
    text = request.form['entry_text']
    
    # 2. Create a new Python object using our LogEntry model.
    new_entry = LogEntry(text=text)
    
    # 3. Add the new object to the database session.
    # This stages the object for saving.
    db.session.add(new_entry)
    
    # 4. Commit the session.
    # This writes all staged changes (our new entry) to the database permanently.
    db.session.commit()
    
    # 5. Redirect the user back to the homepage.
    # url_for('main.index') generates the URL for the 'index' function
    # within our 'main' blueprint. This is the correct way to link between pages.
    return redirect(url_for('main.index'))