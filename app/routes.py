# routes.py

# --- IMPORTS ---
from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import LogEntry


# --- BLUEPRINT SETUP ---
bp = Blueprint('main', __name__)


# --- ROUTES ---

@bp.route('/')
@bp.route('/index')
def index():
    entries = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

@bp.route('/add', methods=['POST'])
def add_entry():
    text = request.form['entry_text']
    new_entry = LogEntry(text=text)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('main.index'))

# ======================================================
# NEW ROUTES FOR UPDATE AND DELETE
# ======================================================

# This route handles both displaying the edit form (GET) and processing it (POST)
# The <int:entry_id> part is a dynamic converter that captures the ID from the URL.
@bp.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    # Find the specific entry by its ID, or return a 404 Not Found error if it doesn't exist
    entry = LogEntry.query.get_or_404(entry_id)
    
    # If the user submitted the form (a POST request)
    if request.method == 'POST':
        # This is the UPDATE part of CRUD
        entry.text = request.form['entry_text']
        db.session.commit()
        return redirect(url_for('main.index'))
    
    # If the user is just visiting the page (a GET request), show the edit form
    return render_template('edit_entry.html', entry=entry)

# This route handles deleting an entry
@bp.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    # This is the DELETE part of CRUD
    entry = LogEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.index'))