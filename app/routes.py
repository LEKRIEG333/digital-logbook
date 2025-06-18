# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import repository

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """
    READ Operation: Display all log entries, or a filtered list based on a search query.
    """
    # Check if a 'search_query' was provided in the URL's arguments (from the GET form)
    query = request.args.get('search_query')
    
    if query:
        # If there is a query, use the repository's search function
        entries = repository.search_entries(query)
    else:
        # Otherwise, get all entries as before
        entries = repository.get_all_entries()
        
    # Pass the entries (either all or filtered) and the query to the template.
    # The 'search_query=query' part is so we can pre-fill the search box.
    return render_template('index.html', entries=entries, search_query=query)

@bp.route('/add', methods=['POST'])
def add():
    entry_text = request.form['entry_text']
    entry_category = request.form.get('category')
    repository.add_entry(text=entry_text, category=entry_category)
    flash('Log entry created successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    entry = repository.get_entry_by_id(id)
    return render_template('edit.html', entry=entry)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_text = request.form['entry_text']
    new_category = request.form.get('category')
    repository.update_entry(id, new_text, new_category)
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:id>')
def delete(id):
    repository.delete_entry(id)
    return redirect(url_for('main.index'))