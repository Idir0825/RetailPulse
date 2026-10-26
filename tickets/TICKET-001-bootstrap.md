# TICKET-001 — Bootstrap the RetailPulse environment

**Epic:** Local development environment  
**Priority:** High  
**Target duration:** 45–75 minutes  
**Status:** Completed (verified 2026-10-11)

> Historical bootstrap ticket, retained as evidence of completed setup. Later tickets use the product-driven template in `_TEMPLATE.md`.

## Context

The company provides a simulated operational database and two external data sources. Before introducing application services or pipelines, the development environment must be reproducible and the supplied fixtures must be accessible.

## Expected outcome

Launch an isolated PostgreSQL database, load the source records, inspect source tables, and capture initial assumptions and risks.

## Environment

- Windows, Docker Desktop, PyCharm and DBeaver.
- PostgreSQL exposed through **`localhost:5433`**, without interfering with another local PostgreSQL on port 5432.
- Generated PostgreSQL CSV files in `data/seed/` and external files in `data/external/`.
- The PostgreSQL `source` schema is an **upstream operational system**, not the intended future analytics warehouse.

## Bootstrap steps (historical)

1. Open the project in PyCharm and initialize a local Git repository (`git init`).
2. Copy `.env.example` to `.env` and inspect `docker-compose.yml`.
3. Start Docker Desktop and run `docker compose up -d`.
4. Confirm a healthy PostgreSQL container with `docker compose ps`.
5. Connect from DBeaver to `localhost:5433` using database/user/password from `.env`.
6. Inspect the `source` schema; tables are initially empty.
7. Load the fixtures using `python scripts/load_source.py` (or `--reset` when intentionally replacing already loaded fixtures).
8. Count `source.customers`, `source.orders`, and `source.stores`, and run a join between orders and customers.
9. Review `data/manifest.json`, `docs/00_cadrage.md`, and `docs/02_data_dictionary.md`.
10. Capture three business questions and three potential data-quality risks for subsequent backlog work.

## PowerShell commands

```powershell
Copy-Item .env.example .env
docker compose up -d
docker compose ps
python scripts/inspect_data.py
python scripts/load_source.py
```

If the generated fixtures are missing, run:

```powershell
python src/simulator/generate.py --output data
```

## Acceptance checks

```sql
SELECT COUNT(*) FROM source.customers; -- 12500
SELECT COUNT(*) FROM source.orders;    -- 200000
SELECT COUNT(*) FROM source.stores;    -- 52

SELECT o.order_id, o.ordered_at, c.customer_id, c.city
FROM source.orders AS o
JOIN source.customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id
LIMIT 10;
```

- [x] PostgreSQL container healthy.
- [x] DBeaver connection to `localhost:5433` works.
- [x] Expected counts loaded (52 stores, 12,500 customers, 200,000 orders).
- [x] The source join works.
- [x] External CSV and JSONL sources exist.
- [x] Distinction between the upstream source schema and a future analytics warehouse understood.
- [x] Three business questions and three data-quality risks documented during review.

## Review evidence

Docker status, expected table counts, an order/customer join and the initial observations were reviewed. The ticket was marked complete before work started on TICKET-002.

## Out of scope

Application ingestion, analytics warehouse, REST API, frontend, GCP and production orchestration.
