"""Independent reference calculations for the full QLTCS workbook (read-only)."""
import openpyxl,sys,json,datetime,statistics,collections,re
from zoneinfo import ZoneInfo
w=openpyxl.load_workbook(sys.argv[1],data_only=True)
def avg(a):return statistics.mean(a) if a else None
def wd(start,end):
 if not isinstance(start,datetime.datetime) or not isinstance(end,datetime.datetime) or end<start:return None
 total=0.;cursor=start
 while cursor<end:
  stop=min(end,datetime.datetime.combine(cursor.date()+datetime.timedelta(days=1),datetime.time()))
  if cursor.weekday()<5:total+=(stop-cursor).total_seconds()/86400
  cursor=stop
 return total
q=[r for r in list(w['Q2&3'].values)[1:] if r[3]=='Klacht'];closed=[r for r in q if r[17]=='5. Afgemeld' and isinstance(r[30],datetime.datetime)];durations=[wd(r[7],r[30]) for r in closed];durations=[v for v in durations if v is not None]
standard={'Onvoldoende':0,'Matig':25,'Voldoende':50,'Goed':75,'Uitstekend':100}
scra={'Nee':0,'Ja, maar niet actueel':50,'Ja, en afgelopen jaar bevestigd':100}
rules={
'L-04':scra,'L-05':scra,'L-06':{'Nee':0,'Gedeeltelijk ja':50,'Ja':100},
'T-01':{'Nee':0,'Ja. Voor een deel van de assets of gedeeltelijk naar wens':50,'Ja':100},
'T-02':{'Er is niks':0,'Er is iets op papier':30,'Overeenstemming over effort en impact':70,'Samen initiatieven die in lijn zijn met de roadmap':100},
'T-03':{'Geen':0,'Leverancier maakt verschillen met andere netbeheerders inzichtelijk':30,'Leverancier geeft impact en effort aan in komen tot sector standaardiseren':70,'Wordt samengewerkt aan standaarden of bewuste keuze voor afwijking':100},
'T-04':{'Er is geen RFC proces geïmplementeerd bij de leverancier':0,'RFC proces en systeem zijn afgesproken tussen Liander en leverancier. Versiebeheer RFC is op orde':30,'RFC proces en systeem loopt conform afspraken (RFC worden geprioriteerd en opgevolgd)':70,'Leverancier en Liander halen afgesproken looptijden voor RFC':100},
'T-05':{'Geen ondersteuning':0,'Kennis en tekening zijn beschikbaar':30,'Reserve onderdelen zijn beschikbaar':70,'Er vindt nog doorontwikkeling plaats op oude componenten':100},'T-06':standard,
'C-01':{'Leverancier heeft prijsverhoging buiten de afgesproken indexatie doorgevoerd':0,'Leverancier volgt afgesproken prijsindexatie':50},
'C-02':{'Geen kosten-verbetervoorstel':0,'Idee(ën) zijn aangedragen maar niet gerealiseerd':50,'Idee(ën) zijn aangedragen en gerealiseerd':100},
'C-03':{'Niet':0,'Deels':50,'Volledig':100},'C-04':standard,
'C-05':{'Leverancier heeft zich niet aan afspraken gehouden en ook niet flexibel opgesteld aangaande problemen of uitdagingen':0,'Leverancier heeft zich gehouden aan reguliere afspraken, maar geen extra flexibiliteit getoond bij problemen of uitdagingenOf   er zijn geen verzoeken geweest voor flexibiliteit aan de leverancier.':60,'Leverancier heeft flexibel meegedacht':80,'Leverancier heeft uitstekende flexibiliteit getoond':100},
'C-06':{'Geen':0,'Nagenoeg geen':25,'Gemiddeld':50,'Regelmatig':75,'Vaak':100},
'C-07':dict(zip(['Nooit prioriteit gegeven','Zelden prioriteit gegeven','Soms prioriteit gegeven','Regelmatig prioriteit gegeven','Vaak prioriteit gegeven'],[0,25,50,75,100])),
'C-08':dict(zip(['Nooit initiatief getoond','Zelden initiatief getoond','Af en toe initiatief getoond','Regelmatig initiatief getoond','Vaak initiatief getoond'],[0,25,50,75,100])),
'C-09':dict(zip(['Geen inzet van expertise','Beperkte inzet van expertise','Redelijke inzet van expertise','Goede inzet van expertise','Uitstekende inzet van expertise'],[0,25,50,75,100])),
'C-10':dict(zip(["Geen investering en/of risico's voor Alliander","Beperkte investering en/of risico's voor Alliander","Enige investering en/of risico's voor Alliander","Redelijke investering en/of risico's voor Alliander","Veel investering en/of risico's voor Alliander"],[0,25,50,75,100]))}
columns={'L':{'L-04':[17],'L-05':[19],'L-06':[21]},'T':{f'T-{i+1:02}':[17+2*i] for i in range(6)},'C':dict(zip([f'C-{i:02}' for i in range(1,11)],[[17],[19],[21,22,23,24,25],[27],[29],[31],[33],[35],[37],[39]]))}
scores={f'L-{i:02}':{'value':None,'count':0} for i in range(1,4)};counts={};missing_contract={}
for tab,specs in columns.items():
 rows=[r for r in list(w[tab].values)[1:] if r[0] is not None and r[4]==1];counts[tab]=len(rows);missing_contract[tab]=sum(not r[16] for r in rows)
 for id,cols in specs.items():
  values=[]
  for r in rows:
   vs=[rules[id].get(r[c]) for c in cols]
   if all(v is not None for v in vs):values.append(avg(vs))
  scores[id]={'value':avg(values),'count':len(values)}
groups=collections.defaultdict(list)
for r in list(w['S1'].values)[7:]:
 if r[0] and isinstance(r[5],(int,float)):groups[' '.join(str(r[0]).split()).casefold()].append(r[5])
s1=avg([vs[0] for vs in groups.values() if len(set(vs))==1])
weights=[r for r in list(w['S2'].values)[7:] if all(isinstance(r[i],(float,int)) for i in (3,4))]
s2=100*sum(r[3] for r in weights)/sum(r[4] for r in weights)
reference_time=datetime.datetime(2026,10,20,12)
open_rows=[r for r in q if r[17]!='5. Afgemeld' and r[30] is None and isinstance(r[0],datetime.datetime)]
report={'catalog':sum(bool(re.fullmatch('[QLTCS]-[0-9]{2}',str(r[0] or ''))) for r in w["KPI's"].values),'Q02':avg(durations),'Q02_eligible':len(durations),'closed':len(closed),'open':sum(r[17]!='5. Afgemeld' and r[30] is None for r in q),'S01':s1,'S02':s2,'Q03_reference_time':'2026-10-20T12:00:00+02:00','Q03':avg([wd(r[0],reference_time) for r in open_rows]),'surveys':counts,'missing_contract':missing_contract,'scores':scores,'workday_cases':{'friday_monday':wd(datetime.datetime(2026,10,16,12),datetime.datetime(2026,10,19,12)),'weekend':wd(datetime.datetime(2026,10,17),datetime.datetime(2026,10,19))}}
assert report['catalog']==29 and report['Q02_eligible']==42
print(json.dumps(report,indent=2,ensure_ascii=False))
