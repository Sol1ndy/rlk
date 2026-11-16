import sys, time
sys.path.insert(0, '.')
from psim import *
DP = Path('/home/user/rlk/roguelike')
s = PSim(DP / 'data/rlk/function')
pl = Ent('player', (0.5, 64.0, 0.5), (0.0, 0.0), ['player', 'rlk_body'])
s.ents.append(pl); s.player = pl
t0 = time.time()
s.call('rlk:load', Ctx(None, (0, 0, 0), (0, 0)))
print('load', time.time() - t0, 'cmds', s.n)
for k, v in s.errors.most_common(40):
    print(v, k)
print('ignored', sorted(s.ignored.items(), key=lambda x: -x[1])[:20])
print('ids', len(s.storage.get('rlk:items', {}).get('ids', [])))
