# Alliander Supplier Rating System

Open **Alliander_SRS_Dashboard.html** rechtstreeks in Edge of Chrome. Dit is het complete, zelfstandige dashboard: de dataset, Excel-parser (SheetJS CE 0.18.5, Apache 2.0), CSS en JavaScript zijn ingebed. Internet, installatie en een webserver zijn voor gebruik niet nodig. Het bestand bevat leveranciers- en meldingsgegevens; deel het als brondata.

## Gebruik

Vijf pagina's: management, kwaliteit, duurzaamheid, leveranciersvergelijking en datakwaliteit. Kies meerdere leveranciers via de zoekbare keuzelijst. Een lege selectie betekent alle leveranciers. Grafiekbalken openen bronrecords; de berekeningen staan hieronder beschreven. Tabellen ondersteunen zoeken, sorteren, rijdetails en CSV-export (alle gefilterde zoekresultaten, maximaal 500 rijen zichtbaar). Download-CSV gebruikt puntkomma's, UTF-8 BOM en beschermt tegen formule-injectie. Ontbrekende gegevens verschijnen als **Geen data**, geldige nullen blijven nul.

**Excel laden** vervangt de dataset alleen in het huidige venster, zonder upload naar een server. Heropenen herstelt de ingebedde brondata. Een bijgewerkt bestand moet dezelfde tabbladen en kolomstructuur gebruiken. Sla Excel-formules eerst op met actuele berekende resultaten: de parser voert geen Excel-formules uit. Voor een nieuw zelfstandig HTML-bestand met bijgewerkte ingebedde data: gebruik het bouwscript hieronder.

## Mapping en berekeningen

| KPI / bron | Mapping en verwerking |
|---|---|
| Q2&3 vanaf rij 2 | A aanmelding; B nummer; D soort; F leverancier; G omschrijving; O contractmanager; P contract; R status; S/T categorie/subcategorie; AE afmelding; AF/AG alleen bronvergelijking. AB/AC/AD blijven in ruwe bronrecords beschikbaar. |
| Q-02 | Alleen `Klacht`, status `5. Afgemeld`, geldige A en AE. Gemiddelde `(AE-A)` in kalenderdagen inclusief kloktijd, één decimaal. Aantal afgesloten klachten erbij. |
| Q-03 | Alleen `Klacht`, status niet `5. Afgemeld`, geen geldige AE en geldige A. Kalenderleeftijd tot de actuele kloktijd in Europe/Amsterdam, elke minuut bijgewerkt. De grafiek Q3 toont het gemiddelde aantal dagen per leverancier. |
| S1 | Rij 7 bevat daadwerkelijk de kop; data vanaf rij 8. A leverancier; B/C matchtypes; D ladder; E SBTi; F opgeslagen punten; G datakwaliteit. Unieke leveranciers met numerieke scores worden gemiddeld. |
| S2 vanaf rij 8 | A boekmaand; B leverancier; C contract; D circulair gewicht; E totaalgewicht; F bronfractie. `100 × SOM(D) / SOM(E)`, inclusief negatieve gewichten, alleen rijen met twee numerieke gewichten. Noemer nul = geen score. |
| S3 vanaf rij 12 | A leverancier; B:F componenten; G score (ook tekst `70/100`); H leidende tekstuele band; I verbeterstappen. Bij meerdere leveranciers: verdeling over banden, geen categorie-gemiddelde. |

Datumbereik filtert uitsluitend Q op aanmelddatum. **Boekmaand S2** filtert uitsluitend circulariteit: de bron bevat `01` t/m `06`, zonder jaar; er wordt geen jaar verzonnen. Contract filtert Q en S2. S1 en S3 volgen uitsluitend de leverancierselectie. Kalenderdagen zijn verschillen tussen lokale kloktijden; een dag tijdens een zomer-/wintertijdwisseling telt als één kalenderdag.

Leveranciers worden uitsluitend gekoppeld door volledige naam na trimmen, samenvoegen van overtollige spaties en hoofdletterongevoelige vergelijking. Voorloopnullen blijven behouden; geen fuzzy matching of afgeleide codes. `(leeg)` wordt als ontbrekend behandeld. Records zonder leverancier tellen wel in algemene Q/S2-totalen, maar worden niet aan een leverancier toegeschreven.

## Validatie en bekende bronbeperkingen

- Import: 5.300 Q-records, 4.597 S1-records inclusief 254 naamloze formule-rijen, 92 S2-records, 7 S3-records.
- 2.177 klachten: 2.016 geldig afgesloten en 161 openstaand. Q-02 **11,9409405313 dagen**; S-02 **10,0035487611%**.
- S1: 1.463 extra records voor herhaalde leveranciersnamen; identieke scores tellen één keer. Vier leveranciers hebben conflicterende punten en krijgen geen geaggregeerde S1-score. 2.876 unieke leveranciers met geldige, eenduidige score; gemiddelde **5,0486787204 punten**. Naamloze nulregels worden niet als leverancier geteld.
- S2: twee records met negatieve gewichten, zes met totaalgewicht nul en zes Excel-fouten in F. Negatieve records zijn behouden; F-fouten blokkeren een geldige D/E-berekening niet. De `(leeg)`-rij blijft aanwezig in de importcontrole.
- S3: scores 70, 70, 70, 60, 60, 40 en 10; vijfmaal `Ontwikkeld publiek aantoonbaar`, éénmaal `Basis publiek aantoonbaar`, éénmaal `Beperkt publiek aantoonbaar`.
- Geen dubbele meldingnummers in deze bron. Toekomstige dubbelingen worden zichtbaar gemeld, niet automatisch verwijderd: zonder bronbeslissing is niet te bepalen welke melding behouden moet blijven. Bij conflicterende S3-duplicaten wordt evenmin een band gekozen.
- AF bevat geen vergelijkbare numerieke duren. Van 2.016 AG-waarden wijken 1.080 meer dan één minuut af van AE−A. AG is daarom geen rekenbasis. Zie `validation_report.json`.
- Negatieve klachtduur en toekomstige aanmeldingen worden als ongeldige berekeningen gemeld en uitgesloten. Ontbrekende afmelddatum is op zichzelf geen fout bij openstaande klachten.
- De vormgeving gebruikt het groen, oranje en bordeauxrood van het aangeleverde Alliander-logo. Benaderde kleuren: groen `#62892f` / `#719a34`, donkergroen `#344b1c`, oranje `#ef7d00` en bordeauxrood `#8c171b`. Dit zijn visuele benaderingen van de afbeelding, geen geverifieerde officiële kleurcodes. De productnaam is **Supplier Rating System**.
- Gecontroleerd met Chromium (desktop en mobiel), inclusief netwerkblokkering voor externe verzoeken en browser in een andere tijdzone. Geen afzonderlijke uitvoering in Microsoft Edge. Rechtstreekse `file://`-navigatie is door het beheerde testbrowserbeleid geblokkeerd; de tests gebruikten een lokale statische server. Het product zelf gebruikt geen serverfunctionaliteit.

## Reproduceren met Python

```sh
cd /workspace/SRS-HTML
python -m venv /workspace/scratch/srs-venv
/workspace/scratch/srs-venv/bin/pip install --cache-dir /tmp/srs-pip-cache -r requirements.txt
/workspace/scratch/srs-venv/bin/python build_dashboard.py 'data/SRS data & KPI berekening (2).xlsx'
/workspace/scratch/srs-venv/bin/python validate_data.py 'data/SRS data & KPI berekening (2).xlsx'
```

Het bouwscript leest zowel formules als opgeslagen uitkomsten met openpyxl, valideert de tabbladen en embedt JSON veilig in het template. Het bronbestand wordt alleen gelezen. De SHA-256 van de ongewijzigde bronkopie is `baf8cb5c82ce65dfa7334892ec1d70a880c3ca75cbc96fbf017f03439af32369`.

`validate_data.py` is een onafhankelijke Python-controle van de oorspronkelijke aangeleverde dataset (referentieaantallen zijn assertions in deze controle, niet in dashboardberekeningen). `vendor/XLSX-LICENSE` bevat de licentie van de ingebedde parser. Het HTML-bestand is het enige benodigde bestand voor eindgebruikers.

De functionele browsertest staat in `test_browser.cjs` en gebruikt Playwright 1.56.1 met `/usr/bin/chromium`. In deze cloudomgeving: voer `NODE_PATH=/workspace/scratch/srs-tools/node_modules node test_browser.cjs` uit. De test levert het HTML-bestand via lokale browserinterceptie aan en heeft geen serverproces nodig. De test controleert de KPI's onafhankelijk tegen `validation_report.json`, alle vijf pagina's, zoek/sorteer/CSV, meervoudige selectie, alle filters, drilldown, afwezigheid van de verwijderde KPI-kaarten, herimport, geldige nul/conflicterende scores, negatieve en nulgewichten, mobiele breedte en het ontbreken van externe verzoeken. `browser_test_report.txt` bevat de uitkomst. Browserafhankelijkheden zijn uitsluitend voor ontwikkeling; het eindproduct bevat ze niet.

Het dashboard toont uitsluitend Q-02, Q-03, S-01, S-02 en S-03 als prestatie-indicatoren. De KPI-kaarten en aanvullende grafieken met klachten per maand en statusverdelingen zijn verwijderd. Filters, KPI-uitsplitsingen, bronrecords en technische datakwaliteitscontroles blijven beschikbaar.

De twee kwaliteitsgrafieken heten **Q2 – Doorlooptijd afgesloten klachten per leverancier** en **Q3 – Gemiddelde leeftijd openstaande klachten per leverancier**. Beide tonen gemiddelden in dagen met één decimaal. De leeftijdsgroepen zijn vervangen door Q3-gemiddelden. Drilldown bevat uitsluitend de bijbehorende afgesloten (Q2) of openstaande (Q3) klachten.
