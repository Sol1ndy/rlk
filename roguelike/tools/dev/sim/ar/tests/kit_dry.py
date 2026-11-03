#!/usr/bin/env python3
"""kit_dry.py (S3): the whole S3 build with api.K forced on (as when S1K's manifest exists) into a dummy writer: no
exception, every kit call names a contract preset / prop / decal / hud / sound with its args, macro lines carry $(..),
the fx call count per subtree. python3 kit_dry.py [<roguelike dir>]"""
import re
import sys
import types
from pathlib import Path
SCR = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
DP = Path(sys.argv[1]) if len(sys.argv) > 1 else SCR / 'ar/wt_i1/roguelike'
sys.path.insert(0, str(DP / 'tools'))
sys.path.insert(0, str(SCR / 'ar/s3/lib'))
import cmsim as C  # noqa: E402
from mboss_arlecchino import api  # noqa: E402
api.K._on = lambda: True
from mboss_arlecchino import core, ai, bond, p1, p2, seq  # noqa: E402
check, summary = C.check, C.summary


class DW:
    def __init__(self):
        self.files = {}
        self.out = types.SimpleNamespace(written=set())

    def w(self, rel, body):
        self.files[rel] = body if isinstance(body, list) else body.split('\n')
        self.out.written.add((api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve())


W = DW()
for p in p1.PATTERNS:
    p.build(W)
ctx = core.Ctx(list(p1.PATTERNS), W, [])
ai.build(W, ctx)
bond.build(W, ctx)
core.build(W, ctx)
bad, calls = [], {}
for rel, lines in W.files.items():
    for ln in lines:
        if not ln or ln.lstrip().startswith('#'):
            continue
        if ln.lstrip().startswith('$') != ('$(' in ln):
            bad.append((rel, 'macro', ln[:80]))
        for m in re.finditer(r'function rlk:boss/arlecchino/fx/([a-z_/]+)(?: (\{[^}]*\}|with storage \S+ \S+))?', ln):
            path, args = m.group(1), m.group(2) or ''
            sub, _, name = path.rpartition('/')
            table = {'p': api.KIT_PRESETS, 'prop': api.KIT_PROPS, 'decal': api.KIT_DECALS, 'hud': api.KIT_HUD}.get(sub)
            if sub == 'snd':
                ok = name in api.KIT_SOUNDS
            elif sub == '':
                ok = name in api.KIT_FIXED
            else:
                ok = table is not None and name in table and (args.startswith('with') or
                                                              sorted(re.findall(r'(\w+):', args)) == sorted(table[name]))
            if not ok:
                bad.append((rel, path, args))
            calls[sub or 'fixed'] = calls.get(sub or 'fixed', 0) + 1
check('kit-on build: no exception, every fx call is a contract name with its args, macro lines ok', not bad, bad[:5])
print('     kit calls by kind:', calls, '- files', len(W.files))
summary('kit_dry')
