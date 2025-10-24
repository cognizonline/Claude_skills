---
name: memory-quarterly-review
description: Assemble quarterly business reviews by mining Cogniz memories for goals, metrics, highlights, and risks.
version: 1.1.0
---

# Memory Quarterly Review

This skill orchestrates Cogniz memories into quarter-end narratives, providing leadership with a consistent view of goals, metrics, customer impact, and risks.

## Activation Triggers
- Quarter-end reviews, QBR preparations, or strategic retrospectives.  
- Compliance or audit checkpoints requiring a verified quarterly record.  
- Cross-functional storytelling for portfolio, product, or program updates.

## Requirements
1. Cogniz configuration in `C:\Users\[Username]\.cogniz\config.json`.  
2. Quarter tagging applied consistently (for example `quarter:2025-Q3`).  
3. Defined scope (team, product line, company-wide) and required sections.  
4. Access to Cogniz memory manager scripts via relative path, environment variable, or `--memory-api-path`.

## Bundled Resources
- `scripts/compile_review.py` – Aggregates category-specific memories into an outline (`--memory-api-path`, `--verbose`).  
- `references/quarterly_review_data_map.md` – Maps memory categories to review sections.  
- `assets/quarterly_review_outline.md` – Template for the final narrative or slide-ready content.

## Standard Operating Procedure
1. **Clarify scope**  
   - Confirm quarter label, audience, and required annexes.  
   - Update the data map when new memory categories are introduced.

2. **Run the compilation helper**  
   - Windows / VS Code:  
     ```powershell
     if (!(Test-Path .\out)) { New-Item -ItemType Directory out | Out-Null }
     python .\scripts\compile_review.py `
       --config "C:\Users\[Username]\.cogniz\config.json" `
       --quarter "2025-Q3" `
       --output ".\out\2025-Q3-review.md" `
       --verbose
     ```  
   - Claude web UI bash tool:  
     ```bash
     python3 scripts/compile_review.py \
       --config "/Users/[Username]/.cogniz/config.json" \
       --quarter "2025-Q3" \
       --verbose
     ```  
   - Use `--categories` to tailor the section list; add `--memory-api-path` when required.

3. **Synthesize the narrative**  
   - Annotate each section using `references/quarterly_review_data_map.md`.  
   - Populate `assets/quarterly_review_outline.md` with KPI tables, customer stories, and next-quarter priorities.  
   - Attach supporting charts or dashboards as appendices.

4. **Validate accuracy**  
   - Confirm metrics with data owners and note the source (dashboard, warehouse extract).  
   - Validate risk statuses and mitigation owners with program leads.  
   - Capture open data gaps with owners and deadlines.

5. **Store and package**  
   - Persist the narrative:  
     ```powershell
     python ..\cogniz-memory-manager-local\scripts\memory_api.py `
       --config "C:\Users\[Username]\.cogniz\config.json" store `
       --content "@quarterly-review\n<final outline or memo>" `
       --category "quarterly-reviews" `
       --tags "quarter:2025-Q3,scope:<team>"
     ```  
   - Package the skill for distribution when updates land: `python package_all_skills.py --dist-dir dist`.

## Security & Governance
- Ensure sensitive metrics align with corporate data classifications; redact customer or employee PII.  
- Maintain author and approver metadata for audit readiness.  
- Store `--verbose` logs alongside the deliverable when operating in regulated environments.  
- Reference secure vaults instead of embedding credentials or links to restricted systems.

## Resilience & Observability
- Leverage verbose logging to troubleshoot API errors or missing categories.  
- Document upstream data outages (analytics warehouse, CRM) and revisit the review once data flows resume.  
- Version stored outlines to track quarterly deltas and facilitate roll-forward analysis.

## References
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)  
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)  
- [Skills API guide](https://docs.claude.com/en/api/skills-guide)  
- Cogniz Memory Manager skill (`../cogniz-memory-manager-local/SKILL.md`).

