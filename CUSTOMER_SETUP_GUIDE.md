# Customer Setup Guide - Cogniz Memory Skills

**For customers using the Cogniz Memory Platform SaaS**

This guide shows how to set up Claude Skills to work with your Cogniz account.

---

## Overview

You're using Cogniz Memory Platform as a **hosted service** (SaaS). You don't need to install anything on your own server - just connect Claude to your Cogniz account.

**Flow**:
```
1. Sign up at cogniz.online
2. Get your API key from the dashboard
3. Install Claude Skills
4. Configure skills to use cogniz.online
5. Start using skills in Claude!
```

---

## Step 1: Get Your API Key

### Sign Up for Cogniz

1. Visit [cogniz.online](https://cogniz.online)
2. Click **Sign Up** and create your account
3. Choose a plan (Free tier available)
4. Verify your email

### Generate API Key

1. Log in to [cogniz.online](https://cogniz.online)
2. Go to **Dashboard** → **API Keys**
3. Click **Generate New Key**
4. Copy your API key (looks like: `mp_live_abc123...`)

**Important**: Save this key securely! You can't view it again after leaving the page.

---

## Step 2: Install Claude Skills

### Option A: Claude Code (VS Code)

```bash
# In Claude Code terminal:
git clone https://github.com/cognizonline/Claude_skills.git
cd Claude_skills
```

### Option B: Claude.ai Web

1. Download skills from [GitHub](https://github.com/cognizonline/Claude_skills)
2. Extract the ZIP file
3. In Claude.ai → Settings → Skills
4. Upload individual skill folders

### Option C: Claude API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-claude-api-key")

# Upload a skill
with open("memory-optimizer.zip", "rb") as f:
    skill = client.skills.create(name="memory-optimizer", file=f)
```

---

## Step 3: Configure Skills

### Create Configuration File

Create a file at:
- **Windows**: `C:\Users\YourName\.cogniz\config.json`
- **Mac/Linux**: `~/.cogniz/config.json`

```json
{
  "base_url": "https://cogniz.online",
  "api_key": "mp_live_YOUR_API_KEY_HERE",
  "project_id": "default",
  "project_name": "My Project"
}
```

**Replace**:
- `mp_live_YOUR_API_KEY_HERE` with your actual API key from Step 1
- `default` with your project name (optional)

### Set File Permissions (Mac/Linux)

```bash
chmod 600 ~/.cogniz/config.json
```

---

## Step 4: Verify Setup

### Test Connection

**Windows (PowerShell)**:
```powershell
cd Claude_skills\cogniz-memory-manager-local\scripts
python memory_api.py --config "C:\Users\YourName\.cogniz\config.json" list --limit 5
```

**Mac/Linux**:
```bash
cd Claude_skills/cogniz-memory-manager-local/scripts
python3 memory_api.py --config ~/.cogniz/config.json list --limit 5
```

**Expected Output**:
```
✓ Connected to cogniz.online
✓ API key valid
✓ Found 0-5 memories (depending on what you've stored)
```

If you see errors, check:
- API key is correct
- Internet connection is working
- cogniz.online is accessible

---

## Step 5: Start Using Skills

### Example 1: Optimize Storage

```
You (in Claude Code):
"Use memory-optimizer to analyze my storage"

Claude:
I'll analyze your Cogniz storage...
[Connects to cogniz.online using your API key]
[Analyzes your data]
[Shows potential savings]
```

### Example 2: Create Account Briefing

```
You:
"Generate an account briefing for customer Acme Corp"

Claude:
I'll search your Cogniz memories for Acme Corp...
[Queries cogniz.online API]
[Finds relevant memories]
[Generates formatted briefing]
```

### Example 3: Track Learning

```
You:
"Log what I learned today about Python decorators"

Claude:
I'll store this in your Cogniz learning tracker...
[Saves to cogniz.online]
[Applies spaced repetition schedule]
[Returns confirmation]
```

---

## How It Works (Technical)

```
┌──────────────────┐
│  Your Computer   │
│                  │
│  Claude Code     │
│  + Skills        │
└────────┬─────────┘
         │
         │ Uses config.json
         │ to connect to:
         │
         v
┌─────────────────────────────┐
│  cogniz.online              │
│  (Hosted by Cogniz Team)    │
│                             │
│  REST API:                  │
│  /wp-json/memory/v1/        │
│    ├─ /store                │
│    ├─ /search               │
│    ├─ /projects             │
│    └─ /user-stats           │
│                             │
│  Your Data:                 │
│  ├─ Projects                │
│  ├─ Memories                │
│  ├─ API Keys                │
│  └─ Usage Stats             │
└─────────────────────────────┘
```

**Key Points**:
1. ✅ Skills run on YOUR computer (in Claude)
2. ✅ Data is stored on cogniz.online (our servers)
3. ✅ API key authenticates YOUR account
4. ✅ No server setup needed
5. ✅ Works from anywhere with internet

---

## Frequently Asked Questions

### Q: Do I need to install WordPress?
**A: No!** The WordPress backend runs on cogniz.online. You just connect to it.

### Q: Where is my data stored?
**A: On cogniz.online servers.** We handle all the infrastructure, backups, and maintenance.

### Q: Can I use multiple API keys?
**A: Yes!** Generate different keys for different projects or team members.

### Q: What if cogniz.online is down?
**A: Skills will show an error.** Data is safe on our servers and will be available when service resumes.

### Q: Can I export my data?
**A: Yes!** Use the export feature in your cogniz.online dashboard.

### Q: Is my data secure?
**A: Yes!** We use:
- HTTPS encryption for all API calls
- Secure API key authentication
- Regular backups
- SOC 2 compliance (coming soon)

### Q: Can I self-host instead?
**A: Not currently supported for customers.** We may offer enterprise self-hosting in the future.

---

## Pricing & Plans

Your Cogniz plan determines:
- Number of projects
- Storage limits
- API rate limits
- Advanced features

View plans at [cogniz.online/pricing](https://cogniz.online/pricing)

Upgrade or downgrade anytime from your dashboard.

---

## Troubleshooting

### Error: "Unable to connect to cogniz.online"

**Check**:
1. Internet connection is working
2. Can access cogniz.online in browser
3. No firewall blocking outbound HTTPS

**Fix**: Test connectivity:
```bash
curl https://cogniz.online/wp-json/memory/v1/
```

---

### Error: "Invalid API key"

**Check**:
1. API key is copied correctly (no extra spaces)
2. Key hasn't been regenerated
3. Account is active

**Fix**:
1. Log in to cogniz.online
2. Go to API Keys
3. Verify key or regenerate if needed
4. Update config.json with new key

---

### Error: "Project not found"

**Check**:
1. Project ID exists in your account
2. project_id in config.json is correct

**Fix**:
1. Log in to cogniz.online
2. Go to Projects
3. Copy exact project ID
4. Update config.json

---

### Error: "Rate limit exceeded"

**Cause**: You've exceeded API calls for your plan

**Fix**:
1. Wait for rate limit to reset (usually 1 hour)
2. Or upgrade to higher plan at cogniz.online

---

## Support

Need help?

- **Documentation**: [docs.cogniz.online](https://cogniz.online) (coming soon)
- **Email**: support@cogniz.online
- **GitHub Issues**: [Report bugs](https://github.com/cognizonline/Claude_skills/issues)
- **Status**: [status.cogniz.online](https://cogniz.online) (coming soon)

---

## Next Steps

✅ You're all set! Here's what to do next:

1. **Try a skill**: Start with memory-optimizer or memory-context-economizer
2. **Store some data**: Use the store endpoint to save memories
3. **Create a project**: Organize your work into projects
4. **Invite team**: Share your workspace (Team plan required)
5. **Explore features**: Try all 14 skills to find what's useful

**Happy memory managing!** 🚀

---

**Last Updated**: October 24, 2025
**Skills Version**: 2.0.0
**Compatible with**: Cogniz Platform v2.0+
