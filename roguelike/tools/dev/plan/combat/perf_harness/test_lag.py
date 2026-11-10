#!/usr/bin/env python3
"""test_lag.py <dp>: the late-game lag fixes hold (Fix A of plan/combat/research_misc.md §4), on the pworld tick model
(F5 seat present; view/ride_tick's item lines run before the real rlk:player/tick).

  1 combat churn (18 items ★★★, 400 ticks: skill cooldown + energy steps rebuild the hotbar items) runs the inventory
    sort / equipment scan only at the 10-s fallback (<= 4 scans)
  2 a rebuilt skill / burst item has the consumable component at the end of the tick that rebuilt it
  3 an F press: 0 scans in the next 6 ticks, the weapon is back in hotbar.0 with the consumable and its rlk:h/* model,
    the off hand is empty
  4 real inventory edits still sort: two items swapped in the inventory (an event) -> a pass; an rlk item put in the off
    hand by F (event, no UI item there) -> a pass; an event while the map is open (vMap 1) with a UI item in the off
    hand -> a pass
Exit 1 on any failure. The release tree fails 1, 2 and 3 (124 scans, 0/67, 3 scans).
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pworld import LATE, world, tick, combat_after, f_press, pctx  # noqa: E402

dp = sys.argv[1]
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    fails += not ok


s, pl = world(dp, LATE, 3)
P = ('e', pl.id)
inv = pl.data['inv']
s.setsc(P, 'skillCd', 0)
s.setsc(P, 'energy', 9999999)
for _ in range(10):
    tick(s)

# 1 + 2
sc0 = s.ncall['rlk:items/equip_scan']
rebuilt, cons_ok = 0, 0
for k in range(400):
    a = s.ncall['rlk:char/skill_item'] + s.ncall['rlk:char/burst_item']
    tick(s, lambda s, k=k: combat_after(s, k))
    if s.ncall['rlk:char/skill_item'] + s.ncall['rlk:char/burst_item'] > a:
        rebuilt += 1
        cons_ok += all('minecraft:consumable' in (inv.get(f'hotbar.{i}') or {'c': {}})['c'] for i in (1, 2))
n = s.ncall['rlk:items/equip_scan'] - sc0
check(n <= 4, f'1 combat churn 400 ticks: {n} equipment scans (want <= 4, the 10-s fallback)')
check(rebuilt > 20 and cons_ok == rebuilt, f'2 {cons_ok}/{rebuilt} hotbar rebuild ticks end with the consumable on slots 1-2')

# 3
s.setsc(P, 'skillCd', 0)
s.setsc(P, 'burstCd', 0)
for _ in range(30):
    tick(s)
sc0 = s.ncall['rlk:items/equip_scan']
f_press(s)
for _ in range(6):
    tick(s)
w = inv.get('hotbar.0') or {'c': {}}
check(s.ncall['rlk:items/equip_scan'] == sc0, f'3 F press: {s.ncall["rlk:items/equip_scan"] - sc0} scans in 6 ticks (want 0)')
check(w['c'].get('minecraft:custom_data', {}).get('rlk_ui', {}).get('role') == 'attack' and 'weapon.offhand' not in inv
      and 'minecraft:consumable' in w['c'] and str(w['c'].get('minecraft:item_model', '')).startswith('rlk:h/'),
      f'3 weapon back in hotbar.0 (model {w["c"].get("minecraft:item_model")}, consumable '
      f'{"minecraft:consumable" in w["c"]}), off hand empty')


# 4
def passes_after(edit):
    for _ in range(3):
        tick(s)
    sc = s.ncall['rlk:items/equip_scan']
    edit()
    tick(s)
    return s.ncall['rlk:items/equip_scan'] - sc


def swap():
    inv['inventory.9'], inv['inventory.10'] = inv['inventory.10'], inv['inventory.9']
    s.call('rlk:player/inv/dirty', pctx(s))


check(passes_after(swap) >= 1, '4 two items swapped in the inventory -> a sort')
order0 = list(s.storage['rlk:pinv']['order'])


def item_to_offhand():                 # F over an item slot with the inventory open: the item goes to the off hand
    inv['weapon.offhand'] = inv.pop('inventory.11')
    s.call('rlk:player/inv/dirty', pctx(s))


check(passes_after(item_to_offhand) >= 1, '4 an rlk item moved to the off hand -> a sort (it is dropped as before)')


def map_event():
    s.setsc(P, 'vMap', 1)
    inv['weapon.offhand'] = {'id': 'minecraft:stick', 'c': {'minecraft:custom_data': {'rlk_ui': {'role': 'skill'}}}, 'count': 1}
    s.call('rlk:player/inv/dirty', pctx(s))


check(passes_after(map_event) >= 1, '4 an inventory event with the map open and a UI item in the off hand -> a sort')
s.setsc(P, 'vMap', 0)
print('test_lag:', 'PASS' if not fails else f'FAIL ({fails})')
sys.exit(1 if fails else 0)
