"""Package recorded browser evidence; this does not perform a new browser audit.

Refresh qa/remote-browser.json through cua_repl before reusing for a new release.
The evidence compares headings, paragraphs and table cells in the rendered DOM,
excluding the dynamic quiz, after removing layout whitespace. It is not a binary
file hash check. All 232 original library entries have a separate exact test.
"""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
slug='lord-day28-feast-20261024-v1-GTser';org='08-Ser-GT-Je-Personal-20261003'
targets={'github_pages':f'https://{org.lower()}.github.io/{slug}/','surge':f'https://{slug.lower()}.surge.sh/'}
checks=json.loads((ROOT/'qa/remote-browser.json').read_text(encoding='utf-8'))
assert len(checks)==10 and all(c['rendered_content_matches_local'] for c in checks)
result={'checked':'2026-10-25','release':'v1.0.0','version_name_date':'2026-10-24 (draft started)','repo':f'https://github.com/{org}/{slug}','content_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'public_urls':targets,'verification_method':'cua_repl browser navigation and DOM text comparison for all 5 pages on both hosts; whitespace ignored, dynamic quiz excluded','checks':checks,'all_public_page_text_checks_pass':True,'github_pages_workflow':{'run_id':40146695682,'content_head':'bb80a2033019e7a0dcd0e3119768112d46971077','status':'success'},'limits':['A separate Python batch binary-download attempt hit local TLS/proxy timeouts; browser page verification replaced it. No remote binary-equality claim.','Browser source comparison is recorded evidence, not a live network test when this script is rerun.']}
# Resolve the actual recorded workflow identity from GitHub rather than invent it.
runs=json.loads(subprocess.check_output(['gh','run','list','--limit','3','--json','databaseId,status,conclusion,headSha'],cwd=ROOT,text=True))
run=next(r for r in runs if r['headSha']==result['github_pages_workflow']['content_head'])
assert run['status']=='completed' and run['conclusion']=='success'
result['github_pages_workflow']['run_id']=run['databaseId']
(ROOT/'deployment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 10 publicly rendered pages match local text; GitHub Pages workflow succeeded.')
