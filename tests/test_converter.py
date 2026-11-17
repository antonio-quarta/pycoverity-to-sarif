import json
import tempfile
import unittest
from pathlib import Path

from coverity_sarif import convert_to_sarif, impact_to_level


class ConverterTests(unittest.TestCase):
    def test_impact_to_level_maps_coverity_severity(self):
        self.assertEqual(impact_to_level("High"), "error")
        self.assertEqual(impact_to_level("Medium"), "warning")
        self.assertEqual(impact_to_level("Low"), "note")
        self.assertEqual(impact_to_level("Unknown"), "none")

    def test_convert_to_sarif_writes_rule_result_and_location(self):
        issue = {
            "checkerName": "RESOURCE_LEAK",
            "checkerProperties": {
                "impact": "High",
                "cweCategory": 401,
                "subcategoryShortDescription": "Resource leak",
                "subcategoryLongDescription": "Allocated memory is not released",
                "category": "Resource",
            },
            "events": [
                {
                    "main": True,
                    "strippedFilePathname": "src/main file.c",
                    "lineNumber": "42",
                    "eventDescription": "Possible resource leak",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "coverity.json"
            output_file = Path(temp_dir) / "results.sarif"
            input_file.write_text(json.dumps({"issues": [issue]}), encoding="utf-8")

            sarif = convert_to_sarif(input_file, output_file)

            self.assertEqual(sarif["version"], "2.1.0")
            run = sarif["runs"][0]
            driver = run["tool"]["driver"]
            self.assertEqual(len(driver["rules"]), 1)
            self.assertEqual(driver["rules"][0]["id"], "401")
            self.assertEqual(driver["rules"][0]["defaultConfiguration"]["level"], "error")

            result = run["results"][0]
            self.assertEqual(result["ruleId"], "401")
            self.assertEqual(result["level"], "error")
            self.assertEqual(result["message"]["text"], "Possible resource leak")
            physical_location = result["locations"][0]["physicalLocation"]
            self.assertEqual(physical_location["artifactLocation"]["uri"], "src/main%20file.c")
            self.assertEqual(physical_location["region"]["startLine"], 42)
            self.assertEqual(json.loads(output_file.read_text(encoding="utf-8")), sarif)

    def test_convert_to_sarif_rejects_missing_issues_array(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "coverity.json"
            output_file = Path(temp_dir) / "results.sarif"
            input_file.write_text(json.dumps({"issues": None}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "issues array"):
                convert_to_sarif(input_file, output_file)


if __name__ == "__main__":
    unittest.main()