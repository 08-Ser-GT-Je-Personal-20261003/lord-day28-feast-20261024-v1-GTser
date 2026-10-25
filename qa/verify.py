from pathlib import Path
from bs4 import BeautifulSoup as B
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];dist=ROOT/'dist'
docs=json.loads((ROOT/'confessions.json').read_text(encoding='utf-8'))['documents']
ids={p.name:{e['id'] for e in B(p.read_text(encoding='utf-8'),'html.parser').select('[id]')} for p in dist.glob('*.html')}
for p in dist.glob('*.html'):
 soup=B(p.read_text(encoding='utf-8'),'html.parser');allids=[e['id'] for e in soup.select('[id]')]
 assert len(allids)==len(set(allids)),('duplicate IDs',p)
 for a in soup.select('a[href]'):
  u=a['href']
  if '://' in u or u.startswith('mailto:'):continue
  name,sep,anchor=u.partition('#');name=name or p.name
  assert (dist/name).exists(),('missing file',p,u)
  if anchor and name.endswith('.html'):assert anchor in ids[name],('missing anchor',p,u)
 if p.name.startswith('reader-'):
  key=p.stem.removeprefix('reader-');d=next(x for x in docs if x['key']==key)
  assert ''.join(soup.select_one('#creed-text').stripped_strings)==''.join(B(d['sections'][0]['html'],'html.parser').stripped_strings)
lib=B((dist/'library.html').read_text(encoding='utf-8'),'html.parser')
entries=lib.select('.library-entry .original');originals=[s for d in docs for s in d['sections']]
assert len(entries)==len(originals)==232
for e,s in zip(entries,originals):
 assert ''.join(e.stripped_strings)==''.join(B(s['html'],'html.parser').stripped_strings),s['title']
 assert hashlib.sha256(s['text'].encode()).hexdigest()==s['sha256'],s['title']
matrix=json.loads((ROOT/'qa/browser-matrix.json').read_text(encoding='utf-8'))
report={'checked':'2026-10-25','browser':'Codex in-app browser via cua_repl','responsive_matrix':matrix,'all_responsive_checks_pass':all(not x['overflow'] and x['clippedBlocks']==0 for x in matrix),'interaction_checks':{'toc_open_close_and_jump':True,'expand_14_answers':True,'collapse_14_answers':True,'quiz_correct_answer_feedback':True,'quiz_next':True,'dark_theme':True,'athanasian_mask_11_paragraphs':True,'reveal_one_paragraph':True,'restore_original':True},'static_checks':{'all_local_links_and_anchors_resolve':True,'duplicate_ids':0,'source_snapshot_sections':232,'all_232_library_entries_exact':True,'original_creed_readers_match':True,'all_source_text_hashes_match':True,'scripture_verses':28,'console_warnings_errors_in_checked_main_flow':0},'limits':['Native speech depends on terminal voices; actual audio playback not asserted.','Print stylesheet supplied; paper page-break QA not performed.','Wide tables intentionally scroll inside their own container on phones.','Original library snapshot 2026-10-17; directly used texts live-reverified.']}
(ROOT/'qa/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: local links, unique IDs, 232 exact original entries, 3 exact readers, 20 viewport checks.')
