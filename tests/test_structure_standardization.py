import unittest

try:
    from scripts.build_datasets.standardize_structures_rdkit import standardize
except (ImportError, OSError):
    standardize = None


@unittest.skipIf(standardize is None, "RDKit is tested in the pinned Linux container")
class StructureStandardizationTests(unittest.TestCase):
    def test_salt_is_removed_and_identity_is_stable(self):
        result = standardize(["x", "", "CC(=O)[O-].[Na+]"])
        self.assertEqual(result[6], "standardized")
        self.assertEqual(result[3], "CC(=O)O")
        self.assertEqual(result[5], "QTBSBXVTEAMEQO-UHFFFAOYSA-N")
        self.assertEqual(result[8], "1")

    def test_invalid_smiles_is_explicitly_rejected(self):
        result = standardize(["x", "", "not-a-smiles"])
        self.assertEqual(result[6], "rejected")
        self.assertEqual(result[7], "smiles_parse_failed")


if __name__ == "__main__":
    unittest.main()
