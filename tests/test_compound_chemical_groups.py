from scripts.build_datasets.build_compound_chemical_groups import describe
import unittest
class ChemicalGroupTests(unittest.TestCase):
 def test_benzene_has_expected_murcko_scaffold(self):
  r=describe(('UHOVQNZJYSORNB-UHFFFAOYSA-N','c1ccccc1'));self.assertEqual(r[2],'c1ccccc1');self.assertEqual(r[8],'generated')
 def test_ecfp4_is_deterministic(self):
  a=describe(('x','CCO'));b=describe(('x','CCO'));self.assertEqual(a[6],b[6]);self.assertEqual(len(a[5]),256)
 def test_acyclic_scaffold_is_explicitly_empty(self): self.assertEqual(describe(('x','CCO'))[2],'')
if __name__=='__main__':unittest.main()
