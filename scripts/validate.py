from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
required=[
'<!-- UPA_AUTHOR_IDENTITY_START -->','**Author:** Zahid Hussain','**Designation:** Founder & CEO',
'**Organization:** Scopewise Consulting','**Email:** mzhspk@gmail.com','**Generated with:** Universal Prompt Architect',
'**Architecture:** R6','**Copyright:** Copyright © 2026 Scopewise Consulting. All rights reserved.','<!-- UPA_AUTHOR_IDENTITY_END -->']
checks=[('COPY-THIS-Free-Go.txt',1500),('COPY-THIS-Plus-Pro-Business-Enterprise-Education.txt',5000)]
ok=True
for name,limit in checks:
    text=(ROOT/name).read_text(encoding='utf-8')
    print(f'{name}: {len(text)}/{limit}')
    if len(text)>limit: ok=False; print('FAIL: character limit exceeded')
    for token in required:
        if token not in text: ok=False; print(f'FAIL: {name} missing attribution token: {token}')
if (ROOT/'VERSION').read_text().strip()!='1.0.0': ok=False; print('FAIL: VERSION must be 1.0.0')
for forbidden in ['modules','private','upstream']:
    if (ROOT/forbidden).exists(): ok=False; print(f'FAIL: forbidden public path exists: {forbidden}')
for p in (ROOT/'release').glob('*.library.json'):
    json.loads(p.read_text(encoding='utf-8')); print(f'{p.name}: JSON PASS')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
