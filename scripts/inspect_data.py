#!/usr/bin/env python3
"""Validate fixture counts without a PostgreSQL or Docker dependency."""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data'/'manifest.json').read_text(encoding='utf-8'))
for name, expected in manifest['counts'].items():
    ext=name in {'supplier_prices','web_events'}
    suffix='.jsonl' if name=='web_events' else '.csv'
    path=ROOT/'data'/('external' if ext else 'seed')/(name+suffix)
    with path.open(encoding='utf-8',newline='') as f:
        actual=sum(1 for _ in f)-(0 if name=='web_events' else 1)
    mark='OK' if expected==actual else 'MISMATCH'
    print(f'{mark:8} {name:22} expected={expected:>8,} actual={actual:>8,}')
    if actual!=expected: raise SystemExit(1)
print('All counts match manifest.')
