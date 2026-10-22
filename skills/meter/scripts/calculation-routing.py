#!/usr/bin/env python3
"""Recommend a campaign method from dated examples; no service access or writes."""
import argparse
import json
from pathlib import Path
import re


MATRIX = Path(__file__).resolve().parents[1] / "references/calculation-coverage.json"
METHOD_TOOLS = {"legacy": "meter_ots_reach", "new": "meter_new_ots_reach"}


def recommend(country_code, requested_method=None, *, new_ots_no_data=False,
              allow_legacy_fallback=False):
    """Keep explicit methods and distinguish a recommendation from verification.

    The fallback flag represents the task's permission to change methodology,
    not account authorization. Actual service permissions still apply.
    """
    if not isinstance(country_code, str) or not re.fullmatch(r"[A-Za-z]{2}", country_code):
        raise ValueError("country_code must be an ISO alpha-2 code")
    if requested_method not in (None, "legacy", "new"):
        raise ValueError("requested_method must be legacy or new")
    if type(new_ots_no_data) is not bool or type(allow_legacy_fallback) is not bool:
        raise ValueError("recovery flags must be booleans")
    code = country_code.upper()
    matrix = json.loads(MATRIX.read_text())
    entry = next((country for country in matrix["countries"] if country["code"] == code), None)
    verified = entry["methods"] if entry else []
    default = entry["default_method"] if entry else "legacy"
    selected = requested_method or default
    # A country absent from the dated table is unverified, not forbidden. A
    # permitted legacy probe there retains that unverified status.
    audited_legacy_zero = entry is not None and "legacy" not in verified
    fallback = (new_ots_no_data and selected == "new" and allow_legacy_fallback
                and not audited_legacy_zero)
    return {
        "country_code": code,
        "basis": "dated_verified_examples" if entry else "unverified_country",
        "verified_at": matrix["verified_at"],
        "verified_period": matrix["period"],
        "verified_methods": list(verified),
        "default_tool": METHOD_TOOLS[default],
        "selected_tool": METHOD_TOOLS[selected],
        "selection": "explicit_method" if requested_method else "reference_default",
        "selected_method_verified": selected in verified,
        "sample_city": entry["verified_city"] if entry else None,
        "legacy_fallback_allowed": bool(fallback),
        "fallback_tool": METHOD_TOOLS["legacy"] if fallback else None,
        "fallback_method_verified": "legacy" in verified if fallback else None,
        "scope": matrix["scope"],
        "city_policy": "Use the actual inventory city; sample_city is an example, not a substituted input.",
        "access_policy": "Recommendations grant no account or country access.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("country_code", help="ISO alpha-2 country code")
    parser.add_argument("--method", choices=METHOD_TOOLS, help="Preserve an explicitly requested method")
    parser.add_argument("--new-ots-no-data", action="store_true", help="The retained New OTS response explicitly returned no_data")
    parser.add_argument("--allow-legacy-fallback", action="store_true", help="The task permits changing to legacy")
    args = parser.parse_args()
    try:
        result = recommend(args.country_code, args.method,
                           new_ots_no_data=args.new_ots_no_data,
                           allow_legacy_fallback=args.allow_legacy_fallback)
    except (ValueError, OSError, KeyError):
        parser.exit(2, "Invalid routing input or unavailable coverage reference.\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
