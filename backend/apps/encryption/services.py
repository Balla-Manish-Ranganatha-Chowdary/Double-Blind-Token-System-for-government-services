from cryptography.fernet import Fernet
from django.conf import settings
import uuid


class EncryptionService:
    """Double-blind token encryption service"""
    
    def __init__(self):
        # Keys are already base64 encoded strings from .env
        # Fernet expects bytes, so encode them
        key1 = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
        key2 = settings.ENCRYPTION_KEY_SECONDARY.encode() if isinstance(settings.ENCRYPTION_KEY_SECONDARY, str) else settings.ENCRYPTION_KEY_SECONDARY
        
        self.cipher_te1 = Fernet(key1 if key1 else Fernet.generate_key())
        self.cipher_te2 = Fernet(key2 if key2 else Fernet.generate_key())
    
    def generate_token(self):
        """Generate UUID-based token"""
        return str(uuid.uuid4())
    
    def generate_te1_token(self, data: str) -> str:
        """
        Generate TE1 token from data
        First layer encryption - stored with application
        """
        if not data:
            raise ValueError("Data cannot be empty")
        return self.cipher_te1.encrypt(data.encode()).decode()
    
    def generate_te2_token(self, te1_token: str) -> str:
        """
        Generate TE2 token from TE1 token
        Second layer encryption - shown to citizens
        """
        if not te1_token:
            raise ValueError("TE1 token cannot be empty")
        return self.cipher_te2.encrypt(te1_token.encode()).decode()
    
    def decrypt_te1_token(self, te1_token: str) -> str:
        """Decrypt TE1 to original data"""
        if not te1_token:
            raise ValueError("TE1 token cannot be empty")
        return self.cipher_te1.decrypt(te1_token.encode()).decode()
    
    def decrypt_te2_token(self, te2_token: str) -> str:
        """Decrypt TE2 to TE1"""
        if not te2_token:
            raise ValueError("TE2 token cannot be empty")
        return self.cipher_te2.decrypt(te2_token.encode()).decode()
    
    def full_decrypt(self, te2_token: str) -> str:
        """Decrypt from TE2 all the way to original data"""
        te1 = self.decrypt_te2_token(te2_token)
        return self.decrypt_te1_token(te1)
    
    # Backward compatibility aliases
    def encrypt_te1(self, token: str) -> str:
        """Alias for generate_te1_token"""
        return self.generate_te1_token(token)
    
    def encrypt_te2(self, token: str) -> str:
        """Alias for generate_te2_token (encrypts data to TE1 then TE2)"""
        te1 = self.generate_te1_token(token)
        return self.generate_te2_token(te1)
    
    def decrypt_te1(self, te1_token: str) -> str:
        """Alias for decrypt_te1_token"""
        return self.decrypt_te1_token(te1_token)
    
    def decrypt_te2(self, te2_token: str) -> str:
        """Alias for decrypt_te2_token"""
        return self.decrypt_te2_token(te2_token)


# Backward compatibility alias
TokenEncryptionService = EncryptionService
