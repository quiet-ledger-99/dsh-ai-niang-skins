"""Rebuild the theme body and its offline preview from local source assets."""
from pathlib import Path
import json, shutil, subprocess, sys, os
os.environ.setdefault("PYTHONUTF8", "1")
R=Path(__file__).resolve().parent.parent
for script in ('build-assets-raster.py','build-css.py','build-raster.py'):
    subprocess.run([sys.executable,str(R/'source'/script)],check=True)
C=json.loads((R/'source/theme.json').read_text(encoding="utf-8"))
copy=json.loads((R/'source/preview-copy.json').read_text(encoding="utf-8"))
html=(R/'source/preview.html').read_text(encoding="utf-8")
for key,value in copy.items():html=html.replace('@@'+key+'@@',value)
html=html.replace('@@VIDEO@@',C['backgroundVideo'])
html=html.replace('href="preview.css"','href="preview.css?v=020"').replace('src="preview.js"','src="preview.js?v=020"')
(R/'preview/index.html').write_text(html,encoding="utf-8")
for f in ('preview.css','preview.js','motion-player.html'):shutil.copy2(R/'source'/f,R/'preview'/f)
cover=R/'screenshots/home-raster-020.jpg'
if cover.exists():shutil.copy2(cover,R/'skin'/C['id']/'preview/cover.jpg')
print('Build complete:',C['name'])
