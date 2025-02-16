import zipfile
import os
from datetime import datetime
from security import SecurityManager

class BackupManager:
    def __init__(self):
        self.security = SecurityManager()
        
    def create_backup(self, password):
        """Create an encrypted backup of diary entries"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.zip"
        
        with zipfile.ZipFile(backup_file, 'w') as zipf:
            if os.path.exists('diary_entries.json'):
                with open('diary_entries.json', 'r') as f:
                    encrypted_data = f.read()
                    zipf.writestr('diary_entries.json', encrypted_data)
                    
        # Encrypt the entire backup file
        with open(backup_file, 'rb') as f:
            data = f.read()
            encrypted_data = self.security.encrypt_data(data.decode(), password)
            
        with open(backup_file, 'w') as f:
            f.write(encrypted_data)
            
        return backup_file
        
    def restore_backup(self, backup_file, password):
        """Restore diary entries from a backup"""
        with open(backup_file, 'r') as f:
            encrypted_data = f.read()
            decrypted_data = self.security.decrypt_data(encrypted_data, password)
            
        with open(backup_file, 'wb') as f:
            f.write(decrypted_data.encode())
            
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall()
