#!/usr/bin/env python3
"""test_consts.py <dp>: the shared number constants that rlk:load sets on the `tmp` objective (`#c<n> tmp`, `#<n> tmp`,
`#neg<n> tmp`) keep their load value through inventory sorts and equipment scans.

`player/inv/order_count2` used `#c2 tmp` (the constant 2 that char/nefer/cat_tick multiplies the catalyst's yaw by) as
its hotbar-count temporary, so every sort set it to 0 and 네페르's floating catalyst stopped turning until /reload.
Checks, each on a fresh world after the real rlk:load: (1) `#c2 tmp` = 2 after one sort (player/inv/manage +
items/equip_scan, as player/tick runs them), with no items, with 3 items and with 18 items; (2) every constant above
equals its load value after the whole late-run scenario of pworld (sorts, scans, 400 combat ticks, an F press, a
discard). Exit 1 on any failure.
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pworld import SMALL, LATE, world, tick, combat_after, f_press, pctx  # noqa: E402

dp = Path(sys.argv[1])
LOAD = (dp / 'data/rlk/function/load.mcfunction').read_text(encoding='utf-8')
CONST = {m.group(1): int(m.group(2)) for m in re.finditer(r'^scoreboard players set (#(?:c|neg)?\d+) tmp (-?\d+)$', LOAD, re.M)}
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    fails += not ok


def sort_once(s):
    c = pctx(s)
    s.call('rlk:player/inv/manage', c)
    s.call('rlk:items/equip_scan', c)


check(CONST.get('#c2') == 2 and len(CONST) > 20, f'load sets {len(CONST)} shared constants, #c2 tmp = {CONST.get("#c2")}')
for tag, items in (('no items', []), ('3 items', SMALL), ('18 items', LATE)):
    s, pl = world(dp, items, 0, settle=0)
    s.setsc('#c2', 'tmp', 2)                      # as rlk:load left it (the world's give/settle ticks already sorted)
    sort_once(s)
    check(s.sc('#c2', 'tmp') == 2, f'{tag}: #c2 tmp after one sort = {s.sc("#c2", "tmp")} (want 2)')

s, pl = world(dp, LATE, 3)
P = ('e', pl.id)
s.setsc(P, 'skillCd', 0)
s.setsc(P, 'energy', 9999999)
for k in range(400):
    tick(s, lambda s, k=k: combat_after(s, k))
    if k == 200:
        f_press(s)
inv = s.player.data['inv']
if 'inventory.12' in inv:                         # discard one item (click it onto the cursor), then let it sort
    inv['player.cursor'] = inv.pop('inventory.12')
    s.call('rlk:player/inv/dirty', pctx(s))
for _ in range(220):                              # past the 10-s fallback
    tick(s)
bad = {k: (v, s.sc(k, 'tmp')) for k, v in CONST.items() if s.sc(k, 'tmp') != v}
check(not bad, f'late run: {len(CONST)} constants keep their load value after sorts / scans / combat / F / discard'
      + (f' — changed: {bad}' if bad else ''))
print('test_consts:', 'PASS' if not fails else f'FAIL ({fails})')
sys.exit(1 if fails else 0)
