# Contributing to GitMuse

First off, thank you for considering contributing to GitMuse! It's people like you that make GitMuse such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples** to demonstrate the steps
* **Describe the behavior you observed** and what you expected
* **Include screenshots** if possible
* **Include your environment details** (OS, Python version, GitMuse version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description** of the suggested enhancement
* **Provide specific examples** to demonstrate the enhancement
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include tests for new features
* Update documentation as needed
* End all files with a newline

## Development Process

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/gitmuse.git
cd gitmuse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gitmuse tests/

# Run specific test file
pytest tests/test_analyzer.py
```

### Code Style

We use several tools to maintain code quality:

```bash
# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### Commit Messages

Please use GitMuse to generate your commit messages! 😉

But seriously, follow Conventional Commits:
* `feat`: A new feature
* `fix`: A bug fix
* `docs`: Documentation changes
* `style`: Code style changes (formatting, etc.)
* `refactor`: Code refactoring
* `test`: Adding or updating tests
* `chore`: Maintenance tasks

## Project Structure

```
gitmuse/
├── src/gitmuse/          # Main source code
│   ├── ai/               # AI provider implementations
│   ├── generators/       # Commit message generators
│   ├── cli.py            # Command-line interface
│   ├── analyzer.py       # Git diff analyzer
│   └── config.py         # Configuration manager
├── tests/                # Test files
├── docs/                 # Documentation
└── examples/             # Usage examples
```

## Adding a New AI Provider

To add support for a new AI provider:

1. Create a new file in `src/gitmuse/ai/your_provider.py`
2. Implement the `BaseAIProvider` interface
3. Add it to the factory in `ai/factory.py`
4. Add tests in `tests/test_ai_providers.py`
5. Update documentation

## Release Process

1. Update version in `setup.py` and `__init__.py`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. CI will automatically publish to PyPI

## Questions?

Feel free to open an issue or reach out to the maintainers!

Thank you for contributing! 🎉
