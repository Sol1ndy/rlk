#!/usr/bin/env python3
"""Resource-pack lint for client-only failures the server load check cannot see.

usage: python3 -I rplint.py <unpacked resource pack>
Fails (exit 1) on: asset paths with characters outside [a-z0-9_.-/] (one bad id makes the client reject a whole
atlas or model set), invalid or missing atlas sources, JSON that does not parse, and font bitmap providers the client
cannot draw: a cell (image width / columns x image height / rows) over 256 px in either direction silently becomes the
missing-glyph box (the glyph atlas page is 256 x 256: review/v/client_facts.md 7 - the 11-11b parry streak was 512 x 288),
`ascent` > `height` fails the font codec (that font file is skipped), a missing bitmap file rejects the provider.
"""
import glob
import json
import os
import re
import struct
import sys

rp = sys.argv[1]
ok_path = re.compile(r'[a-z0-9_.\-/]+')
ok_id = re.compile(r'[a-z0-9_.\-]+:[a-z0-9_.\-/]+')
problems = []
for f in glob.glob(os.path.join(rp, 'assets', '**', '*'), recursive=True):
    if os.path.isdir(f):
        continue
    rel = os.path.relpath(f, os.path.join(rp, 'assets'))
    if not ok_path.fullmatch(rel):
        problems.append(f'bad path: {rel}')
    if f.endswith(('.json', '.mcmeta')):
        try:
            json.load(open(f, encoding='utf-8'))
        except Exception as e:  # noqa: BLE001
            problems.append(f'bad json: {rel}: {e}')
for atlas in glob.glob(os.path.join(rp, 'assets', '*', 'atlases', '*.json')):
    try:
        srcs = json.load(open(atlas, encoding='utf-8')).get('sources', [])
    except Exception:  # noqa: BLE001
        continue
    for s in srcs:
        rid = s.get('resource')
        if rid is None:
            continue
        if not ok_id.fullmatch(rid):
            problems.append(f'bad atlas id in {os.path.basename(atlas)}: {rid}')
            continue
        ns, p = rid.split(':', 1)
        if ns != 'minecraft' and not os.path.exists(os.path.join(rp, 'assets', ns, 'textures', p + '.png')):
            problems.append(f'missing atlas texture in {os.path.basename(atlas)}: {rid}')
FONT_CELL_MAX = 256  # net.minecraft.client.gui.font.FontTexture.SIZE


def png_size(path):
    with open(path, 'rb') as fh:
        head = fh.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n' or head[12:16] != b'IHDR':
        return None
    return struct.unpack('>II', head[16:24])


for font in sorted(glob.glob(os.path.join(rp, 'assets', '*', 'font', '**', '*.json'), recursive=True)):
    frel = os.path.relpath(font, os.path.join(rp, 'assets'))
    try:
        provs = json.load(open(font, encoding='utf-8')).get('providers', [])
    except Exception:  # noqa: BLE001
        continue
    for pv in provs:
        if not isinstance(pv, dict) or pv.get('type') != 'bitmap':
            continue
        fid, chars = pv.get('file', ''), pv.get('chars') or []
        height, ascent = pv.get('height', 8), pv.get('ascent')
        if isinstance(ascent, (int, float)) and isinstance(height, (int, float)) and ascent > height:
            problems.append(f'font ascent > height in {frel}: {fid} (ascent {ascent}, height {height})')
        if not ok_id.fullmatch(fid) or not chars or not all(isinstance(r, str) and r for r in chars):
            problems.append(f'bad font bitmap provider in {frel}: {fid!r}')
            continue
        ns, pth = fid.split(':', 1)
        img = os.path.join(rp, 'assets', ns, 'textures', pth)
        if not os.path.exists(img):
            if ns != 'minecraft':
                problems.append(f'missing font bitmap in {frel}: {fid}')
            continue
        size = png_size(img)
        if size is None:
            problems.append(f'font bitmap is not a PNG in {frel}: {fid}')
            continue
        cols = len(chars[0])           # code points per row (surrogate-free: Python str = code points)
        if any(len(r) != cols for r in chars):
            problems.append(f'font chars rows differ in length in {frel}: {fid}')
            continue
        cw, ch = size[0] // cols, size[1] // len(chars)
        if cw > FONT_CELL_MAX or ch > FONT_CELL_MAX:
            problems.append(f'font cell over {FONT_CELL_MAX} px in {frel}: {fid} cell {cw}x{ch} '
                            f'(image {size[0]}x{size[1]}, {cols}x{len(chars)} glyphs) -> drawn as the missing-glyph box')
print(f'rplint: {len(problems)} problem(s)')
for p in problems[:40]:
    print('  ' + p)
sys.exit(1 if problems else 0)
