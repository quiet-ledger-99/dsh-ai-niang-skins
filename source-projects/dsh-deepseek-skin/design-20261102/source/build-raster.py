"""Bind painted PNG atlases and nine-slice frames to native DSH controls."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
C=json.loads((R/'source/theme.json').read_text(encoding='utf-8'));O=R/'skin'/C['id']
groups={
 'icon-nav-atlas.png':['plugins','schedules','board','memory','more','search','filter','add-workspace','folder','folder-open','pair-phone','remote-access'],
 'icon-controls-atlas.png':['settings','feedback','logout','login','attach','permission','send','model','preset','crest','new-session','close']}
mapping={'columns':4,'rows':3,'icons':{name:{'atlas':atlas,'column':i%4,'row':i//4} for atlas,names in groups.items() for i,name in enumerate(names)}}
(O/'assets/ui/icon-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
native={
'plugins':'[data-slot="sidebar"] [class*="_panelGlyph"]:has(path[d^="M7.84457 5.06199"])',
'schedules':'[data-slot="sidebar"] [class*="_panelGlyph"]:has(path[d^="M8 14C11.3137"])',
'board':'[data-slot="sidebar"] [class*="_panelGlyph"]:has([data-dsh-panel-entry="task-board"])',
'memory':'[data-slot="sidebar"] [class*="_panelGlyph"]:has([data-dsh-plugin="dsh-mnemon"][data-dsh-part="sidebar-icon"])',
'more':'[data-slot="sidebar"] button[class*="_panelRow"][aria-haspopup="menu"] [class*="_panelGlyph"]',
'search':'[data-slot="sidebar.workspaces"] button[class*="_searchButton"]',
'filter':'[data-slot="sidebar.workspaces"] button:has(>svg path[d^="M2.3 5h5.85"])',
'add-workspace':'[data-slot="sidebar.workspaces"] button:has(>svg path[d^="M5.54492 2.06738"])',
'folder':'[data-slot="sidebar.workspaces"] [class*="_folder"]:has(>svg)',
'folder-open':'[data-slot="sidebar.workspaces"] [class*="_folder"]:has(+ [class*="_chevron"] [class*="_arrowOpen"])',
'pair-phone':'[data-slot="sidebar.footer.action"] button[data-dsh-plugin="remote-bridge"][data-dsh-part="entry"]',
'remote-access':'[data-slot="sidebar.footer.action"] button:has(>svg path[d^="M4.2 1.8h2.4"])',
'settings':'[data-menu-material="translucent"] span:has(>svg path[d^="M8 9.75012C8.9665"])',
'feedback':'[data-menu-material="translucent"] span:has(>svg path[d^="M4.74024 9.11029"])',
'logout':'[data-menu-material="translucent"] span:has(>svg path[d^="M3.9961 1.40039"])',
'login':'[data-menu-material="translucent"] span:has(>svg path[d^="M8 8.25C9.51878"])',
'attach':'[data-composer-card] button[class*="_add"]',
'send':'[data-composer-card] button[class*="_primary"]',
'crest':'[data-slot="conversation.hero.brand.mark"]',
'permission':'[data-approval-key] [class*="_strip"]::before',
'new-session':'[data-dsh-part="new-session"]::before',
'close':'[data-dsh-surface="settings"] button[class*="_close"]',
'model':'[data-slot="sidebar"] [class*="_panelGlyph"]:has(.tps-side)'}
def paint(name,selector,size):
 v=mapping['icons'][name];return selector+'{background-image:url(\'assets/ui/'+v['atlas']+'\')!important;background-size:400% 300%!important;background-position:'+str(v['column']/3*100)+'% '+str(v['row']/2*100)+'%!important;background-repeat:no-repeat!important;width:'+str(size)+'px;height:'+str(size)+'px;flex-shrink:0}\n'
css='\n/* 0.2 — all visible custom glyphs use painted PNG atlas cells. */\n'
for key,sel in native.items():
 css+=paint(key,sel,40 if key=='crest' else 32 if key in ['plugins','schedules','board','memory','more','model','attach','send','close'] else 26)
 if '::' not in sel:css+=sel+' svg{visibility:hidden}\n'
css+=r'''

[data-slot="sidebar"]>div:first-child{background:#172c50 url('assets/ui/sidebar-raster-v1.png') center/100% 100% no-repeat;border-right:1px solid #b9d5ea88}
[data-slot="sidebar"] [class*="_panelRow"]{height:38px;min-height:38px;gap:10px;background:linear-gradient(100deg,#172d50e8,#183050ba);border:1px solid #aacde54d;border-radius:8px;box-shadow:inset 0 1px #e2f5ff16,0 2px 5px #06132922}
[data-slot="sidebar"] [class*="_panelRow"]:hover{background:linear-gradient(100deg,#355b87ee,#244770dd);border-color:#d3edffb0;box-shadow:inset 2px 0 #bee5fa,0 2px 8px #06172d55}
[data-slot="sidebar"] [class*="_panelGlyph"]{width:32px!important;height:32px!important;filter:drop-shadow(0 1px 2px #08162c66)}
[class*="_logoRow"]:has([class*="_wide"] [data-slot="sidebar.brand.mark"]){height:85px!important;min-height:85px!important}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"]){height:81px!important;min-height:81px!important;padding:25px 36px 27px!important;justify-content:center;align-items:flex-start!important}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::before{inset:-4px -3px -1px;background:url('assets/ui/brand-raster-v1.png') center/100% 100% no-repeat}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::after{left:32px;right:32px;top:49px;color:#c9e7fb;font-size:8px;letter-spacing:3px}
[data-slot="sidebar.brand.mark"]{display:none!important}
[data-slot="sidebar.brand.name"]{justify-content:center;align-items:center;line-height:1.1;height:23px;white-space:nowrap;color:#f2f9ff!important}
[data-slot="sidebar.brand.name"] svg{width:118px!important;max-width:118px!important}
[class*="_brandIdentity"]:has([data-slot="sidebar.brand.name"]){justify-content:center;width:100%;gap:0}
[data-dsh-part="new-session"]{position:relative;height:36px;min-height:36px;margin-top:3px!important;margin-bottom:8px!important;border:1px solid #b7d5e9b0;background:linear-gradient(#33587fef,#1a375cf5)!important;box-shadow:inset 0 1px #f4fcff55,inset 0 -2px #081b362e,0 3px 8px #06172b44;color:#f1f9ff}
[data-dsh-part="new-session"]::before{content:"";position:absolute;left:15px;top:50%;transform:translateY(-50%);pointer-events:none}
[data-dsh-part="new-session"] svg{visibility:hidden}
[data-slot="sidebar.workspaces"] [class*="_sessionRow"][aria-selected="true"]{background:linear-gradient(90deg,#527ba6cc,#254466dd);border-color:#b9dced77;box-shadow:inset 2px 0 #d4f0ff,inset 0 1px #f6fcff19}
[data-slot="sidebar.settings"]{background:linear-gradient(110deg,#28486be8,#152d4edb);border-color:#bdd8e777}
[data-composer-card]{border:0!important;background:linear-gradient(125deg,#f6fcfff5,#e8f4fbee)!important;border-radius:11px!important;padding:26px 36px 29px!important;box-shadow:0 8px 23px #10284450!important;min-height:130px}
[data-composer-card]::after{display:none!important}
[data-composer-card]::before{content:"";position:absolute;inset:-12px -14px -16px;z-index:1;border:0 solid transparent;border-image-source:url('assets/ui/composer-raster-v1.png');border-image-slice:43% 21% 43% 21% fill;border-image-width:53px 104px 53px 104px;pointer-events:none;filter:drop-shadow(0 3px 4px #1139574d)}
[data-composer-card]>:not(:is(tooltip,[role="tooltip"])){position:relative;z-index:2}
[data-composer-card]:focus-within::before{filter:drop-shadow(0 0 4px #a9e4ff99) drop-shadow(0 3px 4px #11395755)}
[data-composer-card] button[class*="_primary"]{border:1px solid #b0d2e788;box-shadow:inset 0 1px #fff7,0 2px 6px #234c6d44;background-color:#426e9e!important}
[data-dsh-surface="composer"]{padding-bottom:8px!important}
[class*="_composerHero"] [class*="_titleGroup"]{background:linear-gradient(125deg,#f6fcfff0,#deedf7eb);border:1px solid #b1d1e7b0;box-shadow:inset 0 0 0 3px #edfaff55,0 6px 20px #13385830}
[data-dsh-part="message-body"]{background-image:none;border-color:#93bad699;box-shadow:inset 0 0 0 4px #d6eaf533,0 6px 22px #102d4726}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"]){border:1px solid #96bad4cc;border-radius:14px;box-shadow:0 13px 35px #10274455}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"])::before{background:#f1f9fff7!important;backdrop-filter:blur(28px) saturate(.55)}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"])::after{content:"";position:absolute;inset:-7px;z-index:2;border:0 solid transparent;border-image-source:url('assets/ui/panel-frame-raster-v1.png');border-image-slice:28% fill;border-image-width:38px;pointer-events:none;background:none!important;filter:drop-shadow(0 2px 2px #1e486544)}
[data-approval-key] [class*="_strip"]{padding:14px 32px 12px 35px;background:linear-gradient(100deg,#e0eef8ee,#d1e7f2dd);border-bottom-color:#9bbdd488;color:#284b6e}
[data-approval-key] [class*="_actionRow"]{padding:14px 28px 20px;background:linear-gradient(100deg,#e4f1f8ee,#d8ebf5dd)}
[data-approval-key] [class*="_actionRow"]>button:last-child{background:linear-gradient(#598bb8,#315d8d)!important;border-color:#c6e4f7b0;box-shadow:inset 0 1px #eefaff70,0 3px 7px #19395544}
[data-question-key] :is([class*="_heading"],[class*="_header"],.question-heading){padding:21px 30px 12px}
[data-question-key] [aria-checked="true"]{background:linear-gradient(100deg,#d7ebf7,#ecf7fd);border-color:#7fa8c6;box-shadow:inset 3px 0 #4c7ba8,inset 0 1px #fff9}
[data-dsh-surface="settings"]{isolation:isolate;background-image:none;border-color:#a5c8e0cc;box-shadow:inset 0 0 0 4px #ecf8ff66,0 20px 60px #10294366}
[data-dsh-surface="settings"]::after{content:"";position:absolute;inset:2px;z-index:5;border:0 solid transparent;border-image-source:url('assets/ui/panel-frame-raster-v1.png');border-image-slice:28% fill;border-image-width:25px;pointer-events:none}
[data-menu-material="translucent"]{border-color:#9fc4dfcc!important;box-shadow:inset 0 0 0 3px #d7edf87f,0 10px 28px #0c284955}
[data-menu-material="translucent"]::after{content:"";position:absolute;inset:-3px;z-index:2;border:0 solid transparent;border-image-source:url('assets/ui/panel-frame-raster-v1.png');border-image-slice:28% fill;border-image-width:24px;pointer-events:none}
@media(max-height:780px){
 [class*="_logoRow"]:has([class*="_wide"] [data-slot="sidebar.brand.mark"]){height:78px!important;min-height:78px!important}
 :is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"]){height:74px!important;min-height:74px!important;padding-top:22px!important;padding-bottom:24px!important}
 :is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::after{top:46px}
 [data-slot="sidebar"] [class*="_panelRow"]{height:34px;min-height:34px;margin-block:1px;padding-block:1px}
 [data-slot="sidebar"] [class*="_panelGlyph"]{width:30px!important;height:30px!important}
 [data-composer-card]{padding-top:24px!important;padding-bottom:26px!important;min-height:126px}
 [data-composer-card]::before{inset:-11px -12px -14px;border-image-width:48px 94px 48px 94px}
}
@media(max-width:700px){
 [data-composer-card]{padding:24px 28px 29px!important;min-height:130px}
 [data-composer-card]::before{inset:-10px -10px -14px;border-image-width:46px 76px 46px 76px}
}


/* Completed native flow items do not always retain the streaming markdown hook. */
[data-chat-flow-kind]:not([data-chat-flow-kind="tool-call"]):not(:has([data-dsh-part="message-body"])){
 color:var(--skin-fg);--dsw-alias-label-primary:var(--skin-fg);--dsw-alias-label-secondary:var(--skin-secondary);
 background:linear-gradient(125deg,#f6fcfff2,#e9f4fbee);backdrop-filter:blur(22px) saturate(.65);
 border:1px solid #a4c7dfaa;border-radius:13px;padding:19px 23px;box-shadow:inset 0 1px #fff9,0 5px 18px #12314b26;
}
[data-slot="sidebar"] button[aria-haspopup="menu"]:has(img){background:#183552eb;border:1px solid #a9ccdf77;border-radius:10px}
[data-slot="sidebar"] button[aria-label="打开使用统计设置"]{background:#193654ee;border:1px solid #a6cadd66;border-radius:9px}


[data-dsh-surface="composer"] button:not([data-composer-card] button){background:#edf8fff0;border:1px solid #adcee27f;border-radius:7px;padding:4px 9px;color:#284866;box-shadow:0 2px 5px #14324b1a}
.context-line>span{background:#edf8fff0;border:1px solid #adcee27f;border-radius:6px;padding:2px 7px;color:#284866}

'''

with (O/'patches.css').open('a',encoding='utf-8') as f:f.write(css)
print('DeepSeek painted materials bound')
