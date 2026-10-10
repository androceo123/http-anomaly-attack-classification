"""Verify original artifact hashes without loading serialized models."""
import argparse, hashlib, json
from pathlib import Path

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path('.'),help='Root of tesis_http_organizada')
    p.add_argument('--include-external',action='store_true',help='Require and check the heavy artifact mirror too')
    p.add_argument('--output',type=Path,help='Optional JSON report; does not overwrite an existing file')
    a=p.parse_args();root=a.root.resolve()
    catalog=root/'07_reproducibilidad/catalogo_archivos.json'
    data=json.loads(catalog.read_text(encoding='utf-8'))
    results=[];skipped=0
    for r in data['physical_files']:
        if not r['git_eligible'] and not a.include_external:
            skipped+=1;continue
        target=(root/r['path']).resolve()
        if not target.is_relative_to(root):
            raise ValueError('Path outside archive root')
        status='ok'
        if not target.is_file():status='missing'
        elif target.stat().st_size!=int(r['bytes']):status='size_mismatch'
        elif digest(target)!=r['sha256']:status='sha256_mismatch'
        results.append({'path':r['path'],'status':status})
    failures=[r for r in results if r['status']!='ok']
    report={'checked':len(results),'passed':len(results)-len(failures),'skipped_external':skipped,'failures':failures,'scope':'original retained artifacts; generated documentation has a separate manifest'}
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if failures else 0

if __name__=='__main__':raise SystemExit(main())
