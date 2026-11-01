# RetailPulse — Development roadmap

This is a **living milestone plan**, not a list of mandatory tickets or a fixed teaching schedule. Each step exists because it creates a usable capability. The next step is chosen when the preceding work and current constraints are understood.

## Current implementation boundary

- A deterministic generator creates synthetic PostgreSQL, supplier CSV, and JSONL source datasets.
- Docker Compose and the bootstrap loader can initialize the PostgreSQL `source` schema.
- The initial Git baseline is established.
- **Not yet implemented:** RetailPulse's application importer, application-managed persistence, API, frontend, job history, automated product tests, or GCP deployment.

The earlier SQL profiling exercise has been retired as a delivery requirement. Historical work can remain in Git history; there is **no open ticket to close** before product development starts.

## Product milestones

| Phase | User-visible outcome | Engineering work driven by the need | Evidence |
|---|---|---|---|
| 1. Supplier import | A catalog operator can submit supplier cost updates via CLI. | Python application entry point, input contracts, database persistence, focused tests. | Import succeeds; invalid input is reported; reruns behave safely. |
| 2. Operational reliability | An operator can inspect, understand, and retry processing runs. | Execution metadata, transaction boundaries, structured logging, failure recovery, integration tests. | Demonstrable success, rejection, and crash/retry scenarios. |
| 3. Backend access | Internal software can query products, supplier updates, and job results. | REST API, service boundaries, pagination, error contracts, API tests. | Documented, repeatable HTTP interactions. |
| 4. Cross-source processing | Supported records from operational sources can be synchronized. | Incremental extraction, change handling, validated transformations, scheduling when justified. | Recoverable repeated processing with measured results. |
| 5. Operator frontend | Staff can use important workflows from a browser. | Frontend connected to the API, navigation, loading/error states, end-to-end tests. | Import and inspection workflows work without a terminal. |
| 6. Deployment and operations | The application can be deployed and observed reliably. | CI/CD, containers, configuration/secrets, targeted GCP services, health and monitoring. | Reproducible deployment and actionable diagnostics. |
| 7. Applied optimization | A genuine operational bottleneck is improved. | Algorithm profiling, rule-based baseline, optional NumPy/ML where beneficial. | Measured improvement against a documented baseline. |

The order can change when dependencies or product value warrant it. Testing, documentation, version control, and architecture discussions accompany **every phase**, not just the last.

## Next development move

**Start the supplier cost import capability.** Before implementation, agree on the expected command-line behavior and minimum database contract, particularly deduplication, invalid records, and source-versus-owned tables. Implement the smallest useful vertical slice, add tests, review, and commit/push at meaningful checkpoints.

## Technology selection rule

Use the simplest tool that solves the current need. Python, PostgreSQL, and Docker are the present foundation. FastAPI, React/TypeScript, GCP, and additional data/analytics tooling are **planned directions**, not functionality claimed as complete. Avoid microservices or distributed frameworks without evidence of need.
