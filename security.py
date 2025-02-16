from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import hashlib
import time

class SecurityManager:
    def __init__(self):
        self.password_hash = None
        self.last_activity = time.time()
        
    def set_password(self, password):
        """Hash and store the password"""
        self.password_hash = self._hash_password(password)
        
    def verify_password(self, password):
        """Verify if the entered password is correct"""
        return self.password_hash == self._hash_password(password)
        
    def _hash_password(self, password):
        """Create a secure hash of the password"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def check_inactivity(self):
        """Check if the application should auto-lock"""
        current_time = time.time()
        return (current_time - self.last_activity) > 300  # 5 minutes
        
    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = time.time()
        
    def encrypt_data(self, data, password):
        """Encrypt data using AES"""
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32, count=100000)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(salt + cipher.nonce + tag + ciphertext).decode()
        
    def decrypt_data(self, encrypted_data, password):
        """Decrypt data using AES"""
        data = base64.b64decode(encrypted_data)
        salt = data[:16]
        nonce = data[16:32]
        tag = data[32:48]
        ciphertext = data[48:]
        key = PBKDF2(password, salt, dkLen=32, count=100000)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
