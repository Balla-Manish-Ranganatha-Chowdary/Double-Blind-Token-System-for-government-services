# System Architecture

## Double-Blind Token System

### Token Layers
1. **Original Token**: UUID generated on submission
2. **TE1 (Token Encryption Layer 1)**: AES-256 encrypted, stored with user data, shown to citizens
3. **TE2 (Token Encryption Layer 2)**: Second encryption layer, shown to officers

### Flow
```
Citizen submits → Generate UUID → Encrypt to TE1 → Encrypt to TE2
                                      ↓                ↓
                                  User sees TE1    Officer sees TE2
```

Officers cannot reverse TE2 to identify citizens. System decrypts only when needed for final processing.

## AI Modules

### Classification AI
- Extracts text from uploaded PDFs
- Keyword-based classification (upgradeable to ML models)
- Maps to service categories
- Routes to appropriate officer hierarchy

### Redaction AI
- Scans for PII patterns (Aadhaar, phone, names)
- Auto-rejects if identity data found
- Prevents officer-citizen identification

## Database Schema

### Core Tables
- **citizens**: User PII (encrypted)
- **officers**: Officer details, hierarchy, workload
- **applications**: Application lifecycle with double-blind tokens
- **application_files**: Uploaded documents
- **token_mappings**: Secure token relationships

## Security Layers
1. End-to-end encryption
2. Row-level database security
3. Double-blind token isolation
4. AI-powered PII detection
5. Audit logging

## Scalability
- Horizontal scaling for AI services
- Load-balanced Django instances
- PostgreSQL connection pooling
- Async task processing with Celery
