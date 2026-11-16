#!/usr/bin/env python3
"""Compare a validator's output with its known baseline (findings that are pre-existing or known false positives).

    python3 vcheck.py <refs|macro|nbt|pack|lint> <validator output> [--save]

S1-CM's copy of scratchpad mb3/tests/vcheck.py (same normalisation; baselines in ./baseline/). The baselines are M0's
(scratchpad mb3/tests/baseline/{refs,macro,lint}.txt, which accept every finding of the M0 tree 039b911) plus the chapter
mode's accepted findings, all of known false-positive classes (listed in baseline/ACCEPTED.md with the reason):
  refs   ar/<aid>/full_rim -> rlk:mboss/hz/p/c/ (macro-built name $(kp); hz/p/c/1..60 exist; the M0 hz/d/full line it replaces
         had the same finding)
  macro  `function ... with storage ...` / `with entity ...` calls read as "called without args" (ar/*/tp_in, oob,
         full_rim, arena/<aid>/s/<i> and l/<look>/<i> -> done, cb/won_*, music/*, resume, start_body, test/*,
         room/obj/k_cboss*); the macro-built hz/p/c/$(kp) of full_rim
  lint   `stopsound` and `time query gametime` (commands unknown to the linter: music/*, px/hit, px/dup), `playsound $(ev)`
         (a macro event id the linter cannot resolve), `bad target '<uuid>'` in px/cproto/** (the proxies' fixed UUIDs, as
         in the M0 butterfly rig lines), `execute without run` in cproto/test (`... run execute store success ... unless ...`)
"""
import re
import sys
from pathlib import Path

KIND, OUT = sys.argv[1], Path(sys.argv[2])
BASE = Path(__file__).resolve().parent / 'baseline' / f'{KIND}.txt'
text = OUT.read_text(encoding='utf-8', errors='replace')


def findings():
    out = set()
    if KIND == 'refs':
        on = False
        for line in text.splitlines():
            if line.startswith('missing refs'):
                on = True
                continue
            if on and '->' in line:
                out.add(re.sub(r':\d+ ->', ' ->', line.strip()))
    elif KIND == 'macro':
        for line in text.splitlines():
            if line.startswith('BAD '):
                line = re.sub(r'^BAD .*?/data/', 'BAD data/', line)
                out.add(re.sub(r'\.mcfunction:\d+ ', '.mcfunction ', line))
    elif KIND == 'lint':
        for line in text.splitlines():
            m = re.match(r'^(\S+?):\d+: (.*)$', line)
            if m:
                msg = re.sub(r"'524c4b4d-[0-9a-f-]+'", "'<uuid>'", m.group(2))
                out.add(f'{m.group(1)}: {msg[:300]}')
    return out


if KIND == 'nbt':
    m = re.search(r'invalid (\d+)', text)
    ok = bool(m) and m.group(1) == '0'
    print(('ok   ' if ok else 'FAIL ') + f'check_nbtpath: {m.group(0) if m else "no summary line"}')
    sys.exit(0 if ok else 1)
if KIND == 'pack':
    m = re.search(r'(\d+) problem', text)
    ok = bool(m) and m.group(1) == '0'
    print(('ok   ' if ok else 'FAIL ') + f'check_mboss_pack: {m.group(0) if m else "no summary line"}')
    sys.exit(0 if ok else 1)
now = findings()
if '--save' in sys.argv:
    BASE.write_text('\n'.join(sorted(now)) + '\n', encoding='utf-8')
    print(f'saved {len(now)} {KIND} findings to {BASE}')
    sys.exit(0)
base = set(l for l in BASE.read_text(encoding='utf-8').splitlines() if l.strip())
new, gone = sorted(now - base), sorted(base - now)
ok = not new
print(('ok   ' if ok else 'FAIL ') + f'{KIND}: {len(now)} findings, {len(new)} new, {len(gone)} fixed vs the baseline')
for x in new[:40]:
    print('   new  ', x)
for x in gone[:10]:
    print('   gone ', x)
sys.exit(0 if ok else 1)
