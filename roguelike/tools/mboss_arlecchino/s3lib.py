"""S3 helpers of the 아를레키노 (Arlecchino) module generator (OWNER: S3; contract S:ar/contract.md §1): score / call
shorthands, the kit-or-stand-in visual and sound lines, the hazard lines from api.HITS (with the FN-1 bond option or its
documented stand-in), the lock marker, and the pattern builder PB used by p1.py (S4 may use it for p2.py).

Importing has no side effects. Runtime conventions (contract §3.4): @s = the body, at it; #pt kn = the pattern clock (0 in
p/<key>/start, +1 before each p/<key>/tick); the shown clip tick == #pt (the core calls rig/tick after the pattern). A
hit of clip event e is a quiet hazard created at #pt e - 1 with tell 1 (hz/init sets mbHzT -1), so it strikes on the
game tick of #pt e; its aim is the body yaw at creation (the patterns stop turning LOCK ticks before every hit).
Hazards, props and markers of a pattern carry rlk_kn_p + rlk_kn_p_<key>; p/<key>/cancel kills them (idempotent).

Bond-of-Life hits (contract §3.1, FN-1): with S1's mboss_lib option (api.fn1_ready()) a bol hazard is made with
hz_opts(bol=BOL_HIT); until then (documented stand-in, removed at I1) the pattern raises #bolw kn on the strike tick and
the core's bond tick turns a landed hit (#mbHitEv) of that tick into #mbHitBol (bond.py). P1 never strikes a bol and a
plain hazard on the same tick (pat_p1 checks it), so the stand-in cannot mislabel a hit.
"""
from collections import defaultdict

from . import api

L, K = api.L, api.K
NS, OBJ, CY = api.NS, api.OBJ, api.CY
LOCK = 6                     # ticks before a follow-up hit when the body stops turning toward the player (aim locked)
LOCK_FIRST = 8               # ... before the first hit of a cast
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'
ARENA_M = '@e[type=minecraft:marker,tag=rlk_mb_arena,limit=1]'
LOCK_M = '@e[type=minecraft:marker,tag=rlk_kn_lock,limit=1]'
TID = {n.split(' ')[0]: tid for tid, n in api.TEST_IDS.items() if n.split(' ')[0] in api.P1 + api.P2}  # key -> test id = #pat id
AT_BODY = 'at @s rotated as @s rotated ~ 0'
FN1 = api.fn1_ready()


def fn(rel):
    return f'function {NS}{rel}'


def sset(name, v):
    return f'scoreboard players set {name} {OBJ} {int(v)}'


def gate(cond, cmd):
    """`execute <cond> run <cmd>`, merged into cmd's own execute chain when it has one."""
    return f'execute {cond} {cmd[8:]}' if cmd.startswith('execute ') else f'execute {cond} run {cmd}'


def tag_p(key):
    return f'rlk_kn_p_{key}'


def tags_nbt(key, *more):
    tg = ['rlk_room', 'rlk_mb_aux', api.TAGS['pat'], tag_p(key)] + list(more)
    return '[' + ','.join(f'"{t}"' for t in tg) + ']'


def clip_id(clip):
    return api.CLIP_ORDER.index(clip)


def num(v, nd=3):
    return L.num(v, nd)


def placed(lines, pos):
    """Run each line at a position / rotation (pos = execute subcommands); an `execute ... run X` line gets them before
    its first ' run '."""
    out = []
    for c in lines:
        if not c:
            continue
        if c.startswith('execute '):
            i = c.index(' run ')
            out.append(c[:i] + ' ' + pos + c[i:])
        else:
            out.append(f'execute {pos} run {c}')
    return out


# ------------------------------------------------------------------------------------------------- sounds
# Vanilla stand-ins of the kit's sound recipes (api.KIT_SOUNDS names; PLAN §3-5) while S1K's kit is missing.
SND_FALLBACK = {
    'step': [('entity.player.attack.nodamage', 0.4, 0.6)],
    'swing_light': [('entity.player.attack.sweep', 0.8, 1.1), ('item.firecharge.use', 0.3, 1.4)],
    'swing_heavy': [('entity.player.attack.sweep', 1.0, 0.7), ('item.firecharge.use', 0.5, 0.9)],
    'spin': [('entity.player.attack.sweep', 1.0, 0.6), ('item.trident.riptide_1', 0.6, 1.3)],
    'slam': [('entity.generic.explode', 0.7, 1.2), ('block.anvil.land', 0.4, 0.6)],
    'wheel_spin': [('item.trident.riptide_2', 0.6, 1.4), ('block.fire.ambient', 0.6, 1.0)],
    'wheel_throw': [('item.trident.throw', 1.0, 0.7), ('entity.blaze.shoot', 0.5, 0.8)],
    'wheel_catch': [('item.trident.return', 0.8, 0.9)],
    'claw_reach': [('block.respawn_anchor.charge', 0.6, 1.5)],
    'claw_grab': [('entity.evoker_fangs.attack', 1.0, 0.7), ('entity.wither.hurt', 0.4, 1.6)],
    'leap': [('entity.ender_dragon.flap', 0.7, 1.4), ('item.firecharge.use', 0.6, 0.8)],
    'apex': [('block.fire.ambient', 0.8, 0.7)],
    'dive': [('entity.phantom.swoop', 0.8, 1.2)],
    'impact': [('entity.generic.explode', 0.9, 1.0), ('item.firecharge.use', 0.6, 0.6)],
    'wing_burst': [('entity.phantom.flap', 0.8, 0.6), ('item.elytra.flying', 0.4, 1.6)],
    'wing_hit': [('entity.player.attack.sweep', 1.0, 0.5), ('entity.wither.shoot', 0.4, 1.4)],
    'dash_tell': [('entity.ravager.roar', 0.4, 1.8), ('block.respawn_anchor.charge', 0.5, 1.2)],
    'dash': [('entity.blaze.shoot', 0.7, 1.4), ('entity.phantom.swoop', 0.5, 1.6)],
    'follow': [('entity.player.attack.sweep', 1.0, 0.8), ('entity.generic.explode', 0.5, 1.4)],
    'zig': [('entity.phantom.swoop', 0.5, 1.8)],
    'sweep': [('entity.player.attack.sweep', 1.0, 0.6)],
    'brand': [('block.respawn_anchor.set_spawn', 0.7, 1.4), ('entity.wither.shoot', 0.4, 0.6)],
    'bond_gain': [('block.respawn_anchor.charge', 0.6, 0.7)],
    'bond_tick': [('block.fire.extinguish', 0.25, 1.6)],
    'orb_spawn': [('block.amethyst_block.chime', 0.6, 1.2)],
    'flood': [('block.respawn_anchor.deplete', 0.8, 0.6)],
    'threads': [('entity.evoker_fangs.attack', 1.0, 0.8), ('entity.wither.shoot', 0.5, 0.6)],
    'blast': [('entity.generic.explode', 1.0, 0.7), ('entity.wither.break_block', 0.4, 1.2)],
    'cracks': [('block.basalt.break', 0.8, 0.6)],
    'blade_rise': [('block.pointed_dripstone.place', 1.0, 0.6), ('item.trident.return', 0.5, 0.6)],
    'blade_fly': [('item.trident.throw', 0.9, 0.6), ('entity.phantom.swoop', 0.6, 0.7)],
    'cross_hit': [('entity.evoker_fangs.attack', 1.0, 1.0), ('entity.player.attack.sweep', 0.8, 0.6)],
    'rim': [('block.pointed_dripstone.fall', 1.0, 0.7)],
    'clone_launch': [('entity.phantom.swoop', 0.8, 0.8), ('entity.illusioner.cast_spell', 0.5, 1.2)],
    'clone_hit': [('entity.player.attack.sweep', 1.0, 0.9), ('entity.wither.shoot', 0.3, 1.6)],
    'perch': [('entity.spider.ambient', 0.5, 0.6)],
    'shock_gain': [('block.beacon.power_select', 0.8, 1.4), ('entity.wither.ambient', 0.25, 1.8)],
    'shock_hit': [('entity.generic.explode', 0.7, 1.4), ('block.respawn_anchor.deplete', 0.6, 1.4)],
    'break': [('entity.wither.break_block', 1.0, 0.8), ('block.glass.break', 1.0, 0.6)],
    'stun': [('entity.iron_golem.damage', 0.6, 0.6)],
}


def snd(name):
    """The kit sound recipe, or its vanilla stand-in lines while the kit is missing (at the execution position)."""
    k = K.snd(name)
    if k:
        return [k]
    return [L.sound(e, v, p) for e, v, p in SND_FALLBACK[name]]


# ------------------------------------------------------------------------------------------------- visuals
# Vanilla stand-in particles (the footage's two colours: Pyro orange-gold, Bond-of-Life crimson-black).
DUST = {1: 'minecraft:dust{color:[1.0,0.55,0.16],scale:1.4}', 2: 'minecraft:dust{color:[0.72,0.04,0.12],scale:1.6}'}
FLAME = {1: 'minecraft:flame', 2: 'minecraft:crimson_spore'}


def part(p, dx, dy, dz, spd, n):
    return f'particle {p} ~ ~ ~ {num(dx, 2)} {num(dy, 2)} {num(dz, 2)} {num(spd, 3)} {int(n)} force @a[tag=player]'


def H(y):
    """A height on her figure (api.SIZE 1.4: the D0 numbers are already scaled)."""
    return num(y, 2)


def kit_or(kit_line, fallback, pos):
    """The kit call placed at pos, else the fallback lines placed at pos."""
    if kit_line:
        return placed([kit_line], pos)
    return placed(fallback, pos)


def fx_slash(r, c, roll=0, pitch=0, yaw=0, h=1.4):
    """A slash arc on the body (yaw / pitch / roll = offsets from the body yaw; kit slash_arc, c 1 Pyro / 2 BoL). The kit
    keeps its arc above the floor (pivot at h; S5 / K2: the vertical slashes pass h 2.0 so the clamp keeps their reach).
    The executor is already turned by yaw, so the kit's own yaw offset is 0 (it would add the offset twice)."""
    k = K.p('slash_arc', r=int(round(r * 10)), yaw=0, pitch=int(pitch), roll=int(roll), c=c)
    fb = [part('minecraft:sweep_attack', r * 0.3, 0.15, r * 0.3, 0, 3), part(DUST[c], r * 0.3, 0.2, r * 0.3, 0, 14),
          part(FLAME[c], r * 0.25, 0.2, r * 0.25, 0.02, 8)]
    if k:
        return placed([k], f'{AT_BODY} rotated ~{int(yaw)} 0 positioned ~ ~{H(h)} ~')
    return placed(fb, f'{AT_BODY} rotated ~{int(yaw)} 0 positioned ^ ^{H(1.0)} ^{num(r * 0.55, 2)}')


def fx_spin(r, c, h=1.0):
    k = K.p('spin_ring', r=int(round(r * 10)), c=c)
    return kit_or(k, [part(FLAME[c], r * 0.45, 0.1, r * 0.45, 0.03, 30), part(DUST[c], r * 0.5, 0.1, r * 0.5, 0, 20)],
                  f'at @s positioned ~ ~{H(h)} ~')


def fx_impact(r, c, pos=None):
    k = K.p('impact_burst', r=int(round(r * 10)), c=c)
    return kit_or(k, [part('minecraft:explosion', r * 0.25, 0.1, r * 0.25, 0, 2), part(DUST[c], r * 0.4, 0.2, r * 0.4, 0, 24)],
                  pos or f'{AT_BODY} positioned ~ ~0.2 ~')


def fx(name, fallback=(), pos=None, **a):
    """A kit preset at pos (default: the body, 1.4 b up), else the fallback lines there."""
    return kit_or(K.p(name, **a), list(fallback), pos or f'{AT_BODY} positioned ~ ~{H(1.4)} ~')


def hud(name, **a):
    k = K.hud(name, **a)
    return [k] if k else []


def line_say(lid):
    """The dialog subtitle of api.LINES[lid]: kit hud/line {id}, else the framework's typed subtitle (mboss/line/say)."""
    k = K.hud('line', id=lid)
    return k if k else L.say(api.LINES[lid], '#FF9AA8', gap=2, hold=50, snd=1)


def kit_with(sub, name, path):
    """A kit macro call reading its args from storage rlk:kn <path> (redraws with runtime values), '' without the kit."""
    table = {'decal/': api.KIT_DECALS, 'p/': api.KIT_PRESETS, 'prop/': api.KIT_PROPS, 'hud/': api.KIT_HUD}[sub]
    assert name in table
    return f'function {NS}fx/{sub}{name} with storage {api.STORAGE} {path}' if K._on() else ''


# ------------------------------------------------------------------------------------------------- hazards
SHAPE_FN = {'sector': L.hz_sector, 'disc': L.hz_disc, 'line': L.hz_line, 'ring': L.hz_ring}


def hz_tag(key):
    """Tag the hazard just made (#hzLast) rlk_kn_p + rlk_kn_p_<key> (core/hz_tag/<key>; the pattern's cancel kills it)."""
    return (f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run '
            f'function {NS}core/hz_tag/{key}')


def bol_opts(bol):
    """The FN-1 option kwargs of a bol hazard (empty while S1's mboss_lib lacks it: the #bolw stand-in marks the tick)."""
    return {api.FN1_OPT: api.BOL_HIT} if bol and FN1 else {}


def hz_opts(key, tier_dmg, bol, grp=False, kb=None, back=None, noparry=None):
    """The one-shot options of a pattern hazard: quiet (#hzQuiet 1: the floor markings of PLAN §1.5 are the kit decals,
    vanilla dust stand-ins while the kit is missing), no framework sound, Pyro, the FN-1 bond option. noparry=1: one of her
    unparriable hits (combat overhaul, api.NOPARRY): her hazards are made at the strike frame, so the pattern calls the
    warning glint itself at the hit's tell tick (np_warn below) and the framework draws none (glint=False)."""
    return L.hz_opts(quiet=1, sfx=0, grp=grp, kb=kb, el=api.PYRO, back=back, noparry=noparry, glint=not noparry, **bol_opts(bol))


def np_warn():
    """The unparriable-attack warning glint on her chest (@s = body; core/np: the rig's chest anchor of the running clip
    tick): put it at the tell tick of an unparriable hit that can be dodged (api.NOPARRY and the full-arena / per-mille hits
    the framework's rule makes unparriable), >= api.TELL_BIG t before the strike."""
    return fn('core/np')


def hazard(key, hit, grp=False, tell=1, kb=None, pos=None, dims=None, back=None, yaw=0, noparry=None):
    """Lines that create the hazard of api.HITS entry `hit` (aim = body yaw + yaw), striking `tell` ticks later.
    pos: execute subcommands for the origin (default the body on the floor); dims: shape args override (line length)."""
    clip, event, shape, hdims, tier, bol = hit
    dims = dims or hdims
    tier_dmg = api.dmg(tier, 1 if key in api.P1 else 2)
    out = hz_opts(key, tier_dmg, bol, grp=grp, kb=kb, back=back, noparry=noparry)
    if shape == 'full':
        call = L.hz_full(tell, tier_dmg)
    elif shape == 'disc_ahead':
        call = L.hz_disc(dims[0], tell, tier_dmg)
        pos = pos or f'{AT_BODY} positioned ^ ^ ^{num(dims[1], 2)} positioned ~ {CY} ~'
    else:
        call = SHAPE_FN[shape](*dims, tell, tier_dmg)
    where = pos or f'{AT_BODY} positioned ~ {CY} ~'
    rot = f' rotated ~{int(yaw)} 0' if yaw else ''
    out.append(f'execute {where}{rot} run {call}')
    out.append(hz_tag(key))
    return out


def bol_mark():
    """The FN-1 stand-in: the strike tick of a bol hazard (bond/tick reads it with #mbHitEv next tick). Empty with FN-1."""
    return [] if FN1 else [sset('#bolw', 1)]


# ------------------------------------------------------------------------------------------------- pattern builder
class PB:
    """Collects the commands of one pattern by pattern tick and writes p/<key>/{start,tick,cancel,k/<t>}; records every
    hit (event tick, HITS index, tell start, group) for the tests (p1.TABLE)."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.ticks = defaultdict(list)
        self.ranges = []                    # (t0, t1, command)
        self.cancel_lines = []
        self.hits = []                      # dicts: t, idx, tell, grp, kb, bol
        self.end_t = None
        self.grp_n = 0
        self.extra_files = []

    def at(self, t, *lines):
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                self.ticks[t].extend(x for x in ln if x)
            elif ln:
                self.ticks[t].append(ln)

    def rng(self, t0, t1, cmd):
        if t1 >= t0 and cmd:
            self.ranges.append((t0, t1, cmd))

    def track(self, t0, t1, deg=10):
        """Turn toward the player by at most deg per tick on pattern ticks t0..t1."""
        self.rng(max(1, t0), t1, f'function rlk:mboss/mv/turn {{max:{int(deg)}}}')

    def advance(self, t0, t1, d, unless_within):
        """Step d blocks forward per tick on t0..t1 while the player is farther than unless_within (mv/step: mv/ok)."""
        self.rng(max(1, t0), t1, f'execute at @s unless entity {PLAYER[:-1]},distance=..{num(unless_within, 2)}] '
                                 f'run function rlk:mboss/mv/step {{d:{num(d, 3)}}}')

    def group(self, t):
        """A new volley group at tick t (before the hazards of one strike: one hit per group)."""
        self.at(t, L.GRP_NEW)
        self.grp_n += 1
        return self.grp_n

    def hit(self, idx, tell_from, grp=0, kb=None, **kw):
        """The api.HITS[key][idx] hazard: made at its event tick - 1 (tell 1). tell_from = the first visible motion of
        this hit (tests: event - tell_from >= TELL_MIN / TELL_BIG)."""
        h = api.HITS[self.key][idx]
        t = api.ev(h[0], h[1])
        assert t >= 1 and tell_from <= t
        self.at(t - 1, hazard(self.key, h, grp=bool(grp), kb=kb, **kw))
        if h[5]:
            self.at(t, bol_mark())
        self.hits.append(dict(t=t, idx=idx, tell=tell_from, grp=grp, kb=kb or 0, bol=h[5], shape=h[2]))
        return t

    def end(self, t):
        self.end_t = t
        self.at(t, sset('#done', 1))

    def write(self, start_head=()):
        key, W = self.key, self.W
        assert self.end_t is not None, key
        name = api.PATTERN_NAMES[key]
        W.w(f'p/{key}/start', [f'# {key.upper()} {name} (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.',
                               sset('#done', 0)] + list(start_head) + self.ticks.get(0, []))
        tick = [f'# {key.upper()} {name}: one pattern tick (#pt kn = 1..{self.end_t}); events in k/<t>.']
        for t0, t1, cmd in self.ranges:
            rr = f'{t0}' if t0 == t1 else f'{t0}..{t1}'
            tick.append(gate(f'if score #pt {OBJ} matches {rr}', cmd))
        for t in sorted(k for k in self.ticks if k >= 1):
            lines = self.ticks[t]
            if len(lines) == 1 and not lines[0].startswith('$'):
                tick.append(gate(f'if score #pt {OBJ} matches {t}', lines[0]))
            else:
                W.w(f'p/{key}/k/{t}', [f'# {key.upper()} pattern tick {t}'] + lines)
                tick.append(f'execute if score #pt {OBJ} matches {t} run {fn(f"p/{key}/k/{t}")}')
        W.w(f'p/{key}/tick', tick)
        W.w(f'p/{key}/cancel', [f'# {key.upper()} cancel (any executor; idempotent): its hazards, markers and props, the body',
                                '# glide, the looks back to rest.',
                                f'kill @e[tag={tag_p(key)}]',
                                'kill @e[type=minecraft:marker,tag=rlk_kn_lock]', 'kill @e[type=minecraft:marker,tag=rlk_kn_dp]',
                                'kill @e[type=minecraft:marker,tag=rlk_mb_lock]',
                                f'execute as {BODY[:-1]},tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
                                f'execute as {BODY} at @s run {fn("core/looks_rest")}'] + self.cancel_lines)
