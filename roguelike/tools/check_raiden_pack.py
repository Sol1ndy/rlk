"""Validate the generated Narukami / player-weapon resource pack content before shipping.

Usage: python tools/check_raiden_pack.py <unpacked resource pack> [<datapack>]
Minecraft rejects a whole model (it renders as the magenta/black missing model) when a face
uv leaves 0..16, an element leaves -16..32 or a rotation angle is not a 22.5-degree step, so
these are checked strictly, together with texture variables, sprite files/atlas entries and
every rlk:raiden/... item model the datapack refers to.
"""
from pathlib import Path
import json
import re
import sys

rp = Path(sys.argv[1])
dp = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1]
A = rp / 'assets'
atlas = json.loads((A / 'minecraft/atlases/items.json').read_text(encoding='utf-8'))
sprites = {s.get('sprite') or s.get('resource') for s in atlas['sources']}
errors = []
roots = [A / 'rlk/models/item/raiden', A / 'rlk/models/item/player_motion/weapons']
for root in roots:
    for mf in root.rglob('*.json'):
        name = mf.relative_to(A / 'rlk/models/item')
        md = json.loads(mf.read_text(encoding='utf-8'))
        tex = md.get('textures', {})
        for key, t in tex.items():
            if t.startswith('#'):
                continue
            ns, path = t.split(':') if ':' in t else ('minecraft', t)
            if t not in sprites and not (A / ns / 'textures' / (path + '.png')).exists():
                errors.append(f'{name}: texture {t} is neither a file nor an atlas sprite')
            elif t not in sprites and ns == 'rlk':
                errors.append(f'{name}: texture {t} is not registered in the item atlas')
        for i, el in enumerate(md.get('elements', [])):
            if any(v < -16 or v > 32 for v in el['from'] + el['to']):
                errors.append(f'{name}#{i}: element outside -16..32')
            r = el.get('rotation')
            if r and r.get('angle') not in (-45, -22.5, 0, 22.5, 45):
                errors.append(f'{name}#{i}: rotation angle {r.get("angle")}')
            for fname, f in el['faces'].items():
                uv = f.get('uv')
                if uv and (min(uv) < 0 or max(uv) > 16):
                    errors.append(f'{name}#{i}.{fname}: uv {uv} outside 0..16')
                if f.get('rotation', 0) not in (0, 90, 180, 270):
                    errors.append(f'{name}#{i}.{fname}: uv rotation {f["rotation"]}')
                ref = f['texture'].lstrip('#')
                if ref not in tex:
                    errors.append(f'{name}#{i}.{fname}: undefined texture #{ref}')
refs = set()
for fn in (dp / 'data/rlk/function/boss/raiden').rglob('*.mcfunction'):
    refs |= set(re.findall(r'rlk:raiden/[a-z0-9_/]+(?=")', fn.read_text(encoding='utf-8')))
for r in sorted(refs):
    if not (A / 'rlk/items' / (r.split(':')[1] + '.json')).exists():
        errors.append(f'datapack refers to missing item model {r}')
for e in errors[:60]:
    print('ERROR', e)
print(f'checked {sum(1 for r in roots for _ in r.rglob("*.json"))} models, {len(refs)} item references: '
      f'{len(errors)} problem(s)')
sys.exit(1 if errors else 0)
