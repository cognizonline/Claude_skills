# Sales Metrics Dictionary

| Metric | Definition | Source Memory Tags |
|--------|------------|--------------------|
| Pipeline ARR | Sum of ARR for opportunities in active pipeline. | `category:deal-notes`, `stage:<stage>` |
| Commit ARR | Opportunities with signed agreements or verbal commits. | `category:deal-notes`, `tag:commit` |
| Expansion ARR | Additional ARR from existing customers. | `category:deal-notes`, `tag:expansion` |
| Churn Risk ARR | ARR at risk due to churn or downgrades. | `category:deal-notes`, `tag:churn` |
| Usage Adoption | Weekly or monthly active usage change. | `category:usage-analytics`, `metric:active-users` |
| Health Score | Qualitative assessment (green/yellow/red). | `category:deal-notes`, `tag:health` |
| Win Rate | Closed won deals divided by total closed deals. | Combine `category:deal-notes` with outcome tags. |

Maintain consistency by updating this dictionary when new tags or metrics are introduced.

