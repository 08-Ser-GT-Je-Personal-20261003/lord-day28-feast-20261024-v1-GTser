from pathlib import Path
import json, re, html, hashlib, concurrent.futures
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True)
SLUG='lord-day28-feast-20261024-v1-GTser'
ORG='08-Ser-GT-Je-Personal-20261003'
REPO=f'https://github.com/{ORG}/{SLUG}'
PAGES=f'https://{ORG.lower()}.github.io/{SLUG}/'
SURGE=f'https://{SLUG.lower()}.surge.sh/'
source_file=ROOT/'confessions.json'
if not source_file.exists():source_file=ROOT.parent/'research/fulltexts.json'
data=json.loads(source_file.read_text(encoding='utf-8'))
docs={x['key']:x for x in data['documents']}

questions=[
('1 · 信息','为什么先读出埃及记12章，再读马太福音26章？',
 '两段并读使我们看见“审判—代替—得救—筵席—出发”的脉络。出12记真实的历史救赎；林前5:7明确把逾越节羔羊与基督关联，太26则由主亲自解释自己的身体和血。不是讲道人凭相似细节编故事，而是沿正典已经提供的方向理解成全。',
 '核心经文：出12:12–14；太26:28；林前5:7。追问：如果只讲温暖的团契聚餐，哪些关于罪与赦免的内容会消失？'),
('2 · 两个应许','问75的两个应许有什么区别，为什么缺一不可？',
 '第一个应许把信徒的确据放在已经发生的救赎上：基督为我舍身流血。第二个应许把现在持续的滋养放在活着的基督身上：他亲自喂养更新我。一个不是抽象历史知识，另一个不是没有历史根基的情绪体验；二者同属一位救主的恩典。',
 '可用一句话复述：他已经为我成就，他今天使我有份。两者不等同于两次献祭，也不是两套救法。'),
('3 · 一次献祭','若十字架已经完全，为什么还要一再领圣餐？',
 '一次献祭解决的是救恩根基是否充足；一再领餐面对的是信徒在今生持续需要被坚固。圣餐不增加基督的功德，乃表明并印证同一应许，由圣灵使我们凭信分享同一基督。神也藉圣道圣礼保守我们，并未因预定终局就取消过程。',
 '核心经文：来10:10–18；林前11:26。认信关联：问75；多特第五项14条。错误答案：“每次再赎一点罪。”'),
('4 · 圣灵与信心','“属灵地吃喝”是不是只在脑中想象？',
 '不是。“属灵”指圣灵施行，而非所领受的是虚构。我们用口吃喝记号，以信心领受记号所表明的基督。信心不是使礼物变真实的创造力，而是领受者依赖应许；真实性根于基督的设立与圣灵的工作。',
 '核心经文：林前10:16–17；问76。追问：如果只说“我想起耶稣”，会遗漏“基督亲自喂养”中的哪个主体？'),
('5 · 升天的主','基督在天上，为什么不是与我们分离？',
 '升天说明他的真实人性与尊荣，不说明救恩联系中断。同一位圣灵住在基督和信徒里面，使我们与整位基督联合。我们不必使他的人性无限化，才能肯定真实相交；也不把他的人性当成仅能远观的往事。',
 '核心经文：徒3:21；西3:1–4；问76。信经关联：升天、父右边、再来，以及一位基督真实的神人二性。'),
('6 · 省察','“不配”与“不按理”有什么不同？',
 '没有人凭自身功德配得救主；但林前11警告的是不合宜的吃喝方式，包括轻慢主、破坏身体的相交。省察旨在悔改并照主命令吃喝，不是找到一个不再有罪的人。把普遍不配当作永远不领餐的理由，与把普遍有罪当作不必悔改的理由，都走偏了。',
 '核心经文：林前11:17–34，尤其28节“然后吃”；参问81–82。实际处理仍须当地教会牧养与监督。'),
('7 · 情境：恐惧','有人说：“我这周又失败了，我没有资格来。”怎样回应？',
 '先听清具体罪与态度，不能只给口号。若他忧伤、认罪、信靠基督并愿意改变，应引他从自我资格转向主的应许，提醒圣餐为坚固软弱信徒而设。若涉及需要赔偿、止害、纪律的具体事情，也要真实处理，安慰不等于取消责任。',
 '分辨重点：软弱是否被带到基督面前，还是被用来继续遮掩。可以问：“你正倚靠谁？你愿意怎样离弃这个罪？”不要要求他先达到无罪。'),
('8 · 情境：顽梗','有人公开伤害别人，拒绝悔改，却说“圣餐是恩典，谁都不能拦我”，怎么办？',
 '恩典的应许不能被拿来保护对主的顽梗。教会应劝戒、查明情况并按圣经和教会秩序施行监督；目标是悔改、挽回和保护会众。不是由旁人私下武断判定其永恒结局，也不是用“人人有罪”抹去持续不悔改的区别。',
 '核心经文：太18:15–20；林前5；11:27–32；主日30。谨防两种错误：漠视罪，或把纪律当报复。'),
('9 · 一个身体','为什么一个人领餐的态度，与他对穷人的态度有关？',
 '林前11的背景包含聚会分裂、有人饥饿、有人醉酒，羞辱没有的人。林前10:17又把同受一个饼与一个身体相连。因此领餐不能被封闭成私人的宗教感受。接受基督的施予，必挑战我对同属基督之人的轻看。',
 '行动问题：教会中的时间安排、饭食、探访、经济支援，是否让弱者实际被记念？这些行动不是赚取圣餐，而是认识圣餐的结果。'),
('10 · 圣约','既有恩典之约的统一，为什么旧约礼规不全部直接搬过来？',
 '统一在同一位救主、同一恩典与信心的救法；差异在救赎历史阶段、预表与成全、主亲自规定的新约施行。连续性不等于所有细节相同。参与资格必须按新约整全教导辨明，不能只从逾越节家庭参与直接跳到圣餐结论。',
 '核心经文：林前10–11；来8–10。说明时同时问：“什么持续？什么因基督成全而改变？新约具体怎样吩咐？”'),
('11 · 感觉','领餐时没有特别感动，是不是没有领受任何恩惠？',
 '不能从缺乏强烈感受直接下这个结论。圣礼的真实性在主的设立与应许，不在情绪峰值；但也不可对麻木、例行公事从不省察。应持守听道、祷告、悔改与群体生活，求主使信心成长，而非追逐可复制的宗教刺激。',
 '问75–76；多特第五项11、14条可作拓展。恩惠常以更持久的信靠、悔改与爱逐渐显明，不能用一次体验为神工作规定形式。'),
('12 · 三大信经','三份信经怎样帮助我们理解这桌子？它们是不是圣餐礼文？',
 '它们首先说明我们所信的神与基督是谁：三一神、真正的神子、真实成为人、受难、复活、升天、再来。若救主不是神，他不能成为完全救主；若他没有真实人性，他就没有真实为我们舍身。它们不是完整的圣餐礼文，不能直接从其沉默中读出全部礼规。',
 '辨识练习：使徒信经突出救恩叙事；尼西亚信经界定子与灵的神性；亚他那修信经严谨划定三一与二性的边界。'),
('13 · 文本忠实','为什么信条引句必须原样，而讲解又可以用自己的话？',
 '引用承担“这份文件就是这样说”的责任；讲解承担“我如何理解它”的责任。若把二者混在一起，就无法检验解释是否忠于原文。网站因此保留CCI字词与标点，编者认为需要说明的排字或历史问题放在区块以外，不静默修正。',
 '实际练习：分别找一句圣经明言、一个正典关联、一项历史推断、一句牧养应用。它们应共同服务真理，却不能声称有同一种证据等级。'),
('14 · 救赎闭环','请用“罪—救赎—感恩”概括整篇，为什么次序不能倒转？',
 '罪：我在审判下、不能自救。救赎：基督一次舍己，圣灵使我凭信分享他的恩惠。感恩：我省察领受、爱神爱人、盼望再来。若把感恩放在赎罪之前，就把果子变为根；若救赎之后永无感恩，就把活的联合降格成无生命的标签。',
 '结束讨论：本周一项具体悔改、一项具体关爱、一次对主应许的复述。不要用行动清单代替信靠基督；让行动从领受而来。')
]

def esc(s):return html.escape(s,quote=True)
def safe_id(doc,s,i):
 if doc=='heidelberg':return f'heidelberg-{i+1}'
 if doc=='belgic':return f'belgic-{i+1}'
 if doc=='dort':
  m=re.search(r'/section([^/]+)/(\d+)$',s['source']);return 'dort-'+m.group(1)+'-'+m.group(2)
 return doc

def head(title):
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="海德堡要理问答主日28：原创欧陆改革宗讲章、历史背景、逐段释经、六份认信原典与讨论。"><title>{esc(title)} · GTser</title><link rel="icon" href="assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="app.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><div id="progress" aria-hidden="true"></div>'''
def toolbar(back=False):
 return f'''<header class="topbar"><a class="brand" href="index.html"><img src="assets/mark.svg" width="30" height="30" alt=""> GTser <span>· 主日28</span></a><div class="tools">{'<a href="index.html#creeds">← 返回讲章</a>' if back else '<button id="toc-toggle" aria-controls="toc" aria-expanded="false">☰ 目录</button>'}<button id="theme" aria-label="切换深浅主题">◐ <span>夜读</span></button><button id="font-size" aria-label="切换正文字号">A＋</button><button id="print">打印</button></div></header>'''
def footer():return f'<footer><b>GTser · 主日28</b><p>2026.10.24 / v1.0.0 · 原创讲章与教学图示</p><a href="{REPO}">源码与版本</a> · <a href="index.html#sources">来源说明</a><p>主以应许喂养，我们以感恩回应。</p></footer><a class="to-top" href="#" aria-label="回到顶部">↑</a></body></html>'

def quote(s):return f'<div class="source-quote"><a class="source-label" href="{s["source"]}" target="_blank" rel="noopener">CCI 原文 ↗</a><div class="original">{s["html"]}</div></div>'

# Fresh checks operate on exact textual fragments without modifying the source snapshot.
selected=[(k,s) for k in ['apostles','nicene','athanasian'] for s in docs[k]['sections']]
selected += [('heidelberg',s) for s in docs['heidelberg']['sections'] if s.get('lord_day')==28]
selected += [('belgic',docs['belgic']['sections'][34])]
dort14=next(s for s in docs['dort']['sections'] if s['source'].endswith('/section5/14'))
selected += [('dort',dort14)]
def check_url(url):
 r=requests.get(url,timeout=40);r.raise_for_status();soup=BeautifulSoup(r.content,'html.parser')
 return soup,hashlib.sha256(r.content).hexdigest()
urls=list(dict.fromkeys(s['source'] for _,s in selected))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: fetched=dict(zip(urls,pool.map(check_url,urls)))
checks=[]
for key,s in selected:
 soup,rawhash=fetched[s['source']]
 if key in ['apostles','nicene','athanasian']:el=soup.select_one('.article-body .alert-primary')
 elif key=='heidelberg':
  num=re.match(r'\d+',s['title']).group();el=next(x for x in soup.select('#block-tulip-content .entity-reference > span > article') if x.select_one('h4').get_text().strip().startswith(num))
 else:el=soup.select_one('#block-tulip-content > article > div')
 for nav in el.select('nav,script,style'):nav.decompose()
 live=''.join(el.stripped_strings)
 frozen=''.join(BeautifulSoup(s['html'],'html.parser').stripped_strings)
 ok=re.sub(r'\s+','',live)==re.sub(r'\s+','',frozen)
 checks.append({'document':key,'section':s['title'],'url':s['source'],'matches_after_layout_whitespace_only':ok,'snapshot_text_sha256':s['sha256'],'live_raw_sha256':rawhash})
 if not ok:raise RuntimeError('Live source mismatch: '+s['title'])
(DIST/'source-verification.json').write_text(json.dumps({'checked':'2026-10-25','snapshot':'2026-10-17','policy':'Word choices, punctuation, numbering retained; layout whitespace excluded for live comparison.','checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')

scripture_file=ROOT/'scriptures.json'
if scripture_file.exists():scriptures=json.loads(scripture_file.read_text(encoding='utf-8'))
else:
 scriptures=[]
 for title,search,book,chapter,start,end in [('马太福音26:17–30','Matthew%2026%3A17-30','Matt',26,17,30),('出埃及记12:1–14','Exodus%2012%3A1-14','Exod',12,1,14)]:
  url=f'https://www.biblegateway.com/passage/?search={search}&version=CUVS'
  r=requests.get(url,timeout=40);r.raise_for_status();soup=BeautifulSoup(r.content,'html.parser');verses=[]
  for n in range(start,end+1):
   spans=soup.select(f'.passage-text span.text.{book}-{chapter}-{n}')
   assert spans,(title,n)
   fragments=[]
   for span in spans:
    for remove in span.select('sup,.crossreference,.footnote'):remove.decompose()
    fragments.append(re.sub(r'\s+','',span.get_text()))
   verses.append({'number':n,'text':''.join(fragments)})
  scriptures.append({'title':title,'source':url,'version':'CUVS','verses':verses})
 scripture_file.write_text(json.dumps(scriptures,ensure_ascii=False,indent=2),encoding='utf-8')
body=(ROOT/'content.html').read_text(encoding='utf-8')
body=body.replace('{{SCRIPTURES}}',''.join('<article class="scripture"><h3>'+s['title']+'</h3>'+''.join(f'<p><sup>{v["number"]}</sup> {esc(v["text"])}</p>' for v in s['verses'])+'</article>' for s in scriptures))
body=body.replace('{{HEIDELBERG28}}',''.join(quote(s) for s in docs['heidelberg']['sections'] if s.get('lord_day')==28))
belgic=docs['belgic']['sections'][34]
belgic_p=BeautifulSoup(belgic['html'],'html.parser').find('p')
body=body.replace('{{BELGICQUOTE}}',f'<div class="original">{belgic_p}</div>')
body=body.replace('{{DORT14}}',f'<div class="original">{dort14["html"]}</div>')
body=body.replace('{{DISCUSSIONS}}',''.join(f'<article class="question"><span>{esc(cat)}</span><h3>{esc(q)}</h3><details class="answer"><summary>查看答案与分析</summary><p>{esc(a)}</p><p class="note">{esc(note)}</p></details></article>' for cat,q,a,note in questions))
for k,v in [('PAGES',PAGES),('SURGE',SURGE),('REPO',REPO)]:body=body.replace('{{'+k+'}}',v)
assert '{{' not in body
soup=BeautifulSoup(body,'html.parser')
toc=''
for s in soup.select('section[data-title]'):
 toc+=f'<a href="#{s["id"]}">{esc(s["data-title"])}</a>'
 if s['id']=='sermon':toc+=''.join(f'<a class="toc-sub" href="#{h["id"]}">{esc(h.get_text().split("：")[0])}</a>' for h in s.select('h3[id]'))
hero='''<div class="hero"><div class="hero-copy"><span class="eyebrow">海德堡要理问答 · 主日28</span><h1>为你舍下，<br>使你得饱足。</h1><p>基督在他的筵席上<br>丰丰富富地喂养我们的灵魂</p><div class="hero-meta"><span>马太福音26:17–30</span><span>出埃及记12:1–14</span><span>2026.10.24 · V1</span></div><a class="button" href="#sermon">进入讲章 ↓</a><a class="text-button" href="#orientation">先看整体 →</a></div><figure class="hero-art"><img src="assets/table.svg" alt="原创象征插图：桌上的饼和杯，背后是光中的十字架" width="700" height="540"><figcaption>一次献祭的恩惠，今日仍真实施予。</figcaption></figure></div>'''
index=head('基督在他的筵席上丰丰富富地喂养我们的灵魂')+toolbar()+f'<aside id="toc" aria-label="章节目录"><div class="toc-head"><b>阅读目录</b><button id="toc-close" aria-label="关闭目录">×</button></div>{toc}<a href="library.html">▤ 六份认信原典库</a><small>原文与讲解分开 · 点击章节跳转</small></aside><main id="main">'+hero+body+'</main>'+footer()
(DIST/'index.html').write_text(index,encoding='utf-8')

for key in ['apostles','nicene','athanasian']:
 d=docs[key];s=d['sections'][0]
 reader=head(d['title']+' · 干净阅读版')+toolbar(True)+f'''<main id="main" class="reader"><div class="reader-heading"><span class="eyebrow">CCI 中文原文 · 干净阅读版</span><h1>{d['title']}</h1><p>先读全文，再遮盖回忆；再点原段，即可恢复。</p><div class="reader-tools"><button id="mask-toggle" aria-pressed="false">开启背诵遮盖</button><button id="speak">▷ 朗读</button><button id="speak-stop">停止</button><a href="{s['source']}" target="_blank" rel="noopener">CCI来源 ↗</a></div><p id="speech-status" class="note" aria-live="polite"></p></div><article class="creed-clean original" id="creed-text">{s['html']}</article><div class="reader-end"><p>背诵工具只改变显示，不改动正文。点击每段可暂时揭示；键盘也可操作。打印时自动恢复全部文字并隐藏工具。</p><a href="index.html#creeds">三经比较与历史背景 →</a><a href="library.html#{key}">完整原典库 →</a></div></main>'''+footer()
 (DIST/f'reader-{key}.html').write_text(reader,encoding='utf-8')

library=head('六份认信原典库')+toolbar(True)+'''<main id="main" class="library"><div class="section-head"><span>THE CONFESSIONAL LIBRARY</span><h1>六份认信原典库</h1><p>CCI网站中文文本 · 2026年10月17日快照</p></div><p>保留原站字词、标点、脚注上标与参考经文。原典正文未以本讲解释改写。三份信经及本讲直接引用章节于2026年10月25日再核；其他章节不宣称全部在当天重新抓取。多特范围按该站收录的59条正面教义与4组驳谬，未擅补其他译本的独立结语。</p><nav class="library-nav" aria-label="原典目录">'''+''.join(f'<a href="#{k}">{d["title"]}</a>' for k,d in docs.items())+'</nav>'
for key,d in docs.items():
 library+=f'<section id="{key}"><h2>{d["title"]}</h2>'
 for i,s in enumerate(d['sections']):
  sid=safe_id(key,s,i)
  # Creed parent already uses its canonical anchor.
  anchor=f' id="{sid}"' if sid!=key else ''
  library+=f'<article class="library-entry"{anchor}><h3>{esc(s["title"])}</h3><a class="source-label" href="{s["source"]}" target="_blank" rel="noopener">CCI原文来源 ↗</a><div class="original">{s["html"]}</div></article>'
 library+='</section>'
library+='</main>'+footer()
(DIST/'library.html').write_text(library,encoding='utf-8')

# Deliver only source texts needed by this independent project; no older project metadata.
(ROOT/'confessions.json').write_text(json.dumps({'snapshot_date':'2026-10-17','source':'https://ccifellowship.org','documents':data['documents']},ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'package.json').write_text(json.dumps({'name':SLUG.lower(),'version':'1.0.0','private':True,'scripts':{'build':'python build.py','preview':'python -m http.server 4188 -d dist'}},indent=2),encoding='utf-8')
(ROOT/'.gitignore').write_text('__pycache__/\nnode_modules/\nqa/*.png\ndist/CNAME\n',encoding='utf-8')
(DIST/'.nojekyll').touch()
readme=f'''# 主日28 · 基督在他的筵席上丰丰富富地喂养我们的灵魂

2026-10-24 · v1.0.0 · GTser

| 链接 | 地址 |
| --- | --- |
| GitHub Pages | {PAGES} |
| Surge | {SURGE} |
| 源码仓库 | {REPO} |

## 内容

原创欧陆改革宗讲章，按“喂养的信息、方式、吩咐”展开；含历史与上下文、逐段释经、救赎历史与圣约脉络、三经比较、14组讨论与答案、复习自测。六份认信原典来源统一为CCI，三经另有干净阅读与背诵页。原典库不是原创译文。

## 运行与维护

Python 3；安装 `requests beautifulsoup4`，运行 `python build.py`。构建会从CCI在线复核本讲引用章节；网络或原文差异会导致构建停止，防止静默替换。`python -m http.server 4188 -d dist` 预览。直接发布 `dist/`，无运行时依赖、无密钥、无数据库。

源码内容为 `content.html`；构建逻辑 `build.py`；认信规范快照 `confessions.json`；样式与交互位于 `dist/style.css`、`dist/app.js`，原创SVG在 `dist/assets/`。首次构建复用项目参考资料，独立仓库后续构建读取本仓库的 `confessions.json`。

GitHub Pages由工作流发布dist。Surge手动部署dist至上表域名。账号凭据不得写入源码、README或日志。

## 原文与验证

原文快照日期2026-10-17；本讲直接引用的三经、海德堡75–77、比利时35、多特第五项14于2026-10-25在线比对，记录在 `dist/source-verification.json`。原文词语标点不修改，版面空白单独处理。其余原典章节不宣称当天重抓。完整范围按CCI收录，不补其他译本结语。版本名日期保留起稿日2026-10-24，发布核验日期另见deployment.json。

浏览器验证见 `qa/report.json`；部署最终验证见 `deployment.json`。历史推断与经文明言分开；原创地图非比例、非考古复原。圣诗编号按用户原大纲保留，未猜测未指定诗本歌词。

所有原创讲解、图示可作为学习资料；认信译文权利归相关权利人，不对第三方译文附加本项目许可证。
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print(json.dumps({'pages':len(list(DIST.glob('*.html'))),'source_checks':len(checks),'all_match':all(x['matches_after_layout_whitespace_only'] for x in checks),'sermon_characters':len(BeautifulSoup(body,'html.parser').select_one('.sermon-body').get_text()),'total_content_characters':len(BeautifulSoup(body,'html.parser').get_text())},ensure_ascii=False))
