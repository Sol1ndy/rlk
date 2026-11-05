"""S3 helpers of the 홍련 (Scarlet) module generator (OWNER: S3; contract S:hr/contract.md §3): score / call shorthands,
the fake-player registry of the core (FP), the kit-or-stand-in sound / visual lines, the hazard lines from api.HITS, the
lock / probe helpers and the pattern builder PB used by p1.py (S4 may use it for p_ghost.py).

Importing has no side effects. Runtime conventions (contract §3.5, api.Pattern): @s = the body, at it; #pt hr = the
pattern clock (0 in p/<key>/start, +1 before each p/<key>/tick); the shown clip tick == #pt (the core calls rig/tick
after the pattern). A hit of clip event e is a quiet hazard created at #pt e - 1 with tell 1 (hz/init sets mbHzT -1), so
it strikes on the game tick of #pt e; its aim is the body yaw at creation (the pattern stops turning api.LOCK_LEAD ticks
before every hit). Hazards and markers of a pattern carry rlk_hr_p + rlk_hr_p_<key>; p/<key>/cancel kills them.
"""
from collections import defaultdict

from . import api

L, K = api.L, api.K
NS, OBJ, CY = api.NS, api.OBJ, api.CY
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'                 # the player's body (the avatar in F5 / shoulder view): hit / aim point
PL = '@a[tag=player,limit=1]'                       # the player entity (scores: dashInvT, rnDie, curHealth, ...)
ARENA_M = '@e[type=minecraft:marker,tag=rlk_mb_arena,limit=1]'
LOCK_T = api.TAGS['lock']
LOCK_M = f'@e[type=minecraft:marker,tag={LOCK_T},limit=1]'
PROBE_T = api.TAGS['probe']
PROBE_M = f'@e[type=minecraft:marker,tag={PROBE_T},limit=1]'
ANCHOR_M = f'@e[type=minecraft:marker,tag={api.TAGS["anchor"]},limit=1]'
AT_BODY = 'at @s rotated as @s rotated ~ 0'
LOCK = api.LOCK_LEAD


# ------------------------------------------------------------------------------------------------- ids
def _tid():
    """key -> #pat id: the P1 / P2 keys at their test id (api.TEST_IDS), the gauntlets at their 'now' test (21 / 27)."""
    t = {v: k for k, v in api.TEST_IDS.items() if v in api.P1 + api.P2}
    for g in api.GAUNTLETS:
        t[g] = next(k for k, v in api.TEST_IDS.items() if v.startswith(f'{g} now'))
    assert sorted(t) == sorted(api.P1 + api.P2) and len(set(t.values())) == len(t), t
    return t


TID = _tid()                                   # a1 1 a2 2 a3 3 a4 4 a6 5 a9 6 a10 7 r1 11 r2 12 r3 13 a8 21 a13 27
KEY_OF = {v: k for k, v in TID.items()}
SEQ_ID = {n: i + 1 for i, n in enumerate(api.SEQS)}   # #sqn hr: the running sequence (0 none)
GK = {'a8': 1, 'a13': 2}                       # #gk hr: the current / pending gauntlet
AT_OF = {'a8': 60, 'a13': 5}                   # repel {at} of each gauntlet's counter cinematic


# ------------------------------------------------------------------------------------------------- the core's fake players
# Every fake player of objective hr that S3 writes (api.CORE_FP + the S3 extras below). cleanup resets exactly these (never
# api.EV_FP: the reward hook reads them after cleanup); the generator checks every '#name hr' S3 writes is listed here.
# I1 (request s3-5): the S3 extras live in the contract now (api.CORE_FP, same order; api.CORE_CONSTS).
CONSTS = api.CORE_CONSTS
FP_EXTRA = ()
FP_PATTERN_PREFIXES = tuple(f'#{k}_' for k in api.P1)       # p1.py's own pattern scores (#<key>_<x>)
FP = tuple(api.CORE_FP) + tuple(FP_EXTRA)
assert len(FP) == len(set(FP)), 'duplicate fake player'
assert not set(FP) & set(api.EV_FP)


def fn(rel):
    return f'function {NS}{rel}'


def sset(name, v):
    return f'scoreboard players set {name} {OBJ} {int(v)}'


def sop(a, op, b, obj_b=OBJ):
    return f'scoreboard players operation {a} {OBJ} {op} {b} {obj_b}'


def gate(cond, cmd):
    """`execute <cond> run <cmd>`, merged into cmd's own execute chain when it has one."""
    return f'execute {cond} {cmd[8:]}' if cmd.startswith('execute ') else f'execute {cond} run {cmd}'


def tag_p(key):
    return f'rlk_hr_p_{key}'


def tags_nbt(*tags):
    return '[' + ','.join(f'"{t}"' for t in ('rlk_room', 'rlk_mb_aux') + tags) + ']'


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


def pm_of(dst, src_sel, src_obj, pm, dst_obj=OBJ):
    """dst = src x pm / 1000 (pm 0..1000; multiply first up to 2 000 000, divide first above: no int32 overflow), >= 1."""
    assert 0 <= int(pm) <= 1000
    d = f'{dst} {dst_obj}'
    return [f'scoreboard players operation {d} = {src_sel} {src_obj}',
            sset('#t5', pm), sset('#t4', 0),
            f'execute if score {d} matches ..2000000 run {sset("#t4", 1)}',
            f'execute if score #t4 {OBJ} matches 1 run scoreboard players operation {d} *= #t5 {OBJ}',
            f'scoreboard players operation {d} /= #c1000 {OBJ}',
            f'execute if score #t4 {OBJ} matches 0 run scoreboard players operation {d} *= #t5 {OBJ}',
            f'execute if score {d} matches ..0 run scoreboard players set {d} 1']


# ------------------------------------------------------------------------------------------------- sounds / visuals
def snd(name, pos='at @s'):
    """The kit sound recipe at pos, or while the kit is missing its vanilla layers (api.KIT_SOUND_RECIPES: the plan's
    events / volumes / pitches, mboss_lib.sound's min-volume rule)."""
    k = K.snd(name)
    if k:
        return placed([k], pos)
    return placed([L.sound(e, v, p) for e, v, p in api.KIT_SOUND_RECIPES[name]], pos)


# Vanilla stand-in particles while the kit (S1K) is missing: the lilac sword-qi, the yellow tell, the white glint.
DUST = {'lilac': 'minecraft:dust{color:[0.79,0.49,0.87],scale:1.2}', 'magenta': 'minecraft:dust{color:[0.88,0.25,0.62],scale:1.2}',
        'yellow': 'minecraft:dust{color:[1.0,0.88,0.29],scale:1.6}', 'white': 'minecraft:dust{color:[1.0,0.95,0.98],scale:1.0}',
        'crimson': 'minecraft:dust{color:[0.91,0.27,0.42],scale:1.4}'}
C_DUST = {api.C_LILAC: 'lilac', api.C_MAGENTA: 'magenta', api.C_YELLOW: 'yellow', api.C_CRIMSON: 'crimson',
          api.C_WHITE: 'white'}


def part(p, dx, dy, dz, spd, n):
    return f'particle {p} ~ ~ ~ {num(dx, 2)} {num(dy, 2)} {num(dz, 2)} {num(spd, 3)} {int(n)} force @a[tag=player]'


def fx_lines(name, fallback=(), **a):
    """The kit preset line fx/p/<name> {a} (unplaced), else the fallback lines (vanilla particles; none = nothing)."""
    k = K.p(name, **a)
    return [k] if k else list(fallback)


def fx(name, fallback=(), pos=None, **a):
    """The kit preset fx/p/<name> {a} at pos (execute subcommands; default: the body, 1.3 b up, rotated as it), else the
    fallback lines there."""
    return placed(fx_lines(name, fallback, **a), pos or f'{AT_BODY} positioned ~ ~1.3 ~')


def fx_arc(r, c=api.C_LILAC, yaw=0, pitch=0, roll=0, h=1.3):
    """A sword-qi crescent (kit qi_arc {r,yaw,pitch,roll,c}, r in blocks; the kit args are offsets from the executor,
    which is rotated as the body), else a lilac dust fan at the reach."""
    return fx('qi_arc', [part(DUST[C_DUST.get(c, 'lilac')], r * 0.35, 0.25, r * 0.35, 0, 18),
                         part('minecraft:sweep_attack', r * 0.25, 0.1, r * 0.25, 0, 2)],
              pos=f'{AT_BODY} positioned ~ ~{num(h, 2)} ~', r=int(round(r * 10)), yaw=int(yaw), pitch=int(pitch),
              roll=int(roll), c=int(c))


def hud(name, **a):
    k = K.hud(name, **a)
    return [k] if k else []


def line(lid):
    """Her typed line api.LINES[lid] through the kit (fx/hud/line {id}; contract §2: shown only through the kit)."""
    return hud('line', id=lid)


# ------------------------------------------------------------------------------------------------- hazards
SHAPE_FN = {'sector': L.hz_sector, 'disc': L.hz_disc, 'line': L.hz_line}


def hz_tag(key):
    """Tag the hazard just made (#hzLast) rlk_hr_p + rlk_hr_p_<key> (core/hz_tag/<key>; the pattern's cancel kills it)."""
    return (f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run '
            f'function {NS}core/hz_tag/{key}')


def hz_opts(kb, grp=False, act=None):
    """The one-shot options of every hazard of 홍련: quiet (#hzQuiet 1, no framework outline or flash: no floor decal of
    any kind, PLAN §1.4), no framework sound (the kit / stand-in sounds are the pattern's), Electro (el 3), knockback."""
    return L.hz_opts(quiet=1, sfx=0, grp=grp, kb=kb, el=api.ELEC, act=act)


def hazard(key, hit, grp=False, tell=1, pos=None, dims=None):
    """Lines that create the quiet hazard of api.HITS entry `hit`, striking `tell` ticks later. pos: execute
    subcommands for the origin (default: the body on the floor, aim = body yaw); dims: shape args override."""
    clip, event, shape, hdims, tier, kb = hit
    dims = dims or hdims
    if shape == 'pdisc':
        shape = 'disc'
    out = hz_opts(kb, grp=grp)
    call = SHAPE_FN[shape](*dims, tell, api.DMG[tier])
    where = pos or f'{AT_BODY} positioned ~ {CY} ~'
    out.append(f'execute {where} run {call}')
    out.append(hz_tag(key))
    return out


# ------------------------------------------------------------------------------------------------- pattern builder
class PB:
    """Collects the commands of one pattern by pattern tick and writes p/<key>/{start,tick,cancel,k/<t>}; records every
    hit (event tick, HITS index, the first visible motion, volley group, kb) for the tests (p1.TABLE)."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.ticks = defaultdict(list)
        self.ranges = []                    # (t0, t1, command)
        self.cancel_lines = []
        self.hits = []
        self.end_t = None
        self.grp_n = 0
        self.motions = []                   # (t0, t1, kind) of the body moves (tests)

    def at(self, t, *lines):
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                self.ticks[t].extend(x for x in ln if x)
            elif ln:
                self.ticks[t].append(ln)

    def rng(self, t0, t1, cmd):
        if t1 >= t0 and cmd:
            self.ranges.append((t0, t1, cmd))

    def track(self, t0, t1, deg=api.TRACK['deg']):
        """Turn toward the player by at most deg per tick on pattern ticks t0..t1."""
        self.rng(max(1, t0), t1, f'function rlk:mboss/mv/turn {{max:{int(deg)}}}')

    def advance(self, t0, t1, d=api.TRACK['step'], stop=api.TRACK['min']):
        """Step d blocks forward per tick on t0..t1 while the player is farther than stop (mv/step: mv/ok-checked)."""
        self.rng(max(1, t0), t1, f'execute at @s unless entity {PLAYER[:-1]},distance=..{num(stop, 2)}] '
                                 f'run function rlk:mboss/mv/step {{d:{num(d, 3)}}}')
        self.motions.append((max(1, t0), t1, 'step'))

    def group(self, t):
        """A new volley group at tick t (before the hazards of one strike: one hit per group)."""
        self.at(t, L.GRP_NEW)
        self.grp_n += 1
        return self.grp_n

    def hit(self, idx, tell_from, grp=0, **kw):
        """The api.HITS[key][idx] hazard: made at its event tick - 1 (tell 1). tell_from = the first visible motion of
        this hit (tests: event - tell_from >= TELL_MIN / TELL_BIG)."""
        h = api.HITS[self.key][idx]
        t = api.ev(h[0], h[1])
        assert t >= 1 and tell_from <= t
        self.at(t - 1, hazard(self.key, h, grp=bool(grp), **kw))
        self.hits.append(dict(t=t, idx=idx, tell=tell_from, grp=grp, kb=h[5], shape=h[2], tier=h[4], dims=h[3]))
        return t

    def end(self, t):
        self.end_t = t
        self.at(t, sset('#done', 1))

    def write(self, start_head=()):
        key, W = self.key, self.W
        assert self.end_t is not None, key
        name = api.PATTERN_NAMES[key]
        W.w(f'p/{key}/start', [f'# {key.upper()} {name} (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.',
                               sset('#done', 0)] + list(start_head) + self.ticks.get(0, []))
        tick = [f'# {key.upper()} {name}: one pattern tick (#pt hr = 1..{self.end_t}); events in k/<t>.']
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
        W.w(f'p/{key}/cancel', [f'# {key.upper()} cancel (any executor; idempotent): its hazards and markers, the body glide, the',
                                '# body back on the floor when airborne, the stance.',
                                f'kill @e[tag={tag_p(key)}]',
                                f'execute as {BODY[:-1]},tag=rlk_mb_mv] run function rlk:mboss/mv/stop'] + self.cancel_lines)
