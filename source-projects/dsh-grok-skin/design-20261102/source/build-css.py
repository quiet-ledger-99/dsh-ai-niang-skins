"""Build complete token palettes and native semantic component styling."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
C=json.loads((R/'source/theme.json').read_text()); P=C['colors']; O=R/'skin'/C['id']
def token(k,v):return '--dsw-'+k+':'+v+';'
t={
'alias-bg-base':'transparent','alias-bg-layer-1':P['surface'],'alias-bg-layer-2':P['raised'],'alias-bg-layer-3':P['third'],'alias-bg-layer-4':P['fourth'],
'alias-bg-module-platform':P['raised'],'alias-bg-overlay':P['surface'],'alias-bg-skeleton':P['third'],
'alias-bg-mask-1':'#0c142766','alias-bg-mask-2':'#0c142733','alias-bg-mask-3':'#0c142799',
'alias-label-primary':P['fg'],'alias-label-secondary':P['secondary'],'alias-label-tertiary':P['muted'],'alias-label-caption':P['muted'],'alias-label-dimmed':P['muted'],'alias-label-primary-dimmed':P['muted'],'alias-label-primary-inverted':P.get('inverted',P['onAccent']),'alias-label-primary-foreground':P['onAccent'],
'alias-brand-primary-new-colorprimary-new-color':P['accent'],'alias-brand-primary':P['accent'],'alias-brand-primary-invert':P['onAccent'],'alias-brand-text':P['link'],
'alias-button-primary-fill':P['accent'],'alias-button-primary-hover':P['link'],'alias-button-primary-dimmed':P['third'],
'alias-button-floating-fill':P['raised'],'alias-button-floating-hover':P['third'],'alias-button-elevated-fill':P['surface'],
'alias-button-ghost-active-fill':P['hover'],'alias-button-ghost-active-hover':P['hover'],'alias-button-ghost-active-border':P['border'],
'alias-interactive-bg-hover':P['hover'],'alias-interactive-bg-hover-solid':P['third'],'alias-interactive-bg-active':P['hover'],'alias-interactive-bg-hover-accent':P['hover'],
'alias-border-l1':P['border'],'alias-border-l2':P['border'],'alias-border-l2-darkmode-thin':P['border'],'alias-border-l3':P['border'],'alias-border-l4':P['muted'],
'alias-state-business-primary':P['accent'],'alias-state-business-tertiary':P['third'],'alias-link':P['link'],
'specific-sidebar-fill':'transparent','specific-sidebar-nav-item-active':P['hover'],'specific-sidebar-nav-item-hover':P['hover'],'specific-sidebar-nav-item-active-accent':P['accent'],
'specific-input-major':P['surface'],'specific-menu':P['decision'],'menu-surface-fill':P['decision'],'specific-selector':P['raised'],'specific-tip':P['surface'],
'specific-bubble':P['glass'],'specific-bubble-highlight':P['raised'],
'alias-scrollbar-bg-l1':P['border'],'alias-scrollbar-bg-l2':P['border'],'alias-scrollbar-hover-l1':P['muted'],'alias-scrollbar-hover-l2':P['muted'],
'alias-tooltip-bg':P['fg'],'alias-tooltip-fg':P['surface'],'alias-toast-bg':P['surface'],
'alias-markdown-code-block':P['code'],'alias-markdown-code-block-banner':P['raised'],'alias-markdown-inline-code':P['hover'],
'alias-settings-card-fill':P['surface'],'alias-settings-card-stroke':P['border'],'alias-menu-icon':P['secondary']}
palette='\n'.join(token(k,v) for k,v in t.items())
css='/* '+C['name']+' — full palette, semantic surfaces, no hooks. */\n'
css+=':root,body[data-ds-dark-theme]{color-scheme:'+P['scheme']+';color:'+P['fg']+';background-color:'+P['surface']+';\n'+palette
css+='\n'+''.join('--skin-'+k+':'+v+';' for k,v in P.items() if k!='scheme')+'}\n'
css+='''
[data-dsh-surface="root"],[data-dsh-surface="conversation"]{background:transparent}
[data-dsh-surface="conversation"]{isolation:isolate}
[data-dsh-surface="session-header"],header[data-window-drag]:has([data-conversation-header-leading]),[class*="_viewTabs"]:has([role="tab"]){background:var(--skin-glass)!important;backdrop-filter:blur(16px);color:var(--skin-fg);border-bottom:1px solid var(--skin-border)}
[data-dsh-surface="details"]{background:var(--skin-decision);color:var(--skin-fg);border-left:1px solid var(--skin-border)}
[data-dsh-part="message-body"]{box-sizing:border-box;color:var(--skin-fg);background:url('assets/ui/corner.svg') right 7px top 7px/31px 31px no-repeat,var(--skin-glass);backdrop-filter:blur(20px) saturate(.8);border:1px solid var(--skin-border);border-radius:13px;padding:20px 24px;box-shadow:inset 0 0 0 4px #b3c9df08,0 5px 22px #080e2426}
[data-dsh-part="message-body"] :is(p,li,h1,h2,h3,h4,blockquote,pre,code,table){color:inherit}
[data-dsh-part="message-body"] :is(h1,h2){font-family:"Songti SC","STSong",serif;font-weight:500;letter-spacing:.5px;padding-bottom:9px;border-bottom:1px solid var(--skin-border)}
[data-dsh-part="message-body"] a{color:var(--skin-link)}
[data-dsh-part="message-body"] blockquote{background:var(--skin-hover);border-left:3px solid var(--skin-accent);padding:10px 16px;border-radius:0 7px 7px 0}
[data-changed-files],[data-presented-file],:is([data-tool],[data-chat-flow-kind="tool-call"]){color:var(--skin-fg);background:var(--skin-glass)!important;border:1px solid var(--skin-border);border-radius:9px;backdrop-filter:blur(14px)}
:is([data-tool],[data-chat-flow-kind="tool-call"]){padding:5px 10px;margin-block:4px}
[data-changed-files],[data-presented-file]{--changes-fill:var(--skin-glass);--changes-hover:var(--skin-raised)}
[data-dsh-surface="settings"]{color-scheme:inherit;color:var(--skin-fg);background:var(--skin-surface) url('assets/ui/corner.svg') left 7px top 7px/27px 27px no-repeat;border:1px solid var(--skin-border);box-shadow:inset 0 0 0 4px #91bad310,0 20px 60px #090d2655;--dsw-alias-bg-base:var(--skin-surface);--dsw-alias-settings-card-fill:var(--skin-raised);--dsw-alias-settings-card-stroke:var(--skin-border)}
[data-menu-material="translucent"]{color:var(--skin-fg);background:var(--skin-decision)!important;border:1px solid var(--skin-border)!important;box-shadow:0 10px 30px #07112d55,inset 0 0 0 3px #b6c7d909;backdrop-filter:blur(24px)}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"]){position:relative;isolation:isolate;background:transparent!important;border:1px solid var(--skin-muted);border-radius:14px;box-shadow:0 16px 46px #080e2859;color:var(--skin-fg)}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"])::before{content:"";position:absolute;inset:0;z-index:0;border-radius:inherit;background:var(--skin-decision);backdrop-filter:blur(28px) saturate(.55);pointer-events:none}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"])>*{position:relative;z-index:1}
:is([data-question-key]>section,[data-approval-key]>[class*="_card"])::after{content:"";position:absolute;inset:4px;z-index:2;border:1px solid var(--skin-border);border-radius:10px;background:url('assets/ui/corner.svg') left top/21px 21px no-repeat,url('assets/ui/corner.svg') right bottom/21px 21px no-repeat;pointer-events:none}
[data-question-key] :is([role="radio"],[role="checkbox"]){color:var(--skin-fg);background:var(--skin-hover);border:1px solid var(--skin-border)}
[data-question-key] [aria-checked="true"]{background:var(--skin-raised);border-color:var(--skin-accent);box-shadow:inset 3px 0 var(--skin-accent)}
[data-question-key] textarea{color:var(--skin-fg);background:var(--skin-code);border-color:var(--skin-border)}
[data-question-key] textarea::placeholder{color:var(--skin-muted);opacity:1}
[data-question-key] [class*="_footer"]:not([class*="_footerActions"]){border-top:1px solid var(--skin-border)}
[data-approval-key] [class*="_strip"]{box-sizing:border-box;display:flex;align-items:center;gap:10px;min-height:44px;padding:10px 18px;border-bottom:1px solid var(--skin-border);background:var(--skin-hover);color:var(--skin-fg);letter-spacing:.5px}
[data-approval-key] [class*="_strip"]::before{content:"";width:26px;height:26px;flex:none;background:url('assets/icons/permission.svg') center/contain no-repeat}
[data-approval-key] [class*="_strip"]>[data-state]{margin-left:auto;color:var(--skin-secondary);font-size:11px}
[data-approval-key] [data-approval-scroll]{padding:16px 18px;gap:10px}
[data-approval-key] [class*="_headline"]{font-size:14px;line-height:1.7;color:var(--skin-fg)}
[data-approval-key] [class*="_command"]{background:var(--skin-code);border:1px solid var(--skin-border);border-radius:8px;padding:11px 13px;font-size:12px;line-height:1.6;color:var(--skin-fg)}
[data-approval-key] [class*="_actionRow"]{padding:12px 18px 16px;gap:10px;border-top:1px solid var(--skin-border);background:var(--skin-hover)}
[data-approval-key] [class*="_reject"]{min-width:70px;color:var(--skin-fg);background:var(--skin-surface);border:1px solid var(--skin-border);border-radius:7px}
[data-approval-key] [class*="_actionRow"]>button:last-child{min-width:94px;min-height:34px;color:var(--skin-onAccent);background:var(--skin-accent)!important;border:1px solid var(--skin-muted);border-radius:7px;box-shadow:inset 0 1px #fff3,0 3px 9px #070b2326}
[data-dsh-surface="composer"]{background:transparent!important}
[data-composer-card]{position:relative;isolation:isolate;background:var(--skin-decision)!important;color:var(--skin-fg);border:1px solid var(--skin-border)!important;border-radius:13px!important;padding:20px 24px 18px!important;box-shadow:0 5px 22px #07112c3b!important}
[data-composer-card]::after{content:"";position:absolute;inset:-7px -8px;z-index:1;background:url('assets/ui/frame.svg') center/100% 100% no-repeat;pointer-events:none}
[data-composer-input]{color:var(--skin-fg)!important;background:transparent!important;caret-color:var(--skin-accent)}
[data-composer-card] :is([data-composer-input],textarea)::placeholder{color:var(--skin-muted)!important;opacity:1}
[data-composer-card] button[class*="_primary"]{background:var(--skin-accent)!important;color:var(--skin-onAccent)!important;box-shadow:inset 0 1px #fff4}
[data-composer-card] button[class*="_add"]{color:var(--skin-secondary);background:var(--skin-raised)!important;border:1px solid var(--skin-border)}
body:has(:is([data-question-key],[data-approval-key])) [data-dsh-composer-frost]{display:none}
[data-dsh-composer-frost]{background:var(--skin-glass);border-radius:13px}
::selection{background:var(--skin-third);color:var(--skin-fg)}
'''
if C.get('rasterIcons'):
 css=css.replace("url('assets/ui/corner.svg') right 7px top 7px/31px 31px no-repeat,","")
 css=css.replace(" url('assets/ui/corner.svg') left 7px top 7px/27px 27px no-repeat","")
 css=css.replace("background:url('assets/ui/corner.svg') left top/21px 21px no-repeat,url('assets/ui/corner.svg') right bottom/21px 21px no-repeat","background:none")
css=css.replace("background:url('assets/icons/permission.svg') center/contain no-repeat",'background:none').replace("background:url('assets/ui/frame.svg') center/100% 100% no-repeat",'background:none')
(O/'skin.css').write_text(css)
patch='''/* Native DSH bindings. No scripting or global style reset. */
[data-dsh-skin-layer="background"]{background:var(--skin-surface) url('assets/wallpaper.png') center/cover no-repeat}
[data-dsh-skin-layer="background"]>:is(img,video){position:absolute!important;left:0!important;top:var(--skin-header-offset,40px)!important;bottom:auto!important;width:100%!important;height:calc(100% - var(--skin-header-offset,40px))!important;object-fit:cover!important;object-position:center top!important}
[data-dsh-surface="sidebar"]{color:var(--skin-sideFg);--dsw-alias-label-primary:var(--skin-sideFg);--dsw-alias-label-secondary:var(--skin-sideMuted);--dsw-alias-label-tertiary:var(--skin-sideMuted);--dsw-alias-label-caption:var(--skin-sideMuted);--dsw-specific-sidebar-fill:transparent;--dsw-alias-interactive-bg-hover:#b4c9df20;--dsw-alias-interactive-bg-active:#b4c9df30}
[data-slot="sidebar"]>div:first-child{background:var(--skin-side) url('assets/ui/sidebar.svg') center/100% 100% no-repeat;border-right:1px solid var(--skin-border)}
[class*="_logoRow"]:has([class*="_wide"] [data-slot="sidebar.brand.mark"]){height:82px!important;min-height:82px;align-items:center}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"]){position:relative;isolation:isolate;box-sizing:border-box;width:100%;height:76px;min-height:76px;padding:16px 18px 28px 57px!important;color:var(--skin-sideFg)!important}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::before{content:"";position:absolute;inset:0;z-index:-1;background:url('assets/ui/frame.svg') center/100% 100% no-repeat;pointer-events:none}
:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"])::after{content:THEME_LABEL;position:absolute;left:53px;right:16px;top:48px;color:var(--skin-sideMuted);text-align:center;font:9px/1.3 "Songti SC",serif;letter-spacing:2px;pointer-events:none}
[data-slot="sidebar.brand.mark"]{position:absolute;left:17px;top:16px;width:32px!important;height:32px!important;background:url('assets/ui/crest.svg') center/contain no-repeat}
[data-slot="sidebar.brand.mark"]>svg{visibility:hidden}
[data-slot="sidebar.brand.name"]{color:var(--skin-sideFg)!important}
[data-slot="sidebar.brand.name"] svg{width:128px!important;max-width:128px;height:auto!important}
[data-dsh-part="new-session"]{min-height:36px;margin:4px 9px 9px!important;border:1px solid #b7c9dc44;border-radius:8px;color:var(--skin-sideFg);background:#829dbd17 url('assets/ui/frame.svg') center/100% 100% no-repeat!important;box-shadow:inset 0 1px #e4f4ff13,0 2px 7px #0002;letter-spacing:2px}
[data-slot="sidebar"] [class*="_panelRow"]{box-sizing:border-box;min-height:36px;height:36px;gap:10px;margin:2px 9px;padding:3px 11px;border:1px solid #c5dcf315;border-radius:7px;background:linear-gradient(100deg,#b1d2f30c,transparent);color:var(--skin-sideFg)}
[data-slot="sidebar"] [class*="_panelRow"]:hover{background:#bed3e51c;border-color:#b5cee54d;box-shadow:inset 2px 0 var(--skin-sideMuted)}
[data-slot="sidebar"] [class*="_panelGlyph"]{width:28px!important;height:28px!important;flex:none;background-position:center;background-size:28px 28px;background-repeat:no-repeat}
[data-slot="sidebar.workspaces"]>div:first-child{margin:7px 8px 0;padding:5px 3px;border:0;border-top:1px solid #bed3e52b;background:transparent;box-shadow:none}
[data-slot="sidebar.workspaces"] [class*="_sectionLabel"]{color:var(--skin-sideMuted);letter-spacing:1px}
[data-slot="sidebar.workspaces"] [class*="_sessionRow"]{min-height:31px;margin-block:2px;border:1px solid transparent;border-radius:6px;color:var(--skin-sideFg)}
[data-slot="sidebar.workspaces"] [class*="_sessionRow"][aria-selected="true"]{background:#c2d3e51c;border-color:#b7cee52e;box-shadow:inset 2px 0 var(--skin-sideMuted)}
[data-slot="sidebar.settings"]{margin:7px 9px;border:1px solid #c5d8ed33;border-radius:9px;background:#b3c7db0d}
[data-slot="sidebar.settings"] [aria-haspopup="menu"]{color:var(--skin-sideFg);min-height:37px}
[data-slot="sidebar.footer.action"] button{border:1px solid #bad2e42b;border-radius:6px;background:#e0f0ff0b}
[data-slot="conversation.hero.brand.mark"]{width:40px;height:38px;background:url('assets/ui/crest.svg') center/contain no-repeat;flex:none}
[data-slot="conversation.hero.brand.mark"]>svg{visibility:hidden}
[class*="_composerHero"]{position:relative;box-sizing:border-box;min-height:calc(100svh - 95px);justify-content:flex-end!important;padding-top:170px!important;padding-bottom:18px!important}
[class*="_composerHero"]>:has([data-slot="conversation.hero.brand.mark"]){position:absolute!important;top:54px;left:30px;max-width:390px;width:auto!important;align-items:flex-start!important}
[class*="_composerHero"] [class*="_titleGroup"]{padding:16px 23px;border:1px solid var(--skin-border);border-radius:13px 4px;background:var(--skin-glass);color:var(--skin-fg);box-shadow:0 6px 22px #08162b26;backdrop-filter:blur(14px)}
[class*="_composerHero"] [class*="_title"]{font-family:"Songti SC",serif;font-weight:500;font-size:29px;letter-spacing:2px}
@media(max-height:760px){[class*="_logoRow"]:has([class*="_wide"] [data-slot="sidebar.brand.mark"]){height:74px!important;min-height:74px}:is(button,span)[class*="_wide"]:has([data-slot="sidebar.brand.mark"]){height:70px;min-height:70px}[data-slot="sidebar"] [class*="_panelRow"]{height:33px;min-height:33px}}
@media(max-width:700px){[data-composer-card]{padding:18px 19px 16px!important}[data-dsh-part="message-body"]{padding:17px 18px}[class*="_composerHero"] [class*="_titleGroup"]{padding:12px 16px;font-size:13px;max-width:260px}[class*="_composerHero"] [class*="_title"]{font-size:24px}[class*="_composerHero"]>:has([data-slot="conversation.hero.brand.mark"]){left:15px;top:28px;max-width:calc(100% - 30px)}}
@media(prefers-reduced-motion:reduce){[data-dsh-skin-layer="background"]>video{visibility:hidden}}
'''.replace('THEME_LABEL',json.dumps(C['name'].split(' · ')[1],ensure_ascii=False))
if C['theme']=='grok':patch+='\n[data-dsh-skin-layer="background"]>:is(img,video){object-position:left top!important}\n@media(max-width:700px){[data-dsh-skin-layer="background"]>:is(img,video){object-position:35% top!important}}\n[class*="_composerHero"]>:has([data-slot="conversation.hero.brand.mark"]){left:auto!important;right:35px!important;top:75px!important;max-width:350px}\n'
nav={
'plugins':'[data-slot="sidebar"] [class*="_panelGlyph"]:has(path[d^="M7.84457 5.06199"])',
'schedules':'[data-slot="sidebar"] [class*="_panelGlyph"]:has(path[d^="M8 14C11.3137"])',
'board':'[data-slot="sidebar"] [class*="_panelGlyph"]:has([data-dsh-panel-entry="task-board"])',
'memory':'[data-slot="sidebar"] [class*="_panelGlyph"]:has([data-dsh-plugin="dsh-mnemon"][data-dsh-part="sidebar-icon"])',
'more':'[data-slot="sidebar"] button[class*="_panelRow"][aria-haspopup="menu"] [class*="_panelGlyph"]',
'search':'[data-slot="sidebar.workspaces"] button[class*="_searchButton"]',
'filter':'[data-slot="sidebar.workspaces"] button:has(>svg path[d^="M2.3 5h5.85"])',
'add-workspace':'[data-slot="sidebar.workspaces"] button:has(>svg path[d^="M5.54492 2.06738"])',
'folder':'[data-slot="sidebar.workspaces"] [class*="_folder"]:has(>svg)',
'pair-phone':'[data-slot="sidebar.footer.action"] button[data-dsh-plugin="remote-bridge"][data-dsh-part="entry"]',
'remote-access':'[data-slot="sidebar.footer.action"] button:has(>svg path[d^="M4.2 1.8h2.4"])',
'settings':'[data-menu-material="translucent"] span:has(>svg path[d^="M8 9.75012C8.9665"])',
'feedback':'[data-menu-material="translucent"] span:has(>svg path[d^="M4.74024 9.11029"])',
'logout':'[data-menu-material="translucent"] span:has(>svg path[d^="M3.9961 1.40039"])',
'login':'[data-menu-material="translucent"] span:has(>svg path[d^="M8 8.25C9.51878"])'}
for name,sel in ({} if C.get('rasterIcons') else nav).items():
 size=28 if name in ['plugins','schedules','board','memory','more'] else 24
 patch+=f'\n{sel}'+'{background:url(\'assets/icons/'+name+f'.svg\') center/{size}px {size}px no-repeat!important;'+f'min-width:{size}px;min-height:{size}px;'+'}\n'+sel+' svg{visibility:hidden}\n'
patch+='[data-slot="sidebar.workspaces"] [class*="_folder"]:has(+ [class*="_chevron"] [class*="_arrowOpen"]){background-image:url(\'assets/icons/folder-open.svg\')!important}\n'
if C.get('rasterIcons'):
 patch=patch.replace('assets/ui/sidebar.svg','assets/ui/sidebar-raster-v1.png').replace('assets/ui/frame.svg','assets/ui/brand-raster-v1.png')
 patch=patch.replace("background:url('assets/ui/crest.svg') center/contain no-repeat",'background:none')
 patch=patch.replace("background-image:url('assets/icons/folder-open.svg')!important",'background-image:none!important')
(O/'patches.css').write_text(patch)
print(O/'skin.css')

# Native attachment and send controls reuse the same drawn icon assets.
if not C.get('rasterIcons'):
 with (O/'patches.css').open('a') as f:
  f.write("\n[data-composer-card] button[class*=\"_add\"]{background:var(--skin-raised) url('assets/icons/attach.svg') center/25px 25px no-repeat!important}\n[data-composer-card] button[class*=\"_add\"]>svg{visibility:hidden}\n[data-composer-card] button[class*=\"_primary\"]{background:var(--skin-accent) url('assets/icons/send.svg') center/27px 27px no-repeat!important}\n[data-composer-card] button[class*=\"_primary\"]>svg{visibility:hidden}\n")
