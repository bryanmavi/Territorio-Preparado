import unittest
from server import demo_records, reconcile
class CountingTests(unittest.TestCase):
 def test_report_overlap_not_counted_twice(self):
  r=reconcile(demo_records());self.assertEqual((r['reports'],r['unique_people'],r['duplicate_reports'],r['households']),(128,104,24,32));self.assertEqual(r['shelter_people'],78)
 def test_missing_identity_is_not_a_person(self):
  r=reconcile([{'source':'brigada'}, {'person_id':'DEMO-1','household_id':'H-1'}]);self.assertEqual(r['unique_people'],1);self.assertEqual(r['excluded'],1)
 def test_disagreement_requires_review(self):
  r=reconcile([{'person_id':'DEMO-1','household_id':'H-1'},{'person_id':'DEMO-1','household_id':'H-2'}]);self.assertEqual(r['unique_people'],1);self.assertEqual(r['conflicts'],['DEMO-1'])
if __name__=='__main__':unittest.main()
