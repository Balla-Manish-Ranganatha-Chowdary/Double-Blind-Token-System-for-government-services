#!/usr/bin/env python
"""
Database setup script for Government Services Portal
Run this after migrations to create initial data
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.officers.models import Officer

def create_sample_data():
    print("Creating sample admin and officers...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@gov.in',
            password='admin123'
        )
        print("✓ Admin created (username: admin, password: admin123)")
    else:
        print("✓ Admin already exists")
    
    # Create sample officers
    officers_data = [
        {'username': 'officer_revenue_1', 'password': 'officer123', 'department': 'Revenue', 'level': 1},
        {'username': 'officer_revenue_2', 'password': 'officer123', 'department': 'Revenue', 'level': 2},
        {'username': 'officer_police_1', 'password': 'officer123', 'department': 'Police', 'level': 1},
        {'username': 'officer_transport_1', 'password': 'officer123', 'department': 'Transport', 'level': 1},
        {'username': 'officer_municipal_1', 'password': 'officer123', 'department': 'Municipal', 'level': 1},
    ]
    
    for data in officers_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            Officer.objects.create(
                user=user,
                department=data['department'],
                hierarchy_level=data['level']
            )
            print(f"✓ Created {data['username']} ({data['department']}, Level {data['level']})")
        else:
            print(f"✓ {data['username']} already exists")
    
    print("\n✅ Setup complete!")
    print("\nLogin credentials:")
    print("Admin: username=admin, password=admin123")
    print("Officers: username=officer_*, password=officer123")

if __name__ == '__main__':
    create_sample_data()
