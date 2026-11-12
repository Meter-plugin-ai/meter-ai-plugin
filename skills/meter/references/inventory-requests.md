# Inventory scope and connection diagnosis

Use the user's connected METER MCP tools. A country-wide request such as «Сколько цифровых экранов в Узбекистане?» is a valid business request; translate it into supported queries while retaining its scope.

## Build a supported query

For national inventory, use the authorized country code without a city or ID:

```json
{"countryCode":"UZ","limit":50,"skip":0}
```

For a city or individual surface include its exact inventory city spelling or an actual surface ID. City and ID selectors must resolve to the declared country. Never guess IDs or use a country name as a city. Address and description require a city or ID.

Use `limit <= 50`, beginning at `skip=0`. Advance by the number of rows returned until a successful short page. Check IDs across pages for duplicates or reversals. Inventory may change during pagination, so disclose that a multi-page result is not a frozen snapshot. An error, duplicate, reversal, or incomplete scan cannot establish a national total. If `country_inventory_unavailable` occurs, the upstream does not yet support the country filter; explain the limitation and use a complete trusted city roster only when one is available. Do not infer completeness from a list of major cities.

For counts, filter actual returned digital/type/status fields after retrieving the pages. Keep different sides with distinct IDs and do not equate surfaces, screens and physical constructions without an authoritative grouping key. Retain source warnings such as dismantled status. A record does not confirm bookable availability.

## Handle a generic denial

`MCP -32600: Tool access denied` alone does not distinguish missing permissions from unresolved geography or an unavailable authorization dependency.

- Inspect the submitted arguments first. If a known city/ID from the user's scope was omitted, correct it and retry once. For a country-only request, verify whether the server supports the national inventory path; retain the actual error.
- Do not retry unchanged denials or cycle through countries, identities, credentials, or direct API routes. If a correctly scoped request still fails, report the tool, sanitized selectors and observed error. Use available read-only diagnostics to distinguish the cause; otherwise leave it unresolved.
- A successful `meter_status` proves reachability only. A successful city inventory call proves that this connection can execute that particular request; it does not validate every tool or all national inventory.
- If server diagnostics are available, `country_scope_resolution_failed` with `EMPTY_SCOPE` indicates missing geography evidence; `UNKNOWN_SELECTOR`, `UNSAFE_SELECTOR` and `MIXED_COUNTRIES` require inspecting the selectors. Explicit denied authorization decisions, subscription messages and backend failures are different evidence and should retain their actual meaning.
- Check the actual connected plugin. An empty global `codex mcp list` does not prove that a ChatGPT-managed METER AI connection is absent. Recommend OAuth reconnection only when connection/token evidence supports it, not merely because a tool returned this generic error.

Describe an argument correction as a corrected request, not as repaired OAuth, changed permissions or a server deployment.
