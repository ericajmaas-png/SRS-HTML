# SRS duurzaamheid — circulair inkopen en grondstoffenpaspoorten

Open **Alliander_SRS_GSPP_Dashboard.html** in Chrome of Edge. Dit is een nieuw, zelfstandig HTML-bestand met CSS, JavaScript, Excel-parser en brondata ingebed. De bestaande SRS- en duurzaamheidsdashboards zijn niet gewijzigd. Er is geen backend of internet nodig.

## Gebruik

- **Overzicht:** gewogen circulariteit, aandeel actuele paspoorten en aandeel ontbrekende paspoorten. Doorklikken naar gewichten, actuele status en de ontbrekende artikelen.
- **Uitsplitsing:** alle drie KPI’s per leverancier, contract, productcategorie of de combinatie daarvan. Zoeken, sorteren, pagineren, bronregels en CSV-export.
- **Ontbrekende GSPP’s:** welke artikelen/paspoortversies ontbreken, inclusief leveranciernummer, contracten, productcategorie en omschrijving. Ook onbekende aanwezigheid, niet-actuele paspoorten en niet-identificeerbare artikelen zijn apart te selecteren.
- **Datakwaliteit:** controles op het volledige bronbestand, onafhankelijk van filters.

Filters: kwartaal, leverancier, contract en productcategorie. **Kwartaal volgt standaard de boekmaand**: 1–3 Q1, 4–6 Q2 enzovoort. De bron bevat geen boekjaar; het dashboard verzint geen jaar. Het huidige bestand bevat alleen boekmaanden 1–6. Onder *Peildatum en definities* kun je overschakelen naar het invoerkwartaal van het GSPP. Dat laatste kan de aanwezigheidspercentages vertekenen, omdat ontbrekende paspoorten doorgaans geen invoerdatum hebben; ze staan dan onder Onbekend.

De peildatum voor actualiteit start op de actuele datum in **Europe/Amsterdam** en kan worden gewijzigd. Standaard wordt *Datum paspoort* gebruikt. *Wanneer ingevoerd* is als afzonderlijke, zichtbaar benoemde alternatieve definitie beschikbaar. Filters wissen behoudt deze expliciete definities en peildatum. Er worden geen historische bestanden of paspoortwijzigingen gereconstrueerd uit een momentopname.

## Bron, inspectie en mapping

Bron: `data/Inzicht volledigheid GSPP presentatie bron.xlsx`, ongewijzigde lokale kopie van de upload. De volledige werkmap blijft lokaal; het dashboard bevat alleen de benodigde velden, zonder niet-benodigde interne documentlinks of factuurbedragen. De originele Excel wordt niet meegepubliceerd in Git. Voor opnieuw bouwen of de onafhankelijke Python-validatie is de oorspronkelijke upload nodig. SHA-256: `262e5234a9ca16ca3815c751940ed14c5ad2916f4722fa10fb707cda62ecbdbc`.

Er zijn **546 echte inkoopregels** in Kernassets en **385 documentregels** in GSPP inkopen. 687 lege of doorgetrokken formule-/opmaakregels zonder bedrijfsidentiteit in Kernassets en 6 lege registerregels worden niet ingelezen. Toelichting is leeg. Dia 3,4&6 en Dia 5&6 zijn presentatie-/draaitabelsamenvattingen met vaste criteria ‘vanaf januari 2025’ respectievelijk ‘vanaf juli 2025’; ze zijn geen aanvullende bron en worden niet dubbel geteld. Hun labels Geldig GSPP worden niet gebruikt als dynamische 12-maandentoets.

| Bron | Kolommen |
|---|---|
| Kernassets, kop rij 1 | A boekmaand; C goederengroep; D/E artikelnummer/omschrijving; F/G leveranciernummer/naam; H contract; K contract-gewichtseenheid; R Prod.cat.KPI; S GSPP?; U versie; W gerecycled ingangsgewicht; Z totaalgewicht; AA gewichtsvlag; AD nieuwe circulariteitsfractie ter controle; AG invoerwaarde; AH invoerkwartaal ter broninzage. |
| GSPP inkopen, kop rij 1 | A naam paspoort; B productnaam; C datum paspoort; D/E leveranciernaam/-nummer; F artikelnummer; H versie; R wanneer ingevoerd. |

In de ingestelde invoerkwartaalvariant wordt AG opnieuw geïnterpreteerd als datum of kwartaal; AH wordt niet blind vertrouwd. Formules worden niet uitgevoerd. Python en browserupload gebruiken de opgeslagen Excel-uitkomsten en herkennen omringende spaties/hoofdletters in tabbladnamen. Belangrijke kolomkoppen worden gecontroleerd; verschoven structuren worden afgewezen.

De uploadfunctie leest alleen Kernassets en GSPP inkopen. Bij een afgewezen import blijft de oude dataset behouden. Heropenen herstelt de ingebedde bron. Interne documentlinks worden niet opgehaald of automatisch geopend; niet-benodigde link-/medewerkervelden zijn niet ingebed.

## KPI 1 — resultaat circulariteit

`100 × SOM(Kernassets!W) / SOM(Kernassets!Z)` over de geselecteerde regels met twee numerieke gewichten en een **niet-nul totaalgewicht**. Dit is het gerecyclede ingangsgewicht en sluit aan op de *nieuwe* bronkolom AD. Kolom AB/AC (oude berekening) en X (recyclebaarheid aan het einde) worden niet bij de teller opgeteld. Bronpercentages worden nooit gewoon gemiddeld.

- 378 van 546 bronregels zijn zo berekenbaar.
- 46 regels hebben wel circulair gewicht maar totaalgewicht nul. Deze zouden het totaalcijfer sterk verhogen zonder bijbehorende noemer; ze worden niet als percentage geaggregeerd. De overige nulgewichtsregels zijn evenmin individueel berekenbaar.
- De vier retourregels met een geldig negatief totaalgewicht blijven behouden. Negatieve waarden worden niet op zichzelf verwijderd. Zeven extra negatieve tellerregels zonder totaalgewicht behoren tot de niet-berekenbare groep.
- Som gerecycled ingangsgewicht: **744.773,08547**; som totaalgewicht: **7.446.224,0198339**; resultaat **10,002023622794704%**.
- Bij een groepssom van nul ontstaat geen percentage. Een echte teller nul met geldige noemer geeft 0%, geen ontbrekende score.
- W/Z is voor alle 378 berekenbare regels gelijk aan bronkolom AD binnen de opgeslagen afrondingsmarge van 0,000001 fractie.
- Absolute eenheden worden als *brongewicht* getoond. Het dashboard aggregeert de reeds berekende W/Z-gewichten als vergelijkbare brongewichten, zonder eigen eenheidsconversie. Twaalf berekenbare regels hebben geen herkenbare contract-gewichtseenheid in K; dat staat in Datakwaliteit en vereist broncontrole. Er wordt geen kilogramlabel verzonnen.

## KPI 2 — actualiteit binnen 12 maanden

`100 × aantoonbaar actuele aanwezige benodigde GSPP’s / alle aanwezige benodigde GSPP’s`.

Een paspoort is aantoonbaar actueel wanneer de gekozen datum ligt in het inclusieve interval **peildatum minus 12 kalendermaanden t/m peildatum**. Schrikkeldagen en kalendermaanden worden correct behandeld. Toekomstige datums tellen niet als actueel.

Een kwartaaltekst, zoals 2025 Q4, is een interval van kwartaalbegin t/m kwartaaleinde. Het hele interval binnen de grens betekent Actueel; het hele interval ervoor betekent Ouder dan 12 maanden. Een grens die door het kwartaal loopt betekent Onzekere datum. Er wordt geen eerste of laatste dag als werkelijke paspoortdatum verzonnen. Nederlandse dag-maand-jaarstrings worden herkend. Onbekende, onzekere en toekomstige datums staan apart; zij zitten wel in de noemer van aanwezige paspoorten en tellen niet als aantoonbaar actueel.

Op **2 november 2026**, op basis van *Datum paspoort*: **0 van 179 actueel**, **129 ouder dan 12 maanden**, **50 datum onbekend**. Dit is geen importfout. Op basis van *Wanneer ingevoerd*: **3 actueel**, **151 ouder**, **15 onzeker**, **10 onbekend**. Een onleesbare peildatum geeft geen actualiteitspercentage.

De scope is de paspoortbehoefte van de geselecteerde inkopen. Ongebruikte documenten buiten die inkopen worden niet aan een contract geraden of in de KPI-noemer geplaatst. Het register van 385 regels is geen lijst van 385 unieke, voor de selectie benodigde paspoorten.

## KPI 3 — aanwezigheid en ontbrekende paspoorten

`100 × aantoonbaar ontbrekende benodigde GSPP’s / alle identificeerbare benodigde GSPP’s`.

De teleenheid is een **unieke artikelnummer–leveranciersnummer–opgegeven-versiecombinatie** binnen de selectie. Herhaalde maandinkopen en meerdere contractposities tellen voor die paspoortbehoefte één keer. Een niet-opgegeven versie is expliciet een aparte, niet nader gespecificeerde behoefte. Bij uitsplitsing per contract/categorie wordt opnieuw binnen die groep ontdubbeld; groepen kunnen hetzelfde paspoort nodig hebben en zijn dus niet altijd optelbaar.

- Bronstatus GSPP? = NEE en geen exact gekoppeld document: Ontbrekend.
- Bronstatus JA: Aanwezig volgens bron, ook als het document niet precies te koppelen is. Niet-gekoppeld is geen bewijs van ontbreken; de datum blijft dan onbekend.
- JA en NEE binnen dezelfde behoefte, of NEE terwijl een exact document aanwezig is: Onbekend/tegenstrijdig. Niet automatisch als aanwezig of ontbrekend geteld.
- Een exact document zonder expliciete bronstatus is bewijs van aanwezigheid; zonder beide blijft aanwezigheid onbekend.
- Artikelcode ## is geen unieke identiteit. De **12 inkoopregels** met zulke identiteiten worden niet samengevoegd tot fictieve artikelen en staan buiten de paspoortpercentages. Ze blijven apart vindbaar in de ontbrekendelijst.

Zonder filters zijn er **252 benodigde combinaties**: **179 aanwezig**, **73 aantoonbaar ontbrekend**, **0 onbekend**. Ontbrekend: **28,9682539683%**; aanwezig: **71,0317460317%**. Zestien aanwezige combinaties zijn niet exact aan een document te koppelen. De lijst toont de ontbrekende artikelen, leverancier, versie, contracten en categorieën plus de onderliggende bronregels.

## Identiteit, versies en bronproblemen

Koppeling gebeurt uitsluitend op de afzonderlijke artikel- en leveranciersidentifiers, met exacte versie als die is opgegeven. Voorloopnullen in tekstcodes blijven behouden. Namen dienen alleen voor weergave: verschillende leveranciernummers worden niet samengevoegd omdat hun namen gelijk zijn. Samengestelde sleutels P/Q en G in het register bevatten zeer grote/afgeronde getallen; deze worden niet gebruikt of gereconstrueerd.

Zonder opgegeven versie kunnen meerdere registerdocumenten overblijven. Alleen als al die kandidaten dezelfde actualiteitsstatus hebben wordt die status gebruikt. Bij verschillende statussen blijft de datum onbekend; er wordt geen nieuwste, gunstigste of willekeurige versie gekozen. Een specifiek gevraagde versie wordt niet vervangen door een andere versie met een ingevulde datum.

47 bronregels hebben geen Prod.cat.KPI en verschijnen als **Niet ingedeeld**. Een productgroep uit een ander tabblad wordt niet stilzwijgend als vervanging gebruikt. Contractwaarden # en W blijven als bronwaarden zichtbaar; er worden geen contractnummers geraden. Een paspoortdatum in 1905 blijft als bronfout te controleren; er wordt geen verondersteld jaartal gecorrigeerd.

## Reproduceren en validatie

```sh
python build_gspp.py 'data/Inzicht volledigheid GSPP presentatie bron.xlsx'
python validate_gspp.py 'data/Inzicht volledigheid GSPP presentatie bron.xlsx'
NODE_PATH=/workspace/scratch/srs-tools/node_modules node test_gspp.cjs
```

`validate_gspp.py` berekent de referentie rechtstreeks vanuit openpyxl, onafhankelijk van het dashboard. `gspp_validation_report.json` bevat totaalcijfers en uitkomsten voor Q1, Q2, contract 4600002231, categorie Kabels en beide datumdefinities, met vaste peildatum 2026-11-02.

`test_gspp.cjs` controleert die waarden in de browser, alle filters, groepen, ontbrekendelijst, zoeken/sorteren/pagineren/CSV, bronrecords, kwartaalintervallen, exacte datumboundary en schrikkeldag, toekomst/onbekende datum, identiteit met voorloopnullen, versies, conflicten, retouren, nulnoemers, lokale Excel-upload, behoud bij foutieve import, desktop/tablet/mobiel, Amsterdam-datum en offline gedrag. Fictieve randgevallen bestaan uitsluitend in een tijdelijk browserprofiel, niet in de ingebedde dataset. Zie `gspp_test_report.txt`.

De browsercontrole gebruikt Chromium; een afzonderlijke Edge-uitvoering is niet gedaan. De embedded parser is SheetJS CE 0.18.5, Apache 2.0; licentie in `vendor/XLSX-LICENSE`. Alleen het HTML-bestand is voor eindgebruik nodig.
