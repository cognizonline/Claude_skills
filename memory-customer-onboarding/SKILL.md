---
name: memory-customer-onboarding
description: Guide new customer onboarding by reusing Cogniz memories from past implementations and logging fresh milestones.
---

# Memory Customer Onboarding

This skill operationalises customer onboarding by combining historical playbooks, discovery notes, progress updates, and blockers stored in Cogniz.

## Activation Triggers
- New customer implementation or expansion kickoffs.  
- Reset of onboarding programs after delays or change requests.  
- Leadership demand for clear onboarding status and risk visibility.

## Requirements
1. Cogniz configuration at `C:\Users\[Username]\.cogniz\config.json`.  
2. Account tag/project ID aligned across onboarding memories (`account:beacon-labs`, etc.).  
3. Target launch date, phase ownership, and stakeholder roster confirmed.  
4. Cogniz memory manager scripts reachable via default path, environment variable, or `--memory-api-path`.

## Bundled Resources
- `scripts/build_onboarding_plan.py` – Compiles playbooks, discovery notes, progress updates, and blockers (`--memory-api-path`, `--verbose`).  
- `references/onboarding_phase_guidelines.md` – Detailed guidance for kickoff, integration, enablement, launch, and post-launch phases.  
- `assets/onboarding_plan_template.md` – Fillable plan template for cross-functional alignment.

## Standard Operating Procedure
1. **Collect inputs**  
   - Confirm industry, success metrics, launch date, and implementation leads.  
   - Ensure discovery notes are captured; prompt sales or success teams if gaps exist.

2. **Generate the draft plan**  
   - Windows / VS Code:  
     ```powershell
     if (!(Test-Path .\out)) { New-Item -ItemType Directory out | Out-Null }
     python .\scripts\build_onboarding_plan.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --account "<account-slug>" `
       --industry "finance" `
       --output ".\out\onboarding-plan.md" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/build_onboarding_plan.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --account "<account-slug>" \
       --industry "finance" \
       --verbose
     ```  
   - Modify `--industry`, `--limit`, or `--memory-api-path` as needed.

3. **Tailor the plan**  
   - Transfer insights into `assets/onboarding_plan_template.md`.  
   - Map tasks to phase owners, due dates, and success metrics using `references/onboarding_phase_guidelines.md`.  
   - Document blockers with mitigation owners and escalation paths.

4. **Review with stakeholders**  
   - Walk through the plan during kickoff/status calls; log decisions as new Cogniz memories tagged `onboarding-progress`.  
   - Update the template when milestones complete or scope changes.

5. **Store plan and retrospectives**  
   - Persist the plan:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@onboarding-plan\n<completed template>" `
       --category "onboarding" `
       --tags "account:<account-slug>,phase:plan"
     ```  
   - After launch, store a retrospective tagged `phase:retro` for reuse on future projects.  
   - Package releases with `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Protect customer credentials, architecture diagrams, and compliance artefacts—reference secure vaults rather than embedding secrets.  
- Track stakeholder approvals and attach meeting notes to the stored plan.  
- Retain verbose logs when operating in regulated industries for audit readiness.  
- Apply data retention policies when archiving or deleting historical onboarding documents.

## Resilience & Observability
- Use verbose logging to identify missing playbooks or tagging inconsistencies.  
   - Document upstream system outages (CRM, analytics) and refresh the plan once data sync resumes.  
- Maintain version history in Cogniz to monitor onboarding progress across revisions.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager skill (`../cogniz-memory-manager-local/SKILL.md`).

