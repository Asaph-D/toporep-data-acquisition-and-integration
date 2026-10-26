from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "validation" / "validate_input_manifest.py"
spec = importlib.util.spec_from_file_location("validate_input_manifest", MODULE)
validator = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(validator)


class ValidateManifestTests(unittest.TestCase):
    def test_current_manifest_is_structurally_valid(self) -> None:
        manifest = Path(__file__).resolve().parents[1] / "normalized" / "manifests" / "input_manifest.csv"
        self.assertEqual(validator.validate(manifest), [])

    def test_duplicate_is_rejected(self) -> None:
        header = "source,source_release,relative_path,role,format,compression,bytes,sha256,rows,columns,unit,status,reason\n"
        row = "x,v,data/x/missing,matrix,csv,,0,,,,,blocked,required_pattern_not_found\n"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "manifest.csv"
            path.write_text(header + row + row, encoding="utf-8")
            errors = validator.validate(path)
        self.assertTrue(any("duplicate_path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

