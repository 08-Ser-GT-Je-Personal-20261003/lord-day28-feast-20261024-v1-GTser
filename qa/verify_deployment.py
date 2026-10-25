from pathlib import Path
import requests,json,hashlib,concurrent.futures,subprocess
ROOT=Path(__file__).resolve().parents[1]
slug='lord-day28-feast-20261024-v1-GTser';org='08-Ser-GT-Je-Personal-20261003'
targets={'github_pages':f'https://{org.lower()}.github.io/{slug}/','surge':f'https://{slug.lower()}.surge.sh/'}
files=['index.html','library.html','reader-apostles.html','reader-nicene.html','reader-athanasian.html','style.css','app.js','assets/table.svg','assets/mark.svg','source-verification.json']
def canon(raw):return raw.replace(b'\r\n',b'\n')
def check(item):
 platform,base,name=item;r=requests.get(base+name,timeout=40)
 expected=(ROOT/'dist'/name).read_bytes()
 actual=hashlib.sha256(canon(r.content)).hexdigest();want=hashlib.sha256(canon(expected)).hexdigest()
 return {'platform':platform,'url':base+name,'status':r.status_code,'matches_local_except_line_endings':actual==want,'sha256':actual}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:checks=list(pool.map(check,[(k,v,f) for k,v in targets.items() for f in files]))
result={'checked':'2026-10-25','release':'v1.0.0','version_name_date':'2026-10-24 (draft started)','repo':f'https://github.com/{org}/{slug}','content_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'public_urls':targets,'checks':checks,'all_pass':all(c['status']==200 and c['matches_local_except_line_endings'] for c in checks)}
(ROOT/'deployment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'all_pass':result['all_pass'],'checked_files':len(checks),'failures':[c for c in checks if c['status']!=200 or not c['matches_local_except_line_endings']]},ensure_ascii=False))
assert result['all_pass'],'Deployment differs from local source'
