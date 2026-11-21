import json
from pathlib import Path

root = Path(__file__).resolve().parent
src = root / 'src'
assets = root / 'docs' / 'assets'
credits = json.loads((assets / 'photo-credits.json').read_text(encoding='utf-8'))
credits.pop('download_status', None)
data = (src / 'data.js').read_text(encoding='utf-8').replace(
    '/*__CREDITS__*/', json.dumps(credits, ensure_ascii=False)
)
html = (src / 'index.html').read_text(encoding='utf-8')
html = html.replace('/*__STYLES__*/', (src / 'styles.css').read_text(encoding='utf-8'))
html = html.replace('/*__DATA__*/', data)
html = html.replace('/*__APP__*/', (src / 'app.js').read_text(encoding='utf-8'))

image_key = 'const PHOTO_ASSETS = {};'
if html.count(image_key) != 1:
    raise ValueError('Expected one photo asset declaration')
root_photo_paths = {
    image.stem: f'docs/assets/{image.name}' for image in sorted(assets.glob('*.jpg'))
}
root_html = html.replace(image_key, f'const PHOTO_ASSETS = {json.dumps(root_photo_paths)};')

for path, page in ((root / 'docs' / 'index.html', html), (root / 'index.html', root_html)):
    path.write_text(page, encoding='utf-8', newline='\n')
    print(f'Built {path.relative_to(root)}')
