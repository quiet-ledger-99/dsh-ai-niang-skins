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
'new-session':'[data-dsh-part="new-session"]::before'}
def paint(name,selector,size):
 v=mapping['icons'][name];return selector+'{background-image:url(\'assets/ui/'+v['atlas']+'\')!important;background-size:400% 300%!important;background-position:'+str(v['column']/3*100)+'% '+str(v['row']/2*100)+'%!important;background-repeat:no-repeat!important;width:'+str(size)+'px;height:'+str(size)+'px;flex-shrink:0}\n'
css='\n/* 0.2 — all visible custom glyphs use painted PNG atlas cells. */\n'
for key,sel in native.items():
 css+=paint(key,sel,40 if key=='crest' else 32 if key in ['plugins','schedules','board','memory','more'] else 26)
 if '::' not in sel:css+=sel+' svg{visibility:hidden}\n'
css+='''
[data-slot="sidebar"]>div:first-child{background:#171017 url('assets/ui/sidebar-raster-v1.png') center/100% 100% no-repeat;border-right:1px solid #a87b4e99}
[data-slot="sidebar"] [class*="_panelRow"]{height:39px;min-height:39px;gap:11px;background:linear-gradient(100deg,#26141be6,#25151b80);border:1px solid #c69a6a30;border-radius:7px;box-shadow:inset 0 1px #e8ba7910,0 2px 5px #0003}
[data-slot="sidebar"] [class*="_panelRow"]:hover{background:linear-gradient(100deg,#5b263bcc,#2d1920b3);border-color:#d4aa7490;box-shadow:inset 2px 0 #d6ab73,0 2px 9px #08060a66}
[data-slot="sidebar"] [class*="_panelGlyph"]{width:32px!important;height:32px!important;filter:drop-shadow(0 1px 2px #03010380)}
[class*="_logoRow"]:has([class*="_wide"] [data-slot="sidebar.brand.mark"]){height:89px!important;min-height:89px!important}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"]){height:84px!important;min-height:84px!important;padding:24px 35px 29px!important;justify-content:center;align-items:flex-start!important}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::before{inset:-6px -4px -2px;background:url('assets/ui/brand-raster-v1.png') center/100% 100% no-repeat}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::after{left:28px;right:28px;top:51px;color:#d9bb8d;font-size:8px;letter-spacing:3px}
[data-slot="sidebar.brand.mark"]{display:none!important}
[data-slot="sidebar.brand.name"]{justify-content:center;align-items:center;line-height:1.1;height:24px;white-space:nowrap;color:#fff0d4!important}
[data-slot="sidebar.brand.name"] svg{width:124px!important;max-width:124px!important}
[class*="_brandIdentity"]:has([data-slot="sidebar.brand.name"]){justify-content:center;width:100%;gap:0}
[data-dsh-part="new-session"]{height:37px;min-height:37px;margin-top:4px!important;margin-bottom:9px!important;border:1px solid #be945b99;background:linear-gradient(#59323ee6,#2e1721f5)!important;box-shadow:inset 0 1px #edcf9355,inset 0 -2px #0a050a55,0 3px 8px #06040b66;color:#ffeacf}
[data-dsh-part="new-session"]{position:relative}
[data-dsh-part="new-session"]::before{content:"";position:absolute;left:15px;top:50%;transform:translateY(-50%);pointer-events:none}
[data-dsh-part="new-session"] svg{visibility:hidden}
[data-slot="sidebar.workspaces"] [class*="_sessionRow"][aria-selected="true"]{background:linear-gradient(90deg,#7c3a4e99,#36202bcc);border-color:#cc9a6744;box-shadow:inset 2px 0 #d8ac77,inset 0 1px #ffe4ae12}
[data-slot="sidebar.settings"]{background:linear-gradient(110deg,#351c26e6,#1e121bcc);border-color:#b38b5a66}
[data-composer-card]{border:0!important;background:#231822f5!important;border-radius:10px!important;padding:33px 43px 44px!important;box-shadow:0 8px 27px #06030b80!important;min-height:145px}
[data-composer-card]::after{display:none!important}
[data-composer-card]::before{content:"";position:absolute;inset:-13px -15px -24px;z-index:1;border:0 solid transparent;border-image-source:url('assets/ui/composer-raster-v1.png');border-image-slice:46% 22% 46% 22% fill;border-image-width:66px 115px 66px 115px;pointer-events:none;filter:drop-shadow(0 3px 4px #06030a99)}
[data-composer-card]>:not(:is(tooltip,[role="tooltip"])){position:relative;z-index:2}
[data-composer-card]:focus-within::before{filter:drop-shadow(0 0 4px #d7915155) drop-shadow(0 4px 5px #05020a80)}
[data-composer-card] button[class*="_primary"]{border:1px solid #e3b46c88;box-shadow:inset 0 1px #ffe1a844,0 2px 6px #06030a77;background-color:#46212f!important}
[data-dsh-surface="composer"]{padding-bottom:12px!important}
[class*="_composerHero"] [class*="_titleGroup"]{background:linear-gradient(130deg,#261722ed,#211322eb);border:1px solid #ba8c5e88;box-shadow:inset 0 0 0 3px #ba8c5e10,0 6px 22px #05030c55}
[data-dsh-part="message-body"]{background-image:none;border-color:#c69b6966;box-shadow:inset 0 0 0 4px #e8b76e08,0 6px 22px #05030c55}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"]){border-color:#cb9d6f99;box-shadow:inset 0 0 0 4px #e8b46a09,0 16px 46px #05030d77}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"])::after{background:none!important;border-color:#d5ac7433}
[data-approval-key] [class*="_strip"]{background:linear-gradient(100deg,#57303dd9,#35202be6);border-bottom-color:#c0966466;color:#ffe8c5}
[data-dsh-surface="settings"]{background-image:none;border-color:#bd935f99;box-shadow:inset 0 0 0 4px #edc0790a,0 20px 65px #04020c99}
[data-menu-material="translucent"]{border-color:#be955faa!important;box-shadow:inset 0 0 0 3px #ba8c5e0f,0 12px 34px #030208aa}
@media(max-height:780px){
 [class*="_logoRow"]:has([class*="_wide"] [data-slot="sidebar.brand.mark"]){height:80px!important;min-height:80px!important}
 :is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"]){height:76px!important;min-height:76px!important;padding-top:21px!important;padding-bottom:25px!important}
 :is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::after{top:46px}
 [data-slot="sidebar"] [class*="_panelRow"]{height:35px;min-height:35px;margin-block:1px;padding-block:1px}
 [data-slot="sidebar"] [class*="_panelGlyph"]{width:30px!important;height:30px!important}
 [data-composer-card]{padding-top:28px!important;padding-bottom:35px!important;min-height:135px}
 [data-composer-card]::before{inset:-12px -12px -20px;border-image-width:58px 103px 58px 103px}
}
@media(max-width:700px){
 [data-composer-card]{padding:29px 31px 37px!important;min-height:140px}
 [data-composer-card]::before{inset:-9px -10px -18px;border-image-width:55px 85px 58px 85px}
}
'''
with (O/'patches.css').open('a',encoding='utf-8') as f:f.write(css)
print('Painted raster atlas bindings built')
