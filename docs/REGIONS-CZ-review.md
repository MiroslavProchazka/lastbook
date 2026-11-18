# Review of the Czechia region documents

An independent read of the three new files on `cz-region` against their German counterparts and against the code they
cite. Nothing in the three files was changed; this review is the only new file.

- **Scope.** `docs/REGIONS-CZ.md`, `docs/regions-cz-proposed.json`, `docs/REGIONS-CZ-code-impact.md`; compared with
  `docs/REGIONS-DE.md` and `docs/regions-de-proposed.json`; every `file:line` reference checked against the working
  tree at `2a57de1`.
- **What this review did not check.** The external world: every publisher page, licence text, byte length and taginfo
  count is taken as the documents state it. This review was done offline and reopened no publisher page, so "opened"
  cannot be confirmed here — only that a claim is internally consistent and marked.

## Verdict

The shape is right and the arithmetic is right. All 14 regions parse, every code, name, district, municipality, box
and extract size agrees between the Markdown and the JSON, all padding is exactly 0.15° rounded outward, and 122 of
128 code references point at the line they claim. Three things should not ship as they stand: the list of boxes that
reach a neighbouring country is wrong in two places, the two new prose documents contradict each other about whether
the ISO codes and the postal conventions were actually read, and one byte figure is described as a TIFF in one file
and a ZIP in the other.

## Blocking

### B1. The neighbour list is wrong for CZ-31 and CZ-53

`docs/REGIONS-CZ.md:112-116`, `docs/regions-cz-proposed.json` entries `CZ-31` and `CZ-53`.

The Markdown says: "`CZ-20`, `CZ-32`, `CZ-41`, `CZ-42` and `CZ-51` reach Germany … `CZ-31`, `CZ-63` and `CZ-64` reach
Austria", and then "`CZ-10` and `CZ-53` reach no neighbour at all in that test." The JSON agrees: `CZ-31` carries
`padded_box_touches: ["Austria"]`, and `CZ-53` carries no such key at all.

Reproducing the stated test — a grid over each padded box tested against the same file, `web/world-context.json`
(Natural Earth 1:110m) — gives:

| Region | Padded box | Hit in the file | Points |
|---|---|---|---|
| `CZ-31` | 13.38, 48.40, 15.76, 49.78 | Germany, 13.38–13.59 E / 48.60–49.04 N | 2,415 |
| `CZ-53` | 15.21, 49.42, 17.02, 50.36 | Poland, 16.34–16.80 E / 50.22–50.36 N | 3,190 |
| `CZ-10` | 14.07, 49.79, 14.86, 50.33 | none | 0 |
| `CZ-32` | 12.25, 48.79, 14.00, 50.26 | Austria, 13.53–13.79 E / 48.79–48.88 N | 756 |

CZ-31 and CZ-53 are not artefacts of a coarse outline: Jihočeský kraj borders Bavaria along the Šumava, and
Pardubický kraj reaches the Polish border in okres Ústí nad Orlicí. The CZ-53 box additionally reaches 0.15° of the
Kłodzko salient in Poland, and the CZ-31 box covers a band of the Bavarian Forest. Both omissions matter for the very
reason the section exists: a per-region build that clips rows by box will pull German and Polish rows into these two
maps, and the document that is supposed to warn about it says there are none.

The `CZ-32`/Austria hit is the opposite case — Austria's 1:110m outline is drawn about 0.1° too far north there, and
that patch is Bavaria in reality — which is worth saying out loud, because it puts a number on how far the test can be
trusted.

Fix: add `Germany` to `CZ-31` and `Poland` to `CZ-53` in both files, and replace "`CZ-10` and `CZ-53` reach no
neighbour at all" with "`CZ-10` reaches no neighbour", plus one sentence that the 1:110m outline is off by up to ~0.1°
at the Austrian border.

### B2. The two new prose documents contradict each other about what was read

`docs/REGIONS-CZ.md:46-49` and `:251-254` against `docs/REGIONS-CZ-code-impact.md:283-287`.

REGIONS-CZ.md says the codes "were read from Wikipedia's copy of ISO 3166-2:CZ (opened)", and the JSON repeats it
(`codes.verified`). REGIONS-CZ-code-impact.md:286-287 says "The ISO 3166-2:CZ codes `CZ-10` … `CZ-80` are quoted from
general knowledge".

The same split appears for the postal conventions: REGIONS-CZ.md:251-254 quotes Česká pošta ("Mezi trojčíslím a
dvojčíslím PSČ je jedna mezera") and its "What was checked" list at `:312` includes "Česká pošta's page on
addressing", while code-impact:283-285 says the postcode and address-order "conventions … are general knowledge about
the country … they should be checked against Česká pošta's addressing rules before the parser is written".

One of each pair is wrong. The mark scheme is the only reason to trust these documents, and it is exactly this class of
disagreement a maintainer will look for. Fix: make code-impact defer to REGIONS-CZ.md — the codes came from
Wikipedia's copy (and nowhere near the ISO site), and the PSČ form was read on Česká pošta's page — or correct
REGIONS-CZ.md if that is the untrue one.

### B3. One byte count is a TIFF in one file and a ZIP in the other

`docs/REGIONS-CZ.md:172-173` against the `INSPIRE elevation grid (EL-GRID)` entry in the JSON.

The Markdown: "The INSPIRE elevation grid is one 7,685,616,237-byte TIFF for the whole country." The JSON:
"Zip is 7,685,616,237 bytes." Both cite the Atom feed and its file length as the source, so only one can be right.
This is not cosmetic: 7.7 GB is either the raster the terrain builder would read or an archive of unknown uncompressed
size, and "Still undecided" item 5 (REGIONS-CZ.md:293-296) asks a maintainer to weigh that grid against DMR 4G and
DMR 5G on exactly that basis.

Fix: change the one word to what the feed actually says, and if it is a ZIP, name the uncompressed size or say it is
unknown.

## Should fix

### S1. `NAME` is at line 26, not 24

`docs/REGIONS-CZ-code-impact.md:120` and `:205` cite `engine/setup/manifest.py:24` for the id pattern. Line 24 is
`import urllib.parse`; `NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$')` is line 26. REGIONS-CZ.md:60 gets it
right, so the two documents disagree as well. The conclusion (hyphens allowed) is unaffected.

### S2. `build_packs.py:1353` is cited for the opposite of what it does

`docs/REGIONS-CZ-code-impact.md:194`: "Set `source='OpenStreetMap'` — the pack cut copies exactly that value
(`packaging/build_packs.py:1353, 1409`)." Line 1353 is in `base_set` and reads
`INSERT INTO place SELECT * FROM src.place WHERE source<>'OpenStreetMap'`; only 1409 is the state cut,
`… WHERE source='OpenStreetMap' AND lon BETWEEN …`. Cite 1409 alone, or cite 1353 as the reason the base set carries
no OSM places.

### S3. `tools/build_map.py:13` is a docstring delimiter

`docs/REGIONS-CZ-code-impact.md:46`: "takes its input and output as `argv` (`tools/build_map.py:13`)". Line 13 is the
closing `"""`; the statement is `SRC, DST = sys.argv[1], sys.argv[2]` at line 17. The claim is true, the pin is not.

### S4. The table list for `buildings.sqlite` names a table the cited file does not create

`docs/REGIONS-CZ-code-impact.md:50` gives "`bldg(x, y, part, n, data)`, `bldg_socal`, `bldg_osm`, `meta` —
`tools/build_buildings.py:94-98`". Those lines create `bldg`, `done`, `bldg_socal`, `done_socal` and `meta`; `bldg_osm`
is written by `tools/build_osm_heights.py`. The omission is the more useful half: `packaging/state_maps.py:117`
rejects a pack that still holds `done` or `done_socal`, so a builder for Czechia has to know they exist and has to
drop them. Name the file that makes `bldg_osm` and note the two progress tables.

### S5. The JSON's top-level key set drifts from its siblings

`docs/regions-cz-proposed.json` uses `not_open_or_not_used`; `regions-de-proposed.json`,
`regions-fr-proposed.json` and `regions-es-proposed.json` all use `not_open_nationwide`. Everything else at the top
level matches. A reader or a future script that walks the siblings by key will silently miss DIBAVOD, the aerial
imagery and EuroCrops. Rename to `not_open_nationwide` unless the change is deliberate for all four files.

### S6. Most `verified` fields in the JSON carry no mark

`docs/regions-cz-proposed.json`, `country_layers`: 18 of the 22 entries have `"verified": "2026-11-18"` and nothing
else. Only DIBAVOD ("not checked — …"), dams ("search only — …") and the two address entries ("… opened …") use the
vocabulary the Markdown defines at `REGIONS-CZ.md:17-21`. The Markdown's own preface says "Each source carries one of
three marks"; the machine-readable file does not. Either add the mark to the `verified` string or add a separate
`mark` field (`opened` / `search_only` / `not_checked`) so the two files say the same thing.

### S7. Two counts exist only in the JSON, and one only in the prose

`docs/regions-cz-proposed.json` `country_layers.pois[0].counts` holds `emergency=water_tank` 206 and
`shop=supermarket` 2,941, neither of which appears in the Markdown's help-point table (`REGIONS-CZ.md:205-217`). In the
other direction the same `counts` object carries `emergency=drinking_water` 0, which the Markdown states only in prose
(`REGIONS-CZ.md:219`). Nothing contradicts, but a reader comparing the two files will find 11 rows against 14. Add the
two rows, or say in the Markdown why they are left out.

### S8. Factual claims about sources that carry no mark

The mark scheme is only worth something if it is applied to the prose, not just to the tables. These claims are about
what a publisher says or publishes, and carry no **opened** / **search only** / **not checked**:

| Where | Claim |
|---|---|
| `REGIONS-CZ.md:25-29` | "one licence, Creative Commons CC BY 4.0, for nearly every layer"; "RÚIAN has been open data since 2012, and ZABAGED, the elevation models, Geonames and the state map series since 1 July 2023, all free of charge" — the 2023 date appears in no other file and in no table row |
| `REGIONS-CZ.md:124-126` | "Geofabrik cuts Czechia into exactly the 14 kraje" |
| `REGIONS-CZ.md:145` | "Moravia-Silesia's file name is `moravskoslezky` on Geofabrik, with a letter missing" (derivable from the table above it, so the mildest of these) |
| `REGIONS-CZ.md:186-189` | ZABAGED's 5,805,826,649 and 6,742,892,709 bytes, "buildings are among its 142 planimetric feature types", INSPIRE buildings "one file per obec, roughly 6,258 of them" |
| `REGIONS-CZ.md:196-198` | Geonames' "about 165 types of named object", "three-year revision cycle", 46,625,753 bytes |
| `REGIONS-CZ.md:224-228` | ČÚZK's attribution form "ČÚZK, [rok]", the metadata and the change note — the single most load-bearing licence claim in the document, and the German sibling marks its equivalent "(opened, document of 19 August 2025)" at `REGIONS-DE.md:200` |
| `REGIONS-CZ.md:233-235` | "Microsoft's README says … CDLA Permissive 2.0"; "Overture lists the same data under the ODbL" |
| `REGIONS-CZ.md:255-259` | "The formatted-address rows in the special RÚIAN address export follow decree 359/2011 Sb." — no source at all, and it is not in the "What was checked" list |

Most of these are probably fine — the "What was checked" list covers the pages — but the check is on the reader to
match a prose claim to a bullet three hundred lines later. Add "(opened)" or "(search only)" where the sentence makes
the claim, as REGIONS-CZ.md already does at `:203` and `:307`.

## Nits

1. `engine/setup/install.py:108-112` (`code-impact.md:37`) — `def map_member` is line 109; the range should be
   109-114.
2. `tools/build_water.py:21-29` (`code-impact.md:48`) is cited for a column list that includes `water_fts`; that table
   is created at line 290 of the same file.
3. `tools/build_terrain.py:150-152` (`code-impact.md:49`) lists `tile` and `meta` but the range also creates `done` at
   line 152. Same class as S4, without the consequence.
4. `padded_box_touches` is present on 12 regions and absent — not `[]` — on `CZ-10` and `CZ-53`; `contains` appears only
   on `CZ-20`. A consumer has to test for the key. Give every region the key with an empty list.
5. `code-impact.md:226-227` drops the prefixes its own text keeps: `map.js:108, 875`, `setup.js:110, 274-280`, and
   `MAPS.md:85-88` / `REGIONS-FR.md:50-66` at `:19`. Everything else in the file is `web/map.js`, `docs/…`.
6. `code-impact.md:279` says "every claim is a reading of the code at commit `9542e80`" while the branch head is
   `2a57de1`. `git diff --stat 9542e80 HEAD` shows only the three new docs, so the statement holds, but name the head
   and note the code is identical — otherwise the next reader has to check.
7. `REGIONS-DE.md:221` and `REGIONS-ES.md:240` say where the attribution belongs (`THIRD_PARTY_NOTICES.md`, which
   exists at the repository root). The CZ licence section (`REGIONS-CZ.md:222-244`) never says. FR omits it too, so
   this is a gap against the DE template rather than a break with the family.
8. `REGIONS-DE.md:12-13` records that "a person reviewing the result" took part. `REGIONS-CZ.md:12-15` says what was
   opened and what was computed, and not who reviewed it.
9. The JSON's `licences` map holds `LPIS-not-copyrighted`, which is a data.gov.cz record status, not a licence, and its
   `url` is a catalogue record. Two kinds of key in one map makes a consumer's life harder; a `status` field on the
   crop entry would carry the same fact.
10. `REGIONS-CZ.md:102-104` calls the extreme-point check a check, but the four numbers it compares against (12.0906 E,
    18.8593 E, 48.5518 N, 51.0557 N) are the maxima and minima of the same file the boxes came from. It is a
    consistency check on the arithmetic, not on the data — worth one clause so nobody reads it as independent.

## What passed

- **Template.** Every section of `REGIONS-DE.md` has a counterpart: title, proposal caveat, "How things were checked",
  "Why Czechia …", "What a region is" with Codes and Boxes, "Sources, layer by layer" with Notes, "Help points",
  "Licence notes and attribution", "How addresses are written", "Still undecided", "What was checked, and what was
  not". Two differences are justified: "Prague inside Central Bohemia" replaces "City-states" (same argument, one
  enclave instead of two), and DE's "Nationwide" / "State by state" split is dropped with the reason given at
  `:152-153`. One addition is not a deviation at all: `### OpenStreetMap extracts` also exists in `REGIONS-FR.md:149`.
  The eight items of S8 and nit 7 are the only template-shaped gaps.
- **JSON.** Parses with `json`. 14 regions. Codes, names, `national_code`, `okresy`, `obce`, raw box, padded box,
  extract name, `.osm.pbf` bytes and `-free.gpkg.zip` bytes are identical in the Markdown table and the JSON for all
  14 regions — checked by parsing both and comparing field by field, not by eye.
- **Maths.** For all 14: `west < east` and `south < north`; the padded box equals the raw box ∓ 0.15 rounded outward
  to 0.01; every padded value lies inside 12.09–18.86 E / 48.55–51.06 N ± 0.15. The four extremes sit exactly on the
  limit — `CZ-41` west 11.94, `CZ-80` east 19.01, `CZ-31` south 48.40, `CZ-42` north 51.21 — which passes, but only
  because the tolerance and the padding are the same number.
- **Containment.** Only `CZ-20` contains `CZ-10`, raw and padded, as `:118-120` claims.
- **Numbers.** 72,842,120 in both files (once in the Markdown, in all 14 `bbox.source` blocks); 77 districts and 6,258
  municipalities in both, and the table's `okresy` and `obce` columns sum to exactly those; the 14 `.osm.pbf` sizes sum
  to 1,060,544,679, as `:146` says. The figure 53,617 in the brief appears in neither file, so there was nothing to
  compare — worth asking where it came from.
- **Code references.** 128 distinct `file:line` references in `REGIONS-CZ-code-impact.md`, of which 3 are wrong (S1,
  S2, S3), 1 is off by one (nit 1) and 2 name an incomplete table list (S4, nit 2). The other 122 land on the line they
  describe, including all of §3.2, §3.8, the table in §2.2 apart from S4, and every reference into `REGIONS-DE.md`,
  `REGIONS-FR.md`, `REGIONS.md`, `MAPS.md` and `SETUP-API.md`. The three line-pinned references in
  `REGIONS-CZ.md:57-61` (`manifest.py:72`, `install.py:267`, `manifest.py:26`) are all correct, as are its claims
  that `CZ` is absent from `STATE_CODES`, that `PR`, `MO`, `PA` and `US` are taken, and that `POI_KEEP` contains
  `fuel` while `build_map.py` reads only the `gis_osm_pois_*` and `gis_osm_natural_*` tables, so it never matches.

## Appendix: how to reproduce

Only `python3` and the working tree were used; no installs.

```python
# 1. the two files agree, field by field
import json, re
md = open('docs/REGIONS-CZ.md').read()
j = json.load(open('docs/regions-cz-proposed.json'))
rows = {m[0]: m[1:] for m in re.findall(r'\| `(CZ-\d\d)` \| (\d+) \| (.+?) \| (\d+) \| ([\d,]+) \| ([\d., ]+) \| ([\d., ]+) \|$', md, re.M)}
# compare rows[code] with each region's national_code, name, okresy, obce, bbox, padded_0_15
```

```python
# 2. every file:line reference, resolved and printed with its line
import re
pat = re.compile(r'((?:[\w./-]+/)*[\w.-]+\.(?:py|js|swift|json|md|sh)):(\d+)(?:[-–](\d+))?')
for path, start, end in sorted(set(pat.findall(open('docs/REGIONS-CZ-code-impact.md').read()))):
    lines = open(path).read().split('\n')
    print(path, start, lines[int(start) - 1])
```

```python
# 3. the neighbour test, over the same Natural Earth file the document names
#    a 400 x 400 grid over each padded box, point-in-polygon against Germany, Poland, Austria, Slovakia
```

The three sketches above are the shape of the checks, not the exact scripts (about sixty lines in total); they are not
shipped with this review.
