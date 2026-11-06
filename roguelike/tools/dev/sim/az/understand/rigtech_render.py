#!/usr/bin/env python3
"""Offline render of an mboss-style display-entity rig (UUID-addressed parts), for the chapter-boss rigs.

The renderer behind every earlier rig render is scratchpad preview/raiden_preview.py (a numpy z-buffer rasteriser
that interprets summon / data merge / data modify / tp / function and loads item definitions + models from an RP).
The other copy, scratchpad mb/gw/tools/preview.py (the one mb3/rigwork/tools/r.sh and renders.py call, with --clean),
is gone from disk. raiden_preview.py has no UUID selector, so the mboss rigs' `data merge entity <uuid>` lines did
nothing; render_bfv.py / render_integ.py patch Scene.select. This wrapper applies the same patch and then runs the
normal CLI, so every raiden_preview.py flag works (--spawn / --apply / --views / --extent / --center / --strip ...).
A .jpg output name is written as JPEG (quality 88) to keep disk use modest.

    python3 -I rigtech_render.py --dp <debug dp> --rp <rp> --spawn rlk:mboss/<id>/rig/spawn \
        --apply rlk:<x>_dbg/<clip>/<t> --views front,right,iso --light mc -q -o out.jpg
"""
import importlib.util
import re
import sys
from pathlib import Path

S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
spec = importlib.util.spec_from_file_location('preview', S / 'preview/raiden_preview.py')
PV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PV)

UUID = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
_sel0 = PV.Scene.select


def _uuid_ints(u):
    h = u.replace('-', '')
    out = []
    for i in range(4):
        v = int(h[8 * i:8 * i + 8], 16)
        out.append(v - (1 << 32) if v >= (1 << 31) else v)
    return out


def _select(self, sel, ctx):
    if UUID.fullmatch(sel):
        want = _uuid_ints(sel)
        return [e for e in self.entities if e.alive and [int(x) for x in (e.nbt.get('UUID') or [])] == want]
    return _sel0(self, sel, ctx)


PV.Scene.select = _select

if __name__ == '__main__':
    argv = sys.argv[1:]
    out = None
    if '-o' in argv:
        i = argv.index('-o')
        out = argv[i + 1]
        if out.lower().endswith(('.jpg', '.jpeg')):
            argv[i + 1] = out.rsplit('.', 1)[0] + '.__tmp.png'
    PV.main(argv)
    if out and out.lower().endswith(('.jpg', '.jpeg')):
        from PIL import Image
        tmp = Path(out.rsplit('.', 1)[0] + '.__tmp.png')
        Image.open(tmp).convert('RGB').save(out, quality=88)
        tmp.unlink()
