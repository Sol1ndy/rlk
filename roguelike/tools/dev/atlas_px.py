"""Stitched items-atlas size of an unpacked resource pack (release gate "atlas budget").

    python3 -I atlas_px.py <unpacked RP>

Sums w x h of every PNG named by assets/minecraft/atlases/items.json (vanilla sources count 256 px each), the method of
the Raiden suite's budget check. Budget: keep <= 13.2 M px (11-02: 12.63 M; the client's limit is about 15.5 M).
Copied unchanged from the old session's scratchpad ar/review/atlas_px.py (docstring added).
"""
import json, sys
from pathlib import Path
rp = Path(sys.argv[1])
def png_size(f):
    h = f.read_bytes()[:24]
    return int.from_bytes(h[16:20], 'big'), int.from_bytes(h[20:24], 'big')
atlas = json.loads((rp / 'assets/minecraft/atlases/items.json').read_text(encoding='utf-8'))
px = n = 0
for src in atlas.get('sources', []):
    res_id = src.get('resource', '')
    ns, path = res_id.split(':', 1) if ':' in res_id else ('minecraft', res_id)
    f = rp / 'assets' / ns / 'textures' / f'{path}.png'
    n += 1
    if f.exists():
        w, h = png_size(f); px += w * h
    elif ns == 'minecraft':
        px += 256
print(f'stitched items atlas {px} px ({px / 1e6:.3f} M) from {n} sources')
