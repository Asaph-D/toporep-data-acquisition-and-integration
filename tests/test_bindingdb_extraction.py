from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]/"scripts/build_datasets/extract_bindingdb_assays.py"
spec=importlib.util.spec_from_file_location("bindingdb_extract",MODULE)
module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)


class BindingDBExtractionTests(unittest.TestCase):
    def test_parse_exact_nm(self):
        relation,value,molar,pactivity=module.parse_nm("100")
        self.assertEqual(relation,"="); self.assertEqual(value,100.0); self.assertAlmostEqual(molar,1e-7); self.assertAlmostEqual(pactivity,7.0)

    def test_parse_censored_nm(self):
        self.assertEqual(module.parse_nm(">= 10000")[0],">=")

    def test_reject_range_and_zero(self):
        self.assertIsNone(module.parse_nm("1-10")); self.assertIsNone(module.parse_nm("0"))


if __name__=="__main__": unittest.main()
