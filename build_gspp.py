"""Read only the business rows needed for the standalone GSPP dashboard."""
import argparse,datetime,hashlib,json,pathlib
import openpyxl
ROOT=pathlib.Path(__file__).parent

def extract(path):
    wb=openpyxl.load_workbook(path,data_only=True)
    names={}
    for n in wb.sheetnames:
        k=n.strip().casefold()
        if k in names:raise ValueError('Dubbele tabbladnaam: '+n)
        names[k]=n
    def read(name,width,identity,keep):
        if name.casefold() not in names:raise ValueError('Tabblad ontbreekt: '+name)
        sheet=wb[names[name.casefold()]];rows=[];ignored=0
        expected={1:'INV Boekperiode',4:'INVpos Artikelnr',6:'PO Leverancier',8:'POpos Contractnr',19:'GSPP?',23:'GEWICHT CIRC. BEKEND Rec In',26:'TOTAAL GEWICHT'} if name=='Kernassets' else {3:'Datum paspoort',5:'Leveranciernummer',6:'Artikelnummer'}
        for col,label in expected.items():
            if str(sheet.cell(1,col).value).strip().casefold()!=label.casefold():raise ValueError(f'{name}: verwachte kolom {col} ({label}) ontbreekt')
        for cells in sheet.iter_rows(min_row=2,max_col=width):
            if not any(cells[i].value is not None for i in identity):ignored+=1;continue
            v=[]
            for i,c in enumerate(cells):
                value=c.value if i in keep else None
                if isinstance(value,(datetime.datetime,datetime.date)):value=value.isoformat()
                if c.data_type=='e' and i in keep:value={'error':value}
                v.append(value)
            rows.append({'row':cells[0].row,'v':v})
        return rows,ignored
    k,ki=read('Kernassets',34,[0,3,5,7],{0,2,3,4,5,6,7,10,17,18,20,22,25,26,29,32,33})
    p,pi=read('GSPP inkopen',18,[0,4,5],{0,1,2,3,4,5,7,17})
    return {'purchases':k,'passports':p,'meta':{'file':pathlib.Path(path).name,'sha256':hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest(),'ignoredPurchaseRows':ki,'ignoredPassportRows':pi}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('excel');args=parser.parse_args();raw=extract(args.excel)
    html=(ROOT/'gspp.template.html').read_text().replace('/* GSPP_APP */',(ROOT/'gspp.js').read_text()).replace('/* GSPP_DATA */',json.dumps(raw,ensure_ascii=False).replace('</','<\\/')).replace('/* EXCEL_PARSER */',(ROOT/'vendor/xlsx.full.min.js').read_text())
    (ROOT/'Alliander_SRS_GSPP_Dashboard.html').write_text(html)
    print(json.dumps({'records':{k:len(raw[k]) for k in ['purchases','passports']},'meta':raw['meta']},ensure_ascii=False))
