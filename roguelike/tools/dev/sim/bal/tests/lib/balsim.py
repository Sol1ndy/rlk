"""balsim.py — the simulator of the balance-gauge suite (combat overhaul lane B; scratch tool, never shipped).

`mcsim.py` here is a vendored, unchanged copy of `tools/dev/sim/hr/tests/lib/mcsim.py` (md5 7ac6cf81…). This file adds
what rlk:bal/** and the family paths use, as the game does it:
- `ride <e> mount <v>` and `execute on passengers|vehicle` (Ent.vehicle = the vehicle's id);
- entity NBT flags: `data merge entity <sel> {NoAI:1b,…}`, `execute if|unless data entity <sel> {NoAI:1b}`, NoAI from the
  summon NBT; `data modify entity <sel> text set from storage <st> <path>` / `set value` (Ent.text);
- `time query gametime` (Sim.gametime, advanced by tick()); `execute if|unless function` (mcsim's), `return fail`;
- a function allowlist: REAL prefixes run from the datapack, everything else is a logged no-op stub (Sim.stubbed: name,
  executor tags) — so a test can say which family functions were reached and that no attack start was called.
Unknown commands (particle, playsound, effect, team, attribute, …) are logged in Sim.cmds_seen and otherwise ignored.
"""
import copy
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcsim  # noqa: E402
from mcsim import Ent, Ctx, Return, split  # noqa: E402

REAL_DEFAULT = ('rlk:bal/', 'rlk:cm/tick', 'rlk:cm/cancel', 'rlk:cm/c2/cancel', 'rlk:cm/c3/cancel', 'rlk:cm/dr/interrupt',
                'rlk:cm/hold_on', 'rlk:cm/hold_off', 'rlk:mob/unstun', 'rlk:mob/stun', 'rlk:element/frz_start',
                'rlk:element/frz_on', 'rlk:element/frz_end', 'rlk:element/frz_tick', 'rlk:mboss/d/bal_',
                'rlk:boss/raiden/bal_', 'rlk:boss/raiden/sg/stun_', 'rlk:mob/hb_cleanup', 'rlk:combat/apply_mods',
                'rlk:combat/clear_atkflags', 'rlk:items/hook/burst_dmg', 'rlk:char/after_hit')


class BalSim(mcsim.Sim):
    def __init__(self, dp, real=REAL_DEFAULT, extra_real=()):
        super().__init__(Path(dp) / 'data/rlk/function')
        self.dp = Path(dp)
        self.real = tuple(real) + tuple(extra_real)
        self.stubbed = []          # (gametime, fid, tags of the executor)
        self.cmds_seen = {}        # command word -> count (the ignored ones)
        self.sounds = []           # (gametime, event)
        self.particles = []        # (gametime, name, pos)
        self.gametime = 1000
        self.cmd_count = 0
        self.stub_fns = {}         # fid -> python callable(sim, ctx, macro) for stubs with behaviour
        self.objectives = set()

    # ------------------------------------------------------------ world helpers
    def spawn(self, etype, pos=(0.5, 201.0, 0.5), tags=(), nbt=None, **scores):
        e = Ent(etype, pos, (0.0, 0.0), tags)
        e.vehicle = None
        e.nbt = dict(nbt or {})
        e.text = None
        self.ents.append(e)
        for k, v in scores.items():
            self.setsc(('e', e.id), k, v)
        return e

    def ctx(self, e=None):
        return Ctx(e, tuple(e.pos) if e else (0.0, 0.0, 0.0), tuple(e.rot) if e else (0.0, 0.0))

    def run(self, fid, e=None, macro=None):
        return self.call(fid if ':' in fid else 'rlk:' + fid, self.ctx(e), macro)

    def s(self, e, obj):
        return self.sc(('e', e.id) if isinstance(e, Ent) else e, obj)

    def set(self, e, obj, v):
        self.setsc(('e', e.id) if isinstance(e, Ent) else e, obj, v)

    def passengers(self, e):
        return [x for x in self.ents if x.alive and getattr(x, 'vehicle', None) == e.id]

    def tick(self, n=1):
        self.gametime += n

    def stub_calls(self, pat=None):
        return [c for c in self.stubbed if pat is None or re.search(pat, c[1])]

    # ------------------------------------------------------------ functions
    def is_real(self, fid):
        return any(fid == r or (r.endswith('/') and fid.startswith(r)) or (not r.endswith('/') and fid.startswith(r) and r.endswith('_'))
                   for r in self.real)

    def call(self, fid, ctx, macro=None):
        if not self.is_real(fid):
            self.stubbed.append((self.gametime, fid, tuple(sorted(ctx.ex.tags)) if ctx.ex else ()))
            f = self.stub_fns.get(fid)
            return f(self, ctx, macro) if f else 1
        p = self.root / (fid.split(':', 1)[1] + '.mcfunction')
        if not p.exists():
            raise FileNotFoundError(fid)
        return super().call(fid, ctx, macro)

    # ------------------------------------------------------------ commands
    def cmd(self, t, ctx):
        self.cmd_count += 1
        c = t[0]
        if c == 'ride':
            src = self.select(t[1], ctx) if t[1] != '@s' else [ctx.ex]
            if t[2] == 'mount':
                dst = self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]
                if src and dst:
                    src[0].vehicle = dst[0].id
            elif t[2] == 'dismount' and src:
                src[0].vehicle = None
            return 1
        if c == 'time' and t[1] == 'query' and t[2] == 'gametime':
            return self.gametime
        if c == 'summon':
            n0 = len(self.ents)
            r = super().cmd(t, ctx)
            for e in self.ents[n0:]:
                e.vehicle = None
                e.nbt = {}
                e.text = None
                nbt = t[5] if len(t) > 5 else ''
                if re.search(r'NoAI:1b', nbt):
                    e.nbt['NoAI'] = 1
                m = re.search(r'translation:\[(-?[\d.]+)f,(-?[\d.]+)f,(-?[\d.]+)f\]', nbt)
                if m:
                    e.nbt['translation'] = tuple(float(x) for x in m.groups())
                m = re.search(r'scale:\[(-?[\d.]+)f', nbt)
                if m:
                    e.nbt['scale'] = float(m.group(1))
            return r
        if c == 'data' and t[1] == 'merge' and t[2] == 'entity':
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                for k, v in re.findall(r'(\w+):(-?\d+)b', t[4]):
                    e.nbt[k] = int(v)
            return 1
        if c == 'data' and t[1] == 'modify' and t[2] == 'entity' and t[4] == 'text':
            e = (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex])[0]
            if t[6] == 'from' and t[7] == 'storage':
                e.text = copy.deepcopy(self.path_get(self.storage[t[8]], t[9]))
            elif t[6] == 'value':
                e.text = t[7]
            return 1
        if c == 'playsound':
            self.sounds.append((self.gametime, t[1]))
            return 1
        if c == 'particle':
            self.particles.append((self.gametime, t[1].split('{')[0], ctx.pos))
            return 1
        if c == 'kill':
            r = super().cmd(t, ctx)
            alive = {e.id for e in self.ents}
            for e in self.ents:
                if getattr(e, 'vehicle', None) is not None and e.vehicle not in alive:
                    e.vehicle = None     # a passenger of a dead vehicle is dismounted (hb_cleanup then kills it)
            return r
        if c in ('effect', 'team', 'attribute', 'title', 'tellraw', 'bossbar', 'damage', 'swing', 'stopsound', 'item'):
            self.cmds_seen[c] = self.cmds_seen.get(c, 0) + 1
            return 1
        if c == 'return' and t[1] == 'fail':
            raise Return(0)
        if c == 'scoreboard' and t[1] == 'objectives':
            if t[2] == 'add':
                self.objectives.add(t[3])
            elif t[2] == 'remove':
                self.objectives.discard(t[3])
                for key in [k for k in self.scores if k[1] == t[3]]:
                    del self.scores[key]
            return 1
        return super().cmd(t, ctx)

    def execute(self, t, ctx):
        """mcsim's execute plus `on passengers|vehicle`, `if|unless data entity <sel> {..}` (NBT flags)."""
        i, stores = 0, []
        while i < len(t):
            k = t[i]
            if k == 'run':
                v = self.cmd(t[i + 1:], ctx)
                for s_ in stores:
                    self.store(s_, v, ctx)
                return v
            if k == 'as':
                ents = self.select(t[i + 1], ctx)
                if not ents:
                    return 0
                rest, last = t[i + 2:], 0
                for e in ents:
                    last = self.execute(rest, ctx.copy(ex=e))
                return last
            if k == 'on':
                rel = t[i + 1]
                if rel == 'passengers':
                    ents = self.passengers(ctx.ex) if ctx.ex else []
                else:
                    v = getattr(ctx.ex, 'vehicle', None)
                    ents = [e for e in self.ents if e.id == v and e.alive]
                if not ents:
                    return 0
                rest, last = t[i + 2:], 0
                for e in ents:
                    last = self.execute(rest, ctx.copy(ex=e))
                return last
            if k == 'at':
                ents = self.select(t[i + 1], ctx)
                if not ents:
                    return 0
                ctx = ctx.copy(pos=tuple(ents[0].pos), rot=tuple(ents[0].rot))
                i += 2
            elif k == 'positioned':
                if t[i + 1] == 'as':
                    ctx = ctx.copy(pos=tuple(self.select(t[i + 2], ctx)[0].pos))
                    i += 3
                else:
                    ctx = ctx.copy(pos=self.coords(t[i + 1:i + 4], ctx))
                    i += 4
            elif k == 'rotated':
                if t[i + 1] == 'as':
                    ctx = ctx.copy(rot=tuple(self.select(t[i + 2], ctx)[0].rot))
                else:
                    ctx = ctx.copy(rot=tuple(ctx.rot[j] + float(v[1:] or 0) if v.startswith('~') else float(v)
                                             for j, v in enumerate(t[i + 1:i + 3])))
                i += 3
            elif k in ('in', 'anchored'):
                i += 2
            elif k in ('if', 'unless'):
                neg = k == 'unless'
                kind = t[i + 1]
                if kind == 'score':
                    a = self.sc(self.holder(t[i + 2], ctx), t[i + 3])
                    if t[i + 4] == 'matches':
                        ok = self.in_range(a, t[i + 5])
                        i += 6
                    else:
                        b = self.sc(self.holder(t[i + 5], ctx), t[i + 6])
                        ok = a is not None and b is not None and {'<': a < b, '<=': a <= b, '=': a == b, '>=': a >= b,
                                                                  '>': a > b}[t[i + 4]]
                        i += 7
                elif kind == 'entity':
                    ok = bool(self.select(t[i + 2], ctx))
                    i += 3
                elif kind == 'data' and t[i + 2] == 'entity':
                    es = self.select(t[i + 3], ctx) if t[i + 3] != '@s' else ([ctx.ex] if ctx.ex else [])
                    want = {kk: int(vv) for kk, vv in re.findall(r'(\w+):(-?\d+)b', t[i + 4])}
                    ok = bool(es) and all(es[0].nbt.get(kk, 0) == vv for kk, vv in want.items())
                    i += 5
                elif kind == 'data':
                    try:
                        st = self.storage.get(t[i + 3], {})
                        if t[i + 4].startswith('{'):
                            pat = self.snbt(t[i + 4])
                            ok = all(self.match(st.get(kk), vv) for kk, vv in pat.items())
                        else:
                            self.path_get(st, t[i + 4])
                            ok = True
                    except (KeyError, IndexError, TypeError):
                        ok = False
                    i += 5
                elif kind == 'function':
                    ok = bool(self.call(t[i + 2], ctx))
                    i += 3
                else:
                    raise NotImplementedError(kind)
                if ok == neg:
                    return 0
            elif k == 'store':
                n = 4 if t[i + 2] == 'score' else 6
                stores.append(t[i + 1:i + 1 + n])
                i += 1 + n
            else:
                raise NotImplementedError(k)
        v = 1
        for s_ in stores:
            self.store(s_, v, ctx)
        return v


def ck(results, name, ok, info=''):
    results.append((name, bool(ok), info))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'   [{info}]'))
    return ok


def summary(results):
    bad = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(bad)}/{len(results)} passed' + (f', {len(bad)} FAILED' if bad else ''))
    return 1 if bad else 0
