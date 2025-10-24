---
name: usage-analytics
description: Generate usage reports and analytics from platform database for business intelligence and insights
---

# Usage Analytics Reporter

Generates comprehensive usage reports and analytics from the Cogniz Memory Platform database. Analyzes user behavior, storage patterns, API usage, and business metrics to provide actionable insights.

## When to use this skill

Use this skill when:
- Preparing monthly or quarterly business reviews
- Need to track user engagement and retention metrics
- Analyzing storage usage and optimization opportunities
- Creating reports for investors or stakeholders
- Monitoring platform health and growth trends

## Instructions

1. **Connect to database**

Establish connection to WordPress database:

```python
from utils.analytics import UsageAnalytics

analytics = UsageAnalytics(
    db_host='localhost',
    db_name='wordpress',
    db_user='wp_user',
    db_pass='wp_password'
)
```

2. **Query usage data**

Fetch relevant metrics for the specified time period:

```python
report = analytics.generate_report(
    report_type='usage_summary',
    time_period='last_30_days'
)
```

3. **Calculate key metrics**

Compute analytics including:
- DAU/WAU/MAU (Daily/Weekly/Monthly Active Users)
- Storage usage by category
- API request patterns
- Growth trends and comparisons

4. **Format and export**

Generate formatted report in markdown, JSON, or CSV based on user needs.

## Examples

### Example 1: Monthly Business Review

**User**: "Generate a usage report for last month"

**Output**:
```markdown
# Usage Report - January 2024

## Executive Summary
- Total Memories: 15,847 (+23% MoM)
- Storage Used: 2.3 GB (+18% MoM)
- Active Users: 234 (+15% MoM)
- API Requests: 47,392 (+31% MoM)

## User Engagement
- DAU: 87 users
- WAU: 156 users
- MAU: 234 users
- DAU/MAU Ratio: 37.2% (Strong retention)

## Storage by Category
| Category | Memories | Storage |
|----------|----------|---------|
| Documentation | 5,234 | 856 MB |
| Meeting Notes | 3,891 | 423 MB |
| Code Snippets | 2,456 | 312 MB |

## Growth Trends
All metrics showing positive month-over-month growth.
API usage growth (31%) outpacing user growth (15%),
indicating increasing platform engagement.
```

### Example 2: Storage Analysis

**User**: "Analyze storage usage by project"

**Output**:
```json
{
  "total_projects": 87,
  "total_storage_gb": 2.3,
  "top_projects": [
    {
      "name": "engineering-docs",
      "memories": 3456,
      "storage_mb": 567,
      "percent_of_total": 24.6
    },
    {
      "name": "meeting-notes-2024",
      "memories": 2891,
      "storage_mb": 423,
      "percent_of_total": 18.4
    }
  ],
  "recommendations": [
    "Consider archiving inactive projects",
    "Optimize 'engineering-docs' for 120 MB potential savings"
  ]
}
```

### Example 3: Weekly API Metrics

**User**: "Show API usage metrics for this week"

**Output**:
```
API Performance - Last 7 Days

Total Requests: 11,234
Success Rate: 99.3%
Average Response Time: 127ms

Top Endpoints:
1. POST /store - 6,789 requests (60.4%)
2. GET /search - 3,456 requests (30.8%)
3. DELETE /delete - 989 requests (8.8%)

Peak Usage: Tuesday 2-3 PM (1,567 requests/hour)
```

## Guidelines

- **Accuracy**: Validate all SQL queries return correct data
- **Privacy**: Never expose individual user data without authorization
- **Performance**: Optimize queries for large datasets (100K+ records)
- **Insights**: Include actionable recommendations, not just raw data
- **Visualization**: Use tables and charts for clarity
- **Time periods**: Support daily, weekly, monthly, quarterly, and annual ranges

## Technical Details

**Key Metrics Calculated**:
- **DAU**: Unique users active in last 24 hours
- **WAU**: Unique users active in last 7 days
- **MAU**: Unique users active in last 30 days
- **DAU/MAU Ratio**: User stickiness indicator (>30% is good)
- **MoM Growth**: Month-over-month percentage change

**Database Queries**:
```sql
-- Example: Daily Active Users
SELECT COUNT(DISTINCT user_id) as dau
FROM wp_memory_usage
WHERE DATE(activity_date) = CURDATE();

-- Example: Storage by Category
SELECT category, COUNT(*) as count,
       SUM(compressed_size) as storage
FROM wp_memory_entries
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY category;
```

**Performance**:
- Report generation: ~2 seconds for 30-day period
- Supports datasets up to 1M+ memory entries
- Optimized with database indexes on date fields
