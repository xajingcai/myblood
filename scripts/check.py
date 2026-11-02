"""Structural validation only; not clinical triage."""
from pathlib import Path
from datetime import datetime
import json
import math
import re
import sys
ROOT = Path(__file__).resolve().parents[1]

def validate(rows):
    errors = []
    if not isinstance(rows, list):
        return ['Records must be a JSON array.']
    seen = set()
    sessions = {}
    for i, x in enumerate(rows, 1):
        prefix = f'Record {i}: '
        if not isinstance(x, dict):
            errors.append(prefix + 'must be an object'); continue
        try:
            dt = datetime.fromisoformat(x['timestamp'])
            if dt.utcoffset() is None: raise ValueError()
        except (KeyError, TypeError, ValueError):
            errors.append(prefix + 'timestamp needs ISO datetime and timezone'); dt = None
        sid = x.get('session_id')
        if not isinstance(sid, str) or not sid.strip():
            errors.append(prefix + 'session_id required'); sid = None
        idx = x.get('reading_index')
        if type(idx) is not int or idx < 1:
            errors.append(prefix + 'reading_index must be a positive integer'); idx = None
        period = x.get('period')
        if period not in ('morning', 'evening', 'other'):
            errors.append(prefix + 'invalid period')
        for key in ('systolic', 'diastolic'):
            v = x.get(key)
            if type(v) not in (int, float) or not math.isfinite(v) or v <= 0:
                errors.append(prefix + key + ' must be a finite positive number')
        a, b = x.get('systolic'), x.get('diastolic')
        if type(a) in (int, float) and type(b) in (int, float) and a <= b:
            errors.append(prefix + 'systolic must exceed diastolic; verify source')
        pulse = x.get('pulse')
        if pulse is not None and (type(pulse) not in (int, float) or not math.isfinite(pulse) or pulse <= 0):
            errors.append(prefix + 'pulse must be null or finite positive number')
        if type(x.get('included')) is not bool:
            errors.append(prefix + 'included must be boolean')
        if x.get('included') is False and not str(x.get('exclusion_reason') or '').strip():
            errors.append(prefix + 'excluded record needs reason')
        if sid is not None and idx is not None:
            key = (sid, idx)
            if key in seen: errors.append(prefix + 'duplicate session/index')
            seen.add(key)
        if sid is not None and dt is not None:
            signature = (dt.date().isoformat(), period, str(dt.utcoffset()))
            if sid in sessions and sessions[sid] != signature:
                errors.append(prefix + 'session spans dates, periods or offsets')
            sessions[sid] = signature
    return errors

def load_records(path):
    rows = json.loads(path.read_text(encoding='utf-8-sig'))
    errors = validate(rows)
    if errors: raise ValueError('\n'.join(errors))
    return rows

def main():
    errors = []
    for f in ROOT.rglob('*.md'):
        if '.git' in f.parts: continue
        for link in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', f.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#'): continue
            if not (f.parent / link.split('#')[0]).exists():
                errors.append(f'{f.relative_to(ROOT)}: missing link {link}')
    path = ROOT / 'private/readings.json'
    if path.exists():
        try:
            rows = load_records(path)
            print(f'Records validated: {len(rows)}')
        except (ValueError, OSError) as exc: errors.append(str(exc))
    else: print('Private readings absent: CI checks structure only.')
    if errors:
        print('\n'.join(errors)); return 1
    print('PASS: structural checks only; clinical safety not assessed.')
    return 0

if __name__ == '__main__': sys.exit(main())
