---
name: memory-account-briefing
description: Build executive account briefings by combining Cogniz memories, revenue metrics, and usage analytics for high-priority customers.
---

# Memory Account Briefing

This skill equips Claude to assemble executive-ready account briefings that consolidate Cogniz memories, financial signals, and usage data. It follows Anthropic’s enterprise skill authoring guidance and is designed for reproducible packaging and deployment.

## Activation Triggers
- Leadership or account teams request a renewal, QBR, or escalation briefing.
- Ownership of an account is handed off to a different team or region.
- Risk or expansion signals emerge in support notes, deal updates, or telemetry.

## Requirements
1. Cogniz configuration present at `C:\Users\[Username]\.cogniz\config.json` with valid API key, base URL, and project ID.  
2. Cogniz memory manager scripts accessible locally; set `COGNIZ_MEMORY_MANAGER_PATH` or use the `--memory-api-path` flag if the manager lives outside `../cogniz-memory-manager-local/scripts`.  
3. Account tagging conventions agreed with revenue teams (for example `account:acme-analytics`).  
4. Optional: target directory such as `.\out` for briefing exports (create if absent).

## Bundled Resources
- `scripts/generate_brief.py` – Queries Cogniz, classifies findings (highlights, risks, actions, metrics), and emits Markdown/JSON briefings. Supports `--memory-api-path` and `--verbose`.  
- `references/account_briefing_checklist.md` – Assurance checklist covering metadata, risks, and follow-up expectations.  
- `assets/account_briefing_template.md` – Markdown scaffold for human-friendly deliverables.

## Standard Operating Procedure
1. **Confirm prerequisites**  
   - Verify Cogniz configuration and account tag with the requestor.  
   - If the memory manager scripts are not adjacent to this skill, export `COGNIZ_MEMORY_MANAGER_PATH=<absolute path>` or pass `--memory-api-path`.

2. **Run the retrieval helper**  
   - Windows / VS Code:  
     ```powershell
     if (!(Test-Path .\out)) { New-Item -ItemType Directory out | Out-Null }
     python .\scripts\generate_brief.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --account "account:<slug>" `
       --lookback-days 45 `
       --limit 60 `
       --output ".\out\account-briefing.md" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/generate_brief.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --account "account:<slug>" \
       --lookback-days 45 \
       --limit 60 \
       --verbose
     ```

3. **Review and enrich**  
   - Validate section coverage against `references/account_briefing_checklist.md`.  
   - Move `notes` items into highlights or risks when appropriate.  
   - Augment with revenue forecasts or usage charts produced by companion skills (for example `memory-revenue-forecast`).

4. **Curate the deliverable**  
   - Populate `assets/account_briefing_template.md` with ARR, renewal date, milestone tables, and owner assignments.  
   - Reference memory IDs or external ticket links for auditability.

5. **Store and package**  
   - Persist the final narrative via the Cogniz memory manager:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@account-briefing\n<final markdown content>" `
       --category "account-briefings" `
       --project-id "<project-id>" `
       --project-name "<friendly-name>"
     ```  
   - Include tags such as `account:<slug>` and `briefing`.  
   - Package updates with `python package_all_skills.py --dist-dir dist` when preparing releases.

## Security & Governance
- Classify briefings according to corporate data policies; omit secrets and redirect to secure vault references when necessary.  
- Verify the Cogniz config file and memory manager directories inherit enterprise file permissions.  
- Confirm mitigation owners acknowledge action items before distribution and record confirmation in Cogniz.  
- Retain activity logs (`--verbose`) for audit requests and incident investigations.

## Resilience & Observability
- Use the `--verbose` flag for structured logging; integrate with central log collection if available.  
- The helper surfaces dependency issues (missing memory manager, config) with actionable messages—address before re-running.  
- If the Cogniz API is unavailable, pause brief generation and log the outage in your operational tracker.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide) and related API endpoints.  
- Cogniz Memory Manager documentation in `../cogniz-memory-manager-local/SKILL.md`.

