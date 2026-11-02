"""Package original PNG material assets and the received DeepSeek v4 film."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent.parent
C=json.loads((R/'source/theme.json').read_text(encoding='utf-8'));O=R/'skin'/C['id']
U=O/'assets/ui';U.mkdir(parents=True,exist_ok=True);(O/'preview').mkdir(exist_ok=True)
for p in (R/'source/raster-v1').glob('*.png'):shutil.copy2(p,U/p.name)
shutil.copy2(R/'source'/C['wallpaper'],O/'assets/wallpaper.png')
film=R/'source'/C['backgroundVideo'];shutil.copy2(film,O/'assets'/film.name)
media={'type':'video','src':'assets/'+film.name}
M={'skinManifestVersion':2,'id':C['id'],'name':C['name'],'nameEn':C['nameEn'],'version':C['version'],'author':'qianweitao · Codex','tagline':C['tagline'],'description':C['description'],'accent':C['accent'],'tags':C['tags'],'order':2,'license':'User-supplied character references; AI-assisted derivative artwork; rights not transferred','attribution':'人物参考由用户提供；原画、图标、边框使用内置imagegen；动态背景由用户交回的Grok Bot视频提供。','preview':{'light':'preview/cover.jpg','dark':'preview/cover.jpg'},'contributes':{'stylesheet':'skin.css','patches':'patches.css','backgroundMedia':{'light':media,'dark':media}}}
(O/'skin.json').write_text(json.dumps(M,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(O)
