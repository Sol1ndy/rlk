"""F1: the consumable component lands in the same tick as the rebuild (inside player/tick's self-event window):
modelled as ride_cons right after player/tick's char/hotbar, i.e. before the invEvt reset (player/tick:98)."""
import sys
sys.path.insert(0, '.')
import scen
from scen import *
PT = (FN / 'player/tick.mcfunction').read_text(encoding='utf-8').split('\n')
j = next(i for i, l in enumerate(PT) if 'player/hotbar/tick' in l)
PT2 = PT[:j + 1] + ['function rlk:perf/ride_cons'] + PT[j + 1:]

def run(tag, items, stars):
    s, pl = world(items, stars)
    s.cache['rlk:player/tick'] = PT2
    P = ('e', pl.id)
    s.setsc(P, 'skillCd', 0); s.setsc(P, 'energy', 9999999)
    for _ in range(5): tick(s)
    ml0 = sum(s.macro_lines.values())
    report(f'F1 {tag} out of combat', measure(s, 400), 400)
    report(f'F1 {tag} combat churn', measure(s, 400, combat_after), 400)
for tag, items, stars in (('small(3)', SMALL, 0), ('late(18,★★★)', LATE, 3)):
    run(tag, items, stars)
