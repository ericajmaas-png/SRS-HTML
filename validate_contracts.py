"""Independent, read-only article-to-contract checks for the mapping workbook."""
import sys, json, collections, re, math
import openpyxl
w=openpyxl.load_workbook(sys.argv[1],data_only=True)
def articles(v):
 if isinstance(v,(int,float)):
  return [str(int(v))] if math.isfinite(v) and int(v)==v and 10**7<=v<10**8 else []
 return sorted(set(re.findall(r'(?<!\d)\d{8}(?!\d)',str(v or ''))))
m=collections.defaultdict(set);mapping=list(w['Contact Artikel mapping'].values)[1:]
for c,a,*_ in mapping:
 c,a=str(c).strip(),str(a).strip()
 if c and a:m[a].add(c)
counts=collections.Counter();linked=[]
for r in list(w['Q2&3'].values)[1:]:
 if r[3]!='Klacht':continue
 a=articles(r[4]);candidates=set().union(*(m.get(x,set()) for x in a));unmapped=[x for x in a if x not in m];existing=str(r[15]).strip() if r[15] else ''
 if existing:status='Bestaand contract'
 elif not a:status='Ongeldig artikelnummer' if isinstance(r[4],(int,float)) and r[4] else 'Artikelnummer ontbreekt'
 elif unmapped:status='Onvolledige artikelmapping' if candidates else 'Artikel niet in mapping'
 elif len(candidates)==1:status='Automatisch via artikel';linked.append((r[1],next(iter(candidates))))
 else:status='Meerdere contracten mogelijk'
 counts[status]+=1
report={'mapping_rows':len(mapping),'unique_articles':len(m),'articles_multiple_contracts':sum(len(cs)>1 for cs in m.values()),'complaints':sum(counts.values()),'status':dict(counts),'linked_complaints':len(linked),'linked_unique_contracts':len(set(c for _,c in linked))}
assert sum(counts.values())==2177
print(json.dumps(report,indent=2,ensure_ascii=False))
