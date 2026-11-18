# What in the code stands between Lastbook and a Czech region

This is a code reading, not a proposal for a data source: [REGIONS.md](REGIONS.md) and the other `REGIONS-*.md` files
already answer "which open dataset replaces each federal list". This file answers only "what in this repository has to
change, and how much". Everything below was read in the working tree on 18 November 2026. Nothing was built or run, so
every figure is a reading of code, and every estimate is the analyst's, not a measurement.

Czechia (Czech Republic, `CZ`, 78,871 km², 14 *kraje*) is used as the example region. It is a good test case because it
is small enough to be one region, it is landlocked (no coastline or sea layer), and its ISO 3166-1 code `CZ` collides
with no US state code in `STATE_CODES` (`engine/address_search.py:26`).

## 1. Verdict

| Question | Answer |
|---|---|
| Does the map format itself block a Czech map? | **No.** A map set is a folder of SQLite files plus `map-set.json`, with no country, projection, unit or place-name assumptions in the format (§2). |
| What blocks it? | **The address pipeline**, and only that: parsing (`engine/address_search.py`), the index builder (`tools/build_addresses.py`) and the two-letter index/region naming rule (`engine/setup/manifest.py:72`, `engine/setup/install.py:267`). §3.1–3.5. |
| Is a single-country `CZ` region cheap? | **Yes.** `CZ` passes every `[A-Z]{2}` gate in the repository unchanged; only the box rule, the place builder and the setup wording need work (§3.3, §3.6, §3.8). |
| Are the 14 *kraje* cheap? | **No.** Their ISO codes are `CZ-10` … `CZ-80` (digits), which fail `build_packs.build_map` (`packaging/build_packs.py:1471`) and the address-index rule (`engine/setup/manifest.py:72`). That is the same wall France hit ([REGIONS-FR.md:50-66](REGIONS-FR.md)). |
| Does any code already support a non-US region? | **No.** No code reads `regions-proposed.json` or any `regions-*.json`; there is no region concept, no `country` field, no non-US builder. §6. |

## 2. The map set the app expects

### 2.1 `map-set.json`

Written by `packaging/build_packs.py:1476`:

```json
{"name": "CA",
 "files": {"derived/geo/national.sqlite": 129593344, "derived/geo/places.sqlite": 13312000, "...": 0},
 "bytes": 414000000,
 "seconds": 41}
```

Read by `engine/setup/install.py:301-311` (`map_set`, `map_name`) and enforced by `check_map`
(`engine/setup/install.py:321-333`): every listed file must exist at exactly that size, and each must match
`map_member` (`engine/setup/install.py:108-112`), i.e. `derived/geo/<name>.sqlite`, `map-set.json`,
`derived/geo/national-status.json`, `derived/geo/socal-cells.json`, or
`library-data/geography/resources/atlas.sqlite`. **Nothing in that check is about the United States**: `name` is an
opaque string, and `map_name` returns it verbatim as `state.current.map` (`engine/setup/api.py:269`).

### 2.2 Files, tables and who reads them

| File | Tables (columns) | Read by | Can CZ fill it without a code change? |
|---|---|---|---|
| `derived/geo/national.sqlite` | `feat(id, layer, cls, name, minz, geom)`, `feat_idx` RTREE`(id, minx, maxx, miny, maxy, minz, maxz)`, `poi(id, cls, name, lon, lat)`, `meta(key, value)` — `tools/build_map.py:128-131` | `server.py` tiles and pins (`server.py:703-710`) | **Yes.** `tools/build_map.py` takes its input and output as `argv` (`tools/build_map.py:13`) and reads a Geofabrik GeoPackage. Its docstring says SoCal; the code does not. OSM tags are global, so a Czech `-free.gpkg` works as it stands. |
| `derived/geo/places.sqlite` | `place(id, name, kind, detail, lat, lon, rank, source)`, `place_fts` FTS5`(name, detail)` — `tools/build_places.py:28-29` | `server.py:1395-1450` (`/api/places`, route at `server.py:2093`) | **Not with the shipped tool** (it reads GNIS and Census, `tools/build_places.py:32-48`), but the schema needs nothing new. A ~60-line builder from the same GeoPackage is enough (§4). |
| `derived/geo/water.sqlite` | `resource(id, source_id, kind, name, lat, lon, detail, source, origin)`, `spatial` RTREE, `feat`, `feat_idx`, `meta`, `water_fts` — `tools/build_water.py:21-29` | `server.py:1064-1080` | Schema yes; the builder reads NID and NHD (US). OSM `waterway`/`natural=water` needs a new reader or a different tool. |
| `derived/geo/terrain.sqlite` | `tile(z, x, y, png)`, `meta` — `tools/build_terrain.py:150-152` | `server.py:798`, relief/contours/3D | Schema yes; source is USGS 3DEP (`tools/build_terrain.py:5`). Copernicus GLO-30 or ČÚZK DMR needs a new reader. |
| `derived/geo/buildings.sqlite` | `bldg(x, y, part, n, data)`, `bldg_socal`, `bldg_osm`, `meta` — `tools/build_buildings.py:94-98` | `server.py:934-1013` | Schema yes; the tool reads Microsoft's *US* footprint release (`tools/build_buildings.py:1`). The global release has the same format, so this is a fetch-argument change plus a check. |
| `derived/geo/crops.sqlite` | `resource`, `spatial`, `tile`, `meta` — `tools/build_crops.py:151-155` | `server.py:1065` | Schema yes; USDA CDL is US-only. Empty tables are legal and show nothing. |
| `library-data/geography/resources/atlas.sqlite` | `resource`, `spatial`, `metadata` | `server.py:1532` | Schema yes, but **no builder exists in this repository** ([MAPS.md:85-88](MAPS.md)). It can ship schema-only, like the California-only layers. |
| `derived/geo/national-status.json` | `{state, stage, features}` — `packaging/state_maps.py:94-96` | `server.py:713-719` | Yes. |
| `derived/geo/socal-cells.json` | `[]` outside Southern California — `packaging/state_maps.py:96-97` | `server.py:725-742` | Yes, and it must be `[]`: `socal_cells()` writes the file itself when it is missing (`server.py:727-737`). |
| `derived/geo/addresses/<ID>.sqlite` | `addr(num, street, norm, city, state, zip, lat, lon)`, `meta` — `tools/build_addresses.py:48`, `packaging/address_indexes.py:55` | `engine/address_search.py:88-125` | Schema yes; **builder and parser no** (§3.1–3.3). |

Most of these are optional to the running app: the water, buildings, terrain and crop databases and the aerial photos
are each guarded by an existence check (`server.py:895, 997, 1013, 1074, 1559, 1570`, `1500-1501`). **They are not
optional to the publisher**: the scan in `packaging/state_maps.py:81-82` requires the file set to equal `ALLOWED`
exactly (`packaging/state_maps.py:43-44`), so a shipped map set must carry crops and atlas even if they are empty.

### 2.3 What the app needs vs what the publisher needs

- To **open** a Czech map, the app needs `derived/geo/national.sqlite`, `derived/geo/places.sqlite` and `map-set.json`;
  every other file is opened only if present (`server.py:703-710`, `1395-1450`).
- To **install** one through setup, the zip needs `map-set.json` plus whatever it lists, at the listed sizes
  (`engine/setup/install.py:321-333`) — still no country assumption.
- To **publish** it, `packaging/state_maps.py:71-122` must pass, and that scan does have US assumptions: exact file set,
  `map-set.json.name == code`, and a buildings bbox check that calls `build_packs.state_box` (§3.3).

## 3. Every place the code is wired to the United States

### 3.1 Address parsing — the real wall

| Place | What it assumes | What a Czech address does |
|---|---|---|
| `engine/address_search.py:41-43` `is_address_query` | a house number, then a space, then a street | Czech order is street, then number: `Vinohradská 12, 120 00 Praha 2` is not recognised as an address at all and goes to the place finder. |
| `engine/address_search.py:56-66` `_parts` | the postcode is the **last** word and is exactly `\d{5}` | Czech PSČ is 3+2 digits written with a space (`110 00`). `normalize` splits it into `110` and `00`, so no postcode is read; written as `11000` it is read. In a Czech address the PSČ comes **before** the town, not at the end. |
| `engine/address_search.py:67-76` | the last 1–3 words are a US state name or code | A Czech town is the last word(s) and matches no state, so the state stays empty — harmless. Two-letter Czech town abbreviations could match a US code (e.g. a street ending in `me`/`il`), which is the failure France measured ([REGIONS-FR.md:265-268](REGIONS-FR.md)). |
| `engine/address_search.py:10-16`, `tools/build_addresses.py:17-19` | English street-type words (`street`, `avenue`, `boulevard`, `north`…) | No `ulice`, `náměstí`, `třída`, `nábřeží`, or the abbreviations `ul.`, `nám.`, `tř.`. |
| `engine/address_search.py:37-38`, `tools/build_addresses.py:22-24` | letters outside `a-z0-9` are separators | `Müllerstraße`-style damage: `náměstí` becomes `n m st`, `třída` becomes `t da`. Czech needs folding (`ě→e`, `ř→r`, `č→c`, `š→s`, `ž→z`, `ů→u`) on **both** the build and the query side, or a tokenizer that folds for you. |
| `engine/address_search.py:46-53` `street_forms` | English ordinals and `n/s/e/w` direction prefixes | Mostly harmless; the ordinal expansion simply never fires for Czech names. |
| `engine/address_search.py:88-90` | the index file is chosen by its **two-letter stem** equal to a US state code | Works unchanged for one `CZ.sqlite`; the id is compared only when a state was parsed, which a Czech query never produces. With no state it searches **all** `addresses/*.sqlite` (`engine/address_search.py:88`), so a CZ index is found. |
| `packaging/address_indexes.py:49` | one index per entry of `state_maps.NAMES`, split by the `state` column | `NAMES` holds 52 US codes (`packaging/state_maps.py:35-41`); a `CZ` index would be skipped by `publish_one`'s `state_maps.NAMES[state]` (line 113) and never built by `build()`. |
| `mobile/ipad/Lastbook/API/MapAPI.swift:1339-1344, 1375-1393` | the same parser and the same `STATE_CODES`, in Swift | Any engine change must be made twice. |

### 3.2 The two-letter index rule

- `engine/setup/manifest.py:72` — an `address_indexes` entry whose id is not `[A-Z]{2}` makes the **whole manifest**
  invalid (`validate` returns `None`), so one bad index id silently disables setup's online manifest.
- `engine/setup/install.py:267` — an upgrade moves only `[A-Z]{2}\.(sqlite|json)` out of `derived/geo/addresses/`;
  anything else is left behind and the user loses address search without a message.
- `engine/setup/api.py:276` — the installed index is looked for at `addresses/<id>.sqlite` with a `<id>.json` receipt.
- `engine/setup/api.py:453-457` — with no explicit `address_id`, the address index id is taken **from the map id**
  (`address_id or map_id`). So a map called `CZ-B` would need an address index called `CZ-B`, which the rule above
  forbids.

For `CZ` this is fine and nothing needs to change. For `CZ-10` … `CZ-80` it is the same blocker as France
(`docs/REGIONS-FR.md:50-53`).

### 3.3 The box, and where it comes from

`packaging/build_packs.py:1288-1294` cuts a state by `min/max` of `zcta` rows in `derived/packs/maps/source/profiles.sqlite`
plus 0.15°. There are no ZCTAs outside the US, so `state_box` raises `no ZIP centres for state CZ`
(`packaging/build_packs.py:1292-1293`). The same function is called from the publisher's buildings check
(`packaging/state_maps.py:113`), so the whole publication path dies with it.

`packaging/state_maps.py:57-60` derives the state list from the same `zcta` table, and `FIRST`
(`packaging/state_maps.py:34`) is a hard-coded US release order. `--order` therefore never reaches a non-US region; an
explicit `packaging/state_maps.py CZ` would, until `state_box` fails.

Fix shape: a box table (the `REGIONS-*.md` files already carry padded boxes computed from official boundaries), or a
`box` key in the map set. Local to `build_packs.state_box` plus its one caller in the scan.

### 3.4 Map set names

`packaging/build_packs.py:1471-1474` accepts exactly three shapes: `base`, `us`, or `re.fullmatch(r'[A-Z]{2}', name)`.
`CZ` passes. `CZ-10` does not, and the error is `unknown map set CZ-10`.

The manifest itself is more generous: map ids are checked by `NAME` (`engine/setup/manifest.py:24`), which allows
hyphens, so `maps` could already carry `DE-BY`-style ids — but see §3.2 for their address indexes.

### 3.5 Names and per-state lists

| Place | Content | Effect on CZ |
|---|---|---|
| `packaging/state_maps.py:35-41` `NAMES` | 52 US names | `NAMES[code]` at `packaging/address_indexes.py:113` raises `KeyError` for `CZ`; `NAMES.get(code, code)` at `packaging/state_maps.py:282` degrades to a bare `CZ` title. |
| `packaging/state_maps.py:33` `KEEP` | `CA`, `RI` kept on disk | Nothing. |
| `engine/address_search.py:17-27` | `STATE_NAMES`, `STATE_CODES`, `STATES` | Nothing for `CZ`; a Czech region name would never match anyway. |
| `mobile/ipad/Lastbook/API/MapAPI.swift:1343-1344` | the same list again | Duplicate to keep in step. |

### 3.6 The place finder

`tools/build_places.py` is the only US-only piece of the `/api/places` path:

- `tools/build_places.py:32-48`: GNIS populated places, Census ZCTA and county gazetteers. None exist for CZ.
- `tools/build_places.py:49-59`: named OSM places from `derived/geo/map.sqlite`, with the detail string
  `'Southern California (OpenStreetMap)'` hard-coded at lines 53 and 58. The SQL is region-neutral.

The read side (`server.py:1395-1450`) has no country assumption at all beyond cosmetics: `norm()` rewrites
`saint → st` (`server.py:1418`), the last-resort detail is `'United States'` in the water path only
(`server.py:1390`), and the FTS query is built from `re.findall(r'\w+', q)` (`server.py:1401`). The tokenizer is
`unicode61` (`tools/build_places.py:29`), whose default `remove_diacritics=1` folds Czech diacritics on both sides — so
`Ricany` should find `Říčany`. That is a property of SQLite, not of this repository, and was **not** tested here.

### 3.7 The layer builders

| Tool | US source | Consequence for CZ |
|---|---|---|
| `tools/build_water.py:1-9` | USACE NID, USGS NHD | new reader needed (OSM or ČÚZK) |
| `tools/build_crops.py:1-8` | USDA Cropland Data Layer | empty, or a EU land-cover mapping (the class list is US crop names) |
| `tools/build_terrain.py:5` | USGS 3DEP | new reader (Copernicus GLO-30, ČÚZK DMR 5G) |
| `tools/build_buildings.py:1-11` | Microsoft US footprints | global release exists in the same format; fetch argument plus a check |
| `tools/build_aerial_coast.py`, `tools/fetch_aerial*.py`, `tools/fetch_lidar.py`, `tools/fetch_nhd.sh`, `tools/fetch_msbuildings.sh` | US agencies | not needed; `has_aerial()` simply stays false (`server.py:1500-1501`) |
| `tools/build_coast.py:86` | closes the sea at longitude `-125` | **not needed for CZ** — landlocked, so no ocean polygon |

### 3.8 The interface, in words and units

These are not blockers, and each is a one-line change, but they are what a Czech user would see first:

- `web/map.js:9` — `const US = [-124.8, 24.4, -66.9, 49.4]` is the fallback view when a map set reports no bounds
  (`web/map.js:93`), so a CZ map with no pins would open on the United States.
- `web/map.js:114` — the button reads `US`, `aria-label="Whole United States"`, replaced by `All` only when the map
  reports bounds (`web/map.js:201`).
- `web/map.js:82` — every distance is formatted in miles (`(km / 1.609).toFixed(...) + ' mi'`); `server.py:1388` does the
  same for water results (`km / 1.609 … ' mi away'`).
- `web/map.js:221` — the coverage note keys off a hard-coded SoCal box (`32.5 < lat < 35.9 && -121.4 < lon < -114.1`),
  the same numbers as `server.py:1444`.
- `web/map.js:108, 875` — "ZIP code", "5-digit ZIP", "Add your state's address search".
- `web/map.js:876` — result zooming keys off `/county/i.test(p.kind)`, and `web/map.js:54-55` labels US record fields
  (`County`, `API number`, `WellStatus`) for the California-only layers.
- `server.py:1444` — `'onMap': bool(pack_info()) or 32.5 < lat …`: for any pack the flag is `True`, so
  `assistant.py:316` would not warn about an off-map Czech place. Cosmetic, but wrong in both directions.
- `server.py:1383` — `d['county'] + ' County'` in the water detail line.
- `server.py:1543-1575` (`map_info`) — the "What this map covers" list is a fixed list of US sources and paths.
- `packaging/build_packs.py:63` — `MAP_CREDIT` is a fixed US credit line, copied into every pack's sources page
  (`packaging/build_packs.py:1242-1243`).
- `web/setup.js:274-280, 299` — "Select your state", "Choose your state", "not available for this state yet";
  `web/setup.js:110` even rewrites the pack description "a detailed map of California". The picker itself is generic:
  it lists `S.manifest.maps` sorted by title (`web/setup.js:92`) and sends the chosen id verbatim (`web/setup.js:282`).

## 4. Minimum for the app to open a Czech map with working place search

Not addresses — places. Six steps, no engine change at all:

1. **Get a CZ GeoPackage.** Geofabrik's `czech-republic-latest-free.gpkg.zip` (ODbL) is the same input format
   `tools/build_map.py` reads.
2. **Build `national.sqlite`.** `python3 tools/build_map.py czech-republic.gpkg derived/geo/national.sqlite`. This gives
   `feat`/`feat_idx` (roads, land use, water outlines, place labels) and `poi` (hospitals, pharmacies, fire stations,
   drinking water, …), which is exactly what `web/map.js` draws and `map_contents()` reports (`server.py:1517-1540`).
   Skip `tools/build_coast.py`.
3. **Build `places.sqlite`.** Same tables as `tools/build_places.py:28-29`: `place` + `place_fts`, filled from the
   `layer='place'` features and named `poi` rows of that same file. Set `source='OpenStreetMap'` — the pack cut copies
   exactly that value (`packaging/build_packs.py:1353, 1409`) — and use `rank` 1 for cities, 3 for towns, 4 for the
   rest, which is what the ordering in `server.py:1435` expects.
4. **Write `map-set.json`** with `{"name": "CZ", "files": {...}, "bytes": N, "seconds": N}`, plus
   `derived/geo/national-status.json` and `derived/geo/socal-cells.json` = `[]`.
5. **Drop the folder into a library's `derived/geo/`** and start the app; `PLACEDB` and `MAPDB` are fixed paths
   (`server.py:43-44`) and both are opened if present.
6. **Place search then works unchanged**: `/api/places` (`server.py:2093`, function at `server.py:1395`) → FTS on
   `place_fts`, `onMap` true because a pack is open. Clicking a result flies the map there (`web/map.js:876`).

To make it an **installable** map set, the zip must contain `map-set.json` and the files it lists
(`engine/setup/install.py:321-333`) and a `maps` entry must exist in the manifest — that entry's `id` `CZ` passes
`NAME` (`engine/setup/manifest.py:24`) and `[A-Z]{2}` where it matters. Nothing else is required: the app does not need
`water`, `terrain`, `buildings`, `crops` or `atlas` to be non-empty.

To make it **publishable** by `packaging/state_maps.py` you additionally need the full `ALLOWED` file set
(`packaging/state_maps.py:43-44`), a name in `NAMES` (`packaging/state_maps.py:35`), a working `state_box` (§3.3) and
`derived/packs/private-terms.txt`, which lives outside the repository (`packaging/state_maps.py:73-75`).

## 5. Effort

Estimates assume one developer who knows the repository. "Small" is a change confined to one function with tests;
"days" means a format, contract or manifest decision that also touches `docs/SETUP-API.md`, the tests in `app/tests/`
and the iPad port.

### Small and local (hours)

| Change | Where | Estimate |
|---|---|---|
| A box from a table instead of from ZCTAs | `packaging/build_packs.py:1288-1294` + caller `packaging/state_maps.py:113` | 3–6 h |
| `CZ` in the publishing lists (`NAMES`, release order) | `packaging/state_maps.py:34-41, 57-60` | 1 h |
| Place builder for any `map.sqlite`/`national.sqlite` (parameterise the label and the input) | `tools/build_places.py:49-59` | 2–4 h |
| Empty-schema siblings so the `ALLOWED` set passes (crops, atlas) | reuse `empty_like`, `packaging/build_packs.py:1306-1323` | 2 h |
| UI wording: "state" → "region", `map.js:108, 875`, `setup.js:110, 274-280` | 2 files | 2 h |
| `onMap` bbox, `US` fallback view, `MAP_CREDIT` | `server.py:1444`, `web/map.js:9, 114`, `packaging/build_packs.py:63` | 3 h |
| Metric distances | `web/map.js:82`, `server.py:1388` | 2 h |

### Days

| Change | Where | Estimate |
|---|---|---|
| **Czech address parsing**: number after street, PSČ with a space, Czech street words, diacritic folding on both sides, a rule that says which country an index is | `engine/address_search.py:10-77`, `tools/build_addresses.py:17-24` | **3–5 d** including the query test set; the French trial went from 1 of 28 queries found to 28 of 28 with such a rework (`docs/REGIONS-FR.md:291-294`) |
| Declaring the rule in the data (`meta.country = 'CZ'`) | index builders + `engine/address_search.py:88` | 1 d (the FR trial did exactly this, `docs/REGIONS-FR.md:295-297`) |
| **Address index building for CZ**: `country = 'CZ'` instead of `'US'`, PSČ kept whole instead of `left(postcode,5)`, region kept instead of `state.upper()[:2]` | `tools/build_addresses.py:32, 41, 53` | 1–2 d |
| Splitting/publishing the index per region | `packaging/address_indexes.py:49, 113` (iterates `NAMES`, splits on `state`) | 1 d |
| The same work in Swift | `mobile/ipad/Lastbook/API/MapAPI.swift:1339-1400` | 3–5 d |
| Manifest/install rule for hyphenated region ids **if** CZ is split into *kraje* | `engine/setup/manifest.py:72`, `engine/setup/install.py:267`, `docs/SETUP-API.md:131-182`, `app/tests/test_setup.py` | 2–3 d, and it is a published contract, so a maintainer decision comes first (`docs/REGIONS.md:136-138`) |
| New per-layer builders (water, terrain, buildings, crops) | `tools/build_water.py`, `build_terrain.py`, `build_buildings.py`, `build_crops.py` | 1–3 d each, dominated by source work, not by app code |

### Three realistic scopes

| Scope | Content | Estimate |
|---|---|---|
| **A. Local, unlisted** | `national.sqlite` + `places.sqlite` + `map-set.json`, installed by hand; map and place search work, no addresses, not in the manifest | **2–4 d** |
| **B. One published `CZ` region** | A, plus the box table, the publish scan, setup wording, a manifest entry, `CZ` address index with a Czech parser (engine only, iPad unchanged) | **2–3 weeks** |
| **C. 14 *kraje*** | B, plus hyphenated ids through manifest/install/`map-set.json`, one index per region, the Prague-inside-Středočeský question (the Berlin/Brandenburg case, `docs/REGIONS-DE.md:45-52`), and the iPad port | **+2 weeks, after a contract decision** |

The anchor for these numbers is the French trial build, which is described in this repository but not included in it
(`docs/REGIONS-FR.md:270-312`): the map format held unchanged, the per-layer builders and the address parser were the
whole job, and the result was 414 MB for three départements. Nothing in that account suggests the map set format itself
needs a change for CZ.

## 6. Is there any existing path for a region outside the US?

**No.** Concretely:

- No code reads `docs/regions-proposed.json`, `regions-de-proposed.json`, `regions-fr-proposed.json` or any sibling
  (checked by searching the tree for `regions-` outside `docs/`). `docs/REGIONS.md:8-11` states the same: "No code reads
  it, and it does not ship".
- `packaging/build_packs.py:1460-1474` knows three map set names and no others.
- There is no `country` column or key in any map file the builders write. `feat`, `poi`, `place`, `resource` and `addr`
  carry none, and the only "region" field is `addr.state`, two characters, written as `state.upper()[:2]`
  (`tools/build_addresses.py:53`). A `meta` key could be added by a builder, as the French trial did, but nothing in the
  app reads one today.
- The map install path is id-agnostic (`engine/setup/install.py:301-333`, `engine/setup/api.py:452-460`), so it would
  accept `CZ` today; the address index path is not (`engine/setup/manifest.py:72`, `engine/setup/install.py:267`).
- Setup's screens call everything a "state" (`web/setup.js:274-280`), and `map_info` and `MAP_CREDIT` list US agencies
  and US source paths by name (`server.py:1543-1575`, `packaging/build_packs.py:63`).

The nearest thing to a hook is the French trial's proposal that each index declare its spelling rule in `meta`
(`docs/REGIONS-FR.md:295-297`), and the Berlin issue it cites (#79, `norm = de-1`). Adopting one key — say
`meta.country` plus an optional `meta.norm` — is the smallest honest way to make the address path country-aware, and it
is a data-format decision that should be made once for all regions rather than per country.

## 7. What this reading did not establish

- No build was run and no data was downloaded; every claim is a reading of the code at commit `9542e80`.
- Whether Overture's address theme carries Czech rows, and how many, was not measured. `tools/build_addresses.py:32`
  filters on a `country` column, so the pipeline is the right one; Germany's 19.3 M rows
  (`docs/REGIONS-DE.md:152-155`) show what the count looks like when a country is covered.
- Czech postcode and address-order conventions (PSČ as `110 00`, street before number, orientation numbers such as
  `12/345`) are general knowledge about the country, not something this repository documents; they should be checked
  against Česká pošta's addressing rules before the parser is written.
- The ISO 3166-2:CZ codes `CZ-10` … `CZ-80` are quoted from general knowledge; the other region files also note that
  their codes were not checked against the ISO site (`docs/REGIONS-DE.md:37-38`).
- The SQLite `unicode61` diacritic folding assumed in §3.6 is a documented default, not something this repository tests.
- Whether one `CZ` region is the right granularity (78,871 km², 10.9 M people) is a product decision, not a code one;
  the precedent in this repository for small countries is one region (`GY`, `PY`, `IE`, `LK` in the `REGIONS-*.md`
  files).
