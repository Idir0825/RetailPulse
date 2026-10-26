# RetailPulse — Architecture overview

## Implemented today

```text
Synthetic generator (src/simulator/generate.py)
           |
           +--> data/seed/*.csv ------> scripts/load_source.py
           |                                   |
           |                                   v
           |                          Docker PostgreSQL 17
           |                              schema: source.*
           |
           +--> data/external/supplier_prices.csv
           +--> data/external/web_events.jsonl
```

The simulator and loader are **bootstrap tooling**. They are not the planned application import pipeline. The repository currently contains only the operational fixture database and read-only quality assessment work.

## Proposed evolution — not implemented

```text
PostgreSQL source.*       Supplier CSV / web JSONL      External APIs
         \                       |                        /
          \                      |                       /
           +---------- Python ingestion / services -----+
                                 |
                    Validation, batch tracking,
                    transactions and diagnostics
                                 |
                  Application-owned persistence
                                 |
             +-------------------+------------------+
             |                                      |
         REST API                            Scheduled jobs
             |                                      |
     Operator frontend                     Analytics / GCP
```

**Rationale:** a small, modular Python backend can serve the first workflows without distributed infrastructure. Database and service boundaries will be designed during feature implementation; naming above does not establish a committed stack beyond the current bootstrap.

## Architectural principles

1. **Protect upstream data:** keep `source.*` distinct from any RetailPulse-owned operational or analytical tables.
2. **Simple first:** defer queues, microservices and multiple databases until their operational value is clear.
3. **Observable behavior:** record what each operation received, changed, accepted and rejected.
4. **Safe retries:** repeat processing without duplicate side effects or partial corruption where possible.
5. **Testable boundaries:** distinguish file/API access, validation, application behavior and persistence.
6. **API before UI:** let a future frontend consume a documented contract rather than querying the database directly.
7. **Evidence over claims:** only label features implemented after running acceptance checks.

## Open decisions

- Storage schema and conflict policy for supplier pricing (decide with the first import ticket).
- Error/rejection contract and batch status model (as operating requirements emerge).
- Scheduling, analytics and GCP services (defer until workloads exist).
- Frontend choice and authorization model (defer until the API and users are defined).

Record significant trade-offs in short Architecture Decision Records when they arise, not as prework disconnected from a feature.
