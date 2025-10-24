---
name: memory-idea-vault
description: Maintain a searchable archive of creative ideas, experiments, and inspiration using Cogniz memories with smart tagging.
version: 1.1.0
---

# Memory Idea Vault

This skill captures brainstorming sparks, customer insights, and creative experiments in a structured vault for rapid prioritisation.

## Activation Triggers
- Ideation workshops, hackathons, or product strategy sessions.  
- Customer interviews and research sprints that surface new opportunities.  
- Leadership planning that requires visibility into innovation backlogs.

## Requirements
1. Cogniz configuration at `C:\Users\[Username]\.cogniz\config.json`.  
2. Tagging conventions aligned with product/marketing (topic, audience, timeline, status).  
3. Agreement on idea lifecycle stages (backlog, in-progress, launched).  
4. Access to Cogniz memory manager scripts via default path, environment variable, or `--memory-api-path`.

## Bundled Resources
- `scripts/log_idea.py` – Stores new ideas with structured metadata and next steps (`--memory-api-path`, `--verbose`).  
- `references/idea_tagging_guide.md` – Taxonomy covering topic, audience, timeline, status, inspiration.  
- `assets/idea_snapshot_template.md` – Template for rich idea descriptions when preparing reviews.

## Standard Operating Procedure
1. **Capture the spark**  
   - Collect title, summary, topic, impact, effort, inspiration, and proposed next step.  
   - Encourage contributors to include owners or reviewers when applicable.

2. **Log via helper script**  
   - Windows / VS Code:  
     ```powershell
     python .\scripts\log_idea.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --title "Memory Automation Playbook Series" `
       --summary "Three-part content series teaching customers how to automate Cogniz memory capture." `
       --topic "content-marketing" `
       --impact high `
       --effort medium `
       --next-step "Draft outline for part one." `
       --reference "memory:8452 customer interview notes" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/log_idea.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --title "Memory Automation Playbook Series" \
       --summary "Three-part content series teaching customers how to automate Cogniz memory capture." \
       --topic "content-marketing" \
       --impact high \
       --effort medium \
       --verbose
     ```

3. **Document richer context (optional)**  
   - Use `assets/idea_snapshot_template.md` to capture personas, user problems, solution approaches, and success metrics.  
   - Link supporting artifacts (Figma, whiteboards, research docs).

4. **Maintain the backlog**  
   - Review by query:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" search `
       --query "category:idea-vault status:backlog timeline:quarter" `
       --limit 50
     ```  
   - Update status to `in-progress` or `launched` by storing follow-up memories referencing the original idea ID.

5. **Promote or archive**  
   - Store status updates summarising progress, decisions, or launch outcomes.  
   - Archive deprioritised ideas with rationale and links to decision logs.  
   - Package the skill with `python package_all_skills.py --dist-dir dist` when distributing updates.

## Security & Governance
- Exclude confidential roadmaps or customer PII; link to secure systems instead.  
- Maintain audit trails for idea approvals and prioritisation decisions.  
- Retain verbose logs when idea capture forms part of regulated innovation pipelines.  
- Apply retention policies to archive or purge stale ideas on a fixed cadence.

## Resilience & Observability
- Use verbose logging to diagnose tagging gaps or dependency issues.  
- If Cogniz returns no results, confirm query filters and repository health.  
- Incorporate periodic backlog reviews to keep the vault actionable.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager skill (`../cogniz-memory-manager-local/SKILL.md`).

