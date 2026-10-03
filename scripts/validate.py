from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
ATTR='© 2026 Zahid Hussain / Scopewise Consulting | UPA R6'
checks=[('COPY-THIS-Free-Go.txt',1500),('COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt',5000)]
ok=True
texts={}
for name,limit in checks:
    text=(ROOT/name).read_text(encoding='utf-8'); texts[name]=text
    print(f'{name}: {len(text)}/{limit}')
    if len(text)>limit: ok=False; print('FAIL: character limit exceeded')
    if not text.startswith(ATTR+'\n'): ok=False; print('FAIL: compact attribution missing')
    if '<!-- UPA_AUTHOR_IDENTITY_START -->' in text: ok=False; print('FAIL: long attribution banner still present')
for token in ['unrelated tasks','documents/reports','AI/prompt','primary, official or governing sources','secondary sources for context/corroboration','high-consequence/disputed claims']:
    if token not in texts['COPY-THIS-Free-Go.txt']: ok=False; print('FAIL Free/Go coverage:',token)
for token in ['NOVEL DOMAINS & AI','unfamiliar domains','agents, Skills or automation','governing primary/official sources','Use secondary sources for context, interpretation or discovery','Cross-check high-consequence/disputed claims','primary verification is unavailable']:
    if token not in texts['COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt']: ok=False; print('FAIL paid coverage:',token)
if (ROOT/'VERSION').read_text().strip()!='1.0.1': ok=False; print('FAIL: VERSION')
for forbidden in ['modules','private','upstream']:
    if (ROOT/forbidden).exists(): ok=False; print('FAIL: forbidden public path:',forbidden)
for p in (ROOT/'release').glob('*.library.json'):
    d=json.loads(p.read_text(encoding='utf-8'))
    if d['author']['name']!='Zahid Hussain' or d['author']['organization']!='Scopewise Consulting': ok=False; print('FAIL metadata',p.name)
    if d.get('validation_tier')!='SCENARIO_PASS' or d.get('release_state')!='SCENARIO_VALIDATED': ok=False; print('FAIL qualification',p.name)
    if d.get('runtime_validation_status')!='NOT_RUN': ok=False; print('FAIL runtime truthfulness',p.name)
    print(f'{p.name}: JSON/full metadata PASS')
report=json.loads((ROOT/'validation/public.test-report.json').read_text(encoding='utf-8'))
print('public test report JSON: PASS')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
