import unittest
from outbox_crash_replay import run
class Tests(unittest.TestCase):
 def test_actual_process_kills_show_atomic_commit_and_duplicate_delivery(self):
  rows={(r['stage'],r['consumer']):r for r in run({})['scenarios']}
  for mode in ('naive','idempotent'):
   a=rows['before_commit',mode];self.assertEqual(a['domain_rows_after_recovery'],0);self.assertEqual(a['effects_after_recovery'],0)
   a=rows['after_commit',mode];self.assertEqual(a['domain_rows_after_recovery'],1);self.assertEqual(a['effects_after_recovery'],1);self.assertEqual(a['acked_after_recovery'],1)
  self.assertEqual(rows['after_delivery_before_ack','naive']['effects_after_recovery'],2);self.assertEqual(rows['after_delivery_before_ack','idempotent']['effects_after_recovery'],1)
 def test_repeated_owned_runs_leave_same_logical_receipts(self):
  d={'stages':['after_delivery_before_ack'],'consumers':['idempotent']};self.assertEqual(run(d),run(d))
 def test_unknown_stages_rejected(self):
  with self.assertRaises(ValueError):run({'stages':['invented']})
