---
name: revenue-calculator
description: Calculate SaaS revenue metrics including MRR, ARR, churn, LTV, and growth projections
---

# Revenue Calculator

Calculates key SaaS revenue metrics and financial KPIs for the Cogniz Memory Platform. Analyzes subscription data, calculates MRR/ARR, tracks churn, projects growth, and provides financial insights for business decisions and investor reporting.

## When to use this skill

Use this skill when:
- Preparing monthly or quarterly financial reports
- Need current MRR, ARR, or churn metrics
- Creating investor updates or board presentations
- Analyzing unit economics (LTV, CAC, payback period)
- Forecasting revenue growth and projections

## Instructions

1. **Load subscription data**

Connect to database or payment provider to fetch subscription information:

```python
from utils.calculator import RevenueCalculator

calc = RevenueCalculator()
calc.load_data(source='database')  # or 'paystack', 'csv'
```

2. **Calculate metrics**

Compute requested financial KPIs:

```python
mrr = calc.calculate_mrr()
churn = calc.calculate_churn(period='last_month')
ltv_cac = calc.calculate_unit_economics()
```

3. **Analyze trends**

Compare to previous periods and identify growth patterns:

```python
growth = calc.analyze_growth(periods=12)  # Last 12 months
```

4. **Generate report**

Create formatted financial dashboard with insights and recommendations.

## Examples

### Example 1: Current MRR

**User**: "What's our current MRR?"

**Output**:
```markdown
# Monthly Recurring Revenue - January 2024

**Current MRR**: $12,450 (+18% MoM)

## Breakdown
- New MRR: $2,340 (47 new customers)
- Expansion MRR: $780 (12 upgrades)
- Churned MRR: -$420 (5 cancellations)
- Net New MRR: $2,700

## By Plan Tier
| Plan | Customers | MRR | % Total |
|------|-----------|-----|---------|
| Enterprise | 8 | $4,000 | 32.1% |
| Pro | 45 | $4,050 | 32.5% |
| Starter | 89 | $2,670 | 21.4% |
| Free | 92 | $0 | 0% |
```

### Example 2: Churn Analysis

**User**: "Analyze churn for Q1"

**Output**:
```json
{
  "period": "Q1 2024",
  "customer_churn_rate": 2.1,
  "revenue_churn_rate": 3.4,
  "churned_customers": 15,
  "churned_mrr": 1260,
  "churn_reasons": {
    "price_sensitivity": 6,
    "moved_to_competitor": 3,
    "no_longer_needed": 6
  },
  "benchmark_comparison": {
    "your_churn": 2.1,
    "industry_average": 5.0,
    "status": "excellent"
  }
}
```

### Example 3: Financial Dashboard

**User**: "Generate complete financial dashboard"

**Output**:
```markdown
# Cogniz Financial Dashboard - January 2024

## Revenue Metrics
- MRR: $12,450 (+18% MoM)
- ARR: $149,400
- Customers: 234 (+15% MoM)

## Unit Economics
- ARPU: $54.50
- LTV: $1,308
- CAC: $125
- LTV:CAC Ratio: 10.5:1 [PASS] (Excellent)
- Payback Period: 2.3 months [PASS]

## Health Metrics
- Customer Churn: 2.1% [PASS] (Target: <5%)
- Quick Ratio: 7.2 [PASS] (Target: >4)
- Net Revenue Retention: 106% [PASS] (Target: >100%)

## 3-Month Forecast
- Feb 2024: $14,100 MRR (268 customers)
- Mar 2024: $15,800 MRR (305 customers)
- Apr 2024: $17,500 MRR (345 customers)

All health metrics are GREEN. Business is in strong growth phase.
```

## Guidelines

- **Accuracy**: Validate all calculations against source data
- **Consistency**: Use standard SaaS metric definitions
- **Context**: Always compare to previous periods and benchmarks
- **Insights**: Provide actionable recommendations, not just numbers
- **Formatting**: Use currency symbols, percentages, and clear labels
- **Privacy**: Aggregate data only, no individual customer information

## Technical Details

**Key Formulas**:

```
MRR = Sum of all monthly subscription values
ARR = MRR × 12

Customer Churn Rate = (Churned / Total at Start) × 100
Revenue Churn Rate = (Churned MRR / Total MRR at Start) × 100

LTV = ARPU / Monthly Churn Rate
LTV:CAC Ratio = LTV / CAC

Quick Ratio = (New MRR + Expansion MRR) / Churned MRR
Net Revenue Retention = ((Start MRR + Expansion - Churn) / Start MRR) × 100
```

**Healthy Benchmarks**:
- Customer Churn: <5% monthly
- LTV:CAC Ratio: >3:1 (10:1 is excellent)
- Quick Ratio: >4
- Net Revenue Retention: >100%
- CAC Payback: <12 months

**Performance**:
- Calculation time: <1 second for up to 10,000 customers
- Supports real-time updates from payment webhooks
- Historical data analysis for trend detection
