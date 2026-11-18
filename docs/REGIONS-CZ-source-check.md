# Czechia: an independent check of the sources in REGIONS-CZ.md

This note tests seven factual and licence claims made in [REGIONS-CZ.md](REGIONS-CZ.md) against the publishers' own
pages. It was written on 18 November 2026 and changes nothing else in the repository. Every page below was opened in a
browser and read; search results were used only to find the pages, never as evidence.

The question behind it is narrower than the proposal: the library is for one person's own use and is not going to be
distributed. So for each licence the note says which duties are triggered by *sharing* the data and which are not
triggered at all by a private copy. That distinction is the same in all four open licences below: CC BY 4.0, CC BY-SA
4.0, ODbL and the Copernicus DEM terms attach their obligations to distribution or public communication, not to
private use.

Verdicts: **confirmed** (the publisher's page says it), **partly** (right in substance, wrong or missing in detail),
**wrong** (the page says otherwise), **unverified** (the page could not be read, or no publisher source was found).

| # | Claim in REGIONS-CZ.md | Verdict | What the publisher actually says (verbatim) | URL | Personal use vs distribution |
|---|---|---|---|---|---|
| 1 | ČÚZK open data are CC BY 4.0 and ask for the source in the form "ČÚZK, [rok]" | **confirmed**, but the duty is narrower than the document implies | "poskytuje prostorová data spadající do kategorie otevřený dat (včetně metadat) bezúplatně na základě licence Creative Commons CC-BY 4.0"; "**tiskové výstupy z těchto dat a prohlížecí služby nad těmito daty** musí obsahovat uvedení zdroje ve formátu: „ČÚZK, [rok]“, kde časové údaje jsou vztaženy k aktuálnosti použitého datového souboru"; "šířit údaje lze pouze společně s příslušnými metadaty"; "v případě šíření upraveného díla, uvést popis úpravy" | https://cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx | The format is required of *print outputs and viewing services over the data*, and the metadata rule is tied to "šířit" (disseminating). CC BY itself is conditional: "**Pokud Sdílíte** Licencovaný obsah (včetně jeho upravené podoby) musíte: …" (reproduced on the same page). A private, undisclosed copy triggers nothing. A published app is a viewing service over the data — the credit line belongs on screen, not only in a notice file. |
| 1b | "no English attribution sentence is published, so there is nothing to quote beyond the format itself" | **wrong** | An English page exists and does publish one, in an older wording: "data printouts and viewing services including these data must contain the source in the form “ČÚZK ” where time information is related to the updatedness of the particular dataset." That page is "Version 1.0 - dated April 4, 2016", does not name CC BY 4.0, does not list ZABAGED (it predates July 2023), and drops the `[rok]` placeholder | https://cuzk.gov.cz/English/Practical-Information/Conditions-of-Provision-for-Spatial-Data-and-Netwo/Conditions-for-CUZK-Spatial-Data-Provision.aspx | Same effect as 1, but the English page is stale: quote the Czech page, not the English one, and say so. |
| 2 | ZABAGED, DMR 4G/5G, RÚIAN, Geonames and INSPIRE copies are free open data from 1 July 2023 (RÚIAN from 2012) | **partly** — dates right for ZABAGED, wrong grouping for INSPIRE, "free" needs the format caveat | "ČÚZK … začal v roce 2012 poskytovat údaje RÚIAN jako otevřená data a současně rozhodl, že podmnožina těchto údajů, představující témata „Katastrální parcely“, „Budovy“, „Adresy“ a „Územní členění“ směrnice INSPIRE bude rovněž poskytována jako otevřená"; "katastrální mapy v digitální formě … od 1. 1. 2014"; "**Od 1. 7. 2023** navíc zveřejňuje Zeměměřický úřad údaje ZABAGED®, ortofota České republiky, státního mapového díla, databázového souboru geografického názvosloví a bodových polí bezplatně jako otevřená data"; "Souborová data všech produktů ZABAGED® - výškopis jsou od 1. 7. 2023 poskytována **ve vybraných formátech** stahovacími službami ATOM jako otevřená data, bezplatně, na základě licence Creative Commons CC BY 4.0"; DMR 4G is "ve formě výšek diskrétních bodů v pravidelné síti (5 x 5 m) bodů s úplnou střední chybou výšky 0,3 m v odkrytém terénu a 1 m v zalesněném terénu" | https://cuzk.gov.cz/Uvod/Produkty-a-sluzby/Otevrena-data/Otevrena-data-zakladni-informace.aspx · https://geoportal.cuzk.gov.cz/Default.aspx?mode=TextMeta&text=vyskopisZBG&side=vyskopis&menu=30&head_tab=sekce-02-gp · https://geoportal.cuzk.gov.cz/Default.aspx?lng=CZ&mode=TextMeta&text=dSady_zabaged&side=zabaged&menu=24&head_tab=sekce-02-gp | No licence question here: everything is CC BY 4.0, so the personal/distribution split is the one in row 1. But only *selected formats* are open — "K objednání dat v dalších formátech a jiných formách distribuce můžete využít aplikaci eshop" — so which format a build uses is a licence-relevant choice, not a technical one. |
| 3 | DIBAVOD (VÚV TGM) states no licence and is long-term unmaintained | **confirmed** | "UPOZORNĚNÍ – DIBAVOD je z důvodů nefinancování jeho správy a aktualizace **dlouhodobě neaktualizovaný zdroj** vodohospodářských dat. Aktualizováno je jen několik vybraných datových sad."; "V případě zájmu o využití dat prosím kontaktujte Mgr. Aleše Zbořila…". No licence, terms-of-use or rights sentence on the project, use, object-list or structure pages; the footer reads "© 2025 Výzkumný ústav vodohospodářský T.G.Masaryka, v.v.i." | https://www.dibavod.cz/ · https://www.dibavod.cz/20/vyuziti-dat-dibavod.html · https://www.dibavod.cz/27/struktura-dibavod.html | "No licence" is not "free": with no grant, the default is all rights reserved, and the contact line is an invitation to ask, not a permission. A copy made for one's own use falls under the private-use exception of the Copyright Act (§ 30), so a personal library is defensible; putting the derived `water.sqlite` into anything handed to someone else would need VÚV's written permission. |
| 4 | LPIS (MZe) is recorded on data.gov.cz as "Not copyrighted / NOT protected" | **confirmed**, with two caveats | Per distribution, the record shows: "Terms of use — **Not copyrighted** (Copyrighted work) · **Not copyrighted** (Copyrighted database) · **Not protected** (Sui generis db rights)". The title of the record is "LPIS - **district Hlavní město Praha**". MZe's own export page gives the legal basis: "Export obsahuje data, které jsou veřejnosti dostupná na základě zákona č. 252/1997 Sb., o zemědělství § 3a." That page states no licence either | https://data.gov.cz/dataset?iri=https://data.gov.cz/zdroj/datov%C3%A9-sady/00020478/9c2678534cc534ebb99af3b449119244 · https://mze.gov.cz/public/portal/mze/farmar/LPIS/uzivatelske-prirucky/prirucky-pro-verejny-lpis/export-dat-lpis.html | Nothing is claimed, so nothing is owed either way. The caveat is scope: the row cited is the Prague district dataset, and the DPB/XML distributions of the same record are marked "**Contains personal data**" — a data-protection question, not a copyright one, and it does not arise at all for a private library. |
| 5a | Overture Maps contains addresses for Czechia | **confirmed** | Attribution page, Addresses → Czechia: "Contains data from Český úřad zeměměřický a katastrální (ČÚZK). Available under CC BY 4.0. Accessed: 2026-11-17." The theme page says Overture "maintains over 475 million address point entities" built from "over 175 sources" | https://docs.overturemaps.org/attribution/ · https://docs.overturemaps.org/guides/addresses/ | Overture hands the Czech rows back under the same CC BY 4.0 as ČÚZK, so nothing changes in practice; the ODbL applies to the parts that come from OSM. Taking addresses from Overture rather than from ČÚZK directly does not simplify the attribution. |
| 5b | Microsoft building footprints include `CzechRepublic` | **confirmed**, with a gotcha | README: "The data is freely available for download and use under CDLA Permissive 2.0." and "This data is licensed by Microsoft under the CDLA Permissive 2.0." The current index (`dataset-links.csv`, dated 2026-11-12) has 225 distinct regions and **88 rows for Czechia — but under two region names**: `CzechRepublic` (47 rows) and `Czechia` (41 rows), covering 49 distinct quadkeys, about 443 MiB listed in total | https://github.com/microsoft/GlobalMLBuildingFootprints · https://bfppub.blob.core.windows.net/$web/2026-11-12/dataset-links.csv | CDLA Permissive 2.0 puts no condition on the result — the only duty is not to sue over patents. Nothing changes between private and distributed use. The doc's remark that Overture lists the same data under the ODbL is also right: Overture's Buildings section says "Global ML Building Footprints. **Licensed by Microsoft under the Open Database License.**" Two publishers, two licences for one dataset. |
| 6 | The Copernicus DEM GLO-30 licence allows redistribution with the notices quoted | **partly** — one notice is verbatim on the ESA page, the second is not there, and no clause granting redistribution was read | "The GLO-30 and GLO-90 datasets are available worldwide with a free license."; "**When communicating to the General Public or distributing** the Copernicus WorldDEM-30 (GLO-30), the User shall inform the General Public of the source by using the following notice: © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved"; adapted: "produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 … all rights reserved". No sentence containing "liability" appears on that page | https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM | The notice is due only "when communicating to the General Public or distributing". A private terrain tile set owes nothing; a shared map pack owes both the source notice and, if the DEM was resampled or merged, the "produced using" notice. Note that permission to distribute is *implied* by these obligations, not stated in a granting clause on this page; the ESA User Licence and the Mission Specific Annex were not read. |
| 7a | ISO 3166-2:CZ uses the numeric codes CZ-10 … CZ-80 for the 14 regions | **confirmed** (secondary standards source; ISO's own platform unreachable) | OMG's ISO 3166-2 ontology for Czechia, which reproduces the ISO list, defines exactly 14 first-level units — `CZ-10` "Praha, Hlavní město", `CZ-20` "Středočeský kraj", `CZ-31` "Jihočeský kraj", `CZ-32` "Plzeňský kraj", `CZ-41` "Karlovarský kraj", `CZ-42` "Ústecký kraj", `CZ-51` "Liberecký kraj", `CZ-52` "Královéhradecký kraj", `CZ-53` "Pardubický kraj", `CZ-63` "Kraj Vysočina", `CZ-64` "Jihomoravský kraj", `CZ-71` "Olomoucký kraj", `CZ-72` "Zlínský kraj", `CZ-80` "Moravskoslezský kraj" — and contains **no** `CZ-PR` or other letter code | https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-CZ.ttl | Not a licensing question. |
| 7b | the letter codes were withdrawn on 15 November 2016 | **unverified** | ISO's Online Browsing Platform returns **HTTP 403** to this host and to a real browser session (Cloudflare "security verification"), so the change log could not be read at the source. The only statement of the 2016-11-15 date found is Wikipedia's reproduction of that change log, which the document already cites — i.e. the document is its own evidence | https://www.iso.org/obp/ui/#iso:code:3166:CZ (blocked) · https://en.wikipedia.org/wiki/ISO_3166-2:CZ | Not a licensing question, but the report's "opened" mark should not stand for a fact whose only source is a wiki. |

## The one thing the document gets substantively wrong

**The scope of the attribution duty.** REGIONS-CZ.md says ČÚZK "asks for the source in a fixed form, **"ČÚZK, [rok]"**",
full stop. ČÚZK scopes that format to "tiskové výstupy z těchto dat a prohlížecí služby nad těmito daty" — print
outputs and viewing services — and scopes the metadata duty to dissemination ("šířit"). Since the app *is* a viewing
service over the data, the obligation still lands on a published build; it just does not land on a private copy, and
the document's phrasing makes it sound as though every use carried it.

**And the English page.** The claim that "no English attribution sentence is published" is false. There is one, in a
2016 version of the page that predates both CC BY 4.0 being named and ZABAGED becoming open, and it prints the format
as "ČÚZK " without the year placeholder. That divergence is worth recording — an English reader who quotes the English
page will quote a stale document.

## What has to change in REGIONS-CZ.md

1. **Line 224–228 (CC BY 4.0 note).** Scope the "ČÚZK, [rok]" format to print outputs and viewing services, as the
   Czech page does, instead of presenting it as a general condition. Delete "no English attribution sentence is
   published" and replace it with the English wording plus its 2016 date and its missing year placeholder.
2. **Line 27–29 and 224.** Split the 1 July 2023 date from the INSPIRE themes: Katastrální parcely, Budovy, Adresy and
   Územní členění (and the digital cadastral map from 1 January 2014) have been open since 2012, not since 2023. The
   2012 date for RÚIAN is right, but the page says "v roce 2012", not 1 July.
3. **Line 26 and the layer table.** Add "ve vybraných formátech" wherever ZABAGED, DMR 4G/5G or Geonames are called
   free: only selected formats are open data, the rest is still sold through the e-shop. This matters for the
   proposal, because it decides whether the 5.8 GB ZABAGED GeoPackage and the DMR sheets are downloadable at all.
4. **Line 34 and 176–180 (DIBAVOD).** "Carries no licence at all" should become "grants no licence; all rights
   reserved by default, permission on request (contact on the project page)" — the difference decides whether a
   derived `water.sqlite` may ever leave the machine. Keep the "long-term unmaintained" quote, which is exact.
5. **Line 236–237 (LPIS).** Say that the cited data.gov.cz record is the **Prague district** dataset, not a national
   one, and add MZe's own basis for publishing — § 3a of Act 252/1997 Sb., quoted on the export page. Note that the
   DPB/XML distributions on the same record are marked "Contains personal data".
6. **Line 233–235 (Microsoft).** The quote is accurate against the current README; add that Overture's buildings
   attribution now explicitly says Microsoft's footprints are "Licensed by Microsoft under the Open Database
   License", so the conflict is stated by both sides, not inferred. Add the naming trap as well: the 2026-11-12 index
   files Czechia under both `CzechRepublic` and `Czechia`, so the "fill" filter in REGIONS-CZ.md line 161 has to match
   both, and the two sets share 39 quadkeys.
7. **Line 238 (Copernicus).** "The two notices quoted in REGIONS.md" is only half supported by the ESA page: the
   source notice is there verbatim (with a "produced using …" variant for modified data), the liability sentence is
   not. Either source the liability sentence or drop it, and record that the granting clause itself was not read.
8. **Line 44–50 and 317 (ISO codes).** Replace "read from Wikipedia's copy … not checked against the ISO site" with
   the check that was possible — OMG's ISO 3166-2 ontology confirms the 14 numeric codes and the absence of the
   letter codes — and mark the 15 November 2016 date as unverified, because the ISO platform answered HTTP 403.
9. **Line 12–21 and 305–321 ("What was checked").** The marks are broadly honest, but three of them need downgrading:
   the ISO codes (row 7b), the Copernicus licence (row 6, the licence text itself was never read), and the English
   ČÚZK page, which was not opened at all.

## What the personal-versus-distribution split comes to

For a library that stays on one machine, none of these licences imposes anything: CC BY, CC BY-SA and ODbL attach
their duties to sharing, and the Copernicus notices are due only when data are distributed or communicated to the
public. Two exceptions and one trap:

- **DIBAVOD is not open at all.** No licence means no permission; a private copy is covered by the private-use
  exception, redistribution is not.
- **The ODbL and CC BY-SA travel with a published build.** Merging ČÚZK points into an OSM-derived database, or using
  EuroCrops in `crops.sqlite`, would put a share-alike condition on the result — but only once the result is
  distributed. The document's worry at line 240–244 is therefore a distribution question, not a build question.
- **If the library is ever handed to someone else** — even one person — the duties switch on together: "ČÚZK, 2026"
  visible in the app, the metadata passed on, the changes described, the Copernicus notice, and the ODbL or CC BY-SA
  notice for anything derived from OSM or EuroCrops. Keeping a provenance record per layer now costs nothing and is
  the only thing that cannot be reconstructed later.
