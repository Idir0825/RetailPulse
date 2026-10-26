# Getting started — local development

This guide covers the **upstream simulation and PostgreSQL bootstrap** supplied with RetailPulse. These tools seed a local environment; they are not the RetailPulse application ingestion engine.

## Prerequisites

- Python 3.12 or newer
- Docker Desktop (or Docker Engine) with Docker Compose
- Git
- Optional: DBeaver for browsing PostgreSQL

Run all commands from the repository root. Examples below use **PowerShell**; adapt the environment-variable copy command for your shell.

## 1. Create local configuration

```powershell
Copy-Item .env.example .env
```

The `.env` file holds **local-only** configuration and should never be committed to Git. Default database settings are defined in `.env.example`.

## 2. Generate sample source files

On a Git clone, generate the CSV and JSONL fixtures before loading them. They are excluded from Git because they can be reproduced:

```powershell
python src/simulator/generate.py --output data --seed 20261010
```

If you received a project archive containing `data/seed/` and `data/external/`, you can skip generation.

The default data generation can consume time and disk space. Verify the resulting counts:

```powershell
python scripts/inspect_data.py
```

The expected counts are described by [`data/manifest.json`](../data/manifest.json).

## 3. Start PostgreSQL

```powershell
docker compose up -d
docker compose ps
```

The Compose configuration provides PostgreSQL 17 and initializes the `source` schema for a **new database volume**. The default host port is `5433`.

## 4. Load the source data

```powershell
python scripts/load_source.py
```

The script uses Docker and PostgreSQL `COPY` to load the generated CSV files into `source.*` tables. It is intended for **initial fixture loading**; running it repeatedly against populated tables can cause primary-key conflicts.

Connect with DBeaver (or another PostgreSQL client):

| Setting | Default |
|---|---|
| Host | `localhost` |
| Port | `5433` |
| Database | `retailpulse` |
| Username | `retailpulse` |
| Password | See local `.env` |

Check the source data:

```sql
SELECT COUNT(*) FROM source.customers;
SELECT COUNT(*) FROM source.orders;
SELECT COUNT(*) FROM source.stores;
```

With default settings, the counts are **12,500**, **200,000**, and **52** respectively.

## Resetting local fixtures

To discard and reload the **simulated source tables**:

```powershell
python scripts/load_source.py --reset
```

**Caution:** `--reset` truncates the `source` tables. It does not just append missing records. Use it only for expendable local fixture data.

Docker's named volume persists after `docker compose down`. Running `docker compose down -v` deletes that volume and its database contents.

## Where to go next

- [Product overview](../README.md)
- [Data dictionary](02_data_dictionary.md)
- [Architecture and boundaries](architecture.md)
- [Feature roadmap and delivery status](01_roadmap.md)
- [Engineering workflow](engineering_workflow.md)
