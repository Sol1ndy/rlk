"""P2's entries and the gauntlets of 홍련 on the new combat (hr_design §2.2, §2.4; lane H1): MX 자광 십자참, NB 낙월 사선,
Q 자영 포박 · 천공 낙월 (P2 only) and the gauntlets G1 = A8 자영 연참 (60 %) / G2 = A13 필살 · 자영 연참 (5 %), with the
shared ghost helpers g/**. Written by tools/build_mboss_scarlet.py through api.Writer('S4', api.OWN['S4']) (outputs
F:boss/scarlet/p/{mx,nb,q,a8,a13}/** and F:boss/scarlet/g/**).

MX / NB / Q are built with s3lib.PB like the P1 kit (api.HITS rows, the parry cue of every P hit, the flashes of every N
hit). The gauntlets come from api.SCRIPTS (the rows: a clip's start on the pattern clock, the cut made at that step) and
api.ev (every effect / sound / move at its clip event); every cut through api.cut() (g/cut/make / aim / lock): a quiet,
parryable Electro disc of api.CUT_R that follows the player until its lock = strike - 7, where the parry cue plays (the
pink glint at her blade + its chime). The shield is the 5-segment gauge (shield.py): a cut whose hit is judged a perfect
parry takes one segment (the core's shield/tick after every gauntlet tick); a perfect dodge, a tier 2 / 1 parry or walking
out takes none.

Runtime (api.Pattern; @s = the body, at it; clock #pt hr = played ticks since start; the shown clip tick == #pt):
- p/<key>/start (tick 0), p/<key>/tick -> the 16-tick block p/<key>/b/<i> -> the tick file p/<key>/k/<t> (gauntlets),
  p/<key>/cancel (any executor, idempotent). #done hr 1 on the last tick: G1 at JUDGE_T 220 with a deflect (the core
  starts seq/repel in that tick) or FAIL60_P2_T 240 after the fail; G2 at 242 with a deflect, 254 after a survived fail.
- Spots g/spot/<name> (@s = the body): a marker rlk_hr_gsp at the first candidate passing mv/ok (inside MOVE_R 22.5, feet
  and head free), the candidates relative to the player's facing (api.REAPPEAR), else the guaranteed fallback: the point
  on the player -> C line at the move's distance (<= FALLBACK_R from C), walked toward the axis until mv/ok passes.
- The ghost: rlk_hr_ghost on the body + the rig look form/ghost from the lilac switch (T0); the core keeps rlk_mb_inv
  then; off at the dive's reappearance (form normal, A8.9). Q's grab: ghost 4-20.
- The gauntlet frame: the judge at api.JUDGE_T calls shield/judge; the warning banner goes. Gauge 0: #done in the same
  tick (the repel's first frames are the gold deflect; g_deflect is no longer played). Fail by the gauntlet's switch: not
  lethal (G1 by default) = ult/fail60 at the player's floor spot, she lands on the impact point, g_reform, #done at
  FAIL60_P2_T; lethal (G2 by default) = the black overlay 3 t before the judge when segments are left, at the judge the
  pink-white overlay + scarlet_line + petal_burst + the slash sound + ult/fatal as the player, she lands 2 b in front.
- Cancel (pause / reload / death / cleanup / tests): every entity of the pattern (rlk_hr_p_<key>, rlk_hr_cut, the spot
  marker), the body back to normal (ghost tag off, form normal, blade off, visible, no glide, on the floor); a gauntlet
  also turns the banner off. Never #ph, the gauge or the bars. The field stays crimson: no dark look is requested.

TABLE[key] = the recorded hits and EVENTS[key] = (tick, kind, name, source) of every effect / sound / rig call of a
gauntlet for the tests (pat_ghost.py) and renders; MOVES[key] = the body moves; CUES[key] the parry cue ticks.
"""
import math
from collections import defaultdict

from . import api
from . import s3lib as S
from .s3lib import PB, sset, fn, part, placed
from . import blade as B

L, K = api.L, api.K
E = api.ev
OBJ, NS, CY = api.OBJ, api.NS, api.CY
BODY, PLAYER, PL, ARENA_M = S.BODY, S.PLAYER, S.PL, S.ARENA_M
OK = 'function rlk:mboss/mv/ok'
FACE = 'function rlk:mboss/mv/face'
STOP = 'function rlk:mboss/mv/stop'
TAG_P, TAG_CUT, TAG_GHOST = api.TAGS['pat'], api.TAGS['cut'], api.TAGS['ghost']
CNT_T = 'rlk_hr_cnt'                 # the hazard marker of a counting cut
SPOT_T = 'rlk_hr_gsp'                # the transient spot marker of g/spot/<name>
FACE_LOCK = f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0'   # she faces the lock marker
SPOT_M = f'@e[type=minecraft:marker,tag={SPOT_T},limit=1]'
SPOT_ALL = f'@e[type=minecraft:marker,tag={SPOT_T}]'
KILL_SPOT = f'kill {SPOT_ALL}'
BLOCK = 16                           # ticks per dispatch block of p/<key>/tick
FIRST_PERSON, AVATAR = 'if entity @a[tag=rlk_body]', 'unless entity @a[tag=rlk_body]'   # F2 (HR-45): no avatar = first person
DUST = S.DUST
GAUNT = api.GAUNTLETS
TABLE, EVENTS, MOVES, CUES, FLASHES, PPW = {}, {}, {}, {}, {}, {}


def num(v, nd=3):
    return L.num(v, nd)


def cut_sel(s):
    return f'@e[type=minecraft:marker,tag={TAG_CUT},scores={{{OBJ}={int(s)}}},limit=1]'


def at_cut(s, h=0.0):
    """Execute subcommands: at the cut of strike s (its lock point, on the floor), rotated as the player's facing."""
    up = f' positioned ~ ~{num(h, 2)} ~' if h else ''
    return f'at {cut_sel(s)} rotated as {PL} rotated ~ 0{up}'


def at_player(h=0.0):
    up = f' positioned ~ ~{num(h, 2)} ~' if h else ''
    return f'at {PLAYER} rotated as {PL} rotated ~ 0 positioned ~ {CY} ~{up}'


def at_body(h=0.95):
    return f'{S.AT_BODY} positioned ~ ~{num(h, 2)} ~'


def ring_fb(r, c='lilac', n=None):
    """Vanilla stand-in of a flat sword-qi ring of radius r (while the kit is missing)."""
    return [part(DUST[c], r * 0.55, 0.05, r * 0.55, 0, n or int(10 + 6 * r)), part('minecraft:sweep_attack', r * 0.4, 0.05, r * 0.4, 0, 3)]


def puff_fb(c='lilac', n=16):
    return [part(DUST[c], 0.35, 0.7, 0.35, 0.02, n), part('minecraft:end_rod', 0.25, 0.6, 0.25, 0.04, 4)]


# ================================================================================================= the shared helpers g/**
# Spot candidates (PLAN §4.1 movement safety, §4.5 approaches; api.REAPPEAR): (basis, yaw offset deg, distance b).
# Bases (all on the floor): 'face' = the player's spot rotated as the player's facing (+ = right); 'tobody' = from the
# player toward her; 'frombody' = beyond the player, away from her; 'away' = from her, away from the player. The tail is
# the guaranteed fallback's distance along the player -> C line (None: her own spot).
RE = api.REAPPEAR
_D1F = RE['D1']['fallback_dist']
SPOTS = {
    'd1': ([('face', RE['D1']['bearing'], RE['D1']['dist'])] + [('face', b, _D1F) for b in RE['D1']['fallback']],
           RE['D1']['dist'], 'D1 far reappear: 14 b at -40 (front-left); else +40 / 0 / +-90 at 10 b'),
    'side': ([('face', RE['D1']['end'][1], RE['D1']['end'][0]), ('face', -RE['D1']['end'][1], RE['D1']['end'][0]),
              ('face', 0, RE['D1']['end'][0]), ('face', 180, RE['D1']['end'][0])], RE['D1']['end'][0],
             'the station at the player\'s right (1.5 b at +90): the D1 dash end, the chain cuts, the D3 / D4 landings'),
    'd2': ([('face', RE['D2']['bearing'], RE['D2']['dist']), ('face', -RE['D2']['bearing'], RE['D2']['dist']),
            ('face', 0, RE['D2']['dist']), ('face', RE['D2']['bearing'], 6.0), ('face', -RE['D2']['bearing'], 6.0)],
           RE['D2']['dist'], f"D2 side reappear: {num(RE['D2']['dist'])} b at {RE['D2']['bearing']:+d} (low, the player's front-right); "
           f"else {-RE['D2']['bearing']:+d} / 0 / +-{abs(RE['D2']['bearing'])} at 6 b"),
    'd2e': ([('face', RE['D2']['end'][1], RE['D2']['end'][0]), ('face', -RE['D2']['end'][1], RE['D2']['end'][0]),
             ('face', 0, RE['D2']['end'][0])], RE['D2']['end'][0], 'the D2 glide stop: 1.6 b at +45 (front-right)'),
    'd3': ([('face', RE['D3']['bearing'], RE['D3']['dist']), ('face', -RE['D3']['bearing'], RE['D3']['dist']),
            ('face', 0, RE['D3']['dist'])], RE['D3']['dist'], 'D3 blink: 2.5 b at +60 (up-right; the caller adds 3 b up)'),
    'd4': ([('face', RE['D4']['bearing'], RE['D4']['dist']), ('face', -RE['D4']['bearing'], RE['D4']['dist']),
            ('face', 0, RE['D4']['dist']), ('face', RE['D4']['bearing'], 8.0), ('face', -RE['D4']['bearing'], 8.0)],
           RE['D4']['dist'], f"D4 far reappear: {num(RE['D4']['dist'])} b at {RE['D4']['bearing']:+d} (the player's front-left); "
           f"else {-RE['D4']['bearing']:+d} / 0 / +-{abs(RE['D4']['bearing'])} at 8 b"),
    # round V (v_brief §3 VB 4): never on the player's own spot (the F5 lens ended up inside her): 1.3 b before them
    'over': ([('face', 0, 1.3), ('face', 90, 1.3), ('face', -90, 1.3)], 1.5,
             '1.3 b in front of the player (the A8.3 leap adds the height)'),
    'dv': ([('face', 0, 4.5), ('face', 30, 4.5), ('face', -30, 4.5), ('face', 0, 3.0)], 3.0,
           'the A8.9 dive\'s reappearance: 4.5 b in front of the player (the caller adds DIVE_UP): in the F5 view, the whole wind-up'),
    'land': ([('face', 0, 2.0), ('face', 90, 2.0), ('face', -90, 2.0)], 2.0,
             'the A13 fail landing 2 b in front of the player (she dove from straight above them: not toward her)'),
}


def _origin(basis, a):
    if basis == 'face':
        return f'at {PLAYER} positioned ~ {CY} ~ rotated as {PL} rotated ~{num(a, 1)} 0'
    if basis == 'tobody':
        return f'at {PLAYER} positioned ~ {CY} ~ facing entity @s feet rotated ~{num(a, 1)} 0'
    if basis == 'frombody':
        return f'at {PLAYER} positioned ~ {CY} ~ facing entity @s feet rotated ~{num(180 + a, 1)} 0'
    if basis == 'away':
        return f'at @s positioned ~ {CY} ~ facing entity {PLAYER} feet rotated ~{num(180 + a, 1)} 0'
    raise ValueError(basis)


def spot_files(W):
    w = W.w
    put = fn('g/spot/put')
    w('g/spot/put', ['# The spot marker here (on the floor; a g/spot/<name> found it).',
                     f'summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(TAG_P, SPOT_T)}}}'])
    w('g/spot/clamp', [
        '# @s = the spot marker on the floor: 0.5 b toward the arena axis until mv/ok passes (at most 60 steps, then the axis',
        '# C itself): the guaranteed fallback never stands in a block or outside MOVE_R.',
        f'execute if function {OK[9:]} run return 1',
        f'scoreboard players add #g_c {OBJ} 1',
        f'execute if score #g_c {OBJ} matches 60.. at {ARENA_M} positioned ~ {CY} ~ run return run tp @s ~ ~ ~',
        f'execute facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
        f'execute at @s run {fn("g/spot/clamp")}'])
    for name, (cands, tail, what) in SPOTS.items():
        lines = [f'# Spot {name} (@s = the body): {what}. The first candidate passing mv/ok (MOVE_R {num(api.MOVE_R, 1)}, feet and head',
                 '# free) gets the marker rlk_hr_gsp; ' + ('else her own spot' if tail is None else
                                                            f'else the guaranteed fallback {num(tail, 1)} b from the player toward C (at most {num(api.FALLBACK_R, 0)} b from C)')
                 + ', walked toward the axis until mv/ok passes.', KILL_SPOT]
        for basis, a, d in cands:
            lines.append(f'execute {_origin(basis, a)} positioned ^ ^ ^{num(d, 2)} if function {OK[9:]} run return run {put}')
        if tail is None:
            lines.append(f'execute at @s positioned ~ {CY} ~ run {put}')
        else:
            lines.append(f'execute at {PLAYER} positioned ~ {CY} ~ facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^{num(tail, 2)} '
                         f'run {put}')
            # a player near the rim: the point lies farther than FALLBACK_R from C -> the same line at FALLBACK_R from C
            lines.append(f'execute as {SPOT_M} at @s unless entity {ARENA_M[:-1].replace(",limit=1", "")},distance=..{num(api.FALLBACK_R, 1)}] '
                         f'at {ARENA_M} positioned ~ {CY} ~ facing entity {PLAYER} feet rotated ~ 0 positioned ^ ^ ^{num(api.FALLBACK_R, 1)} '
                         f'run tp @s ~ ~ ~')
        lines += [sset('#g_c', 0), f'execute as {SPOT_M} at @s run {fn("g/spot/clamp")}']
        w(f'g/spot/{name}', lines)


def cut_files(W):
    w = W.w
    r = int(round(api.CUT_R * 10))
    w('g/cut/make', [
        '# {s,t,dmg,kb,n} (api.cut; @s = the pattern\'s executor = the body): a ghost cut (PLAN §5.3) = a quiet Electro disc hazard',
        f'# of radius CUT_R {num(api.CUT_R, 1)} b at the player\'s feet on the floor, striking t ticks later (at pattern tick s), active 2 t,',
        '# dmg % of the base hit, knockback kb along her -> the player (kbdir 1, the marker\'s yaw); no outline, flash or decal;',
        '# parryable (#hzNoParry 0): a perfect parry of it takes one gauge segment (shield/tick).',
        '# g/cut/tag stamps it (objective hr = s, rlk_hr_cut, the pattern tags, rlk_hr_cnt when it counts: n 1).',
        f'$scoreboard players set #g_s {OBJ} $(s)', f'$scoreboard players set #g_n {OBJ} $(n)']
      + L.hz_opts(quiet=1, sfx=0, el=api.ELEC, act=2, kbdir=1, noparry=0)
      + ['$scoreboard players set #hzKB mb $(kb)',
         f'$execute at {PLAYER} positioned ~ {CY} ~ facing entity @s feet rotated ~180 0 run function rlk:mboss/hz/disc '
         f'{{r:{r},tell:$(t),dmg:$(dmg)}}',
         f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run {fn("g/cut/tag")}'])
    tag = ['# @s = the cut hazard just made: its strike tick (objective hr), the cut + pattern tags of the running pattern (#pat),',
           '# rlk_hr_cnt for a counting cut (the gauntlets).',
           f'scoreboard players operation @s {OBJ} = #g_s {OBJ}', f'tag @s add {TAG_CUT}', f'tag @s add {TAG_P}',
           f'execute if score #g_n {OBJ} matches 1 run tag @s add {CNT_T}']
    for k in api.P2:
        tag.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run tag @s add {S.tag_p(k)}')
    w('g/cut/tag', tag)
    w('g/cut/aim', [
        '# {s}: the cut of strike s on the player again (its marker to the player\'s floor spot, yaw her -> the player; the',
        '# framework\'s hz/aim recomputes its axis: this tick\'s hit test uses it). Until the lock (strike - LOCK_LEAD).',
        f'$execute at {PLAYER} positioned ~ {CY} ~ facing entity {BODY} feet rotated ~180 0 as @e[type=minecraft:marker,tag={TAG_CUT},'
        f'scores={{{OBJ}=$(s)}}] run {L.hz_aim()}'])
    w('g/cut/lock', [
        f'# {{s}}: the lock of the cut of strike s (strike - LOCK_LEAD {api.LOCK_LEAD}): the last aim; from now on it stays (the',
        '# parry cue of the cut plays in this tick: the pattern\'s own line).',
        f'$function {NS}g/cut/aim {{s:$(s)}}'])


def body_files(W):
    w = W.w
    w('g/ground', ['# @s = the body: back on the floor at once if airborne (a cancelled leap / hang): the spot below when mv/ok, else C.',
                   f'execute if entity @s[tag=rlk_mb_mv] run {STOP}',
                   f'execute store result score #g_y {OBJ} run data get entity @s Pos[1] 100',
                   f'execute if score #g_y {OBJ} matches ..{CY * 100 + 4} run return 0',
                   f'execute at @s positioned ~ {CY} ~ if function {OK[9:]} run return run tp @s ~ ~ ~',
                   f'execute at {ARENA_M} positioned ~ {CY} ~ run tp @s ~ ~ ~'])
    w('g/reset', ['# @s = the body (a cancelled ghost pattern): solid and visible in her normal colours, the blade glow off, no glide,',
                  '# on the floor. Idempotent.',
                  f'tag @s remove {TAG_GHOST}', api.rig('look/form/normal'), api.rig('look/blade/off'), api.rig('state/normal'),
                  fn('g/ground')])
    w('g/bolt', [f'# A decoration bolt here (@s any; the floor spot 3-6 b from the player): no hit box (PLAN §4.5, questions.md Q-A12).']
      + S.fx('deco_bolt', [part(DUST['yellow'], 0.05, 1.6, 0.05, 0, 14), part('minecraft:electric_spark', 0.1, 1.2, 0.1, 0.05, 6)],
             pos='positioned ~ ~ ~')
      + S.snd('deco_bolt', pos='positioned ~ ~ ~'))


_G_DONE = set()


def g_files(W):
    """g/** once per Writer (every pattern build calls it; the files are the same)."""
    if id(W) in _G_DONE:
        return
    _G_DONE.add(id(W))
    cut_files(W)
    spot_files(W)
    body_files(W)


# ================================================================================================= the pattern builder
class GB:
    """Collects the commands of one pattern by pattern tick and writes p/<key>/{start,tick,cancel}, the 16-tick blocks
    b/<i> and the tick files k/<t>; records the hits (TABLE), the effect / sound / rig events (EVENTS) and the moves."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.ticks = defaultdict(list)
        self.hits, self.events, self.moves, self.cues = [], [], [], []
        self.start_head, self.cancel_lines = [], []
        self.end_t = None

    def at(self, t, *lines):
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                self.ticks[t].extend(x for x in ln if x)
            elif ln:
                self.ticks[t].append(ln)

    def rng(self, t0, t1, *lines):
        for t in range(t0, t1 + 1):
            self.at(t, *lines)

    def ev(self, t, kind, name, src=None):
        self.events.append((t, kind, name, src))

    def fx(self, tick, name, fallback, pos, src=None, **a):
        self.at(tick, S.fx(name, fallback, pos=pos, **a))
        self.ev(tick, 'fx', name, src)

    def snd(self, t, name, pos='at @s', src=None):
        self.at(t, S.snd(name, pos=pos))
        self.ev(t, 'snd', name, src)

    def play(self, t, clip):
        self.at(t, api.play(clip))
        self.ev(t, 'clip', clip, (clip, 0))

    def look(self, t, ch, v, src=None):
        self.at(t, api.rig(f'look/{ch}/{v}'))
        self.ev(t, 'look', f'{ch}/{v}', src)

    def cut(self, c, count, step):
        made, lock, strike, tier, kb = c
        for t, ln in api.cut(made, lock, strike, tier, kb, count):
            self.at(t, ln)
        # the parry cue at the lock tick (hr_design §2.4): the pink glint at her blade + its chime
        self.at(lock, S.cue())
        self.ev(lock, 'cue', 'parry', ('cut', strike))
        self.cues.append(lock)
        self.hits.append(dict(kind='cut', t=strike, made=made, lock=lock, tier=tier, kb=kb, n=count, step=step,
                              shape='pdisc', dims=(api.CUT_R,), dmg=api.DMG[tier], tell=made, parry='P', cue=lock))

    def end(self, t, cond=None):
        if self.end_t is None or t > self.end_t:
            self.end_t = t
        self.at(t, S.gate(cond, sset('#done', 1)) if cond else sset('#done', 1))

    def write(self, title):
        key, W = self.key, self.W
        assert self.end_t is not None, key
        name = api.PATTERN_NAMES[key]
        W.w(f'p/{key}/start', [f'# {key.upper()} {name} ({title}; S4, p_ghost.py): pattern tick 0 (@s = the body, at it; clock #pt hr).',
                               sset('#done', 0)] + self.start_head + self.ticks.get(0, []))
        ts = sorted(t for t in self.ticks if t >= 1)
        assert ts and ts[-1] <= self.end_t, (key, ts[-1:], self.end_t)
        blocks = defaultdict(list)
        for t in ts:
            W.w(f'p/{key}/k/{t}', [f'# {key.upper()} pattern tick {t}.'] + self.ticks[t])
            blocks[t // BLOCK].append(t)
        tick = [f'# {key.upper()} {name}: one pattern tick (#pt hr 1..{self.end_t}), dispatched by {BLOCK}-tick blocks to k/<t>.']
        for b in sorted(blocks):
            lo, hi = b * BLOCK, b * BLOCK + BLOCK - 1
            tick.append(f'execute if score #pt {OBJ} matches {lo}..{hi} run return run {fn(f"p/{key}/b/{b}")}')
            W.w(f'p/{key}/b/{b}', [f'# {key.upper()} ticks {lo}..{hi}.']
                + [f'execute if score #pt {OBJ} matches {t} run return run {fn(f"p/{key}/k/{t}")}' for t in blocks[b]])
        W.w(f'p/{key}/tick', tick)
        cancel = [f'# {key.upper()} cancel (pause / reload / death / cleanup / tests; any executor; idempotent): its hazards, cuts, discs and',
                  '# markers; the body solid, visible, normal colours, on the floor.' + (' The banner off, the darkness lifted.' if key in GAUNT else ''),
                  f'kill @e[tag={S.tag_p(key)}]', f'kill @e[type=minecraft:marker,tag={TAG_CUT}]', KILL_SPOT,
                  f'execute as {BODY} run {fn("g/reset")}'] + self.cancel_lines
        W.w(f'p/{key}/cancel', cancel)
        CUES[key] = sorted(self.cues)
        TABLE[key] = sorted(self.hits, key=lambda h: h['t'])
        EVENTS[key] = sorted(self.events, key=lambda e: e[0])
        MOVES[key] = self.moves


# ================================================================================================= moves (PLAN §4.5)
def spot(name):
    return fn(f'g/spot/{name}')


def up_pos(up):
    return f' positioned ~ ~{num(up, 2)} ~' if up else ''


def tp_spot(name, up=0.0):
    """The body to spot `name` (+ up) at once, facing the player (a reappearance)."""
    return [spot(name), STOP, f'execute positioned as {SPOT_M}{up_pos(up)} run tp @s ~ ~ ~', KILL_SPOT, FACE]


def glide_spot(name, t, up=0.0):
    return [spot(name), f'execute positioned as {SPOT_M}{up_pos(up)} run function rlk:mboss/mv/glide {{t:{int(t)}}}', KILL_SPOT]


def leap_spot(name, t, h, up=0.0):
    return [spot(name), f'execute positioned as {SPOT_M}{up_pos(up)} run function rlk:mboss/mv/leap {{t:{int(t)},h:{int(h)}}}',
            KILL_SPOT]


def rise(up, t):
    return [f'execute at @s positioned ~ ~{num(up, 2)} ~ run function rlk:mboss/mv/glide {{t:{int(t)}}}']


def hide():
    return [api.rig('state/hidden')]


# Round V (lane VB; v_brief §3 VB 2, 4): the station of a gauntlet cut = the place and the yaw she cuts from, fixed STATION_LEAD t
# before the strike (an approach: when she appears) as the marker rlk_hr_gst: the drawn blade path of the cut stands THERE from
# then on (in the player's view beside the avatar while she is still far away or unseen), she arrives on it and takes its yaw.
ST_T = 'rlk_hr_gst'
ST_M = f'@e[type=minecraft:marker,tag={ST_T},limit=1]'
AT_ST = f'at {ST_M} rotated as {ST_M}'
STATION_LEAD = 10


def station(name, up=0.0):
    """The station marker at spot `name` (+ up), facing the player (@s = the body)."""
    return [f'kill @e[type=minecraft:marker,tag={ST_T}]', spot(name),
            f'execute as {SPOT_M} at @s{up_pos(up)} facing entity {PLAYER} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
            f'tag {SPOT_M} add {ST_T}', f'tag {ST_M} remove {SPOT_T}']


def glide_st(t):
    return [f'execute positioned as {ST_M} run function rlk:mboss/mv/glide {{t:{int(t)}}}']


def face_st():
    return [f'execute rotated as {ST_M} run tp @s ~ ~ ~ ~ 0']


# each move's contact: its sound (round V: the sword-qi is the blade's own sweep, blade.py; the kit's hand-placed qi_ring / qi_band
# / qi_arc / qi_x / qi_dome / qi_vert at the cut spot are gone, review v S1)
CONTACT = {'A8.1': 'g_ring', 'A8.2': 'g_rise', 'A8.3': 'g_leap_cut', 'A8.4': 'g_sweep', 'A8.5': 'g_x', 'A8.6': 'g_wrap',
           'A8.7': 'g_dome', 'A8.8': 'g_vert'}
# the spot a move cuts from (the station; g/spot/<name>) and its height
ST_SPOT = {'A8.3': ('over', 2.5)}
APPROACH_END = {'D1': 'side', 'D2': 'd2e', 'D3': 'side', 'D4': 'side'}
APPROACH = ('D1', 'D2', 'D3', 'D4')
TRAIL = {'D1': 125, 'D2': 65, 'D4': 105}          # ghost_trail len (tenths): the nominal dash / glide / run lengths
HANG_UP, HANG_T = 3.0, 3                          # A8.4: she springs straight up and hangs (PLAN §4.5)
RISE_UP = 8.0                                     # A8.8: she rises 8 b up and out of view
LEAP_UP, LEAP_T, LEAP_H = 2.5, 6, 30              # A8.3: mv/leap {t:6,h:30} over the player (gauntlets: to 2.5 b above them)
DIVE_UP, DIVE_STOP = RE['A8.9']['up'], 1.0        # A8.9: DIVE_UP above the spot `dv` (in view), the dive to 1 b above the spot `land`
RESTATION_T, DROP_T = 3, 2                        # the chain cuts' small glide to the station; A8.5's drop from the hang
LAND_T = 2                                        # the fail: her landing from 1 b above the player (A8: on the impact point;
#                                                   the lethal fail: 2 b in front of the player)
# Decoration bolts (api.BOLTS): (bearing relative to the player's facing, distance 3-6 b) per bolt
BOLT_AT = ((-60, 3.6), (75, 4.4), (-130, 5.2), (150, 5.8))
EXTRA_VANISH = api.EXTRA_VANISH                    # g_ring does not end vanished: the vanish before D2's reappearance
FAIL_END = 12                                     # G2: #done this long after a survived fail (-> the revive stance)


class Walk:
    """Builds one scripted pattern from its api.SCRIPTS rows (t >= 0)."""

    def __init__(self, key, W):
        self.key = key
        self.gb = GB(key, W)
        self.rows = [r for r in api.SCRIPTS[key] if r[0] >= 0]
        self.clip_rows = [r for r in self.rows if r[2]]
        self.strikes = {r[3][2]: r for r in self.rows if r[3]}
        self.gauntlet = key in GAUNT

    # ------------------------------------------------------------------ helpers
    def next_clip_t(self, t):
        later = [r[0] for r in self.clip_rows if r[0] > t]
        return min(later) if later else None

    def prev_step(self, t):
        prev = [r for r in self.clip_rows if r[0] < t]
        return prev[-1][1] if prev else None

    def ends_vanished(self, t, clip, gone, burst=True):
        """The clip (started at t) ends vanished (S2a: g_tell 4, g_x 14, g_leap 17, g_vert 18): its 'gone' effect and
        state/hidden at its end, unless the next clip starts first (play replaces the running clip)."""
        g = self.gb
        nxt = self.next_clip_t(t)
        tg, te = t + E(clip, gone), t + E(clip, 'end')
        if burst and (nxt is None or nxt > tg):
            g.fx(tg, 'ghost_burst', puff_fb(), at_body(0.95), src=(clip, gone))
        if nxt is None or nxt > te:
            g.at(te, hide())
            g.ev(te, 'rig', 'state/hidden', (clip, 'end'))

    def contact_fx(self, step, s, clip, t):
        """The contact of a move at strike s (clip started at t): its sound, the drawn path of the cut at the station from the
        station's tick on (the head arrives on s), the slash as the blade sweeps."""
        g = self.gb
        g.snd(s, CONTACT[step], pos=at_cut(s) if s in self.strikes else at_player(), src=('hit', step))
        sw = B.Swing(clip, E(clip, 'hit'))
        q = self.st_tick[s]
        out = B.Out()
        r = B.path_ride(out, self.key, sw, t, max(q, s - B.SHOW_FIRST), B.COL['P'], f'c{s}')
        for tt in sorted(out.t):                      # the path stands at the station (her place and yaw at the strike)
            g.at(tt, [S.gate(AT_ST, c) for c in out.t[tt]])
        out2 = B.Out()
        pcs = B.slash(out2, self.key, sw, t, B.SLASH[api.C_LILAC], f'c{s}')
        for tt in sorted(out2.t):
            g.at(tt, out2.t[tt])
        g.ev(r['show'], 'fx', 'sw_path', ('hit', step))
        B.DRAWN.setdefault(self.key, []).append(dict(kind='ride', clip=clip, event='hit', hit=s, first=False, col='P', sw=sw, t0=t,
                                                     show=r['show'], lead=s - r['show'], pts=r['pts'], end=r['end'], pieces=pcs, step=step))

    def restation(self, s):
        """A chain cut: at its lock (s - LOCK_LEAD) she shifts to the station beside the locked spot and faces the player."""
        lk = s - api.LOCK_LEAD
        self.gb.at(lk, face_st(), glide_st(RESTATION_T))
        self.gb.moves.append((lk, lk + RESTATION_T, 'station'))

    # ------------------------------------------------------------------ steps
    def s_tell(self, t):                              # A8.T
        g = self.gb
        g.play(t, 'g_tell')
        g.look(t, 'form', 'ghost', ('g_tell', 'lilac'))
        g.at(t, f'tag @s add {TAG_GHOST}')
        g.ev(t, 'tag', 'ghost+', ('g_tell', 'lilac'))
        g.snd(t, 'g_tell', src=('g_tell', 'lilac'))
        g.fx(t + E('g_tell', 'burst'), 'ghost_burst', puff_fb(n=24), at_body(0.95), src=('g_tell', 'burst'))
        self.ends_vanished(t, 'g_tell', 'gone', burst=False)   # the burst is at 3 (PLAN §4.5 A8.T)

    def s_d1(self, t):
        g = self.gb
        go, arr = t + E('g_dash', 'go'), t + E('g_dash', 'arrive')
        g.play(t, 'g_dash')
        g.at(t, tp_spot('d1'))
        g.moves.append((t, t, 'reappear d1'))
        g.snd(t, 'g_appear', src=('g_dash', 'appear'))
        g.at(go, FACE)
        g.fx(go, 'ghost_trail', [part(DUST['lilac'], 0.3, 0.4, 0.3, 0, 12)], at_body(0.95), src=('g_dash', 'go'), len=TRAIL['D1'])
        g.at(go, glide_st(arr - go))
        g.at(arr, face_st())
        g.moves.append((go, arr, 'dash side'))
        g.snd(go, 'g_dash', src=('g_dash', 'go'))

    def s_d2(self, t):
        g = self.gb
        go, stop = t + E('g_glide', 'go'), t + E('g_glide', 'stop')
        g.play(t, 'g_glide')
        g.at(t, tp_spot('d2'))
        g.moves.append((t, t, 'reappear d2'))
        g.snd(t, 'g_appear', src=('g_glide', 'appear'))
        g.at(go, FACE)
        g.fx(go, 'ghost_trail', [part(DUST['lilac'], 0.3, 0.2, 0.3, 0, 10)], at_body(0.45), src=('g_glide', 'go'), len=TRAIL['D2'])
        g.at(go, glide_st(stop - go))
        g.at(stop, face_st())
        g.moves.append((go, stop, 'glide d2e'))
        g.snd(go, 'g_dash', src=('g_glide', 'go'))

    def s_d3(self, t):
        g = self.gb
        gone, app, land = (t + E('g_drop', k) for k in ('gone', 'appear', 'land'))
        g.play(t, 'g_drop')
        g.fx(t, 'ghost_flash', [part(DUST['white'], 0.3, 0.8, 0.3, 0, 14), part('minecraft:electric_spark', 0.3, 0.8, 0.3, 0.1, 8)],
             at_body(0.95), src=('g_drop', 'flash'))
        g.snd(t, 'g_flash', src=('g_drop', 'flash'))
        g.fx(gone, 'ghost_burst', puff_fb(c='white'), at_body(1.1), src=('g_drop', 'gone'))
        g.at(app, tp_spot('d3', RE['D3']['up']))
        g.moves.append((app, app, 'reappear d3 (up)'))
        g.at(app, glide_st(land - app))
        g.at(land, face_st())
        g.moves.append((app, land, 'drop side'))

    def s_d4(self, t):
        g = self.gb
        run, lunge = t + E('g_run', 'run'), t + E('g_run', 'lunge')
        g.play(t, 'g_run')
        g.at(t, tp_spot('d4'))
        g.moves.append((t, t, 'reappear d4'))
        g.fx(t, 'ghost_burst', puff_fb(), at_body(0.8), src=('g_run', 'appear'))
        g.at(run, FACE)
        g.fx(run, 'ghost_trail', [part(DUST['lilac'], 0.3, 0.3, 0.3, 0, 10)], at_body(0.8), src=('g_run', 'run'), len=TRAIL['D4'])
        g.at(run, glide_st(lunge - run))
        g.at(lunge, face_st())
        g.moves.append((run, lunge, 'run side'))
        for i in range(3):                           # footsteps x3 during the run-in
            g.snd(run + i * (lunge - run) // 3, 'g_step', src=('g_run', 'run'))

    def s_cut_move(self, t, step, clip):
        """A8.1 .. A8.8: the contact effects at the cut of strike t + hit; the station for chain cuts; the move's own motion."""
        g = self.gb
        s = t + E(clip, 'hit')
        g.play(t, clip)
        if step == 'A8.3':
            lk, lp = s - api.LOCK_LEAD, s - LEAP_T       # the lock (she takes the station's yaw), the leap (coil + 3 -> the hit, 6 t)
            g.at(lk, face_st())
            g.snd(lp, 'g_leap', src=('plan', 'A8.3 breeze.jump at 3'))
            g.at(lp, f'execute positioned as {ST_M} run function rlk:mboss/mv/leap {{t:{LEAP_T},h:{LEAP_H}}}')
            g.moves.append((lp, s, 'leap over (2.5 b up)'))
            self.ends_vanished(t, clip, 'gone')
        elif step == 'A8.5':
            lk = s - api.LOCK_LEAD
            g.at(lk, face_st())
            g.at(t + E('g_x', 'drop'), glide_st(DROP_T))
            g.moves.append((t, t + DROP_T, 'drop side'))
            self.ends_vanished(t, clip, 'gone')
        elif self.prev_step(t) not in APPROACH:
            self.restation(s)
        if step == 'A8.4':
            sp = t + E('g_sweep', 'spring')
            g.at(sp, rise(HANG_UP, HANG_T))
            g.moves.append((sp, sp + HANG_T, 'spring up (hang)'))
        if step == 'A8.8':
            glow, rs, gone = (t + E('g_vert', k) for k in ('glow', 'rise', 'gone'))
            g.look(glow, 'blade', 'pink', ('g_vert', 'glow'))
            g.at(glow, api.rig('anchor/blade_tip'))
            g.fx(glow, 'glint', [part(DUST['magenta'], 0.1, 0.1, 0.1, 0, 8)], f'at {S.ANCHOR_M} rotated as @s',
                 src=('g_vert', 'glow'), c=api.C_MAGENTA)
            g.snd(glow, 'g_glow', src=('g_vert', 'glow'))
            g.look(s, 'blade', 'off', ('g_vert', 'hit'))
            g.at(rs, rise(RISE_UP, gone - rs))
            g.moves.append((rs, gone, 'rise out of view'))
            g.at(gone, hide())
            g.ev(gone, 'rig', 'state/hidden', ('g_vert', 'gone'))
        self.contact_fx(step, s, clip, t)

    def s_dive(self, t):                              # A8.9: normal colours, 6 b above the player, the dive (the judge)
        g = self.gb
        dv, hit = t + E('g_dive', 'dive'), t + E('g_dive', 'hit')
        g.play(t, 'g_dive')
        g.look(t, 'form', 'normal', ('g_dive', 'appear'))
        g.at(t, f'tag @s remove {TAG_GHOST}')
        g.ev(t, 'tag', 'ghost-', ('g_dive', 'appear'))
        # round V (v_brief §3 VB 4): she reappears IN the F5 view, DIVE_UP over the spot `dv` 4.5 b before the player, the blade
        # raised, for the whole wind-up (the clip's 15 t), the plunge's way drawn from her blade to the player (the head lands on
        # the judge tick); the dive ends 1 b over the spot `land` 2 b before the player, never on them
        g.at(t, tp_spot('dv', DIVE_UP))
        g.fx(t, 'ghost_burst', puff_fb(c='white'), at_body(1.1), src=('g_dive', 'appear'))
        g.moves.append((t, t, f'reappear {num(DIVE_UP, 1)} b up, 4.5 b before the player'))
        g.snd(dv, 'g_dive', src=('g_dive', 'dive'))
        g.at(dv, glide_spot('land', hit - dv, DIVE_STOP))
        g.moves.append((dv, hit, 'dive to 1 b above the spot before the player'))
        P1F.sw_runtime(g.W)
        out = B.Out()
        tip = B.track('g_dive')['t'][E('g_dive', 'dive')]
        r = B.target_line(out, self.key, t, dv, hit, B.COL['purple'],
                          f'at @s rotated as @s rotated ~ 0 positioned {B.car(tip)} facing entity {{T}} feet', PLAYER, PLAYER, dy='0')
        for tt in sorted(out.t):
            g.at(tt, out.t[tt])
        g.ev(t, 'fx', 'sw_line', ('g_dive', 'appear'))
        B.DRAWN.setdefault(self.key, []).append(dict(kind='line', hit=hit, show=r['show'], lead=hit - r['show'], col='purple', first=True, lock=dv))

    def s_judge(self, jt):
        g = self.gb
        key = self.key
        g.at(jt, api.shield('judge'), *S.hud('warn', on=0))
        g.ev(jt, 'shield', 'judge', 'JUDGE_T')
        g.ev(jt, 'hud', 'warn0', 'JUDGE_T')
        g.at(jt, S.gate(f'if score #gres {OBJ} matches 2', fn(f'p/{key}/fail')))
        # gauge 0 (#gres 1): no hazard; #done in this tick: the core starts seq/repel {at} at once (REPEL_T = JUDGE_T; the
        # repel's first frames are the gold deflect: she is 1 b above the player in normal colours, the dive's last pose)
        g.end(jt, cond=f'if score #gres {OBJ} matches 1')
        # the fail branch by the gauntlet's switch (hr_design §2.4): lethal = the instant death staged as 홍련일섬 (G2 by
        # default; G1 with ULT60_LETHAL), else the 500 per-mille dive hit (G1 by default). #done: G1 at FAIL60_P2_T (-> P2),
        # G2 FAIL_END t after the judge (-> the revive stance -> lead_re -> G2 again); a real death pauses the fight first
        # (the core cancels the gauntlet).
        lethal = api.ULT60_LETHAL if key == 'a8' else api.ULT5_LETHAL
        F = api.FAIL5_T
        black_t = jt - (F['slash'] - F['black'])
        if key == 'a13':
            assert F['slash'] == jt and F['black'] == black_t
        if lethal:
            black = [x for x in (K.ovl('black', 0, 3, 0),) if x]
            if black:
                g.at(black_t, S.gate(f'if score {api.PIPS_FP} {OBJ} matches 1..', black[0]))
            g.ev(black_t, 'hud', 'ovl black (segments left)', 'FAIL5_T black')
            fail = ([f'# {key.upper()} fail (#gres 2 at T + {jt}; lethal: ULT{60 if key == "a8" else 5}_LETHAL {lethal}; @s = the body): the instant death staged',
                     '# as 홍련일섬: the pink-white flash, the scarlet line across the player\'s view (yaw 90, as CS1) rising 13 deg',
                     '# toward their right through their chest, the petal burst, the slash; ult/fatal as the player (through i-frames,',
                     '# parries and shields; Ronova\'s revive applies). She lands 2 b in front of the player (g_reform).']
                    + [x for x in (K.ovl('pinkwhite', 0, 3, 8),) if x]
                    + [x for x in (K.fixed('keep_on'),) if x]
                    + S.fx('scarlet_line', [part(DUST['crimson'], 3.0, 0.05, 0.05, 0, 60)], pos=f'{AVATAR} {at_player(1.3)}',
                           len=600, yaw=90, roll=13)
                    + S.fx('scarlet_line', [], pos=f'{FIRST_PERSON} {at_player(1.62)} positioned ^ ^ ^1.2', len=600, yaw=90, roll=13)
                    + S.fx('petal_burst', [part('minecraft:cherry_leaves', 1.2, 0.8, 1.2, 0.05, 40)], pos=at_player(1.0), r=20)
                    + [x for x in (K.fixed('keep_off'),) if x]
                    + S.snd('fatal_slash', pos=f'at {PLAYER}')
                    + [f'execute as {PL} at @s run {api.shield("fatal")}', api.play('g_reform'), FACE] + glide_spot('land', LAND_T))
            g.ev(jt, 'fail', 'fatal', 'JUDGE_T')
        else:
            fail = [f'# {key.upper()} fail (#gres 2 at T + {jt}; not lethal: ULT{60 if key == "a8" else 5}_LETHAL {lethal}; @s = the body): the dive lands on the',
                    f'# player: ult/fail60 at the player\'s floor spot ({api.FAIL60_PM} per mille, never kills, the push ring there blows them',
                    f'# ~{num(api.FAIL60_PUSH[0] + 0.5, 1)} b off it); she lands on the impact point (from 1 b above it in {LAND_T} t), g_reform.',
                    f'execute at {PLAYER} positioned ~ {CY} ~ run {api.shield("fail60")}', api.play('g_reform'), FACE] + glide_spot('land', LAND_T)
            g.ev(jt, 'fail', 'fail60', 'JUDGE_T')
        g.W.w(f'p/{key}/fail', fail)
        g.at(jt + E('g_reform', 'end'), S.gate(f'if score #gres {OBJ} matches 2', api.play('idle2')))
        g.end(api.FAIL60_P2_T if key == 'a8' else jt + FAIL_END)

    # ------------------------------------------------------------------ the whole script
    def build(self):
        g, key = self.gb, self.key
        # the stations (round V): per strike s the tick its station is fixed: an approach's start for the cut the approach
        # leads into, else STATION_LEAD before the strike (never before the tick after the strike before it)
        self.st_tick = {}
        moves = [(t, step, clip) for t, step, clip, _c in self.rows if step in CONTACT]
        prev_s = None
        for t, step, clip in moves:
            s = t + E(clip, 'hit')
            before = [r for r in self.clip_rows if r[0] < t]
            app = before[-1] if before and before[-1][1] in APPROACH else None
            if app:
                q, name, up = app[0], APPROACH_END[app[1]], 0.0
            else:
                q = max((prev_s or 0) + 1, s - STATION_LEAD)
                name, up = ST_SPOT.get(step, ('side', 0.0))
            self.st_tick[s] = q
            g.at(q, station(name, up))
            g.ev(q, 'station', name, (step, s))
            prev_s = s
        g.cancel_lines.append(f'kill @e[type=minecraft:marker,tag={ST_T}]')
        for t, step, clip, c in self.rows:
            if step == 'A8.T':
                self.s_tell(t)
            elif step == 'D1':
                self.s_d1(t)
            elif step == 'D2':
                self.s_d2(t)
            elif step == 'D3':
                self.s_d3(t)
            elif step == 'D4':
                self.s_d4(t)
            elif step in CONTACT:
                self.s_cut_move(t, step, clip)
            elif step == 'A8.9':
                self.s_dive(t)
            elif step == 'judge':
                self.s_judge(t)
            else:
                raise ValueError((key, step))
            if c:
                g.cut(c, 1 if self.gauntlet else 0, step)
        for t in EXTRA_VANISH.get(key, ()):
            g.fx(t, 'ghost_burst', puff_fb(), at_body(0.95), src=('script', 'vanish'))
            g.at(t, hide())
            g.ev(t, 'rig', 'state/hidden', ('script', 'vanish'))
        if self.gauntlet:
            for i, bt in enumerate(api.BOLTS[key]):
                b, d = BOLT_AT[i % len(BOLT_AT)]
                keep = bt == api.JUDGE_T[key] and K.fixed('keep_on')     # F2 (HR-17): the fail's tick: kept with its line
                g.at(bt, keep or None,
                     f'execute at {PLAYER} rotated as {PL} rotated ~{num(b, 1)} 0 positioned ^ ^ ^{num(d, 2)} positioned ~ {CY} ~ run '
                     f'{fn("g/bolt")}', (K.fixed('keep_off') if keep else None))
                g.ev(bt, 'fx', 'deco_bolt', ('BOLTS', i))
                g.ev(bt, 'snd', 'deco_bolt', ('BOLTS', i))
            g.cancel_lines += S.hud('warn', on=0)
        return g


# ================================================================================================= the gauntlets
def build_gauntlet(key):
    def build(W):
        g_files(W)
        w = Walk(key, W)
        w.build().write('G1: the 60 % gauntlet' if key == 'a8' else 'G2: the 5 % ultimate gauntlet')
    return build


# ================================================================================================= P2's three entries
TRK = api.TRACK
P1F = __import__('mboss_scarlet.p1', fromlist=['p1'])     # the P1 kit's helpers (lock_fn, tail, ground, trail, at_anchor)


def _finish(pb, key):
    pb.write()
    TABLE[key] = pb.hits
    MOVES[key] = pb.motions
    CUES[key], FLASHES[key], PPW[key] = sorted(pb.cues), sorted(pb.flashes, key=lambda x: x[1]), pb.pp
    return pb


def face_lock():
    return FACE_LOCK


# ------------------------------------------------------------------------------------------------- MX 자광 십자참
def build_mx(W):
    """The purple cross (video P-m, with P-y as its retreat): a player nearer than 6 b -> she leaps back to ~9 b first (12 t,
    no flash; the pattern clock is held at 0 meanwhile); the iai crouch, the purple star 4, the lock 9, the streak to 1.6 b
    from the lock 14-16, the X on the lock 16 (unparriable), the cue 21, the dome round her 28 (parryable, kb 3). At
    <= 30 % HP the core may start it once more at once (api.MX_REPEAT)."""
    g_files(W)
    key = 'mx'
    pb = PB(key, W)
    pb.owner = 'p_ghost.py'
    lock, go, x, dome = (E(key, k) for k in ('lock', 'go', 'x', 'dome'))
    end = api.PAT_END[key]
    near, far, pre_t = api.MX_RETREAT
    assert lock == x - S.LOCK
    w = W.w
    w(f'p/{key}/retreat', [
        f'# MX retreat (@s = the body, tick 0; the player nearer than {num(near)} b): a {pre_t}-t leap straight back to about {num(far)} b',
        '# from them (probed through mv/ok), the backstep clip; the pattern clock waits (#mx_pre).',
        sset('#mx_pre', pre_t), api.play('backstep'),
        'function rlk:mboss/mv/dist',
        sset('#t', int(far * 10)), f'scoreboard players operation #t {OBJ} -= #mbDist mb',
        f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches ..0 run {sset("#t", 1)}',
        f'execute at @s facing entity {PLAYER} feet rotated ~180 0 run {fn("core/dash/probe")}',
        f'execute positioned as {S.PROBE_M} run function rlk:mboss/mv/leap {{t:{pre_t},h:10}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'] + S.snd('g_leap'))
    w(f'p/{key}/pre', [
        '# MX retreat tick (@s = the body): the clock is held at 0; at its end the iai crouch starts (clip mx from its tick 0).',
        sset('#pt', 0), f'scoreboard players remove #mx_pre {OBJ} 1', FACE,
        f'execute if score #mx_pre {OBJ} matches ..0 run {api.play(key)}'])
    pb.tick_head = [f'execute if score #mx_pre {OBJ} matches 1.. run return run {fn(f"p/{key}/pre")}']
    pb.at(0, FACE, sset('#mx_pre', 0),
          f'execute at @s if entity {PLAYER[:-1]},distance=..{num(near)}] run return run {fn(f"p/{key}/retreat")}',
          api.play(key))
    pb.motions.append((0, pre_t, 'retreat (held clock)'))
    pb.track(1, lock - 1, TRK['deg'])
    pb.at(lock, P1F.lock_fn(pb, key), FACE_LOCK)
    # the streak: to 1.6 b from the lock on her side (mv/ok-checked; else she cuts from where she stands)
    pb.at(go, f'execute at {S.LOCK_M} facing entity @s feet rotated ~ 0 positioned ^ ^ ^1.6 if function rlk:mboss/mv/ok run '
              f'function rlk:mboss/mv/glide {{t:{x - go}}}',
          S.snd('g_dash'), S.fx('afterimage', pos=at_body(1.2), len=90))
    pb.motions.append((go, x, 'streak'))
    pb.hit(0, tell_from=0, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    P1F.dash_line(pb, key, x - B.SHOW_FIRST, lock, x)
    B.ride(pb, key, 0, path=False)
    pb.at(x, S.snd('g_x'))
    pb.track(x + 1, dome - S.LOCK, TRK['deg'])
    pb.hit(1, tell_from=x)
    B.ride(pb, key, 1, prev=x)
    pb.at(dome, S.snd('g_dome'))
    pb.pp_window(dome)
    P1F.tail(pb, dome, end)
    return _finish(pb, key)


# ------------------------------------------------------------------------------------------------- NB 낙월 사선
def build_nb(W):
    """The falling-moon bands (video P-n): she leaps 5 b up and <= 6 b toward the player, hangs, and cuts three long
    diagonal bands through the player's locked spot (each lock 7 t before its band, the cue there), then lands. In the air
    2-46 (44 t: the ceiling of hr_design §8.5)."""
    g_files(W)
    key = 'nb'
    pb = PB(key, W)
    pb.owner = 'p_ghost.py'
    leap, apex, land = E(key, 'leap'), E(key, 'apex'), E(key, 'land')
    bs = [E(key, f'b{i}') for i in (1, 2, 3)]
    end = api.PAT_END[key]
    h, travel = api.LEAP_H[key], api.NB_TRAVEL
    ln, wd = api.HITS[key][0][3]
    assert land - leap <= api.AIR_MAX
    w = W.w
    w(f'p/{key}/leap', [
        f'# NB leap (@s = the body, tick {leap}): the floor point <= {num(travel)} b toward the player (3 b short of them; probe),',
        f'# then a rise of {num(h)} b to above it in {apex - leap} t.',
        'function rlk:mboss/mv/dist',
        f'scoreboard players operation #t {OBJ} = #mbDist mb',
        f'scoreboard players remove #t {OBJ} 30',
        f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches ..-1 run {sset("#t", 0)}',
        f'execute if score #t {OBJ} matches {int(travel * 2) + 1}.. run {sset("#t", int(travel * 2))}',
        f'execute at @s facing entity {PLAYER} feet rotated ~ 0 run {fn("core/dash/probe")}',
        f'execute positioned as {S.PROBE_M} positioned ~ {CY + h} ~ run function rlk:mboss/mv/glide {{t:{apex - leap}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'])
    pb.at(0, FACE, api.play(key))
    pb.track(1, leap - 1, TRK['deg'])
    pb.at(leap, fn(f'p/{key}/leap'), S.snd('leap'))
    P1F.trail(pb, (leap, (leap + apex) // 2, apex))
    pb.motions.append((leap, apex, 'leap'))
    prev = apex
    for i, t in enumerate(bs):
        lk = t - S.LOCK
        assert lk == E(key, f'lock{i + 1}')
        pb.track(prev, lk - 1, 20)
        pb.at(lk, P1F.lock_fn(pb, key), FACE_LOCK)
        yaw = api.NB_YAW[i]
        org = f'at {S.LOCK_M} rotated as @s rotated ~{yaw} 0 positioned ^ ^ ^-{num(ln / 2)}'
        pb.hit(i, tell_from=0 if i == 0 else prev, pos=f'{org} positioned ~ {CY} ~')
        # round V: the cut's path on her blade (in the air) + the band's own line through the locked spot at chest height from
        # the lock on (white-gold: parryable), burning white as the band strikes
        B.ride(pb, key, i, prev=bs[i - 1] if i else None)
        out = B.Out()
        B.static_line(out, key, f'n{i}', lk, t, B.COL['P'], f'at {S.LOCK_M} rotated as @s rotated ~{yaw} 0 positioned ^ ^1.2 ^-{num(ln / 2)}', ln)
        out.into(pb)
        pb.at(t, S.fx('qi_beam', [part(DUST['lilac'], 0.5, 0.3, 4.0, 0, 40), part(DUST['white'], 0.3, 0.2, 3.0, 0, 12)],
                      pos=f'at {S.LOCK_M} rotated as @s rotated ~{yaw} 0 positioned ~ ~0.6 ~', len=int(ln * 10)), S.snd('g_sweep'))
        prev = t + 1
    # she drops to the floor below after the last band and lands at `land`
    pb.at(bs[-1], f'execute at @s positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:{land - bs[-1]}}}')
    pb.motions.append((bs[-1], land, 'land'))
    P1F.tail(pb, bs[-1], end, moved=land)
    P1F.ground(pb)
    return _finish(pb, key)


# ------------------------------------------------------------------------------------------------- Q 자영 포박 · 천공 낙월
def build_q(W):
    """The ghost grab and the sky moon (video P-q; hr_design §8.2: the grab is unparriable). q_grab: a far lilac glint 0, the
    ghost form 4-20, the purple star 8, the lock 13, the ghost lunge 16-20 (<= 14 b), the grab 20 (a disc at the lock; no
    knockback: HA-08, the throw is her pose and only the pillar, the chain's last hit, pushes). The grab strikes after the module tick, so the branch is taken at api.Q_AIR_T0 (21): missed /
    perfect-dodged / left the disc -> she reforms, the end at api.Q_MISS_END; landed -> q_air from 21: she rises, the
    diagonal beam (cue, parryable), the dive (cue, parryable), a second leap, the purple star, the sky mark on the locked
    spot (a line from the sky and a short line at the feet: never an area) and the pillar (unparriable). The player stays on
    the ground and in control."""
    g_files(W)
    key = 'q'
    pb = PB(key, W)
    pb.owner = 'p_ghost.py'
    ghost, lock, go, grab = (E('q_grab', k) for k in ('ghost', 'lock', 'go', 'grab'))
    T0 = api.Q_AIR_T0
    A = lambda e: T0 + E('q_air', e)          # noqa: E731  a q_air event on the pattern clock
    HIT, MISS = f'if score #q_hit {OBJ} matches 1', f'unless score #q_hit {OBJ} matches 1'
    dmax = api.DASH_LEN[key]
    h1, h2 = api.LEAP_H['q'], api.LEAP_H['q2']
    assert lock == grab - S.LOCK
    w = W.w
    gh = lambda ls: [S.gate(HIT, x) for x in ls if x]      # noqa: E731
    # ---- q_grab
    pb.at(0, FACE, sset('#q_hit', 0), api.play('q_grab'),
          P1F.at_anchor('blade_mid', S.fx_lines('glint', [part(DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    pb.track(1, lock - 1, TRK['deg'])
    pb.at(ghost, api.rig('look/form/ghost'), f'tag @s add {TAG_GHOST}', S.snd('g_tell'),
          S.fx('ghost_burst', puff_fb(n=20), pos=at_body(0.95)))
    reach = num(dmax + 1.6, 2)
    pb.at(lock, P1F.lock_fn(pb, key), FACE_LOCK,
          # a locked spot beyond her reach is pulled in along her aim: the grab lands where she arrives, never farther
          f'execute at @s positioned ~ {CY} ~ unless entity {S.LOCK_M[:-1]},distance=..{reach}] rotated as @s rotated ~ 0 '
          f'positioned ^ ^ ^{reach} run tp {S.LOCK_M} ~ ~ ~')
    w(f'p/{key}/lunge', [
        f'# Q ghost lunge (@s = the body, tick {go}): along the locked aim to within 2 b of the locked spot, at most {num(dmax)} b',
        f'# (0.5 b probe steps through mv/ok), in {grab - go} t.',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(TAG_P, S.PROBE_T)}}}',
        f'execute at @s rotated as @s as {S.PROBE_M} run tp @s ~ ~ ~ ~ 0',
        sset('#t', int(dmax * 2)), sset('#t2', 0),
        f'execute as {S.PROBE_M} at @s run {fn(f"p/{key}/lstep")}',
        f'execute positioned as {S.PROBE_M} run function rlk:mboss/mv/glide {{t:{grab - go}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'])
    w(f'p/{key}/lstep', [
        '# Q lunge probe step (@s = the probe, at / rotated as it): 0.5 b on while mv/ok passes, until within 2 b of the lock.',
        f'execute if score #t2 {OBJ} >= #t {OBJ} run return 0',
        f'execute if entity {S.LOCK_M[:-1]},distance=..2.0] run return 0',
        'execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0',
        'tp @s ^ ^ ^0.5',
        f'scoreboard players add #t2 {OBJ} 1',
        f'execute at @s run {fn(f"p/{key}/lstep")}'])
    pb.at(go, fn(f'p/{key}/lunge'), S.snd('g_dash'),
          S.fx('ghost_trail', [part(DUST['lilac'], 0.3, 0.4, 0.3, 0, 12)], pos=at_body(0.95), len=int(dmax * 10)))
    pb.motions.append((go, grab, 'ghost lunge'))
    pb.hit(0, tell_from=0, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~', kbdir=1)
    P1F.dash_line(pb, key, grab - B.SHOW_FIRST, lock, grab)
    pb.at(grab, api.rig('look/form/normal'), f'tag @s remove {TAG_GHOST}',
          S.fx('claw_streaks', [part(DUST['lilac'], 0.6, 1.0, 0.6, 0, 16)], pos=f'at {S.LOCK_M} positioned ~ {CY + 1} ~', r=12))
    # ---- the branch (the grab's result is this tick's #hpp: the hits of hers the core read)
    pb.at(T0, f'execute if score #hpp {OBJ} matches 1.. run {sset("#q_hit", 1)}',
          S.gate(MISS, api.play('g_reform')), S.gate(HIT, api.play('q_air')), gh(S.snd('thrown')))
    turn = f'function rlk:mboss/mv/turn {{max:{TRK["deg"]}}}'
    pb.rng(T0 + 1, api.Q_MISS_END - 1, S.gate(MISS, turn))
    pb.at(T0 + E('g_reform', 'end'), S.gate(MISS, fn('ai/tail')))
    pb.rng(T0 + E('g_reform', 'end') + 1, api.Q_MISS_END - 1, S.gate(MISS, fn('ai/tail_step')))
    pb.at(api.Q_MISS_END, S.gate(MISS, sset('#done', 1)))
    # ---- q_air (only when the grab landed)
    rise, apex, dive, hit, leap2, apex2, lock3, pillar, drop, land2 = (
        A(k) for k in ('rise', 'apex', 'dive', 'hit', 'leap', 'apex2', 'lock3', 'pillar', 'drop', 'land2'))
    beam = A('beam')
    assert hit - rise <= api.AIR_MAX and land2 - leap2 <= api.AIR_MAX
    pb.at(rise, gh([f'execute at @s positioned ~ {CY + h1} ~ run function rlk:mboss/mv/glide {{t:{apex - rise}}}']),
          gh(S.snd('leap')), gh(S.fx('afterimage', pos=at_body(1.2), len=20)))
    pb.motions.append((rise, apex, 'rise'))
    pb.rng(apex, A('lock1') - 1, S.gate(HIT, f'function rlk:mboss/mv/turn {{max:20}}'))
    pb.at(A('lock1'), gh([P1F.lock_fn(pb, key), FACE_LOCK]))
    ln, wd = api.HITS[key][1][3]
    pb.hit(1, tell_from=T0, t=beam, cond=HIT, pos=f'at @s positioned ~ {CY} ~ facing entity {S.LOCK_M} feet rotated ~ 0')
    P1F.drop_line(pb, key, 'q_air', beam - B.SHOW_FIRST, A('lock1'), beam, idx=1, t0=T0, cond=HIT)
    B.ride(pb, key, 1, t0=T0, cond=HIT, path=False)
    pb.at(beam, gh(S.fx('qi_beam', [part(DUST['lilac'], 0.4, 1.5, 0.4, 0, 40)],
                        pos=f'at @s positioned ~ ~0.8 ~ facing entity {S.LOCK_M} feet', len=int(ln * 10))), gh(S.snd('g_rise')))
    pb.rng(beam + 1, A('lock2') - 1, S.gate(HIT, f'function rlk:mboss/mv/turn {{max:20}}'))
    pb.at(A('lock2'), gh([P1F.lock_fn(pb, key), FACE_LOCK]))
    pb.at(dive, gh([P1F.near(P1F.LAND_SHORT, hit - dive)]), gh(S.snd('g_dive')),
          gh(S.fx('afterimage', pos=at_body(1.2), len=30)))
    pb.motions.append((dive, hit, 'dive'))
    pb.hit(2, tell_from=beam, t=hit, cond=HIT, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    P1F.drop_line(pb, key, 'q_air', hit - B.SHOW_CHAIN, A('lock2'), hit, idx=2, t0=T0, cond=HIT)
    B.ride(pb, key, 2, t0=T0, cond=HIT, path=False)
    pb.at(hit, gh(S.fx('dive_impact', [part(DUST['lilac'], 1.0, 0.1, 1.0, 0, 30)], pos=f'at {S.LOCK_M} positioned ~ {CY + 0.1} ~', r=26)),
          gh(S.snd('a4_impact', pos=f'at {S.LOCK_M}')))
    pb.rng(hit + 1, leap2 - 1, S.gate(HIT, turn))
    pb.at(leap2, gh([f'execute at @s positioned ~ {CY + h2} ~ run function rlk:mboss/mv/glide {{t:{apex2 - leap2}}}']),
          gh(S.snd('leap')), gh(S.fx('afterimage', pos=at_body(1.2), len=20)))
    pb.motions.append((leap2, apex2, 'leap'))
    pb.rng(apex2, lock3 - 1, S.gate(HIT, f'function rlk:mboss/mv/turn {{max:20}}'))
    # the sky mark at the lock tick: the video's only ground mark, a line (never an area)
    pb.at(lock3, gh([P1F.lock_fn(pb, key), FACE_LOCK]),
          gh(S.fx('sky_mark', [part(DUST['white'], 0.02, 6.0, 0.02, 0, 40), part(DUST['magenta'], 0.9, 0.02, 0.02, 0, 12)],
                  pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')))
    pb.hit(3, tell_from=hit, t=pillar, cond=HIT, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    P1F.drop_line(pb, key, 'q_air', pillar - B.SHOW_FIRST, lock3, pillar, idx=3, t0=T0, cond=HIT)
    B.ride(pb, key, 3, t0=T0, cond=HIT, path=False)
    pb.at(pillar, gh(S.fx('sky_pillar', [part(DUST['white'], 0.5, 6.0, 0.5, 0, 80), part(DUST['magenta'], 0.8, 0.3, 0.8, 0, 20)],
                          pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~', r=24)), gh(S.snd('sky_pillar', pos=f'at {S.LOCK_M}')))
    pb.at(drop, gh([f'execute at @s positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:{land2 - drop}}}']))
    pb.motions.append((drop, land2, 'drop'))
    end = T0 + 90
    pb.rng(pillar + 1, end - 1, S.gate(HIT, turn))
    pb.at(land2, S.gate(HIT, fn('ai/tail')))
    pb.rng(land2 + 1, end - 1, S.gate(HIT, fn('ai/tail_step')))
    pb.motions.append((land2 + 1, end - 1, 'tail move'))
    pb.end(end)
    pb.cancel_lines += [f'execute as {BODY} run {fn("g/reset")}']
    return _finish(pb, key)


BUILD = {'mx': build_mx, 'nb': build_nb, 'q': build_q, 'a8': build_gauntlet('a8'), 'a13': build_gauntlet('a13')}
NOTES = {'mx': 'the purple X on the locked spot (unparriable) + the dome round her (parryable); a leap back first when near',
         'nb': 'a leap, three long diagonal bands through the locked spots (parryable), the landing',
         'q': 'the ghost grab (unparriable); landed: the beam, the dive (parryable), the sky pillar (unparriable)',
         'a8': 'G1, the 60 % gauntlet: 9 parry cuts, the dive = the judge (gauge 0 -> repel {at:60}, else fail60 -> P2)',
         'a13': 'G2, the 5 % ultimate: 11 parry cuts, the dive = the judge (gauge 0 -> repel {at:5}, else the instant death)'}
CLIPS_OF = {'mx': ('mx', 'backstep'), 'nb': ('nb',), 'q': ('q_grab', 'q_air', 'g_reform')}


def _clips(key):
    if key in CLIPS_OF:
        return CLIPS_OF[key]
    return tuple(sorted({r[2] for r in api.SCRIPTS[key] if r[2]} | {'g_reform', 'idle2'}))


PATTERNS = [api.Pattern(k, S.TID[k], _clips(k), BUILD[k], notes=NOTES[k]) for k in api.P2]
assert [p.key for p in PATTERNS] == list(api.P2)
