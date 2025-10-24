---
name: memory-personal-journal
description: Capture and compress daily reflections, highlights, and follow-ups using the Cogniz Memory Platform.
version: 1.1.0
---

# Memory Personal Journal

This skill supports daily reflection habits by prompting, formatting, and (optionally) storing personal journal entries within Cogniz.

## Activation Triggers
- Start or end-of-day reflection routines.  
- Coaching or wellbeing check-ins requiring progress tracking.  
- Recording highlights after significant events (presentations, milestones).

## Requirements
1. Cogniz configuration at `C:\Users\[Username]\.cogniz\config.json`.  
2. Agreed tagging/privacy expectations (for example dedicated project `project:journal`).  
3. Consent from the journal owner before storing entries.  
4. Access to Cogniz memory manager scripts via adjacent path, environment variable, or `--memory-api-path`.

## Bundled Resources
- `scripts/log_entry.py` – Formats entries from a text file and optionally stores them (`--memory-api-path`, `--verbose`).  
- `references/daily_prompt_bank.md` – Rotating prompt sets covering reflection, gratitude, growth, wellbeing.  
- `assets/journal_entry_template.md` – Pre-structured Markdown template for manual entry.

## Standard Operating Procedure
1. **Prompt the entry**  
   - Select prompts from `references/daily_prompt_bank.md`.  
   - Encourage responses following `assets/journal_entry_template.md`.

2. **Prepare the journal file**  
   - Create a dated file (for example `journal_2025-10-20.txt`) based on the template.  
   - Capture highlights, challenges, takeaways, gratitude, and next actions.

3. **Format and (optionally) store**  
   - Windows / VS Code:  
     ```powershell
     python .\scripts\log_entry.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --content-file ".\journal_2025-10-20.txt" `
       --date 2025-10-20 `
       --store `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/log_entry.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --content-file "./journal_2025-10-20.txt" \
       --date 2025-10-20 \
       --store \
       --verbose
     ```  
   - Omit `--store` to keep the entry local; use `--memory-api-path` if the memory manager scripts are elsewhere.

4. **Manual storage (optional)**  
   - When storing without the helper, include date tags and consent notes:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@journal\n<final entry>" `
       --category "personal-journal" `
       --project-id "<project-id>"
     ```

5. **Review history**  
   - Retrieve past entries to summarise progress:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" search `
       --query "category:personal-journal last-14-days" `
       --limit 14
     ```

## Security & Governance
- Respect privacy and consent—do not store journal entries without explicit approval.  
- Encourage anonymisation or redaction of sensitive personal information.  
- Store `--verbose` logs securely if journaling falls under wellbeing or HR programmes.  
- Honor deletion/redaction requests promptly and confirm removal via Cogniz.

## Resilience & Observability
- Use verbose logging to troubleshoot config or dependency issues.  
- If the Cogniz API is unreachable, keep entries local and retry after service restoration.  
- Encourage weekly summaries to monitor recurring themes and wellbeing signals.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager skill (`../cogniz-memory-manager-local/SKILL.md`).

