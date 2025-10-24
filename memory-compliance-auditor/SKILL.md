---
name: memory-compliance-auditor
description: Audit Cogniz memories for policy alignment, sensitive data exposure, and regulatory compliance issues.
version: 1.1.0
---

# Memory Compliance Auditor

This skill equips Claude to detect, report, and escalate potential compliance violations within Cogniz memories using configurable rule packs.

## Activation Triggers
- Scheduled compliance sweeps (monthly, quarterly, or pre-audit).  
- Pre-flight checks before exporting memories to external systems or partners.  
- Incident response investigations or new regulatory requirements.

## Requirements
1. Cogniz configuration (`C:\Users\[Username]\.cogniz\config.json`) with API key and project ID.  
2. Confirmed audit scope (categories, date range, business unit).  
3. Alignment with legal/security on severity definitions and remediation workflow.  
4. Access to Cogniz memory manager scripts via default path, env var, or `--memory-api-path`.

## Bundled Resources
- `scripts/run_audit.py` – Scans memories using configurable regex rules, emits Markdown and optional JSON, supports `--memory-api-path` and `--verbose`.  
- `references/compliance_pattern_catalog.md` – Default rule catalogue with severity guidance and actions.  
- `assets/compliance_report_template.md` – Structured remediation template for distribution to security/legal teams.

## Standard Operating Procedure
1. **Scope the review**  
   - Define categories, date range, severity expectations, and stakeholders.  
   - Update `references/compliance_pattern_catalog.md` or provide a custom JSON rule pack via `--rules`.

2. **Execute the scan**  
   - Windows / VS Code:  
     ```powershell
     if (!(Test-Path .\out)) { New-Item -ItemType Directory out | Out-Null }
     python .\scripts\run_audit.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --query "category:support-notes last-90-days" `
       --limit 300 `
       --output ".\out\compliance-findings.md" `
       --output-json ".\out\compliance-findings.json" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/run_audit.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --query "category:support-notes last-90-days" \
       --limit 300 \
       --verbose
     ```

3. **Classify findings**  
   - Review Markdown/JSON outputs; severity is derived from the rule definitions.  
   - Populate `assets/compliance_report_template.md` with issue owners, remediation plans, and due dates.

4. **Remediate**  
   - Coordinate redaction, deletion, or credential rotation with system owners.  
   - Execute deletions via the Cogniz memory manager only after explicit approval and log the action ID.  
   - Update the JSON/Markdown outputs to reflect remediation status.

5. **Store and distribute**  
   - Save the final report in Cogniz:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@compliance-report\n<completed report>" `
       --category "compliance" `
       --tags "audit,quarter:2025-Q4"
     ```  
   - Share outputs with security/legal; retain `--verbose` logs for audit trails.  
   - Repackage the skill for distribution using `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Enforce least privilege on Cogniz API keys used for scanning.  
- Never delete or redact without recorded approval—document decision IDs in the stored report.  
- Update rule packs when policies evolve; maintain change history in version control.  
- Ensure audit artefacts (Markdown/JSON) are classified and stored per corporate data retention policy.

## Resilience & Observability
- Use verbose logging to confirm rule pack loading and API interactions.  
- If the scan returns no results due to API restrictions or outages, capture the incident and retry via scheduled automation.  
- Integrate the JSON output with SIEM or GRC tooling for ongoing monitoring when required.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager documentation (`../cogniz-memory-manager-local/SKILL.md`).

