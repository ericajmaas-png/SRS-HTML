"""Independent Python reference from the original workbook, without dashboard code."""
import openpyxl,datetime,calendar,collections,json,re,sys,pathlib
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
def ident(v):
 if isinstance(v,(int,float)) and not isinstance(v,bool):return str(int(v)) if float(v).is_integer() and 0<v<=2**53-1 else ''
 s=str(v).strip() if v is not None else ''
 return '' if s.lower() in ('','0','#','##','(leeg)') else s
def interval(v):
 if isinstance(v,datetime.datetime):return v.date(),v.date()
 if isinstance(v,datetime.date):return v,v
 if isinstance(v,(float,int)) and v>0:
  x=openpyxl.utils.datetime.from_excel(v)
  return (x.date(),x.date()) if isinstance(x,datetime.datetime) else None
 if not isinstance(v,str):return None
 s=v.strip();q=re.fullmatch(r'(\d{4})\s*Q([1-4])',s,re.I)
 if q:
  y,n=map(int,q.groups());m=3*n;return datetime.date(y,m-2,1),datetime.date(y,m,calendar.monthrange(y,m)[1])
 for fmt in ('%Y-%m-%d','%d-%m-%Y','%d/%m/%Y'):
  try:d=datetime.datetime.strptime(s,fmt).date();return d,d
  except ValueError:pass
 return None
asof=datetime.date(2026,11,2);cut=datetime.date(asof.year-1,asof.month,min(asof.day,calendar.monthrange(asof.year-1,asof.month)[1]))
def state(v):
 d=interval(v)
 if d is None:return 'Datum onbekend'
 lo,hi=d
 return 'Toekomstige datum' if lo>asof else 'Ouder dan 12 maanden' if hi<cut else 'Actueel' if lo>=cut and hi<=asof else 'Onzekere datum'
k=[(i,r) for i,r in enumerate(wb['Kernassets'].iter_rows(min_row=2,values_only=True),2) if any(r[c] is not None for c in (0,3,5,7))]
p=[(i,r) for i,r in enumerate(wb['GSPP inkopen'].iter_rows(min_row=2,values_only=True),2) if any(r[c] is not None for c in (0,4,5))]
index=collections.defaultdict(list)
for i,r in p:
 if ident(r[5]) and ident(r[4]):index[(ident(r[5]),ident(r[4]))].append(r)
def calc(rs,basis='passport'):
 groups=collections.defaultdict(list)
 for i,r in rs:
  if ident(r[3]) and ident(r[5]):groups[(ident(r[3]),ident(r[5]),ident(r[20]))].append(r)
 counts=collections.Counter();states=collections.Counter();unmatched=0
 for (article,supplier,version),rr in groups.items():
  candidates=index[(article,supplier)];matched=[r for r in candidates if ident(r[7])==version] if version else candidates
  flags={str(r[18]).strip().upper() for r in rr if r[18] is not None}
  conflict=('JA' in flags and 'NEE' in flags) or ('NEE' in flags and bool(matched))
  presence='Onbekend' if conflict else 'Ontbrekend' if 'NEE' in flags else 'Aanwezig' if 'JA' in flags or matched else 'Onbekend'
  counts[presence]+=1
  if presence=='Aanwezig':
   if not matched:unmatched+=1
   values=[r[2] for r in matched] if basis=='passport' else [r[17] for r in matched] if matched else [r[32] for r in rr]
   statuses={state(v) for v in values};fresh=next(iter(statuses)) if len(statuses)==1 else 'Datum onbekend';states[fresh]+=1
 valid=[r for i,r in rs if isinstance(r[22],(int,float)) and isinstance(r[25],(int,float)) and r[25]!=0]
 c=sum(r[22] for r in valid);w=sum(r[25] for r in valid);n=len(groups);present=counts['Aanwezig'];missing=counts['Ontbrekend']
 return {'rows':len(rs),'units':n,'present':present,'missing':missing,'unknown':counts['Onbekend'],'unmatchedPresent':unmatched,'current':states['Actueel'],'freshPct':100*states['Actueel']/present if present else None,'missingPct':100*missing/n if n else None,'presencePct':100*present/n if n else None,'c':c,'w':w,'circular':100*c/w if w else None,'validWeights':len(valid),'unidentified':sum(not ident(r[3]) or not ident(r[5]) for i,r in rs),'states':dict(states)}
report={'asOf':asof.isoformat(),'rawPurchaseRows':len(k),'rawPassportRows':len(p),'all':calc(k),'entered':calc(k,'entered'),'Q1':calc([(i,r) for i,r in k if 1<=r[0]<=3]),'Q2':calc([(i,r) for i,r in k if 4<=r[0]<=6]),'contract':calc([(i,r) for i,r in k if ident(r[7])=='4600002231']),'category':calc([(i,r) for i,r in k if r[17]=='Kabels'])}
pathlib.Path('gspp_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
