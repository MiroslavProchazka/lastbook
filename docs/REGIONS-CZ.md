# Detailed maps for Czechia: a proposal

This is a proposal for discussion, not a decision. It answers, for Czechia, the questions [MAPS.md](MAPS.md) asks before
coverage can go beyond the United States: which open source replaces each federal list, under what licence, what a
"state" is there, and how addresses are written. It follows the shape of [REGIONS-DE.md](REGIONS-DE.md),
[REGIONS-FR.md](REGIONS-FR.md) and [REGIONS.md](REGIONS.md) and is meant to feed the same design discussion (issue #31).
The machine-readable version is [regions-cz-proposed.json](regions-cz-proposed.json).

Nothing here changes the app, the engine or a build. No code reads the JSON, and nothing here ships: builds package
`web/` and `content/` only.

**How things were checked.** Research was done on 18 November 2026, opening the publishers' own pages. The 14 region
boxes were computed the same day from ČÚZK's own boundary file, which was downloaded in full (72,842,120 bytes) and
every vertex read; the OpenStreetMap extract sizes are HTTP HEAD answers, and the OpenStreetMap counts come from
taginfo's API. A second pass the same day reopened the seven licence and date claims that carry the most weight, and
its readings are recorded in [REGIONS-CZ-source-check.md](REGIONS-CZ-source-check.md); where the two disagree, the
marks below follow that pass. Each source carries one of three marks:

- **opened**: the dataset or licence page itself was opened and read;
- **search only**: the fact was seen in a search result from the publisher's own site, but the page itself was not
  opened;
- **not checked**: the page could not be reached or read, or the question was not looked at; the row says what is
  missing.

## Why Czechia is a different case

Germany needed 16 state agencies and four licences. Czechia has one surveying office, ČÚZK, and one licence,
Creative Commons CC BY 4.0, for nearly every layer this proposal needs (opened): ZABAGED (buildings, water, land use),
DMR 4G and DMR 5G (elevation), RÚIAN (addresses and administrative units), Geonames and the INSPIRE copies of these.
RÚIAN has been open data since 2012, and with it the four INSPIRE themes Katastrální parcely, Budovy, Adresy and Územní
členění; ZABAGED, the elevation models, Geonames and the state map series have been free open data since 1 July 2023,
but only in selected formats (*ve vybraných formátech*), the rest still being sold through ČÚZK's e-shop.

So the question is not "is there an open source" but three narrower ones: how Lastbook reads Czech addresses, which
Czech projection it converts from (S-JTSK / Křovák, EPSG:5514, or ETRS89 / TM33, EPSG:3045), and how a permissive
licence sits next to OpenStreetMap's share-alike one in the same `poi` table. There is also a real gap: the water layer
that Czech water management uses, DIBAVOD, grants no licence on its own pages — no licence means all rights reserved
by default, with permission on request from VÚV (opened).

## What a region is

Czechia has 14 self-governing regions (*kraje*), one of them the capital, Prague. The proposal is one map region per
kraj, 14 in all, the level closest to a US state. Below them sit 77 districts (*okresy*, Prague counting as one) and
6,258 municipalities (*obce*), counted from the boundary file used for the boxes.

### Codes

ISO 3166-2:CZ gives the regions **two digits**, not two letters: `CZ-10` Prague, `CZ-20` Central Bohemia, `CZ-31` South
Bohemia, `CZ-32` Plzeň, `CZ-41` Karlovy Vary, `CZ-42` Ústí nad Labem, `CZ-51` Liberec, `CZ-52` Hradec Králové, `CZ-53`
Pardubice, `CZ-63` Vysočina, `CZ-64` South Moravia, `CZ-71` Olomouc, `CZ-72` Zlín, `CZ-80` Moravia-Silesia. These were
checked against OMG's ISO 3166-2 ontology for Czechia, which reproduces the ISO list: it defines exactly these 14
first-level units and carries no letter code (opened). Wikipedia's copy of ISO 3166-2:CZ also records that ISO replaced
the older letter form (`CZ-PR`, `CZ-JC`, `CZ-JM`, `CZ-KA`, `CZ-KR`, `CZ-LI`, `CZ-OL`, `CZ-PA`, `CZ-PL`, `CZ-ST`, `CZ-US`,
`CZ-VY`, `CZ-ZL`, `CZ-MO`) on 15 November 2016; **that date is unverified**, because ISO's Online Browsing Platform
answers HTTP 403 and the change log could not be read at the source (not checked). The codes themselves were not checked
against the ISO site, as REGIONS.md, REGIONS-DE.md and REGIONS-FR.md also note for theirs.

- **A bare `CZ` is safe.** It is not in `STATE_CODES` (`engine/address_search.py`), so it collides with no US state.
- **The letter codes are not usable as they stand.** Three of the 14 old parts are US codes: `PR` (Puerto Rico), `MO`
  (Missouri) and `PA` (Pennsylvania). A fourth, `US`, is the ISO 3166-1 code for the United States and would read as a
  country rather than a region. None of the other ten (`JC`, `JM`, `KA`, `KR`, `LI`, `OL`, `PL`, `ST`, `VY`, `ZL`) is a
  US code, and neither is the bare `CZ`.
- **The current numeric codes fail the address-index rule.** `engine/setup/manifest.py` line 72 and
  `engine/setup/install.py` line 267 accept an address index only under `[A-Z]{2}`; `packaging/build_packs.py`
  (`build_map`) accepts a map set only as `base`, `us` or `[A-Z]{2}`, and refuses anything else as an unknown map set.
  `CZ-10` does pass `NAME` in `engine/setup/manifest.py` line 26, which allows hyphens, so a map id is fine where an
  index name is not.

### Prague inside Central Bohemia

Prague is an enclave: the Central Bohemian Region surrounds it completely. The `CZ-20` box already contains the whole
`CZ-10` box, so a Central Bohemian map would show Prague's streets, buildings and help points without any extra rule.
Address search is the different case, as in REGIONS-DE.md for Berlin: it reads one index per region, so a `CZ-20` map
would find Prague streets on the map but not Prague addresses unless the index is cut by box rather than by region.

### Boxes

Each box is the extent of the kraj's boundary in ČÚZK's **INSPIRE Administrative Units** product, national level
`Kraj`, in ETRS89 (EPSG:4258): `https://services.cuzk.gov.cz/gml/inspire/au/epsg-4258/1.zip`, 72,842,120 bytes, whose
Atom feed was updated on 17 November 2026. The file holds 6,258 `Obec`, 77 `Okres`, 14 `Kraj` and one `Stát`, and each
municipality names its district and each district its region through `upperLevelUnit`, so the counts below are read
from the hierarchy, not estimated from the geometry.

Every vertex was read in the file's own order (latitude, then longitude, which is what the GML axis order for
EPSG:4258 means), and each box was then widened by 0.15° and rounded outward to 0.01°, the margin `map_sets.state` uses
for US states.

| Code | ČÚZK code | Name | Okresy | Obce | Box (west, south, east, north) | Box with 0.15° margin |
|---|---|---|---|---|---|---|
| `CZ-10` | 19 | Hlavní město Praha (Prague) | 1 | 1 | 14.2244, 49.9419, 14.7068, 50.1774 | 14.07, 49.79, 14.86, 50.33 |
| `CZ-20` | 27 | Středočeský kraj (Central Bohemia) | 12 | 1,144 | 13.3965, 49.5013, 15.5355, 50.6189 | 13.24, 49.35, 15.69, 50.77 |
| `CZ-31` | 35 | Jihočeský kraj (South Bohemia) | 7 | 624 | 13.5360, 48.5518, 15.6042, 49.6211 | 13.38, 48.40, 15.76, 49.78 |
| `CZ-32` | 43 | Plzeňský kraj (Plzeň) | 7 | 501 | 12.4005, 48.9413, 13.8403, 50.1044 | 12.25, 48.79, 14.00, 50.26 |
| `CZ-41` | 51 | Karlovarský kraj (Karlovy Vary) | 3 | 134 | 12.0906, 49.8904, 13.3018, 50.4603 | 11.94, 49.74, 13.46, 50.62 |
| `CZ-42` | 60 | Ústecký kraj (Ústí nad Labem) | 7 | 354 | 12.9403, 50.0770, 14.6529, 51.0557 | 12.79, 49.92, 14.81, 51.21 |
| `CZ-51` | 78 | Liberecký kraj (Liberec) | 4 | 215 | 14.3426, 50.4719, 15.6326, 51.0232 | 14.19, 50.32, 15.79, 51.18 |
| `CZ-52` | 86 | Královéhradecký kraj (Hradec Králové) | 5 | 448 | 15.1042, 50.0384, 16.5855, 50.7805 | 14.95, 49.88, 16.74, 50.94 |
| `CZ-53` | 94 | Pardubický kraj (Pardubice) | 4 | 451 | 15.3628, 49.5721, 16.8674, 50.2076 | 15.21, 49.42, 17.02, 50.36 |
| `CZ-63` | 108 | Kraj Vysočina (Vysočina) | 5 | 704 | 14.8882, 48.9376, 16.4183, 49.8612 | 14.73, 48.78, 16.57, 50.02 |
| `CZ-64` | 116 | Jihomoravský kraj (South Moravia) | 7 | 673 | 15.5424, 48.6165, 17.6469, 49.6333 | 15.39, 48.46, 17.80, 49.79 |
| `CZ-71` | 124 | Olomoucký kraj (Olomouc) | 5 | 402 | 16.7120, 49.2688, 17.9181, 50.4494 | 16.56, 49.11, 18.07, 50.60 |
| `CZ-72` | 141 | Zlínský kraj (Zlín) | 4 | 307 | 17.1097, 48.8541, 18.4156, 49.5398 | 16.95, 48.70, 18.57, 49.69 |
| `CZ-80` | 132 | Moravskoslezský kraj (Moravia-Silesia) | 6 | 300 | 17.1465, 49.3926, 18.8593, 50.3280 | 16.99, 49.24, 19.01, 50.48 |

ČÚZK code is the `nationalCode` field of the AU file, which is not the ISO code and not the four-digit ČSÚ municipality
code; it is given only so the file can be matched after a download.

As a check, the outer edges of the country fall where Czechia's extreme points are usually given: 12.0906° E in the
Karlovy Vary region, 18.8593° E in Moravia-Silesia, 48.5518° N in South Bohemia and 51.0557° N in Ústí nad Labem. Those
four numbers are the maxima and minima of the same file the boxes came from, so this tests the arithmetic, not the
boundary. The `Okres` count matches the 76 districts plus Prague. Two things in the source are worth knowing: the Atom
feed states `žádné podmínky neplatí` ("no conditions apply") as its rights line while the product page names CC BY 4.0,
and the four outermost region boxes also give the country's own extent, so the kraj polygons run to the state border.

**Boxes that reach another country.** A state map holds every row inside its box, so a padded box that crosses a border
would pick up foreign rows from any source that has them. The padded boxes were tested against the Natural Earth 1:110m
outlines this repository ships in `web/world-context.json`, which is coarse and only indicative:

- `CZ-20`, `CZ-31`, `CZ-32`, `CZ-41`, `CZ-42` and `CZ-51` reach Germany; `CZ-20`, `CZ-51`, `CZ-52`, `CZ-53`, `CZ-71` and
  `CZ-80` reach Poland; `CZ-64`, `CZ-72` and `CZ-80` reach Slovakia; `CZ-31`, `CZ-32`, `CZ-63` and `CZ-64` reach Austria.
- `CZ-10` reaches no neighbour at all in that test.
- `CZ-32`'s Austrian hit is the test's own error, and the useful one to know about: Austria's 1:110m outline is drawn
  about 0.1° too far north there and that patch is Bavaria in reality, which puts a number on how far the outline can
  be trusted.
- `CZ-20` reaching Poland is the least certain of these: its north-east corner lies close to the Czech-Polish border, and
  at 1:110m the outline is too coarse to settle it.

The fix used in REGIONS-FR.md applies here too: cut by obec or okres outlines, and keep the box for display and the
spatial index. No region's box contains another region's, except Prague inside Central Bohemia, but neighbouring boxes
overlap widely.

### OpenStreetMap extracts

Geofabrik cuts Czechia into exactly the 14 kraje (opened), so each region has its own extract and no merge step is
needed. Sizes are from HEAD requests on the `-latest` files on 18 November 2026; the whole-country page said data up to
2026-11-13T21:22:20Z and a 908 MB `czech-republic-latest.osm.pbf`.

| Code | Extract (`https://download.geofabrik.de/europe/czech-republic/<name>-latest…`) | `.osm.pbf`, bytes | `-free.gpkg.zip`, bytes |
|---|---|---|---|
| `CZ-10` | `praha` | 45,153,187 | 54,698,497 |
| `CZ-20` | `stredocesky` | 182,113,855 | 293,825,711 |
| `CZ-31` | `jihocesky` | 97,268,666 | 186,442,923 |
| `CZ-32` | `plzensky` | 71,917,389 | 138,895,592 |
| `CZ-41` | `karlovarsky` | 30,885,544 | 58,434,888 |
| `CZ-42` | `ustecky` | 112,420,789 | 193,345,107 |
| `CZ-51` | `liberecky` | 47,137,109 | 82,155,846 |
| `CZ-52` | `kralovehradecky` | 60,357,319 | 108,367,660 |
| `CZ-53` | `pardubicky` | 55,378,128 | 99,989,927 |
| `CZ-63` | `vysocina` | 73,638,857 | 149,388,827 |
| `CZ-64` | `jihomoravsky` | 92,081,970 | 151,972,650 |
| `CZ-71` | `olomoucky` | 58,447,086 | 104,040,464 |
| `CZ-72` | `zlinsky` | 53,105,434 | 99,276,355 |
| `CZ-80` | `moravskoslezky` | 80,639,346 | 141,385,959 |

Two details, both from the pages opened above: Moravia-Silesia's file name is `moravskoslezky` on Geofabrik, with a
letter missing, and `tools/build_map.py` reads the free GeoPackage, which exists for all 14. The 14 `.osm.pbf` files add
up to 1,060,544,679 bytes, more than the 908 MB whole-country file; the difference is probably the overlap Geofabrik
keeps around each extract boundary, which was not measured.

## Sources, layer by layer

One national source covers most layers, and the INSPIRE copies are whole-country files rather than per-region ones, so
the "state by state" table of REGIONS-DE.md has no counterpart here.

| Layer (file) | US source today | Proposed for Czechia | Publisher | Licence | Checked |
|---|---|---|---|---|---|
| Terrain (`terrain.sqlite`) | USGS 3DEP, 1 arc-second | DMR 4G, 5 × 5 m grid, TIFF per map sheet; DMR 5G where the extra detail is wanted; Copernicus GLO-30 as fallback | ČÚZK; ESA / Airbus | CC BY 4.0; Copernicus licence | opened; Copernicus licence text not checked |
| Water (`water.sqlite`) | NHD | INSPIRE physical waters (HY-P) and hydrographic network (HY-NET), GeoPackage, whole state; OSM as supplement | ČÚZK; OSM contributors | CC BY 4.0; ODbL | opened |
| Dams | NID | OSM `waterway=dam` and reservoir areas | OSM contributors | ODbL | tag wiki search only |
| Crops (`crops.sqlite`) | USDA Cropland Data Layer | LPIS public export, SHP: farmer blocks, physical blocks, vineyards, landscape features; EuroCrops as alternative | Ministerstvo zemědělství; EuroCrops | no rights claimed; CC BY-SA 4.0 | opened |
| Buildings (`buildings.sqlite`) | Microsoft US footprints, OSM heights | ZABAGED, one GeoPackage for the whole state; INSPIRE buildings per obec; Overture or Microsoft as fill | ČÚZK; Overture; Microsoft | CC BY 4.0; ODbL; CDLA Permissive 2.0 | opened; Overture's Czech mix not checked |
| Places (`places.sqlite`) | GNIS, Census gazetteers, OSM | Geonames, GeoPackage, whole state; RÚIAN municipalities; OSM named places | ČÚZK; OSM contributors | CC BY 4.0; ODbL | opened |
| Addresses (`addresses/<code>.sqlite`) | Overture addresses | RÚIAN address places, CSV per obec; INSPIRE addresses; Overture (the same RÚIAN) as the route the tool already reads | ČÚZK; Overture | CC BY 4.0 | opened |
| Points of interest (`poi` rows) | OSM | OSM, as today | OSM contributors | ODbL | counts read |

Notes:

- **Terrain.** `tools/build_terrain.py` reads 1 arc-second GeoTIFFs from a fixed USGS path and writes zoom 4 to 12
  tiles. DMR 4G is a regular 5 × 5 m grid with a mean height error of 0.3 m in open terrain and 1 m under forest, and
  ČÚZK publishes it as TIFF as well as LAZ; one map sheet (BENE09) was 768,908 bytes. DMR 5G is a point cloud from
  airborne laser scanning (2009–2013, completed 2016) with 0.18 m and 0.3 m accuracy, published only as LAZ, so it needs
  a rasterisation step first. The INSPIRE elevation grid is one TIFF for the whole country, delivered as a ZIP
  (`INSPIRE_EL_GRID_3045.zip`, 7,685,616,237 bytes, opened); the uncompressed size is not stated on the feed, and
  neither is its grid spacing, so neither was checked. All three are bare-earth models, unlike Copernicus GLO-30,
  which is a surface model and would put the relief on the tree canopy and the roofs.
- **Water.** HY-P (454,051,469 bytes zipped) and HY-NET (194,208,037 bytes zipped) come as one file each, the first for
  water areas and the second for the network of watercourses. DIBAVOD, the water-management database that Czech
  hydrologists actually use, is **not proposed**: its pages grant no licence, which leaves all rights reserved by
  default, the project page asks anyone who wants to use the data to contact VÚV, and the data set is described as
  long-term unmaintained, with only a few layers still updated (opened). Its download page lists object groups from
  basic surface and ground water through protected zones and measuring points to flood areas, so the loss is real; a
  written permission has to be obtained before it can be used, and a private copy is defensible where a shared one
  would not be.
- **Crops.** LPIS is declared land use, so areas are exact sums rather than satellite pixels, and vineyards are their
  own entity (OPV). It is regenerated weekly, and the export page gives the URL pattern
  `https://mze.gov.cz/public/app/eagriapp/lpisdata/<date>-<code>-DPB-SHP.zip` with a list of available dates. Whether it
  has a class for orchards and berry plantations — the three kinds `tools/build_crops.py` keeps — was not established.
  EuroCrops would supply the harmonised taxonomy, but under CC BY-SA 4.0, which would make the crop layer share-alike.
- **Buildings.** ZABAGED comes as a single 5,805,826,649-byte GeoPackage in S-JTSK, or 6,742,892,709 bytes in
  ETRS89/TM33, dated 2026-10-04 (Atom feed, opened); buildings are among its 142 planimetric feature types, but the
  layer name was not confirmed. The GeoPackage is the format ČÚZK serves through that ATOM service, so it is one of the
  selected formats that are open data; other formats and media stay behind the e-shop. The INSPIRE buildings service
  splits the country into one file per obec, roughly 6,258 of them, which suits per-region builds badly. Neither
  carries building heights, so a 3D view would have no more than OSM's `height` and `building:levels`. Microsoft's
  index files Czechia under **two** region names, `CzechRepublic` and `Czechia` (88 rows over 49 distinct quadkeys in
  the 2026-11-12 `dataset-links.csv`), so a fill filter has to match both (opened).
- **Addresses.** The RÚIAN CSV per obec is the closest match for an address index: obec, městský obvod or městská část,
  část obce, ulice, type (č.p. or č.ev.), číslo domovní, číslo orientační and its letter, PSČ, S-JTSK coordinates, and a
  validity date; monthly. Overture's Czech rows come from the same register, so the existing
  `tools/build_addresses.py` route would need a country filter and the field changes below; whether that is enough was
  not tried.
- **Places.** Geonames gives standardised names for about 165 types of named object at the detail of the 1:10 000 base
  map, on a three-year revision cycle; the GeoPackage is 46,625,753 bytes (product page and Atom feed, opened).
  `places.sqlite` has no population column today, so a Czech place would carry its obec code and part of obec in
  `detail` (see "Still undecided").

## Help points

OSM is the only source proposed, and no national open list with coordinates was looked for. Counts from taginfo for
Geofabrik's Czechia extract, data until 17 November 2026 21:23 UTC (opened):

| Tag | Count | Notes |
|---|---|---|
| `amenity=pharmacy` | 2,562 | |
| `amenity=fire_station` | 6,776 | inflated, as in Germany: stations drawn as building and node |
| `amenity=police` | 1,152 | |
| `amenity=hospital` | 307 | |
| `amenity=drinking_water` | 1,510 | |
| `man_made=water_well` | 2,574 | |
| `emergency=water_tank` | 206 | |
| `emergency=drinking_water` | 0 | the German emergency-well kind; no Czech rows at all |
| `amenity=fuel` | 3,630 | Geofabrik files fuel in its `traffic` tables, and `tools/build_map.py` reads only the `pois` and `natural` tables, so `fuel` in its `POI_KEEP` never matches |
| `amenity=doctors` | 1,501 | |
| `amenity=clinic` | 595 | |
| `amenity=school` | 4,929 | in the data and in no layer today |
| `amenity=post_office` | 3,062 | in the data and in no layer today |
| `shop=supermarket` | 2,941 | |

`emergency=drinking_water` is the German emergency-well kind and is empty in Czechia. Its public-warning
network (sirens) and its emergency drinking-water points were not looked for, so their absence is not proven.

## Licence notes and attribution

- **CC BY 4.0** (ČÚZK, for everything in the tables above). ČÚZK's terms page (opened) asks for the source in a fixed
  form, **"ČÚZK, [rok]"**, where the year is that of the data used, but it scopes that format to **printed outputs and
  viewing services over the data** ("tiskové výstupy z těchto dat a prohlížecí služby nad těmito daty"); the metadata
  duty is tied to dissemination ("šířit"), as is the description of changes to a modified work. A private copy triggers
  none of it, while a published app is a viewing service over the data, so there the credit line belongs on screen, not
  only in a notice file. An English page (opened, "Version 1.0 - dated April 4, 2016") does publish a sentence:
  'data printouts and viewing services including these data must contain the source in the form "ČÚZK " where time
  information is related to the updatedness of the particular dataset.' It is stale — it names no CC BY 4.0, lists no
  ZABAGED, and drops the `[rok]` placeholder — so the Czech page is the one to quote.
- **ODbL** (OSM). As for the US map: credit "© OpenStreetMap contributors", say the data is under the ODbL, and offer a
  database built from it under the ODbL too. Nothing in the app answers article 4.6 today.
- **CC BY-SA 4.0** (EuroCrops, if used). Credit, link, note changes, and share adaptations under the same licence; that
  would travel with the crop layer into `crops.sqlite` (repository page opened; the licence text itself was not
  reopened).
- **CDLA Permissive 2.0** (Microsoft footprints, as a fill). Microsoft's README says data is "freely available for
  download and use under CDLA Permissive 2.0" (opened); Overture's buildings attribution now says the same data is
  "Licensed by Microsoft under the Open Database License", so the conflict is stated by both publishers rather than
  inferred from a list — the same conflict REGIONS.md records for Guyana and REGIONS-DE.md for Germany.
- **No rights claimed** (LPIS). The data.gov.cz record (opened) marks the work, the database and the sui generis right
  "Not copyrighted"/"Not protected", but the record cited is the **Prague district** dataset, not a national one, and
  its DPB/XML distributions are marked "Contains personal data". The Ministry's export page (opened) states no licence
  either, only the legal basis: § 3a of Act 252/1997 Sb. Neither statement is a grant, so nothing is owed either way; a
  general terms page for LPIS was not opened.
- **Copernicus WorldDEM-30**, only if GLO-30 is used. The collection page (opened) calls GLO-30 and GLO-90 "available
  worldwide with a free license" and carries the source notice verbatim — "© DLR e.V. 2010-2014 and © Airbus Defence
  and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved" — with a
  "produced using" variant for modified data; the notice falls due when data are communicated to the general public or
  distributed. The liability sentence REGIONS.md quotes is not on that page, and no clause granting redistribution was
  read, so the licence text is **not checked**: the ESA User Licence and its mission-specific annex were not opened.

These notices belong wherever the map already credits its sources, and in `THIRD_PARTY_NOTICES.md` at the repository
root, which is where REGIONS-DE.md and REGIONS-ES.md put them.

Two licence questions belong to the maintainers rather than to this proposal. First, CC BY 4.0 requires the metadata to
travel with the data, and a map pack holds SQLite files, not metadata records, so the pack would need a place to keep
them. Second, merging CC BY 4.0 points into the same `poi` table as OSM points probably makes a derived database under
the ODbL, which would put a share-alike condition on ČÚZK data that ČÚZK does not impose; one file or table per licence
avoids the question. That is a question, not legal advice.

## How addresses are written

- **Order.** Street, then house number, then postcode and town on the last line: "Karlova 12, 110 00 Praha 1". The town
  may carry the part of the municipality (*část obce*) after it, which is how Prague's districts are written ("Praha 1",
  "Praha 10"); in RÚIAN these are separate fields (obec, městský obvod/městská část, část obce), not a single string.
- **Postcode.** Five digits, written as three digits, one space, two digits: "110 00", "602 00". Česká pošta's page on
  addressing (opened) says exactly that ("Mezi trojčíslím a dvojčíslím PSČ je jedna mezera") and puts the postcode and
  the delivery place on the last line. Postcodes are assigned by postal routing, not by kraj, so they cannot stand in
  for a region code; how far the first digit falls together with a region was not checked.
- **Two house numbers.** A Czech address can carry a descriptive number (*číslo popisné*, unique within a část obce) and
  an orientation number (*číslo orientační*, a position within a street), written together as "1234/56" and often with a
  letter ("12a", "56/3b"). RÚIAN keeps them apart: `CisloDomovni`, `CisloOrientacni`, `CisloOrientacniPismeno`, with a
  type attribute for č.p. or č.ev. The formatted-address rows in the special RÚIAN address export follow decree
  359/2011 Sb.; neither that decree nor the export's data description was opened, so the connection is not checked.
- **Street words.** *ulice*, *náměstí* (square), *třída* (avenue), *nábřeží* (embankment), *sídliště*, *alej*; the type
  usually precedes the name ("náměstí Míru", "třída Masarykova"), unlike German or French usage. Diacritics are
  meaningful and are frequently dropped when typed in a hurry ("namesti", "Jindrisska").
- **What the current code does with that** (read in this repository on 18 November 2026):
  - `normalize()` in `engine/address_search.py` keeps only `a-z` and `0-9`, so "náměstí Míru" becomes `n m st m ru` and
    "Česká" becomes `esk`. Accents and diacritics need folding (á to a, č to c, ř to r, ě to e) on both sides, not
    deletion.
  - `is_address_query()` needs a digit first, so "Karlova 12, 110 00 Praha 1" is not treated as an address at all:
    Czech addresses start with the street.
  - `_parts()` takes a postcode only as the last word and only as five digits without a space, while the PSČ comes
    before the town and carries a space; "110 00" would arrive as two number words.
  - `tools/build_addresses.py` keeps only `country = 'US'`, cuts the postcode to five characters, and reads one
    `region` field; RÚIAN has no such field, and its obec code, part of obec and Prague district would each need a home.
  - The engine picks index files by a two-letter stem and applies US rules to any index it finds; there is no `meta`
    switch in this repository's code, unlike the trial described in REGIONS-FR.md.

## Still undecided

Each of these needs the maintainers' decision before any code changes.

1. **Codes.** Whether the map ids are the current numeric ISO codes (`CZ-10` … `CZ-80`), which fail the `[A-Z]{2}`
   checks for address indexes; or the obsolete letter codes (`CZ-PR`, `CZ-ST` …), which pass them but are no longer ISO,
   collide with `PR`, `MO` and `PA`, and include `US`; or a scheme of Lastbook's own. Whatever is chosen, how setup lists
   14 regions, and whether a region code may ever equal a US code, is part of the same decision.
2. **Address indexes, per region or per box.** Prague's addresses inside a Central Bohemian map are the reason the
   German proposal raises this. RÚIAN is published per obec, so an index could be cut by obec lists rather than by the
   0.15° box, which would also stop a border box from pulling in German or Austrian addresses.
3. **RÚIAN's licence conditions in practice.** "ČÚZK, [rok]", the metadata passed on, and a description of changes: where
   the year and the metadata live in a map pack, and whether merging with OSM data forces the ODbL on the result.
4. **Čísla popisná versus orientační.** Which number an address index stores and matches. A descriptive number alone is
   ambiguous outside its část obce; an orientation number alone is ambiguous between towns; a user types "Karlova 12"
   for one and "nábřeží 1234/56" for the other. Whether a query with one number falls back to the other, and which one
   the map card shows, are decisions.
5. **Terrain.** DMR 4G's TIFF sheets (5 m, bare earth, one file per SM5 sheet), DMR 5G's LAZ point clouds that need
   rasterising, or the single 7.7 GB INSPIRE ZIP, whose TIFF inside is of unknown uncompressed size.
   `tools/build_terrain.py` samples a lon/lat grid from a GeoTIFF's tie-point tags, so the first is the only one it can
   read at all; all three still need a conversion out of S-JTSK or TM33 before that.
6. **Crops.** LPIS as declared parcels (exact areas, weekly, no rights claimed) or EuroCrops (harmonised taxonomy,
   share-alike); whether LPIS has a class for orchards and berries, which is what the crop layer keeps today.
7. **DIBAVOD.** Whether to ask VÚV for written permission, or to leave the river network to ČÚZK's HY-NET and OSM.
8. **Help points.** Whether the kinds that have data and no layer (schools, post offices) get layers for Czechia first,
   and whether Czechia has national lists worth adding (sirens, defibrillators); neither was looked for.
9. **Places.** Whether `places.sqlite` gets a population column or keeps population and obec codes in `detail`, and how
   the část obce is shown next to the obec.

## What was checked, and what was not

- Opened on 18 November 2026: ČÚZK's terms page for spatial data and its open-data page, with the English version of
  the terms page ("Version 1.0 - dated April 4, 2016"); the product pages for DMR 5G, DMR 4G and Geonames; the INSPIRE
  ATOM service list, with the feeds for AU, AD, BU, HY-P, HY-NET, GN, EL-GRID and ZABAGED-GPKG, and their file lengths;
  the RÚIAN public-access page and the product page for the CSV address export per obec; the DIBAVOD project, structure
  and use pages; the LPIS export page; the LPIS record on data.gov.cz; the EuroCrops and Microsoft building-footprint
  repositories with Microsoft's `dataset-links.csv`; Overture's attribution page; the Copernicus DEM collection
  description on dataspace.copernicus.eu; Geofabrik's Czechia page; taginfo's Czechia site and API; Česká pošta's page
  on addressing; the Wikipedia copy of ISO 3166-2:CZ; OMG's ISO 3166-2 ontology for Czechia.
- Computed on 18 November 2026: the 14 boxes, from ČÚZK's INSPIRE AU file as described above; the okres and obec counts
  per region, from the same file's `upperLevelUnit` links; the 14 OpenStreetMap file sizes, by HTTP HEAD.
- Seen only in search results: the OSM wiki page for `waterway=dam`.
- Not checked: the ISO Online Browsing Platform, which answers HTTP 403, so the 15 November 2016 date for the letter
  codes rests on Wikipedia's copy of the change log; the text of CC BY 4.0, CC BY-SA 4.0, CDLA Permissive 2.0 and the
  Copernicus licence (all linked from the pages opened, and for Copernicus the ESA User Licence and its
  mission-specific annex were not opened at all); the LPIS attribute sheet and its crop classes; the ZABAGED layer name
  for buildings and whether ZABAGED or INSPIRE buildings carry heights; the grid spacing of the INSPIRE elevation grid
  and the uncompressed size of its ZIP; which sources make up Overture's Czech buildings theme and how many Czech
  address rows it holds; OSM coverage of addresses and buildings measured per region; national lists for sirens,
  defibrillators or emergency water; the Ministry of Agriculture's own terms page for LPIS; decree 359/2011 Sb. and the
  RÚIAN data description that the formatted-address rows come from.
