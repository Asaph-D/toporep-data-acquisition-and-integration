from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]/"scripts/normalize/build_structured_axes.py"
spec=importlib.util.spec_from_file_location("build_structured_axes",MODULE)
axes=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(axes)


class StructuredAxesTests(unittest.TestCase):
    def test_ensembl_version_is_removed(self):
        self.assertEqual(axes.ensembl("ENSG000001234.12"),"ENSG000001234")
        self.assertIsNone(axes.ensembl("TP53"))

    def test_tcga_contract_does_not_claim_raw_tpm(self):
        text=MODULE.read_text(encoding="utf-8")
        self.assertIn("log2_tpm_plus_0_001",text)

    def test_disk_guard_is_defined(self):
        self.assertEqual(axes.MIN_FREE,80_000_000_000)


if __name__=="__main__": unittest.main()
