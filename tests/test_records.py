import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check import validate
from report import summarize

def row(day=1, sid='a', idx=1, sbp=120, included=True):
    return dict(timestamp=f'2026-11-{day:02d}T07:00:00+08:00', session_id=sid,
                reading_index=idx, period='morning', systolic=sbp, diastolic=70,
                included=included, exclusion_reason='' if included else 'movement')

class RecordsTest(unittest.TestCase):
    def test_empty_has_no_prediction(self):
        self.assertEqual(validate([]), [])
        self.assertIsNone(summarize([])['equal_day_mean_mmHg'])
    def test_duplicate_rejected(self):
        self.assertTrue(validate([row(), row()]))
    def test_missing_timezone_rejected(self):
        x = row(); x['timestamp'] = '2026-11-01T07:00:00'
        self.assertTrue(validate([x]))
    def test_exclusion_requires_reason(self):
        x = row(included=False); x['exclusion_reason'] = ''
        self.assertTrue(validate([x]))
    def test_nonfinite_rejected(self):
        self.assertTrue(validate([row(sbp=float('nan'))]))
    def test_session_cannot_span_dates(self):
        self.assertTrue(validate([row(), row(day=2,idx=2)]))
    def test_day_weighting_and_exclusion(self):
        xs = [row(sbp=120), row(idx=2,sbp=120), row(sid='b',sbp=120),
              row(day=2,sid='c',sbp=140), row(day=2,sid='c',idx=2,sbp=200,included=False)]
        self.assertEqual(validate(xs), [])
        out = summarize(xs)
        self.assertEqual(out['equal_day_mean_mmHg'], [130,70])
        self.assertEqual(out['excluded_records'], 1)
        self.assertIn('c',out['sessions_with_less_than_two_included_readings'])

if __name__ == '__main__': unittest.main()
