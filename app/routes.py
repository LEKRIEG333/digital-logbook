# routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import LogEntry

# Create a Blueprint object to organize our routes
bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """
    READ Operation: Display all log entries.
    """
    # Query the database for all entries, ordered by newest first
    entries = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    # Pass the entries to the template for rendering
    return render_template('index.html', entries=entries)

@bp.route('/add', methods=['POST'])
def add():
    """
    CREATE Operation: Add a new log entry.
    """
    # Get the text from the form submission
    entry_text = request.form['entry_text']
    
    # Create a new LogEntry object with the submitted text
    new_entry = LogEntry(text=entry_text)
    
    # Add the new entry to the database session and commit the transaction
    db.session.add(new_entry)
    db.session.commit()
    
    # Redirect the user back to the main page to see the new entry
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    """
    Part 1 of UPDATE: Display the form to edit an existing entry.
    """
    # Find the specific entry by its ID. 
    # db.get_or_404 is a shortcut that returns the object or a 404 Not Found error.
    entry = db.get_or_404(LogEntry, id)
    # Render the edit template, passing the existing entry data to it
    return render_template('edit.html', entry=entry)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    """
    Part 2 of UPDATE: Process the form submission and save the changes.
    """
    entry = db.get_or_404(LogEntry, id)
    # Update the entry's text with the new text from the form
    entry.text = request.form['entry_text']
    # Commit the changes to the database
    db.session.commit()
    # Redirect back to the main page
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:id>')
def delete(id):
    """
    DELETE Operation: Remove an entry from the database.
    """
    entry = db.get_or_404(LogEntry, id)
    # Delete the entry from the database
    db.session.delete(entry)
    db.session.commit()
    # Redirect back to the main page
    return redirect(url_for('main.index'))