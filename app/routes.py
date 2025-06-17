# NEW: flash is added to the import list
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import LogEntry

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    entries = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

@bp.route('/add', methods=['POST'])
def add():
    entry_text = request.form['entry_text']
    entry_category = request.form.get('category')
    
    new_entry = LogEntry(text=entry_text, category=entry_category)
    
    db.session.add(new_entry)
    db.session.commit()
    
    # --- NEW: Flash a success message to the user ---
    flash('Log entry created successfully!', 'success')
    # --- End of new code ---
    
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    entry = db.get_or_404(LogEntry, id)
    return render_template('edit.html', entry=entry)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    entry = db.get_or_404(LogEntry, id)
    entry.text = request.form['entry_text']
    entry.category = request.form.get('category')
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:id>')
def delete(id):
    entry = db.get_or_404(LogEntry, id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.index'))