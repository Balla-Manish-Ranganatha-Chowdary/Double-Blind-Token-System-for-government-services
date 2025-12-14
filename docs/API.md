# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### Applications

#### Submit Application
```
POST /applications/submit/
Content-Type: multipart/form-data

Body:
- name: string
- age: integer
- address: string
- aadhaar: string (12 digits)
- files: file[] (PDF files)

Response:
{
  "token": "encrypted_te1_token",
  "message": "Application submitted successfully",
  "application_id": 1
}
```

#### Check Status
```
GET /applications/status/{token}/

Response:
{
  "id": 1,
  "token_te1": "...",
  "service_category": "LAND_RECORD",
  "status": "ASSIGNED",
  "created_at": "2024-01-01T00:00:00Z",
  "files": [...]
}
```

### Officers

#### List Officers
```
GET /officers/
Authorization: Required

Response:
[
  {
    "id": 1,
    "username": "officer1",
    "hierarchy_level": 1,
    "department": "Revenue",
    "workload_count": 5
  }
]
```

## Status Values
- SUBMITTED
- CLASSIFIED
- REDACTION_CLEARED
- ASSIGNED
- IN_REVIEW
- FORWARDED
- APPROVED
- REJECTED

## Service Categories
- LAND_RECORD
- POLICE_VERIFICATION
- RATION_CARD
- VEHICLE_REGISTRATION
- BUILDING_PERMISSION
- REVENUE_MUTATION
- OTHER
