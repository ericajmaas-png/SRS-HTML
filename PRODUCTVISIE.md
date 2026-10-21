# Implementatie productvisie Supplier Rating System

Bron: de door de gebruiker aangeleverde **Productvisie Supplier Rating System.pdf**, gelezen inclusief de afbeelding met thema’s en subthema’s op pagina 2. De PDF is een productspecificatie; geen instructie om brondata of toegangsrechten te wijzigen.

## Van visie naar werking

| Visie | Implementatie |
|---|---|
| Home: hoe doet mijn leverancier het? | Standaard start op Leveranciersprestatie met één leverancier, periode, contract, totaalscore indien berekenbaar en vijf QLTCS-thema’s. Q/C actief; L/T/S duidelijk als latere fase. |
| Eerste fase kwalitatieve Q en C | Kwaliteit bevat Q-04/SQA; commercieel C-01 t/m C-10. De bestaande kwantitatieve Q-02/Q-03 worden niet vermengd met kwalitatieve punten. Q-04 heeft geen bronantwoorden en blijft ontbrekend. |
| Thema → cluster → KPI | Scoreopbouw met uitklapbare clusters en clusterfilter. Commercieel: Betaalbaarheid C1–2, Kostentransparantie C3, Samenwerking C4–6, Customer of Choice C7–10; Q4 Kwaliteitsmanagementsysteem, volgens de PDF. |
| Score, maximum en categorie | Elke kwalitatieve KPI maximaal 100. Gewogen scores en categoriegemiddelden met expliciete berekeningsregels. Marker in balk = categoriegemiddelde. |
| Ontwikkeling in de tijd | Kwartaaloverzicht met composietscore én alle onderliggende commerciële KPI’s. De historische context gebruikt alle kwartalen binnen hetzelfde contract, los van de geselecteerde periode; dit staat bij het overzicht. Zonder vastgestelde weging blijven individuele kwartaal-KPI’s beschikbaar. |
| Vergelijkbare leveranciers | Alleen expliciet toegewezen categoriegenoten. Leverancierfocus en globale selectie beperken de categoriebenchmark niet; contract, jaar, kwartaal en halfjaar blijven gelden. |
| Onderbouwen en opvolgen | Drilldown met respons, bronrij, contract, periode, antwoord, punten en interne toelichting. Verbeteracties met eigenaar, deadline, context en status. |
| Intern gebruik | Informatie en toelichtingen blijven intern; geen automatische leverancierpublicatie, verzending of publieke presentatie. |
| Betrouwbaarheid | Nul blijft geldige score. Ontbrekende of conflicterende antwoorden worden niet gescoord. Eerdere bronkoppelingen en QLTCS-analyses behouden onder Verdieping. |

## Vast te stellen definities en grenzen

- **Geen vastgestelde weging in de bron.** De bestaande Excel-gewichten zijn deels als datums opgeslagen. Het dashboard initialiseert daarom geen gewichten. Via *Categorieën en wegingen* kan een definitie-eigenaar positieve relatieve KPI-gewichten invoeren; 0 = uitgesloten. De berekening is `SOM(KPI-score × gewicht) / SOM(gewicht)`. Alleen positief gewogen KPI’s vormen de definitie; de homepagina toont ze expliciet. Alle betreffende KPI’s moeten voor de leverancier meetbaar zijn; anders blijft de samengestelde score ontbreken. Thema en cluster gebruiken dezelfde gewichten binnen hun eigen deelverzameling. Er zijn geen extra themawegingen of automatische statusgrenzen.
- **Categorieën ontbreken als betrouwbare expliciete mapping.** Categorieën worden handmatig vastgelegd voor leveranciers met commerciële responsen, niet afgeleid uit bedrijfsnamen of uit vrije contractbeschrijvingen. Categorievergelijking is hoofdletterongevoelig. Geen categorie betekent geen benchmark.
- **Benchmark:** reken eerst dezelfde KPI/composiet per leverancier uit; middel vervolgens de geldige leveranciersscores met gelijk gewicht. De geselecteerde leverancier telt mee. Minimaal twee meetbare leveranciers vereist. Aantal meetbare leveranciers staat erbij; ontbrekende leveranciers worden niet nul.
- **Bronkwaliteit:** commerciële scorerichting C-06 is inhoudelijk opvallend (meer verkeerde facturen geeft meer punten). Dit blijft zichtbaar als aandachtspunt en wordt niet stilzwijgend veranderd. Q-04/SQA ontbreekt. Medallia-antwoorden voor Q worden niet verzonnen uit SAP-klachten.
- De nummering op de PDF-afbeelding wijkt op onderdelen af van het Excel-KPI-werkblad, onder andere L4–7 en C-codes bij duurzaamheid. De bestaande bron-KPI-codes blijven behouden om foutieve herclassificatie te voorkomen; de nieuwe Q/C-clusterindeling volgt de visie.
- De applicatie blijft het expliciet gevraagde zelfstandige offline **HTML-bestand**, geen Power BI-rapport. Een gedeelde dienst met circa 16 gebruikers, autorisaties, versiebeheer van definities en centrale actieopslag vergt een afzonderlijke omgeving. Binnen deze offline oplevering blijven instellingen en acties per browser opgeslagen en overdraagbaar via JSON. Een opgeslagen configuratie is geen formele goedkeuring van definities.
- Excel-upload blijft dezelfde bestandsstructuur en opgeslagen formule-uitkomsten gebruiken. Onbekende toekomstige Medallia-exportstructuren vereisen een nieuwe gevalideerde mapping. Q4 zonder aangeleverde structuur wordt niet op goed geluk ingelezen.
- Bestaande leverancieraliassen worden toegepast vóór het nieuwe dashboard; als een hoofdnaam achteraf verandert, moeten categorie- en actiekoppelingen naar die hoofdnaam opnieuw gecontroleerd worden.
- Geen totaalrapport of leverancierspresentatie wordt automatisch gedeeld. De contractmanager bepaalt welke interne informatie extern gebruikt wordt.

## Validatie

`test_product_vision.cjs` controleert de drie pagina’s, ontbrekende scores, de onafhankelijke herberekening van een gewogen gemiddelde en benchmark, onvoldoende dekking, categorieafbakening, periodebehoud, clusterfilter, bronantwoorden, actieopvolging, browseropslag, mobiele breedte en offline gedrag. Categorieën en gewichten die de test invoert zijn uitsluitend testinstellingen in een tijdelijk browserprofiel, nooit ingebedde productdata. De bestaande QLTCS-, import-, koppel- en filtertests blijven van toepassing op de verdieping.
