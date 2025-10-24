# Contributing to Cogniz Memory Skills

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behaviors**:
- Trolling, insulting/derogatory comments, personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct reasonably considered inappropriate

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details**:
  - OS and version
  - Python version
  - Claude platform (Code/Web/API)
  - Skill version

**Template**:
```markdown
### Description
[Clear description of the bug]

### Steps to Reproduce
1. Go to '...'
2. Execute '...'
3. See error

### Expected Behavior
[What you expected to happen]

### Actual Behavior
[What actually happened]

### Environment
- OS: [e.g., Windows 11]
- Python: [e.g., 3.11.5]
- Claude Platform: [e.g., Claude Code 1.2.0]
- Skill: [e.g., memory-optimizer v2.0.0]

### Additional Context
[Any other relevant information]
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Use case**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about
- **Impact**: Who benefits from this enhancement?

### Pull Requests

1. **Fork the repository** and create your branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**:
   - Follow code style guidelines (see below)
   - Add tests if applicable
   - Update documentation
   - Keep commits atomic and well-described

3. **Test your changes**:
   ```bash
   # Run tests (if available)
   pytest tests/

   # Test manually with Claude
   # Verify skill loads and functions correctly
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "feat: Add export to PDF feature for account briefings"
   git commit -m "fix: Handle missing project_id gracefully"
   git commit -m "docs: Update installation guide for macOS"
   ```

   Use conventional commit format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation only
   - `style:` Formatting, missing semicolons, etc.
   - `refactor:` Code restructuring
   - `test:` Adding tests
   - `chore:` Maintenance tasks

5. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**:
   - Use the PR template
   - Link related issues
   - Request review from maintainers

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Claude Code or Claude.ai account (for testing)
- Cogniz Memory Platform account

### Setup Steps

```bash
# Clone your fork:
git clone https://github.com/YOUR-USERNAME/Claude_skills.git
cd Claude_skills

# Add upstream remote:
git remote add upstream https://github.com/cognizonline/Claude_skills.git

# Create virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies:
pip install -r requirements.txt

# Install dev dependencies (optional):
pip install pytest black mypy
```

### Running Tests

```bash
# Run all tests:
pytest tests/

# Run specific test file:
pytest tests/test_optimizer.py

# Run with verbose output:
pytest -v

# Run with coverage:
pytest --cov=. --cov-report=html
```

## Code Style Guidelines

### Python Code

Follow [PEP 8](https://pep8.org/) style guide:

```bash
# Format with Black (recommended):
black .

# Check with Flake8:
flake8 .

# Type checking with mypy:
mypy .
```

**Key conventions**:
- Use 4 spaces for indentation
- Max line length: 100 characters (scripts), 88 (Black default)
- Use type hints for function signatures
- Write docstrings for all public functions

**Example**:
```python
def optimize_memories(
    memories: List[MemoryItem],
    mode: str = "optimize",
    options: Optional[Dict[str, Any]] = None
) -> OptimizationResult:
    """
    Optimize memory content and metadata.

    Args:
        memories: List of memory items to process
        mode: Optimization mode ('analyze', 'optimize', 'report')
        options: Optional configuration dictionary

    Returns:
        OptimizationResult with savings and improvements

    Raises:
        ValueError: If mode is invalid
    """
    ...
```

### SKILL.md Format

Follow Anthropic's Skills Specification:

```markdown
---
name: skill-name
description: Clear description of what the skill does and when to use it
version: 2.0.0
---

# Skill Name

[Brief introduction]

## Activation Triggers
- When X happens
- When user asks for Y

## Requirements
1. Requirement 1
2. Requirement 2

## Bundled Resources
- `scripts/script.py` - Description
- `references/doc.md` - Description
- `assets/template.md` - Description

## Standard Operating Procedure
[Step-by-step instructions]

## Security & Governance
[Data handling, permissions, compliance]

## Resilience & Observability
[Error handling, logging, monitoring]

## References
- [Link 1]
- [Link 2]
```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Examples**:
```
feat(memory-optimizer): add dry-run mode for preview
fix(account-briefing): handle missing account tag gracefully
docs(readme): update installation instructions for Windows
chore: bump dependencies to latest versions
```

## Skill Development Guidelines

### Creating a New Skill

1. **Choose appropriate name**: Use `memory-` prefix for memory management skills

2. **Create directory structure**:
   ```bash
   mkdir -p new-skill/{scripts,references,assets}
   ```

3. **Create SKILL.md**:
   - Follow template in `template-skill/`
   - Include clear activation triggers
   - Document all dependencies

4. **Add helper scripts** (if needed):
   - Use argument parsing with `argparse`
   - Include `--verbose` flag for debugging
   - Handle errors gracefully

5. **Write documentation**:
   - Add README.md to skill directory
   - Include usage examples
   - Document configuration

6. **Test thoroughly**:
   - Test in Claude Code
   - Test in Claude.ai
   - Test edge cases

### Skill Quality Checklist

Before submitting:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] Description clearly states when to use the skill
- [ ] All scripts are executable and have proper shebang
- [ ] Dependencies are documented
- [ ] Configuration requirements are clear
- [ ] Error messages are helpful
- [ ] Security considerations are addressed
- [ ] Examples demonstrate key use cases
- [ ] README.md exists (if complex skill)
- [ ] Tested in at least one Claude platform

## Documentation Guidelines

### Writing Style

- Use clear, concise language
- Write in active voice
- Use examples to illustrate concepts
- Include command examples that users can copy-paste
- Add warnings/notes for important information

### Markdown Formatting

```markdown
# Headers follow ATX style (use #, ##, ###)

**Bold** for emphasis, *italic* for terms

`inline code` for commands, filenames, code

```code blocks```
for multi-line code/commands

- Bullet lists for unordered items
1. Numbered lists for sequential steps

[Links](https://example.com) with descriptive text

> Blockquotes for important notes
```

## Testing Guidelines

### Manual Testing

For each skill:

1. **Installation test**: Verify skill loads correctly
2. **Basic functionality**: Test primary use case
3. **Edge cases**: Test with missing/invalid inputs
4. **Error handling**: Verify graceful failures
5. **Documentation**: Confirm examples work

### Automated Testing (if applicable)

```python
# tests/test_skill.py
import pytest
from skills.memory_optimizer import optimize

def test_optimization_reduces_size():
    """Test that optimization reduces memory size"""
    original = {"content": "  test  \n\n\n"}
    result = optimize(original)
    assert len(result["content"]) < len(original["content"])

def test_optimization_preserves_meaning():
    """Test that optimization preserves semantic content"""
    original = {"content": "important text"}
    result = optimize(original)
    assert "important text" in result["content"]
```

## Review Process

### What Reviewers Look For

- **Code quality**: Follows style guidelines
- **Functionality**: Works as intended
- **Tests**: Adequate test coverage
- **Documentation**: Clear and complete
- **Security**: No vulnerabilities introduced
- **Performance**: No significant regressions

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Breaking changes are documented

## Release Process

Maintainers will:

1. Review and merge approved PRs
2. Update CHANGELOG.md
3. Tag release with semantic version
4. Publish to GitHub releases
5. Update documentation site

## Community

### Getting Help

- **Questions**: [GitHub Discussions](https://github.com/cognizonline/Claude_skills/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/cognizonline/Claude_skills/issues)
- **Email**: support@cogniz.online

### Recognition

Contributors will be recognized in:
- Repository README
- Release notes
- Contributors page

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

**Thank you for contributing to Cogniz Memory Skills!** 🎉

Your efforts help make AI-powered knowledge management better for everyone.

[← Back to README](README.md)
