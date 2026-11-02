"""Build the skin's editable SVG enamel ornaments. No generation service is used here."""
from pathlib import Path
import json, shutil

ROOT=Path(__file__).resolve().parent.parent
C=json.loads((ROOT/'source/theme.json').read_text())
OUT=ROOT/'skin'/C['id']; A=OUT/'assets'; UI=A/'ui'; ICON=A/'icons'
for p in (UI,ICON,OUT/'preview'):p.mkdir(parents=True,exist_ok=True)
night=C['theme']=='grok'
gold='#c79962' if night else '#b6a079'
bright='#ffe6af' if night else '#e2f5ff'
deep='#25121d' if night else '#233f6b'
enamel='#742c43' if night else '#81c2e5'
white='#f8e4c7' if night else '#f3fcff'
def svg(w,h,body,extra=''):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {extra}><defs><linearGradient id="metal" x2=".85" y2="1"><stop stop-color="{bright}"/><stop offset=".33" stop-color="{gold}"/><stop offset=".52" stop-color="{bright}"/><stop offset="1" stop-color="{gold}"/></linearGradient><radialGradient id="enamel" cx=".3" cy=".2" r=".85"><stop stop-color="{enamel}"/><stop offset="1" stop-color="{deep}"/></radialGradient></defs>{body}</svg>'''
def save(name,w,h,body,extra=''): (UI/name).write_text(svg(w,h,body,extra))
whale='M10 27C10 19 18 13 29 16C36 18 36 24 40 23C42 22 42 18 40 16C46 16 48 12 49 11C49 20 47 25 42 28C41 39 29 43 19 37C13 34 10 31 10 27Z'
bat='M6 29L10 15L21 21L28 11L35 21L46 15L50 29L39 26L34 36L28 31L22 36L17 26Z'
crest=(f'<path d="{bat}" fill="url(#enamel)" stroke="url(#metal)" stroke-width="1.8"/><path d="M30 6C22 7 21 15 28 18C18 17 16 8 23 3" fill="url(#metal)"/><path d="M28 20L32 25L28 31L24 25Z" fill="#b93d58"/>' if night else f'<path d="{whale}" fill="url(#enamel)" stroke="url(#metal)" stroke-width="1.5"/><circle cx="18" cy="25" r="1.8" fill="{white}"/><path d="M25 12Q20 7 20 5M27 11Q28 5 32 5" fill="none" stroke="{enamel}" stroke-width="2"/><path d="M15 33Q24 40 35 34" fill="none" stroke="{white}" stroke-width="1.3"/>')
save('crest.svg',56,48,crest)
# Distinct central objects retain navigation meaning at 24-28 pixels.
objects={
'plugins':'<path d="M20 14L28 9L36 14L36 22L42 26L36 30L36 40L28 46L20 40L20 30L14 26L20 22Z"/><circle cx="28" cy="26" r="6"/><path d="M25 11L25 5L31 5L31 11M22 42L22 48L34 48L34 42"/>',
'schedules':'<circle cx="28" cy="30" r="16"/><circle cx="28" cy="30" r="12"/><path d="M28 20L28 30L36 34M23 12L23 6L33 6L33 12M17 13L13 9M39 13L43 9"/>',
'board':'<path d="M11 43V20L17 11L23 20V43M24 43V14L30 5L36 14V43M37 43V20L43 11L49 20V43M8 45H51"/><path d="M15 24H19M15 30H19M28 20H32M28 27H32M41 25H45M41 32H45"/>',
'memory':'<path d="M7 14Q18 10 28 18Q38 10 49 14V42Q38 39 28 47Q18 39 7 42Z"/><path d="M28 18V47M12 22Q19 20 23 24M12 29Q19 27 23 31M34 23H43M34 30H43"/>',
'more':'<path d="M28 6L36 15L28 23L20 15ZM28 33L36 42L28 51L20 42ZM5 28L14 20L22 28L14 36ZM34 28L43 20L51 28L43 36Z"/><circle cx="28" cy="28" r="3"/>',
'search':'<circle cx="24" cy="23" r="15"/><circle cx="24" cy="23" r="10"/><path d="M35 34L47 46L43 50L31 38M18 13Q24 9 31 14"/>',
'filter':'<path d="M12 11V46M28 11V46M44 11V46M8 20H16M24 35H32M40 20H48"/><path d="M12 14L18 20L12 26L6 20ZM28 29L34 35L28 41L22 35ZM44 14L50 20L44 26L38 20Z"/>',
'add-workspace':'<path d="M8 44V17L17 9H32L37 16H47V44Z"/><path d="M27 21V37M19 29H35"/><circle cx="27" cy="29" r="12"/>',
'folder':'<path d="M6 43V14H23L28 20H50V43Q28 49 6 43Z"/><path d="M9 25H47M12 39Q28 43 44 39"/><path d="M28 27L34 33L28 39L22 33Z"/>',
'folder-open':'<path d="M6 39V14H23L28 20H49V25M6 43L12 26H53L47 45Z"/><path d="M25 31L31 37L25 43L19 37Z"/>',
'pair-phone':'<path d="M15 6H41V49H15Z"/><path d="M19 13H37V40H19ZM24 45H32M24 9H32M21 18H26V23H21ZM30 18H35V23H30ZM21 28H26V33H21ZM30 28H35V36"/>',
'remote-access':'<path d="M15 8Q7 13 12 27Q19 43 34 47Q45 49 49 38L38 30L31 36Q23 32 20 24L26 18Z"/><path d="M33 8Q46 11 48 23M33 15Q40 17 41 24"/>',
'settings':'<path d="M23 6H33L35 13L42 14L47 22L42 28L46 35L41 43L34 42L29 49L20 46L19 39L11 37L8 28L14 23L12 16L20 12Z"/><circle cx="28" cy="28" r="11"/><circle cx="28" cy="28" r="5"/>',
'feedback':'<path d="M10 42L15 29L38 7Q49 6 48 17L23 40Z"/><path d="M15 29L23 40M10 42L7 49L23 45M25 19L36 29M13 48H45"/>',
'logout':'<path d="M11 46V16L22 6L33 16V46M5 47H38M17 43V21Q22 13 27 21V43M29 28H49M41 20L49 28L41 36"/>',
'login':'<path d="M24 47V16L35 6L46 16V47M19 48H52M3 28H32M24 20L32 28L24 36"/>',
'send':'<path d="M28 47V11M14 25L28 10L42 25"/><path d="M20 40L28 47L36 40"/>',
'attach':'<path d="M29 45L13 29Q5 20 14 12Q22 5 30 13L44 27Q50 34 43 40Q36 47 30 40L18 28Q15 24 19 21Q22 18 25 21L35 31"/>',
'permission':'<path d="M28 5L46 13V27Q44 42 28 51Q12 42 10 27V13Z"/><path d="M20 28L26 34L38 21"/>',
'model':'<path d="M28 6L46 17V39L28 50L10 39V17ZM10 17L28 28L46 17M28 28V50"/><circle cx="28" cy="28" r="6"/>',
'preset':'<path d="M28 6L33 19L47 14L41 28L50 38L36 38L28 51L20 38L6 38L15 28L9 14L23 19Z"/><circle cx="28" cy="28" r="7"/>'}
if night:
 objects['plugins']='<path d="M8 27L12 13L21 19L28 9L35 19L44 13L48 27L39 25L34 39L28 34L22 39L17 25Z"/><path d="M21 20L35 34M35 20L21 34M18 44Q28 50 38 44"/>'
 objects['memory']='<path d="M12 9H42V47H12Q7 44 12 40ZM12 40H42M17 12V37M22 13H39M22 35H39"/><path d="M28 18L35 25L28 32L21 25Z"/><path d="M35 30L43 34L35 38Z"/>'
 objects['schedules']='<circle cx="28" cy="31" r="16"/><path d="M28 21V31L37 35M24 12V7H32V12M17 13L13 9M39 13L43 9M26 18Q17 23 19 33Q15 24 22 18Z"/>'
else:
 objects['plugins']='<path d="M8 34Q7 20 17 18Q19 7 28 7Q37 7 39 18Q49 20 48 34L39 46H17Z"/><path d="M28 10V36M18 19L24 36M38 19L32 36M10 28L21 39M46 28L35 39M17 46Q28 40 39 46"/><path d="M26 34H30V41H26Z"/>'
 objects['board']='<path d="M7 13L22 8L35 13L49 8V43L35 48L22 43L7 48Z"/><path d="M22 8V43M35 13V48M11 21L18 19M11 27L18 25M26 23L31 25M26 30L31 32M39 19L45 17M39 26L45 24M39 34L45 32"/>'
 objects['memory']='<path d="M7 13Q18 9 28 17Q38 9 49 13V41Q38 38 28 46Q18 38 7 41Z"/><path d="M28 17V46M11 21Q17 19 23 23M11 28Q17 26 23 30M34 23Q40 18 42 24L46 22Q45 28 41 30Q35 32 34 27Z"/>'
 objects['schedules']='<circle cx="28" cy="30" r="16"/><circle cx="28" cy="30" r="12"/><path d="M28 20V30L35 34M23 12V6H33V12M14 40Q20 36 27 40T42 40M7 30H12M44 30H49"/>'
for key,obj in objects.items():
 if night:
  border='<path d="M6 18L11 7L22 4L28 1L34 4L45 7L50 18M6 39L11 50L23 52L28 55L33 52L45 50L50 39" fill="none" stroke="url(#metal)" stroke-width="1"/><path d="M2 27L8 22L8 34ZM54 27L48 22L48 34Z" fill="url(#enamel)" stroke="url(#metal)" stroke-width=".8"/>'
 else:
  border='<path d="M5 19Q2 9 13 6Q20 2 28 4Q37 2 45 7Q54 12 50 21M5 37Q2 47 14 50Q20 54 28 52Q39 54 47 47Q54 43 50 35" fill="none" stroke="url(#metal)" stroke-width="1.2"/><circle cx="5" cy="28" r="2.3" fill="#ddf6ff" stroke="#86b7ce"/><circle cx="51" cy="28" r="2.3" fill="#ddf6ff" stroke="#86b7ce"/>'
  if key=='board':obj=obj.replace('L17 11','Q17 9 17 11').replace('L30 5','Q30 3 30 5')
 art=border+f'<g fill="url(#enamel)" stroke="url(#metal)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">{obj}</g>'
 art+=('<path d="M28 24L32 28L28 33L24 28Z" fill="#ae3551" stroke="#eec18e" stroke-width=".8"/>' if night else '<path d="M25 6Q28 2 31 6" fill="none" stroke="#b5e7ff" stroke-width="1.5"/>')
 (ICON/(key+'.svg')).write_text(svg(56,56,art))
# Frames have clear centers, so decoration cannot cover text or consume layout height.
if night:
 frame='''<path d="M8 34L26 8H357L400 2L443 8H774L792 34V126L774 152H443L400 158L357 152H26L8 126Z" fill="none" stroke="url(#metal)" stroke-width="1.6"/><path d="M17 36L31 17H351L400 8L449 17H769L783 36V124L769 143H449L400 152L351 143H31L17 124Z" fill="none" stroke="#c7996266"/><path d="M24 26Q67 32 91 15M776 26Q733 32 709 15M24 134Q67 128 91 145M776 134Q733 128 709 145" fill="none" stroke="url(#metal)"/><path d="M400 3L408 11L400 22L392 11ZM400 138L408 149L400 157L392 149Z" fill="#95304a" stroke="url(#metal)"/>
<path d="M24 64Q39 69 45 80Q37 87 24 96M776 64Q761 69 755 80Q763 87 776 96" fill="none" stroke="url(#metal)"/>
<path d="M25 49L29 58L25 65L21 58ZM775 49L779 58L775 65L771 58Z" fill="url(#metal)"/>'''
else:
 frame='''<path d="M8 41Q5 8 40 9H357Q381 9 400 3Q419 9 443 9H760Q795 8 792 41V119Q795 152 760 151H443Q419 151 400 157Q381 151 357 151H40Q5 152 8 119Z" fill="none" stroke="url(#metal)" stroke-width="1.8"/><path d="M17 42Q15 18 42 18H355Q381 18 400 10Q419 18 445 18H758Q785 18 783 42V118Q785 142 758 142H445Q419 142 400 150Q381 142 355 142H42Q15 142 17 118Z" fill="none" stroke="#78bde5aa"/><path d="M28 18Q60 38 89 12M772 18Q740 38 711 12M28 142Q60 122 89 148M772 142Q740 122 711 148" fill="none" stroke="#a6d9ee" stroke-width="2"/><path d="M31 53Q40 64 31 80Q24 65 31 53M769 53Q760 64 769 80Q776 65 769 53" fill="#def7ff" stroke="#82b1d0"/><circle cx="400" cy="10" r="5" fill="#b9e9ff" stroke="url(#metal)"/><circle cx="400" cy="150" r="5" fill="#d8f4ff" stroke="url(#metal)"/>'''
save('frame.svg',800,160,frame,'preserveAspectRatio="none"')
save('divider.svg',400,24,'<path d="M7 12H158M242 12H393M35 8L7 12L35 16M365 8L393 12L365 16" stroke="url(#metal)" fill="none"/><g transform="translate(182,-2) scale(.64)">'+crest+'</g>')
corner=('<path d="M4 47V16L16 4H47M9 38V19L19 9H38M7 7L25 13L13 25Z" fill="none" stroke="url(#metal)"/><path d="M17 17L23 23L17 29L11 23Z" fill="#8a3047"/>' if night else '<path d="M4 47V20Q4 4 20 4H47M10 39V22Q10 10 22 10H39M5 5Q29 6 27 24Q12 31 5 5Z" fill="none" stroke="#7cb9d8"/><circle cx="17" cy="17" r="4" fill="#d9f4ff" stroke="url(#metal)"/>')
save('corner.svg',52,52,corner)
# Sidebar engraving is subdued; no character art is hidden underneath navigation labels.
pattern='<path d="M14 0V900M266 0V900" stroke="url(#metal)" stroke-opacity=".45"/>'
for y in range(50,950,90):
 pattern+=f'<g transform="translate(15,{y})" opacity=".13">'+('<path d="M12 0Q52 12 27 46Q10 62 20 85M20 24L2 18M27 46L46 35M20 65L40 72" fill="none" stroke="#d6ac72"/>' if night else '<path d="M8 0Q41 17 19 43Q-1 64 27 88M19 43Q50 53 36 71M19 23Q1 14 2 5" fill="none" stroke="#a8d5ee"/>')+'</g>'
save('sidebar.svg',280,900,pattern,'preserveAspectRatio="none"')
shutil.copy2(ROOT/'source'/C['wallpaper'],A/'wallpaper.png')
video=ROOT/'source/background-loop-v1.mp4'
media={'type':'video','src':'assets/background-loop-v1.mp4'} if video.exists() else {'type':'image','src':'assets/wallpaper.png'}
if video.exists():shutil.copy2(video,A/'background-loop-v1.mp4')
manifest={'skinManifestVersion':2,'id':C['id'],'name':C['name'],'nameEn':C['nameEn'],'version':'0.1.0','author':'qianweitao · Codex','tagline':C['tagline'],'description':C['description'],'accent':C['accent'],'tags':C['tags'],'order':3 if night else 2,'license':'User-supplied character references; AI-assisted derivative artwork; rights not transferred','attribution':'人物原设与参考由用户提供；原画使用内置 imagegen；界面与图标由 Codex 制作。','preview':{'light':'preview/cover.jpg','dark':'preview/cover.jpg'},'contributes':{'stylesheet':'skin.css','patches':'patches.css','backgroundMedia':{'light':media,'dark':media}}}
(OUT/'skin.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(OUT)
