# How Cogniz Memory Skills Work (SaaS Model)

**A simple explanation for customers and developers**

---

## The Simple Version

```
You sign up → Get API key → Install skills → Use Claude → It works!
```

---

## The Visual Version

```
┌─────────────────────────────────────────────────────────────┐
│                    Customer's Computer                       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Claude Code (VS Code)                      │    │
│  │                                                     │    │
│  │  Customer: "Generate account briefing for Acme"    │    │
│  │                                                     │    │
│  │  Claude: I'll search your Cogniz memories...       │    │
│  │          [Using memory-account-briefing skill]     │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│                         │ Reads config:                      │
│                         │ ~/.cogniz/config.json             │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐    │
│  │ config.json:                                        │    │
│  │ {                                                   │    │
│  │   "base_url": "https://cogniz.online",            │    │
│  │   "api_key": "mp_live_abc123..."                  │    │
│  │ }                                                   │    │
│  └──────────────────────┬──────────────────────────────┘    │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ HTTPS API Call
                          │ Bearer mp_live_abc123...
                          │
                          v
┌─────────────────────────────────────────────────────────────┐
│                    cogniz.online                             │
│                   (Hosted by you)                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │          WordPress + Memory Platform Plugin        │    │
│  │                                                     │    │
│  │  1. Receives API call                              │    │
│  │  2. Validates API key mp_live_abc123...            │    │
│  │  3. Finds customer's account                       │    │
│  │  4. Queries database for "Acme" memories           │    │
│  │  5. Decompresses content                           │    │
│  │  6. Returns results                                │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                      │
│  ┌────────────────────┴───────────────────────────────┐    │
│  │          Database                                   │    │
│  │                                                     │    │
│  │  wp_memory_api_keys                                │    │
│  │    ├─ mp_live_abc123... → User: John               │    │
│  │                                                     │    │
│  │  wp_memory_projects                                │    │
│  │    ├─ Project: sales-data (John's)                 │    │
│  │                                                     │    │
│  │  wp_memory_entries                                 │    │
│  │    ├─ Memory 1: "Acme signed Q1..."                │    │
│  │    ├─ Memory 2: "Acme renewal due..."              │    │
│  │    └─ Memory 3: "Acme feedback..."                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step: What Actually Happens

### Step 1: Customer Signs Up

**Customer action**: Goes to cogniz.online and creates account

**What happens**:
- WordPress creates user account
- Assigns default "Free" plan
- Creates default project
- Generates first API key

**Result**: Customer has `mp_live_abc123...` API key

---

### Step 2: Customer Installs Skills

**Customer action**: Clones GitHub repo or uploads skills to Claude

```bash
git clone https://github.com/cognizonline/Claude_skills.git
```

**What happens**:
- Customer downloads 14 skill folders
- Each has SKILL.md, scripts, templates
- No installation needed - just files

**Result**: Skills are available in Claude Code

---

### Step 3: Customer Creates Config

**Customer action**: Creates `~/.cogniz/config.json`

```json
{
  "base_url": "https://cogniz.online",
  "api_key": "mp_live_abc123...",
  "project_id": "default"
}
```

**What happens**:
- File saved on customer's computer
- Skills will read this file when needed
- API key authenticates to YOUR platform

**Result**: Skills know where to connect

---

### Step 4: Customer Uses Skill

**Customer action**: Types in Claude Code:
```
"Store this meeting note in my Cogniz memory"
```

**What Claude does**:
1. Recognizes this needs memory storage
2. Loads memory-* skill (whichever matches best)
3. Skill reads config.json
4. Skill calls Python script
5. Script makes HTTPS request to cogniz.online

**API Call**:
```http
POST https://cogniz.online/wp-json/memory/v1/store
Authorization: Bearer mp_live_abc123...
Content-Type: application/json

{
  "content": "Meeting with John - discussed Q4 targets...",
  "project_id": "default",
  "category": "meetings"
}
```

**Your WordPress plugin**:
1. Receives POST request
2. Validates `mp_live_abc123...` API key
3. Finds it belongs to customer "John"
4. Checks John's plan limits (storage, requests)
5. Compresses content using Cerebrium/local
6. Stores in `wp_memory_entries` table
7. Returns success response

**Response**:
```json
{
  "status": "success",
  "memory_id": "mem_xyz789",
  "compressed_size": 145,
  "original_size": 234,
  "compression_ratio": 0.62
}
```

**Claude shows customer**:
```
✓ Stored in Cogniz Memory
Memory ID: mem_xyz789
Compressed: 234 bytes → 145 bytes (38% savings)
```

---

## Data Flow for Different Skills

### memory-optimizer (Standalone)

```
Customer → Claude
         ↓
   memory-optimizer skill
         ↓
   Local Python algorithm
   (no API call needed)
         ↓
   Results shown to customer
```

**No Cogniz API needed** - works entirely locally

---

### memory-account-briefing (API-dependent)

```
Customer: "Briefing for Acme"
         ↓
   Claude loads skill
         ↓
   Skill calls: GET /search?query=account:acme
         ↓
   cogniz.online searches database
         ↓
   Returns matching memories
         ↓
   Skill formats as briefing
         ↓
   Claude shows customer
```

**Requires Cogniz API** - calls your hosted platform

---

### revenue-calculator (Currently broken)

```
Customer: "Calculate MRR"
         ↓
   Claude loads skill
         ↓
   Skill tries to import calculator.py
         ↓
   ERROR: File doesn't exist
         ↓
   Claude tells customer it's not implemented
```

**Needs implementation** - code missing

---

## Customer's Perspective

### What they see:

1. **Sign up page** at cogniz.online
2. **Dashboard** with API keys, projects, usage
3. **Claude interface** with skills installed
4. **Results** when they ask Claude to do things

### What they DON'T see:

1. WordPress admin panel (that's yours)
2. Database tables (that's yours)
3. Compression algorithms (handled automatically)
4. Your server infrastructure

### What they pay for:

- Storage space for their memories
- Number of projects
- API rate limits
- Advanced features (if any)

---

## Your Perspective (Platform Owner)

### What you provide:

1. **Hosted WordPress** with memory-platform plugin
2. **API endpoints** at cogniz.online/wp-json/memory/v1/*
3. **User accounts** and authentication
4. **Data storage** and backups
5. **Skills repository** on GitHub
6. **Support** and documentation

### What customers provide:

1. Their own **Claude subscription**
2. Their own **computer** (runs Claude)
3. Their own **internet** connection
4. Their **API key** (from your platform)
5. **Payment** for your service tiers

### Revenue model:

- **Free tier**: Limited projects, storage
- **Pro tier**: More projects, storage, features
- **Enterprise**: Custom limits, support, SLAs

---

## Security Model

### Authentication Flow

```
1. Customer makes API call with: Bearer mp_live_abc123...
2. Your WordPress validates key in wp_memory_api_keys table
3. Finds key belongs to user_id = 42
4. Checks user's plan limits
5. Allows/denies request based on limits
6. Logs usage for billing
```

### What's secure:

- ✅ HTTPS encryption (if you have SSL)
- ✅ API key authentication
- ✅ User data isolation (each user sees only their data)
- ✅ Rate limiting per plan
- ✅ Audit logs

### What customers should do:

- Keep API key secret (like a password)
- Use config file with restricted permissions
- Don't share API keys with others
- Regenerate if compromised

---

## Scaling Considerations

### As you grow:

**10 customers**:
- Shared hosting fine
- Manual support okay
- Simple monitoring

**100 customers**:
- Need VPS or cloud hosting
- Automated billing
- Basic monitoring/alerts
- Support ticket system

**1,000 customers**:
- Load balancer + multiple servers
- Database optimization
- CDN for static assets
- Automated support
- 24/7 monitoring

**10,000 customers**:
- Kubernetes/Docker containers
- Database sharding
- Dedicated support team
- SLA guarantees
- Enterprise features

---

## Common Misconceptions

### ❌ "Customers need to install WordPress"
**✅ Reality**: NO! You run WordPress. Customers just use the API.

### ❌ "Skills run on my server"
**✅ Reality**: NO! Skills run on customer's computer in Claude.

### ❌ "Customers need technical knowledge"
**✅ Reality**: Just need to copy config file and install skills.

### ❌ "This is self-hosted software"
**✅ Reality**: It's SaaS - you host, customers consume.

### ❌ "Skills store data locally"
**✅ Reality**: Data goes to your cogniz.online database.

---

## Success Metrics to Track

### Customer metrics:

- API calls per day/month
- Storage used
- Active projects
- Error rates
- Response times

### Business metrics:

- Signups per week
- Conversion free → paid
- Churn rate
- MRR/ARR
- Customer acquisition cost

### Technical metrics:

- API uptime
- Average response time
- Database size
- Bandwidth used
- Error logs

---

## Next Steps for Customers

1. ✅ Sign up at cogniz.online
2. ✅ Get API key
3. ✅ Install skills from GitHub
4. ✅ Create config.json
5. ✅ Test connection
6. ✅ Start using Claude with skills!

See [CUSTOMER_SETUP_GUIDE.md](CUSTOMER_SETUP_GUIDE.md) for detailed instructions.

---

## Next Steps for You (Platform Owner)

1. **Deploy cogniz.online**
   - Ensure WordPress is accessible
   - Enable SSL certificate
   - Configure DNS

2. **Test end-to-end**
   - Create test account
   - Generate API key
   - Test all skills work

3. **Create marketing**
   - Demo video
   - Use case examples
   - Pricing page

4. **Launch**
   - Open signups
   - Monitor logs
   - Respond to feedback

---

**Questions?** See other docs:
- [README.md](README.md) - Overview
- [CUSTOMER_SETUP_GUIDE.md](CUSTOMER_SETUP_GUIDE.md) - Customer instructions
- [INSTALLATION.md](INSTALLATION.md) - Technical details
- [HONEST_ASSESSMENT.md](HONEST_ASSESSMENT.md) - What works/doesn't

---

**You're running a SaaS business! 🚀**
