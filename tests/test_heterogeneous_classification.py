from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]/"scripts/normalize/classify_heterogeneous_sources.py"
spec=importlib.util.spec_from_file_location("classify",MODULE)
classify=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(classify)
MATERIALIZER=Path(__file__).resolve().parents[1]/"scripts/normalize/materialize_expression_atlas.py"
materialize_spec=importlib.util.spec_from_file_location("materialize_atlas",MATERIALIZER)
materialize_atlas=importlib.util.module_from_spec(materialize_spec); assert materialize_spec.loader; materialize_spec.loader.exec_module(materialize_atlas)


class ClassificationTests(unittest.TestCase):
    def test_atlas_accession(self):
        self.assertEqual(classify.atlas_accession("_dl_E-MTAB-2706-tpms.tsv"),"E-MTAB-2706")

    def test_geo_unknown_unit_is_blocked(self):
        text=MODULE.read_text(encoding="utf-8")
        self.assertIn("blocked_unit_and_platform_annotation",text)
        self.assertNotIn('"unit":"tpm","technology":"unresolved"',text)

    def test_geo_rma_is_explicit_but_still_needs_probe_mapping(self):
        result=classify.geo_processing_semantics("Normalized with robust multi-array average (RMA).")
        self.assertEqual(result["unit"],"log2_rma_expression")
        self.assertEqual(result["technology"],"microarray")

    def test_geo_quantile_alone_does_not_prove_scale(self):
        result=classify.geo_processing_semantics("Data were quantile normalized.")
        self.assertEqual(result["unit"],"unknown")

    def test_atlas_five_number_summary_is_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"atlas.tsv"
            path.write_text("GeneID\tGene Name\tg1\nENSG1\tA\t1,2,3,4,5\n",encoding="utf-8")
            probe=classify.atlas_cell_probe(path)
        self.assertEqual(probe["cell_encoding"],"five_number_summary")
        self.assertEqual(probe["packed_widths"],"5")

    def test_atlas_summary_median(self):
        self.assertEqual(materialize_atlas.decode_summary("1,2,3,4,5")[2],3.0)
        with self.assertRaises(ValueError):
            materialize_atlas.decode_summary("5,4,3,2,1")


if __name__=="__main__": unittest.main()
