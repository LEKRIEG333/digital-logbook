# models.py

import datetime
from app import db

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True, default='General') 
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<LogEntry {self.id}: {self.text[:50]}>'