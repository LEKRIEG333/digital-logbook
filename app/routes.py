from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import LogEntry

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # NEW: Query the database for all entries, ordered by newest first
    entries = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    # NEW: Pass the entries to the template
    return render_template('index.html', entries=entries)

@bp.route('/add', methods=['POST'])
def add():
    # NEW: Get the text from the form submission
    entry_text = request.form['entry_text']
    
    # Create a new LogEntry object
    new_entry = LogEntry(text=entry_text)
    
    # Add the new entry to the database session and commit
    db.session.add(new_entry)
    db.session.commit()
    
    # Redirect the user back to the main page
    return redirect(url_for('main.index'))