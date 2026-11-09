# METER for Claude, ChatGPT and Codex

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/meter-logo-white.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/meter-logo.svg">
  <img src="assets/meter-logo.svg" alt="METER" width="340" height="64">
</picture>

Plan outdoor advertising with METER in Claude Code, Cowork, ChatGPT and Codex. Discover OOH/DOOH inventory, calculate projected audience Universe, OTS and Reach, inspect audience profiles, and prepare address-program spreadsheets from validated results.

Requires a connected existing METER account with access to the requested tools and country. Installing the plugin grants no additional data access. It provides analytical planning, with no subscription sales, upgrades, checkout, advertising booking, payments or advertisements.

## Install in Claude Code

```text
/plugin marketplace add Meter-plugin-ai/meter-ai-plugin
/plugin install meter@meter-plugins
```

Restart Claude Code or run `/reload-plugins`. Open `/mcp`, select the METER server and complete OAuth sign-in if requested. Invoke `/meter:meter` or describe the planning task naturally. If METER is already connected separately, use one connection for the task to avoid ambiguous duplicate tools.

This is METER's own marketplace. Listing in Anthropic's official directory is subject to review; this repository does not claim approval or Anthropic verification.

## Codex and ChatGPT

The OpenAI package is generated at `plugins/meter` from the same reviewed skills and assets. See [OpenAI installation and usage](docs/openai-package.md) and [OpenAI submission preparation](docs/openai-submission.md). Claude directory approval and OpenAI directory approval are separate; neither is claimed by this repository.

## Cowork

Use the plugin's released ZIP with Cowork's plugin upload flow, or install from a marketplace supported by your workspace. Complete MCP sign-in when prompted. Availability and installation controls depend on the client and organization settings.

## Try it

- “Find up to three inventory records in Ташкент. Show their METER IDs, addresses and actual OOH/DOOH classification.”
- “Calculate the audience Universe in Ташкент for ages 20–45, all genders and income abc.”
- “Using those exact surface IDs, calculate legacy OTS and Reach for the same audience and period. Label modeled contacts separately from unique audience.”
- “Create an XLSX address program from those results, with campaign totals, an inventory table and a numbered city map.”

Use a city and period covered by your account. Spreadsheet creation depends on file-authoring tools available in your client; this package does not install a spreadsheet runtime.

Client-ready address programs include a city map whose point numbers match the inventory table, unless a table-only export was requested. Missing coordinates, a basemap or authoring capabilities must be disclosed as an incomplete export. See the [export contract](skills/meter/references/excel-export.md).

## Calculation behavior

There are 16 METER tools. The [dated country guide](skills/meter/references/country-coverage.md) contains verified combined OTS/Reach examples in **24 countries**: legacy in 22 and New OTS in 6, with four countries represented in both. Without an explicit method, Italy and Morocco use New OTS; the other 22 use legacy. An explicit methodology is preserved. This is sampled API evidence from 22 October 2026 for September 2026, not live coverage or a guarantee for every city, surface, audience, period or other endpoint. Access still depends on the account and country subscription; other countries remain unverified rather than prohibited.

A `no_data` result means data is unavailable for that request, not zero. When permitted by the brief and country guidance, the skill tries equivalent legacy once and names the method used. Italy and Morocco have no automatic legacy fallback because their audited legacy results were zero. HTTP 200 with zero metrics does not establish working calculation coverage. An optional offline [routing helper](skills/meter/references/country-coverage.md#optional-local-routing-helper) makes the same recommendation without calling METER or granting access.

Campaign Reach optimization compares whole-program calculations under a persisted brief. The optional local ledger checker detects changed requests and selects the best recorded feasible result; it is not a hosted optimizer or proof of global optimality. See [campaign planning](skills/meter/references/campaign-planning.md).

Program preparation also checks inventory status and conflicting static/digital metadata before selection. An optional local helper calculates a sourced or explicitly assumed budget by component and range; missing prices remain unavailable, and placement availability remains unconfirmed. See [inventory and budget](skills/meter/references/inventory-budget.md).

The local [XLSX builder](skills/meter/references/export-builder.md) binds the final campaign IDs to the table, editable budget and embedded numbered map. It uses available client authoring tools and cached attributed tiles, adds readable detail panels for dense points and checks the saved workbook. Missing map inputs or prices remain explicit partial results; it fetches no basemap and installs no renderer.

Historical small-scenario API measurements were roughly <1 second for simple queries, 1–3 seconds for selection/legacy calculations, 6–8 seconds for New OTS, and 12–15 seconds for some breakdowns. These exclude OAuth and remote MCP overhead and are not an SLA. See [method timings and limitations](skills/meter/references/performance.md).

## Troubleshooting

First identify the requested connection and the failing layer. A different METER integration's result does not validate this package, a website-root 404 does not test the MCP endpoint, and a successful status/docs probe does not validate campaign calculations. The [diagnostics guide](skills/meter/references/diagnostics.md) distinguishes these cases and provides an optional read-only local classifier. Its package version resource identifies those files; installed skills, MCP server and calculation service versions are separate observations.

- **Client authentication / MCP endpoint HTTP 401:** reconnect METER in the client’s connection settings (`/mcp` in Claude Code) and complete OAuth. A 401 inside a tool's upstream API result does not by itself establish a client login failure.
- **Existing access required:** explain that the capability is unavailable under the signed-in account’s current entitlements. Check existing access with the account administrator; do not start a subscription, upgrade or payment flow. Reinstalling or repeated sign-in does not change entitlements.
- **Wallet verification unavailable:** try again shortly; an outage does not grant temporary data access.
- **Access denied / invalid country scope:** ask your METER administrator to check your existing account's tool and country permissions. Installing again does not grant permissions.
- **New OTS no_data:** consult the country guide. Use equivalent legacy once if the task permits; IT/MA retain the unavailable result without automatic legacy fallback. Do not invent metrics.
- **Timeout:** narrow the inventory/period or try later. Avoid repeating an unchanged request automatically.
- **Incomplete inventory:** finish pagination or narrow the query before producing a final program.

## Data and security

The package contains instructions, branding, one HTTPS MCP configuration and optional local helpers for country routing, campaign validation, budgets, XLSX exports and diagnostics. Helpers use no network or credentials; export helpers write only explicitly named new local outputs. The package installs no executable hooks, local MCP server or database connector. Calculation inputs and results pass between your assistant client and METER. Authentication is handled through OAuth; never put passwords or tokens in prompts or GitHub issues. See [data handling](docs/data-handling.md) and [security reporting](SECURITY.md).

## Development and review

```sh
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
python3 scripts/validate-package.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

See [reviewer scenarios](docs/reviewer-guide.md) and [verification evidence](docs/verification.md). This repository contains only the client plugin; hosted METER services and datasets are separate.

## License

The client plugin in this repository is licensed under [GNU Affero General Public License version 3 only](LICENSE) (`AGPL-3.0-only`). Hosted METER services and datasets are separate from this repository; using them requires an existing account with the applicable access and service terms.
