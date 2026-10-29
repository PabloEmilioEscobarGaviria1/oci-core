import os
import tempfile
import unittest
from unittest.mock import patch

import oci


class OCITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = os.getcwd()
        os.chdir(self.tmp.name)
        oci.init_db()

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def test_add_knowledge(self):
        args = type("Args", (), {"kind": "hypothesis", "claim": "Test claim",
                                 "source": "Test source", "confidence": 0.7})()
        oci.add_knowledge(args)
        with oci.connect() as db:
            row = db.execute("SELECT claim, confidence FROM knowledge").fetchone()
        self.assertEqual(row["claim"], "Test claim")
        self.assertAlmostEqual(row["confidence"], 0.7)

    def test_forecast_and_score(self):
        args = type("Args", (), {"question": "Will test pass?", "probability": 0.8,
                                 "target_date": "2030-01-01", "assumptions": "Test only"})()
        oci.add_forecast(args)
        with patch("builtins.print") as mocked:
            oci.score_forecast(type("Args", (), {"id": 1, "outcome": 1})())
        self.assertTrue(mocked.called)
        with oci.connect() as db:
            row = db.execute("SELECT outcome FROM forecasts WHERE id = 1").fetchone()
        self.assertEqual(row["outcome"], 1)

    def test_probability_bounds_enforced_by_sql(self):
        with self.assertRaises(Exception):
            with oci.connect() as db:
                db.execute(
                    "INSERT INTO forecasts(question, probability, target_date, assumptions, created_at) VALUES (?, ?, ?, ?, ?)",
                    ("bad", 2.0, "2030-01-01", "", "now"))


if __name__ == "__main__":
    unittest.main()
