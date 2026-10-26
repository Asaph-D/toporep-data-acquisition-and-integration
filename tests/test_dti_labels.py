from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]/"scripts/build_datasets/build_bindingdb_entities_labels.py"
spec=importlib.util.spec_from_file_location("dti_labels",MODULE)
module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)


class DTILabelTests(unittest.TestCase):
    def test_exact_boundary_is_positive(self): self.assertEqual(module.measurement_label("=",6.0,6.0),"positive")
    def test_less_than_is_lower_concentration(self): self.assertEqual(module.measurement_label("<",6.0,6.0),"positive")
    def test_greater_than_boundary_is_negative(self): self.assertEqual(module.measurement_label(">",6.0,6.0),"negative_measured")
    def test_censoring_can_be_ambiguous(self):
        self.assertEqual(module.measurement_label("<",5.0,6.0),"ambiguous")
        self.assertEqual(module.measurement_label(">",7.0,6.0),"ambiguous")


if __name__=="__main__": unittest.main()
