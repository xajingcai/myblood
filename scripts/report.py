"""Descriptive summaries; no diagnosis or forecast."""
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import json
import sys
from check import load_records

def summarize(rows):
    groups = defaultdict(list)
    for x in rows:
        if x['included']:
            day = datetime.fromisoformat(x['timestamp']).date().isoformat()
            groups[(day, x['session_id'])].append(x)
    days = defaultdict(list)
    incomplete = []
    for (day, sid), xs in groups.items():
        days[day].append([sum(x[k] for x in xs)/len(xs) for k in ('systolic','diastolic')])
        if len(xs) < 2: incomplete.append(sid)
    daily = {day: [sum(v[i] for v in ss)/len(ss) for i in (0,1)] for day,ss in sorted(days.items())}
    return {
        'raw_records': len(rows),
        'excluded_records': sum(not x['included'] for x in rows),
        'included_days': len(daily),
        'included_sessions': len(groups),
        'sessions_with_less_than_two_included_readings': incomplete,
        'daily_mean_mmHg': daily,
        'equal_day_mean_mmHg': [sum(v[i] for v in daily.values())/len(daily) for i in (0,1)] if daily else None,
        'scope': 'All recorded included dates; not automatically a weekly report. Missing dates are not imputed.',
        'prediction': 'Not generated; descriptive data only.'
    }

if __name__ == '__main__':
    path = Path(__file__).resolve().parents[1] / 'private/readings.json'
    try:
        result = summarize(load_records(path))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr); sys.exit(1)
