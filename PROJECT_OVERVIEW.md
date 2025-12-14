# Government Services Portal - Double-Blind Token System

## Project Summary

A full-stack web application that revolutionizes government service delivery by implementing a double-blind token system to eliminate corruption. The system ensures that citizens don't know which officer is reviewing their application, and officers don't know whose application they're reviewing.

## Core Innovation: Double-Blind Token System

### How It Works

1. **Token Generation**: When a citizen submits an application, a unique UUID token is generated
2. **First Encryption (TE1)**: Token is encrypted using AES-256 (Fernet) - shown to citizens
3. **Second Encryption (TE2)**: TE1 is encrypted again with a different key - shown to officers
4. **Isolation**: Officers only see TE2 and cannot decrypt it to identify the citizen
5. **Decryption**: System decrypts tokens only when needed for final processing

### Why This Prevents Corruption

- **No Identity Visibility**: Officers cannot see applicant names, addresses, or any identifying information
- **No Officer Selection**: Citizens cannot choose or know which officer handles their case
- **Automated Assignment**: AI assigns applications based on workload and hierarchy
- **Audit Trail**: All actions are logged but identities remain encrypted during review

## System Architecture

### Frontend (Next.js 14)
- **Citizen Pages**: Home, Apply, Check Status
- **Officer Pages**: Login, Dashboard (view/approve/reject applications)
- **Admin Pages**: Login, Analytics Dashboard, Officer Management

### Backend (Django 5 + DRF)
- **Authentication**: Token-based auth for officers/admins
- **Encryption Service**: Double-blind token encryption/decryption
- **AI Services**: 
  - Document classification (determines service category)
  - PII detection (auto-rejects if personal info found in PDFs)
- **Assignment Algorithm**: Workload-based officer assignment with hierarchy support
- **Analytics**: Real-time dashboard for admins

### Database (PostgreSQL)
- **Citizens**: Encrypted personal information
- **Officers**: Hierarchy, department, workload tracking
- **Applications**: Double-encrypted tokens, status tracking
- **Files**: Uploaded documents with redaction flags

## Key Features Implemented

### ✅ User Portal
- [x] Home page explaining the project
- [x] Application submission form (name, age, address, Aadhaar)
- [x] PDF document upload
- [x] Token generation and display
- [x] Status tracking by token
- [x] No service selection (AI determines category)

### ✅ Officer Portal
- [x] Login required (no signup)
- [x] Dashboard showing assigned applications
- [x] View anonymized applications (TE2 tokens only)
- [x] View uploaded documents
- [x] Approve/Reject functionality
- [x] Multi-level approval forwarding

### ✅ Admin Portal
- [x] Login required (no signup)
- [x] Analytics dashboard with:
  - Total applications
  - Approval/rejection rates
  - Status breakdown
  - Service category distribution
  - Officer workload distribution
  - Recent applications (last 7 days)
- [x] Officer management page:
  - Add new officers
  - View all officers
  - Deactivate officers
  - Set department and hierarchy level

### ✅ AI Agents
- [x] **Classification AI**: Reads PDF content and determines service category
  - Categories: Land Record, Police Verification, Ration Card, Vehicle Registration, Building Permission, Revenue Mutation
- [x] **Redaction AI**: Scans documents for PII before assignment
  - Detects: Names, Aadhaar numbers, phone numbers
  - Auto-rejects applications with personal identifiers

### ✅ Security Features
- [x] Double-blind token encryption (TE1 + TE2)
- [x] Token-based authentication
- [x] No signup for officers/admins (admin creates accounts)
- [x] Encrypted file storage
- [x] CORS protection
- [x] SQL injection protection (Django ORM)

### ✅ Workflow Automation
- [x] Automatic service classification
- [x] Automatic PII detection and rejection
- [x] Workload-based officer assignment
- [x] Multi-level approval routing
- [x] Hierarchy-aware forwarding

## Application Lifecycle

```
1. SUBMITTED → Citizen submits application
2. CLASSIFIED → AI determines service category
3. REDACTION_CLEARED → AI confirms no PII in documents
4. ASSIGNED → Assigned to officer based on workload
5. IN_REVIEW → Officer is reviewing
6. FORWARDED → Sent to next hierarchy level (if needed)
7. APPROVED / REJECTED → Final decision
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 14 (React, TypeScript) |
| Backend | Django 5.0 + Django REST Framework |
| Database | PostgreSQL 15+ |
| Authentication | Token Authentication (DRF) |
| Encryption | Cryptography (Fernet) |
| AI/ML | PyPDF2, spaCy, transformers |
| File Storage | Django FileField (upgradeable to S3) |

## API Endpoints

### Public Endpoints
- `POST /api/applications/submit/` - Submit application
- `GET /api/applications/status/{token}/` - Check status

### Officer Endpoints (Auth Required)
- `GET /api/applications/officer/list/` - List assigned applications
- `POST /api/applications/officer/action/{id}/` - Approve/reject

### Admin Endpoints (Admin Auth Required)
- `GET /api/analytics/dashboard/` - Analytics data
- `GET /api/officers/` - List all officers
- `POST /api/officers/create/` - Create officer
- `PATCH /api/officers/update/{id}/` - Update officer
- `DELETE /api/officers/delete/{id}/` - Deactivate officer

## UI Design Philosophy

- **Minimalist**: Clean layouts, ample whitespace
- **Professional**: Government-grade appearance
- **Functional**: Focus on usability over aesthetics
- **Accessible**: Clear typography, good contrast
- **Responsive**: Works on desktop and mobile

## Security Considerations

1. **Encryption Keys**: Stored in environment variables, never in code
2. **Password Hashing**: Django's built-in PBKDF2 algorithm
3. **Token Security**: Unique tokens per session, stored securely
4. **File Upload**: Validated file types, size limits
5. **SQL Injection**: Protected by Django ORM
6. **XSS Protection**: React's built-in escaping
7. **CSRF Protection**: Django middleware

## Future Enhancements

- [ ] Advanced ML models for classification (BERT/RoBERTa)
- [ ] OCR for scanned documents
- [ ] Real-time notifications
- [ ] SMS/Email alerts
- [ ] Mobile app
- [ ] Blockchain audit trail
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with existing government systems

## Project Structure

```
/
├── backend/
│   ├── apps/
│   │   ├── users/          # Citizen management
│   │   ├── officers/       # Officer management & assignment
│   │   ├── applications/   # Application lifecycle
│   │   ├── encryption/     # Double-blind token service
│   │   ├── ai_services/    # Classification & redaction
│   │   └── analytics/      # Admin analytics
│   ├── config/             # Django settings
│   ├── manage.py
│   ├── requirements.txt
│   └── setup_db.py         # Initial data setup
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx              # Home
│   │       ├── apply/                # Application form
│   │       ├── status/               # Status check
│   │       ├── officer/
│   │       │   ├── login/            # Officer login
│   │       │   └── dashboard/        # Officer dashboard
│   │       └── admin/
│   │           ├── login/            # Admin login
│   │           ├── dashboard/        # Analytics
│   │           └── officers/         # Officer management
│   ├── package.json
│   └── next.config.js
│
├── docs/                   # Documentation
├── README.md
├── SETUP_INSTRUCTIONS.md
└── PROJECT_OVERVIEW.md
```

## Testing Checklist

- [ ] Submit application without PII in documents → Should succeed
- [ ] Submit application with name in PDF → Should auto-reject
- [ ] Check status with valid token → Should show status
- [ ] Officer login and view applications → Should see TE2 tokens only
- [ ] Officer approve application → Should update status
- [ ] Multi-level approval → Should forward to next hierarchy
- [ ] Admin view analytics → Should show all metrics
- [ ] Admin create officer → Should create successfully
- [ ] Admin deactivate officer → Should mark inactive

## License

This project is intended for educational and government use.
