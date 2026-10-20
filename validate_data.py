"""Independent validation of the source workbook; does not modify it."""
import sys, json, datetime, statistics, collections
import openpyxl
w=openpyxl.load_workbook(sys.argv[1],data_only=True)
q=list(w['Q2&3'].values)[1:]
complaints=[r for r in q if str(r[3]).strip().casefold()=='klacht']
closed=[r for r in complaints if r[17]=='5. Afgemeld' and isinstance(r[0],datetime.datetime) and isinstance(r[30],datetime.datetime)]
durations=[(r[30]-r[0]).total_seconds()/86400 for r in closed]
weights=[r for r in list(w['S2'].values)[7:] if all(isinstance(r[c],(float,int)) for c in [3,4])]
norm=lambda x:' '.join(str(x or '').split()).casefold()
groups=collections.defaultdict(list)
for r in list(w['S1'].values)[7:]:
 if r[0] and isinstance(r[5],(int,float)):groups[norm(r[0])].append(r[5])
valid=[v[0] for v in groups.values() if len(set(v))==1]
compare={}
for idx in [31,32]:
 pairs=[]
 for r,d in zip(closed,durations):
  v=r[idx]
  if isinstance(v,datetime.timedelta):v=v.total_seconds()/86400
  if isinstance(v,datetime.time):v=(v.hour*3600+v.minute*60+v.second)/86400
  if isinstance(v,(int,float)):pairs.append((d,v))
 compare[openpyxl.utils.get_column_letter(idx+1)]={'comparable':len(pairs),'equal_within_one_minute':sum(abs(a-b)<=1/1440 for a,b in pairs),'mean_source':statistics.mean(b for a,b in pairs) if pairs else None}
report={'records':{'Q2&3':len(q),'S1':len(list(w['S1'].values)[7:]),'S2':len(weights),'S3':len(list(w['S3'].values)[11:])},'complaints':len(complaints),'closed':len(closed),'open_without_end':sum(r[17]!='5. Afgemeld' and r[30] is None for r in complaints),'Q02':statistics.mean(durations),'S01':statistics.mean(valid),'S01_unique_valid':len(valid),'S01_conflicts':sum(len(set(v))>1 for v in groups.values()),'S02':100*sum(r[3] for r in weights)/sum(r[4] for r in weights),'source_duration_comparison':compare}
assert len(q)==5300 and len(complaints)==2177 and len(closed)==2016
assert report['open_without_end']==161
print(json.dumps(report,indent=2,ensure_ascii=False))
