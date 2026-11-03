#!/usr/bin/env python3
"""cmsim.py: the chapter-mode (AZ-CM) test world of the S1-CM suites (scratch tool, never shipped).

Built on vendored, unchanged copies of the S1-HARN harness (lib/azsim.py, lib/fgsim.py, lib/mcsim.py; md5 in
../README.md) so later edits there cannot move these suites. AzSim already runs the engine functions of plan 8.1 for
real (combat/apply with the AZ-CM lines, gold_drop, the room entry / clear functions, player/take_damage, the shields)
and resolves UUID selectors. CmSim adds what the chapter mode needs on top:

- a sparse block world: fill / setblock (strict, replace <block>, replace air) and `execute if|unless block`, so the
  sliced arena builds, look jobs, sentinels, clears and the barrier sweep are real;
- chunk loading: forceload add / remove per chunk with a configurable load delay (`LOAD_DELAY` ticks after the add),
  plus an always-loaded square around the player (`PLAYER_LOAD` blocks), and `execute if|unless loaded`;
- captured tellraw / title / stopsound lines (`s.tells`, `s.titles`, `s.stops`) next to fgsim's playsounds;
- quoted NBT path keys (cur.music."1".ev);
- the real F:mboss/arena/** (azsim stubs every arena ensure: removed here) and a room-generation emulation for boss
  maps (`boss_map`: the REAL room/pick/boss, then the zone markers and cells of rlk:room cur as room/gen_zones makes them).
"""
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import azsim as A  # noqa: E402
import fgsim as G  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ent, Ctx  # noqa: E402

C0 = G.C0
FAIL = []
LOAD_DELAY = [3]          # ticks after forceload add before the chunk counts as loaded
PLAYER_LOAD = [96]        # blocks around the player that are always loaded (the player's own view distance)


def check(name, ok, info=''):
    print(('ok   ' if ok else 'FAIL ') + name, info if info else '')
    if not ok:
        FAIL.append(name)
    return ok


def summary(label):
    print(f'ALL {label} CHECKS PASSED' if not FAIL else f'{len(FAIL)} {label} CHECK(S) FAILED: {FAIL}')
    sys.exit(1 if FAIL else 0)


def _path_parts(path):
    return re.findall(r'"[^"]*"|[^.\[\]"]+|\[-?\d+\]', path)


def _key(p):
    return p[1:-1] if p.startswith('"') else p


class CmSim(A.AzSim):
    # cproto's tiny anchor rig (clip / tick scores, two displays) is part of the framework test: it runs for real
    RIGS = tuple(r for r in A.AzSim.RIGS if 'cproto' not in r)

    def __init__(self, root):
        super().__init__(root)
        self.blocks = {}
        self.fl = {}              # (cx, cz) chunk -> tick it was forceloaded
        self.tells, self.titles, self.stops = [], [], []
        self.fills = 0
        self.difficulty = 2           # `difficulty` (query): 0 peaceful .. 3 hard
        self.big_fills = []           # (function, volume, command) of engine fills over the vanilla limit (they fail)
        self.gen_hook = None          # rlk:room/gen replacement (python), e.g. boss_map for test/chapter_ch

    def call(self, fid, ctx, macro=None):
        if fid == 'rlk:room/gen' and self.gen_hook is not None:
            self.gen_hook(self)
            return 1
        return super().call(fid, ctx, macro)

    # ------------------------------------------------------------------ storage paths: mcsim's NBT path grammar (S5)
    # ------------------------------------------------------------------ chunks
    def chunk_loaded(self, x, z):
        pl = self.player()
        if pl is not None and abs(pl.pos[0] - x) <= PLAYER_LOAD[0] and abs(pl.pos[2] - z) <= PLAYER_LOAD[0]:
            return True
        t0 = self.fl.get((math.floor(x) >> 4, math.floor(z) >> 4))
        return t0 is not None and self.t - t0 >= LOAD_DELAY[0]

    def forceload(self, op, x0, z0, x1, z1):
        for cx in range(min(x0, x1) >> 4, (max(x0, x1) >> 4) + 1):
            for cz in range(min(z0, z1) >> 4, (max(z0, z1) >> 4) + 1):
                if op == 'add':
                    self.fl.setdefault((cx, cz), self.t)
                else:
                    self.fl.pop((cx, cz), None)

    def forceloaded(self, x, z):
        return (math.floor(x) >> 4, math.floor(z) >> 4) in self.fl

    # ------------------------------------------------------------------ blocks
    @staticmethod
    def bname(b):
        b = b.replace('minecraft:', '')
        return b

    def block_test(self, pos, pred):
        x, y, z = (math.floor(v) for v in pos)
        if not self.chunk_loaded(x, z):
            return False
        cur = self.blocks.get((x, y, z), 'air')
        pred = self.bname(pred)
        if pred.startswith('#'):
            if pred in ('#rlk:dash_pass', '#rlk:cm_pass'):
                return cur in ('air', 'light', 'light[level=9]', 'light[level=15]') or cur.startswith('light')
            return False
        if '[' in pred and '[' not in cur:
            return cur == pred.split('[')[0]
        return cur == pred or cur.split('[')[0] == pred

    def setb(self, x, y, z, b):
        b = self.bname(b)
        if b == 'air':
            self.blocks.pop((x, y, z), None)
        else:
            self.blocks[(x, y, z)] = b

    def cmd(self, t, ctx):
        c = t[0]
        if (c == 'data' and len(t) == 10 and t[1] == 'modify' and t[2] == 'storage' and t[5] == 'set' and t[6] == 'from'
                and t[7] == 'entity' and t[9] in ('Pos', 'Rotation')):
            # `data modify storage <st> <path> set from entity <sel> Pos|Rotation` (mv/plpos, PERF-4): the whole list
            es = self.select(t[8], ctx) if t[8] != '@s' else [ctx.ex]
            if not es:
                return 0
            self.path_set(self.storage.setdefault(t[3], {}), t[4], list(es[0].pos if t[9] == 'Pos' else es[0].rot))
            return 1
        if c == 'forceload':
            if t[1] in ('add', 'remove') and len(t) >= 6:
                p0 = self.coords([t[2], '0', t[3]], ctx)
                p1 = self.coords([t[4], '0', t[5]], ctx)
                self.forceload(t[1], math.floor(p0[0]), math.floor(p0[2]), math.floor(p1[0]), math.floor(p1[2]))
            return 1
        if c == 'setblock':
            x, y, z = (math.floor(v) for v in self.coords(t[1:4], ctx))
            if not self.chunk_loaded(x, z):
                return 0
            self.setb(x, y, z, t[4])
            return 1
        if c == 'fill':
            a = [math.floor(v) for v in self.coords(t[1:4], ctx)]
            b = [math.floor(v) for v in self.coords(t[4:7], ctx)]
            blk = t[7]
            mode = t[8] if len(t) > 8 else 'replace'
            flt = self.bname(t[9]) if mode == 'replace' and len(t) > 9 and t[9] != 'strict' else None
            lo = [min(a[i], b[i]) for i in range(3)]
            hi = [max(a[i], b[i]) for i in range(3)]
            vol = (hi[0] - lo[0] + 1) * (hi[1] - lo[1] + 1) * (hi[2] - lo[2] + 1)
            if vol > 32768:
                # vanilla: the command fails (commandModificationBlockLimit 32768). A chapter-mode output that does it is
                # a generator bug (raise); an M0 engine file's oversize fill is recorded and fails as in game.
                fid = self.stack[-1] if self.stack else ''
                if fid.startswith(('rlk:mboss/', 'rlk:room/cboss/')):
                    raise RuntimeError(f'fill of {vol} blocks in {fid}: {" ".join(t)}')
                self.big_fills.append((fid, vol, ' '.join(t)))
                return 0
            if not (self.chunk_loaded(lo[0], lo[2]) and self.chunk_loaded(hi[0], hi[2])):
                return 0
            self.fills += 1
            n = 0
            for x in range(lo[0], hi[0] + 1):
                for y in range(lo[1], hi[1] + 1):
                    for z in range(lo[2], hi[2] + 1):
                        if flt is not None:
                            cur = self.blocks.get((x, y, z), 'air')
                            if cur != flt and cur.split('[')[0] != flt:
                                continue
                        self.setb(x, y, z, blk)
                        n += 1
            return n
        if c == 'tellraw':
            self.tells.append((self.t, ' '.join(t[2:])))
            return 1
        if c == 'title':
            self.titles.append((self.t, ' '.join(t[1:])))
            return 1
        if c == 'stopsound':
            self.stops.append((self.t, ' '.join(t[2:])))
            return 1
        if c == 'data' and len(t) == 5 and t[1] == 'remove' and t[2] == 'entity' and t[4] in ('attack', 'interaction'):
            ents = self.select(t[3], ctx) if t[3] != '@s' else ([ctx.ex] if ctx.ex else [])
            for e in ents:
                e.data.pop(t[4], None)
            return 1 if ents else 0
        if c == 'difficulty' and len(t) == 1:
            return self.difficulty
        return super().cmd(t, ctx)

    def execute(self, t, ctx):
        # `if|unless loaded x y z`: the chunk model (mcsim answers every loaded test with true)
        for i in range(len(t) - 4):
            if t[i] in ('if', 'unless') and t[i + 1] == 'loaded':
                p = self.coords(t[i + 2:i + 5], ctx)
                ok = self.chunk_loaded(p[0], p[2])
                if ok == (t[i] == 'unless'):
                    return 0
                return self.execute(t[:i] + t[i + 5:], ctx)
            if t[i] == 'run':
                break
        return super().execute(t, ctx)

    # interaction NBT `attack` / `interaction` (the stored click), kept in e.data: tested and removed for real
    def data_entity_test(self, kind, sel, path, ctx):
        if kind == 'entity' and path in ('attack', 'interaction'):
            ents = self.select(sel, ctx) if sel != '@s' else ([ctx.ex] if ctx.ex else [])
            return bool(ents) and path in ents[0].data
        return super().data_entity_test(kind, sel, path, ctx)

    def tell_text(self, since=0):
        return '\n'.join(x for tt, x in self.tells if tt >= since)


SCRATCH = HERE.parent / 'tmp'


def variant(dp, edit, label='v', gens=('build_mboss_core', 'build_mboss_arena', 'build_cboss_rooms')):
    """A temporary copy of the datapack tree (under ../tmp) whose registry `edit(reg)` changed, regenerated by `gens`.
    Generated folders (F:mboss, F:room/cboss, F:boss/test) and tools/ are real copies, everything else hard links (no
    generator writes there). tools/dev is never copied. Returns the copy's root; remove it with drop_variant.
    11-03 (deliberate deviations from the vendored copy): tools/dev is skipped, because this harness and its tmp/, where
    the copy is being built, may sit inside the tested tree (roguelike/tools/dev/sim) and the walk would copy the copy
    without end; F:boss/test is a real copy, because build_mboss_core.py writes it and a hard link let it rewrite the
    tested tree's files in place."""
    import os
    import shutil
    import subprocess
    import tempfile
    SCRATCH.mkdir(exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix=f'cm_{label}_', dir=SCRATCH)) / 'roguelike'
    src = Path(dp).resolve()
    real = ('data/rlk/function/mboss', 'data/rlk/function/room/cboss', 'data/rlk/function/boss/test', 'tools')
    for d, dirs, files in os.walk(src):
        rel = Path(d).relative_to(src)
        dirs[:] = [x for x in dirs if x not in ('__pycache__', '.git') and not (rel == Path('tools') and x == 'dev')]
        (root / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            r = (rel / f).as_posix()
            if any(r == p or r.startswith(p + '/') for p in real) or r == 'pack.mcmeta':
                shutil.copy2(Path(d) / f, root / rel / f)
            elif r.startswith('data/'):
                os.link(Path(d) / f, root / rel / f)
    regp = root / 'tools/mboss_registry.json'
    reg = json.loads(regp.read_text(encoding='utf-8'))
    edit(reg)
    regp.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for g in gens:
        r = subprocess.run([sys.executable, f'tools/{g}.py'], cwd=root, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f'{g} failed in the variant: {r.stdout[-500:]}{r.stderr[-1500:]}')
    return root


def drop_variant(root):
    import shutil
    shutil.rmtree(Path(root).parent, ignore_errors=True)


def entry(reg, bid):
    return next(b for b in reg['boss'] if b['id'] == bid)


def install(s, lv=4, hp=100000):
    """azsim's stubs minus its arena stubs (the real arena jobs run here)."""
    A.install_stubs(s, lv=lv, hp=hp)
    base = mcsim.Sim.load.__get__(s)

    def load_cm(fid):
        if fid not in s.cache and not fid.startswith(A.REAL_PREFIX) and fid not in A.REAL and fid.startswith(A.LEAF_PREFIX):
            s.cache[fid] = []
        return base(fid)
    s.load = load_cm
    for k in list(s.cache):
        if k.startswith('rlk:mboss/arena/'):
            del s.cache[k]
    s.cache['rlk:combat/input/poll_attack'] = ['scoreboard players add #POLLA mb 1', 'data remove entity @s attack']
    s.cache['rlk:combat/input/poll_right'] = ['scoreboard players add #POLLR mb 1']
    s.cache['rlk:room/gen'] = ['scoreboard players add #ROOMGEN azs 1']
    s.cache['rlk:room/obj/make_node'] = ['summon minecraft:marker ~ ~1 ~ {Tags:["rlk_obj","rlk_room","rlk_azs_new"]}',
                                         'scoreboard players operation @e[tag=rlk_azs_new] oact = #oact tmp',
                                         'scoreboard players operation @e[tag=rlk_azs_new] oarg = #oarg tmp',
                                         'scoreboard players add #MAKENODE mb 1',
                                         'tag @e[tag=rlk_azs_new] remove rlk_azs_new']
    for k in ('rlk:lobby/leave', 'rlk:lobby/go', 'rlk:run/save_pos', 'rlk:view/map_close', 'rlk:lvup/exit',
              'rlk:mboss/test/help', 'rlk:minimap/build'):
        s.cache[k] = []


def setup(dp, lv=4, hp=100000, seed=1018, player_level=5, player_pos=(0.5, 201.0, 33.5)):
    s, zone, pl = A.setup(force=0, lv=lv, hp=hp, seed=seed, player_level=player_level, player_pos=player_pos, dp=dp, cls=CmSim)
    install(s, lv=lv, hp=hp)
    s.call('rlk:mboss/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 5)
    s.setsc('#mapType', 'room', 8)
    return s, pl


def zones(s, kind=None):
    return A.zones(s, kind)


def boss_map(s, chapter=1):
    """The boss map of `chapter` as room/gen builds it (#mapType 8): the REAL room/pick/boss writes rlk:room cur, then
    one zone marker per zone (data = the zone record, zid / zkind / zst 0) with its cell markers, zone 1 built and
    visited (room/gen:22-23). Returns the zone markers; `#RDLAYOUT azs` counts Raiden's (stubbed) layout."""
    for e in s.ents:
        if 'rlk_room' in e.tags and e.etype != 'player':
            e.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.storage.setdefault('rlk:room', {}).pop('cur', None)
    s.setsc('#chapter', 'room', chapter)
    s.call('rlk:room/pick/boss', C0)
    cur = s.storage.get('rlk:room', {}).get('cur')
    out = []
    if not cur:
        return out
    for zr in cur['zones']:
        z = Ent('marker', (zr['cx'] + 0.0, zr['cy'], zr['cz'] + 0.0), tags=['rlk_room', 'rlk_zone'])
        z.data = json.loads(json.dumps(zr))
        s.ents.append(z)
        for o, v in (('zid', zr['id']), ('zkind', zr['kind']), ('zst', 0)):
            s.setsc(('e', z.id), o, v)
        for c in zr['cells']:
            m = Ent('marker', (c['x0'], 201, c['z0']), tags=['rlk_room', 'rlk_zcell'])
            s.ents.append(m)
            for o in ('ex0', 'ex1', 'ez0', 'ez1'):
                s.setsc(('e', m.id), o, c[o])
            s.setsc(('e', m.id), 'zid', zr['id'])
        out.append(z)
    z1 = [z for z in out if s.sc(('e', z.id), 'zid') == 1]
    if z1:
        s.call('rlk:room/zone_build', Ctx(z1[0], tuple(z1[0].pos), (0, 0)))
    return out


def entrance(s, zs=None):
    """Build and enter the kind-9 entrance zone (as door_reveal and the player stepping in do): the REAL zone_build
    (-> room/cboss/<id>/build -> cb/prep) and zone_enter (-> cb/enter -> k_cboss). Returns (zone, gate or None)."""
    z9 = [z for z in (zs or zones(s, 9)) if s.sc(('e', z.id), 'zkind') == 9][0]
    zc = Ctx(z9, tuple(z9.pos), (0, 0))
    s.call('rlk:room/zone_build', zc)
    s.call('rlk:room/zone_enter', zc)
    return z9, gate_of(s)


def gate_of(s):
    gs = [e for e in s.ents if e.alive and 'rlk_obj' in e.tags and s.sc(('e', e.id), 'oact') == 16]
    return gs[-1] if gs else None


def click(s, obj):
    return s.call('rlk:room/obj/click', Ctx(obj, tuple(obj.pos), (0, 0)))


def moved(s):
    """A test teleport of the player inside one sim tick (pl.pos = ...): mv/plpos caches the body position per game
    tick (PERF-4), as a player's own movement happens between ticks; the test drops the cache like a chapter-runtime
    teleport does (#mbPlG -1)."""
    s.setsc('#mbPlG', 'mb', -1)


def world(s):
    A.world(s)


def run(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        world(s)


def until(s, cond, limit=1500):
    for _ in range(limit):
        if cond(s):
            return True
        world(s)
    return cond(s)


def body_of(s):
    return A.body_of(s)


def mb(s, k):
    return s.sc(k, 'mb')


def esc(s, e, o):
    return s.sc(('e', e.id), o)


def proxies(s):
    return [e for e in s.ents if e.alive and 'rlk_mb_px' in e.tags]


def fight(s, boss_id='cproto', chapter=1, limit=1500):
    """test/chapter_ch-like entry without the command: the boss map with #cbForce (under #mbTest 1), the entrance,
    the gate pressed once no arena job runs, until the fight state (#mbSt 1). Returns (zone, gate)."""
    rec = s.storage['rlk:mboss']['cbyid'][boss_id]
    s.setsc('#mbTest', 'mb', 1)
    s.setsc('#cbForce', 'mb', rec['n'])
    zs = boss_map(s, chapter)
    z9, gate = entrance(s, zs)
    pl = s.player()
    pl.pos = [z9.pos[0], 201.0, z9.pos[2] + 4]
    ok = until(s, lambda s: (mb(s, '#mbArBuild') or 0) == 0, limit)
    gate = gate_of(s)
    if gate is None:
        raise RuntimeError('no gate object')
    click(s, gate)
    if not until(s, lambda s: (mb(s, '#mbSt') or 0) == 1, limit):
        raise RuntimeError('the chapter boss did not reach the fight state')
    return z9, gate
