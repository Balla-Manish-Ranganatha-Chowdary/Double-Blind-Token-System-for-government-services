#!/usr/bin/env python
"""
Generate encryption keys for the double-blind token system
"""

from cryptography.fernet import Fernet

print("Generating encryption keys for double-blind token system...\n")

key1 = Fernet.generate_key().decode()
key2 = Fernet.generate_key().decode()

print("Add these to your .env file:\n")
print(f"ENCRYPTION_KEY={key1}")
print(f"ENCRYPTION_KEY_SECONDARY={key2}")
print("\nKeep these keys secure and never commit them to version control!")
