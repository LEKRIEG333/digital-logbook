# repository.py

from app import db
from app.models import LogEntry

def get_all_entries():
    """Retrieves all log entries, newest first."""
    return LogEntry.query.order_by(LogEntry.timestamp.desc()).all()

def add_entry(text, category):
    """Adds a new log entry to the database."""
    new_entry = LogEntry(text=text, category=category)
    db.session.add(new_entry)
    db.session.commit()
    return new_entry

def get_entry_by_id(id):
    """Retrieves a single entry by its unique ID."""
    return db.get_or_404(LogEntry, id)

def update_entry(id, new_text, new_category):
    """Updates the text and category of an existing entry."""
    entry = get_entry_by_id(id)
    entry.text = new_text
    entry.category = new_category
    db.session.commit()
    return entry

def delete_entry(id):
    """Deletes an entry from the database."""
    entry = get_entry_by_id(id)
    db.session.delete(entry)
    db.session.commit()