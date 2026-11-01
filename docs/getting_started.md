# Getting started — local development

This guide initializes the **simulated upstream sources** used during RetailPulse development. The simulator and source loader are bootstrap tooling; they are not the RetailPulse product importer.

## Prerequisites

- Python 3.12+
- Docker Desktop (or Docker Engine) with Compose
- Git
- Optional: DBeaver or another PostgreSQL client

Run commands from the repository root. Examples use PowerShell on Windows.

## 1. Local configuration

```powershell
Copy-Item .env.example .env
```

Keep `.env` local. Use only development credentials from the example for the local PostgreSQL container.

## 2. Generate source fixtures

On a fresh clone, generate the fixture datasets before loading them into PostgreSQL:

```powershell
python src/simulator/generate.py --output data --seed 20261010
python scripts/inspect_data.py
```

If using a project archive that includes `data/seed/` and `data/external/`, generating them again is optional. The expected record counts are in [`data/manifest.json`](../data/manifest.json).

## 3. Start PostgreSQL

```powershell
docker compose up -d
docker compose ps
```

The development database uses PostgreSQL 17 and maps container port `5432` to host port `5433` by default. On creation of a **fresh Docker volume**, `sql/source_schema.sql` initializes schema `source` and its tables. The same SQL is available in the repository and must not be omitted from an archive or Git clone.

## 4. Load the source tables

```powershell
python scripts/load_source.py
```

This is an initial fixture loader. To reload an existing populated source, use its documented `--reset` option deliberately, not repeated blind inserts:

```powershell
python scripts/load_source.py --reset
```

**Warning:** `--reset` truncates `source.*` contents. Docker's `docker compose down -v` deletes the whole database volume, including any app-managed data you may add later.

Connect to PostgreSQL using `localhost:5433`, database/user `retailpulse`, and password defined in your local `.env`.

Sanity checks:

```sql
SELECT COUNT(*) FROM source.customers; -- 12500
SELECT COUNT(*) FROM source.orders;    -- 200000
SELECT COUNT(*) FROM source.stores;    -- 52
```

## 5. Develop RetailPulse itself

Once the fixtures are ready, the next product capability is **supplier cost import**. Its input file is `data/external/supplier_prices.csv`; it contains supplier cost updates rather than retail list prices. No product ingestion command or API exists in the bootstrap alone. See the [roadmap](01_roadmap.md), [product specification](product_spec.md), and [architecture](architecture.md) before choosing the first implementation.

## Troubleshooting

- **Container is healthy but tables are absent:** verify `sql/source_schema.sql` exists and whether the volume was created before the initialization script was mounted. PostgreSQL initialization scripts run only for a new data directory.
- **Loader reports primary-key conflicts:** data may already be populated; do not reset or truncate unless existing data can safely be discarded.
- **Data files missing on a clone:** regenerate the fixtures using the simulator.
- **Port 5433 unavailable:** adjust `POSTGRES_PORT` in `.env` and connect using the chosen host port.
