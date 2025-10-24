---
name: memory-learning-tracker
description: Track learning goals, organize notes, and schedule revisits using Cogniz memories and spaced repetition prompts.
version: 1.1.0
---

# Memory Learning Tracker

This skill helps learners capture session notes, create spaced repetition reminders, and monitor progress inside Cogniz.

## Activation Triggers
- After study sessions, workshops, or mentoring calls.  
- Preparing for certifications or technical interviews.  
- Coaching scenarios that require accountability across sessions.

## Requirements
1. Cogniz configuration at `C:\Users\[Username]\.cogniz\config.json`.  
2. Topic taxonomy agreed with the learner (for example `topic:rust-ownership`).  
3. Preferred review cadence (defaults to spaced repetition intervals).  
4. Access to Cogniz memory manager scripts through default path, env var, or `--memory-api-path`.

## Bundled Resources
- `scripts/log_learning.py` – Stores learning notes and optional reminders (`--memory-api-path`, `--verbose`).  
- `references/spaced_repetition_intervals.md` – Guidance for review scheduling.  
- `assets/learning_session_template.md` – Template for takeaways, practice results, and next actions.

## Standard Operating Procedure
1. **Capture session notes**  
   - Prompt for takeaways, practice outcomes, open questions, and next steps.  
   - Fill `assets/learning_session_template.md` (for example `learning_rust_2025-10-20.md`).

2. **Log the session**  
   - Windows / VS Code:  
     ```powershell
     python .\scripts\log_learning.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --topic "rust-ownership" `
       --notes-file ".\learning_rust_2025-10-20.md" `
       --review-in-days 7 `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/log_learning.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --topic "rust-ownership" \
       --notes-file "./learning_rust_2025-10-20.md" \
       --review-in-days 7 \
       --verbose
     ```  
   - Add `--no-reminder` to skip follow-up creation or `--memory-api-path` if dependencies are relocated.

3. **Tune reminders**  
   - Adjust `--review-in-days` using `references/spaced_repetition_intervals.md`.  
   - Rerun the script with additional intervals (1, 30, 90 days) when needed.

4. **Retrieve history**  
   - Summarise progress before reviews or assessments:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" search `
       --query "category:learning topic:rust-ownership" `
       --limit 25 `
       --sort-by date
     ```  
   - Consolidate findings into study plans or coaching updates.

5. **Reflect and iterate**  
   - After completing a review, store a progress update tagged `status:completed`.  
   - Note blockers or new questions to prioritise future sessions.  
   - Package updates when sharing the skill: `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Respect learner privacy; avoid storing sensitive personal details.  
- Encourage removal of outdated reminders to comply with retention policies.  
- Maintain verbose logs when skill usage falls under coaching or HR programmes.  
- Confirm deletion requests promptly and document the action.

## Resilience & Observability
- Use verbose logging to diagnose missing dependencies or API errors.  
- Retry logging if Cogniz services are unavailable; keep local notes until resolved.  
- Periodically review tags to ensure topics and statuses remain consistent.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager skill (`../cogniz-memory-manager-local/SKILL.md`).

