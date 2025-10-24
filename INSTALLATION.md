# Installation Guide

Comprehensive installation instructions for Cogniz Memory Skills across all Claude platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Claude Code (VS Code)](#claude-code-vs-code)
  - [Claude.ai Web](#claudeai-web)
  - [Claude API](#claude-api)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

1. **Claude Access** (one of):
   - Claude Code extension for VS Code
   - Claude.ai Pro, Team, or Enterprise plan
   - Claude API access with code execution enabled

2. **Cogniz Memory Platform** account:
   - Sign up at [cogniz.online](https://cogniz.online)
   - Free tier available
   - Generate API key from Settings

### Optional (for Python scripts)

3. **Python 3.8 or higher**
   - Download from [python.org](https://python.org)
   - Verify: `python --version` or `python3 --version`

4. **Git** (for cloning repository)
   - Download from [git-scm.com](https://git-scm.com)
   - Verify: `git --version`

---

## Installation Methods

### Claude Code (VS Code)

The easiest method for developers using VS Code.

#### Step 1: Install Claude Code Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "Claude Code"
4. Click **Install**

#### Step 2: Install Skills via Marketplace

```bash
# In VS Code terminal or Claude Code chat:
/plugin marketplace add cognizonline/Claude_skills

# Install all skills:
/plugin install cogniz-memory-skills

# Or install individual skills:
/plugin install memory-optimizer@cogniz-memory-skills
/plugin install memory-account-briefing@cogniz-memory-skills
```

#### Step 3: Verify Installation

```bash
# List installed skills:
/plugin list
```

You should see all 14 Cogniz Memory Skills listed.

---

### Claude.ai Web

For users on Claude.ai Pro, Team, or Enterprise plans.

#### Step 1: Enable Skills

1. Sign in to [claude.ai](https://claude.ai)
2. Go to **Settings** (gear icon)
3. Navigate to **Capabilities**
4. Enable **"Code execution and file creation"**
5. Enable **"Skills"** toggle

#### Step 2: Download Skills

```bash
# Clone this repository:
git clone https://github.com/cognizonline/Claude_skills.git
cd Claude_skills

# Or download ZIP:
# Visit https://github.com/cognizonline/Claude_skills
# Click "Code" → "Download ZIP"
# Extract to your preferred location
```

#### Step 3: Upload Skills

For each skill you want to use:

1. Compress the skill folder to ZIP:
   ```bash
   # On Mac/Linux:
   cd Claude_skills
   zip -r memory-optimizer.zip memory-optimizer/

   # On Windows (PowerShell):
   Compress-Archive -Path memory-optimizer -DestinationPath memory-optimizer.zip
   ```

2. In Claude.ai:
   - Go to **Settings → Capabilities → Skills**
   - Click **"Upload custom skill"**
   - Select the skill ZIP file
   - Wait for "Uploaded successfully" confirmation

3. Repeat for each skill

**Tip**: Upload the skills you'll use most frequently first (e.g., memory-optimizer, memory-account-briefing).

---

### Claude API

For developers integrating skills via the API.

#### Step 1: Install SDK

```bash
pip install anthropic>=0.34.0
```

#### Step 2: Prepare Skills

```bash
# Clone repository:
git clone https://github.com/cognizonline/Claude_skills.git
cd Claude_skills

# Create ZIP files:
python -c "
import shutil
from pathlib import Path

skills = [d for d in Path('.').iterdir() if d.is_dir() and d.name.startswith(('memory-', 'revenue-', 'usage-'))]
for skill in skills:
    shutil.make_archive(str(skill), 'zip', skill)
    print(f'Created {skill}.zip')
"
```

#### Step 3: Upload via API

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic(api_key="your-api-key")

# Upload all skills:
skill_ids = {}
skills_dir = Path(".")

for zip_file in skills_dir.glob("*.zip"):
    with open(zip_file, "rb") as f:
        skill = client.skills.create(
            name=zip_file.stem,
            file=f
        )
        skill_ids[zip_file.stem] = skill.id
        print(f"Uploaded {zip_file.stem}: {skill.id}")

# Save skill IDs for later use:
import json
with open("skill_ids.json", "w") as f:
    json.dump(skill_ids, f, indent=2)
```

#### Step 4: Use Skills in Conversations

```python
# Load skill IDs:
with open("skill_ids.json") as f:
    skill_ids = json.load(f)

# Use in message:
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    skills=[
        skill_ids["memory-optimizer"],
        skill_ids["memory-account-briefing"]
    ],
    messages=[{
        "role": "user",
        "content": "Optimize memories in my documentation project"
    }]
)

print(response.content[0].text)
```

---

## Configuration

### Cogniz Memory Platform Setup

All skills require access to the Cogniz Memory Platform API.

#### Step 1: Get API Credentials

1. Sign up at [cogniz.online](https://cogniz.online)
2. Complete email verification
3. Navigate to **Settings → API Keys**
4. Click **"Generate New API Key"**
5. Copy the key (shown only once!)
6. Note your Project ID from **Projects** page

#### Step 2: Create Configuration File

Create a JSON configuration file at:

- **Linux/Mac**: `~/.cogniz/config.json`
- **Windows**: `C:\Users\YourName\.cogniz\config.json`

```json
{
  "base_url": "https://api.cogniz.online",
  "api_key": "your-api-key-here",
  "project_id": "your-default-project-id",
  "project_name": "My Project"
}
```

**Security Note**: Keep this file private! Do not commit to version control.

#### Step 3: Set File Permissions (Linux/Mac only)

```bash
chmod 600 ~/.cogniz/config.json
```

### Python Dependencies (Optional)

Only required if you plan to run helper scripts manually:

```bash
# Install from repository root:
pip install -r requirements.txt

# Or install individually:
pip install requests>=2.31.0 python-dateutil>=2.8.2
```

### Environment Variables (Optional)

Alternative to config file for CI/CD environments:

```bash
# Linux/Mac (.bashrc, .zshrc, etc.):
export COGNIZ_API_KEY="your-api-key"
export COGNIZ_PROJECT_ID="your-project-id"
export COGNIZ_BASE_URL="https://api.cogniz.online"

# Windows (PowerShell profile):
$env:COGNIZ_API_KEY = "your-api-key"
$env:COGNIZ_PROJECT_ID = "your-project-id"
$env:COGNIZ_BASE_URL = "https://api.cogniz.online"
```

---

## Verification

### Test Skill Installation

#### In Claude Code:

```
User: List all installed Cogniz skills

Claude: [Should list all 14 skills if installed]
```

#### Test a Specific Skill:

```
User: Use memory-optimizer to analyze potential savings

Claude: I'll use the memory-optimizer skill...
[Should execute successfully and show analysis]
```

### Test Configuration

Run this Python script to verify API connectivity:

```python
import json
import requests
from pathlib import Path

# Load config
config_path = Path.home() / ".cogniz" / "config.json"
with open(config_path) as f:
    config = json.load(f)

# Test connection
response = requests.get(
    f"{config['base_url']}/memories",
    headers={"Authorization": f"Bearer {config['api_key']}"},
    params={"project_id": config['project_id'], "limit": 1}
)

if response.status_code == 200:
    print("✓ Configuration verified successfully!")
    print(f"Project: {config['project_name']}")
    print(f"Memories found: {len(response.json().get('results', []))}")
else:
    print(f"✗ Configuration error: {response.status_code}")
    print(response.text)
```

---

## Troubleshooting

### Common Issues

#### Issue: "Skills not found" in Claude Code

**Solution**:
1. Verify skills are installed: `/plugin list`
2. Reinstall if needed: `/plugin install cogniz-memory-skills`
3. Restart VS Code
4. Check Claude Code extension is up to date

#### Issue: "Unable to locate memory_api.py"

**Cause**: Missing `cogniz-memory-manager-local` dependency

**Solution**:
```bash
# Option 1: Install memory manager locally
git clone https://github.com/cognizonline/cogniz-memory-manager-local.git
cd cogniz-memory-manager-local
pip install -r requirements.txt

# Option 2: Set environment variable
export COGNIZ_MEMORY_MANAGER_PATH="/path/to/cogniz-memory-manager-local/scripts"

# Option 3: Pass path directly in script
python script.py --memory-api-path="/path/to/scripts"
```

#### Issue: "401 Unauthorized" API errors

**Cause**: Invalid or expired API key

**Solution**:
1. Check config file exists and has valid API key
2. Regenerate API key at cogniz.online
3. Update config file with new key
4. Verify no extra spaces in key

#### Issue: "No memories found" in search

**Cause**: Project has no memories or query filters too restrictive

**Solution**:
1. Verify you're using the correct project_id
2. Create test memory at cogniz.online
3. Simplify query parameters
4. Check date range in lookback_days parameter

#### Issue: Python import errors

**Cause**: Missing dependencies

**Solution**:
```bash
# Install all dependencies:
pip install -r requirements.txt

# Or install specific packages:
pip install requests python-dateutil
```

### Getting Help

If you encounter issues not listed here:

1. **Check existing issues**: [GitHub Issues](https://github.com/cognizonline/Claude_skills/issues)
2. **Search discussions**: [GitHub Discussions](https://github.com/cognizonline/Claude_skills/discussions)
3. **Create new issue**: Include:
   - Operating system and version
   - Python version (if applicable)
   - Claude platform (Code/Web/API)
   - Error messages (full text)
   - Steps to reproduce
4. **Email support**: support@cogniz.online

### Debug Mode

Enable verbose logging for troubleshooting:

```python
# In Python scripts:
python script.py --verbose

# Or in code:
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Next Steps

After successful installation:

1. **Try example workflows**: See [README.md](README.md#usage-examples)
2. **Explore individual skills**: Each skill has its own README
3. **Join community**: Share feedback in [Discussions](https://github.com/cognizonline/Claude_skills/discussions)
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

**Questions or feedback?** Open an issue or discussion on GitHub!

[← Back to README](README.md)
