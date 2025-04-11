# Contributing to Ubuntu AI RPA Agent

Thank you for considering contributing to the Ubuntu AI RPA Agent! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. **Fork the repository**

2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/ubuntu-ai-rpa-agent.git
   cd ubuntu-ai-rpa-agent
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add comments for complex logic

5. **Test your changes**
   - Make sure your code works as expected
   - Test edge cases

6. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit a pull request**
   - Provide a clear title and description
   - Reference any related issues

## Development Setup

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install flake8 black isort pytest
   ```

3. Format code before committing:
   ```bash
   black .
   isort .
   ```

## Adding New Features

When adding new features, please consider:

1. **UI Template Detection**
   - Add support for new UI elements
   - Improve detection algorithm

2. **Command Execution**
   - Add new command types
   - Enhance existing commands

3. **LLM Integration**
   - Support for additional models
   - Improve prompting strategy

4. **Documentation**
   - Update README.md
   - Add comments to code
   - Update template examples

## Reporting Bugs

If you find a bug, please create an issue with:
- A clear title and description
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment details

## Feature Requests

Feature requests are welcome! Please provide:
- A clear title and description
- Why the feature would be useful
- Any implementation ideas you have

Thank you for contributing!
