"""One F press (swap hands = the pack's dash) between ticks, then 6 ticks: how many dirty passes follow."""
import sys
sys.path.insert(0, '.')
import scen
from scen import *
CONS2 = CONS + ['function rlk:view/hand_wrap']
for tag, items, stars in (('small(3)', SMALL, 0), ('late(18,★★★)', LATE, 3)):
    s, pl = world(items, stars)
    s.cache['rlk:perf/ride_cons'] = CONS2
    P = ('e', pl.id)
    s.setsc(P, 'skillCd', 0); s.setsc(P, 'energy', 9999999)
    for _ in range(10): tick(s)
    inv = pl.data['inv']
    a0 = s.ncall['rlk:items/equip_scan']; n0 = s.n
    # the swap-hands packet: main hand (hotbar.0) <-> offhand, inventory_changed fires (reward = player/inv/dirty)
    inv['hotbar.0'], inv['weapon.offhand'] = inv.get('weapon.offhand'), inv['hotbar.0']
    if inv['hotbar.0'] is None: del inv['hotbar.0']
    s.call('rlk:player/inv/dirty', pctx(s))
    per = []
    for k in range(6):
        b = s.n; e0 = s.ncall['rlk:items/equip_scan']; w0 = dict(s.inv_change_where)
        tick(s)
        per.append((s.n - b, s.ncall['rlk:items/equip_scan'] - e0, {k_: v - w0.get(k_, 0) for k_, v in s.inv_change_where.items() if v - w0.get(k_, 0) and k_.startswith('rlk:view') or k_.startswith('rlk:perf') and v - w0.get(k_, 0)}))
    print(f'{tag}: after one F-dash: equip_scan runs {s.ncall["rlk:items/equip_scan"] - a0}, commands over 6 ticks {s.n - n0}')
    for k, p in enumerate(per):
        print('   tick', k + 1, p)
