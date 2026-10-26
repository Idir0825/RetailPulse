# RetailPulse — Product and technical scope

**Project type:** fictional internal retail platform. **Data:** entirely synthetic.

## Problem to solve

An omnichannel electronics retailer sells through 52 physical stores and web/mobile channels, with 6 warehouses. Operational information is distributed across transaction records, supplier file deliveries and web-event feeds.

RetailPulse will provide a maintained backend so internal teams can **ingest external updates, verify processing results, and access consistent operational information**. The goal is an integrated engineering product, not a collection of disconnected SQL exercises or notebooks.

## Intended users and jobs

| User | Need / observable outcome |
|---|---|
| Catalog operator | Import supplier pricing files and understand accepted/rejected records |
| Logistics operator | Retrieve product, stock and fulfillment information from controlled interfaces |
| Platform operator | Inspect failures, replay safe operations, and diagnose incidents |
| Downstream system | Query documented REST endpoints without accessing source tables directly |
| Analyst or manager | Receive reliable, explicitly defined reporting datasets when analytics are introduced |

## Existing upstream sources

| Source | Format | Purpose |
|---|---|---|
| PostgreSQL `source.*` | Relational | Stores, warehouses, customers, products, orders, items, payment attempts, shipments, returns, inventory movements and support tickets |
| `data/external/supplier_prices.csv` | CSV | Supplier price update events with intentionally imperfect data |
| `data/external/web_events.jsonl` | JSON Lines | Web/mobile behavioral events, some anonymous and duplicated |

The provided simulator generates the upstream system. **It is not the implementation of RetailPulse**: its ingestion logic, services, tests, APIs and deployments remain to be built.

## Scope and non-goals

**In scope, progressively:** Python application, import/update operations, persistence, tests, error reporting, reliability, useful data transformations, API access, optional web frontend, orchestration and targeted cloud deployment.

**Out of scope:** implementing a real retail checkout or payment gateway; a complete ERP; multiple services or frameworks merely for their own sake; pretending synthetic data represent real commercial performance.

## Engineering constraints

- Start with Windows, Python 3.12+, Docker Compose, PostgreSQL and Git.
- Protect source records; distinguish upstream `source.*` from future application-managed data and analytics models.
- Keep behavior reproducible for a fresh developer checkout.
- Define observable acceptance criteria and verify them before closing a ticket.
- Prefer modular, readable Python; introduce classes, interfaces and patterns for demonstrable reasons.
- Preserve input provenance, avoid unintended duplicates, and provide actionable failure reports.
- Choose cloud infrastructure and distributed processing only for genuine operational or scale needs.
- Document architectural decisions and relevant trade-offs as the system grows.

## Working method

The backlog is composed of **user or operator needs**. The engineer proposes implementation details, consults documentation, writes code and tests, and presents evidence. A reviewer challenges correctness, robustness and design before acceptance. See [`engineering_workflow.md`](engineering_workflow.md).

## Current delivery boundary

The repository contains **a simulated upstream source and local bootstrap tooling**. No supplier import service, FastAPI application, frontend, pipeline orchestrator, Data Warehouse, or GCP infrastructure is claimed to be complete.

`TICKET-001` is finished. `TICKET-002` contains an initial SQL-based quality baseline, currently awaiting review corrections. New product features begin after that review is closed.
