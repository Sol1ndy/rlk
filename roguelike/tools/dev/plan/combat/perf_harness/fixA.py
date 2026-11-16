"""Fix A: A1 consumable + hand_wrap right after the hotbar rebuild (inside player/tick's self-event window);
A2 an F swap of a UI item (handled by player/hotbar/tick this tick) does not mark the inventory dirty."""
import sys
sys.path.insert(0, '.')
from scen import *
CONS2 = CONS + ['function rlk:view/hand_wrap']
PT = (FN / 'player/tick.mcfunction').read_text(encoding='utf-8').split('\n')
j = next(i for i, l in enumerate(PT) if 'player/hotbar/tick' in l)
k = next(i for i, l in enumerate(PT) if 'invEvt matches 1..' in l)
PTA = list(PT)
PTA[k] = 'execute if score @s invEvt matches 1.. unless items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{}}] run scoreboard players set @s invDirty 2'
PTA = PTA[:j + 1] + ['function rlk:perf/ride_cons'] + PTA[j + 1:]
for tag, items, stars in (('small(3)', SMALL, 0), ('late(18,★★★)', LATE, 3)):
    s, pl = world(items, stars)
    s.cache['rlk:perf/ride_cons'] = CONS2
    s.cache['rlk:player/tick'] = PTA
    P = ('e', pl.id)
    s.setsc(P, 'skillCd', 0); s.setsc(P, 'energy', 9999999)
    for _ in range(10): tick(s)
    inv = pl.data['inv']
    a0 = s.ncall['rlk:items/equip_scan']; n0 = s.n
    inv['hotbar.0'], inv['weapon.offhand'] = inv.get('weapon.offhand'), inv['hotbar.0']
    if inv['hotbar.0'] is None: del inv['hotbar.0']
    s.call('rlk:player/inv/dirty', pctx(s))
    for _ in range(6): tick(s)
    ok = 'hotbar.0' in inv and inv['hotbar.0']['c'].get('minecraft:custom_data', {}).get('rlk_ui', {}).get('role') == 'attack' and 'weapon.offhand' not in inv
    print(f'A {tag}: F-dash -> equip_scan runs {s.ncall["rlk:items/equip_scan"] - a0}, commands over 6 ticks {s.n - n0}; weapon back in hotbar.0 {ok}, consumable {"minecraft:consumable" in inv["hotbar.0"]["c"]}, model {inv["hotbar.0"]["c"].get("minecraft:item_model")}')
    report(f'A {tag} combat churn', measure(s, 400, combat_after), 400)
