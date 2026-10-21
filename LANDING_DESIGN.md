# Startpagina: ontwerp en controle

De startpagina is een interne app-home, geen openbare marketingwebsite. De ontwerpvraag is: **welk inzicht wil ik voor het volgende leveranciersgesprek openen?** De belangrijkste actie is het managementoverzicht; het directe leveranciersprofiel is de tweede taak.

## Richting en bron

- Ontwerpaanwijzingen: [taste-skill / design-taste-frontend](https://github.com/Leonxlnx/taste-skill/blob/6010f91a9935f1c167dfc500fb1a475681892e6b/skills/taste-skill/SKILL.md), met de app-screenregels.
- Uitgegeven richting: **Editorial greeting**, seed **1893971964**, workspace/home, light. Palet en lettertype expliciet behouden; geen redraws.
- Bestaande Alliander-identiteit: groen, oranje en bordeauxrood; Segoe UI / systeemfallback; productnaam Supplier Rating System.
- Indeling: 12 kolommen, 24px tussenruimte, maximaal 1100px; rijen 8+4 en 8+4. De beschikbare breedte wordt volledig gebruikt. Op telefoon stapelen de onderdelen; op tablet vervalt de vaste zijbalk.
- Gezicht uit de opdracht: groene onderwerpvelden en de vijf Q/L/T/C/S-onderwerpen als daadwerkelijke navigatie, geen decoratieve iconen.
- Werkende interactie: een echte leveranciersnaam opzoeken en het juiste profiel openen. Bevestigde naamvarianten worden herkend. Een onbekende naam geeft een concrete melding.

De eerdere opzet met een grote gradientbanner en vijf iconentegels is vervangen door rustige inhoudsblokken en echte onderwerprijen. De navigatie is opgeruimd; de groene zijbalk is vlak en donkerder gemaakt voor leesbaar contrast. De kleuren van het aangeleverde logo blijven behouden. Er zijn geen extra foto's, externe fonts, nieuwe meetwaarden of doelen verzonnen.

## Gegevensinventaris

De pagina gebruikt de echte dataset: 5.300 meldingen, 29 KPI-definities, vijf logistieke, drie technische en 27 commerciële responsen. Getallen komen uit dezelfde gegevensobjecten als het dashboard. Het overzicht, vijf onderwerpbestemmingen, leveranciersprofiel, vergelijking, data-upload en datakwaliteit hebben werkende routes. Leverancierskoppelingen en contractkoppelingen blijven lokaal; het bronbestand wordt niet gewijzigd.

## Controle en afwegingen

- Playwright: alle routes, leverancierszoekfunctie inclusief naamvariant, foutmelding, Excel-upload, mobiel menu, herladen en geen externe verzoeken getest.
- Visuele controle: 1440, 768 en 390px; alle inspector-screenshots bekeken. Geen horizontale pagina-overflow.
- Taste-inspector `--app`: **0 FAIL**, drie waarschuwingen; samenvatting in `landing_design_check.json`.
- Taste-bronlint: **0 FAIL**, drie waarschuwingen: bestaande app-eyebrow en nulaanvulling voor datum/KPI-identifiers. De startpagina verbergt de eyebrow; datum- en KPI-identifiers blijven correct geformatteerd.
- Kleurbudgetwaarschuwing: de bestaande Alliander-zijbalk blijft bewust groen op verzoek van de gebruiker, boven het monochrome kleuradvies van de skill.
- Kleine-tekstwaarschuwing: de gedeelde app bevat veel verborgen leveranciersopties en bestaande sublabels van 11–12px. Zichtbare startpaginabody is 13–14px; secundaire labels 12px en de bestaande merkcaption 11px.
- Ruimtewaarschuwing: de primaire actie staat bewust onderaan het linkerbovenvlak, naast het leveranciersformulier. Dit laat de acties op dezelfde rij staan en houdt beide vlakken even hoog.

App-critique: de hoofdtaak staat vooraan, de kolomranden sluiten, datasetgetallen zijn herleidbaar, ontbrekende data krijgt geen verzonnen cijfer en de telefoon heeft een inklapbaar menu. De resterende afwegingen hierboven zijn vastgelegd; geen claims over een afzonderlijke Edge-test.

## Waarom de plug-in niet geïnstalleerd is

De gevraagde CLI-commando's zijn geprobeerd. De eerste opdracht faalde bij het aanmaken van `/run/codex-environment/codex-home/.tmp/marketplaces`: **Read-only file system**. Dit was geen afwijzing door automatische goedkeuringscontrole. Extra GitHub-rechten of een normaal bestandssandbox-permissieverzoek maken deze platformmount niet schrijfbaar.

De skillbron is daarom in `/workspace/scratch/taste-skill` gelezen en gebruikt, zonder Codex-configuratie te veranderen. De plug-in is niet geregistreerd of als geïnstalleerd aangemerkt. Voor plug-ininstallatie zijn een schrijfbare lokale Codex-configuratiemap en een nieuwe sessie nodig; een projectlokale skill onder `.agents/skills` is een alternatief als de cloudclient die locatie ondersteunt. Het HTML-dashboard heeft de plug-in niet nodig om te werken.
