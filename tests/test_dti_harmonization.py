from __future__ import annotations
import importlib.util
import math
import unittest
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]/"scripts/build_datasets/harmonize_dti_assays.py"
spec=importlib.util.spec_from_file_location("harmonize_dti",MODULE)
module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)

class HarmonizationTests(unittest.TestCase):
    def test_activity_types_are_case_insensitive(self):
        self.assertEqual(module.normalize_type("IC50"),"ic50")
        self.assertEqual(module.normalize_type("Ki"),"ki")
        self.assertIsNone(module.normalize_type("Potency"))
    def test_relations_are_strict(self):
        self.assertEqual(module.normalize_relation("<="),"<=")
        self.assertIsNone(module.normalize_relation("~"))
        self.assertIsNone(module.normalize_relation("\\N"))
    def test_unit_conversion_and_pactivity(self):
        molar=module.to_molar(100,"nM")
        self.assertAlmostEqual(molar,1e-7)
        self.assertAlmostEqual(-math.log10(molar),7.0)
        self.assertIsNone(module.to_molar(10,"%"))
        self.assertIsNone(module.to_molar(0,"nM"))

if __name__=="__main__": unittest.main()
