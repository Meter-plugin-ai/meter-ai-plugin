# Reviewer guide

## Package

Name: METER. Publisher: METER / GEOMOTIVE. Purpose: OOH/DOOH inventory discovery and projected audience calculations. Website: https://meter.ad. Source: https://github.com/Meter-plugin-ai/meter-ai-plugin. MCP: https://mcp.meter.ad/meter/mcp (Streamable HTTP, OAuth).

Install following the README and authenticate in the client. A METER account with permission for the selected geography and tools is required. Reviewer account access must be arranged privately with the publisher; this repository intentionally contains no test credentials. Tashkent and the period below are example benchmark conditions, not a guarantee of access for every account.

## Canonical OpenAI cases

Use the [reviewer runbook](reviewer-test-runbook.md) for the exact five positive and three negative prompts, expected tools, observable results and evidence requirements. It is generated from `chatgpt-app-submission.json`, which also populates the OpenAI manifest. Do not maintain a second set of OpenAI examples here. Supplemental spreadsheet tests are separate from the eight submitted cases.

The plugin uses existing-account access only. It does not sell subscriptions, promote upgrades or provide transactional links, checkout, top-ups or payments. An unavailable entitlement is an access limitation, not an invitation to purchase.

## Review boundaries

No ad buying/booking, personal tracking, permit-owner matching or direct database access is shipped. Historical timings are API-only observations, not client performance guarantees. See verification.md for which release checks were actually completed.

## Claude directory submission fields

For current submissions, use the [developer portal](https://claude.ai/directory/manage) and the [current submission guide](https://claude.com/docs/plugins/submit). The client is licensed under [AGPL-3.0-only](../LICENSE); the manifest declares the license and privacy-policy URL. An earlier Console submission with a Withdraw button must be withdrawn when migrating to the new portal, after the replacement is prepared. Keep the plugin name and repository path stable. Automated policy holds require reviewer assessment and are distinct from blocking validation errors.

The following table records the earlier Console form; its optional-license field and review status are historical.

Submitted on 8 September 2026 through the [official submission form](https://platform.claude.com/plugins/submit), after the publisher accepted Anthropic's Software Directory Terms. The [submission list](https://platform.claude.com/plugins/submissions) shows **METER — Submitted and pending review**. This is an application for review, not directory approval or publication.

| Field or reference | Value |
| --- | --- |
| Plugin link | https://github.com/Meter-plugin-ai/meter-ai-plugin |
| Path within repository | Leave empty: the Claude plugin is at the repository root |
| Homepage | https://meter.ad |
| Name | METER |
| Submitted platform | Claude Code only; Claude Cowork has not been tested or selected |
| Privacy policy | https://meter.ad/privacy-policy |
| Service terms | https://meter.ad/terms-of-service?lang=en — GEOMOTIVE LTD, verified published on 8 September 2026 |
| Contact email | hello@meter.ad, as published on the official website |
| License | Leave the optional field empty; this package has no assigned open-source license |

Submitted description: Plan outdoor advertising with METER: discover OOH/DOOH inventory, calculate projected audience Universe, OTS and Reach, inspect audience profiles, and prepare address programs from validated results. Connects through OAuth and requires a METER account with access to the requested tools and countries. New OTS coverage varies; unavailable results are disclosed, and legacy calculations are used only when the task permits. Spreadsheet export depends on the file-authoring tools available in the client.

Five example use cases covering inventory, Universe, legacy OTS/Reach, New OTS coverage handling and spreadsheet output were included. The form displayed **Plugin submitted for review** and confirmed receipt. Reviewer correspondence is directed to hello@meter.ad.

The initial form has no field for reviewer credentials. A dedicated testing account with sample data still needs to be arranged privately for functional review, and service-specific privacy coverage needs confirmation. These remain review dependencies under sections 3.A and 3.D of the [Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy); sending the initial application does not establish that they are complete. The Terms of Service URL in the table is a verified public reference, not a separate field in the current Claude form.

## Dedicated-account verification

Use the [reviewer test and demo runbook](reviewer-test-runbook.md) for the exact eight prepared OpenAI cases and the recording sequence. These instructions do not establish that a reviewer account has been provisioned or that its tests have passed.
