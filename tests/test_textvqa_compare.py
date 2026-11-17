"""CPU-only checks for the paired TextVQA runner (no model or dataset download)."""

import csv
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import textvqa_compare as benchmark


class TextVQATest(unittest.TestCase):
    def test_fixed_sample_is_reproducible_and_nested_in_full(self):
        annotations = {"data": [
            {"question_id": i, "image_id": str(i // 2), "answers": ["x"] * 10}
            for i in range(5000)
        ]}
        first = benchmark.choose_questions(annotations, 200)
        second = benchmark.choose_questions(annotations, 200)
        full = benchmark.choose_questions(annotations, 5000)
        self.assertEqual([x["question_id"] for x in first], [x["question_id"] for x in second])
        self.assertEqual(len(full), 5000)
        self.assertEqual(len(first), 200)
        self.assertTrue({x["question_id"] for x in first}.issubset(
            {x["question_id"] for x in full}))

    def test_resume_preserves_last_success_not_error(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "base_raw.csv"
            row = dict.fromkeys(benchmark.RAW_COLUMNS, "")
            row.update(question_id="42", status="completed", prediction="orange")
            benchmark.append_result(filename, row)
            row.update(question_id="43", status="error", prediction="")
            benchmark.append_result(filename, row)
            row.update(question_id="42", status="completed", prediction="blue")
            benchmark.append_result(filename, row)
            saved = benchmark.read_successes(filename)
            self.assertEqual(saved["42"]["prediction"], "blue")
            self.assertNotIn("43", saved)
            with filename.open(newline="") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), 3)

    def test_paired_cluster_statistic(self):
        base = np.array([0, 0.5, 1, 0.5])
        tuned = np.array([1, 1, 1, 0])
        result = benchmark.paired_cluster_test(
            base, tuned, ["a", "a", "b", "c"],
            bootstrap_iterations=200, permutations=1000,
        )
        self.assertAlmostEqual(result["delta_percentage_points"], 25)
        self.assertEqual(result["distinct_image_clusters"], 3)
        self.assertEqual(result["improved_questions"], 2)
        self.assertEqual(result["worse_questions"], 1)
        self.assertEqual(result["tied_questions"], 1)
        self.assertGreaterEqual(result["paired_image_cluster_signflip_two_sided_p"], 0)
        self.assertLessEqual(result["paired_image_cluster_signflip_two_sided_p"], 1)

    def test_all_ties_are_not_significant(self):
        arr = np.array([0.0, 1.0, 0.5])
        result = benchmark.paired_cluster_test(
            arr, arr, ["a", "a", "b"], bootstrap_iterations=100, permutations=100
        )
        self.assertEqual(result["delta_percentage_points"], 0)
        self.assertEqual(result["paired_image_cluster_signflip_two_sided_p"], 1)
        self.assertEqual(result["delta_95pct_cluster_bootstrap_ci_pp"], [0, 0])


if __name__ == "__main__":
    unittest.main()
