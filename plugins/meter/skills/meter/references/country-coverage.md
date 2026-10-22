# Country recommendations for combined OTS and Reach

These are **dated, sampled API results**, verified on **22 October 2026** for **1–30 September 2026**. They are recommendations for choosing a combined campaign OTS/Reach tool, not live coverage, an access grant, or a guarantee for every city, surface, audience or period. Installing this version does not change account permissions or country subscriptions.

There are **24 countries** with verified nonzero combined OTS and Reach examples: **22 legacy**, **6 New OTS**, with **4 in both**. The public [machine-readable matrix](calculation-coverage.json) contains the same recommendations, actual city spellings from the inventory and the verification scope. Its `inventory_cities` are discovery/alias data; they are not a list of individually verified calculation cities.

## Choose the method

1. Establish the requested country and use the actual localized city string returned by inventory. A country/city alias does not translate or canonicalize an API input. Use returned surface IDs and preserve the requested audience, dates and campaign controls. Do not substitute the example city below for a different user-requested city.
2. If the user did not specify a method, use the table’s default: **New OTS for Italy/IT and Morocco/MA**, **legacy for the other 22 countries**.
3. Preserve an explicitly requested method even when the dated audit did not verify that pair. Explain the verification gap, use the same requested method, and report its actual result; do not silently substitute a method.
4. For an unlisted country, coverage remains **unverified**, not prohibited. Current tool and account access still determine which calls are allowed. In the absence of current evidence or an explicit method, a legacy first probe remains an unverified reference choice, not confirmed support.

| Country | ISO | Verified combined method(s) | Default tool | Verified city example |
| --- | --- | --- | --- | --- |
| United Arab Emirates | AE | Legacy + New OTS | `meter_ots_reach` | Dubai |
| Azerbaijan | AZ | Legacy | `meter_ots_reach` | Baku |
| Bahrain | BH | Legacy | `meter_ots_reach` | Manama |
| Belarus | BY | Legacy | `meter_ots_reach` | Minsk |
| Germany | DE | Legacy | `meter_ots_reach` | Berlin |
| Egypt | EG | Legacy | `meter_ots_reach` | Cairo |
| France | FR | Legacy | `meter_ots_reach` | Paris |
| United Kingdom | GB | Legacy | `meter_ots_reach` | London |
| Georgia | GE | Legacy | `meter_ots_reach` | Batumi |
| Iraq | IQ | Legacy | `meter_ots_reach` | Baghdad |
| Italy | IT | New OTS | `meter_new_ots_reach` | Roma |
| Jordan | JO | Legacy | `meter_ots_reach` | Amman |
| Kyrgyzstan | KG | Legacy | `meter_ots_reach` | Бишкек |
| Kuwait | KW | Legacy | `meter_ots_reach` | Kuwait City |
| Kazakhstan | KZ | Legacy + New OTS | `meter_ots_reach` | Алматы |
| Morocco | MA | New OTS | `meter_new_ots_reach` | Casablanca |
| Oman | OM | Legacy | `meter_ots_reach` | Muscat |
| Pakistan | PK | Legacy | `meter_ots_reach` | Islamabad |
| Poland | PL | Legacy | `meter_ots_reach` | Warsaw |
| Qatar | QA | Legacy + New OTS | `meter_ots_reach` | Doha |
| Saudi Arabia | SA | Legacy | `meter_ots_reach` | Riyadh |
| Tajikistan | TJ | Legacy | `meter_ots_reach` | Душанбе |
| Turkey | TR | Legacy | `meter_ots_reach` | Istanbul |
| Uzbekistan | UZ | Legacy + New OTS | `meter_ots_reach` | Ташкент |

Vatican is not a separate 25th country in this matrix. A surface labeled Vatican returned New OTS metrics through the Rome model; that does not establish an independent Vatican model or country-wide coverage.

## Recovery

- On explicit New OTS `no_data`, keep the unavailable result visible. Retry equivalent legacy **once** only if the brief permits changing methodology and the country guidance permits automatic fallback. Preserve audience, dates, surface IDs and controls, and label any successful fallback as legacy.
- **Italy/IT and Morocco/MA: no automatic legacy fallback.** Their audited legacy examples returned zero OTS, Universe and Reach. Retain unavailable New OTS and its limits. If the user explicitly requests a legacy calculation, preserve that request and disclose the gap; the dated table does not forbid the call.
- In the 22 legacy-verified countries, a task-permitted equivalent legacy fallback can use the verified method. For an unlisted country, a task-permitted legacy probe remains unverified.
- Invalid parameters require correcting the same tool. Other errors, timeouts or zeros do not trigger an automatic methodology change. Do not retry an unchanged timeout.
- HTTP 200 with zero metrics is **not confirmation of working positive calculation coverage**. Retain the actual zero result; do not relabel it as `no_data`, invent an estimate or mark the geo verified.

## What was and was not checked

The checks used one selected surface for each primary country/method example, plus alternate legacy examples for geos with zero results. The reference setup was ages 6–100, all genders, income abc; 10-second creative, one output, block size 0, `impressions=[-1]`, no daily breakdown, normalization 0.3. New OTS examples used UTC and confirmed all 30 days without donor substitution. These are test assumptions, not universal defaults or a confirmed placement schedule.

Positive OTS and Reach, a valid audience denominator, matching IDs and basic Reach bounds were checked. OTS remains projected contacts and Reach remains projected unique audience; these checks do not establish factual model accuracy. The availability observation came from direct API calculations, not a replay proving every client or subscription path. Current responses still determine whether a new request succeeds.

This matrix verifies only `meter_ots_reach` and `meter_new_ots_reach`. Do not infer support for Universe, per-surface or broadcast calculations, profiles, low-level New OTS, inventory selection/ranking or spreadsheet exports from these results. Each requested operation retains its own validation and limits.

## Optional local routing helper

If local Python execution is available, [calculation-routing.py](../scripts/calculation-routing.py) returns the same advisory default, preserves an explicit method and checks whether one legacy fallback may be suggested. It performs no network calls, writes, calculations or access changes. Otherwise apply the table directly; a local runtime is not required to use METER.

```sh
python3 <skill-directory>/scripts/calculation-routing.py IT
python3 <skill-directory>/scripts/calculation-routing.py AZ --method new --new-ots-no-data --allow-legacy-fallback
```

Use `--new-ots-no-data` only for a retained explicit `no_data` response and `--allow-legacy-fallback` only when the task permits changing methodology. Neither flag grants account permissions. `sample_city` is example metadata, never an input to insert silently. Unknown countries and explicitly selected unverified methods remain marked unverified.
