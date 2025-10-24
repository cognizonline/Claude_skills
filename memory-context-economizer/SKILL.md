---
name: memory-context-economizer
description: Teach Claude Code workflows that minimize context usage while preserving output quality in VS Code CLI sessions.
version: 1.0.0
---

# Memory Context Economizer

This skill guides Claude Code to deliver high-quality work with the smallest feasible context footprint when collaborating in VS Code/CLI environments.

## Activation Triggers
- Large codebases or documents risk hitting Claude’s context limit.  
- Iterative tasks where only incremental deltas should be shared.  
- Token-sensitive operations (long pair-programming sessions, extensive log analysis).

## Requirements
1. Cogniz configuration available at `C:\Users\[Username]\.cogniz\config.json` (optional but recommended for storing summaries).  
2. Access to Cogniz memory manager scripts through the default relative path, `COGNIZ_MEMORY_MANAGER_PATH`, or `--memory-api-path`.  
3. Python 3.8+ available locally to run helper tooling (`budget_context.py`).  
4. Adoption of the context brief workflow described below before escalating payload size.

## Bundled Resources
- `scripts/budget_context.py` – Estimates token usage for files/stdin and highlights heavy segments (`--verbose`, `--memory-api-path` not required).  
- `references/context_minimization_principles.md` – Ten guiding principles for lean prompts.  
- `assets/context_brief_template.md` – Prompt template (≤400 tokens) for sharing essential context with Claude.

## Standard Operating Procedure
1. **Establish the context budget**  
   - Clarify desired output and acceptable token budget with the user.  
   - Run `scripts/budget_context.py --input-file <path>` to identify large sections and summarise them before pasting.

2. **Prepare a context brief**  
   - Use `assets/context_brief_template.md` to capture objective, key facts, constraints, and exit criteria.  
   - Attach file paths or commands instead of raw content; invite the user to run CLI commands for deeper data.

3. **Stage prompts in priority order**  
   - Send the context brief first.  
   - Provide optional or low-priority data only after Claude confirms necessity.  
   - When diffing code, share minimal patches (e.g., `git diff` snippets) rather than entire files.

4. **Maintain delta-only iterations**  
   - After Claude responds, supply new inputs as minimal diffs or bullet summaries of changes.  
   - Use `budget_context.py --input-file latest.log --top 3` to trim logs before subsequent prompts.

5. **Archive outputs for reuse**  
   - Optionally store final summaries in Cogniz to avoid re-sending:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@context-brief\n<summary or decisions>" `
       --category "context-archives" `
       --tags "project:<slug>,context-economy"
     ```
   - Reference stored IDs in future prompts instead of repeating context.

6. **Package or iterate**  
   - When updating the skill, follow `package_all_skills.py` to produce distributable zips after validation.

## Security & Governance
- Avoid sharing sensitive logs verbatim; summarise incidents and provide redacted paths.  
- Honour user consent for storing context briefs in Cogniz; delete upon request.  
- Log usage of `budget_context.py` and stored summaries if required by compliance.  
- Ensure local scratch files containing raw context are cleaned up after tasks.

## Resilience & Observability
- Use `--verbose` on helper scripts to diagnose large payloads or performance issues.  
- When CLI tools cannot access data (permissions/network), inform the user and request alternate summaries.  
- Capture and version stored context briefs to trace decision histories without re-sending data.

## References
- `references/context_minimization_principles.md` – quick-access best practices for lean prompts.  
- Anthropic documentation: [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills), [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills), [Skills API guide](https://docs.claude.com/en/api/skills-guide).  
- Cogniz Memory Manager instructions in `../cogniz-memory-manager-local/SKILL.md`.

