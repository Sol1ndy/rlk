"""Prototype of the topic-3 gate + test: lvup/pick_sub with the combat gate, titles logged per tick."""
import sys
sys.path.insert(0, '.')
from psim import *
FN = Path('/home/user/rlk/roguelike/data/rlk/function')
PS = (FN / 'lvup/pick_sub.mcfunction').read_text(encoding='utf-8').split('\n')
i = next(k for k, l in enumerate(PS) if 'set #ps tmp 1' in l)
GATE = ['execute if score #active room matches 1 if score #combat room matches 1.. run scoreboard players set #ps tmp 0',
        'execute if score #mbLive mb matches 1 run scoreboard players set #ps tmp 0']
PSG = PS[:i + 1] + GATE + PS[i + 1:]

class T(PSim):
    def cmd(self, t, ctx):
        if t[0] == 'title':
            self.titles.append((self.t, ' '.join(t[2:4])))
        return super().cmd(t, ctx)

def run(lines, script):
    s = T(FN); s.titles = []
    pl = Ent('player', (0, 64, 0), (0, 0), ['player', 'rlk_body']); s.ents.append(pl); s.player = pl
    s.cache['rlk:lvup/pick_sub'] = lines
    s.cache['rlk:view/ttl_blank'] = []
    P = ('e', pl.id)
    for o, v in (('pkPending', 2), ('pkMode', 0), ('dead', 0), ('ttlT', 0), ('pkSubT', 0)):
        s.setsc(P, o, v)
    for k, o, v in (('#on', 'view', 1), ('#vmode', 'view', 2), ('#active', 'room', 1), ('#combat', 'room', 0), ('#mbLive', 'mb', 0)):
        s.setsc(k, o, v)
    out = []
    for t in range(1, 121):
        s.t = t
        for (at, k, o, v) in script:
            if at == t:
                s.setsc(k, o, v)
        n0 = len(s.titles)
        s.call('rlk:lvup/pick_sub', pctx(s))
        out.append((t, [x[1] for x in s.titles[n0:]]))
    return out

script = [(30, '#combat', 'room', 3), (70, '#combat', 'room', 0), (90, '#mbLive', 'mb', 1)]
for name, lines in (('now', PS), ('gated', PSG)):
    out = run(lines, script)
    sub = [t for t, x in out if any(y.startswith('@s subtitle') or y.startswith('subtitle') for y in x)]
    clr = [t for t, x in out if any('clear' in y for y in x)]
    print(name, 'subtitle sent at ticks', sub, 'clear at', clr)
