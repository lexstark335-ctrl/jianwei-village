from pathlib import Path
import json

root=Path(__file__).resolve().parent
src=root/'src'
credits=json.loads((root/'docs/assets/photo-credits.json').read_text(encoding='utf-8'))
credits.pop('download_status',None)
data=(src/'data.js').read_text(encoding='utf-8').replace('/*__CREDITS__*/',json.dumps(credits,ensure_ascii=False))
html=(src/'index.html').read_text(encoding='utf-8').replace('/*__STYLES__*/',(src/'styles.css').read_text(encoding='utf-8')).replace('/*__DATA__*/',data).replace('/*__APP__*/',(src/'app.js').read_text(encoding='utf-8'))
(root/'docs/index.html').write_text(html,encoding='utf-8')
print('Built docs/index.html',len(html.encode('utf-8')),'bytes')
