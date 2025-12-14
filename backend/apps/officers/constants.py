"""
Constants for officer management
Standardized department and service category mappings
"""

# Department choices (used in Officer model)
DEPARTMENTS = [
    ('REVENUE', 'Revenue'),
    ('POLICE', 'Police'),
    ('HEALTH', 'Health'),
    ('EDUCATION', 'Education'),
    ('TRANSPORT', 'Transport'),
    ('MUNICIPAL', 'Municipal'),
    ('CIVIL_SUPPLIES', 'Civil Supplies'),
    ('GENERAL', 'General'),
]

# Service category to department mapping
SERVICE_TO_DEPARTMENT = {
    'LAND_RECORD': 'REVENUE',
    'POLICE_VERIFICATION': 'POLICE',
    'RATION_CARD': 'CIVIL_SUPPLIES',
    'VEHICLE_REGISTRATION': 'TRANSPORT',
    'BUILDING_PERMISSION': 'MUNICIPAL',
    'REVENUE_MUTATION': 'REVENUE',
    'HEALTH_CERTIFICATE': 'HEALTH',
    'EDUCATION_CERTIFICATE': 'EDUCATION',
    'OTHER': 'GENERAL',
}

# Hierarchy levels
HIERARCHY_LEVELS = [
    (1, 'Junior Officer'),
    (2, 'Senior Officer'),
    (3, 'Deputy Director'),
    (4, 'Director'),
]
