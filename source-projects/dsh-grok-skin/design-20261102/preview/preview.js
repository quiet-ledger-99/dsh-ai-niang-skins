(async()=>{
const $=s=>document.querySelector(s),cfg=window.skinPreview;
const names={home:cfg.short,chat:'设计与阅读',question:'询问 · 下一步',approval:'审批 · 操作范围',icons:'配套器物图标'};
function view(name){for(const k of Object.keys(names))$('#'+k).hidden=k!==name&&!(k==='chat'&&['question','approval'].includes(name));$('#composer').hidden=name==='icons';$('#page-title').textContent=names[name];document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===name)));document.body.classList.remove('drawer');$('#account-menu').hidden=true;}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));document.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>view(b.dataset.target));$('#new').onclick=()=>view('home');
$('#menu').onclick=()=>document.body.classList.toggle('drawer');$('.scrim').onclick=()=>document.body.classList.remove('drawer');
$('#search-toggle').onclick=()=>{$('#search').hidden=!$('#search').hidden;if(!$('#search').hidden)$('#search').focus();};$('#search').oninput=e=>document.querySelectorAll('._sessionRow').forEach(s=>s.hidden=!s.textContent.includes(e.target.value));
let motionOn=true;const video=document.querySelector('video');
function motion(on){motionOn=on;if(on&&!document.hidden)video.play().catch(()=>{});else video.pause();$('#motion').textContent='动效 '+(on?'开':'关');$('#motion').setAttribute('aria-pressed',String(on));$('#motion-check').checked=on;}
document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else if(motionOn)video.play().catch(()=>{});});
$('#motion').onclick=()=>motion(!motionOn);$('#motion-check').onchange=e=>motion(e.target.checked);
function reading(on){document.body.classList.toggle('reading',on);$('#reading-check').checked=on;}$('#read').onclick=()=>reading(!document.body.classList.contains('reading'));$('#reading-check').onchange=e=>reading(e.target.checked);
$('#account').onclick=()=>$('#account-menu').hidden=!$('#account-menu').hidden;$('#settings').onclick=()=>{$('#account-menu').hidden=true;$('#settings-dialog').showModal();};
function toast(t){$('#toast').textContent=t;$('#toast').hidden=false;clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>$('#toast').hidden=true,2600);}
document.querySelectorAll('.local-action').forEach(b=>b.onclick=()=>toast('这是离线样例，没有执行操作。'));
document.querySelectorAll('[role=radio]').forEach(b=>b.onclick=()=>document.querySelectorAll('[role=radio]').forEach(r=>{r.setAttribute('aria-checked',String(r===b));r.querySelector('i').textContent=r===b?'✓':'';}));
$('#permission').onclick=()=>view('approval');$('[data-composer-input]').oninput=e=>$('.send').disabled=!e.target.value.trim();$('#composer').onsubmit=e=>{e.preventDefault();toast('这段文字仅保留在预览页面，没有发送。');};
const iconMap=await (await fetch('../skin/'+cfg.id+'/assets/ui/icon-map.json')).json();
function paintedIcon(name,classes=''){
 const spec=iconMap.icons[name],im=document.createElement('span');
 im.className='raster-icon '+classes;im.setAttribute('aria-hidden','true');im.dataset.skinIcon=name;
 im.style.backgroundImage="url('../skin/"+cfg.id+"/assets/ui/"+spec.atlas+"')";
 im.style.backgroundPosition=(spec.column/3*100)+'% '+(spec.row/2*100)+'%';
 return im;
}
document.querySelectorAll('[data-icon]').forEach(old=>old.replaceWith(paintedIcon(old.dataset.icon,old.className)));
const icons=[['plugins','插件'],['schedules','自动化任务'],['board','任务看板'],['memory','记忆系统'],['more','更多'],['search','搜索'],['filter','视图选项'],['add-workspace','添加工作区'],['folder','文件夹'],['folder-open','已展开文件夹'],['pair-phone','手机配对'],['remote-access','远程访问'],['settings','设置'],['feedback','意见反馈'],['logout','退出登录'],['login','登录'],['attach','附件'],['permission','权限'],['send','发送'],['model','模型'],['preset','预设']];
icons.push(['crest','主题徽记'],['new-session','新会话'],['close','关闭']);
for(const [id,label] of icons){
 const tile=document.createElement('div');tile.className='icon-tile';const art=document.createElement('div');
 art.append(paintedIcon(id),paintedIcon(id,'native'));const title=document.createElement('span');title.textContent=label;
 const en=document.createElement('small');en.textContent=id;tile.append(art,title,en);$('#icon-grid').append(tile);
}
if(matchMedia('(prefers-reduced-motion:reduce)').matches)motion(false);

})().catch(e=>{document.querySelector('#toast').textContent='预览素材载入失败：'+e.message;document.querySelector('#toast').hidden=false;});
