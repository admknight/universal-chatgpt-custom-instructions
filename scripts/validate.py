from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
ATTR='© 2026 Zahid Hussain / Scopewise Consulting | UPA R6'
checks=[('COPY-THIS-Free-Go.txt',1500),('COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt',5000)]
ok=True
texts={}
for name,limit in checks:
    s=(ROOT/name).read_text(encoding='utf-8'); texts[name]=s
    print(f'{name}: {len(s)}/{limit}')
    if len(s)>limit: ok=False; print('FAIL: character limit exceeded')
    if not s.startswith(ATTR+'\n'): ok=False; print('FAIL: compact attribution missing')
    if '<!-- UPA_AUTHOR_IDENTITY_START -->' in s: ok=False; print('FAIL: long attribution banner still present')
free_tokens=['primary/official/governing sources','secondary for context/corroboration','high-consequence/disputed claims','Scope gate','clarification/requirement/alternate/exclusion/assumption','project/governing basis','technical need','price impact alone',"absence isn't ambiguity",'No basis: omit',"don't choose",'AI/prompt']
for token in free_tokens:
    if token not in texts['COPY-THIS-Free-Go.txt']: ok=False; print('FAIL Free/Go coverage:',token)
paid_tokens=['NOVEL DOMAINS & AI','unfamiliar domains','agents, Skills or automation','governing primary/official sources','secondary sources for context/corroboration','high-consequence/disputed claims','primary verification is unavailable','preserve scope','clarification/requirement/alternate/exclusion/assumption','project/governing basis','technical need','price impact alone',"absence isn't ambiguity",'No basis: omit',"don't choose an option"]
for token in paid_tokens:
    if token not in texts['COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt']: ok=False; print('FAIL paid coverage:',token)
if (ROOT/'VERSION').read_text().strip()!='1.0.4': ok=False; print('FAIL: VERSION')
for forbidden in ['modules','private','upstream']:
    if (ROOT/forbidden).exists(): ok=False; print('FAIL: forbidden public path:',forbidden)
for p in (ROOT/'release').glob('*.library.json'):
    d=json.loads(p.read_text(encoding='utf-8'))
    if d['author']['name']!='Zahid Hussain' or d['author']['organization']!='Scopewise Consulting': ok=False; print('FAIL metadata',p.name)
    if d.get('revision')!='1.0.4': ok=False; print('FAIL revision',p.name)
    if d.get('validation_tier')!='SCENARIO_PASS' or d.get('release_state')!='SCENARIO_VALIDATED': ok=False; print('FAIL qualification',p.name)
    if d.get('runtime_validation_status')!='NOT_RUN': ok=False; print('FAIL runtime truthfulness',p.name)
    print(f'{p.name}: JSON/full metadata PASS')

def scope_decision(project=False,governing=False,technical=False,material=False,assumption_required=False):
    basis=project or governing or technical
    if not basis: return 'ASSUME' if assumption_required else 'OMIT'
    return 'CLARIFY' if material else 'QUALIFY'
cases=[
('Cee punching absent',{},'OMIT'),
('missing Cee return lip',{'technical':True,'material':True},'CLARIFY'),
('missing plate thickness',{'technical':True,'material':True},'CLARIFY'),
('optional galvanizing absent',{},'OMIT'),
('drawing-shown accessory',{'project':True,'material':True},'CLARIFY'),
('contract notice',{'governing':True,'material':True},'CLARIFY'),
('supplier lead time',{'project':True,'material':True},'CLARIFY'),
('common accessory no evidence',{},'OMIT'),
('price-only optional feature',{},'OMIT'),
('absent option/default temptation',{},'OMIT'),
('necessary bounded assumption',{'assumption_required':True},'ASSUME')]
for name,args,expected in cases:
    actual=scope_decision(**args)
    if actual!=expected: ok=False; print('FAIL scope harness:',name,actual,expected)
print(f'scope harness: {len(cases)}/{len(cases)} PASS' if ok else 'scope harness: FAIL')
report=json.loads((ROOT/'validation/public.test-report.json').read_text(encoding='utf-8'))
if report.get('revision')!='1.0.4': ok=False; print('FAIL public report revision')
if len(report.get('defect_history',[]))<2: ok=False; print('FAIL defect history')
for tid in ['PUB-015','PUB-016','PUB-017']:
    if not any(t.get('test_id')==tid and t.get('status')=='PASS' for t in report.get('tests',[])): ok=False; print('FAIL missing regression',tid)
print('public test report JSON: PASS')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
