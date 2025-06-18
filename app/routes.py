# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import repository # NEW: Import the repository instead of db and models

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # REFACTORED: The route no longer knows about the database.
    entries = repository.get_all_entries()
    return render_template('index.html', entries=entries)

@bp.route('/add', methods=['POST'])
def add():
    # REFACTORED: The route simply gathers data and passes it to the repository.
    entry_text = request.form['entry_text']
    entry_category = request.form.get('category')
    repository.add_entry(text=entry_text, category=entry_category)
    flash('Log entry created successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    # REFACTORED: The route asks the repository for the specific entry.
    entry = repository.get_entry_by_id(id)
    return render_template('edit.html', entry=entry)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    # REFACTORED: The route gathers the new data and tells the repository to update.
    new_text = request.form['entry_text']
    new_category = request.form.get('category')
    repository.update_entry(id, new_text, new_category)
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:id>')
def delete(id):
    # REFACTORED: The route simply tells the repository to delete the entry.
    repository.delete_entry(id)
    return redirect(url_for('main.index'))