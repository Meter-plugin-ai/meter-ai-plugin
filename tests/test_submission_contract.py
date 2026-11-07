"""Regression guards for rejected commerce and conflicting review instructions."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("runbook", ROOT / "scripts/build-reviewer-runbook.py")
runbook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runbook)


class SubmissionContractTests(unittest.TestCase):
    def test_distributed_content_has_no_subscription_sales_destination_or_price(self):
        # The actual generated distribution is checked, including README and helpers.
        for path in (ROOT / "plugins/meter").rglob("*"):
            if path.is_file() and path.suffix in (".md", ".json", ".py", ".mjs"):
                value = path.read_text().lower()
                self.assertNotIn("window.wallet.meter.ad", value, str(path))
                self.assertNotIn("$599", value, str(path))
                self.assertNotIn("price_usd_per_user_country_month", value, str(path))
                self.assertNotIn("manage_url", value, str(path))

    def test_review_prompts_and_expectations_have_one_source(self):
        source = json.loads((ROOT / "chatgpt-app-submission.json").read_text())
        self.assertEqual((ROOT / "docs/reviewer-test-runbook.md").read_text(), runbook.render(source))
        guide = (ROOT / "docs/reviewer-guide.md").read_text()
        self.assertNotIn("## Positive cases", guide)
        self.assertIn("reviewer-test-runbook.md", guide)
        # The no_data branch must not turn successful New OTS into a required Legacy call.
        new_ots = source["test_cases"][3]
        self.assertNotIn("meter-meter_ots_reach", new_ots["tools_triggered"].split(", "))
        self.assertIn("Only on explicit no_data", new_ots["expected_output"])

    def test_commerce_declaration_and_negative_case_cover_existing_access_only(self):
        manifest = json.loads((ROOT / "plugins/meter/.codex-plugin/plugin.json").read_text())
        review = manifest["extensions"]["com.openai"]["review"]
        self.assertIs(review["commerce"], False)
        self.assertIn("Existing entitlements are enforced", review["commerce_description"])
        self.assertIn("upgrade", review["test_cases"]["negative"][0]["prompt"])
        self.assertIn("checkout/upgrade links", review["test_cases"]["negative"][0]["expected_behavior"])

    def test_campaign_cases_explicitly_lock_comparable_assumptions(self):
        source = json.loads((ROOT / "chatgpt-app-submission.json").read_text())
        for case in source["test_cases"][2:]:
            for control in ("chrono=10", "blockSize=0", "outputsInBlock=1", "impressions=[-1]", "byDays=false", "normalization=0.3"):
                self.assertIn(control, case["user_prompt"])
        self.assertIn("no reporting-period input", source["test_cases"][1]["expected_output"])
