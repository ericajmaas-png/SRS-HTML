# Alliander Supplier Rating System

Open **Alliander_SRS_Dashboard.html** in Edge of Chrome. Het bestand bevat alle CSS, JavaScript, grafiekcode, Excel-parser en brondata. Internet, backend en installatie zijn voor gebruik niet nodig.

Het dashboard heeft tien tabs: Start, Managementoverzicht, Kwaliteit, Logistiek, Techniek, Commercieel, Duurzaamheid, Leveranciersprofiel, Leveranciersvergelijking en Datakwaliteit. Het overzicht toont alle 29 genummerde KPI-definities uit **KPI’s**. De eerder verwijderde KPI-kaarten blijven verwijderd.

## Actuele bron en volledigheid

De actuele bron is `data/SRS data & KPI berekening - QLTCS-v2.xlsx`, de laatst aangeleverde versie met een eigen logistieke vragenlijst. De bron is uitsluitend gelezen en ongewijzigd gekopieerd. SHA-256: `8971153424581bfcc91f3d08856b9299727559febfd39241ac99bb95b9196179`.

**24 van de 29 KPI’s zijn met deze bron berekenbaar.** Q-01 en Q-04 ontbreken als meetdata; L-01, L-02 en L-03 vereisen order-, leverings- en bevestigingsgegevens die niet zijn aangeleverd. Deze vijf KPI’s zijn zichtbaar met de reden waarom geen score kan worden berekend. Ontbrekende antwoorden krijgen nooit automatisch nul.

## Mapping en berekeningen

| Bron | Mapping / verwerking |
|---|---|
| Q2&3, vanaf rij 2 | A aanmelding; B meldingnummer; D soort; E artikelnummer(s); F leverancier; G omschrijving; H uitgestuurd naar leverancier; O contractmanager; P bestaand contract; R status; S/T categorie; AE afmelding. AF/AG zijn uitsluitend bronkolommen, geen rekenbasis. |
| Q-01 | DPPM vereist defectaantallen en totale aantallen artikelen. Niet beschikbaar. De procentuele klassegrenzen in KPI’s zijn bovendien niet eenduidig. Geen verzonnen score. |
| Q-02 | Alleen Klacht met status `5. Afgemeld`, geldige H en AE en AE≥H. Gemiddelde werkdagen tussen uitsturen en afmelden. **42** van **2.016** afgesloten klachten zijn berekenbaar; gemiddelde **45,6732638889 werkdagen**, weergegeven als **45,7**. Een ontbrekende H wordt niet vervangen door A. |
| Q-03 | Alleen Klacht met status niet `5. Afgemeld`, geen geldige AE en geldige A die niet in de toekomst ligt. Gemiddelde werkdagen vanaf A tot de actuele kloktijd in Europe/Amsterdam. **161** openstaande klachten. Wordt iedere minuut bijgewerkt. |
| Q-04 | SQA-assessment ontbreekt. Geen score. |
| S1 | Kop op rij 7, data vanaf rij 8. A leverancier; D ladder; E SBTi; F opgeslagen punten; G datakwaliteit. Gemiddelde over unieke leveranciers met geldige, eenduidige score. Identieke duplicaten tellen één keer; conflicterende scores worden uitgesloten. |
| S2, vanaf rij 8 | A boekmaand; B leverancier; C contract; D circulair gewicht; E totaalgewicht; F bronfractie. Berekening **100 × SOM(D) / SOM(E)**, inclusief negatieve gewichten; uitsluitend twee numerieke gewichten. Noemer nul levert geen score. |
| S3, vanaf rij 12 | A leverancier; B:F componenten; G score (ook tekst `70/100`); H leidende tekstuele volwassenheidsband; I verbeteracties. Meerdere leveranciers: verdeling over banden, geen gemiddelde van categorieën. |
| KPI’s | Kolom A genummerde KPI-code; B cluster; C criterium; E bron; G definitie; L:P antwoordcategorieën. Numerieke punten uit de vervolgregels van hetzelfde KPI-blok. Alleen Q/L/T/C/S met code `X-00` worden opgenomen; ongenummerde toekomstige ideeën niet. |
| L / T / C | Rij 1 kop, eventuele toelichtingsrijen zonder responsnummer worden overgeslagen. A respons-ID; E voltooid; O beoordelingsjaar; P kwartaal; Q contract. Alleen voltooide, niet-conflicterende responsen tellen mee. |

**Werkdagen** zijn maandag t/m vrijdag, berekend over het halfopen tijdinterval tussen de twee tijdstippen, inclusief gedeeltelijke dagen. Weekenden tellen niet mee; feestdagen worden niet afgetrokken omdat geen feestdagenkalender is aangeleverd. Lokale kloktijd is leidend, zonder zomer-/wintertijdcorrectie. De gebruiker heeft deze werkdagdefinitie uit het KPI-werkblad bevestigd; dit vervangt de eerdere kalenderdagen en de vroegere Q-02-berekening vanaf A.

### Logistiek

Vijf logistieke responsen. R → L-04 SCRA; T → L-05 ASL; V → L-06 contingencyplan. Antwoorden worden gekoppeld aan de bronrubriek: 0/50/100 punten. De antwoordvariant `Ja, en afgelopen jaar bevestigd` is expliciet gelijkgesteld aan de rubricering `Ja, en actualiteit afgelopen jaar bevestigd`.

Over alle vijf responsen: L-04 **50**, L-05 **30**, L-06 **80** punten. Eén respons heeft geen contract/leverancier en beoordelingsjaar 2028; deze blijft in het ongefilterde totaal zichtbaar en valt weg bij de betreffende filters. Toekomstige beoordelingsjaren worden in Datakwaliteit gemeld.

### Techniek

Drie responsen. R/T/V/X/Z/AB → T-01 t/m T-06. Punten volgen de bijbehorende antwoordrubriek. De taalkundige variant van het gedeeltelijke roadmapantwoord voor T-01 is expliciet gekoppeld aan 50 punten. Over alle responsen: **50; 43,3333; 70; 0; 100; 58,3333** punten.

### Commercieel

27 responsen. R → C-01, T → C-02, V:Z → C-03, AB → C-04, AD → C-05, AF → C-06, AH → C-07, AJ → C-08, AL → C-09, AN → C-10. Toelichtingen blijven bij de betreffende vraag beschikbaar.

C-03 wordt per respons berekend als het gemiddelde van de vijf componenten (Niet=0, Deels=50, Volledig=100); alle vijf antwoorden zijn vereist. Daarna worden de geldige responsscores gemiddeld. Het gecombineerde antwoord over reguliere flexibiliteit / geen flexibiliteitsverzoeken krijgt de expliciet vermelde **60** punten uit de bron. C-07 t/m C-10 hebben elk 17 ingevulde antwoorden; de tien lege antwoorden tellen niet als nul.

**Let op C-06:** de bron kent `Geen=0`, `Nagenoeg geen=25`, `Gemiddeld=50`, `Regelmatig=75`, `Vaak=100` toe aan verkeerde facturen. Deze inhoudelijk opvallende richting wordt letterlijk gevolgd en zichtbaar toegelicht, niet stilzwijgend omgekeerd.

### Aggregatie en koppeling

Scores van de vragenlijsten zijn gemiddelden over geldige voltooide responsen. Meerdere beoordelingen van hetzelfde contract blijven afzonderlijke beoordelingen. Exact dubbele respons-ID’s binnen hetzelfde tabblad tellen één keer; conflicterende dubbele ID’s worden uitgesloten. Er wordt geen gewogen totaalscore verzonnen: de bronwegingen zijn deels als Excel-datum opgeslagen en vormen geen betrouwbaar numeriek weegschema.

De leveranciersnaam van een assessment wordt gelezen uit het contractveld vóór de dubbele spaties. De respondentnaam wordt nooit als leverancier gebruikt. Zonder contract wordt geen leverancier geraden; zulke responsen tellen wel in het ongefilterde assessmenttotaal. IP-adressen, browsergegevens, respondentnamen en andere niet benodigde enquête-telemetrie zijn uit de ingebedde en lokaal geïmporteerde enquêtegegevens weggelaten. De oorspronkelijke Excel blijft ongewijzigd.

## Filters, details en import

- Leverancierfilter: doorzoekbare multiselect, geldt voor alle bronnen.
- Aanmelddatumbereik: alleen Q. Boekmaand: alleen S2 (de bron bevat maandnummers zonder jaar).
- Beoordelingsjaar en -kwartaal: uitsluitend L/T/C, op O/P; niet op de invuldatum.
- Contract: Q, S2 en L/T/C. Volledige CW-contractnamen uit vragenlijsten worden niet zonder een aparte mapping gelijkgesteld aan SAP-contractnummers.
- S1/S3 hebben geen periode- of contractfilter.
- Grafieken openen bronrecords. Vragenlijstpanels tonen definitie, puntentabel en aantallen.
- Tabellen ondersteunen zoeken, sorteren, rijdetails en CSV-export van alle gefilterde zoekresultaten (maximaal 500 rijen zichtbaar). CSV gebruikt puntkomma’s, UTF-8 BOM en bescherming tegen formule-injectie.

**Excel laden** vervangt de data uitsluitend in het huidige venster. Het bestand wordt niet naar een server verstuurd. Sla Excel-formules vooraf op met berekende uitkomsten: de parser voert geen Excel-formules uit. Het dashboard herkent de bestaande Q/S-structuur en leest optionele L/T/C/KPI’s-tabbladen en de artikel–contractmapping mee. Bij oudere bestanden ontbreken de nieuwe KPI’s expliciet; geen eerdere data blijft ongemerkt hangen. Heropenen herstelt de ingebedde brondata.

## Leveranciers groeperen

Volledige namen worden vergeleken na normalisatie van hoofdletters en spaties; voorloopnullen blijven behouden. Schrijfvarianten met alleen andere leestekens, zoals B.V./BV, worden automatisch gegroepeerd (uitschakelbaar). Verschillen met Group, Holding of landnamen leveren voorstellen op die je bevestigt. Geen fuzzy matching op bedrijfsidentiteit.

Prysmian, Prysmian Group, Prysmian Netherlands B.V. en Prysmian Netherlands BV vallen standaard onder **Prysmian Group**, zoals door de gebruiker aangewezen. Andere groepen kun je beheren via **Leveranciers groeperen**. Koppelingen worden lokaal bewaard en na iedere import opnieuw toegepast; gebruik JSON-export/import voor een andere browser of HTML-versie. Bronnamen blijven in de ruwe bronrecords behouden. Groeperen reset de leverancierselectie, niet de overige filters.

## Artikel–contractmapping

Optioneel tabblad **Contact Artikel mapping** (ook **Contract Artikel mapping**): `Inkoopcontract`, `Artikel`, `Artikelomschrijving`, vanaf rij 2. Een contract kan meerdere artikelen bevatten. Per artikel wordt de verzameling contracten bijgehouden. Alleen als alle gevonden volledige achtcijferige artikelcodes bekend zijn en samen precies één contract opleveren, wordt de klacht automatisch toegewezen. Grote numerieke velden met mogelijk precisieverlies worden niet hersteld of opgedeeld. Bestaande contracten blijven leidend; afwijkingen worden gemeld. P=0 betekent geen contract.

De mapping bevat 5.636 regels, 5.202 artikelen en 197 artikelen met meerdere mogelijke contracten. **214 klachten** zijn automatisch gekoppeld aan **42 contracten**; **1.963** blijven niet eenduidig koppelbaar. Via **Contractkoppelingen** zie je de reden, kandidaten en kun je handmatig kiezen. Handmatige koppelingen worden bewaard op meldingnummer + aanmelddatum en zijn overdraagbaar via JSON. Ze veranderen de bron niet. De kwaliteitstabel/CSV toont bronartikel, oorspronkelijk contract, uiteindelijk contract en koppelstatus.

## Reproduceren en testen

```sh
cd /workspace/SRS-HTML
python -m venv /workspace/scratch/srs-venv
/workspace/scratch/srs-venv/bin/pip install --cache-dir /tmp/srs-pip-cache -r requirements.txt
/workspace/scratch/srs-venv/bin/python build_dashboard.py 'data/SRS data & KPI berekening - QLTCS-v2.xlsx'
/workspace/scratch/srs-venv/bin/python validate_qltcs.py 'data/SRS data & KPI berekening - QLTCS-v2.xlsx'
```

`qltcs_validation_report.json` bevat de onafhankelijke Python-uitkomsten. De historische `validate_data.py` en `validation_report.json` horen bij de oorspronkelijke kalenderdagdefinitie, niet bij de actuele Q-02-definitie.

Browsertests gebruiken Playwright 1.56.1, `/usr/bin/chromium` en `NODE_PATH=/workspace/scratch/srs-tools/node_modules`: `test_qltcs.cjs`, `test_browser.cjs`, `test_aliases.cjs`, `test_contracts.cjs`. Uitkomsten staan in de overeenkomstige `*_test_report.txt`-bestanden. De tests gebruiken lokale response-interceptie zonder extern netwerk. Desktop en mobiel zijn getest; geen afzonderlijke Microsoft Edge-uitvoering. Rechtstreekse file-navigatie is door het testbrowserbeleid geblokkeerd; het product gebruikt geen serverfunctionaliteit.

De vormgeving gebruikt benaderde kleuren uit het aangeleverde Alliander-logo: groen #62892f/#719a34, donkergroen #344b1c, oranje #ef7d00 en bordeauxrood #8c171b. De lokaal ingebedde Excel-parser is SheetJS CE 0.18.5 (Apache 2.0); licentie in `vendor/XLSX-LICENSE`. Alleen het HTML-bestand is nodig voor eindgebruik.

## KPI-weergave

De categoriepagina’s gebruiken compacte horizontale staafdiagrammen. Puntenscores hebben overal een vaste schaal van 0–100; een score van 50 beslaat dus steeds de helft van de schaal. Werkdagen hebben een zichtbare dynamische schaal. Circulariteit gebruikt minimaal 0–100%, met een uitgebreider bereik bij negatieve of hogere waarden. Uitkomst en aantal metingen blijven zichtbaar; de gewogen circulariteit wordt niet vervangen door een gemiddelde van leverancierspercentages.

Vragenlijst-KPI’s tonen daarnaast gestapelde antwoordverdelingen per leverancier, met een legenda en tooltips. Segmenten tellen geldige antwoorden naar de bronrubriek; ontbrekende/ongeldige scores staan apart vermeld en worden geen nul. C3 toont vijf componentantwoorden per volledig ingevulde respons, dus 135 componentantwoorden bij 27 geldige responsen. Klik een segment voor de bijbehorende responsen; bij C3 worden de bronresponsen getoond die minstens één component in die categorie hebben. De kleuren onderscheiden puntencategorieën en zijn geen onafhankelijk oordeel over goed/slecht.

Via **Leveranciersprofiel** kies je één leverancier en optioneel een tweede. Alle 29 KPI’s staan per categorie onder elkaar, inclusief eenheden, aantallen, ontbrekende-dataredenen en bronrecords. Puntenscores gebruiken 0–100; beide profielen delen dezelfde werkdagenschaal. De bestaande globale filters blijven van toepassing; de keuzelijsten bevatten alleen leveranciers binnen de globale leverancierselectie. De zoekfunctie beperkt de leverancierskeuzelijsten. `test_visuals.cjs` controleert schalen, verdelingen, profielen, filters, bronrecords en mobiele weergave; uitkomst in `visuals_test_report.txt`.

## Managementoverzicht

Het managementoverzicht groepeert alle 29 KPI’s in vijf onderwerpsecties: Kwaliteit, Logistiek, Techniek, Commercieel en Duurzaamheid. De lange KPI-tabel en leveranciersgrafieken zijn hier vervangen door compacte KPI-regels. De categoriepagina’s behouden hun leveranciersvergelijkingen. Puntenscores gebruiken 0–100, werkdagen delen een zichtbare schaal en circulariteit blijft een gewogen percentage. Er wordt geen samengesteld totaalcijfer of norm verzonnen.

Bovenaan staat hoeveel KPI’s in de actuele filterselectie berekenbaar zijn (24 van 29 zonder filters). Bij Q2 staat de meetdekking 42 van 2.016 afgesloten klachten. Vragenlijsten tonen een compacte antwoordverdeling over alle geldige responsen; C3 telt de vijf componenten. S3 toont aantallen per tekstuele volwassenheidsband. Een ontbrekende score krijgt een concrete reden. De uitklapbare aandachtspunten geven dekking en ontbrekende data weer.

**Details** opent de betreffende categorie; **Leveranciers vergelijken** opent het leveranciersprofiel. **Bronrecords** en antwoordsegmenten tonen de records achter precies die KPI. De bestaande leverancier-, contract- en periodefilters blijven van toepassing. `test_management.cjs` controleert waarden, aantallen, verdelingen, filters, doorklikken en mobiele breedte; resultaat in `management_test_report.txt`.

Binnen elk managementonderwerp staan berekenbare KPI’s eerst. De uitkomsten zijn zo nodig binnen het onderwerp scrollbaar, zodat het overzicht compact blijft; ontbrekende KPI’s blijven bereikbaar en worden ook bij de aandachtspunten opgesomd.

## Startpagina

Het dashboard opent op **Start**. De landing page biedt toegang tot het managementoverzicht, de vijf KPI-onderwerpen, leveranciersvergelijking en datakwaliteit. Zoek direct een leverancier om het profiel te openen; een bevestigde naamvariant wordt herkend. Een leverancier kiezen past bewust de globale leverancierselectie aan. Overige filters blijven behouden. Andere navigatie vanaf Start behoudt de bestaande filters.

De startpagina verbergt de dashboardfilters. Op mobiel is het menu inklapbaar. Via **Bijgewerkte Excel laden** kan hetzelfde offline importproces worden geopend. Er zijn geen extra bestanden of externe services nodig. `test_landing.cjs` controleert navigatie, leverancierszoekfunctie, import, mobiele menutoestand en herladen; uitkomst in `landing_test_report.txt`.

De ontwerprichting is gebaseerd op **Editorial greeting** uit [taste-skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md), toegepast binnen de bestaande Alliander-huisstijl. De plug-in is niet geïnstalleerd: de cloudmap `/run/codex-environment/codex-home` is alleen-lezen. De skillbron is gelezen vanuit een tijdelijke clone; het dashboard heeft geen runtime-afhankelijkheid van de plug-in. Zie `LANDING_DESIGN.md` voor controle en afwijkingen.

### Robuuste tabbladnamen
De Python-verwerking en lokale Excel-upload herkennen Q2&3, S1–S3, L, T, C en KPI's ongeacht hoofdletters en omringende spaties. Zo wordt `L ` ook als Logistiek ingelezen. Dubbele namen na normalisatie worden afgewezen. Ontbrekende brongegevens blijven ontbrekend; normalisatie creëert geen scores voor Q-01, Q-04 en L-01 t/m L-03.
