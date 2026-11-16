#!/usr/bin/env python3
"""azsim.py: the S1-HARN engine wrapper (plan.md section 8.1 / 8.4; scratch tool, never shipped).

An mcsim world (lib/mcsim.py, lib/fgsim.py: vendored, unchanged copies of S:mb3/tests) on a datapack COPY (default the
M0 archive in ./m0, env AZDP overrides), in which these engine functions run FOR REAL from the datapack (REAL below):

    combat/apply (+ the AZ-CM proxy and RES lines once they exist), combat/apply_mods, combat/res(_low|_high|_neg),
    combat/lv_mult, combat/gold_drop (+ the kill path: heal_orb_roll, kill_xp, sap_loop, gold_spawn),
    combat/clear_atkflags, combat/melee_begin, element/on_hit (+ react, icd, src_*), element/tick for mobs and the
    player (mob/tick:33, player/elem_tick), element/rx_run + element/run/* + element/aoe_hit, element/dot,
    element/lunar/hit, cm/hit_pl2, player/take_damage, player/hurt_elem, engravings/guard/absorb,
    element/shield_absorb(_el), element/shield_gain, room/pick/boss, room/boss_spawn, room/zone_build,
    room/zone_enter, room/combat_clear, room/obj/click, run/next_chapter, player/knockback/check (the N12 push step)

Everything else outside F:mboss is stubbed as fgsim.py does (fgsim.STUBS minus the real list, plus the leaf stubs in
LEAF: sounds, damage numbers, particles-only helpers, map generation, Raiden). The mid-boss framework and modules
(F:mboss/**) always run for real; module rigs are logged (face/player and face/track turn the anchor), the kits run.

Two harness rules that are not engine behaviour:
- random value: a call made directly by a function outside F:mboss (damage-number jitter, heal orb / gold / sapphire
  rolls) draws from a separate engine RNG, so the boss AI's random stream is the same whatever the player does;
- the world tick order is rlk:tick's: low gravity (tick:21-22) -> player elem_tick (player/tick:77) -> mob element
  ticks (mob/tick:33) -> mboss/main (tick:58) -> the room tick (spawn countdown, clear) -> boxes -> schedules.

Usage: python3 azsim.py selftest [dp]    (runs every real function once and checks it; exit 1 on a failure)
"""
import json
import math
import os
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import fgsim as G  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ent, Ctx  # noqa: E402
from mcsim import split as Z_split  # noqa: E402


def _patched_execute():
    """mcsim's execute with one gap filled: `if|unless data entity <sel> data{...}` / `data.<path>` test the entity's
    data compound (mcsim answers every entity data test with true; the room code branches on data{boss_id:...})."""
    import inspect
    import textwrap
    src = textwrap.dedent(inspect.getsource(mcsim.Sim.execute))
    old = "                    else:\n                        ok = True\n                except (KeyError, IndexError, TypeError):"
    new = ("                    else:\n                        ok = self.data_entity_test(t[i + 2], t[i + 3], t[i + 4], ctx)\n"
           "                except (KeyError, IndexError, TypeError):")
    assert src.count(old) == 1, 'mcsim execute layout changed'
    ns = {}
    exec(compile(src.replace(old, new), mcsim.__file__, 'exec'), vars(mcsim), ns)  # noqa: S102
    return ns['execute']

M0 = HERE / 'm0' / 'roguelike'
C0 = G.C0

# ----------------------------------------------------------------------------------------------- real / stubbed
REAL = (
    'rlk:combat/apply', 'rlk:combat/apply_mods', 'rlk:combat/res', 'rlk:combat/res_low', 'rlk:combat/res_high',
    'rlk:combat/res_neg', 'rlk:combat/lv_mult', 'rlk:combat/gold_drop', 'rlk:combat/heal_orb_roll', 'rlk:combat/kill_xp',
    'rlk:combat/sap_loop', 'rlk:combat/gold_spawn', 'rlk:combat/clear_atkflags', 'rlk:combat/melee_begin',
    'rlk:element/on_hit', 'rlk:element/icd', 'rlk:element/icd_reset', 'rlk:element/tick', 'rlk:element/rx_run',
    'rlk:element/aoe_hit', 'rlk:element/dot', 'rlk:element/lunar/hit', 'rlk:element/shield_absorb',
    'rlk:element/shield_absorb_el', 'rlk:element/shield_gain', 'rlk:cm/hit_pl2', 'rlk:player/take_damage',
    'rlk:player/hurt_elem', 'rlk:player/elem_tick', 'rlk:engravings/guard/absorb', 'rlk:room/pick/boss',
    'rlk:room/boss_spawn', 'rlk:room/zone_build', 'rlk:room/zone_enter', 'rlk:room/combat_clear', 'rlk:room/obj/click',
    'rlk:run/next_chapter', 'rlk:player/knockback/check',
)
REAL_PREFIX = ('rlk:element/run/',)

# leaf stubs (engine functions the real list calls that only draw, sound, generate maps or belong to Raiden)
LEAF = {
    'rlk:items/proc/taken': [], 'rlk:items/proc/lion_queue': [], 'rlk:engravings/berserk/taken': [],
    'rlk:player/knockback/start': [], 'rlk:cm/hurt_fx': [], 'rlk:cm/flash': [], 'rlk:element/set_icon': [],
    'rlk:element/infuse_end': [], 'rlk:element/rx_text2': [], 'rlk:element/rx_text3': [],
    'rlk:combat/confirmed_hit_sound': [], 'rlk:combat/text_lunar': [],
    'rlk:combat/heal_orb_spawn': ['scoreboard players add #HEALORB azs 1'],
    'rlk:player/level/add_xp': ['scoreboard players operation #XP azs += #xpAdd tmp'],
    'rlk:combat/sap_spawn': ['scoreboard players add #SAP azs 1'],
    'rlk:room/msg': [], 'rlk:room/door_draw': [], 'rlk:room/door_step': [], 'rlk:room/seal_out': [],
    'rlk:room/seal_check': [], 'rlk:room/cells_kill': [], 'rlk:room/wave_start': [], 'rlk:room/zone_doors': [],
    'rlk:room/gen': ['scoreboard players add #ROOMGEN azs 1'],
    'rlk:room/end_setup': [],
    'rlk:room/raiden/layout': ['scoreboard players add #RDLAYOUT azs 1'],
    'rlk:room/raiden/build': ['scoreboard players add #RDBUILD azs 1'],
    'rlk:boss/raiden/spawn': ['scoreboard players add #RDSPAWN azs 1',
                              'summon minecraft:marker ~ ~ ~ {Tags:["rlk_zmob","rlk_room","rlk_azs_raiden"]}'],
    'rlk:boss/raiden/test/won': [],
    'rlk:room/zb_fn': ['scoreboard players add #ZBFN azs 1'],
    # objects: a marker with the object's oact / oarg (the real ones build text and item displays)
    'rlk:room/obj/make_item': ['summon minecraft:marker ~ ~ ~ {Tags:["rlk_obj","rlk_room","rlk_azs_new"]}',
                               'scoreboard players operation @e[tag=rlk_azs_new] oact = #oact tmp',
                               'scoreboard players operation @e[tag=rlk_azs_new] oarg = #oarg tmp',
                               'tag @e[tag=rlk_azs_new] remove rlk_azs_new'],
    # the mid-boss gate: fgsim's roll + the gate object (oact 14) that room/obj/click presses
    'rlk:room/obj/k_mboss': ['scoreboard players add #REGATE mb 1', 'function rlk:mboss/roll',
                             'summon minecraft:marker ~ ~ ~ {Tags:["rlk_obj","rlk_room","rlk_azs_gate"]}',
                             'scoreboard players set @e[tag=rlk_azs_gate] oact 14',
                             'tag @e[tag=rlk_azs_gate] remove rlk_azs_gate'],
    'rlk:items/hook/on_kill': [], 'rlk:engravings/on_kill': [], 'rlk:items/hook/on_lunar': [],
}
LEAF_PREFIX = ('rlk:snd/', 'rlk:combat/text_crit', 'rlk:combat/text_normal', 'rlk:element/rx_text',
               'rlk:element/display', 'rlk:element/color')

# mob level and boss HP (fgsim stubs room/mob_init: the harness sets the level, the HP comes from the registry)
LV_HP = lambda lv: (100 + 30 * (lv - 1) + 5 * (lv - 1) ** 2 // 100) * 400 // 100   # noqa: E731  mob/level_apply %


def dp_root():
    return Path(os.environ.get('AZDP') or M0)


def registry(dp=None):
    return json.loads((Path(dp or dp_root()) / 'tools/mboss_registry.json').read_text(encoding='utf-8'))


def boss_entry(dp, key):
    reg = registry(dp)
    for b in reg.get('boss', []) + reg.get('cboss', []):
        if b.get('id') == key or b.get('n') == key:
            return b
    return None


def arena_of(dp, b):
    """L.arena_of(b) of plan.md 1.2 R1: arenas[b.arena] when the registry has it, else the plaza arena."""
    reg = registry(dp)
    aid = (b or {}).get('arena', 'plaza')
    if aid != 'plaza' and aid in reg.get('arenas', {}):
        return reg['arenas'][aid]
    return reg['arena']


def has_fn(dp, fid):
    return (Path(dp) / 'data/rlk/function' / (fid.split(':', 1)[1] + '.mcfunction')).exists()


def features(dp=None):
    """Which of the post-M0 parts exist in this datapack (the harness switches them on automatically)."""
    dp = Path(dp or dp_root())
    return dict(
        chapter=has_fn(dp, 'rlk:mboss/cb/route'),                      # AZ-CM chapter mode (S1-CM)
        cproto=(dp / 'data/rlk/function/mboss/cproto').is_dir(),
        px=has_fn(dp, 'rlk:mboss/px/spawn'),                           # framework hit proxies (R8)
        pl_dot=has_fn(dp, 'rlk:mboss/pl_dot'),                         # N7
        mask=(dp / 'data/rlk/function/mboss/hz').is_dir() and any(
            'mask' in p.name for p in (dp / 'data/rlk/function/mboss/hz').iterdir()),   # N4
        push=(dp / 'data/rlk/function/mboss/push').is_dir(),           # N12 / N18
        azhdaha=(dp / 'data/rlk/function/boss/azhdaha/main.mcfunction').exists()
        or (dp / 'data/rlk/function/boss/azhdaha/tick.mcfunction').exists(),
    )


def load_constants(dp):
    """The plain `scoreboard players set #X <obj> N` lines of F:load (engine constants: defence, levels, gold, shields,
    reactions...), so the real functions see the game's numbers."""
    out = []
    for line in (Path(dp) / 'data/rlk/function/load.mcfunction').read_text(encoding='utf-8').split('\n'):
        m = re.match(r'^scoreboard players set (#\S+) (\S+) (-?\d+)\s*$', line)
        if m:
            out.append((m.group(1), m.group(2), int(m.group(3))))
    return out


UUID_RE = re.compile(r'^[0-9a-fA-F]{1,8}-[0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,12}$')


def uuid_norm(u):
    """Canonical hyphenated form of a UUID string (vanilla accepts groups without leading zeros)."""
    g = [int(x, 16) for x in u.split('-')]
    return f'{g[0]:08x}-{g[1]:04x}-{g[2]:04x}-{g[3]:04x}-{g[4]:012x}'


def uuid_of_ints(a):
    v = 0
    for x in a:
        v = (v << 32) | (int(x) & 0xffffffff)
    h = f'{v:032x}'
    return f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}'


# ----------------------------------------------------------------------------------------------- the world
class AzSim(G.FSim):
    RIGS = ('rlk:mboss/guardian/rig/', 'rlk:mboss/butterfly/rig/', 'rlk:mboss/fieldgen/rig/', 'rlk:boss/azhdaha/rig/',
            'rlk:mboss/cproto/rig/', 'rlk:mboss/fieldgen/rig_stub/')
    KITS = ('rlk:mboss/fieldgen/fx/', 'rlk:boss/azhdaha/fx/')
    RIG_REAL = ()                  # rig sub-paths that run for real (none: the framework owns the proxy runtime)

    def __init__(self, root):
        super().__init__(root)
        self.stack = []
        self.erng = random.Random(0)
        self.agent = None          # azfair.Agent (optional)
        self.iframe_end = -1       # last tick of the agent's dash i-frames (dashInvT is set around each hit)
        self.dmg = []              # [t, pct, el, hp_lost, pat, phase, nododge, src, shield_absorbed]
        self.dodges = []           # [t, pct, pat, phase, nododge]
        self.kb = None
        self.hzrec = {}            # hazard marker id -> its scores at hz/init (+ the player position then)
        self.calls_n = {}          # counts of selected engine calls (selftest, reports)
        self.unset_src = {}        # (holder, objective) -> count of unset operation sources read as 0
        self.pat_fn = lambda: 0    # noqa: E731  set by azfair (module pattern score)
        self.ph_fn = lambda: '-'   # noqa: E731  set by azfair (module phase key)

    # -- RNG routing: a `random value` run directly by an engine function (outside F:mboss) uses the engine RNG
    def cmd(self, t, ctx):
        if t[0] == 'scoreboard' and len(t) > 7 and t[1] == 'players' and t[2] == 'operation':
            # vanilla getOrCreatePlayerScore: an unset source score reads (and is created) as 0 (mcsim raises)
            for h in self.holders(t[6], ctx):
                if self.sc(h, t[7]) is None:
                    self.setsc(h, t[7], 0)
                    k = (t[6] if not t[6].startswith('@') else t[6].split('[')[0], t[7])
                    self.unset_src[k] = self.unset_src.get(k, 0) + 1
        if t[0] == 'random' and len(t) > 2 and t[1] == 'value':
            fid = self.stack[-1] if self.stack else ''
            a, b = t[2].split('..')
            rng = random if fid.startswith('rlk:mboss/') or not fid else self.erng
            return rng.randint(int(a), int(b))
        if t[0] == 'summon' and len(t) > 5:
            mu = re.search(r'UUID:\[I;\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\]', t[5])
            uid = uuid_of_ints(mu.groups()) if mu else None
            if uid and any(e.alive and getattr(e, 'uuid', None) == uid for e in self.ents):
                return 0                # vanilla: an entity with that UUID exists -> the summon fails
            v = super().cmd(t, ctx)
            e = self.ents[-1]
            if uid:
                e.uuid = uid
            if 'interaction' in t[1]:
                for k in ('width', 'height'):
                    m = re.search(k + r':(-?[\d.]+)f?', t[5])
                    if m:
                        e.data[k] = float(m.group(1))
            return v
        if t[0] == 'data' and len(t) > 4 and t[1] == 'merge' and t[2] == 'entity' and t[4].startswith('{'):
            ents = self.select(t[3], ctx) if t[3] != '@s' else ([ctx.ex] if ctx.ex else [])
            for e in ents:
                for k in ('width', 'height'):
                    m = re.search(r'(?<![A-Za-z_])' + k + r':(-?[\d.]+)f?', t[4])
                    if m:
                        e.data[k] = float(m.group(1))
            if t[3] != '@s' and not ents:
                return 0
            return 1
        if (t[0] == 'data' and len(t) > 7 and t[1] == 'modify' and t[2] == 'entity' and t[4] in ('width', 'height')
                and t[5] == 'set' and t[6] == 'value'):
            ents = self.select(t[3], ctx) if t[3] != '@s' else ([ctx.ex] if ctx.ex else [])
            for e in ents:
                e.data[t[4]] = float(t[7].rstrip('fd'))
            return 1 if ents else 0
        return super().cmd(t, ctx)

    execute = _patched_execute()

    # -- UUID selectors and score holders (mcsim knows only @-selectors)
    def select(self, sel, ctx):
        if not sel.startswith('@'):
            if UUID_RE.match(sel):
                u = uuid_norm(sel)
                return [e for e in self.ents if e.alive and getattr(e, 'uuid', None) == u]
            return []
        return super().select(sel, ctx)

    def holder(self, t, ctx):
        if UUID_RE.match(t):
            es = self.select(t, ctx)
            return ('e', es[0].id) if es else uuid_norm(t)
        return super().holder(t, ctx)

    def holders(self, t, ctx):
        if UUID_RE.match(t):
            h = self.holder(t, ctx)
            return [h] if h else []
        return super().holders(t, ctx)

    def data_entity_test(self, kind, sel, path, ctx):
        if kind != 'entity':
            return True
        ents = self.select(sel, ctx) if sel != '@s' else ([ctx.ex] if ctx.ex else [])
        if not ents:
            return False
        e = ents[0]
        if path.startswith('data{'):
            return self.match(e.data, self.snbt(path[4:]))
        if path.startswith('data.'):
            try:
                self.path_get(e.data, path[5:])
                return True
            except (KeyError, IndexError, TypeError):
                return False
        if path == 'data':
            return bool(e.data)
        return True                # other entity NBT (OnGround, ...): as mcsim, true

    def store(self, spec, v, ctx):
        if spec[1] == 'entity' and spec[3] in ('width', 'height'):
            e = (self.select(spec[2], ctx) if spec[2] != '@s' else [ctx.ex])[0]
            e.data[spec[3]] = (v or 0) * float(spec[5])
            return
        return super().store(spec, v, ctx)

    def count(self, k):
        self.calls_n[k] = self.calls_n.get(k, 0) + 1

    def call(self, fid, ctx, macro=None):
        for p in self.RIGS:
            if fid.startswith(p):
                sub = fid[len(p):]
                if not sub.startswith(self.RIG_REAL) or not self.RIG_REAL:
                    return self.rig_call(p, sub, ctx)
        if fid.startswith(self.KITS):
            for k in self.KITS:
                if fid.startswith(k):
                    sub = fid[len(k):]
                    if not sub.startswith(G.KIT_INTERNAL):
                        self.kit.append((self.t, k.split('/')[2] + '/' + sub))
                    break
        if fid in ('rlk:combat/apply', 'rlk:element/rx_run', 'rlk:element/dot', 'rlk:element/lunar/hit',
                   'rlk:player/hurt_elem', 'rlk:combat/gold_drop', 'rlk:room/combat_clear', 'rlk:room/boss_spawn',
                   'rlk:room/pick/boss', 'rlk:run/next_chapter', 'rlk:element/shield_absorb', 'rlk:mboss/pl_dot'):
            self.count(fid)
        if fid == 'rlk:cm/hit_pl2':
            return self.hit_pl2(fid, ctx, macro)
        if fid == 'rlk:mboss/pl_dot':
            return self.pl_dot(fid, ctx, macro)
        if fid == 'rlk:mboss/pj/launch':
            self.pjs.append((self.t, dict(macro or {}), self.sc('#pjShape', 'mb'), self.sc('#pjGrp', 'mb')))
        if fid == 'rlk:mboss/line/say' and macro:
            self.says.append((self.t, macro.get('t')))
        if fid == 'rlk:mboss/hz/make':
            g = lambda k: self.sc(k, 'mb')  # noqa: E731
            self.hz.append(dict(t=self.t, tell=g('#hzW'), dmg=g('#hzD'), kind=g('#hzK'), r=g('#hzR'), r0=g('#hzR0'),
                                nd=g('#hzNoDodge'), rearm=g('#hzRearm'), grp=g('#hzGrp'), y1=g('#hzY1'),
                                act=g('#hzAct'), pos=tuple(ctx.pos), yaw=ctx.rot[0]))
        self.stack.append(fid)
        try:
            r = super(G.FSim, self).call(fid, ctx, macro)      # mcsim's call (fgsim's own logging is done above)
        finally:
            self.stack.pop()
        if fid == 'rlk:mboss/hz/init' and ctx.ex is not None:
            self.hz_record(ctx.ex)
        return r

    def rig_call(self, prefix, sub, ctx):
        """A module rig call (rig output is out of scope): logged; face/player and face/track turn the anchor as the
        rig APIs say (instant / at most 4 degrees per call); the Guardian's spear props become pj threat entities."""
        self.rig.append((self.t, prefix.split('/')[2] + '/' + sub))
        if sub == 'prop/spear' and 'guardian' in prefix:
            for e in self.ents:
                e.tags.discard('rlk_mb_gd_prop_new')
            self.ents.append(Ent('item_display', ctx.pos, (ctx.rot[0], 0.0),
                                 ['rlk_room', 'rlk_mb_aux', 'rlk_mb_gd_prop', 'rlk_mb_gd_prop_new']))
        if sub == 'face/player' and ctx.ex is not None:
            return self.call('rlk:fgtest/face_player', ctx)
        if sub == 'face/track' and ctx.ex is not None:
            return self.call('rlk:mboss/mv/turn', ctx, {'max': 4})
        return 1

    def hz_record(self, e):
        g = lambda o: self.sc(('e', e.id), o)  # noqa: E731
        pl = self.agent.player if self.agent else None
        self.hzrec[e.id] = dict(t=self.t, pat=self.pat_fn(), ph=self.ph_fn(), K=g('mbHzK'), W=g('mbHzW'),
                                D=g('mbHzD'), A=g('mbHzA'), Y1=g('mbHzY1'), R=g('mbHzR'), ND=g('mbHzND'),
                                RA=g('mbHzRA'), G=g('mbHzG'), I=g('mbHzI'), pos=tuple(e.pos),
                                ppos=tuple(pl.pos) if pl else None, tags=sorted(e.tags))

    # -- the player hit path (real cm/hit_pl2 -> player/take_damage), with the agent's i-frames and the records
    def player(self):
        if self.agent is not None:
            return self.agent.player
        p = self.select('@a[tag=player,limit=1]', C0)
        return p[0] if p else None

    def hit_pl2(self, fid, ctx, macro):
        pl = self.agent.player if self.agent else None
        nd = (self.sc('#mbNoDodge', 'mb') or 0) == 1
        if pl is not None:
            # the dash i-frames (dashInvT) except for a #hzNoDodge hit (mboss/hurt_nd zeroes them around the call)
            self.setsc(('e', pl.id), 'dashInvT', 1 if (self.t <= self.iframe_end and not nd) else 0)
            self.setsc('#hurtDmg', 'tmp', 0)
            sh0 = (self.sc(('e', pl.id), 'shieldHP') or 0) + (self.sc(('e', pl.id), 'gShield') or 0)
        pct, el = self.sc('#mbHitPct', 'mb'), self.sc('#cmEl', 'tmp')
        self.stack.append(fid)
        try:
            r = super(G.FSim, self).call(fid, ctx, macro)
        finally:
            self.stack.pop()
        if pl is not None:
            if (self.sc('#dodged', 'tmp') or 0) == 1:
                self.dodges.append([self.t, pct, self.pat_fn(), self.ph_fn(), 1 if nd else 0])
            else:
                lost = self.sc('#hurtDmg', 'tmp') or 0
                sh1 = (self.sc(('e', pl.id), 'shieldHP') or 0) + (self.sc(('e', pl.id), 'gShield') or 0)
                self.dmg.append([self.t, pct, el, lost, self.pat_fn(), self.ph_fn(), 1 if nd else 0, 'hit', sh0 - sh1])
                src = self.select('@e[tag=rlk_plkb_source,limit=1]', C0)
                k = self.sc('#cmKB', 'tmp') or 0
                if src and k > 0:
                    yaw = math.radians(src[0].rot[0])
                    self.kb = (-math.sin(yaw), math.cos(yaw), k)
            self.setsc(('e', pl.id), 'dashInvT', 0)
            self.agent.check_death()
        return r

    def pl_dot(self, fid, ctx, macro):
        """N7 mboss/pl_dot (the brand DoT, framework): real; its HP loss is recorded as src 'brand'."""
        pl = self.player()
        hp0 = self.sc(('e', pl.id), 'curHealth') if pl else None
        sh0 = ((self.sc(('e', pl.id), 'shieldHP') or 0) + (self.sc(('e', pl.id), 'gShield') or 0)) if pl else 0
        self.stack.append(fid)
        try:
            r = super(G.FSim, self).call(fid, ctx, macro)
        finally:
            self.stack.pop()
        if pl is not None and hp0 is not None:
            sh1 = (self.sc(('e', pl.id), 'shieldHP') or 0) + (self.sc(('e', pl.id), 'gShield') or 0)
            lost = hp0 - (self.sc(('e', pl.id), 'curHealth') or 0)
            self.dmg.append([self.t, self.sc('#mbDotPct', 'mb') or 0, self.sc('#mbDotEl', 'mb') or 0, lost,
                             self.pat_fn(), self.ph_fn(), 1, 'brand', sh0 - sh1])
            if self.agent:
                self.agent.check_death()
        return r


STUBS = {k: v for k, v in G.STUBS.items() if k not in REAL}
STUBS.update(LEAF)


def install_stubs(s, lv=4, hp=100000):
    for k, v in STUBS.items():
        s.cache[k] = list(v)
    s.cache['rlk:room/mob_init'] = [f'scoreboard players set @s mlv {lv}',
                                    'function rlk:mboss/base_stats with storage rlk:mboss cur',
                                    f'scoreboard players set @s mhpM {hp}', f'scoreboard players set @s mhpC {hp}']
    load = s.load
    arena_ensure = re.compile(r'^rlk:mboss/arena/[^/]+/ensure$')
    arena_other = re.compile(r'^rlk:mboss/arena/[^/]+/(build|rebuild|clear|sweep|done|s/|l/|look/)')

    def load_stubbed(fid):
        if fid not in s.cache and not fid.startswith(REAL_PREFIX) and fid not in REAL and fid.startswith(LEAF_PREFIX):
            s.cache[fid] = []
        if fid not in s.cache and arena_ensure.match(fid):
            s.cache[fid] = ['scoreboard players set #mbArBuild mb 0', 'return 1']
        if fid not in s.cache and arena_other.match(fid):
            s.cache[fid] = []
        return load(fid)
    s.load = load_stubbed


PLAYER_ZERO = ('dead', 'rnDie', 'pkMode', 'vMap', 'devMode', 'pkPending', 'pkMb', 'dashInvT', 'elemMastery', 'bol',
               'scT', 'it_lion_mane', 'it_coin_pouch', 'hurtLv', 'hurtElem', 'elAct', 'burnOn', 'shieldHP', 'shieldT',
               'shieldEl', 'gShield', 'gCd', 'infuseT', 'infuse', 'rxQ', 'frzT', 'quickT', 'icdT', 'icdC', 'rnEr',
               'rnNoE', 'aFire', 'aWater', 'aThunder', 'aIce', 'aGrass', 'aVoid', 'dFire', 'dWater', 'dThunder', 'dIce',
               'dGrass', 'dVoid', 'lnEC', 'ecI')


def setup(force=1, lv=4, hp=100000, seed=1018, player_level=4, player_pos=(40.5, 201.0, 18.0), dp=None, cls=AzSim):
    """A fresh world (fgsim.setup's layout: the player in a mid-boss zone kind 15, first person) with the engine
    constants of F:load, the real list above, and an item-less player of `player_level`
    (HP 100 + 12 (L-1), def 10 + 2 (L-1), atk 10 + 2 (L-1)). `random` is seeded with `seed` (the module's stream) and
    the engine RNG with seed + 7."""
    dp = Path(dp or dp_root())
    G.ROOT[0] = dp / 'data/rlk/function'
    lines = (G.ROOT[0] / 'tick.mcfunction').read_text(encoding='utf-8').split('\n')
    G.TICK_LOWG[:] = [l for l in lines if 'rlk:mboss/lowg_' in l and not l.startswith('#')]
    random.seed(seed)
    s = cls(G.ROOT[0])
    s.erng.seed(seed + 7)
    s.dp = dp
    install_stubs(s, lv=lv, hp=hp)
    s.cache['rlk:fgtest/lowg'] = list(G.TICK_LOWG)
    for k, obj, v in load_constants(dp):
        s.setsc(k, obj, v)
    s.call('rlk:mboss/init', C0)
    for k, v in (('#100', 100), ('#4', 4), ('#2', 2), ('#st10', 10), ('#reactBase', 50)):
        if s.sc(k, 'tmp') is None:
            s.setsc(k, 'tmp', v)
    s.storage.setdefault('rlk:room', {})['ready'] = 1
    s.storage.setdefault('rlk:config', {})['installed'] = 1
    zone = Ent('marker', (40.5, 201.0, 20.5), tags=['rlk_zone'])
    player = Ent('player', player_pos, (180, 0), tags=['player', 'rlk_body'])
    safe = Ent('marker', player_pos, tags=['rlk_safe', 'rlk_room'])
    s.ents += [zone, player, safe]
    for o, v in (('zkind', 15), ('zst', 3), ('zid', 4)):
        s.setsc(('e', zone.id), o, v)
    for o in PLAYER_ZERO:
        s.setsc(('e', player.id), o, 0)
    L = player_level
    hpP = 100 + 12 * (L - 1)
    for o, v in (('curHealth', hpP), ('maxHealth', hpP), ('def', 10 + 2 * (L - 1)), ('level', L),
                 ('critDamage', 150), ('critChance', 30), ('atk', 10 + 2 * (L - 1))):
        s.setsc(('e', player.id), o, v)
    s.setsc('#chapter', 'room', 1)
    s.setsc('#active', 'room', 1)
    s.setsc('#mbForce', 'mb', force)
    s.setsc('berserk', 'engN', 0)
    s.setsc('#lnBuff', 'itv', 0)            # items/hook/tick_player:157 (item-less: 0)
    s.zone, s.pl = zone, player
    return s, zone, player


# ----------------------------------------------------------------------------------------------- the tick
def zones(s, kind=None):
    z = [e for e in s.ents if e.alive and 'rlk_zone' in e.tags]
    return [e for e in z if kind is None or s.sc(('e', e.id), 'zkind') == kind]


def world(s):
    """One game tick of the parts of rlk:tick the fights use (order as in rlk:tick)."""
    s.t += 1
    s.call('rlk:fgtest/lowg', C0)
    pl = s.player()
    if pl is not None:
        # player/tick:77 -> player/elem_tick (shield timer, infusion, the player's element state, Burning on the player)
        s.setsc('#hurtDmg', 'tmp', 0)
        s.setsc(('e', pl.id), 'dashInvT', 1 if s.t <= s.iframe_end else 0)
        hp0 = s.sc(('e', pl.id), 'curHealth') or 0
        s.call('rlk:player/elem_tick', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        s.setsc(('e', pl.id), 'dashInvT', 0)
        lost = hp0 - (s.sc(('e', pl.id), 'curHealth') or 0)
        if lost > 0:
            s.dmg.append([s.t, 0, 'dot', lost, s.pat_fn(), s.ph_fn(), 0, 'dot', 0])
        if s.agent:
            s.agent.check_death()
    # mob/tick:33 for every mob with an element state (decay, ICD, Burning / Electro-Charged DoTs, queued reactions)
    for e in [e for e in s.ents if e.alive and 'rlk_mob' in e.tags and e.etype != 'player']:
        if (s.sc(('e', e.id), 'elAct') or 0) >= 1 and 'rlk_mb_dying' not in e.tags:
            s.call('rlk:element/tick', Ctx(e, tuple(e.pos), tuple(e.rot)))
    if (s.sc('#mbLive', 'mb') or 0) == 1:
        s.call('rlk:mboss/main', C0)
    room_tick(s)
    if (s.sc('#mbBoxOn', 'mb') or 0) == 1:
        s.call('rlk:mboss/box/all', C0)
    s.run_sched()
    s.max_cards = max(s.max_cards, len(s.kit_cards()))


def room_tick(s):
    """The room tick as far as a boss zone needs it: the spawn countdown (room/mob_wave -> boss spawn: kind 15
    mboss/start as fgsim does, kind 9 the REAL room/boss_spawn) and the clear (no rlk_zmob left -> the REAL
    room/combat_clear at the zone)."""
    if (s.sc('#combat', 'room') or 0) < 1:
        return
    zid = s.sc('#combat', 'room')
    z = [e for e in zones(s) if s.sc(('e', e.id), 'zid') == zid] or zones(s, 15) or zones(s, 9)
    if not z:
        return
    z = z[0]
    kind = s.sc(('e', z.id), 'zkind')
    zc = Ctx(z, tuple(z.pos), (0, 0))
    if (s.sc('#spawnT', 'room') or 0) >= 1:
        s.setsc('#spawnT', 'room', s.sc('#spawnT', 'room') - 1)
        if s.sc('#spawnT', 'room') == 0:
            if kind == 9:
                s.call('rlk:room/boss_spawn', zc)
            else:
                s.call('rlk:mboss/start', zc)
    elif not s.select('@e[tag=rlk_zmob,limit=1]', C0):
        s.call('rlk:room/combat_clear', zc)


def run(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        world(s)


# ----------------------------------------------------------------------------------------------- entry paths
def press_gate(s, zone):
    """Mid-boss entry through the REAL room/zone_enter (kind 15 -> k_mboss stub: roll + the gate object, oact 14) and
    the REAL room/obj/click on that object (-> mboss/gate)."""
    s.call('rlk:room/zone_enter', Ctx(zone, tuple(zone.pos), (0, 0)))
    gates = [e for e in s.ents if e.alive and 'rlk_obj' in e.tags and s.sc(('e', e.id), 'oact') == 14]
    if not gates:
        raise RuntimeError('no mid-boss gate object')
    g = gates[-1]
    s.call('rlk:room/obj/click', Ctx(g, tuple(g.pos), (0, 0)))
    return g


def to_fight(s, zone, limit=600):
    press_gate(s, zone)
    for _ in range(limit):
        world(s)
        if (s.sc('#mbSt', 'mb') or 0) == 1:
            return True
    return False


def chapter_entry(s, boss_id, chapter=1, map_idx=5, limit=1200):
    """Chapter-boss entry (AZ-CM, plan.md 1.1): an entrance zone kind 9 with data{boss_id, cboss:1b} -> the REAL
    room/zone_build (-> room/cboss/<id>/build -> mboss/cb/prep) -> the REAL room/zone_enter (-> room/obj/k_cboss,
    oact 16) -> the REAL room/obj/click on the gate (-> mboss/cb/gate -> combat_start) -> the room tick's REAL
    room/boss_spawn (-> mboss/cb/spawn_route -> mboss/cb/start). Needs F:mboss/cb (features()['chapter'])."""
    if not features(s.dp)['chapter']:
        raise RuntimeError('chapter mode (F:mboss/cb) is not in this datapack')
    s.setsc('#chapter', 'room', chapter)
    s.setsc('#mapIdx', 'room', map_idx)
    s.setsc('#mapType', 'room', 8)
    for z in zones(s, 15):
        s.setsc(('e', z.id), 'zkind', 0)
    z = Ent('marker', (40.5, 201.0, 40.5), tags=['rlk_zone'])
    z.data.update({'boss_id': boss_id, 'cboss': 1, 'fn': 'boss'})
    s.ents.append(z)
    for o, v in (('zkind', 9), ('zst', 0), ('zid', 9)):
        s.setsc(('e', z.id), o, v)
    zc = Ctx(z, tuple(z.pos), (0, 0))
    s.call('rlk:room/zone_build', zc)
    s.call('rlk:room/zone_enter', zc)
    gate = None
    for _ in range(limit):
        gs = [e for e in s.ents if e.alive and 'rlk_obj' in e.tags and s.sc(('e', e.id), 'oact') == 16]
        if gs and gate is None:
            gate = gs[-1]
        if gate is not None and (s.sc('#combat', 'room') or 0) < 1 and (s.sc('#mbArBuild', 'mb') or 0) <= 0:
            s.call('rlk:room/obj/click', Ctx(gate, tuple(gate.pos), (0, 0)))
        world(s)
        if (s.sc('#mbSt', 'mb') or 0) == 1:
            return z
    raise RuntimeError('chapter boss did not reach the fight state')


def body_of(s):
    b = s.select('@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]', C0)
    return b[0] if b else None


def strike(s, target, dmg, elem=0, ranged=False, basic=True, crit=0):
    """One player basic attack through the REAL path: combat/melee_begin (as the player), combat/clear_atkflags,
    the basic-attack flags, then combat/apply as the target (the AZ-CM proxy line redirects a proxy to the body).
    Returns (landed, dealt to the boss body, body killed)."""
    pl = s.player()
    pc = Ctx(pl, tuple(pl.pos), tuple(pl.rot))
    if not ranged:
        s.call('rlk:combat/melee_begin', pc)
    s.call('rlk:combat/clear_atkflags', pc)
    for k, v in (('#dmg', dmg), ('#elem', elem), ('#elU', 1000 if elem else 0), ('#icd', 1 if elem else 0),
                 ('#crit', crit), ('#stunHit', 0 if ranged else 1), ('#hitLanded', 0), ('#bowHit', 1 if ranged else 0),
                 ('#lunar', 0), ('#tfm', 0), ('#trueDmg', 0)):
        s.setsc(k, 'tmp', v)
    s.setsc('#basic', 'itv', 1 if basic else 0)
    b = body_of(s)
    hp0 = s.sc(('e', b.id), 'mhpC') if b else None
    s.stack.append('rlk:azsim/strike')
    try:
        s.call('rlk:combat/apply', Ctx(target, tuple(target.pos), tuple(target.rot)))
    finally:
        s.stack.pop()
    s.setsc('#basic', 'itv', 0)
    s.setsc('#bowHit', 'tmp', 0)
    landed = (s.sc('#hitLanded', 'tmp') or 0) == 1
    dealt, killed = 0, False
    if b is not None and hp0 is not None:
        if not b.alive or 'rlk_mb_dying' in b.tags:
            killed = True
            dealt = max(0, s.sc('#dmg', 'tmp') or 0) if landed else 0
        else:
            dealt = hp0 - (s.sc(('e', b.id), 'mhpC') or 0)
    return landed, dealt, killed


# ----------------------------------------------------------------------------------------------- selftest
def selftest(dp=None):
    fails = []

    def ck(name, ok, info=''):
        print(('ok   ' if ok else 'FAIL ') + name, info)
        if not ok:
            fails.append(name)

    dp = Path(dp or dp_root())
    feat = features(dp)
    print('datapack', dp, 'features', feat)
    # 1. constants and the real hit path on the player
    s, zone, pl = setup(force=1, player_level=5, dp=dp)
    ck('constants from F:load', s.sc('#defK', 'tmp') == 100 and s.sc('#shElEff', 'tmp') == 250
       and s.sc('#mobLvDef', 'tmp') == 150, f"defK {s.sc('#defK', 'tmp')} shElEff {s.sc('#shElEff', 'tmp')}")
    ok = to_fight(s, zone)
    ck('mid-boss entry via real zone_enter + obj/click', ok, f"mbSt {s.sc('#mbSt', 'mb')} id {s.sc('#mbId', 'mb')}")
    b = body_of(s)
    # player hit: mboss/hurt -> real cm/hit_pl2 -> take_damage (defence 18, level 4 boss)
    s.setsc('#mbHitPct', 'mb', 100)
    s.setsc('#cmEl', 'tmp', 0)
    s.setsc('#mbKB', 'mb', 0)
    hp0 = s.sc(('e', pl.id), 'curHealth')
    s.call('rlk:mboss/hurt', Ctx(b, tuple(b.pos), (0, 0)))
    lost = hp0 - s.sc(('e', pl.id), 'curHealth')
    atk, mul, lvb = s.sc('#mbAtk', 'mb'), s.sc('#mbDmgMul', 'mb'), s.sc('#mbLv', 'mb')
    raw = max(1, atk * 100 * mul // 10000)
    x = lvb - 1
    raw = raw * (100 + s.sc('#mobLvAtk', 'tmp') * x + s.sc('#mobLvAtk2', 'tmp') * x * x // 100) // 100
    K = 100 + s.sc('#defKLv', 'tmp') * x
    exp = max(1, raw * K // (K + 18))
    ck('player/take_damage real (level scaling + defence)', lost == exp, f'lost {lost} expected {exp} (Lv{lvb})')
    # shields: a 30 HP shield of element 2 absorbs a Hydro hit at 250 %, a physical hit 1:1
    s.setsc(('e', pl.id), 'shieldHP', 0)
    s.setsc('#amt', 'tmp', 30)
    s.setsc('#shEl', 'tmp', 2)
    s.call('rlk:element/shield_gain', Ctx(pl, tuple(pl.pos), (0, 0)))
    ck('element/shield_gain real', s.sc(('e', pl.id), 'shieldHP') == 30 and s.sc(('e', pl.id), 'shieldT') == 300)
    s.setsc('#dmgIn', 'tmp', 50)
    s.setsc('#elem', 'tmp', 2)
    s.call('rlk:element/shield_absorb', Ctx(pl, tuple(pl.pos), (0, 0)))
    ck('element/shield_absorb_el 250 %', s.sc('#dmgIn', 'tmp') == 0 and s.sc(('e', pl.id), 'shieldHP') == 10,
       f"dmgIn {s.sc('#dmgIn', 'tmp')} shield {s.sc(('e', pl.id), 'shieldHP')}")
    s.setsc('#dmgIn', 'tmp', 50)
    s.setsc('#elem', 'tmp', 0)
    s.call('rlk:element/shield_absorb', Ctx(pl, tuple(pl.pos), (0, 0)))
    ck('element/shield_absorb 1:1', s.sc('#dmgIn', 'tmp') == 40 and s.sc(('e', pl.id), 'shieldHP') == 0)
    s.setsc(('e', pl.id), 'gShield', 15)
    s.setsc('#dmgIn', 'tmp', 10)
    s.call('rlk:engravings/guard/absorb', Ctx(pl, tuple(pl.pos), (0, 0)))
    ck('engravings/guard/absorb real', s.sc('#dmgIn', 'tmp') == 0 and s.sc(('e', pl.id), 'gShield') == 5)
    s.setsc(('e', pl.id), 'gShield', 0)
    # hurt_elem (reaction damage on the player: no defence, shields first)
    hp0 = s.sc(('e', pl.id), 'curHealth')
    s.setsc('#dmg', 'tmp', 7)
    s.setsc('#elem', 'tmp', 1)
    s.call('rlk:element/dot', Ctx(pl, tuple(pl.pos), (0, 0)))
    ck('element/dot -> player/hurt_elem real', hp0 - s.sc(('e', pl.id), 'curHealth') == 7)
    # 2. the player's attack: real melee_begin / clear_atkflags / combat/apply / apply_mods / lv_mult / res
    mh0 = s.sc(('e', b.id), 'mhpC')
    landed, dealt, killed = strike(s, b, 18, elem=0)
    lvA, lvB = 5 + 100, s.sc(('e', b.id), 'mlv') * 150 // 100 + 100
    ck('combat/apply real (lv_mult)', landed and dealt == 18 * lvA // (lvA + lvB) and not killed,
       f'dealt {dealt} expected {18 * lvA // (lvA + lvB)} mhpC {mh0}->{s.sc(("e", b.id), "mhpC")}')
    ck('combat/melee_begin real', bool(s.select('@e[tag=rlk_melee_origin]', C0)))
    s.setsc(('e', b.id), 'mres', 30)
    landed, dealt, _ = strike(s, b, 100, elem=0)
    exp = max(1, 100 * lvA // (lvA + lvB) * 70 // 100)
    ck('combat/res real (RES 30)', dealt == exp, f'dealt {dealt} expected {exp}')
    s.setsc(('e', b.id), 'mres', 0)
    # element attach + reaction: Pyro then Hydro = Vaporize x1.5 (element/on_hit + react real; the ICD is real too,
    # so it is reset between the probe hits)
    def icd0():
        s.setsc(('e', b.id), 'icdT', 0)
        s.setsc(('e', b.id), 'icdC', 0)
    icd0()
    strike(s, b, 20, elem=1)
    icd0()
    a_fire = s.sc(('e', b.id), 'aFire') or 0
    landed, dealt, _ = strike(s, b, 20, elem=2)
    base = 20 * lvA // (lvA + lvB)
    ck('element/on_hit + react real (Pyro aura, Vaporize)', a_fire > 0 and dealt > base,
       f'aFire {a_fire} dealt {dealt} vs plain {base}')
    # Overload (Pyro aura + Electro) queues rxQ 3 -> the mob element tick runs rx_run -> run/overload -> aoe_hit
    for o in ('aWater', 'aFire', 'aThunder'):
        s.setsc(('e', b.id), o, 0)
    s.erng.seed(5)
    icd0()
    strike(s, b, 20, elem=1)
    icd0()
    strike(s, b, 20, elem=3)
    q = s.sc(('e', b.id), 'rxQ') or 0
    n0 = s.calls_n.get('rlk:element/rx_run', 0)
    mh1 = s.sc(('e', b.id), 'mhpC')
    world(s)
    ck('element/rx_run + run/overload + aoe_hit real (mob element tick)',
       q == 3 and s.calls_n.get('rlk:element/rx_run', 0) == n0 + 1 and s.sc(('e', b.id), 'mhpC') < mh1,
       f"rxQ {q} rx_run {s.calls_n.get('rlk:element/rx_run', 0) - n0} mhpC {mh1}->{s.sc(('e', b.id), 'mhpC')}")
    # lunar hit (element/lunar/hit real)
    mh1 = s.sc(('e', b.id), 'mhpC')
    s.setsc('#lnB', 'tmp', 30)
    s.setsc('#lnEl', 'tmp', 3)
    s.setsc('#lnT', 'tmp', 1)
    try:
        s.call('rlk:element/lunar/hit', Ctx(b, tuple(b.pos), (0, 0)))
        ck('element/lunar/hit real', s.sc(('e', b.id), 'mhpC') < mh1, f"mhpC {mh1}->{s.sc(('e', b.id), 'mhpC')}")
    except Exception as ex:  # noqa: BLE001
        ck('element/lunar/hit real', False, repr(ex))
    # 3. kill: the real kill path (heal orb roll, kill_xp, gold_drop x goldMul, sapphires) + combat_clear -> mboss/won
    s.setsc(('e', b.id), 'mhpC', 5)
    landed, dealt, killed = strike(s, b, 100)
    gold = [e for e in s.ents if e.alive and 'rlk_gold' in e.tags]
    ck('kill path real (gold_drop, kill_xp, sap_loop)', killed and len(gold) == 1 and (s.sc('#XP', 'azs') or 0) > 0
       and (s.sc('#SAP', 'azs') or 0) == s.sc('#mbSap', 'mb'),
       f"gold {[s.sc(('e', e.id), 'gval') for e in gold]} xp {s.sc('#XP', 'azs')} sap {s.sc('#SAP', 'azs')}")
    gv = s.sc(('e', gold[0].id), 'gval') if gold else 0
    mn, mx, mul = s.sc('#mobGoldMin', 'tmp'), s.sc('#mobGoldMax', 'tmp'), s.sc('#mbGoldMul', 'mb')
    ck('gold_drop amount (min..max x mbGoldMul, chapter 1)', mn * mul <= gv <= mx * mul, f'{gv} in {mn * mul}..{mx * mul}')
    for _ in range(400):
        world(s)
        if (s.sc('#mbLive', 'mb') or 0) == 0 and (s.sc('#combat', 'room') or 0) == 0:
            break
    ck('room/combat_clear real -> mboss/won', s.calls_n.get('rlk:room/combat_clear', 0) >= 1
       and (s.sc('#mbLive', 'mb') or 0) == 0, f"clears {s.calls_n.get('rlk:room/combat_clear', 0)}")
    # UUID entities (cm.md 9.1 / 14: proxies and fixed-id props are addressed by UUID)
    s.cmd(Z_split('summon minecraft:interaction 1.0 201.0 2.0 {UUID:[I;1380731725,1096434688,-2147483648,65],'
                  'Tags:["rlk_mb_px","rlk_azs_u"],width:2.8f,height:4.5f}'), C0)
    dup = s.cmd(Z_split('summon minecraft:interaction 1.0 201.0 2.0 {UUID:[I;1380731725,1096434688,-2147483648,65]}'), C0)
    u = '524c4b4d-415a-4400-8000-000000000041'
    s.cmd(Z_split(f'scoreboard players set {u} mbPart 1'), C0)
    s.cmd(Z_split(f'execute as {u} at @s run tp @s ~1 ~ ~'), C0)
    s.cmd(Z_split(f'data merge entity {u} {{height:3.0f}}'), C0)
    ue = s.select(u, C0)
    ck('UUID summon / select / score / tp / data merge', len(ue) == 1 and dup == 0 and s.sc(('e', ue[0].id), 'mbPart') == 1
       and abs(ue[0].pos[0] - 2.0) < 1e-9 and ue[0].data.get('width') == 2.8 and ue[0].data.get('height') == 3.0)
    for e in ue:
        e.alive = False
    s.ents = [e for e in s.ents if e.alive]
    # 4. room flow (the Raiden smoke on M0; the chapter route once AZ-CM exists)
    s2, z2, p2 = setup(force=1, dp=dp)
    s2.setsc('#chapter', 'room', 2)
    s2.call('rlk:room/pick/boss', C0)
    ck('room/pick/boss real (chapter 2 -> Raiden layout)', (s2.sc('#RDLAYOUT', 'azs') or 0) == 1)
    zb = Ent('marker', (0.5, 201.0, 0.5), tags=['rlk_zone'])
    zb.data.update({'boss_id': 'narukami', 'fn': 'boss'})
    s2.ents.append(zb)
    for o, v in (('zkind', 9), ('zst', 0), ('zid', 9)):
        s2.setsc(('e', zb.id), o, v)
    s2.storage.setdefault('rlk:room', {})['th'] = {'n': 'ruin'}
    zc = Ctx(zb, tuple(zb.pos), (0, 0))
    s2.call('rlk:room/zone_build', zc)
    ck('room/zone_build real (narukami -> raiden/build)', (s2.sc('#RDBUILD', 'azs') or 0) == 1
       and s2.sc(('e', zb.id), 'zst') == 1)
    s2.call('rlk:room/zone_enter', zc)
    ck('room/zone_enter real (kind 9 -> combat_start)', s2.sc('#combat', 'room') == 9 and s2.sc(('e', zb.id), 'zst') == 2)
    for _ in range(25):
        world(s2)
    ck('room/boss_spawn real (-> boss/raiden/spawn)', (s2.sc('#RDSPAWN', 'azs') or 0) == 1)
    for e in s2.ents:
        if 'rlk_azs_raiden' in e.tags:
            e.alive = False
    s2.ents = [e for e in s2.ents if e.alive]
    world(s2)
    objs = [e for e in s2.ents if e.alive and 'rlk_obj' in e.tags and s2.sc(('e', e.id), 'oact') == 8]
    ck('room/combat_clear real (kind 9 -> k_chapter, oact 8)', len(objs) == 1)
    if objs:
        s2.call('rlk:room/obj/click', Ctx(objs[0], tuple(objs[0].pos), (0, 0)))
        ck('room/obj/click real -> run/next_chapter real', s2.sc('#chapter', 'room') == 3
           and (s2.sc('#ROOMGEN', 'azs') or 0) == 1 and s2.sc('#mapIdx', 'room') == 0)
    if feat['chapter']:
        s3, z3, p3 = setup(force=0, dp=dp)
        s3.setsc('#chapter', 'room', 1)
        s3.call('rlk:room/pick/boss', C0)
        print('     chapter mode present: pick/boss chapter 1 ->', 'Raiden' if s3.sc('#RDLAYOUT', 'azs') else 'chapter boss')
        if feat['cproto']:
            try:
                s4, z4, p4 = setup(force=0, dp=dp)
                s4.setsc('#cbForce', 'mb', 0)
                chapter_entry(s4, 'cproto')
                ck('chapter entry on cproto (zone_build -> gate -> boss_spawn -> fight)', True)
            except Exception as ex:  # noqa: BLE001
                ck('chapter entry on cproto', False, repr(ex))
    else:
        print('     chapter mode (F:mboss/cb) absent on this datapack: chapter entry checks skipped')
    print('ignored commands:', dict(sorted(s.ignored.items(), key=lambda x: -x[1])[:12]))
    print('unset operation sources read as 0:', s.unset_src)
    print(f'{len(fails)} failure(s)')
    return fails


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        sys.exit(1 if selftest(sys.argv[2] if len(sys.argv) > 2 else None) else 0)
    print(__doc__)
