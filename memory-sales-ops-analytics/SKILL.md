---
name: memory-sales-ops-analytics
description: Analyze sales pipeline, deal notes, and usage signals stored in Cogniz to produce actionable sales operations insights.
---

# Memory Sales Ops Analytics

This skill transforms Cogniz deal notes and usage analytics into a weekly revenue intelligence briefing for sales leadership.

## Activation Triggers
- Weekly pipeline reviews, revenue standups, or forecast checkpoints.  
- Board/investor updates requiring pipeline and usage insight.  
- Emerging churn or expansion signals needing rapid analysis.

## Requirements
1. Cogniz configuration at `C:\Users\[Username]\.cogniz\config.json`.  
2. Deal and usage memories tagged consistently for stage, segment, and ARR.  
3. Agreement on reporting cadence, segment filters, and KPI definitions.  
4. Access to the Cogniz memory manager scripts via default path, environment variable, or `--memory-api-path`.

## Bundled Resources
- `scripts/pipeline_snapshot.py` – Generates pipeline stage breakdowns and usage signal summaries (`--memory-api-path`, `--verbose`).  
- `references/sales_metrics_dictionary.md` – Defines ARR, commit, churn, and usage metrics for standard reporting.  
- `assets/sales_ops_brief_template.md` – Template for leadership-ready briefs.

## Standard Operating Procedure
1. **Align scope**  
   - Confirm quarter/timeframe, segment filters, and target audience.  
   - Ensure tagging conventions cover stage (`stage:negotiation`), segment, and revenue values.

2. **Run the snapshot helper**  
   - Windows / VS Code:  
     ```powershell
     if (!(Test-Path .\out)) { New-Item -ItemType Directory out | Out-Null }
     python .\scripts\pipeline_snapshot.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --quarter "2025-Q4" `
       --segment "enterprise" `
       --output ".\out\sales-ops-snapshot.md" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/pipeline_snapshot.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --quarter "2025-Q4" \
       --segment "enterprise" \
       --verbose
     ```  
   - Adjust `--quarter`, `--segment`, `--limit`, or `--memory-api-path` to meet business needs.

3. **Quantify metrics**  
   - Use `references/sales_metrics_dictionary.md` to calculate pipeline ARR, commit ARR, expansion ARR, and churn risk.  
   - Associate usage signals with specific deals or accounts to prioritise actions.

4. **Draft the brief**  
   - Fill `assets/sales_ops_brief_template.md` with KPI tables, stage breakdowns, usage insights, and prioritized actions.  
   - Record memory IDs to support drill-down investigations.

5. **Store and package**  
   - Persist the brief in Cogniz:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@sales-ops-brief\n<completed brief>" `
       --category "sales-ops" `
       --tags "week:2025-10-20,segment:enterprise"
     ```  
   - Share with sales leadership and package updates using `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Validate revenue figures with finance or CRM systems before distribution.  
- Avoid embedding raw customer PII; reference secure CRM links when required.  
- Capture owner acknowledgements for risk/action items in Cogniz.  
- Retain verbose logs for audit purposes when operating in regulated environments.

## Resilience & Observability
- Use verbose logging to troubleshoot tagging gaps or API errors.  
- If data sources are stale (CRM sync delays, telemetry outages), document the gap and refresh once data is available.  
- Maintain version history to track week-over-week changes.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager skill (`../cogniz-memory-manager-local/SKILL.md`).

