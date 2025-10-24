# Context Minimization Principles

1. **Assert the objective first.** Restate the desired deliverable in ≤2 sentences before sharing supporting material.  
2. **Chunk input by priority.** Provide essential specs first, then optional references. Be explicit about what can be skipped.  
3. **Summarize long artefacts.** Replace raw logs or transcripts with bullet summaries and attach the path for deeper dives.  
4. **Reuse canonical sources.** Link to shared documents instead of pasting duplicates across prompts.  
5. **Delta updates only.** When iterating, send changes since the last response rather than the full file.  
6. **Track token budget.** Keep a running estimate (e.g., `budget_context.py`) and target ≤70% of the model window.  
7. **Archive completion crumbs.** Store final outputs or decisions locally/externally and reference them to avoid re-sending.  
8. **Clean up scratch buffers.** Delete temporary debugging blocks or verbose logs once the issue is resolved.  
9. **Promote reusable snippets.** Move boilerplate instructions into assets or references to keep SKILL.md concise.  
10. **Enforce exit criteria.** Define “done” upfront to prevent unnecessary back-and-forth prompts.

