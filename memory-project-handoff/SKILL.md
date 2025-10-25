---
name: memory-project-handoff
description: Capture and transfer project context, decisions, and next steps when handing work between teams or sessions.
---

# Memory Project Handoff

This skill automates project transition packets so incoming owners receive current state, outstanding tasks, and risks directly from Cogniz memories.

## Activation Triggers
- Ownership changes (team rotations, coverage handoffs, contractor onboarding).  
- Session wrap-up before extended downtime.  
- Escalations requiring cross-team collaboration where context continuity is critical.

## Requirements
1. Cogniz configuration at `C:\Users\[Username]\.cogniz\config.json`.  
2. Agreed project identifier/tag (for example `project:graph-api`).  
3. Alignment on new owner, due dates, escalation contacts, and secure storage expectations.  
4. Access to the Cogniz memory manager scripts via default path, `COGNIZ_MEMORY_MANAGER_PATH`, or `--memory-api-path`.

## Bundled Resources
- `scripts/create_handoff.py` – Builds state, task, and risk summaries from Cogniz (`--memory-api-path`, `--verbose`).  
- `references/handoff_checklist.md` – Governance checklist ensuring completeness and owner acknowledgment.  
- `assets/handoff_packet_template.md` – Standardized handoff template covering state, tasks, risks, contacts.

## Standard Operating Procedure
1. **Confirm transfer details**  
   - Gather incoming owner name, contact info, required environments, and due dates.  
   - Identify sensitive artifacts that should remain in secured systems.

2. **Generate the packet**  
   - Windows / VS Code:  
     ```powershell
     if (!(Test-Path .\out)) { New-Item -ItemType Directory out | Out-Null }
     python .\scripts\create_handoff.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --project "<project-id-or-slug>" `
       --lookback-days 14 `
       --output ".\out\handoff.md" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/create_handoff.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --project "<project-id-or-slug>" \
       --lookback-days 14 \
       --verbose
     ```  
   - Expand `--lookback-days` for longer running initiatives; set `--memory-api-path` when dependency layout differs.

3. **Complete the template**  
   - Transfer generated sections into `assets/handoff_packet_template.md`.  
   - Add dependencies, contact maps, and environment references.  
   - Embed memory IDs or ticket references for traceability.

4. **Validate with the checklist**  
   - Walk through `references/handoff_checklist.md` with both outgoing and incoming owners.  
   - Confirm all tasks have owners and due dates, and sensitive information is redacted or linked via secure vault references.

5. **Store and distribute**  
   - Persist the packet in Cogniz for institutional memory:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@handoff\n<completed packet>" `
       --category "project-handoffs" `
       --tags "project:<project-id>,owner:<next-owner>"
     ```  
   - Share the stored memory link or exported file with all stakeholders.  
   - Repackage the skill when updates are made: `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Confirm no secrets or regulated data are embedded; reference secure vaults or ticket IDs instead.  
- Record acknowledgment from incoming owners and store the confirmation in Cogniz.  
- Retain verbose logs when operating in regulated environments for audit trails.  
- Follow organizational retention policies when deleting or superseding handoff packets.

## Resilience & Observability
- Use `--verbose` logging to diagnose missing context or API errors.  
- If no memories are returned, expand the lookback window and prompt teams to capture key updates.  
- Document platform outages or dependency issues and retry once resolved.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager documentation (`../cogniz-memory-manager-local/SKILL.md`).

