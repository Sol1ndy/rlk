#!/usr/bin/env python3
"""Shared mcsim harness of the field generator suites (copied from the butterfly's mb2/tests/bfsim.py).

The rig (rlk:mboss/fieldgen/rig/... or, before the real rig is merged, rig_stub/...) is out of scope: its calls are
logged, except face/player and face/track, which turn the anchor as the rig API says (instant / at most 4 degrees per
call). Engine functions outside F:mboss are stubbed with the behaviour the mid-boss relies on; combat/apply keeps the
real element/on_hit, module on_hit and combat/apply_mods (RES, incoming) so the meter and the damage rules are real.

Additions over bfsim: attribute modifiers (`attribute <t> <attr> modifier add|remove`, `base set|get`, `get [scale]`,
the vanilla formula base -> add_value -> x(1 + sum add_multiplied_base) -> x prod(1 + add_multiplied_total)), the
entity Motion store (the view/move avatar jump), and world() runs the two low-gravity lines of rlk:tick (read from
data/rlk/function/tick.mcfunction, so the real lines are tested) before rlk:mboss/main, in rlk:tick's order.

The fx kit (rlk:mboss/fieldgen/fx/**, tools/build_mboss_fg_fx.py) runs for real; its public calls are logged in
FSim.kit (as bfsim does for the butterfly kit), with the executor and the position in FSim.kitctx, and the mcsim gaps it
relies on are filled here (append of every element of a storage list path[]).
"""
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mcsim import Sim, Ent, Ctx  # noqa: E402

C0 = Ctx(None, (0, 0, 0), (0, 0))
RIG_PREFIXES = ('rlk:mboss/fieldgen/rig/', 'rlk:mboss/fieldgen/rig_stub/')
KIT = 'rlk:mboss/fieldgen/fx/'          # the fx / audio / HUD kit (its own stub rig fx/rig_stub/ is not the module's rig)
KIT_INTERNAL = ('e/', 'tele/e/', 'hud/e/', 'p/e/')
FAIL = []
ATTR_BASE = {'minecraft:gravity': 0.08, 'minecraft:jump_strength': 0.41999998688697815, 'minecraft:safe_fall_distance': 3.0,
             'minecraft:scale': 1.0, 'minecraft:movement_speed': 0.1, 'minecraft:fall_damage_multiplier': 1.0}


def check(name, ok, info=''):
    print(('ok   ' if ok else 'FAIL ') + name, info)
    if not ok:
        FAIL.append(name)


def load_api(dp):
    tools = str(Path(dp) / 'tools')
    if tools not in sys.path:
        sys.path.insert(0, tools)
    from mboss_fieldgen import api
    return api


class FSim(Sim):
    def __init__(self, root):
        super().__init__(root)
        self.rig = []            # (tick, rig call)
        self.t = 0
        self.sounds = []         # (tick, event, volume)
        self.hits = []           # (tick, pct, element, nododge) of every player hit (cm/hit_pl2)
        self.calls = []          # (tick, function id) of every module call under rlk:mboss/fieldgen/ (not the rig)
        self.sched = {}
        self.attrs = {}          # entity id -> {attribute: {'base': v, 'mods': {id: (value, op)}}}
        self.motion = {}         # entity id -> [x, y, z]
        self.says = []           # (tick, text) typed captions
        self.log_calls = False
        self.hz = []             # every hazard made: dict(t, tell, dmg, kind, r, r0, nd, rearm, grp, y1, pos, yaw)
        self.pjs = []            # every projectile launched: (t, macro args)
        self.hzhits = []         # every hazard hit attempt (hz/hurt): (t, group, dmg %, kind, marker pos)
        self.kit = []            # (tick, kit call without the prefix, e.g. 'hud/meter_hit', 'tele/clear', 'p/slam')
        self.kitctx = []         # (tick, kit call, executor id or None, position) of the same calls
        self.max_cards = 0       # most kit cards (tag rlk_fk) alive at once (world())

    # ---------------------------------------------------------------- attributes
    def attr(self, e, name):
        name = name if ':' in name else 'minecraft:' + name
        a = self.attrs.setdefault(e.id, {})
        if name not in a:
            a[name] = {'base': ATTR_BASE.get(name, 0.0), 'mods': {}}
        return a[name]

    def attr_value(self, e, name):
        a = self.attr(e, name)
        v = a['base'] + sum(x for x, op in a['mods'].values() if op == 'add_value')
        v *= 1 + sum(x for x, op in a['mods'].values() if op == 'add_multiplied_base')
        for x, op in a['mods'].values():
            if op == 'add_multiplied_total':
                v *= 1 + x
        return v

    def mods(self, e, name):
        return dict(self.attr(e, name)['mods'])

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'attribute':
            ents = self.select(t[1], ctx) if t[1] != '@s' else ([ctx.ex] if ctx.ex else [])
            if not ents:
                return 0
            e = ents[0]
            a = self.attr(e, t[2])
            if t[3] == 'modifier':
                mid = t[5] if t[5].count(':') else 'minecraft:' + t[5]
                if t[4] == 'add':
                    if mid in a['mods']:
                        return 0                # vanilla: "modifier already present" -> the command fails
                    a['mods'][mid] = (float(t[6]), t[7])
                    return 1
                if t[4] == 'remove':
                    return 1 if a['mods'].pop(mid, None) is not None else 0
            if t[3] == 'base':
                if t[4] == 'set':
                    a['base'] = float(t[5])
                    return 1
                if t[4] == 'get':
                    return math.floor(a['base'] * (float(t[5]) if len(t) > 5 else 1))
                if t[4] == 'reset':
                    a['base'] = ATTR_BASE.get(t[2] if ':' in t[2] else 'minecraft:' + t[2], 0.0)
                    return 1
            if t[3] == 'get':
                return math.floor(self.attr_value(e, t[2]) * (float(t[4]) if len(t) > 4 else 1))
            return 0
        if c == 'schedule':
            if t[1] == 'function':
                self.sched[t[2]] = self.t + int(t[3].rstrip('t'))
            elif t[1] == 'clear':
                self.sched.pop(t[2], None)
            return 1
        if c == 'execute' and len(t) == 9 and t[1:4] == ['store', 'result', 'score'] and t[6] == 'if' and t[7] == 'entity':
            n = len(self.select(t[8], ctx))
            for h in self.holders(t[4], ctx):
                self.setsc(h, t[5], n)
            return n
        if c == 'data' and t[1] == 'modify' and t[2] == 'storage' and t[5] == 'merge' and t[6] == 'value':
            st = self.storage.setdefault(t[3], {})
            try:
                node = self.path_get(st, t[4])
            except KeyError:
                node = {}
                self.path_set(st, t[4], node)
            node.update(self.snbt(t[7]))
            return 1
        if (c == 'data' and t[1] == 'modify' and t[2] == 'storage' and t[5] == 'append' and t[6] == 'from'
                and t[7] == 'storage' and t[9].endswith('[]')):
            import copy
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
        if c == 'data' and t[1] in ('modify', 'merge') and t[2] == 'entity' and t[3] != '@s' and not self.select(t[3], ctx):
            return 0                    # no target: the command fails (the kit's stub-rig crack outside its demo)
        if c == 'playsound':
            self.sounds.append((self.t, t[1].split(':')[-1], float(t[7]) if len(t) > 7 else 1.0))
            return 1
        if t[:3] == ['time', 'query', 'gametime']:
            return self.t
        v = super().cmd(t, ctx)
        if t[0] == 'scoreboard' and t[1] == 'players' and t[2] in ('add', 'remove', 'set') and not t[3].startswith('@'):
            return self.sc(self.holder(t[3], ctx), t[4])
        return v

    def store(self, spec, v, ctx):
        if spec[1] == 'entity' and spec[3].startswith('Motion['):
            e = (self.select(spec[2], ctx) if spec[2] != '@s' else [ctx.ex])[0]
            m = self.motion.setdefault(e.id, [0.0, 0.0, 0.0])
            m[int(spec[3][7])] = (v or 0) * float(spec[5])
            return
        return super().store(spec, v, ctx)

    def call(self, fid, ctx, macro=None):
        for p in RIG_PREFIXES:
            if fid.startswith(p):
                sub = fid[len(p):]
                self.rig.append((self.t, sub))
                if sub == 'face/player' and ctx.ex is not None:
                    return self.call('rlk:fgtest/face_player', ctx)
                if sub == 'face/track' and ctx.ex is not None:
                    return self.call('rlk:mboss/mv/turn', ctx, {'max': 4})
                return 1
        if fid.startswith(KIT) and not fid[len(KIT):].startswith(KIT_INTERNAL):
            self.kit.append((self.t, fid[len(KIT):]))
            self.kitctx.append((self.t, fid[len(KIT):], ctx.ex.id if ctx.ex is not None else None, tuple(ctx.pos)))
        if self.log_calls and fid.startswith('rlk:mboss/fieldgen/'):
            self.calls.append((self.t, fid[len('rlk:mboss/fieldgen/'):]))
        if fid == 'rlk:mboss/hz/make':
            g = lambda k: self.sc(k, 'mb')
            self.hz.append(dict(t=self.t, tell=g('#hzW'), dmg=g('#hzD'), kind=g('#hzK'), r=g('#hzR'), r0=g('#hzR0'),
                                nd=g('#hzNoDodge'), rearm=g('#hzRearm'), grp=g('#hzGrp'), y1=g('#hzY1'), act=g('#hzAct'),
                                quiet=g('#hzQuiet'), pos=tuple(ctx.pos), yaw=ctx.rot[0]))
        if fid == 'rlk:mboss/hz/hurt' and ctx.ex is not None:
            g = lambda o: self.sc(('e', ctx.ex.id), o)
            self.hzhits.append((self.t, g('mbHzG'), g('mbHzD'), g('mbHzK'), tuple(ctx.ex.pos)))
        if fid == 'rlk:mboss/pj/launch':
            self.pjs.append((self.t, dict(macro or {}), self.sc('#pjShape', 'mb'), self.sc('#pjGrp', 'mb')))
        if fid == 'rlk:cm/hit_pl2':
            self.hits.append((self.t, self.sc('#mbHitPct', 'mb'), self.sc('#cmEl', 'tmp'), self.sc('#mbNoDodge', 'mb') or 0))
        if fid == 'rlk:mboss/line/say' and macro:
            self.says.append((self.t, macro.get('t')))
        return super().call(fid, ctx, macro)

    def clips(self, since=0):
        return [(t, s[5:]) for t, s in self.rig if s.startswith('play/') and t >= since]

    def rigcalls(self, name, since=0):
        return [t for t, s in self.rig if s == name and t >= since]

    def kitcalls(self, name, since=0):
        """Ticks of the kit call `name` (e.g. 'hud/meter_open', 'tele/clear') at or after `since`."""
        return [t for t, s in self.kit if s == name and t >= since]

    def kit_cards(self):
        return [e for e in self.ents if e.alive and 'rlk_fk' in e.tags]

    def kit_flags(self):
        """The kit's HUD flags (storage rlk:fgkit hud.open / lowg / grog / hint) as a dict of 0 / 1."""
        h = self.storage.get('rlk:fgkit', {}).get('hud', {})
        return {k: int(h.get(k, 0) or 0) for k in ('open', 'lowg', 'grog', 'hint')}

    def run_sched(self):
        for fid, at in sorted(self.sched.items(), key=lambda x: x[1]):
            if at <= self.t:
                del self.sched[fid]
                self.call(fid, C0)


STUBS = {
    'rlk:fgtest/face_player': ['execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'],
    'rlk:room/mob_init': ['scoreboard players set @s mlv 4', 'function rlk:mboss/base_stats with storage rlk:mboss cur',
                          'scoreboard players set @s mhpM 100000', 'scoreboard players set @s mhpC 100000'],
    'rlk:mob/setup': ['tag @s add rlk_mob'],
    'rlk:mob/level_apply': [],
    'rlk:view/sync': ['tp @e[tag=rlk_body] @s'],
    'rlk:view/ttl_blank': [], 'rlk:view/stop_h': [], 'rlk:bossui/draw': [],
    'rlk:room/combat_start': ['scoreboard players operation #combat room = @s zid', 'scoreboard players set #spawnT room 20'],
    'rlk:room/combat_clear': ['scoreboard players set @s zst 3', 'scoreboard players set #combat room 0', 'function rlk:mboss/won'],
    'rlk:room/obj/kill_group': ['kill @s'],
    'rlk:room/obj/k_mboss': ['scoreboard players add #REGATE mb 1', 'function rlk:mboss/roll'],
    'rlk:room/obj/make_node': [],
    'rlk:combat/gold_absorb': ['scoreboard players add #GOLD mb 1', 'kill @s'],
    'rlk:lvup/add': ['$scoreboard players add @s pkPending $(n)'],
    'rlk:lvup/toggle': ['scoreboard players set @s pkMode 1'],
    # cm/hit_pl2 as far as the mid-boss relies on it: the dash i-frames of player/take_damage (dashInvT >= 1 -> dodged)
    'rlk:cm/hit_pl2': ['scoreboard players set #dodged tmp 0',
                       'execute if score @s dashInvT matches 1.. run scoreboard players set #dodged tmp 1',
                       'execute if score #dodged tmp matches 1 run return run scoreboard players add #DODGES mb 1',
                       'scoreboard players add #PHITS mb 1', 'scoreboard players operation #PLAST mb = #mbHitPct mb',
                       'scoreboard players operation #PEL mb = #cmEl tmp'],
    'rlk:player/knockback/check': [],
    'rlk:mboss/arena/ensure': ['return 1'],
    'rlk:combat/clear_atkflags': [],
    'rlk:player/hurt_do': [],
    'rlk:combat/apply': ['execute if entity @s[tag=rlk_mb_dying] run return 0',
                         'execute if entity @s[tag=rlk_mb_inv] unless score #trueDmg tmp matches 1 run return 0',
                         'execute unless score #trueDmg tmp matches 1 run function rlk:element/on_hit',
                         'execute if entity @s[tag=rlk_mb_body] unless score #trueDmg tmp matches 1 run function rlk:mboss/d/on_hit',
                         'execute unless score #trueDmg tmp matches 1 run function rlk:combat/apply_mods',
                         'execute if entity @s[tag=rlk_mb_hit] unless score #trueDmg tmp matches 1 run return run function rlk:mboss/aux_hit',
                         'scoreboard players operation #LASTDMG mb = #dmg tmp',
                         'scoreboard players operation @s mhpC -= #dmg tmp',
                         'execute if score @s mhpC matches ..0 if entity @s[tag=rlk_mb_body] run function rlk:mboss/death_start'],
    'rlk:engravings/on_apply': [], 'rlk:items/hook/on_apply': [], 'rlk:combat/lv_mult': [],
    'rlk:element/rx_text': [], 'rlk:engravings/on_rx': [], 'rlk:element/icd': [],
    'rlk:element/display': [], 'rlk:snd/f42': [],
    'rlk:element/color': [], 'rlk:combat/text_crit_macro': [], 'rlk:combat/text_normal_macro': [],
}

SEED = [3141]
ROOT = [None]
TICK_LOWG = []          # the two low-gravity lines of rlk:tick (the real ones)


def init(dp):
    ROOT[0] = Path(dp) / 'data/rlk/function'
    lines = (ROOT[0] / 'tick.mcfunction').read_text(encoding='utf-8').split('\n')
    TICK_LOWG[:] = [l for l in lines if 'rlk:mboss/lowg_' in l and not l.startswith('#')]
    assert len(TICK_LOWG) == 2, TICK_LOWG
    return load_api(dp)


def setup(force=3, hp=None, player_pos=(40.5, 201.0, 18.0)):
    """A fresh simulated world with the player in a mid-boss zone (first person: the player is the body); `random`
    is seeded per setup (SEED[0] += 1), so every suite run draws the same picks."""
    import random
    random.seed(SEED[0])
    SEED[0] += 1
    s = FSim(ROOT[0])
    for k, v in STUBS.items():
        s.cache[k] = list(v)
    if hp:
        s.cache['rlk:room/mob_init'] = ['scoreboard players set @s mlv 4', 'function rlk:mboss/base_stats with storage rlk:mboss cur',
                                        f'scoreboard players set @s mhpM {hp}', f'scoreboard players set @s mhpC {hp}']
    s.cache['rlk:fgtest/lowg'] = list(TICK_LOWG)
    s.call('rlk:mboss/init', C0)
    for k, v in (('#100', 100), ('#4', 4), ('#2', 2), ('#st10', 10), ('#reactBase', 50)):
        s.setsc(k, 'tmp', v)
    s.storage.setdefault('rlk:room', {})['ready'] = 1
    s.storage.setdefault('rlk:config', {})['installed'] = 1
    zone = Ent('marker', (40.5, 201.0, 20.5), tags=['rlk_zone'])
    player = Ent('player', player_pos, (180, 0), tags=['player', 'rlk_body'])
    safe = Ent('marker', player_pos, tags=['rlk_safe', 'rlk_room'])
    s.ents += [zone, player, safe]
    for o, v in (('zkind', 15), ('zst', 3), ('zid', 4)):
        s.setsc(('e', zone.id), o, v)
    for o in ('dead', 'rnDie', 'pkMode', 'vMap', 'devMode', 'pkPending', 'pkMb', 'def', 'dashInvT', 'elemMastery', 'bol'):
        s.setsc(('e', player.id), o, 0)
    for o, v in (('curHealth', 1000), ('maxHealth', 1000), ('critDamage', 150), ('critChance', 30), ('atk', 100)):
        s.setsc(('e', player.id), o, v)
    s.setsc('#chapter', 'room', 1)
    s.setsc('#active', 'room', 1)
    s.setsc('#mbForce', 'mb', force)
    return s, zone, player


def press_gate(s, zone):
    s.call('rlk:room/obj/k_mboss', Ctx(zone, tuple(zone.pos), (0, 0)))
    gate = Ent('marker', zone.pos, tags=['rlk_obj'])
    s.ents.append(gate)
    s.call('rlk:mboss/gate', Ctx(gate, tuple(gate.pos), (0, 0)))
    return gate


def world(s):
    """The relevant part of rlk:tick (the low-gravity sync, then mboss/main) + room/tick."""
    s.t += 1
    s.call('rlk:fgtest/lowg', C0)
    if (s.sc('#mbLive', 'mb') or 0) == 1:
        s.call('rlk:mboss/main', C0)
    if (s.sc('#combat', 'room') or 0) >= 1:
        if (s.sc('#spawnT', 'room') or 0) >= 1:
            s.setsc('#spawnT', 'room', s.sc('#spawnT', 'room') - 1)
            if s.sc('#spawnT', 'room') == 0:
                z = s.select('@e[tag=rlk_zone,scores={zkind=15},limit=1]', C0)[0]
                s.call('rlk:mboss/start', Ctx(z, tuple(z.pos), (0, 0)))
        elif not s.select('@e[tag=rlk_zmob,limit=1]', C0):
            z = s.select('@e[tag=rlk_zone,scores={zkind=15},limit=1]', C0)[0]
            s.setsc(('e', z.id), 'zst', 3)
            s.setsc('#combat', 'room', 0)
            s.call('rlk:mboss/won', Ctx(z, tuple(z.pos), (0, 0)))
    if (s.sc('#mbBoxOn', 'mb') or 0) == 1:
        s.call('rlk:mboss/box/all', C0)
    s.run_sched()                       # scheduled functions run after the tick functions (the kit's ager, pip unflash)
    s.max_cards = max(s.max_cards, len(s.kit_cards()))


def run(s, n, each=None):
    for _ in range(n):
        if each:
            each(s)
        world(s)


def fg(s, k):
    return s.sc(k, 'mb')


def body_of(s):
    b = s.select('@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]', C0)
    return b[0] if b else None


def hit(s, target, elem, dmg, tfm=0, sub=0):
    """One player hit on target through the stubbed combat/apply (returns the damage dealt)."""
    s.setsc('#elem', 'tmp', elem)
    s.setsc('#dmg', 'tmp', dmg)
    s.setsc('#tfm', 'tmp', tfm)
    s.setsc('#crit', 'tmp', 0)
    s.setsc('#elU', 'tmp', 1000 if elem else 0)
    s.setsc('#icd', 'tmp', 0)
    s.setsc('#trueDmg', 'tmp', 0)
    s.setsc('#sub', 'itv', sub)
    s.setsc('#LASTDMG', 'mb', -1)
    s.call('rlk:combat/apply', Ctx(target, tuple(target.pos), (0, 0)))
    s.setsc('#sub', 'itv', 0)
    return s.sc('#LASTDMG', 'mb')


def test(s, player, n):
    s.call('rlk:mboss/test/pattern', Ctx(player, tuple(player.pos), (0, 0)), {'id': n})


def to_fight(s, zone, limit=400):
    press_gate(s, zone)
    for _ in range(limit):
        world(s)
        if fg(s, '#mbSt') == 1:
            return True
    return False


def pl(s, player, o):
    return s.sc(('e', player.id), o)


def flat(v):
    if isinstance(v, list):
        return ''.join(flat(x) for x in v)
    if isinstance(v, dict):
        return str(v.get('text', '')) + flat(v.get('extra', []))
    return str(v)


def hdist(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def arena_r(e):
    """Horizontal distance from the arena marker (200.5, 8.5: integer summon coordinates are block-centred in game,
    mcsim keeps them as written: 200, 8)."""
    return math.hypot(e.pos[0] - 200.0, e.pos[2] - 8.0)
