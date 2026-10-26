# RetailPulse — Engineering workflow

## Ticket contract

Each ticket describes a **user/operator need**, not a technology to practice. It should contain:

- Actor and problem, with real context for RetailPulse.
- Observable behavior, inputs/outputs and edge cases.
- Constraints and out-of-scope boundaries.
- Acceptance criteria that can be demonstrated or tested.
- Expected deliverables, dependencies and review handoff.

The assignee chooses the design. Do not insert a step-by-step solution into a product ticket. When an important design decision exists, discuss alternatives **before implementation** and document the trade-off. Research and official documentation are permitted.

## Definition of done

- The agreed acceptance criteria are demonstrated.
- Expected failure behavior has been checked.
- Automated tests cover meaningful logic when applicable.
- Relevant documentation and configuration examples are updated.
- No secrets or generated datasets are staged for Git.
- Review feedback is resolved and the delivery is reproducible.

A ticket remains **In review** if corrections are requested, even if most work is finished.

## Git and GitHub cadence

- **Commit** after a cohesive, reviewable change (e.g., add importer CLI, implement validation, add associated tests, fix a documented bug). Work-in-progress commits on a branch are acceptable if clearly labeled.
- **Push** the current branch after meaningful progress, at the end of a development session, or before requesting review; do not wait until the entire project is finished.
- **Pull request / review** once a ticket's acceptance criteria can be demonstrated. Revise and push again if feedback requires changes.
- **Merge** into `main` only after review/validation. Keep `main` reasonably stable.
- For small bootstrap fixes, a simple direct commit may be sufficient; adopt feature branches as product work begins.

Suggested branch names: `feature/ticket-003-supplier-import`, `fix/ticket-002-quality-sql`.

Suggested conventional commit examples:

```text
chore: bootstrap local PostgreSQL sources
docs: define RetailPulse product roadmap
fix: complete source quality checks for ticket 002
feat: import supplier price updates
test: cover invalid supplier records
```

Before staging and pushing:

```powershell
git status
git diff
git add <specific-files>
git diff --cached --stat
git diff --cached
# Inspect staged content before committing
git commit -m "<type>: <short description>"
git push
```

Never stage `.env`, `.venv`, `.idea`, generated CSV/JSONL, or credentials. `data/manifest.json` is small metadata and is deliberately versioned.

## Collaboration sequence

1. Read the ticket and clarify essential contract ambiguities.
2. Propose design when needed; receive critique of the approach, not a prewritten implementation.
3. Implement with documentation available; test locally.
4. Send code, commands, test outputs and trade-offs for review.
5. Apply review notes, commit/push at an appropriate checkpoint, and close the ticket.

**Initial backlog state:** TICKET-001 is completed. TICKET-002 is still in review and needs specific SQL fixes; do not silently replace the author's draft with a completed solution.
