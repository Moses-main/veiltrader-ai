# Contributing to VeilTrader AI

Thank you for your interest in contributing to VeilTrader AI! This document provides guidelines and instructions for contributing to this project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Code Style](#code-style)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Encouraged behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors:**
- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Python 3.12+** installed
2. **Git** installed and configured
3. **GitHub account** for creating pull requests
4. Basic understanding of:
   - DeFi and Ethereum
   - Uniswap V3
   - ERC-8004 standard
   - LLM integration

### Repository Structure

```
veiltrader-ai/
├── main.py                 # Entry point + FastAPI server
├── core.py                 # LLM brain + portfolio reader
├── llm_brain.py            # Privacy-first LLM routing
├── portfolio_reader.py     # On-chain balance reader
├── uniswap_executor.py     # Uniswap V3 swap executor
├── reputation_manager.py   # ERC-8004 integration
├── register_agent.py       # Agent registration
├── common.py               # Shared utilities
├── streamlit_app.py        # Dashboard UI
├── tests/                  # Test suite
├── docs/                   # Documentation
├── README.md               # Project overview
├── CONTRIBUTING.md         # This file
└── LICENSE                 # MIT License
```

---

## Development Setup

### 1. Fork the Repository

```bash
# Click "Fork" on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/veiltrader-ai.git
cd veiltrader-ai
```

### 2. Add Upstream Remote

```bash
git remote add upstream https://github.com/originalowner/veiltrader-ai.git
git fetch upstream
```

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt  # If exists
pip install pytest pytest-cov black ruff mypy
```

### 5. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your test configuration
```

### 6. Verify Setup

```bash
python -c "from common import w3; print(w3().is_connected())"
```

---

## Making Changes

### 1. Create a Feature Branch

```bash
# Always create from develop or main
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
# or
git checkout -b docs/documentation-improvement
```

### 2. Branch Naming Conventions

| Type | Example |
|------|---------|
| Feature | `feature/add-uniswap-v4-support` |
| Bug Fix | `fix/slippage-calculation-error` |
| Documentation | `docs/update-api-reference` |
| Refactor | `refactor/llm-fallback-logic` |
| Test | `test/add-integration-tests` |

### 3. Make Your Changes

- Write clean, commented code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_uniswap_executor.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type Categories

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style (formatting, no logic change) |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvements |
| `ci` | CI/CD changes |

### Examples

```bash
# Good commit messages
git commit -m "feat(uniswap): add support for dynamic fee tiers"
git commit -m "fix(slippage): correct calculation for small trades"
git commit -m "docs(api): update trade-signal endpoint documentation"
git commit -m "test(llm): add integration tests for fallback chain"

# Bad commit messages (avoid)
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "asdfasdf"
```

### Commit Best Practices

- Use imperative mood: "Add feature" not "Added feature"
- Keep subject line under 50 characters
- Separate subject from body with blank line
- Body should explain *what* and *why*, not *how*
- Reference issues: "Fixes #123" or "Closes #456"

---

## Pull Request Process

### 1. Update Your Branch

```bash
git checkout feature/your-feature
git rebase upstream/main  # or upstream/develop
```

### 2. Run Tests

```bash
# All tests must pass
pytest tests/ -v

# Code style check
black --check .
ruff check .
mypy .
```

### 3. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 4. Create Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No linting errors
```

### 5. PR Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, maintainers will merge

---

## Testing

### Test File Structure

```python
# tests/test_module_name.py
import pytest
from module_name import function_to_test

class TestModuleName:
    """Test suite for module_name"""
    
    def test_function_works(self):
        """Test that function returns expected result"""
        result = function_to_test(input_value)
        assert result == expected_output
    
    def test_function_handles_error(self):
        """Test that function raises appropriate error"""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

### Running Tests

```bash
# All tests
pytest tests/

# With coverage report
pytest tests/ --cov=. --cov-report=html --cov-report=term

# Watch mode (rerun on changes)
ptw  # pytest-watch

# Specific test
pytest tests/test_uniswap_executor.py::TestUniswapExecutor::test_quote -v
```

### Test Categories

| Category | Location | Description |
|----------|----------|-------------|
| Unit | `tests/unit/` | Individual function tests |
| Integration | `tests/integration/` | Component interaction tests |
| E2E | `tests/e2e/` | Full system tests (requires testnet) |

---

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

```bash
# Format code
black .

# Check formatting
black --check .

# Lint code
ruff check .

# Type checking
mypy .
```

### Style Rules

1. **Line Length**: 100 characters max
2. **Indentation**: 4 spaces
3. **String Quotes**: Double quotes preferred
4. **Imports**: Alphabetical, grouped by stdlib/external/local

### Import Organization

```python
# Standard library
import os
import json
from datetime import datetime

# Third-party
import requests
from web3 import Web3

# Local application
from common import w3
from core import get_trading_decision
```

### Docstring Format

```python
def function_name(param1: str, param2: int) -> dict:
    """
    Brief description of function.
    
    Longer explanation if needed. Can span multiple lines
    and include examples.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid input provided
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        {'status': 'success'}
    """
    pass
```

---

## Reporting Issues

### Before Submitting

- Search existing issues first
- Verify with latest version
- Check if issue is reproducible

### Issue Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Run '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.12.0]
- Branch: [e.g., main]

**Screenshots** (if applicable)

**Additional Context**
Any other relevant information
```

---

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of proposed feature

**Problem Solved**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other solutions considered

**Additional Context**
Mockups, examples, or implementation ideas
```

---

## Questions?

- Open an issue for bugs or feature requests
- Join discussions in the repository
- Check existing documentation first

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<p align="center">
  Thank you for contributing to VeilTrader AI! 💜
</p>
