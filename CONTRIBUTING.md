# Contributing to Learning Path Analyzer

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes:
   ```bash
   pytest tests/ -v
   ```
5. Make sure your code lints:
   ```bash
   flake8 src tests
   black --check src tests
   ```

### Report Bugs

Report bugs by creating a GitHub issue. Include:

- **Summary**: Brief description of the issue
- **Steps to Reproduce**: How to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, etc.

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for all functions
- Keep functions focused and modular
- Maximum line length: 88 characters (black default)

### Testing

All new features should include tests. Run tests with:

```bash
pytest tests/ -v --cov=src
```

Aim for >85% code coverage.

### Documentation

Update README.md and docstrings when:
- Adding new features
- Changing existing functionality
- Modifying API
- Adding dependencies

## Development Setup

```bash
# Clone and set up
git clone https://github.com/RoadToDestiny/learning-path-analyzer.git
cd learning-path-analyzer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black

# Run tests
pytest

# Format code
black src tests

# Lint code
flake8 src tests
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Reference issues: "Fixes #123" or "Related to #456"

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Community

Contributor Code of Conduct: Be respectful and inclusive. This project is open to everyone.

Thank you for contributing! 🎉
