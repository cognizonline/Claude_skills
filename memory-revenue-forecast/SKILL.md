---
name: memory-revenue-forecast
description: Forecast MRR, ARR, churn, and growth scenarios using Cogniz memory data plus structured projection workflows.
---

# Memory Revenue Forecast

This skill enables Claude to convert Cogniz revenue notes and pipeline memories into conservative, baseline, and stretch forecasts that finance leaders can trust.

## Activation Triggers
- Monthly or quarterly planning cycles requiring updated ARR/MRR projections.  
- Board, investor, or leadership reviews centred on revenue performance.  
- Emergent churn risks or expansion opportunities surfaced in recent Cogniz sessions.

## Requirements
1. Cogniz configuration (`C:\Users\[Username]\.cogniz\config.json`) with API key, base URL, and project ID.  
2. Revenue and pipeline memories tagged consistently (for example `category:revenue-metrics`, `category:sales-notes`).  
3. Agreement on currency, units, and forecast horizon with finance stakeholders.  
4. Access to the Cogniz memory manager scripts via `../cogniz-memory-manager-local/scripts`, environment variable `COGNIZ_MEMORY_MANAGER_PATH`, or the `--memory-api-path` flag.

## Bundled Resources
- `scripts/build_forecast.py` – Retrieves metrics/pipeline notes, extracts structured amounts, and prints multi-scenario tables (`--memory-api-path`, `--verbose` supported).  
- `references/forecast_assumptions_matrix.md` – Template for documenting modelling assumptions and owners.  
- `assets/forecast_summary_template.md` – Markdown scaffold for executive-ready forecast narratives.

## Standard Operating Procedure
1. **Calibrate inputs**  
   - Confirm baseline MRR/ARR from the latest finance source or provide `--baseline-mrr`.  
   - Align on tagging conventions and lookback windows before querying.

2. **Run the helper**  
   - Windows / VS Code:  
     ```powershell
     python .\scripts\build_forecast.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --baseline-mrr 420000 `
       --horizon 6 `
       --limit 100 `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/build_forecast.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --baseline-mrr 420000 \
       --horizon 6 \
       --limit 100 \
       --verbose
     ```  
   - Adjust `--pipeline-query` or `--metrics-query` to target custom categories; supply `--memory-api-path` when the manager scripts reside elsewhere.

3. **Audit the output**  
   - Review the console summary for conservative/baseline/stretch projections.  
   - Investigate warnings about memories lacking numeric amounts and update source data as needed.  
   - Capture key assumptions in `references/forecast_assumptions_matrix.md`.

4. **Compose deliverables**  
   - Populate `assets/forecast_summary_template.md` with scenario tables, drivers, risks, and recommended actions.  
   - Attach charts or spreadsheets if stakeholders require additional analysis.

5. **Store and package**  
   - Save the narrative summary and assumption log via the Cogniz memory manager:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@finance-forecast\n<completed summary>" `
       --category "finance-forecasts" `
       --tags "period:2025-Q4,forecast"
     ```  
   - Package the skill for release with `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Keep sensitive financial metrics aligned with corporate data classification; remove raw customer contracts or pricing unless approved.  
- Record assumption owners and approval timestamps to satisfy audit requests.  
- Preserve `--verbose` logs for compliance reviews and incident investigations.  
- Coordinate with finance control teams before distributing scenario outputs externally.

## Resilience & Observability
- Use the helper’s warnings to identify memories without structured metrics—update source data to maintain model accuracy.  
- If the Cogniz API is unavailable, document the outage and retry after service restoration.  
- Store JSON outputs in version control or BI systems for traceability when required.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide) and forecasting endpoints.  
- Cogniz Memory Manager guide (`../cogniz-memory-manager-local/SKILL.md`).

