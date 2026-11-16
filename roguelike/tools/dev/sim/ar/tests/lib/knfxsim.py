"""knfxsim.py: the mcsim harness of the 아를레키노 fx kit (stage S1K; test_kit.py and scratchpad ar/s1k/render_fx.py).

FxSim = mcsim.Sim (vendored unchanged) + the vanilla server-tick order of the Tachy / Apep kit tests (a tick T runs the
functions at gametime T, then gametime T + 1 and the scheduled functions), the item_display summon SNBT, stage merges,
`data merge entity` / `data modify entity` on the display NBT, particles, sounds, objectives, bossbars, titles,
`scoreboard players set` returning the value set (as 26.3), `append from storage <path>[]`, `execute summon`, and NBT
list filters `path[{...}]` in `data remove storage` / `if|unless data storage`.
"""
import copy
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcsim  # noqa: E402

TAG = 'rlk_kn_fx'
_FILT = re.compile(r"^([^[]*)\[(\{.*\})\]$")


def deep_merge(dst, src):
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = copy.deepcopy(v)


class FxSim(mcsim.Sim):
    def __init__(self, fn_root):
        super().__init__(fn_root)
        self.gt = 1000
        self.sched = {}
        self.events = []
        self.nbt = {}
        self.sounds = []
        self.parts = []
        self.merges = []
        self.objectives = set()
        self.born = {}
        self.bossbars = {}
        self.titles = []
        self.setsc('#true', '__sim', 1)
        self.setsc('#false', '__sim', 0)

    # ---------------------------------------------------------------- NBT list filters
    def _filtered(self, storage, path):
        """(list, [matching indices]) of storage path X[{...}], or None"""
        m = _FILT.match(path)
        if not m:
            return None
        try:
            lst = self.path_get(self.storage.get(storage, {}), m.group(1))
        except (KeyError, IndexError, TypeError):
            return [], []
        if not isinstance(lst, list):
            return [], []
        pat = self.snbt(m.group(2))
        return lst, [i for i, x in enumerate(lst) if self.match(x, pat)]

    def execute(self, t, ctx):
        t = list(t)
        for i in range(len(t) - 4):
            if t[i] in ('if', 'unless') and t[i + 1] == 'data' and t[i + 2] == 'storage' and _FILT.match(t[i + 4]):
                if i > 0 and t[i - 1] == 'run':
                    break
                _lst, idx = self._filtered(t[i + 3], t[i + 4])
                t[i:i + 5] = [t[i], 'score', '#true' if idx else '#false', '__sim', 'matches', '1']
        if t and t[0] == 'summon' and 'run' in t:
            k = t.index('run')
            e = mcsim.Ent(t[1].replace('minecraft:', ''), tuple(ctx.pos), tuple(ctx.rot), ())
            self.ents.append(e)
            return self.cmd(t[k + 1:], ctx.copy(ex=e))
        return super().execute(t, ctx)

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'execute' and len(t) == 9 and t[1:4] == ['store', 'result', 'score'] and t[6] == 'if' and t[7] == 'entity':
            n = len(self.select(t[8], ctx))
            for h in self.holders(t[4], ctx):
                self.setsc(h, t[5], n)
            return n
        if c == 'scoreboard' and t[1] == 'players' and t[2] in ('set', 'add', 'remove'):
            super().cmd(t, ctx)                                # vanilla 26.3: the new total (CommandResponseTracker)
            return sum(self.sc(h, t[4]) or 0 for h in self.holders(t[3], ctx))
        if c == 'scoreboard' and t[1] == 'objectives':
            if t[2] == 'add':
                self.objectives.add(t[3])
            elif t[2] == 'remove':
                self.objectives.discard(t[3])
                self.scores = {k: v for k, v in self.scores.items() if k[1] != t[3]}
            return 1
        if c == 'data' and t[1] == 'remove' and t[2] == 'storage' and _FILT.match(t[4]):
            lst, idx = self._filtered(t[3], t[4])
            for i in reversed(idx):
                del lst[i]
            return len(idx)
        if c == 'data' and t[1] == 'remove' and t[2] == 'storage' and t[4] in ('fx',) and t[3] in self.storage:
            self.storage[t[3]].pop('fx', None)
            return 1
        if (c == 'data' and t[1] == 'modify' and t[2] == 'storage' and t[5] == 'append' and t[6] == 'from'
                and t[7] == 'storage' and t[9].endswith('[]')):
            try:
                src = self.path_get(self.storage.get(t[8], {}), t[9][:-2])
            except KeyError:
                return 0
            st = self.storage.setdefault(t[3], {})
            try:
                lst = self.path_get(st, t[4])
            except KeyError:
                lst = []
                self.path_set(st, t[4], lst)
            lst.extend(copy.deepcopy(src))
            return 1
        if c == 'data' and t[1] == 'modify' and t[2] == 'storage' and t[6] == 'value' and t[7].startswith('[I;'):
            self.path_set(self.storage.setdefault(t[3], {}), t[4], [int(x) for x in t[7][3:-1].split(',')])
            return 1
        if c == 'time' and t[1] == 'query':
            return self.gt
        if c == 'schedule':
            if t[1] == 'function':
                self.sched[t[2]] = self.gt + int(t[3].rstrip('t'))
            elif t[1] == 'clear':
                self.sched.pop(t[2], None)
            return 1
        if c == 'summon' and t[1] == 'minecraft:item_display':
            parsed = self.snbt(t[5]) if len(t) > 5 else {}
            r = super().cmd(t, ctx)
            self.nbt[self.ents[-1].id] = parsed
            self.born[self.ents[-1].id] = self.gt
            return r
        if c == 'data' and t[1] == 'modify' and t[2] == 'entity':
            ents = self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]
            for e in ents:
                if t[4] == '{}' and t[5] == 'merge':
                    self.events.append((self.gt, e.id, t[-1].split('.')[-1]))
                elif 'colors[0]' in t[4]:
                    self.events.append((self.gt, e.id, 'hit'))
                    if t[6] == 'value':
                        n = self.nbt.setdefault(e.id, {})
                        n.setdefault('item', {}).setdefault('components', {}).setdefault(
                            'minecraft:custom_model_data', {})['colors'] = [int(t[7])]
                elif '"minecraft:item_model"' in t[4] and t[6] == 'value':
                    n = self.nbt.setdefault(e.id, {})
                    n.setdefault('item', {}).setdefault('components', {})['minecraft:item_model'] = t[7].strip('"')
                    self.events.append((self.gt, e.id, 'model:' + t[7].strip('"')))
            return 1
        if c == 'data' and t[1] == 'merge' and t[2] == 'entity':
            ents = self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]
            for e in ents:
                if e is not None:
                    self.merges.append((self.gt, e.id, t[4]))
                    try:
                        deep_merge(self.nbt.setdefault(e.id, {}), self.snbt(t[4]))
                    except ValueError:
                        pass
            return 1
        if c == 'kill':
            for e in self.select(t[1], ctx):
                self.events.append((self.gt, e.id, 'kill'))
        if c == 'playsound':
            self.sounds.append((t[1], float(t[7]), float(t[8]), float(t[9])))
        if c == 'particle':
            self.parts.append((t[1], self.coords(t[2:5], ctx)))
        if c == 'bossbar':
            bid = t[2]
            if t[1] == 'add':
                if bid in self.bossbars:
                    return 0
                self.bossbars[bid] = {'name': ' '.join(t[3:]), 'visible': True, 'players': ''}
            elif t[1] == 'remove':
                self.bossbars.pop(bid, None)
            elif t[1] == 'set' and bid in self.bossbars:
                self.bossbars[bid][t[3]] = ' '.join(t[4:]) if t[3] != 'visible' else t[4] == 'true'
            elif t[1] == 'set':
                return 0
            return 1
        if c == 'title':
            self.titles.append((self.gt, ' '.join(t[2:])))
            return 1
        return super().cmd(t, ctx)

    def tick(self, n=1):
        for _ in range(n):
            self.gt += 1
            for fid, at in sorted(self.sched.items(), key=lambda kv: kv[1]):
                if at <= self.gt and fid in self.sched:
                    del self.sched[fid]
                    self.call(fid, mcsim.Ctx(None, (0, 0, 0), (0, 0)))

    def run(self, line, pos=(760.5, 202.4, 8.5), rot=(0.0, 0.0), ex=None):
        return self.cmd(mcsim.split(line), mcsim.Ctx(ex or self.player, pos, rot))

    def cards(self, tag=TAG):
        return [e for e in self.ents if tag in e.tags and e.etype == 'item_display']


def fresh(fn_root):
    s = FxSim(fn_root)
    s.player = mcsim.Ent('player', (760.5, 201.0, 20.5), tags=('player',))
    s.ents.append(s.player)
    s.setsc(('e', s.player.id), 'dead', 0)
    s.setsc(('e', s.player.id), 'rnDie', 0)
    return s
