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
    entry_text = request.form['entry_text']
    # NEW: Get the category from the form. Use .get() for optional fields.
    entry_category = request.form.get('category')
    
    # Pass the new category to the LogEntry constructor
    new_entry = LogEntry(text=entry_text, category=entry_category)
    
    db.session.add(new_entry)
    db.session.commit()
    
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
    entry = db.get_or_404(LogEntry, id)
    entry.text = request.form['entry_text']
    # NEW: Update the category field as well
    entry.category = request.form.get('category')
    db.session.commit()
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