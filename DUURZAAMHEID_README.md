# Afzonderlijk dashboard duurzaamheid

Open **Alliander_SRS_Duurzaamheid.html** rechtstreeks in Chrome of Edge. Dit is een nieuw, zelfstandig bestand van circa 1,2 MB; het bestaande **Alliander_SRS_Dashboard.html** is niet gewijzigd. Alle CSS, JavaScript, de Excel-parser en uitsluitend de S1/S2/S3-data zijn ingebed. Internet en een backend zijn niet nodig.

Het overzicht bevat drie onderdelen, met cijfers en klikbare leveranciersgrafieken:

- **S-01 CO₂-reductie:** numerieke punten uit S1!F, ladder, SBTi en datakwaliteitsvlag.
- **S-02 Circulariteit:** gewogen circulair aandeel, met materiaalgewichten en correcties.
- **S-03 Mensenrechten:** volwassenheidsband, aanvullende score, vijf componenten en verbeteracties uit de bron.

Er zijn drie eenvoudige tabs: Overzicht, Brongegevens en Datakwaliteit. Er is geen informatie uit de kwaliteit-, logistiek-, techniek- of commerciële werkbladen opgenomen. Er is geen samengestelde duurzaamheidsscore en er zijn geen fictieve doelen of normen.

## Bron en mapping

De ingebedde bron is `data/SRS data & KPI berekening - QLTCS-v2.xlsx`. SHA-256: `8971153424581bfcc91f3d08856b9299727559febfd39241ac99bb95b9196179`. Het bronbestand is alleen gelezen.

| Tab | Mapping |
|---|---|
| S1 | Vanaf rij 7, kopregel `Naam` overgeslagen. A leverancier; D CO₂-ladder; E SBTi; F punten; G datakwaliteitsvlag. B/C staan uitsluitend in de oorspronkelijke bronrij. |
| S2 | Vanaf rij 8. A boekmaand; B leverancier; C contract; D circulair gewicht; E totaalgewicht; F bronfractie. |
| S3 | Vanaf rij 12. A leverancier; B:F vijf C-componenten; G aanvullende score, inclusief tekst zoals `70/100`; H leidende volwassenheidsband; I verbeterstappen. |

Python en de lokale upload herkennen S1/S2/S3 ongeacht hoofdletters of omringende spaties. Een bestand met uitsluitend deze drie werkbladen is voldoende; overige werkbladen worden niet ingelezen. De voorgeschreven kolomposities en startrijen blijven vereist.

## Berekeningen en betrouwbaarheid

**S1:** gemiddelde over unieke leveranciers met een numerieke, eenduidige score in F. Nul is geldig. Identieke dubbele scores tellen één keer. Bij verschillende scores voor dezelfde leverancier, ook ontbrekend versus ingevuld, wordt de leverancier uitgesloten van het gemiddelde. Ontbrekende leveranciers worden niet als score-identiteit gebruikt. Brongegevens houdt alle oorspronkelijke rijen zichtbaar.

**S2:** `100 × SOM(D) / SOM(E)` over de geselecteerde records met twee numerieke gewichten. Negatieve waarden en nulgewichten blijven aanwezig. Een totale noemer van nul levert geen score. Percentages in F zijn alleen broncontrole; ze worden niet gemiddeld. De bron specificeert hier geen gewichtseenheid; het dashboard verzint geen kilogramlabel. Regels worden niet ontdubbeld alleen omdat ze dezelfde leverancier hebben: het zijn materiaal-/transactierecords.

**S3:** H bepaalt de classificatie. Bij meerdere leveranciers wordt het aantal per tekstuele band getoond; er is geen numerieke codering of gemiddelde van banden. G en B:F zijn aanvullende details. Exact gelijke duplicaten tellen één keer; verschillen in band, score, componenten of verbeterstappen worden als conflict uitgesloten van de bandverdeling. Componenten worden niet op eigen initiatief herwogen.

Excel-fouten en ontbrekende formule-uitkomsten worden expliciet bewaard en niet als getal geïnterpreteerd. De parser rekent Excel-formules niet uit. Sla een bijgewerkt bestand daarom vooraf op met berekende uitkomsten.

## Filters, namen en import

Het leverancierfilter is doorzoekbaar en ondersteunt meerdere leveranciers. Maand en contract gelden uitsluitend voor S2. S1 en S3 hebben geen betekenisvolle periode of contractkolom. De S2-bron bevat geen volledig boekjaar; daarom wordt geen fictief jaarfilter aangeboden.

Naamnormalisatie is beperkt tot hoofdletters, spaties en leestekenvarianten; cijfers en voorloopnullen in tekstcodes blijven behouden. De eerder bevestigde Prysmian-varianten worden als Prysmian Group weergegeven. Andere Group-, Holding- of landnamen worden niet geraden of samengevoegd. Oorspronkelijke namen blijven zichtbaar bij de bronrecords. Er worden geen instellingen of koppelingen uit het andere dashboard stilzwijgend ingelezen.

Excel laden vervangt de data alleen in het huidige venster, na controle dat alle drie tabs aanwezig zijn. Een afgewezen import behoudt de vorige data. Het bestand wordt niet verstuurd of gewijzigd. Heropenen herstelt de ingebedde bron.

Brongegevens ondersteunt zoeken, sorteren, pagineren, rijdetails en CSV-export van alle gefilterde zoekresultaten. CSV gebruikt UTF-8 BOM en puntkomma’s, met bescherming tegen formule-injectie. Datakwaliteit rapporteert het volledige ingelezen bestand, onafhankelijk van filters. Grafieken tonen aanvankelijk maximaal twaalf leveranciers; Meer tonen en het leverancierfilter maken de overige resultaten bereikbaar.

## Bouwen en testen

```sh
python build_sustainability.py 'data/SRS data & KPI berekening - QLTCS-v2.xlsx'
NODE_PATH=/workspace/scratch/srs-tools/node_modules node test_sustainability.cjs
```

`build_sustainability.py` leest uitsluitend S1/S2/S3 met openpyxl in formule- en uitkomstenmodus en schrijft uitsluitend het nieuwe dashboard. De oorspronkelijke dashboardbuilder blijft behouden.

`test_sustainability.cjs` controleert de uitkomsten tegen de onafhankelijke Python-referentie: S1 **5,0486787204450625** punten over **2.876** unieke leveranciers; S2 **10,003548761074848%**; S3 **7** leveranciers. De test controleert ook nul versus ontbrekend, dubbele en conflicterende scores, gewogen percentages met negatieve en nulgewichten, filterscope, bronrecords, CSV, complete en S-only Excel-upload, ongeldige import, mobiele/tabletweergave en afwezigheid van netwerkverzoeken en JavaScript-fouten. Zie `sustainability_test_report.txt`.

De browsertest gebruikt Chromium. Het bestand gebruikt standaard HTML/JavaScript voor actuele Chrome en Edge; er is geen afzonderlijke Microsoft Edge-uitvoering gedaan. De lokaal ingebedde parser is SheetJS CE 0.18.5, Apache 2.0; licentie: `vendor/XLSX-LICENSE`.
