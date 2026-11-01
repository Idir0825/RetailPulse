# RetailPulse — Engineering workflow

RetailPulse is developed as **one evolving product**, without educational tickets or a mandatory exercise queue. An implementation begins with the next useful user-facing behavior, not with a technology to practice.

## Working together

1. **Choose the next useful outcome.** Describe what an operator, internal client, or component needs to do and how success will be observed.
2. **Think before coding when necessary.** Propose the design and identify uncertainties; ask for a review when interfaces, data models, or reliability choices matter.
3. **Build independently.** Official docs, Internet research, examples, and relevant courses are allowed. Ask for progressive hints and diagnosis rather than a prewritten solution.
4. **Verify behavior.** Run the application, check failure cases, write focused unit/integration tests, and capture relevant outputs.
5. **Review and improve.** Share code, errors, test results, and trade-offs; apply technical feedback before merging.
6. **Move forward.** Ask for the next milestone only when appropriate; there is no obligation to work every day or follow a rigid timetable.

The learning target is approximately **85% hands-on problem solving / 15% contextual theory**. Long-term areas: Python/software engineering (35%), data/cloud (30%), architecture/system design (20%), algorithms/applied AI (15%). These are priorities, **not ticket quotas** or reasons to add technology without product value.

## Definition of done

A meaningful unit of work is complete when its expected behavior is demonstrated, relevant negative cases are tested, documentation/configuration is current, review notes are addressed, and changes can be reproduced without personal environment state.

## Git/GitHub workflow

- **Branch:** create a descriptive branch from a reasonably clean `main` for a cohesive product change, e.g. `feature/supplier-import` or `docs/product-spec`.
- **Commit:** record a logically coherent change after it works or at a useful checkpoint (e.g. `feat: add supplier import entrypoint`, `test: cover malformed cost rows`). A commit is not required after each tiny edit.
- **Push:** push work regularly, especially when finishing a session, backing up substantial changes, or requesting review. Pushing does not mean merging.
- **Pull request:** open a PR when the feature is reviewable and its success criteria can be demonstrated. Update it after review.
- **Merge:** integrate into `main` only after relevant validation. Keep `main` usable.

Useful PowerShell checks:

```powershell
git status
git diff
git diff --cached
git log -3 --oneline
```

For new feature work, typically:

```powershell
git switch main
git pull --ff-only
git switch -c feature/supplier-import
# implement, test, review
git add <selected-paths>
git diff --cached
git commit -m "feat: implement supplier cost import"
git push -u origin feature/supplier-import
```

These are **illustrative commands**, not a request to commit a feature before it exists. The assistant should explain the right commit/push moment based on the actual changes and state. Never commit `.env`, `.venv`, IDE files, real credentials, or large generated fixtures.

## Notes on historical work

The former ticket-based workflow has been discontinued. Removed ticket artifacts need not be recreated or finished. The initial Git commit remains part of repository history; historical branch names may remain in Git without being relevant to current work.
