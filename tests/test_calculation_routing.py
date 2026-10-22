"""Dated country recommendations must not become permissions or silent switches."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/meter"
SCRIPT = SKILL / "scripts/calculation-routing.py"
spec = importlib.util.spec_from_file_location("calculation_routing", SCRIPT)
routing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routing)


class CalculationRoutingTests(unittest.TestCase):
    def test_all_24_countries_have_exact_verified_method_sets_and_defaults(self):
        matrix = json.loads((SKILL / "references/calculation-coverage.json").read_text())
        legacy = set("AE AZ BH BY DE EG FR GB GE IQ JO KG KW KZ OM PK PL QA SA TJ TR UZ".split())
        modern = {"AE", "IT", "KZ", "MA", "QA", "UZ"}
        codes = [country["code"] for country in matrix["countries"]]
        self.assertEqual(len(codes), 24)
        self.assertEqual(set(codes), legacy | modern)
        self.assertEqual(len(set(codes)), len(codes))
        self.assertEqual(matrix["verified_tools"], routing.METHOD_TOOLS)
        self.assertEqual(matrix["verified_at"], "2026-10-22")
        self.assertEqual(matrix["period"], {"from": "2026-09-01", "to": "2026-09-30"})
        for code in codes:
            result = routing.recommend(code)
            self.assertEqual(set(result["verified_methods"]),
                             ({"legacy"} if code in legacy else set()) | ({"new"} if code in modern else set()))
            self.assertEqual(result["selected_tool"], "meter_ots_reach" if code in legacy else "meter_new_ots_reach")
            self.assertTrue(result["selected_method_verified"])
            self.assertFalse(result["legacy_fallback_allowed"])

    def test_italy_and_morocco_default_to_new_with_sourced_city_examples(self):
        for code, city in (("IT", "Roma"), ("MA", "Casablanca")):
            result = routing.recommend(code)
            self.assertEqual(result["selected_tool"], "meter_new_ots_reach")
            self.assertEqual(result["sample_city"], city)
            self.assertNotIn("city", result)
            self.assertIn("not a substituted input", result["city_policy"])

    def test_azerbaijan_defaults_to_legacy_and_both_method_countries_keep_legacy(self):
        self.assertEqual(routing.recommend("AZ")["sample_city"], "Baku")
        for code in ("AZ", "UZ", "KZ", "AE", "QA"):
            self.assertEqual(routing.recommend(code)["selected_tool"], "meter_ots_reach")
        for code in ("UZ", "KZ", "AE", "QA"):
            result = routing.recommend(code, "new")
            self.assertEqual(result["selected_tool"], "meter_new_ots_reach")
            self.assertTrue(result["selected_method_verified"])

    def test_explicit_unverified_method_is_preserved_not_silently_replaced(self):
        for code, method in (("IT", "legacy"), ("MA", "legacy"), ("AZ", "new")):
            result = routing.recommend(code, method)
            self.assertEqual(result["selected_tool"], routing.METHOD_TOOLS[method])
            self.assertEqual(result["selection"], "explicit_method")
            self.assertFalse(result["selected_method_verified"])

    def test_new_only_countries_never_get_automatic_legacy_recovery(self):
        for code in ("IT", "MA"):
            result = routing.recommend(code, "new", new_ots_no_data=True, allow_legacy_fallback=True)
            self.assertFalse(result["legacy_fallback_allowed"])
            self.assertIsNone(result["fallback_tool"])
            self.assertEqual(result["selected_tool"], "meter_new_ots_reach")

    def test_legacy_recovery_requires_both_no_data_and_task_permission(self):
        for code in ("UZ", "AZ"):
            self.assertFalse(routing.recommend(code, "new", new_ots_no_data=True)["legacy_fallback_allowed"])
            self.assertFalse(routing.recommend(code, "new", allow_legacy_fallback=True)["legacy_fallback_allowed"])
            result = routing.recommend(code, "new", new_ots_no_data=True, allow_legacy_fallback=True)
            self.assertTrue(result["legacy_fallback_allowed"])
            self.assertEqual(result["fallback_tool"], "meter_ots_reach")
            self.assertTrue(result["fallback_method_verified"])
            self.assertEqual(result["selected_tool"], "meter_new_ots_reach")

    def test_unknown_and_vatican_remain_unverified_without_blocking_explicit_calls(self):
        for code in ("US", "VA"):
            default = routing.recommend(code)
            self.assertEqual(default["basis"], "unverified_country")
            self.assertEqual(default["verified_methods"], [])
            self.assertIsNone(default["sample_city"])
            self.assertFalse(default["selected_method_verified"])
            explicit = routing.recommend(code, "new", new_ots_no_data=True, allow_legacy_fallback=True)
            self.assertEqual(explicit["selected_tool"], "meter_new_ots_reach")
            self.assertTrue(explicit["legacy_fallback_allowed"])
            self.assertFalse(explicit["fallback_method_verified"])

    def test_generated_codex_resources_match_source_and_version(self):
        for name in ("references/calculation-coverage.json", "references/country-coverage.md", "scripts/calculation-routing.py"):
            self.assertEqual((SKILL / name).read_bytes(), (ROOT / "plugins/meter/skills/meter" / name).read_bytes())
        source = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        generated = json.loads((ROOT / "plugins/meter/.codex-plugin/plugin.json").read_text())
        resource = json.loads((SKILL / "references/package-version.json").read_text())
        self.assertEqual(source["version"], generated["version"])
        self.assertEqual(source["version"], resource["version"])

    def test_cli_is_read_only_and_rejects_invalid_input_without_echoing_it(self):
        before = (SKILL / "references/calculation-coverage.json").read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "it"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["selected_tool"], "meter_new_ots_reach")
        self.assertEqual((SKILL / "references/calculation-coverage.json").read_bytes(), before)
        result = subprocess.run([sys.executable, str(SCRIPT), "private-token-input"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("private-token-input", result.stdout + result.stderr)
        for bad in (None, "", "ITA", "I T", 24):
            with self.assertRaises(ValueError):
                routing.recommend(bad)


if __name__ == "__main__":
    unittest.main()
