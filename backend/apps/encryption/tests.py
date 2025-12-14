"""
Unit tests for encryption services
"""
from django.test import TestCase
from .services import EncryptionService
from cryptography.fernet import InvalidToken


class EncryptionServiceTests(TestCase):
    """Test double-blind token encryption"""
    
    def setUp(self):
        self.service = EncryptionService()
        self.test_data = "TEST123456"
    
    def test_generate_te1_token(self):
        """Test TE1 token generation"""
        te1 = self.service.generate_te1_token(self.test_data)
        self.assertIsNotNone(te1)
        self.assertIsInstance(te1, str)
        self.assertGreater(len(te1), 0)
    
    def test_generate_te2_token(self):
        """Test TE2 token generation"""
        te1 = self.service.generate_te1_token(self.test_data)
        te2 = self.service.generate_te2_token(te1)
        self.assertIsNotNone(te2)
        self.assertIsInstance(te2, str)
        self.assertNotEqual(te1, te2)
    
    def test_decrypt_te1_token(self):
        """Test TE1 token decryption"""
        te1 = self.service.generate_te1_token(self.test_data)
        decrypted = self.service.decrypt_te1_token(te1)
        self.assertEqual(decrypted, self.test_data)
    
    def test_decrypt_te2_token(self):
        """Test TE2 token decryption"""
        te1 = self.service.generate_te1_token(self.test_data)
        te2 = self.service.generate_te2_token(te1)
        decrypted_te1 = self.service.decrypt_te2_token(te2)
        self.assertEqual(decrypted_te1, te1)
    
    def test_full_encryption_cycle(self):
        """Test complete encryption and decryption cycle"""
        # Encrypt
        te1 = self.service.generate_te1_token(self.test_data)
        te2 = self.service.generate_te2_token(te1)
        
        # Decrypt
        decrypted_te1 = self.service.decrypt_te2_token(te2)
        decrypted_data = self.service.decrypt_te1_token(decrypted_te1)
        
        self.assertEqual(decrypted_data, self.test_data)
    
    def test_invalid_token_decryption(self):
        """Test decryption with invalid token"""
        with self.assertRaises(Exception):
            self.service.decrypt_te1_token("invalid_token")
    
    def test_empty_data_encryption(self):
        """Test encryption with empty data"""
        with self.assertRaises(Exception):
            self.service.generate_te1_token("")
    
    def test_none_data_encryption(self):
        """Test encryption with None data"""
        with self.assertRaises(Exception):
            self.service.generate_te1_token(None)
