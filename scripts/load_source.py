#!/usr/bin/env python3
"""Load the simulated operational PostgreSQL source using Docker's psql.

This is an environment bootstrapper, NOT the learner's future ingestion pipeline.
Requires Docker Desktop, a healthy `docker compose up -d` and generated CSV files.
No Python database driver necessary.
"""
import argparse
import csv
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = [
    'stores','warehouses','customers','products','orders','order_items',
    'payments','shipments','returns','inventory_movements','support_tickets'
]

def main():
    parser = argparse.ArgumentParser(description='Load RetailPulse source fixtures to postgres')
    parser.add_argument('--reset', action='store_true', help='Clear all existing source rows before loading; required for a reload')
    args = parser.parse_args()
    env = os.environ.copy()
    envfile = ROOT/'.env'
    if envfile.exists():
        for line in envfile.read_text(encoding='utf-8').splitlines():
            if line and not line.lstrip().startswith('#') and '=' in line:
                key, value = line.split('=',1)
                env.setdefault(key.strip(),value.strip())
    user = env.get('POSTGRES_USER','retailpulse')
    db = env.get('POSTGRES_DB','retailpulse')
    command = ['docker','compose','exec','-T','postgres','psql','-X','-v','ON_ERROR_STOP=1','-U',user,'-d',db]
    if args.reset:
        statement = 'TRUNCATE ' + ', '.join('source.'+t for t in reversed(TABLES)) + ' CASCADE;'
        subprocess.run(command+['-c',statement],cwd=ROOT,env=env,check=True)
    for table in TABLES:
        csv_file = ROOT/'data'/'seed'/f'{table}.csv'
        if not csv_file.is_file():
            raise FileNotFoundError(f'Missing {csv_file} — generate sources first')
        print(f'Loading source.{table} ...',flush=True)
        statement = f"COPY source.{table} FROM STDIN WITH (FORMAT csv, HEADER true, NULL '');"
        with csv_file.open('rb') as f:
            subprocess.run(command+['-c',statement],stdin=f,cwd=ROOT,env=env,check=True)
    print('Source PostgreSQL loaded. Inspect source.orders, source.customers, etc. in DBeaver.')

if __name__=='__main__':
    main()
