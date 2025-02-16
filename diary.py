import json
import os
from datetime import datetime
from security import SecurityManager

class DiaryManager:
    def __init__(self, password):
        self.security = SecurityManager()
        self.security.set_password(password)
        self.entries = []
        self.load_entries()
        
    def add_entry(self, content, mood=None, tags=None):
        """Add a new diary entry"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'content': content,
            'mood': mood,
            'tags': tags or []
        }
        self.entries.append(entry)
        self.save_entries()
        
    def get_entries(self):
        """Get all diary entries"""
        return self.entries
        
    def search_entries(self, query):
        """Search entries containing the query"""
        return [entry for entry in self.entries if query.lower() in entry['content'].lower()]
        
    def save_entries(self):
        """Save entries to file"""
        with open('diary_entries.json', 'w') as f:
            encrypted_data = self.security.encrypt_data(json.dumps(self.entries), 'secret_key')
            f.write(encrypted_data)
            
    def load_entries(self):
        """Load entries from file"""
        if os.path.exists('diary_entries.json'):
            with open('diary_entries.json', 'r') as f:
                encrypted_data = f.read()
                self.entries = json.loads(self.security.decrypt_data(encrypted_data, 'secret_key'))
