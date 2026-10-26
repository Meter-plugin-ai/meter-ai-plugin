# Inventory scope and connection diagnosis

Use the user's connected METER MCP tools. A country-wide request such as «Сколько цифровых экранов в Узбекистане?» is a valid business request; translate it into supported queries while retaining its scope.

## Build a supported query

For `meter_query_surfaces`, send the authorized `countryCode` plus at least one of:

- `city`: the exact city spelling stored in inventory, recovered from the task or a trusted inventory source;
- `id`: an actual METER surface ID supplied by the user or returned by inventory.

Address and description are additional filters, not standalone geography selectors. Every supplied selector must resolve to the declared country. Do not use a guessed ID, an empty city, a wildcard, or a country name in `city`. An alias resolving to a country does not prove that it matches inventory city spelling.

Example for a user request concerning Tashkent:

```json
{"countryCode":"UZ","city":"Ташкент","limit":50,"skip":0}
```

`countryCode` selects the authorization boundary; it does not itself provide the city/ID evidence required by the resolver. Sending only `{"countryCode":"UZ","limit":50,"skip":0}` currently produces `EMPTY_SCOPE` internally and a generic `Tool access denied` to the caller, despite the city and ID fields appearing optional in the tool schema. This behavior was reproduced on 2026-10-26; do not infer the cause of every future denial from that observation.

## Preserve country-wide scope

1. Recover any agreed city list or authoritative inventory roster already available in the task. Use current supported tools if they expose a country-wide inventory or complete city catalog; do not invent such an endpoint.
2. If an authoritative, complete inventory city list is available, query each city in the requested country and paginate each query. Record the source and coverage of that list. A list of familiar or major cities is not a complete national roster.
3. If only a partial list is available, label any retrieved results as partial and name the covered cities. Do not report a national total. If there is no usable list, explain the current country-query limitation and ask for the city scope or a complete inventory export; do not silently substitute Tashkent for Uzbekistan or Almaty for Kazakhstan.
4. A user-provided inventory export can supply a roster or a separately labeled snapshot when appropriate to the request. Disclose its date, unit, filters and coverage. This plugin does not include direct database access. Do not switch sources to evade an authorization denial or disregard a request to use only the OAuth plugin.

For each city use `limit <= 50`, starting at `skip=0`. Advance `skip` by the number of returned rows and stop on a successful short page. A failed page is incomplete retrieval, not zero inventory. On `response_too_large`, retry with a smaller limit at the same offset; if limit 1 fails, report the unresolved page instead of looping. An empty page for an unverified city spelling is not proof that the city has no inventory.

For counts, retrieve all pages before applying digital/type/status filters and counting. Deduplicate repeated rows by the actual surface ID; preserve different sides with different IDs. Do not equate surface records, physical constructions and screens. Use an authoritative grouping key or state that only surface records can be counted. Preserve dismantled/decommissioned warnings and disclose exclusions. A complete city extract does not establish national completeness or bookable availability.

## Handle a generic denial

`MCP -32600: Tool access denied` alone does not distinguish missing permissions from unresolved geography or an unavailable authorization dependency.

- Inspect the submitted arguments first. If a known city/ID from the user's scope was omitted, correct it and retry once. If only a country was requested, follow the country-wide workflow above instead of repeating the same invalid call.
- Do not retry unchanged denials or cycle through countries, identities, credentials, or direct API routes. If a correctly scoped request still fails, report the tool, sanitized selectors and observed error. Use available read-only diagnostics to distinguish the cause; otherwise leave it unresolved.
- A successful `meter_status` proves reachability only. A successful city inventory call proves that this connection can execute that particular request; it does not validate every tool or all national inventory.
- If server diagnostics are available, `country_scope_resolution_failed` with `EMPTY_SCOPE` indicates missing geography evidence; `UNKNOWN_SELECTOR`, `UNSAFE_SELECTOR` and `MIXED_COUNTRIES` require inspecting the selectors. Explicit denied authorization decisions, subscription messages and backend failures are different evidence and should retain their actual meaning.
- Check the actual connected plugin. An empty global `codex mcp list` does not prove that a ChatGPT-managed METER AI connection is absent. Recommend OAuth reconnection only when connection/token evidence supports it, not merely because a tool returned this generic error.

Describe an argument correction as a corrected request, not as repaired OAuth, changed permissions or a server deployment.
