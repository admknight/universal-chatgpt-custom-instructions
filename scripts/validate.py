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
for token in ['unrelated tasks','AI/prompt','primary/official/governing sources','secondary sources for context/corroboration','high-consequence/disputed claims',"common options aren't gaps",'project/governing basis','technical/functional need','if material','assume/qualify']:
    if token not in texts['COPY-THIS-Free-Go.txt']: ok=False; print('FAIL Free/Go coverage:',token)
for token in ['NOVEL DOMAINS & AI','unfamiliar domains','agents, Skills or automation','governing primary/official sources','secondary sources for context/corroboration','high-consequence/disputed claims','primary verification is unavailable','Preserve scope','find material gaps/conflicts',"Common/optional possibilities aren't gaps",'project/governing basis','technical/functional need','if material','otherwise assume/qualify']:
    if token not in texts['COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt']: ok=False; print('FAIL paid coverage:',token)
if (ROOT/'VERSION').read_text().strip()!='1.0.3': ok=False; print('FAIL: VERSION')
for forbidden in ['modules','private','upstream']:
    if (ROOT/forbidden).exists(): ok=False; print('FAIL: forbidden public path:',forbidden)
for p in (ROOT/'release').glob('*.library.json'):
    d=json.loads(p.read_text(encoding='utf-8'))
    if d['author']['name']!='Zahid Hussain' or d['author']['organization']!='Scopewise Consulting': ok=False; print('FAIL metadata',p.name)
    if d.get('revision')!='1.0.3': ok=False; print('FAIL revision',p.name)
    if d.get('validation_tier')!='SCENARIO_PASS' or d.get('release_state')!='SCENARIO_VALIDATED': ok=False; print('FAIL qualification',p.name)
    if d.get('runtime_validation_status')!='NOT_RUN': ok=False; print('FAIL runtime truthfulness',p.name)
    print(f'{p.name}: JSON/full metadata PASS')
report=json.loads((ROOT/'validation/public.test-report.json').read_text(encoding='utf-8'))
if report.get('revision')!='1.0.3': ok=False; print('FAIL public report revision')
if not report.get('defect_history'): ok=False; print('FAIL missing defect history')
if not any(t.get('test_id')=='PUB-015' and t.get('status')=='PASS' for t in report.get('tests',[])): ok=False; print('FAIL missing price-effect regression')
print('public test report JSON: PASS')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
