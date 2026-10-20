"""Build a self-contained dashboard; optionally embed a validated Excel source."""
import argparse, json, datetime, pathlib, collections
import openpyxl
from zoneinfo import ZoneInfo
ROOT=pathlib.Path(__file__).parent

def extract(path):
    formulas=openpyxl.load_workbook(path,data_only=False)
    wb=openpyxl.load_workbook(path,data_only=True)
    starts={'Q2&3':2,'S1':7,'S2':8,'S3':12}
    result={}
    for name,start in starts.items():
        if name not in wb.sheetnames: raise ValueError(f'Tabblad ontbreekt: {name}')
        rows=[]
        for row in wb[name].iter_rows(min_row=start,max_col={'Q2&3':33,'S1':7,'S2':6,'S3':9}[name]):
            if not any(c.value is not None for c in row): continue
            if name=='S1' and str(row[0].value).strip().lower()=='naam': continue
            vals=[]
            for c in row:
                v=c.value
                if isinstance(v,datetime.datetime): v=v.replace(tzinfo=ZoneInfo('Europe/Amsterdam')).isoformat()
                elif isinstance(v,(datetime.date,datetime.time)): v=v.isoformat()
                elif isinstance(v,datetime.timedelta): v=v.total_seconds()/86400
                if c.data_type=='e': v={'error':v}
                if v is None and formulas[name][c.coordinate].data_type=='f': v={'error':'Formule-uitkomst ontbreekt'}
                vals.append(v)
            rows.append({'row':row[0].row,'v':vals})
        result[name]=rows
    mapping_sheet=next((s for s in wb if s.title.strip().casefold() in ('contact artikel mapping','contract artikel mapping')),None)
    if mapping_sheet is not None:
        if [str(mapping_sheet.cell(1,c).value).strip().casefold() for c in (1,2)]!=['inkoopcontract','artikel']:
            raise ValueError('Contractmapping: verwacht kolommen Inkoopcontract en Artikel')
        result['ContractMapping']=[{'row':i,'v':[c.value if c.data_type!='e' else {'error':c.value} for c in row]} for i,row in enumerate(mapping_sheet.iter_rows(min_row=2,max_col=3),2) if any(c.value is not None for c in row)]
    complaints=[r for r in result['Q2&3'] if str(r['v'][3]).strip().lower()=='klacht']
    print(json.dumps({'records':{k:len(v) for k,v in result.items()},'klachten':len(complaints),'afgesloten_met_datum':sum(r['v'][17]=='5. Afgemeld' and bool(r['v'][30]) for r in complaints)},ensure_ascii=False))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('excel'); a=p.parse_args()
    data=extract(a.excel) if a.excel else None
    parser=(ROOT/'vendor/xlsx.full.min.js').read_text()
    template=(ROOT/'dashboard.template.html').read_text()
    out=template.replace('/* EXCEL_PARSER */',parser).replace('/* EMBEDDED_DATA */',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    (ROOT/'Alliander_SRS_Dashboard.html').write_text(out)
    print('HTML geschreven; brondata '+('ingebed' if data else 'ontbreekt'))
