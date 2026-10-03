from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
ATTR='© 2026 Zahid Hussain / Scopewise Consulting | UPA R6'
checks=[('COPY-THIS-Free-Go.txt',1500),('COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt',5000)]
ok=True
for name,limit in checks:
    text=(ROOT/name).read_text(encoding='utf-8')
    print(f'{name}: {len(text)}/{limit}')
    if len(text)>limit: ok=False; print('FAIL: character limit exceeded')
    if not text.startswith(ATTR+'\n'): ok=False; print('FAIL: compact attribution missing')
    if '<!-- UPA_AUTHOR_IDENTITY_START -->' in text: ok=False; print('FAIL: long attribution banner still present')
for token in ['unrelated tasks','documents/reports','AI/prompt']:
    if token not in (ROOT/'COPY-THIS-Free-Go.txt').read_text(encoding='utf-8'): ok=False; print('FAIL Free/Go coverage:',token)
for token in ['NOVEL DOMAINS & AI','unfamiliar domains','agents, Skills or automation']:
    if token not in (ROOT/'COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt').read_text(encoding='utf-8'): ok=False; print('FAIL paid coverage:',token)
if (ROOT/'VERSION').read_text().strip()!='1.0.0': ok=False; print('FAIL: VERSION')
for forbidden in ['modules','private','upstream']:
    if (ROOT/forbidden).exists(): ok=False; print('FAIL: forbidden public path:',forbidden)
for p in (ROOT/'release').glob('*.library.json'):
    d=json.loads(p.read_text(encoding='utf-8'))
    assert d['author']['name']=='Zahid Hussain' and d['author']['organization']=='Scopewise Consulting'
    print(f'{p.name}: JSON/full metadata PASS')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
