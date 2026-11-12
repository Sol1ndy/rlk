#!/usr/bin/env python3
"""hrsim.py: the generic world of the 홍련 (Scarlet, special boss) suites in HR/tests (scratch tool, never shipped).

S1 wrote it with the framework suite (test_special_hr.py); S3 takes HR/tests/lib over after S1's report and extends this
file (tools/mboss_scarlet/api.py HANDOVER); the other stages only read it and keep their own helpers in HR/<stage>/.

Built on vendored, UNCHANGED copies of R:tools/dev/sim/az/tests_cm/lib (cmsim -> azsim -> fgsim -> mcsim; md5s in
README.md beside this file). HrSim = Log + cmsim.CmSim (special fights), AzLog = Log + azsim.AzSim (mid-boss fights in
the plaza with azsim's stubs). What this file adds on top of the chapter-mode world:

- the special-boss entry without a room layout: rift_zone() places a combat zone marker tagged rlk_riftz with
  data.rift.id and an open rift anchor (rlk_rift, riftS 2) of the same zid; enter() runs the REAL mboss/sp/gate as that
  anchor (what room/rift/enter does on a walk-in or a click);
- the room tick of a rift zone (room/tick -> room/combat_tick, which azsim emulates for kind 9 / 15 zones only): the
  spawn countdown ends in the REAL room/mob_wave (its first line sends a rift zone with #spOn 1 to mboss/sp/start_zone),
  and a zone without rlk_zmob runs the REAL room/combat_clear (-> mboss/sp/clear -> sp/won -> sp/won_kill -> sp/reward).
  azsim.room_tick is wrapped at import (module attribute; the vendored file is not edited): every other zone keeps
  azsim's own room tick;
- room/tick's rift line (room/tick:21): the REAL room/rift/tick while #riftOn room is 1, after azsim's tick (the 30-t
  collapse of room/rift/close and the boxes of room/rift/close_end; schedules ran first, harmless for the rift);
- `function <f> with entity <sel> data.<path>`: the macro arguments come from that path (mcsim passes the whole data
  compound), so mboss/sp/start_zone -> sp/start {id} runs as in game;
- logs: s.particles (tick, particle name, pos), s.bars (visible flag per boss bar id), s.bar_draws (ticks of the name
  draw of rlk:mboss, i.e. one mboss/bars run), s.watch {function id: [(tick, executor etype, executor tags, pos)]}
  (fill the dict with the ids to watch before running).

Usage (from a suite in HR/tests): sys.path.insert(0, HERE / 'lib'); import hrsim as H; s, pl = H.setup(dp);
z, a, ok = H.special_fight(s, 'spproto'); H.kill(s, pl); H.finish(s).
"""
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cmsim as C  # noqa: E402
import azsim as A  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ent, Ctx  # noqa: E402

C0 = C.C0
FAIL = C.FAIL
check, summary = C.check, C.summary
variant, drop_variant, entry = C.variant, C.drop_variant, C.entry


class Log:
    """Mixin (before the sim class in the bases): the logs and the `function ... with entity <sel> data.<path>` fix."""

    def __init__(self, root):
        super().__init__(root)
        self.particles = []          # (tick, name, executor position: the particle's own ~ offsets are not applied)
        self.bars = {}               # bossbar id -> visible (bool)
        self.bar_draws = []          # ticks of `bossbar set rlk:mboss name ...` (one per mboss/bars run)
        self.watch = {}              # function id -> [(tick, executor etype, executor tags, pos)]

    def call(self, fid, ctx, macro=None):
        if fid in self.watch:
            ex = ctx.ex
            self.watch[fid].append((self.t, ex.etype if ex is not None else None,
                                    frozenset(ex.tags) if ex is not None else frozenset(), tuple(ctx.pos)))
        return super().call(fid, ctx, macro)

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'function' and len(t) >= 6 and t[2] == 'with' and t[3] == 'entity':
            es = self.select(t[4], ctx) if t[4] != '@s' else ([ctx.ex] if ctx.ex else [])
            if not es:
                return 0
            try:
                macro = es[0].data if t[5] == 'data' else self.path_get(es[0].data, t[5][5:]) if t[5].startswith('data.') else None
            except (KeyError, IndexError, TypeError):
                return 0                  # vanilla: a missing path fails the call
            if not isinstance(macro, dict):
                return 0
            return self.call(t[1], ctx, macro)
        if c == 'particle':
            self.particles.append((self.t, t[1].split('{')[0].replace('minecraft:', ''), tuple(ctx.pos)))
        elif c == 'bossbar' and len(t) >= 5 and t[1] == 'set':
            if t[3] == 'visible':
                self.bars[t[2]] = t[4] == 'true'
            elif t[3] == 'name' and t[2] == 'rlk:mboss':
                self.bar_draws.append(self.t)
        return super().cmd(t, ctx)


# I1b: the walk-through block tags as the game reads them. cmsim's block_test lets only air and light through #rlk:dash_pass
# / #rlk:cm_pass (enough on D0's stub arena); S1K's hr_field has dry grass / crimson roots in the walk disc, which the real
# tags let through (#minecraft:replaceable, and dash_pass names short_dry_grass / tall_dry_grass itself), so in the sim
# mv/ok refused every plant cell and a walk leg or a move stopped at the first tuft. These two tags are now resolved from
# the datapack's own tag files; the vanilla tags they name use their 26.3 contents (replaceable listed; the others by name).
MC_BLOCK_TAGS = {
    'replaceable': ('air', 'water', 'lava', 'short_grass', 'fern', 'dead_bush', 'bush', 'red_shrub', 'short_dry_grass',
                    'tall_dry_grass', 'seagrass', 'tall_seagrass', 'fire', 'soul_fire', 'snow', 'vine', 'glow_lichen',
                    'resin_clump', 'light', 'tall_grass', 'large_fern', 'structure_void', 'void_air', 'cave_air',
                    'bubble_column', 'warped_roots', 'nether_sprouts', 'crimson_roots', 'leaf_litter', 'hanging_roots'),
}
MC_BLOCK_TAG_RULES = {
    'small_flowers': lambda b: b in ('dandelion', 'poppy', 'blue_orchid', 'allium', 'azure_bluet', 'oxeye_daisy', 'cornflower',
                                     'lily_of_the_valley', 'wither_rose', 'torchflower', 'open_eyeblossom', 'closed_eyeblossom')
                               or b.endswith('_tulip'),
    'rails': lambda b: b in ('rail', 'powered_rail', 'detector_rail', 'activator_rail'),
    'buttons': lambda b: b.endswith('_button'),
    'wool_carpets': lambda b: b.endswith('_carpet') and b != 'moss_carpet' and b != 'pale_moss_carpet',
}
PASS_TAGS = ('#rlk:dash_pass', '#rlk:cm_pass')


class HrSim(Log, C.CmSim):
    """The chapter-mode world (block world, chunks, tellraw / title capture) with the logs: special fights."""

    def _tag_test(self, tag, b, seen=()):
        if tag.startswith('#minecraft:'):
            name = tag[11:]
            if name in MC_BLOCK_TAGS:
                return b in MC_BLOCK_TAGS[name]
            return MC_BLOCK_TAG_RULES.get(name, lambda _b: False)(b)
        if tag in seen or not tag.startswith('#rlk:'):
            return False
        cache = self.__dict__.setdefault('_tag_vals', {})
        if tag not in cache:
            f = self.root.parent / 'tags/block' / f'{tag[5:]}.json'
            cache[tag] = json.loads(f.read_text(encoding='utf-8')).get('values', []) if f.exists() else []
        for v in cache[tag]:
            v = v['id'] if isinstance(v, dict) else v
            if v.startswith('#'):
                if self._tag_test(v, b, seen + (tag,)):
                    return True
            elif v.replace('minecraft:', '') == b:
                return True
        return False

    def block_test(self, pos, pred):
        if self.bname(pred) in PASS_TAGS:
            x, y, z = (math.floor(v) for v in pos)
            if not self.chunk_loaded(x, z):
                return False
            cur = self.blocks.get((x, y, z), 'air').split('[')[0]
            return self._tag_test(self.bname(pred), cur)
        return super().block_test(pos, pred)


class AzLog(Log, A.AzSim):
    """azsim's world with the logs: mid-boss fights in the plaza (azsim's stubs, A.setup(..., cls=AzLog) + A.to_fight)."""


def setup(dp, seed=1018, lv=4, hp=100000, player_level=5, player_pos=(0.5, 201.0, 0.5)):
    """A fresh world on the datapack root dp (cmsim.setup with HrSim): the player in a normal map (#mapIdx 2, #mapType 1),
    first person, the rift objectives and constants of room/rift/init, no zone yet. `random` seeded with seed."""
    s, zone, pl = A.setup(force=0, lv=lv, hp=hp, seed=seed, player_level=player_level, player_pos=player_pos, dp=dp,
                          cls=HrSim)
    C.install(s, lv=lv, hp=hp)
    s.call('rlk:mboss/init', C0)
    s.call('rlk:room/rift/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 2)
    s.setsc('#mapType', 'room', 1)
    return s, pl


def rift_zone(s, sid, zid=7, at=(6.5, 201.0, 6.5), yaw=90.0):
    """A visited combat zone (kind 1, zst 2, rlk_riftz, data.rift.id = sid) and its open rift anchor 3 b east of the zone
    marker, facing the zone centre (yaw 90 = west). Returns (zone, anchor)."""
    z = Ent('marker', at, tags=['rlk_room', 'rlk_zone', 'rlk_riftz'])
    z.data = {'rift': {'id': sid}}
    s.ents.append(z)
    for o, v in (('zid', zid), ('zkind', 1), ('zst', 2)):
        s.setsc(('e', z.id), o, v)
    a = Ent('marker', (at[0] + 3.0, at[1], at[2]), (yaw, 0.0), tags=['rlk_room', 'rlk_rift'])
    s.ents.append(a)
    for o, v in (('zid', zid), ('riftS', 2), ('riftT', 0), ('riftCd', 0), ('riftDw', 0), ('riftPk', 0)):
        s.setsc(('e', a.id), o, v)
    s.setsc('#riftOn', 'room', 1)
    s.setsc('#riftUsed', 'room', 1)
    return z, a


def ctx(e):
    return Ctx(e, tuple(e.pos), tuple(e.rot))


def enter(s, anchor):
    """The REAL mboss/sp/gate as the anchor (room/rift/enter's call): 1 = the fight starts, 0 = refused."""
    return s.call('rlk:mboss/sp/gate', ctx(anchor))


# ------------------------------------------------------------------------------------------------- the tick
_AZ_ROOM_TICK = A.room_tick


def room_tick(s):
    """azsim.room_tick, plus the combat tick of a rift zone (room/combat_tick: spawn countdown -> REAL room/mob_wave,
    no rlk_zmob left -> REAL room/combat_clear)."""
    zid = s.sc('#combat', 'room') or 0
    if zid >= 1:
        zs = [e for e in A.zones(s) if s.sc(('e', e.id), 'zid') == zid and 'rlk_riftz' in e.tags]
        if zs:
            z = zs[0]
            zc = Ctx(z, tuple(z.pos), (0, 0))
            if (s.sc('#spawnT', 'room') or 0) >= 1:
                s.setsc('#spawnT', 'room', s.sc('#spawnT', 'room') - 1)
                if s.sc('#spawnT', 'room') == 0:
                    s.call('rlk:room/mob_wave', zc)
            elif not s.select('@e[tag=rlk_zmob,limit=1]', C0):
                s.call('rlk:room/combat_clear', zc)
            return
    _AZ_ROOM_TICK(s)


A.room_tick = room_tick


def world(s):
    """One game tick: azsim's (rlk:tick order, with the rift-zone room tick above), then room/tick's rift line."""
    A.world(s)
    if (s.sc('#riftOn', 'room') or 0) == 1 and (s.sc('#active', 'room') or 0) == 1:
        s.call('rlk:room/rift/tick', C0)


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


def mb(s, k):
    return s.sc(k, 'mb')


def room(s, k):
    return s.sc(k, 'room')


def esc(s, e, o):
    return s.sc(('e', e.id), o)


def body_of(s):
    return A.body_of(s)


def boxes(s):
    return [e for e in s.ents if e.alive and 'rlk_mb_box' in e.tags]


# ------------------------------------------------------------------------------------------------- flows
def special_fight(s, sid, zid=7, limit=900):
    """The rift of special `sid` entered (REAL sp/gate as its anchor), then ticks until the fight state (#mbSt 1).
    Returns (zone, anchor, ok)."""
    z, a = rift_zone(s, sid, zid=zid)
    s.player().pos = list(a.pos)
    r = enter(s, a)
    ok = bool(r) and until(s, lambda s: (mb(s, '#mbSt') or 0) == 1, limit)
    return z, a, ok


def kill(s, pl):
    """/function rlk:mboss/test/kill as the player: a lethal true hit (the kill / reward path)."""
    return s.call('rlk:mboss/test/kill', ctx(pl))


def finish(s, limit=1500):
    """Ticks until the fight is over and its zone cleared (#mbLive 0, #combat 0): the death sequence, death_finish,
    room/combat_clear -> mboss/sp/clear -> sp/won (+ won_kill / won_cancel)."""
    return until(s, lambda s: (mb(s, '#mbLive') or 0) == 0 and (room(s, '#combat') or 0) == 0, limit)


def register_text(dp):
    return (Path(dp) / 'data/rlk/function/mboss/register.mcfunction').read_text(encoding='utf-8')


def record(txt, bid, n):
    """The SNBT record text of entry bid / n in a register text (balanced braces from '{id:"<id>",n:<n>,'), or ''."""
    i = txt.find(f'{{id:"{bid}",n:{n},')
    if i < 0:
        return ''
    depth, q = 0, False
    for j in range(i, len(txt)):
        ch = txt[j]
        if q:
            q = not (ch == '"' and txt[j - 1] != '\\')
        elif ch == '"':
            q = True
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return txt[i:j + 1]
    return ''


# =================================================================================================== S3 additions (11-05)
# The 홍련 module suites (test_scarlet.py, pat_p1.py, test_reward.py; S4's pat_ghost.py may use them): ScSim = HrSim +
# - a dodge model (combat overhaul C, 11-10; was a dash i-frame model on dashInvT): s.dash() starts a dodge on the next world
#   tick: the player's dgAt = that tick's gametime (fgsim's gametime is the world tick), so the REAL player/def/judge (through
#   player/take_damage) sees a perfect dodge for 0..2 t and the pip rule of shield/pip (player/def/q_pf0 / q_pf1: a dodge or
#   an F press 0..2 t before the strike) runs as in game; s.parry() stamps an F press (parAt) the same way. No i-frames;
# - `if|unless predicate rlk:in_sneak` (and the selector argument predicate=rlk:in_sneak): the player's e.data['sneak'];
# - `scoreboard players reset * <objective>`, `scoreboard objectives remove <objective>` (its scores go); per-world-tick command counts (s.cmd_hist); the rig calls of the module
#   (s.rigl: (tick, call)); every hazard made (s.hzr: options, position, yaw, #pt / #pat / #ph of hr); every player hit
#   (s.phits); kit calls under rlk:boss/scarlet/fx/ are stubbed and logged (s.kitl) when a dry build references them;
# - I1b verification round 1: s.kit_real = True runs the kit (rlk:boss/scarlet/fx/**) for real instead, as azsim runs its
#   KITS: the presets' cards, the card ager they schedule (fx/e/world, every tick while a card lives), the cull, the HUD
#   tickers, so their commands are counted (test_scarlet `cost`); s.kitl still logs the calls from outside the kit. Two
#   harness fixes the kit needs (as in the kit's own harness, hr/s1k/lib): typed arrays [I; ...] in SNBT values, and
#   `execute summon <type>` (the summoned entity becomes the executor; summon takes no rotation); kit_on(s) turns it on
#   together with vanilla's order of scheduled functions (s.sched_vanilla: world_sc runs them after the tick's functions at
#   gametime t + 1, in the same server tick, as the overworld's tickTime does; fgsim's order runs them a world tick later;
#   s.t and every log keep the world tick);
# - player/die stubbed (s.deaths; dead 1 or, with s.revive set, Ronova's revive: rnDie for s.revive ticks, then alive);
# - variant_hr(): cmsim.variant with F:boss/scarlet copied for real (a dry build may regenerate it there).
ROOT_SC = 'rlk:boss/scarlet/'
KIT_SC = ROOT_SC + 'fx/'


def kit_internal(sub):
    """A kit function the kit calls or schedules itself (fx/e/*, fx/hud/e/*, fx/p/e/*, fx/prop/e/*), not a kit API call."""
    return sub.startswith('e/') or '/e/' in sub


def ck(name, ok, info=''):
    """cmsim.check printing its info only on a failure."""
    return C.check(name, ok, '' if ok else info)


class ScSim(HrSim):
    def __init__(self, root):
        super().__init__(root)
        self.ncmd = 0
        self.cmd_hist = []
        self.rigl = []
        self.hzr = []
        self.phits = []
        self.kitl = []
        self.kitx = []               # I1b round 1: (executor tags, caller, #ph hr) of each s.kitl entry (same index), kit_ex()
        self.deaths = []
        self.dash_t0 = None
        self.revive = 0
        self.rn_left = 0
        self.hz_particles = []       # particles drawn inside the framework's hazard functions (outline / flash)
        self.kit_real = False        # I1b round 1: True = the kit runs for real (see the comment above ROOT_SC)
        self.sched_vanilla = False   # ... and True = scheduled functions run in the server tick that scheduled them 1t ahead
        self.gt_off = 0              # 1 while they run then (gametime t + 1; s.t and the logs keep the world tick)
        self.nkit = 0                # ... and the commands run inside the kit (per world tick in kit_hist)
        self.kit_hist = []
        self._kit_depth = 0

    # --- typed arrays in SNBT values (the kit's ease / sine tables: `data modify storage ... set value [I; ...]`)
    @staticmethod
    def snbt(s):
        return HrSim.snbt(re.sub(r'\[\s*[IBL]\s*;', '[', s))

    # --- the sneak predicate
    def _sneak(self, e):
        return bool(e is not None and e.data.get('sneak'))

    def select(self, sel, ctx):
        if 'predicate=rlk:in_sneak' in sel:
            base = sel.replace(',predicate=rlk:in_sneak', '').replace('predicate=rlk:in_sneak,', '').replace('[predicate=rlk:in_sneak]', '')
            return [e for e in super().select(base, ctx) if self._sneak(e)]
        return super().select(sel, ctx)

    def execute(self, t, ctx):
        # I1: an absolute `facing <x> <y> <z>` (S2b's seq/**: the moon) becomes `facing entity` of a fixed helper marker at
        # that point (mcsim knows only the entity form), so the subcommands keep their order (port of S2b's ev_dry.py).
        # The helper's tag starts with hrsim_ (never rlk_): no suite's entity filter sees it.
        t = list(t)
        j = 0
        while j < len(t) and t[j] != 'run':
            if t[j] == 'facing' and j + 3 < len(t) and t[j + 1] != 'entity':
                key = 'hrsim_fc_' + '_'.join(t[j + 1:j + 4]).replace('-', 'm').replace('.', 'p')
                if not any(key in e.tags for e in self.ents if e.alive):
                    self.ents.append(Ent('marker', [float(v) for v in t[j + 1:j + 4]], (0.0, 0.0), [key]))
                t[j:j + 4] = ['facing', 'entity', f'@e[tag={key},limit=1]', 'feet']
            j += 1
        # I1b round 1: `execute summon <type> ...` (the kit's height probe and beam marker): the entity is summoned at the
        # context position with rotation 0 0 (summon takes no execute rotation) and runs the rest as the executor; after other
        # subcommands it is the same as `... run execute summon <type> ...`
        j = 0
        while j < len(t) and t[j] != 'run':
            if t[j] == 'summon' and j + 1 < len(t):
                if j:
                    return self.execute(t[:j] + ['run', 'execute'] + t[j:], ctx)
                e = Ent(t[1].replace('minecraft:', ''), ctx.pos, (0.0, 0.0), [])
                self.ents.append(e)
                return self.execute(t[2:], ctx.copy(ex=e))
            j += 1
        # `if|unless predicate rlk:in_sneak` at the head of the chain (after `as`, mcsim recurses with the rest)
        i = 0
        while i < len(t) and t[i] not in ('run', 'as'):
            if t[i] in ('if', 'unless') and i + 2 < len(t) and t[i + 1] == 'predicate':
                ok = t[i + 2] == 'rlk:in_sneak' and self._sneak(ctx.ex)
                if t[i + 2] == 'rlk:in_jump':      # round V (lane VC): the cutscene skip is the jump key (seq/<name>/skipin)
                    ok = bool(ctx.ex is not None and (ctx.ex.data.get('jump') or 'jump' in ctx.ex.data.get('keys', ())))
                if ok == (t[i] == 'unless'):
                    return 0
                return self.execute(t[:i] + t[i + 3:], ctx)
            i += 1
        return super().execute(t, ctx)

    def cmd(self, t, ctx):
        self.ncmd += 1
        if self._kit_depth:
            self.nkit += 1
        if self.gt_off and t[0] in ('time', 'schedule'):
            # the scheduled phase of a vanilla-ordered tick (world_sc): the gametime is t + 1 there
            if t[:3] == ['time', 'query', 'gametime']:
                return self.t + self.gt_off
            if t[1] == 'function':
                self.sched[t[2]] = self.t + self.gt_off + int(t[3].rstrip('t'))
                return 1
        # I1: S2b's sequences use `tp <sel> <x y z> facing (entity <sel> [eyes|feet] | <x y z>)` and `rotate <sel> <yaw>
        # <pitch>` (port of S2b's ev_dry.py; mcsim's tp reads only an optional yaw / pitch, and has no rotate)
        if t[0] == 'tp' and len(t) > 6 and t[5] == 'facing':
            pos = self.coords(t[2:5], ctx)
            if t[6] == 'entity':
                tg = self.select(t[7], ctx)
                if not tg:
                    return 0
                tgt = list(tg[0].pos)
                if len(t) > 8 and t[8] == 'eyes':
                    tgt[1] += tg[0].data.get('eye', 0.0)
            else:
                tgt = self.coords(t[6:9], ctx)
            ents = self.select(t[1], ctx) if t[1] != '@s' else ([ctx.ex] if ctx.ex else [])
            for e in ents:
                e.pos = list(pos)
                dx, dy, dz = (tgt[k] - pos[k] for k in range(3))
                e.rot = [math.degrees(math.atan2(-dx, dz)), math.degrees(-math.atan2(dy, math.hypot(dx, dz)))]
            return 1 if ents else 0
        if t[0] == 'rotate' and len(t) >= 4:
            ents = self.select(t[1], ctx) if t[1] != '@s' else ([ctx.ex] if ctx.ex else [])
            if t[2] == 'facing':      # rotate <sel> facing (entity <sel> [eyes|feet] | <x y z>)  (F:mboss/pull/finish)
                if t[3] == 'entity':
                    tg = self.select(t[4], ctx)
                    if not tg:
                        return 0
                    tgt = list(tg[0].pos)
                    if len(t) > 5 and t[5] == 'eyes':
                        tgt[1] += tg[0].data.get('eye', 0.0)
                else:
                    tgt = self.coords(t[3:6], ctx)
                for e in ents:
                    dx, dy, dz = (tgt[k] - e.pos[k] for k in range(3))
                    e.rot = [math.degrees(math.atan2(-dx, dz)), math.degrees(-math.atan2(dy, math.hypot(dx, dz)))]
                return 1 if ents else 0
            for e in ents:
                e.rot = [ctx.rot[0] + float(t[2][1:] or 0) if t[2].startswith('~') else float(t[2]),
                         ctx.rot[1] + float(t[3][1:] or 0) if t[3].startswith('~') else float(t[3])]
            return 1 if ents else 0
        if t[0] == 'particle' and any(f.startswith('rlk:mboss/hz/') for f in self.stack):
            self.hz_particles.append((self.t, t[1].split('{')[0]))
        if t[0] == 'scoreboard' and len(t) == 4 and t[1] == 'objectives' and t[2] == 'remove':
            for k in [k for k in self.scores if k[1] == t[3]]:
                del self.scores[k]
            return 1
        if t[0] == 'scoreboard' and len(t) == 5 and t[1] == 'players' and t[2] == 'reset' and t[3] == '*':
            for k in [k for k in self.scores if k[1] == t[4]]:
                del self.scores[k]
            return 1
        return super().cmd(t, ctx)

    def call(self, fid, ctx, macro=None):
        if fid.startswith(ROOT_SC + 'rig/') or fid.startswith(ROOT_SC + 'rig_stub/'):
            self.rigl.append((self.t, fid.split('/', 3)[3]))
        if fid.startswith(KIT_SC):
            sub = fid[len(KIT_SC):]
            # stubbed: every call is logged; I1b round 1, kit_real: the kit runs (through azsim's call) and only the calls
            # from outside the kit are logged
            if not self.kit_real or (not kit_internal(sub) and not (self.stack and self.stack[-1].startswith(KIT_SC))):
                self.kitl.append((self.t, sub, dict(macro or {})))
                self.kitx.append((frozenset(ctx.ex.tags) if ctx.ex is not None else frozenset(),
                                  self.stack[-1] if self.stack else '', self.sc('#ph', 'hr')))
            if not self.kit_real:
                return 1
            self._kit_depth += 1
            try:
                return super().call(fid, ctx, macro)
            finally:
                self._kit_depth -= 1
        if fid == 'rlk:mboss/hz/make':
            g = lambda k: self.sc(k, 'mb')  # noqa: E731
            self.hzr.append(dict(t=self.t, tell=g('#hzW'), dmg=g('#hzD'), kind=g('#hzK'), r=g('#hzR'), a=g('#hzAng'),
                                 hw=g('#hzHW'), act=g('#hzAct'), quiet=g('#hzQuiet'), el=g('#hzEl'), kb=g('#hzKB'),
                                 sfx=g('#hzSfx'), vis=g('#hzVis'), grp=g('#hzGrp'), pos=tuple(ctx.pos), yaw=ctx.rot[0],
                                 pt=self.sc('#pt', 'hr'), pat=self.sc('#pat', 'hr'), ph=self.sc('#ph', 'hr')))
        if fid == 'rlk:cm/hit_pl2':
            self.phits.append((self.t, self.sc('#mbHitPct', 'mb'), self.sc('#cmEl', 'tmp'), self.sc('#pat', 'hr')))
        if fid == 'rlk:player/die':
            pl = ctx.ex
            self.deaths.append(self.t)
            if pl is not None:
                if self.revive:
                    self.setsc(('e', pl.id), 'rnDie', self.revive)
                    self.setsc(('e', pl.id), 'curHealth', 1)
                    self.rn_left = self.revive
                else:
                    self.setsc(('e', pl.id), 'curHealth', 0)
                    self.setsc(('e', pl.id), 'dead', 1)
            return 1
        return super().call(fid, ctx, macro)

    def run_sched_at(self, now):
        """fgsim's run_sched for the events due at gametime `now` (vanilla order: now = t + 1, gt_off 1 meanwhile)."""
        for fid, at in sorted(self.sched.items(), key=lambda x: x[1]):
            if at <= now and fid in self.sched:
                del self.sched[fid]
                self.call(fid, C0)

    def dash(self, v0=6, at=None):
        """A dodge started on the world tick `at` (default: the next one): world_sc stamps dgAt = that tick there (as the
        input pre-pass + player/def/dodge_stamp do before every hit of the tick). v0 is kept for the old call sites and
        ignored (11-10: no dash i-frames any more)."""
        self.dash_t0 = self.t + 1 if at is None else at
        self.dash_v0 = v0

    def parry(self, at=None):
        """An F press on the world tick `at` (default: the next one): world_sc stamps parAt there (lockouts not modelled)."""
        self.parry_t0 = self.t + 1 if at is None else at

    def dash_inv(self, t=None):
        """11-10: the dodge gives no i-frames (kept for old callers: always 0)."""
        return 0


def world_sc(s):
    """One game tick as azsim.world (rlk:tick's order) with the dodge model: a dodge (s.dash) or an F press (s.parry) of this
    tick is stamped before the player tick, as the input pre-pass does before every hit (the module's pip check and the
    hazards read it through player/def/judge / q_pf0); Ronova's revive counts down."""
    s.t += 1
    n0, k0 = s.ncmd, s.nkit
    pl = s.player()
    if pl is not None:
        v = 0
        s.setsc(('e', pl.id), 'dashInvT', v)
        s.iframe_end = -1
        if s.sc(('e', pl.id), 'parHit') is None:
            for o in ('parAt', 'parLk', 'parHit', 'dgAt', 'dgRw'):
                s.setsc(('e', pl.id), o, -1000000)
        if s.dash_t0 is not None and s.t == s.dash_t0:
            s.setsc(('e', pl.id), 'dgAt', s.t)
            s.setsc(('e', pl.id), 'dgRw', -1000000)
        if getattr(s, 'parry_t0', None) is not None and s.t == s.parry_t0:
            s.setsc(('e', pl.id), 'parAt', s.t)
            s.setsc(('e', pl.id), 'parHit', -1000000)
        if s.rn_left > 0:
            s.rn_left -= 1
            if s.rn_left == 0:
                s.setsc(('e', pl.id), 'rnDie', 0)
                s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))
        s.setsc('#hurtDmg', 'tmp', 0)
        s.call('rlk:player/elem_tick', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        s.setsc(('e', pl.id), 'dashInvT', v)
    s.call('rlk:fgtest/lowg', C0)
    for e in [e for e in s.ents if e.alive and 'rlk_mob' in e.tags and e.etype != 'player']:
        if (s.sc(('e', e.id), 'elAct') or 0) >= 1 and 'rlk_mb_dying' not in e.tags:
            s.call('rlk:element/tick', Ctx(e, tuple(e.pos), tuple(e.rot)))
    if (s.sc('#mbLive', 'mb') or 0) == 1:
        s.call('rlk:mboss/main', C0)
    A.room_tick(s)
    if (s.sc('#mbBoxOn', 'mb') or 0) == 1:
        s.call('rlk:mboss/box/all', C0)
    if not s.sched_vanilla:
        s.run_sched()
    if (s.sc('#riftOn', 'room') or 0) == 1 and (s.sc('#active', 'room') or 0) == 1:
        s.call('rlk:room/rift/tick', C0)
    if s.sched_vanilla:
        # vanilla (I1b round 1, kit_on): after the tick functions the overworld's tickTime sets gametime t + 1 and runs the
        # events due then, in the same server tick: `time query gametime` reads t + 1 there, and a `1t` made there is due at t + 2
        s.gt_off = 1
        try:
            s.run_sched_at(s.t + 1)
        finally:
            s.gt_off = 0
    if pl is not None:
        s.setsc(('e', pl.id), 'dashInvT', 0)
    s.cmd_hist.append(s.ncmd - n0)
    s.kit_hist.append(s.nkit - k0)
    if hasattr(s, 'max_cards'):
        s.max_cards = max(s.max_cards, len(s.kit_cards()))


def variant_hr(dp, edit, label='sc', gens=('build_mboss_core', 'build_mboss_arena', 'build_cboss_rooms')):
    """cmsim.variant, then F:boss/scarlet replaced by a real copy (a dry build may regenerate it there without writing
    through hard links into the tested tree)."""
    import shutil
    root = C.variant(dp, edit, label=label, gens=gens)
    d = root / 'data/rlk/function/boss/scarlet'
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(Path(dp).resolve() / 'data/rlk/function/boss/scarlet', d)
    return root


def enable_scarlet(reg):
    next(b for b in reg['boss'] if b['id'] == 'scarlet')['enabled'] = True


def dry_build(root, kit=False, theme=False, patch=''):
    """Regenerate F:boss/scarlet in a variant (never the tested tree) with api.K and / or the arena theme forced on and
    any other api attribute patched (patch: Python lines run after `import mboss_scarlet.api as api`, e.g.
    "api.ULT5_LETHAL = False"): a dry build. The calls to the missing kit / look functions appear; ScSim stubs
    F:boss/scarlet/fx/** (logged in s.kitl), the look jobs are the test's stubs."""
    import subprocess
    code = ('import sys; sys.path.insert(0, "tools"); sys.dont_write_bytecode = True; import mboss_scarlet.api as api\n'
            + ('api.K._on = lambda: True\n' if kit else '')
            + ('api.theme_ready = lambda: True\napi.deco = lambda: api.DECO_DEFAULT\n' if theme else '')
            + (patch + '\n' if patch else '')
            + 'P = "tools/build_mboss_scarlet.py"\n'
            + 'exec(compile(open(P, encoding="utf-8").read(), P, "exec"), {"__file__": P, "__name__": "__main__"})\n')
    r = subprocess.run([sys.executable, '-c', code], cwd=root, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'dry build failed: {r.stdout[-800:]}{r.stderr[-2000:]}')
    return r.stdout


def setup_sc(dp, seed=1018, lv=4, hp=100000, player_level=5, cls=None):
    """setup() with the ScSim world (cls: a subclass of ScSim, I1: test_reward's real-SR section)."""
    s, zone, pl = A.setup(force=0, lv=lv, hp=hp, seed=seed, player_level=player_level, player_pos=(0.5, 201.0, 0.5), dp=dp,
                          cls=cls or ScSim)
    C.install(s, lv=lv, hp=hp)
    s.call('rlk:mboss/init', C0)
    s.call('rlk:room/rift/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 2)
    s.setsc('#mapType', 'room', 1)
    # the engine stubs a fight relies on
    s.cache['rlk:char/ronova/revive'] = ['scoreboard players set @s rnRev 1']
    # the arena's look jobs while S1K's theme is missing (a theme-on dry build calls them): a no-op unless a test stubs them
    base_load = s.load

    def load_sc(fid):
        if fid not in s.cache and fid.startswith('rlk:mboss/arena/hr_field/look/'):
            if not (s.root / (fid.split(':', 1)[1] + '.mcfunction')).exists():
                s.cache[fid] = ['scoreboard players add #LOOKN azs 1']
        return base_load(fid)
    s.load = load_sc
    return s, pl


def kit_on(s, vanilla_sched=True):
    """I1b verification round 1: the kit runs for real in s (ScSim.kit_real), with the one engine function it calls,
    view/ttl_blank (the subtitle typer's blank title), real too instead of the engine stubs' empty body: every module kit
    call then costs what it costs in the kit's own harness (hr/s1k/lib/hrfxsim.FxSim). vanilla_sched: scheduled functions
    in vanilla's order (ScSim.sched_vanilla), so the card ager's pass over the cards a tick made counts in that tick, as on
    the server (a `schedule ... 1t` made by a tick function runs before the server tick ends). Returns s."""
    s.kit_real = True
    s.sched_vanilla = vanilla_sched
    s.cache.pop('rlk:view/ttl_blank', None)
    return s


def kit_ex(s, sub):
    """The logged kit calls fx/<sub> as dicts t, a (macro args), tags (the executor's), caller (the calling function), ph (#ph
    hr at the call) — I1b round 1: e.g. which decor prop a prop/moon_halo call re-looked, from where, in which phase."""
    return [dict(t=t, a=a, tags=x, caller=f, ph=ph) for (t, c, a), (x, f, ph) in zip(s.kitl, s.kitx) if c == sub]


def run_sc(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        world_sc(s)


def until_sc(s, cond, limit=1500, each=None):
    for _ in range(limit):
        if cond(s):
            return True
        if each:
            each(s)
        world_sc(s)
    return cond(s)


def hr(s, k):
    return s.sc(k, 'hr')


def bctx(s):
    b = body_of(s)
    return Ctx(b, tuple(b.pos), tuple(b.rot))


def call_sc(s, rel, macro=None):
    return s.call(ROOT_SC + rel, bctx(s), macro)


def test_id(s, n):
    """/function rlk:boss/test/pattern {id:n} as the player (the framework's test entry -> the module's test hook)."""
    pl = s.player()
    return s.call('rlk:boss/test/pattern', Ctx(pl, tuple(pl.pos), tuple(pl.rot)), {'id': n})


def place_player(s, x, z, y=201.0):
    pl = s.player()
    pl.pos = [float(x), float(y), float(z)]
    C.moved(s)
    return pl


def heal(s):
    pl = s.player()
    s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))
    s.setsc(('e', pl.id), 'dead', 0)


def fight_sc(s, sid='scarlet', intro=False, limit=900):
    """Her rift entered (the REAL sp/gate), then until the intro state (#mbSt 0 with her body); intro=False ends the
    intro at once (core/intro/done, as the framework cap / a reload / a test does). Returns ok."""
    z, a = rift_zone(s, sid)
    s.player().pos = list(a.pos)
    r = enter(s, a)
    ok = bool(r) and until_sc(s, lambda s: body_of(s) is not None and (mb(s, '#mbSt') or 0) == 0
                              and (hr(s, '#ph') or 0) == 0 and (s.sc('#sq', 'hr') or 0) >= 1, limit)
    if ok and not intro:
        call_sc(s, 'core/intro/done')
    s.zone_sc = z
    return ok


# ------------------------------------------------------------------------------------------------- pattern runs (S3)
CX, CY_, CZ = 880.0, 201.0, 8.0          # hr_field C (api.CX / CY / CZ)


def ents_tagged(s, prefix='rlk_hr_'):
    """Alive entities with a tag starting with prefix (rlk_hr_*), as (etype, sorted tags)."""
    return [(e.etype, sorted(e.tags)) for e in s.ents if e.alive and any(t.startswith(prefix) for t in e.tags)]


def place_body(s, x, z, yaw=None, y=201.0):
    b = body_of(s)
    b.pos = [float(x), float(y), float(z)]
    if yaw is None:
        pl = s.player()
        yaw = math.degrees(math.atan2(-(pl.pos[0] - b.pos[0]), pl.pos[2] - b.pos[2])) % 360
    b.rot = [float(yaw), 0.0]
    for t in ('rlk_mb_mv',):
        b.tags.discard(t)
    C.moved(s)
    return b


def hold(s, on=True):
    """The test hold (#lock hr): no AI decision while set (a running pattern still finishes)."""
    s.setsc('#lock', 'hr', 1 if on else 0)


def start_pattern(s, key_tid):
    """The test id as the player (/function rlk:boss/test/pattern {id:N}), then the hold: only that pattern runs."""
    r = test_id(s, key_tid)
    hold(s, True)
    return r


def snap(s):
    """(t, body pos, body yaw, #pt, #pat, lock marker pos) of the current tick."""
    b = body_of(s)
    lk = [e for e in s.ents if e.alive and 'rlk_hr_lock' in e.tags]
    return dict(t=s.t, pos=tuple(b.pos) if b else None, yaw=(b.rot[0] % 360) if b else None, pt=hr(s, '#pt'),
                pat=hr(s, '#pat'), lock=tuple(lk[0].pos) if lk else None, mv='rlk_mb_mv' in b.tags if b else False)


# ------------------------------------------------------------------------------------------------- H1 (hr rebuild, 11-11)
# The world of the rebuilt fight's suites (pat_p1 / pat_p2 / pat_ghost / test_gauge / test_bal_hr / test_scarlet) and of
# hrfair 2.0: ScSim + the player's inputs as the game takes them, the judge's result per hit (player/def/end), the
# #hzNoParry option of every hazard made, and lane B's balance clock on her body (mob/tick's balance line; mob/setup runs
# the REAL bal/init).
#   F: the REAL player/f_key at the head of the tick (rlk:tick's input pre-pass, #now cb = this tick): player/def/press
#      (the lock #parGap; round W: the whiff ladder is gone) / player/def/press_re (a refused press: no F for #parRe t,
#      #parMl), and in the judge player/def/par_use (#parChain, any tier). A press is
#      accepted when it stamped parAt = now.
#   dodge: the REAL cooldown score dashCool: refused while >= 1 (player/dash), set to #dashCoolT when accepted, the judge's
#      player/def/dg_refund gives #dashCoolT - #dashCoolHitT back on a dodge that avoided a hit, player/tick's - 1 per tick.
#      Round W (the dash is gone, the reference game's dodge set): a press inside the cooldown 1..#dgChW t after the set's
#      first dodge is the double dodge's second move (player/dodge/again): a new stamp, dashCool + #dashCoolT, one per set.
#      The dodge itself is stamped by world_sc (dgAt; the move and the start-spot box are not modelled: the player stands).
# HB (11-11, review H-A): until then the F lock was a Python model with its own numbers (whiff window 40 not 80, the long
# lock a press late and capped at 36 not 48, a refused press pushing the lock a full #parGap, any parry clearing the
# streak); tests/test_input_hr.py checks this world against the rules of README 3 「패링 · 닷지」 on press sequences.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 6000))   # the dash probes recurse once per 0.5 b (hcut: 32 steps)


class H1Sim(ScSim):
    def __init__(self, root):
        super().__init__(root)
        self.judged = []             # dict(t, dodged, parT, pdg, pat, pt, ph, np) of every judged hit on the player
        self.f_at = set()            # world ticks with an F press asked
        self.f_log = []              # (tick, accepted)
        self.d_at = set()            # world ticks with a dodge asked
        self.d_log = []
        self.d_set = None            # round W: the world tick of this dodge set's first dodge (None after its second move)

    def call(self, fid, ctx, macro=None):
        if fid == 'rlk:mboss/hz/make':
            np_ = self.sc('#hzNoParry', 'mb')
            n0 = len(self.hzr)
            r = super().call(fid, ctx, macro)
            for h in self.hzr[n0:]:
                h['np'] = np_
            return r
        if fid == 'rlk:player/def/end':
            self.judged.append(dict(t=self.t, dodged=self.sc('#dodged', 'tmp') or 0, parT=self.sc('#parT', 'tmp') or 0,
                                    pdg=self.sc('#pdg', 'tmp') or 0, pat=self.sc('#pat', 'hr') or 0, pt=self.sc('#pt', 'hr') or 0,
                                    ph=self.sc('#ph', 'hr') or 0, np=self.sc('#hcNP', 'tmp') or 0))
        return super().call(fid, ctx, macro)

    def press(self, at=None):
        """An F press on world tick `at` (default: the next one), taken by the REAL player/f_key in that tick."""
        self.f_at.add(self.t + 1 if at is None else at)

    def dodge(self, at=None):
        """A dodge on world tick `at` (default: the next one), refused while the REAL dashCool runs."""
        self.d_at.add(self.t + 1 if at is None else at)


def world_h1(s):
    """One game tick of the H1 world: the inputs of this tick (F through the REAL player/f_key, the dodge against the REAL
    dashCool), her balance clock, world_sc, then player/tick's dashCool - 1."""
    t = s.t + 1
    pl = s.player()
    pid = ('e', pl.id) if pl is not None else None
    if pl is not None:
        pc = Ctx(pl, tuple(pl.pos), tuple(pl.rot))
        if t in s.f_at:
            s.f_at.discard(t)
            s.setsc('#now', 'cb', t)
            s.call('rlk:player/f_key', pc)
            s.f_log.append((t, s.sc(pid, 'parAt') == t))
        if t in s.d_at:
            s.d_at.discard(t)
            if (s.sc(pid, 'dashCool') or 0) >= 1:
                if s.d_set is not None and 1 <= t - s.d_set <= s.sc('#dgChW', 'tmp'):
                    s.dash(at=t)                                  # the double dodge's second move
                    s.setsc(pid, 'dashCool', s.sc(pid, 'dashCool') + s.sc('#dashCoolT', 'tmp'))
                    s.d_set = None
                    s.d_log.append((t, True))
                else:
                    s.d_log.append((t, False))
            else:
                s.dash(at=t)
                s.setsc(pid, 'dashCool', s.sc('#dashCoolT', 'tmp'))
                s.d_set = t
                s.d_log.append((t, True))
    b = body_of(s)
    if b is not None and b.alive and (s.sc(('e', b.id), 'balT') or 0) >= 1 and 'rlk_mb_dying' not in b.tags:
        s.call('rlk:bal/tick', Ctx(b, tuple(b.pos), tuple(b.rot)))
    world_sc(s)
    if pid is not None and (s.sc(pid, 'dashCool') or 0) >= 1:
        s.setsc(pid, 'dashCool', s.sc(pid, 'dashCool') - 1)


def setup_h1(dp, seed=11, lv=15, hp=5834, player_level=15):
    """The H1 world: the item-less Lv15 player against her at L16 (lv + her lvAdd 1; hp 260 x LV_HP(16) / 100 = 5834), the balance gauge
    real (mob/setup -> bal/init, bal/load)."""
    s, pl = setup_sc(dp, seed=seed, lv=lv, hp=hp, player_level=player_level, cls=H1Sim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    return s, pl


def run_h1(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        world_h1(s)


def until_h1(s, cond, limit=1500, each=None):
    for _ in range(limit):
        if cond(s):
            return True
        if each:
            each(s)
        world_h1(s)
    return cond(s)


def bal(s, k='bal'):
    b = body_of(s)
    return s.sc(('e', b.id), k) if b is not None else None


def facing_setup(s, dist, side=0.0):
    """Her at the arena centre facing south, the player `dist` b in front of her (and `side` b to her left)."""
    place_player(s, CX + 0.5 + side, CZ + 0.5 + dist)
    place_body(s, CX + 0.5, CZ + 0.5)
