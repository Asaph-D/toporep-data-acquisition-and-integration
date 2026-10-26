from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "audit" / "scan_inputs.py"
spec = importlib.util.spec_from_file_location("scan_inputs", MODULE)
scan_inputs = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(scan_inputs)


class ScanInputsTests(unittest.TestCase):
    def test_known_formats(self) -> None:
        self.assertEqual(scan_inputs.file_format(Path("x.gct.gz")), ("gct", "gzip"))
        self.assertEqual(scan_inputs.file_format(Path("x.gctx.gz")), ("gctx", "gzip"))
        self.assertEqual(scan_inputs.file_format(Path("x.tar.gz")), ("postgres_dump", "gzip"))

    def test_specs_keep_units_separate(self) -> None:
        units = {unit for _, role, unit in scan_inputs.SPECS["expression_atlas"] if role == "matrix"}
        self.assertEqual(units, {"tpm", "fpkm", "analytics"})

    def test_no_training_or_split_output(self) -> None:
        text = MODULE.read_text(encoding="utf-8")
        self.assertNotIn('ROOT / "training"', text)
        self.assertNotIn("splits_", text)


if __name__ == "__main__":
    unittest.main()

