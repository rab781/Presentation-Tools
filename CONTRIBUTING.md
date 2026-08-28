# Contributing to Presentation Control Tool

Thank you for your interest in contributing! Whether you are reporting a bug, suggesting a feature, or writing code, your help is appreciated.

## How to Contribute

1. **Fork the project**: Click the "Fork" button on the top right of the repository page.
2. **Clone your fork**: Download your copy of the repository to your local machine.
   ```bash
   git clone https://github.com/YOUR_USERNAME/Presentation-Tools.git
   cd Presentation-Tools
   ```
3. **Create a branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/AmazingFeature
   ```
4. **Make your changes**: Write your code or documentation. Ensure your code passes all tests and follows existing styling conventions.
5. **Commit your changes**: Write clear, concise commit messages.
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
6. **Push to the branch**: Upload your changes to your fork on GitHub.
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Open a Pull Request**: Go to the original repository and click "New Pull Request" to propose your changes.

## Development Setup

To set up a local development environment, follow the steps in the [Getting Started Tutorial](docs/tutorials/getting-started.md). We recommend using a virtual environment to manage dependencies.

## Testing

Before submitting a Pull Request, ensure that the test suite passes. The project uses Python's built-in `unittest` framework.

Run the tests from the root directory:

```bash
PYTHONPATH=. xvfb-run -a python -m unittest discover tests
```

## Documentation

If you add a new feature or change existing behavior, update the relevant documentation in the `docs/` folder. The project adheres to the [Divio Documentation System](https://documentation.divio.com/), strictly separating content into tutorials, how-to guides, references, and explanations.

## License

By contributing to this project, you agree that your contributions will be licensed under its MIT License.
