from __future__ import annotations

import unittest
from pathlib import Path


class GeneRegistryTests(unittest.TestCase):
    def test_script_does_not_call_external_service(self):
        path=Path(__file__).resolve().parents[1]/"scripts/normalize/build_gene_registry.py"
        text=path.read_text(encoding="utf-8")
        self.assertNotIn("requests.",text)
        self.assertIn("gtex_crosswalk",text)


if __name__=="__main__": unittest.main()
