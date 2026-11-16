#!/usr/bin/env python3
"""pmeas.py <dp> [label] [out.json]: commands per tick (player side) for small(3) / late(18 ★★★): one dirty pass, out of combat,
combat churn, one F-dash (6 ticks). Same tick model for every tree (pworld: seat present, ride_tick's item lines)."""
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pworld import SMALL, LATE, world, tick, measure, combat_after, f_press, one_pass  # noqa: E402

dp = sys.argv[1]
label = sys.argv[2] if len(sys.argv) > 2 else Path(dp).parent.name
t0 = time.time()
res = {}
for tag, items, stars in (('small3', SMALL, 0), ('late18', LATE, 3)):
    s, pl = world(dp, items, stars)
    P = ('e', pl.id)
    r = {'pass': one_pass(s)}
    s.setsc(P, 'skillCd', 0)
    s.setsc(P, 'energy', 9999999)
    for _ in range(10):
        tick(s)
    r['idle'] = measure(s, 400)
    r['combat'] = measure(s, 400, combat_after)
    # F-dash from rest (skill ready, energy full), after the combat block settles
    s.setsc(P, 'skillCd', 0)
    s.setsc(P, 'burstCd', 0)
    s.setsc(P, 'energy', 9999999)
    for _ in range(40):
        tick(s)
    a = s.n
    e0 = s.ncall['rlk:items/equip_scan']
    f_press(s)
    per = []
    for _ in range(6):
        b = s.n
        tick(s)
        per.append(s.n - b)
    inv = s.player.data['inv']
    w = inv.get('hotbar.0') or {'c': {}}
    r['fdash'] = {'total6': s.n - a, 'per_tick': per, 'scans': s.ncall['rlk:items/equip_scan'] - e0,
                  'weapon_back': w['c'].get('minecraft:custom_data', {}).get('rlk_ui', {}).get('role') == 'attack'
                  and 'weapon.offhand' not in inv,
                  'consumable': 'minecraft:consumable' in w['c'], 'model': w['c'].get('minecraft:item_model')}
    r['errors'] = sorted(((str(k), v) for k, v in s.errors.items() if 'health_tick' not in str(k) and 'hunger' not in str(k)),
                         key=lambda x: -x[1])[:10]
    res[tag] = r
    print(f'[{label}] {tag}: pass {r["pass"]}')
    for k in ('idle', 'combat'):
        m = r[k]
        print(f'[{label}] {tag} {k}: avg {m["avg"]:.0f} p50 {m["p50"]} max {m["max"]} equip_scan {m["scans"]} '
              f'({m["scans"] / m["n"] * 20:.2f}/s) manage {m["manages"]}')
    print(f'[{label}] {tag} F-dash: {r["fdash"]}')
    if r['errors']:
        print(f'[{label}] {tag} sim errors: {r["errors"]}')
print(f'[{label}] wall {time.time() - t0:.0f} s')
if len(sys.argv) > 3:                                      # optional JSON copy of the numbers
    Path(sys.argv[3]).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
