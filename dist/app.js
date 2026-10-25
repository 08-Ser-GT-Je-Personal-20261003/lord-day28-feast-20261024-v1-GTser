(()=>{'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const saved={get:k=>{try{return localStorage.getItem('gtser28-'+k)}catch{return null}},set:(k,v)=>{try{localStorage.setItem('gtser28-'+k,v)}catch{}}};
if(saved.get('theme')==='dark')document.documentElement.dataset.theme='dark';
if(saved.get('big')==='1')document.body.classList.add('big');
const theme=$('#theme');function themeLabel(){if(theme)theme.innerHTML=document.documentElement.dataset.theme==='dark'?'◐ <span>日读</span>':'◐ <span>夜读</span>'}themeLabel();
theme?.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme!=='dark';document.documentElement.dataset.theme=dark?'dark':'light';saved.set('theme',dark?'dark':'light');themeLabel()});
$('#font-size')?.addEventListener('click',()=>{document.body.classList.toggle('big');saved.set('big',document.body.classList.contains('big')?'1':'0')});
$('#print')?.addEventListener('click',()=>window.print());
const toc=$('#toc'),toggle=$('#toc-toggle');function setToc(open){toc?.classList.toggle('open',open);toggle?.setAttribute('aria-expanded',String(open))}
toggle?.addEventListener('click',()=>setToc(!toc.classList.contains('open')));$('#toc-close')?.addEventListener('click',()=>{setToc(false);toggle?.focus()});
$$('#toc a').forEach(a=>a.addEventListener('click',()=>setToc(false)));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){setToc(false);stopStory()}});
document.addEventListener('click',e=>{if(toc?.classList.contains('open')&&!toc.contains(e.target)&&!toggle.contains(e.target))setToc(false)});
let queued=false;function progress(){queued=false;const max=document.documentElement.scrollHeight-innerHeight;$('#progress').style.transform=`scaleX(${max>0?Math.min(1,scrollY/max):0})`}
addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(progress)}},{passive:true});addEventListener('resize',progress);progress();
if('IntersectionObserver'in window){const observer=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){$$('#toc a').forEach(a=>a.classList.toggle('current',a.hash==='#'+e.target.id))}})},{rootMargin:'-15% 0px -65% 0px'});$$('section[data-title]').forEach(s=>observer.observe(s))}
$('#answers-all')?.addEventListener('click',()=>$$('details.answer').forEach(d=>d.open=true));$('#answers-hide')?.addEventListener('click',()=>$$('details.answer').forEach(d=>d.open=false));
const story=[['创造 · 与神相交','神创造人，使人在他面前活着。救赎所恢复的不是一个自我中心的乐园，而是与神和好的生命。'],['堕落 · 罪使人隔绝','人背约犯罪，失去与神的平安；真正的饥饿是罪与死亡的问题，不能靠人的自我改善解除。'],['逾越节 · 代替与出离','出12：审判、羊羔、血、筵席、出发。林前5:7提供明确的正典关联：逾越节羔羊指向基督。'],['十字架 · 一次成全','基督的身体为罪人舍，血为多人流，使罪得赦。来9–10：献祭一次而完全，不需重复支付赎价。'],['圣餐 · 今凭信领受','主日28：圣灵使信徒与在天的基督真实相交。看见、领受、尝到记号，信心因应许得坚固。'],['再来 · 完全相交','太26:29；林前11:26；启19：回望救赎、今得喂养、前望筵席。感恩的人在盼望中行路。']];
let storyIndex=0,storyTimer=null;function renderStory(i){storyIndex=i;$('#story-label').textContent=story[i][0];$('#story-text').textContent=story[i][1];$$('[data-story]').forEach(b=>{b.classList.toggle('active',Number(b.dataset.story)===i);b.setAttribute('aria-pressed',String(Number(b.dataset.story)===i))})}
function stopStory(){if(storyTimer)clearInterval(storyTimer);storyTimer=null;if($('#story-play'))$('#story-play').textContent='▶ 播放救赎脉络'}
$$('[data-story]').forEach(b=>b.addEventListener('click',()=>{stopStory();renderStory(Number(b.dataset.story))}));
$('#story-play')?.addEventListener('click',()=>{if(storyTimer){stopStory();return}renderStory(0);$('#story-play').textContent='Ⅱ 暂停';storyTimer=setInterval(()=>{if(storyIndex===5){stopStory();return}renderStory(storyIndex+1)},4500)});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopStory()});
if($('#story-flow'))renderStory(0);
const quiz=[{q:'问75的第二个应许主要强调什么？',o:['我表现够好就可换取救恩','基督亲自喂养、更新我的灵魂','饼杯自动使所有人得救'],a:1,e:'基督不只成就过去的救赎，也藉圣灵使信徒如今分享他的恩惠。'},{q:'圣餐一再举行，表示什么？',o:['十架献祭尚未足够','每次重新支付赎价','同一完全救恩的恩惠一再施行，信心得坚固'],a:2,e:'重复的是圣礼施行，不是基督献祭；参来10:10–18。'},{q:'“属灵相交”指什么？',o:['圣灵使信徒凭信真实分享基督','纯粹在脑中想象','基督的人性必须无处不在'],a:0,e:'主日28同时承认基督在天、我们在地，也承认圣灵所成就的真实联合。'},{q:'哪一句符合罪—救赎—感恩的次序？',o:['先靠感恩行为赢取赦免','基督救赎我，因此我感恩顺服','有救恩就不必离罪'],a:1,e:'果子不是根；感恩是救恩的结果，而非赎价。'},{q:'《亚他那修信经》作者如何说明最准确？',o:['由亚他那修亲笔署名','由十二使徒共同写作','作者不详，属西方拉丁传统'],a:2,e:'历史通称不能自动当作作者署名；CCI导言也明确区分。'}];
let qi=0,answered=false,score=0;
function renderQuiz(){if(!$('#quiz'))return;answered=false;$('#quiz-question').textContent=`${qi+1} / ${quiz.length} · ${quiz[qi].q}`;$('#quiz-feedback').textContent='';$('#quiz-options').replaceChildren(...quiz[qi].o.map((s,i)=>{const b=document.createElement('button');b.textContent=s;b.addEventListener('click',()=>{if(answered)return;answered=true;const good=i===quiz[qi].a;if(good)score++;$$('#quiz-options button').forEach((x,j)=>{x.disabled=true;if(j===quiz[qi].a)x.classList.add('correct')});if(!good)b.classList.add('wrong');$('#quiz-feedback').textContent=(good?'✓ 正确。':'请再想一想。')+quiz[qi].e;$('#quiz-score').textContent=`本轮答对 ${score} 题`});return b}));$('#quiz-next').textContent=qi===quiz.length-1?'重新一轮 ↻':'下一题 →'}
$('#quiz-next')?.addEventListener('click',()=>{qi=(qi+1)%quiz.length;if(qi===0){score=0;$('#quiz-score').textContent=''}renderQuiz()});renderQuiz();
$$('[data-review]').forEach(c=>{c.checked=saved.get(c.dataset.review)==='1';c.addEventListener('change',()=>saved.set(c.dataset.review,c.checked?'1':'0'))});
const creed=$('#creed-text'),mask=$('#mask-toggle');let masked=false;
const paragraphs=creed?[...creed.querySelectorAll('p')]:[];
mask?.addEventListener('click',()=>{masked=!masked;creed.classList.toggle('masked',masked);mask.setAttribute('aria-pressed',String(masked));mask.textContent=masked?'关闭背诵遮盖':'开启背诵遮盖';paragraphs.forEach((p,i)=>{p.classList.remove('revealed');if(masked){p.tabIndex=0;p.setAttribute('role','button');p.setAttribute('aria-label',`第${i+1}段，按回车揭示`);p.setAttribute('aria-pressed','false')}else{p.removeAttribute('tabindex');p.removeAttribute('role');p.removeAttribute('aria-label');p.removeAttribute('aria-pressed')}})});
paragraphs.forEach((p,i)=>{function reveal(){if(!masked)return;p.classList.toggle('revealed');const visible=p.classList.contains('revealed');p.setAttribute('aria-pressed',String(visible));p.setAttribute('aria-label',visible?`第${i+1}段已揭示，按回车遮盖`:`第${i+1}段，按回车揭示`)}p.addEventListener('click',reveal);p.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();reveal()}})});
$('#speak')?.addEventListener('click',()=>{const status=$('#speech-status');if(!('speechSynthesis'in window)){status.textContent='此终端不支持本机朗读，请使用设备的辅助阅读功能。';return}speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(creed.innerText);u.lang='zh-CN';u.rate=.86;const voice=speechSynthesis.getVoices().find(v=>v.lang.startsWith('zh'));if(voice)u.voice=voice;u.onstart=()=>status.textContent='正在朗读；可随时停止。';u.onend=()=>status.textContent='朗读结束。';u.onerror=()=>status.textContent='本机语音暂不可用，请检查终端语音支持。';status.textContent='正在请求本机语音…';speechSynthesis.speak(u)});
$('#speak-stop')?.addEventListener('click',()=>{if('speechSynthesis'in window)speechSynthesis.cancel();$('#speech-status').textContent='已停止朗读。'});
addEventListener('pagehide',()=>{stopStory();if('speechSynthesis'in window)speechSynthesis.cancel()});
})();
