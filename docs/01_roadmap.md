# RetailPulse — Feature roadmap

> Indicative delivery sequence, driven by product needs and reviewed ticket by ticket. Dates and tools are **not commitments**.

## Delivery status

| Ticket / milestone | Scope | Status |
|---|---|---|
| TICKET-001 | Operational source bootstrap | **Completed** |
| TICKET-002 | Initial source-quality baseline | **In review — changes requested** |
| Next feature (ticket to be created) | Supplier price import from CSV | Planned |

**Remaining work on TICKET-002:** correct SQL sections A3 (all channel violations), B2 (nonempty normalized email groups and count), and C3 (stable ordered top five); make labels valid SQL comments and qualify `source.*` references. Preserve the author's work; do not close this ticket prematurely.

## Planned product milestones

| Sequence | User problem / outcome | Candidate engineering work | Evidence of completion |
|---|---|---|---|
| 1. Supplier updates | Catalog staff can import supplier prices without manual database edits | Python CLI/service, schema validation, persistence, transactions | Import works, errors are actionable, repeat imports are safe |
| 2. Reliable operations | Operators can diagnose and replay failed imports | Idempotency, batch tracking, logging, quarantined records, unit/integration tests | Failed runs do not corrupt data; results are reproducible |
| 3. Programmatic access | Internal applications can access supported RetailPulse data | REST API, contracts, pagination, service boundaries, API tests | Documented endpoints with stable behavior |
| 4. Multi-source processing | New source data can be integrated on a recurring basis | Incremental extraction, transformations, scheduling, data quality, SQL | Automated runs with measurable success/failure and recovery |
| 5. Operator interface | People can operate RetailPulse without a terminal | Frontend consuming the API; import status, errors, stock/product views | End-to-end workflows from a browser |
| 6. Deployment and reliability | The system can be deployed and operated consistently | Docker, CI/CD, secrets, targeted GCP components, metrics, recovery | Repeatable deployment, tests, observability |
| 7. Advanced capabilities | Improve a real operational bottleneck | Algorithmic inventory/reorder suggestion, profiling/optimization, optional ML | Baseline comparison and explicit evaluation of benefit |

Milestones can overlap, and testing/documentation/Git discipline apply from the beginning rather than at the end.

## Technical direction

- **Python software engineering:** modularity, appropriate OO design, clear boundaries, tests and maintenance.
- **Data/cloud:** PostgreSQL, ingestion, incremental processing, data quality and justified GCP use.
- **System design:** requirements, separation of concerns, scaling and trade-off documentation.
- **Algorithms:** performance and applied optimization only when there is a real problem to solve.
- **Frontend:** planned after a usable backend contract; technology chosen at the time (web UI is a candidate, not an implemented feature).

The backend should initially remain a **well-structured monolith** unless concrete constraints justify splitting it up.

## Next actions

1. Finish and review TICKET-002.
2. Record a coherent initial repository commit/push (or the first documentation baseline commit if bootstrap is already committed).
3. Create the first product feature ticket around importing supplier pricing data.
4. Review the proposed design **before** an implementation when interfaces or schema changes have meaningful consequences.
