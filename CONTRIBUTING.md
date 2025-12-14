# Contributing to Double-Blind Token System for Government Services

First off, thank you for considering contributing to the Double-Blind Token System for Government Services! It's people like you that make this project a great tool for eliminating corruption in government services.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

---

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@example.com].

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions you've considered**

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- `good-first-issue` - Issues that should only require a few lines of code
- `help-wanted` - Issues that are a bit more involved

### Pull Requests

- Fill in the required template
- Follow the coding standards
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

---

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

### Setup Steps

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/Double-Blind-Token-System-for-Government-Services.git
cd Double-Blind-Token-System-for-Government-Services
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

4. **Setup database**
```bash
createdb gov_services_db
cd backend
python manage.py migrate
python setup_db.py
```

5. **Create a branch**
```bash
git checkout -b feature/your-feature-name
```

---

## Coding Standards

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** where applicable
- Maximum line length: **88 characters** (Black formatter)
- Use **docstrings** for all functions and classes

**Example**:
```python
def calculate_workload(officer: Officer) -> int:
    """
    Calculate the current workload of an officer.
    
    Args:
        officer: The Officer instance to calculate workload for
        
    Returns:
        int: The current workload count
    """
    return officer.workload_count
```

### JavaScript/TypeScript (Frontend)

- Follow **Airbnb JavaScript Style Guide**
- Use **TypeScript** for type safety
- Use **functional components** with hooks
- Maximum line length: **100 characters**

**Example**:
```typescript
interface ApplicationProps {
  id: string;
  status: string;
}

const Application: React.FC<ApplicationProps> = ({ id, status }) => {
  // Component logic
  return <div>{status}</div>;
};
```

### General Guidelines

- Write **self-documenting code**
- Add **comments** for complex logic
- Keep functions **small and focused**
- Use **meaningful variable names**
- Avoid **magic numbers** - use constants

---

## Commit Guidelines

We follow the **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(encryption): add support for RSA encryption

Add RSA encryption as an alternative to Fernet for larger data.
Includes key generation and encryption/decryption methods.

Closes #123
```

```bash
fix(assignment): correct department mapping for HEALTH category

The HEALTH service category was incorrectly mapped to REVENUE
department. Updated mapping in constants.py.

Fixes #456
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** if you've changed APIs
2. **Add tests** for new functionality
3. **Run all tests** and ensure they pass
4. **Run linters** and fix any issues
5. **Update CHANGELOG.md** with your changes

### Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No merge conflicts

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Added tests
- [ ] Tests passing
```

---

## Testing Guidelines

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test --verbosity=2

# Frontend tests (when available)
cd frontend
npm test

# Load tests
k6 run loadtest.js
```

### Writing Tests

#### Backend (Django)

```python
from django.test import TestCase
from apps.encryption.services import EncryptionService

class EncryptionServiceTests(TestCase):
    def setUp(self):
        self.service = EncryptionService()
    
    def test_generate_te1_token(self):
        """Test TE1 token generation"""
        token = self.service.generate_te1_token("TEST123")
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
```

#### Frontend (React)

```typescript
import { render, screen } from '@testing-library/react';
import Application from './Application';

describe('Application Component', () => {
  it('renders application status', () => {
    render(<Application id="123" status="APPROVED" />);
    expect(screen.getByText('APPROVED')).toBeInTheDocument();
  });
});
```

### Test Coverage

- Aim for **80%+ code coverage**
- All new features must include tests
- Bug fixes should include regression tests

---

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include parameter types and return types
- Provide usage examples for complex functions

### Project Documentation

When adding new features, update:

- `README.md` - If it affects setup or usage
- `docs/API.md` - If you add/modify API endpoints
- `docs/ARCHITECTURE.md` - If you change system design
- Relevant guides in the docs folder

---

## Review Process

### What We Look For

1. **Code Quality**: Clean, readable, maintainable
2. **Testing**: Adequate test coverage
3. **Documentation**: Clear and complete
4. **Performance**: No unnecessary performance hits
5. **Security**: No security vulnerabilities

### Timeline

- Initial review: Within 3 business days
- Follow-up reviews: Within 2 business days
- Merge: After approval from 2 maintainers

---

## Getting Help

### Resources

- 📖 [Documentation](docs/)
- 💬 [GitHub Discussions](https://github.com/yourusername/Double-Blind-Token-System-for-Government-Services/discussions)
- 🐛 [Issue Tracker](https://github.com/yourusername/Double-Blind-Token-System-for-Government-Services/issues)

### Contact

- Email: dev@example.com
- Discord: [Join our server]
- Twitter: [@YourHandle]

---

## Recognition

Contributors will be:

- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in the project README

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License with **no patent claims or proprietary rights**.

### Open Source Commitment

All contributions to this project:
- ✅ Are **100% open source** under MIT License
- ✅ Have **no patent restrictions**
- ✅ Can be used **freely by anyone** for any purpose
- ✅ Become part of the **public good**

You retain copyright to your contributions, but grant the community the right to use them under the MIT License.

---

Thank you for contributing to make government services more transparent and corruption-free! 🎉
