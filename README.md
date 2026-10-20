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

Leveranciers worden gekoppeld door volledige naam na trimmen, samenvoegen van overtollige spaties en hoofdletterongevoelige vergelijking, aangevuld met expliciet beheerde naamkoppelingen. Voorloopnullen blijven behouden; geen fuzzy matching of afgeleide codes. `(leeg)` wordt als ontbrekend behandeld. Records zonder leverancier tellen wel in algemene Q/S2-totalen, maar worden niet aan een leverancier toegeschreven.

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
/workspace/scratch/srs-venv/bin/python build_dashboard.py 'data/SRS data & KPI berekening - contractmapping.xlsx'
/workspace/scratch/srs-venv/bin/python validate_data.py 'data/SRS data & KPI berekening (2).xlsx'
```

Het bouwscript leest zowel formules als opgeslagen uitkomsten met openpyxl, valideert de tabbladen en embedt JSON veilig in het template. Het bronbestand wordt alleen gelezen. De SHA-256 van de ongewijzigde bronkopie is `baf8cb5c82ce65dfa7334892ec1d70a880c3ca75cbc96fbf017f03439af32369`.

`validate_data.py` is een onafhankelijke Python-controle van de oorspronkelijke aangeleverde dataset (referentieaantallen zijn assertions in deze controle, niet in dashboardberekeningen). `vendor/XLSX-LICENSE` bevat de licentie van de ingebedde parser. Het HTML-bestand is het enige benodigde bestand voor eindgebruikers.

De functionele browsertest staat in `test_browser.cjs` en gebruikt Playwright 1.56.1 met `/usr/bin/chromium`. In deze cloudomgeving: voer `NODE_PATH=/workspace/scratch/srs-tools/node_modules node test_browser.cjs` uit. De test levert het HTML-bestand via lokale browserinterceptie aan en heeft geen serverproces nodig. De test controleert de KPI's onafhankelijk tegen `validation_report.json`, alle vijf pagina's, zoek/sorteer/CSV, meervoudige selectie, alle filters, drilldown, afwezigheid van de verwijderde KPI-kaarten, herimport, geldige nul/conflicterende scores, negatieve en nulgewichten, mobiele breedte en het ontbreken van externe verzoeken. `browser_test_report.txt` bevat de uitkomst. Browserafhankelijkheden zijn uitsluitend voor ontwikkeling; het eindproduct bevat ze niet.

Het dashboard toont uitsluitend Q-02, Q-03, S-01, S-02 en S-03 als prestatie-indicatoren. De KPI-kaarten en aanvullende grafieken met klachten per maand en statusverdelingen zijn verwijderd. Filters, KPI-uitsplitsingen, bronrecords en technische datakwaliteitscontroles blijven beschikbaar.

De twee kwaliteitsgrafieken heten **Q2 – Doorlooptijd afgesloten klachten per leverancier** en **Q3 – Gemiddelde leeftijd openstaande klachten per leverancier**. Beide tonen gemiddelden in dagen met één decimaal. De leeftijdsgroepen zijn vervangen door Q3-gemiddelden. Drilldown bevat uitsluitend de bijbehorende afgesloten (Q2) of openstaande (Q3) klachten.

## Leveranciers groeperen

Via **Leveranciers groeperen** kun je oorspronkelijke namen zoeken, meerdere namen selecteren en koppelen aan één hoofdnaam. De koppeling geldt voor alle tabbladen, filters, vergelijkingen en KPI-berekeningen, en wordt na een nieuwe Excel-import opnieuw toegepast. Standaard vallen `Prysmian`, `Prysmian Group`, `Prysmian Netherlands B.V.` en `Prysmian Netherlands BV` onder **Prysmian Group** (expliciet door de gebruiker aangewezen varianten). Voor andere leveranciers worden duidelijke schrijfvarianten automatisch gegroepeerd; verschillen in landnaam, Group of Holding worden als voorstel getoond. Er wordt geen fuzzy matching gebruikt.

Koppelingen blijven lokaal in de browser opgeslagen; opslag bij rechtstreeks openen van een HTML-bestand kan per browser en bestandspad verschillen. Gebruik **Koppelingen exporteren/importeren** om de JSON-koppelingen naar een andere computer of HTML-versie mee te nemen. Import vervangt de huidige koppelingen. Je kunt elke koppeling afzonderlijk verwijderen. Het bronbestand en de oorspronkelijke namen in ruwe bronrecords blijven ongewijzigd. Groeperen reset de leverancierselectie; datum-, maand- en contractfilters blijven behouden. S1 telt één geldige score per gegroepeerde leverancier; conflicterende S1/S3-scores worden uitgesloten in plaats van willekeurig gekozen. Q telt de relevante meldingen en S2 telt de gewichten op, inclusief negatieve gewichten.

### Automatische herkenning voor alle leveranciers

**Leveranciers groeperen** scant alle tabbladen. Standaard worden namen samengevoegd wanneer ze na normalisatie van hoofdletters, leestekens en overtollige spaties exact gelijk zijn; bijvoorbeeld `Acme Netherlands B.V.` en `Acme Netherlands BV`. Dit is uitschakelbaar. Letters en cijfers veranderen niet; `Bedrijf 0021` en `Bedrijf 21` blijven verschillend.

Voor namen met dezelfde basis en verschillende achtervoegsels (`Group`, `Groep`, `Holding`, `Holdings`, `Netherlands`, `Nederland`, `BV`, `NV`, `Ltd`, `Limited`, `GmbH`, `Inc`, `LLC`) worden groepsvoorstellen getoond. Controleer de voorgestelde groepen, vink ze aan en kies **Geselecteerde voorstellen toepassen**. De kortste bestaande naam is de voorgestelde hoofdnaam; via de handmatige functie kun je een andere hoofdnaam kiezen. Voorstellen bewijzen geen gezamenlijke bedrijfsidentiteit: juridische entiteiten kunnen verschillend zijn. Bevestiging slaat de koppelingen op voor volgende imports. Nieuwe, niet-herkende namen blijven apart.

`test_aliases.cjs` controleert groepering, behoud van bronnamen, KPI-aggregatie, browseropslag, JSON-import/export, het afwijzen van circulaire koppelingen, automatische schrijfvarianten, groepsvoorstellen, uitschakelen van automatische herkenning en behoud van voorloopnullen.

## Artikel–contractkoppeling

De actuele ingebedde dataset komt uit **data/SRS data & KPI berekening - contractmapping.xlsx**. De eerdere bron blijft apart behouden. De nieuwe bron is ongewijzigd gekopieerd; SHA-256 `42455763b74fa7f77f5ac49f18c88b99b668764cee31735b51536a94a4917ec1`.

Optioneel tabblad **Contact Artikel mapping** (ook **Contract Artikel mapping** wordt herkend): rij 1 bevat `Inkoopcontract`, `Artikel`, `Artikelomschrijving`; gegevens vanaf rij 2. Het bouwscript en lokale Excel-upload lezen deze mapping mee. Q gebruikt artikelgegevens uit kolom **E**, bestaande contracten uit **P**. De waarde `0` in P is geen contract. Voor de huidige bron bevatten alle 2.177 klachten P=0.

Een contract kan onbeperkt meerdere artikelen bevatten. De index is artikel → verzameling contracten; dubbele identieke mappingregels tellen niet dubbel. Artikelcodes worden exact vergeleken, met behoud van voorloopnullen. De klachtenbron bevat achtcijferige artikelcodes; uit E worden volledige achtcijferige tokens gelezen, ook bij meerdere artikelen of een omschrijving. Grote onveilige numerieke waarden worden niet opgedeeld of hersteld, omdat Excel daarin precisie kan hebben verloren.

Automatische toewijzing vereist dat **alle gevonden artikelcodes** voorkomen in de mapping en hun gecombineerde contractverzameling precies één contract bevat. Meerdere artikelen die allemaal onder hetzelfde contract vallen, zijn dus automatisch koppelbaar. Artikelen met meerdere mogelijke contracten, onbekende codes of een gedeeltelijke match worden niet gegokt. Bestaande contracten blijven leidend; een afwijking van de mapping wordt gemeld. Handmatige koppelingen hebben voorrang. Er wordt niet op alleen leveranciersnaam of omschrijving gegokt.

Bij de aangeleverde mapping:

| Controle | Aantal |
|---|---:|
| Mappingregels | 5.636 |
| Unieke artikelen | 5.202 |
| Artikelen met meerdere contracten | 197 |
| Automatisch gekoppelde klachten | 214 |
| Contracten met gekoppelde klachten | 42 |
| Geen bruikbare achtcijferige artikelcode | 1.629 |
| Meerdere mogelijke contracten | 212 |
| Artikel niet in mapping | 101 |
| Gedeeltelijke artikelmapping | 14 |
| Ongeldig numeriek artikelveld | 7 |

Van de 1.629 klachten zonder bruikbare code hebben 1.563 een volledig leeg artikelveld; de overige bevatten bijvoorbeeld `nvt` of vrije tekst. **1.963 klachten kunnen op basis van deze bron niet eenduidig automatisch worden gekoppeld.** Voor volledige dekking zijn aanvullende artikel-/contractgegevens of handmatige keuzes nodig.

Via **Contractkoppelingen** zoek je de klacht, bekijk je de koppelstatus en kandidaten en kies je **Koppelen / wijzigen**. Een handmatig contract kan ook worden ingevuld als het niet in de mapping voorkomt. Handmatige koppelingen worden lokaal bewaard op de combinatie meldingnummer + aanmelddatum; bij dubbele combinaties worden ze niet toegepast. Bronkolommen blijven onveranderd. Verwijderen van een handmatige koppeling herstelt de bron-/mappinglogica. Exporteer/importeer de handmatige koppelingen als JSON om ze mee te nemen naar een andere browser of HTML-versie. De datum van een melding wijzigen betekent dat een oude handmatige koppeling niet automatisch wordt hergebruikt.

De kwaliteitstabel en de CSV-export bevatten het bronartikelveld, het uiteindelijke contract, de koppelstatus, kandidaten en het oorspronkelijke contract. De datakwaliteitspagina toont de koppelaantallen. Bij een contractfilter tellen alleen meldingen met dat toegewezen contract mee; ongekoppelde klachten blijven wel in het ongefilterde Q2/Q3-totaal.

`validate_contracts.py` berekent de koppelaantallen onafhankelijk in Python. `contract_validation_report.json` bevat het resultaat. `test_contracts.cjs` controleert dezelfde aantallen in de browser, Excel-herimport, meerdere artikelen per contract, onvolledige en dubbelzinnige matches, handmatige koppeling, bronbehoud, contractfilter en JSON-opslag.
