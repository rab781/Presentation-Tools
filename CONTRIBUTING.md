# Contributing to Presentation Control Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to the repository.

## Development Setup

1. Fork the project.
2. Clone your fork locally.
3. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Pull Request Process

1. Create a feature branch (`git checkout -b feature/AmazingFeature`).
2. Make your changes.
3. If you add new functionality, please include tests and update the documentation in the `docs/` folder.
4. Ensure all tests pass.
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
6. Push to the branch (`git push origin feature/AmazingFeature`).
7. Open a Pull Request.

## Documentation Guidelines

We treat documentation as code. Every new feature must ship with documentation, and code without docs is considered incomplete.

We use the Divio Documentation System. Please place your documentation in the appropriate directory under `docs/`:

- `docs/tutorials/`: Learning-oriented, step-by-step guides.
- `docs/how-to/`: Task-oriented guides for solving specific problems.
- `docs/reference/`: Information-oriented technical descriptions (e.g., API docs, lists of commands).
- `docs/explanation/`: Understanding-oriented discussions of background concepts.

Do not mix these types in a single file. Keep the voice consistent: use the second person ("you"), present tense, and active voice (except for step-by-step instructions, which should use the imperative mood).