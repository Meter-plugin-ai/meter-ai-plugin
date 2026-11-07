#!/usr/bin/env python3
"""Generate exact reviewer cases from the submission source, never test evidence."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render(submission):
    lines = [
        "# Reviewer test and demo runbook", "",
        "Generated from `chatgpt-app-submission.json`; update that source, then run `python3 scripts/build-reviewer-runbook.py`. These instructions are not evidence of passed tests.", "",
        "## Setup and pass criteria", "",
        "Use the exact submitted plugin version and public OAuth MCP endpoint with the dedicated reviewer account and its existing Uzbekistan access. Credentials belong only in the private portal field. Do not use the owner's existing login as proof of reviewer access. Do not store credentials, tokens or raw authorization exchanges in evidence or recordings.", "",
        "Replay all eight cases in fresh ChatGPT web and mobile sessions, as required by the review. Record client/version, plugin version, account alias, actual arguments, returned method/units, preserved warnings and pass/fail for each surface. Direct MCP probes, responsive desktop layouts and unit tests do not establish mobile-client replay. A status success is not a calculation success; access/service errors or all-zero calculations do not pass positive cases.", "",
        "Use the real returned IDs, not a hard-coded expected roster. The first sample can include a dismantled record; retain that warning in later results. These are analytics records, not bookable inventory. Client prefixes may vary; expected tool names identify the method rather than an exact call count. A status probe is optional once reachability has already been checked.", "",
        "Universe has no campaign-period parameter. Campaign tests explicitly supply inclusive dates, audience and all planning assumptions; keep them identical between comparable totals and per-surface calls. For legacy, use nested audience and normalizeCoeff; for New OTS use top-level demographic fields and normalize_coeff. Never infer filter loss from an empty response echo alone.", "",
    ]
    for key, prefix, title in (("test_cases", "P", "Positive cases"), ("negative_test_cases", "N", "Negative cases")):
        lines += ["## " + title, ""]
        for n, case in enumerate(submission[key], 1):
            lines += [f"### {prefix}{n}: {case['description']}", "", "**Prompt**", "", "> " + case["user_prompt"], "", "**Expected result**", "", case["expected_output"], "", "**Expected tools:** " + (case.get("tools_triggered") or "No operational tool; an optional reachability probe is acceptable.") + ".", ""]
    lines += [
        "## Additional regression checks", "",
        "Verify an already signed-in account without the required existing access: tool discovery must not grant extra tools; status/denial must explain unavailable access without prices, subscription plans, transactional links, purchases or upgrades. Authorization must fail closed. Do not change account entitlements for this check. Test the denied branch with controlled local fixtures when a suitable reviewer account is not available, and label it as local evidence.", "",
        "Test sensitivity to dates and audience with the same IDs and method. Retain submitted arguments as evidence; do not compare different methods as proof of date filtering. A covered New OTS result requires no legacy call; explicit no_data permits only the requested conditional fallback, while arbitrary errors do not.", "",
        "## Demo and reviewer notes", "",
        "Record the actual submitted version in ChatGPT Developer Mode using reviewer-authorized data. Run P1–P5 and N1–N3 with tool inputs/results visible, omit credential entry, and keep source warnings and calculation assumptions visible. Show only analytical functionality and existing-account sign-in, with no purchase/upgrade workflow. Use a reviewer-accessible video URL and verify playback without the owner's session. An older recording must be checked for behavior and version drift; it is not evidence of a corrected live replay.", "",
        "## Release gate", "",
        "Before resubmitting, verify the exact ZIP, source commit, dedicated reviewer OAuth/access, complete web/mobile replay, deployed neutral MCP instructions and denied responses, metadata/skill checks and MCP scan. Preserve all failed or unperformed checks in a separate readiness report. Package validation or an available submission button alone does not establish readiness. Submission and publication are separate actions.", "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(json.loads((ROOT / "chatgpt-app-submission.json").read_text()))
    target = ROOT / "docs/reviewer-test-runbook.md"
    if args.check:
        if target.read_text() != expected:
            raise SystemExit("Reviewer runbook differs from canonical submission cases")
        print("PASS: reviewer runbook matches all eight canonical cases")
    else:
        target.write_text(expected)
