# models.py

import datetime
from app import db

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<LogEntry {self.id}: {self.text[:50]}>'