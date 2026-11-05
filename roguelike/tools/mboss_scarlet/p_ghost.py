"""Ghost patterns of 홍련 (Scarlet), stage S4 (plan S:hr/PLAN.md §4.1-4.5, §5; contract S:hr/contract.md §3.5-3.6):
R1 자영 돌격, R2 월륜 일섬, R3 자영 활강 (P2 entries cut from the gauntlets' moves) and the gauntlets A8 자영 연참 (60 %) /
A13 필살 · 자영 연참 (5 %), with the shared ghost helpers g/**. OWNER: S4. Written by S3's tools/build_mboss_scarlet.py
through api.Writer('S4', api.OWN['S4']) (outputs F:boss/scarlet/p/{r1,r2,r3,a8,a13}/** and F:boss/scarlet/g/**).

Every timing comes from api.SCRIPTS (the rows: a clip's start on the pattern clock, the cut made at that step) and
api.ev (the clip events: every effect / sound / move at its event, PLAN §4.5 move table); every cut through api.cut()
(g/cut/make / aim / lock), every disc through api.disc() (g/disc/throw), the shield only through api.shield(); hits
are the framework's (mboss/hz/disc, mboss/pj/launch), quiet (#hzQuiet 1, no outline / flash / decal), Electro 1U.

Runtime (api.Pattern; @s = the body, at it; clock #pt hr = played ticks since start; the shown clip tick == #pt):
- p/<key>/start (tick 0), p/<key>/tick -> the 16-tick block p/<key>/b/<i> -> the tick file p/<key>/k/<t>,
  p/<key>/cancel (any executor, idempotent). #done hr 1 on the last tick (R1 67, R2 60, R3 49 - F1 HR-14: R1 / R3 end 12 t
  after their last hit; A8 REPEL_T 206 after a deflect / FAIL60_P2_T 214 after the fail; A13 270 both).
- The cut builder (PLAN §5.3): g/cut/make {s,t,dmg,kb,n} makes a quiet Electro disc hazard of api.CUT_R at the player's
  feet on the floor (hz_opts quiet 1 / sfx 0 / el 3 / act 2, kb along her -> the player: kbdir 1), tagged rlk_hr_cut +
  rlk_hr_p + rlk_hr_p_<key of #pat>, objective hr = s (its strike tick), rlk_hr_cnt when it counts; g/cut/aim {s} puts it
  on the player again (mboss/hz/aim, every tick made + 1 .. lock - 1); g/cut/lock {s} the last aim and, for a counting
  cut, shield/cut {s} as its marker at it (S3's pip window at the lock point). R1 / R3 cuts never count (n 0).
- The moon disc (PLAN §4.5 A7): g/disc/throw {kb}: one item display card 1 b in front of her, api.DISC y 0.9 b over the
  floor (the framework's blade rows then cover 0 .. 1.65 b: a jump does not clear it), summoned, then rotated toward its
  lock (pitch 0; F1 HR-15: g/disc/lock put a marker at the player's feet LOCK_LEAD t before the release and turned her to
  it), launched (pj/launch blade, hr 1.4, life 16, wall stop, T2 Electro, kb), dressed by the kit (fx/prop/disc) or a flat
  purple pane stand-in; no homing; never counts for the shield.
- Spots g/spot/<name> (@s = the body): a marker rlk_hr_gsp at the first candidate passing mv/ok (inside MOVE_R 22.5, feet
  and head free), the candidates relative to the player's facing (api.REAPPEAR bearings / distances and their
  fallbacks), else the guaranteed fallback: the point on the player -> C line at the move's distance (<= FALLBACK_R from
  C), walked toward the axis in 0.5 b steps until mv/ok passes (never in blocks).
- The ghost: rlk_hr_ghost on the body + the rig look form/ghost from the lilac switch (T0); the core keeps rlk_mb_inv
  then. Gauntlets: off at the dive's reappearance (form normal, A8.9). R1 / R3: form normal at g_reform's 'solid' event,
  the tag off at the script's 'solid' row (R1 62, R3 46: hittable again); from that row to the end (R2: api.TAIL_MOVE t
  after its last release) she turns to the player and moves as the recovery does (F1 HR-14: ai/tail, ai/tail_step).
- The gauntlet frame (PLAN §5.4-5.5): the judge at api.JUDGE_T calls shield/judge (S3 plays the deflect staging), the
  darkness lifts (arena_look crimson) and the warning banner goes; deflect: she drops from 1 b above the player to the
  floor 1.2 b in front of them (JT + 2 .. JT + 10), #done at REPEL_T; the fail by the gauntlet's switch (question 6):
  not lethal (A8 by default; A13 with ULT5_LETHAL false) = ult/fail60 at the player's floor spot (the push ring blows them
  off it), she lands on that impact point, g_reform; lethal (A13 by default; A8 with ULT60_LETHAL true) = the black overlay
  3 t before the judge when pips are left, at the judge the pink-white overlay + scarlet_line + petal_burst + the slash
  sound + ult/fatal as the player, she lands 2 b in front of them. #done: A8 at FAIL60_P2_T, A13 at REPEL_T.
- Cancel (pause / reload / death / cleanup / tests): every entity of the pattern (rlk_hr_p_<key>, rlk_hr_cut, the spot
  marker), the body back to normal (ghost tag off, form normal, blade off, visible, no glide, on the floor); a gauntlet
  also turns the banner off and requests crimson. Never #ph, the shield or the bars.

TABLE[key] = the recorded hits (cuts / discs) and EVENTS[key] = (tick, kind, name, source) of every effect / sound / rig
call for the tests (S:hr/tests/pat_ghost.py) and renders (S:hr/s4/render_ghost.py); MOVES[key] = the body moves.
"""
import math
from collections import defaultdict

from . import api
from . import s3lib as S
from .s3lib import sset, fn, part

L, K = api.L, api.K
E = api.ev
OBJ, NS, CY = api.OBJ, api.NS, api.CY
BODY, PLAYER, PL, ARENA_M = S.BODY, S.PLAYER, S.PL, S.ARENA_M
OK = 'function rlk:mboss/mv/ok'
FACE = 'function rlk:mboss/mv/face'
STOP = 'function rlk:mboss/mv/stop'
TAG_P, TAG_CUT, TAG_GHOST = api.TAGS['pat'], api.TAGS['cut'], api.TAGS['ghost']
CNT_T = 'rlk_hr_cnt'                 # the hazard marker of a counting cut (g/cut/lock registers its pip window)
SPOT_T = 'rlk_hr_gsp'                # the transient spot marker of g/spot/<name>
DISC_T, DISC_NEW = 'rlk_hr_disc', 'rlk_hr_gdn'
DISC_LOCK_NEW = 'rlk_hr_gln'         # F1 (HR-15): the transient tag of a new disc lock marker (g/disc/lock)
FACE_LOCK = f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0'   # she faces the disc's lock marker
SPOT_M = f'@e[type=minecraft:marker,tag={SPOT_T},limit=1]'
SPOT_ALL = f'@e[type=minecraft:marker,tag={SPOT_T}]'
KILL_SPOT = f'kill {SPOT_ALL}'
BLOCK = 16                           # ticks per dispatch block of p/<key>/tick
FIRST_PERSON, AVATAR = 'if entity @a[tag=rlk_body]', 'unless entity @a[tag=rlk_body]'   # F2 (HR-45): no avatar = first person
DUST = S.DUST
GAUNT = api.GAUNTLETS
TABLE, EVENTS, MOVES = {}, {}, {}


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
    'tell': ([('face', 0, RE['tell']['dist']), ('face', 90, RE['tell']['dist']), ('face', -90, RE['tell']['dist']),
              ('face', 180, RE['tell']['dist'])], RE['tell']['dist'], 'A13: inside the yellow tell, 3 b in front of the player'),
    'far': ([('tobody', 0, RE['tell']['retreat']), ('tobody', 0, 9.0), ('tobody', 0, 6.0), ('tobody', 60, 9.0),
             ('tobody', -60, 9.0)], RE['tell']['retreat'], 'A13: the retreat to 12 b from the player (on the player -> her line)'),
    'back': ([('away', 0, 6.0), ('away', 0, 4.5), ('away', 0, 3.0), ('away', 90, 4.0), ('away', -90, 4.0)], None,
             'R2: the retreat 6 b straight away from the player (shorter / sideways when blocked; else she stays)'),
    'back1': ([('away', 0, 1.0)], None, 'R2: the step back 1 b (else she stays)'),
    'beyond': ([('frombody', 0, 3.0), ('frombody', 0, 2.0), ('frombody', 0, 1.0), ('face', 0, 0.0)], 3.0,
               'R1: the landing 3 b beyond the player (her leap over them)'),
    'over': ([('face', 0, 0.0)], 1.5, 'the player\'s own floor spot (the A8.3 leap and the A8.9 dive add the height)'),
    'land': ([('face', 0, 2.0), ('face', 90, 2.0), ('face', -90, 2.0)], 2.0,
             'the A13 fail landing 2 b in front of the player (she dove from straight above them: not toward her)'),
    'lock': ([('face', 0, 1.2), ('face', 60, 1.2), ('face', -60, 1.2)], 1.2,
             'the deflect: the blade lock 1.2 b in front of the player'),
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
        '# dmg % of the base hit, knockback kb along her -> the player (kbdir 1, the marker\'s yaw); no outline, flash or decal.',
        '# g/cut/tag stamps it (objective hr = s, rlk_hr_cut, the pattern tags, rlk_hr_cnt when it counts: n 1).',
        f'$scoreboard players set #g_s {OBJ} $(s)', f'$scoreboard players set #g_n {OBJ} $(n)']
      + L.hz_opts(quiet=1, sfx=0, el=api.ELEC, act=2, kbdir=1)
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
        f'# {{s}}: the lock of the cut of strike s (strike - LOCK_LEAD {api.LOCK_LEAD}): the last aim; from now on it stays. A counting cut',
        '# registers its pip window at this point (S3\'s shield/cut {s}, as the cut marker, at it).',
        f'$function {NS}g/cut/aim {{s:$(s)}}',
        f'$execute as @e[type=minecraft:marker,tag={CNT_T},scores={{{OBJ}=$(s)}},limit=1] at @s run function {NS}shield/cut {{s:$(s)}}'])


def disc_files(W):
    w = W.w
    D = api.DISC
    kit = bool(K.prop('disc'))
    if kit:
        nbt = f'{{Tags:{S.tags_nbt(TAG_P, DISC_T, DISC_NEW)},teleport_duration:1}}'
    else:
        nbt = (f'{{Tags:{S.tags_nbt(TAG_P, DISC_T, DISC_NEW)},teleport_duration:1,brightness:{{sky:15,block:15}},'
               'item:{id:"minecraft:purple_stained_glass_pane",count:1},transformation:{left_rotation:[0.7071f,0f,0f,0.7071f],'
               f'right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[{num(2 * D["hr"], 2)}f,{num(2 * D["hr"], 2)}f,0.2f]}}}}')
    new = f'@e[type=minecraft:item_display,tag={DISC_NEW}]'
    y = 0.9
    lines = [
        f'# {{kb}} (api.disc; @s = the body, at it): one A7 moon disc (PLAN §4.5): a blade projectile (#pjShape 1, half width',
        f'# {num(D["hr"], 1)} b, {num(D["speed"], 2)} b/t asked = {math.ceil(D["speed"] / 0.25 - 1e-9) * 0.25:.2f} b/t flown (0.25 b sub-steps rounded up), life {D["life"]} t, wall stop),',
        f'# {num(y, 1)} b over the floor (the blade rows cover 0 .. 1.65 b: a jump does not clear it), aimed at its lock (F1 HR-15:',
        f'# g/disc/lock {api.LOCK_LEAD} t before the release; a throw without one locks now) (no homing), {D["tier"]} Electro, kb; one card:',
        '# summoned 1 b in front of her, then rotated (pitch 0), then launched and dressed (kit fx/prop/disc; else a flat purple',
        '# pane). Never counts for the shield. The lock marker goes after the launch.',
        f'kill {new}',
        f'execute unless entity {S.LOCK_M} run {fn("g/disc/lock")}',
        f'execute at @s facing entity {S.LOCK_M} feet rotated ~ 0 positioned ^ ^ ^1 positioned ~ {num(CY + y, 2)} ~ run summon '
        f'minecraft:item_display ~ ~ ~ {nbt}',
        f'execute as {new} at @s facing entity {S.LOCK_M} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~',
        f'execute as {new} run {fn("g/disc/tag")}']
    lines += L.pj_opts(el=api.ELEC, wall=1, shape=D['shape'])
    lines += ['$scoreboard players set #pjKB mb $(kb)',
              f'execute as {new} at @s rotated as @s run {L.pj_launch(D["speed"], D["life"], api.DMG[D["tier"]], D["hr"])}']
    if kit:
        lines.append(f'execute as {new} run {K.prop("disc")}')
    lines += [f'tag {new} remove {DISC_NEW}', f'kill @e[type=minecraft:marker,tag={S.LOCK_T}]']
    w('g/disc/throw', lines)
    tag = ['# @s = the new disc card / its lock marker: the pattern tags of the running pattern (#pat).']
    for k in ('r2', 'a13'):
        tag.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run tag @s add {S.tag_p(k)}')
    w('g/disc/tag', tag)
    # F1 (HR-15, lead decision 11-05): the disc's aim locks LOCK_LEAD t before its release (the rule: aims lock 6-8 t before the
    # hit; PLAN §4.5 A7), so a player walking in still gets the lock + the flight to step out
    w('g/disc/lock', [
        f'# The lock of the next disc ({api.LOCK_LEAD} t before its release; @s = the body): a marker at the player\'s feet on the floor',
        f'# ({S.LOCK_T} + the pattern tags, as p1\'s lock_fn), she faces it from now on; g/disc/throw aims at it and removes it.',
        f'kill @e[type=minecraft:marker,tag={S.LOCK_T}]',
        f'execute at {PLAYER} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(TAG_P, S.LOCK_T, DISC_LOCK_NEW)}}}',
        f'execute as @e[type=minecraft:marker,tag={DISC_LOCK_NEW}] run {fn("g/disc/tag")}',
        f'tag @e[type=minecraft:marker,tag={DISC_LOCK_NEW}] remove {DISC_LOCK_NEW}',
        FACE_LOCK])


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
    disc_files(W)
    spot_files(W)
    body_files(W)


# ================================================================================================= the pattern builder
class GB:
    """Collects the commands of one pattern by pattern tick and writes p/<key>/{start,tick,cancel}, the 16-tick blocks
    b/<i> and the tick files k/<t>; records the hits (TABLE), the effect / sound / rig events (EVENTS) and the moves."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.ticks = defaultdict(list)
        self.hits, self.events, self.moves = [], [], []
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
        self.hits.append(dict(kind='cut', t=strike, made=made, lock=lock, tier=tier, kb=kb, n=count, step=step,
                              shape='pdisc', dims=(api.CUT_R,), dmg=api.DMG[tier], tell=made))

    def disc(self, t, kb, step, cond=None):
        line = api.disc(kb)
        self.at(t, S.gate(cond, line) if cond else line)
        self.hits.append(dict(kind='disc', t=t, kb=kb, step=step, tier=api.DISC['tier'], dmg=api.DMG[api.DISC['tier']],
                              shape='pj_disc', dims=(api.DISC['hr'], api.DISC['speed'], api.DISC['life']), cond=cond,
                              lock=t - api.LOCK_LEAD))

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


# the sword-qi at each move's contact (PLAN §4.5 move table; kit args in tenths / degrees; contract §6: pass every arg)
CONTACT = {
    'A8.1': ('qi_ring', dict(r=22, c=api.C_LILAC), 0.8, lambda: ring_fb(2.2), 'g_ring'),
    'A8.2': ('qi_band', dict(len=70, yaw=0, pitch=35, roll=0, sw=25), 0.3,
             lambda: [part(DUST['lilac'], 0.9, 1.2, 0.9, 0, 26)], 'g_rise'),
    'A8.3': ('qi_arc', dict(r=45, yaw=0, pitch=0, roll=-40, c=api.C_LILAC), 1.2,
             lambda: [part(DUST['lilac'], 1.6, 0.6, 1.6, 0, 30), part(DUST['white'], 1.2, 0.4, 1.2, 0, 10)], 'g_leap_cut'),
    'A8.4': ('qi_ring', dict(r=30, c=api.C_LILAC), 0.1, lambda: ring_fb(3.0), 'g_sweep'),
    'A8.5': ('qi_x', dict(r=25), 0.1, lambda: [part(DUST['lilac'], 1.4, 0.1, 1.4, 0, 30)], 'g_x'),
    'A8.6': ('qi_arc', dict(r=40, yaw=0, pitch=0, roll=15, c=api.C_LILAC), 0.8,
             lambda: [part(DUST['lilac'], 1.5, 0.3, 1.5, 0, 28)], 'g_wrap'),
    'A8.7': ('qi_dome', dict(r=35), 0.0, lambda: ring_fb(3.5) + [part(DUST['white'], 1.6, 1.4, 1.6, 0, 24)], 'g_dome'),
    'A8.8': ('qi_vert', dict(h=34, yaw=0, c=api.C_MAGENTA), 0.0,
             lambda: [part(DUST['magenta'], 0.2, 1.6, 0.2, 0, 26)], 'g_vert'),
}
# F2 (HR-12): where a contact's sword-qi stands from the cut spot in the player's facing frame (b to their left, b ahead): the
# kit stands A8.3's slanted crescent and A8.8's vertical one across the facing, so on the cut spot itself (the player's own
# plane) the first-person camera would see nothing; A8.8 'a tall crescent at the player's right' (PLAN §4.5)
CONTACT_AT = {'A8.3': (0.0, 2.0), 'A8.8': (-1.5, 1.5)}
# F2 (HR-12 / HR-45): A8.6's low wrap at thigh height (0.8 b, was 0.4: the floor clamp shrank it to a sliver from the
# F5 camera); in first person (no avatar) A8.5's floor X sits this far ahead of the cut spot (b; still across it: its
# arms reach 2.5 b), under the camera it would be out of view
CONTACT_FP = {'A8.5': 1.2}
APPROACH = ('D1', 'D2', 'D3', 'D4')
TRAIL = {'D1': 125, 'D2': 65, 'D4': 105}          # ghost_trail len (tenths): the nominal dash / glide / run lengths
HANG_UP, HANG_T = 3.0, 3                          # A8.4: she springs straight up and hangs (PLAN §4.5)
RISE_UP = 8.0                                     # A8.8: she rises 8 b up and out of view
LEAP_UP, LEAP_T, LEAP_H = 2.5, 6, 30              # A8.3: mv/leap {t:6,h:30} over the player (gauntlets: to 2.5 b above them)
DIVE_UP, DIVE_STOP = RE['A8.9']['up'], 1.0        # A8.9: 6 b above the player, the dive to 1 b above them
RESTATION_T, DROP_T = 3, 2                        # the chain cuts' small glide to the station; A8.5's drop from the hang
FALL_T = E('g_deflect', 'lock') - E('g_deflect', 'fall')   # the deflect: 1 b above the player -> the blade lock (8 t)
LAND_T = 2                                        # the fail: her landing from 1 b above the player (A8: on the impact point;
#                                                   the lethal fail: 2 b in front of the player)
# Decoration bolts (api.BOLTS): (bearing relative to the player's facing, distance 3-6 b) per bolt
BOLT_AT = ((-60, 3.6), (75, 4.4), (-130, 5.2), (150, 5.8))
# A13 U4 "vanishes 89" (PLAN §4.5): g_ring does not end vanished; the vanish before D2's reappearance is the pattern's
EXTRA_VANISH = {'a13': (89,)}


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

    def contact_fx(self, step, s):
        g = self.gb
        name, a, h, fb, sound = CONTACT[step]
        pos = at_cut(s, h) if s in self.strikes else at_player(h)
        if step in CONTACT_AT:
            pos += ' positioned ^{} ^ ^{}'.format(*(num(v, 2) for v in CONTACT_AT[step]))
        if step in CONTACT_FP:
            g.at(s, S.fx(name, [], pos=f'{FIRST_PERSON} {pos} positioned ^ ^ ^{num(CONTACT_FP[step], 2)}', **a))
            pos = f'{AVATAR} {pos}'
        g.fx(s, name, fb(), pos, src=('hit', step), **a)
        g.snd(s, sound, pos=at_cut(s) if s in self.strikes else at_player(), src=('hit', step))

    def restation(self, s):
        """A chain cut: at its lock (s - LOCK_LEAD) she shifts to the station beside the locked spot and faces the player."""
        lk = s - api.LOCK_LEAD
        self.gb.at(lk, FACE, glide_spot('side', RESTATION_T))
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
        g.at(go, glide_spot('side', arr - go))
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
        g.at(go, glide_spot('d2e', stop - go))
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
        g.at(app, glide_spot('side', land - app))
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
        g.at(run, glide_spot('side', lunge - run))
        g.moves.append((run, lunge, 'run side'))
        for i in range(3):                           # footsteps x3 during the run-in
            g.snd(run + i * (lunge - run) // 3, 'g_step', src=('g_run', 'run'))

    def s_cut_move(self, t, step, clip):
        """A8.1 .. A8.8: the contact effects at the cut of strike t + hit; the station for chain cuts; the move's own motion."""
        g = self.gb
        s = t + E(clip, 'hit')
        g.play(t, clip)
        if step == 'A8.3':
            lk, lp = s - api.LOCK_LEAD, s - LEAP_T       # the lock (she faces the player), the leap (coil + 3 -> the hit, 6 t)
            g.at(lk, FACE)
            g.snd(lp, 'g_leap', src=('plan', 'A8.3 breeze.jump at 3'))
            if self.gauntlet:
                g.at(lp, leap_spot('over', LEAP_T, LEAP_H, LEAP_UP))
                g.moves.append((lp, s, 'leap over (2.5 b up)'))
            else:
                g.at(lp, leap_spot('beyond', LEAP_T, LEAP_H))
                g.moves.append((lp, s, 'leap beyond (lands 3 b past the player)'))
            if self.gauntlet:
                self.ends_vanished(t, clip, 'gone')
        elif step == 'A8.5':
            lk = s - api.LOCK_LEAD
            g.at(lk, FACE)
            g.at(t + E('g_x', 'drop'), glide_spot('side', DROP_T))
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
        self.contact_fx(step, s)

    def s_dive(self, t):                              # A8.9: normal colours, 6 b above the player, the dive (the judge)
        g = self.gb
        dv, hit = t + E('g_dive', 'dive'), t + E('g_dive', 'hit')
        g.play(t, 'g_dive')
        g.look(t, 'form', 'normal', ('g_dive', 'appear'))
        g.at(t, f'tag @s remove {TAG_GHOST}')
        g.ev(t, 'tag', 'ghost-', ('g_dive', 'appear'))
        g.at(t, tp_spot('over', DIVE_UP))
        g.moves.append((t, t, 'reappear 6 b above the player'))
        g.snd(dv, 'g_dive', src=('g_dive', 'dive'))
        g.at(dv, glide_spot('over', hit - dv, DIVE_STOP))
        g.moves.append((dv, hit, 'dive to 1 b above the player'))
        # the thin vertical blade line 1-2 t before the impact
        g.fx(hit - 2, 'qi_line', [part(DUST['white'], 0.03, 1.2, 0.03, 0, 10)], f'at @s rotated ~ 90 positioned ~ ~0.8 ~',
             src=('g_dive', 'dive'), len=40)

    def s_judge(self, jt):
        g = self.gb
        key = self.key
        g.at(jt, api.shield('judge'), *[x for x in (api.arena_look('crimson'),) if x], *S.hud('warn', on=0))
        g.ev(jt, 'shield', 'judge', 'JUDGE_T')
        g.ev(jt, 'look', 'crimson', 'JUDGE_T')
        g.ev(jt, 'hud', 'warn0', 'JUDGE_T')
        g.at(jt, S.gate(f'if score #gres {OBJ} matches 2', fn(f'p/{key}/fail')))
        # deflect: she halts 1 b above the player (S3's judge plays g_deflect), drops into the blade lock
        fall = jt + E('g_deflect', 'fall')
        g.at(fall, S.gate(f'if score #gres {OBJ} matches 1', fn(f'p/{key}/fall')))
        g.moves.append((fall, fall + FALL_T, 'deflect: down to the blade lock'))
        self.gb.W.w(f'p/{key}/fall', [f'# {key.upper()} deflect (T + {fall - jt} after the judge; @s = the body): from 1 b above the player down to the blade lock',
                                      f'# 1.2 b in front of them in {FALL_T} t (g_deflect fall -> lock), facing them.', FACE]
                    + glide_spot('lock', FALL_T))
        # the fail branch by the gauntlet's switch (PLAN §0.1 question 6, §5.5): lethal = the instant death staged as 홍련일섬
        # (A13 by default; A8 with ULT60_LETHAL), else the 500 per-mille dive hit (A8 by default; A13 with ULT5_LETHAL false:
        # "5 %도 큰 피해만"). #done: A8 at FAIL60_P2_T (-> P2), A13 at REPEL_T (-> the revive stance -> A13 again); a real
        # death pauses the fight first (the core cancels the gauntlet).
        lethal = api.ULT60_LETHAL if key == 'a8' else api.ULT5_LETHAL
        F = api.FAIL5_T
        black_t = jt - (F['slash'] - F['black'])
        if key == 'a13':
            assert F['slash'] == jt and F['black'] == black_t
        if lethal:
            black = [x for x in (K.ovl('black', 0, 3, 0),) if x]
            if black:
                g.at(black_t, S.gate(f'if score {api.PIPS_FP} {OBJ} matches 1..', black[0]))
            g.ev(black_t, 'hud', 'ovl black (pips left)', 'FAIL5_T black')
            fail = ([f'# {key.upper()} fail (#gres 2 at T + {jt}; lethal: ULT{60 if key == "a8" else 5}_LETHAL {lethal}; @s = the body): the instant death staged',
                     '# as 홍련일섬 (PLAN §5.5): the pink-white flash, the scarlet line across the player\'s view (yaw 90, as CS1 C8) rising',
                     '# 13 deg toward their right through their chest, the petal burst, the slash; ult/fatal as the player (through i-frames',
                     '# and shields; Ronova\'s revive applies).',
                     f'# She lands 2 b in front of the player (g_reform).']
                    + [x for x in (K.ovl('pinkwhite', 0, 3, 8),) if x]
                    # F2 (HR-17): kept cards (ult/fatal kills the player in this tick: the kit's dead clear and the pause clear
                    # would take them before the client draws them); HR-45: in first person the line at the eye, 1.2 b ahead
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
                    f'execute at {PLAYER} positioned ~ {CY} ~ run {api.shield("fail60")}', api.play('g_reform'), FACE] + glide_spot('over', LAND_T)
            g.ev(jt, 'fail', 'fail60', 'JUDGE_T')
        g.W.w(f'p/{key}/fail', fail)
        g.at(jt + E('g_reform', 'end'), S.gate(f'if score #gres {OBJ} matches 2', api.play('idle2')))
        if key == 'a8':
            g.end(api.REPEL_T['a8'], cond=f'if score #gres {OBJ} matches 1')
            g.end(api.FAIL60_P2_T)
        else:
            g.end(api.REPEL_T['a13'])

    def s_a7_tell(self, t):
        g = self.gb
        yel, ret, settle = (t + E('a7_tell', k) for k in ('yellow', 'retreat', 'settle'))
        g.play(t, 'a7_tell')
        if self.key == 'a13':
            # she dissolves at the X and reappears inside the yellow tell 3 b in front of the player, retreats to 12 b
            g.fx(t + 1, 'ghost_burst', puff_fb(), at_body(0.95), src=('g_x', 'gone'))
            g.at(t + 1, tp_spot('tell'))
            g.moves.append((t + 1, t + 1, 'reappear in the tell (3 b)'))
            g.at(ret, glide_spot('far', settle - ret))
            g.moves.append((ret, settle, 'retreat 12 b'))
            g.fx(settle, 'ghost_burst', puff_fb(n=10), at_body(0.2), src=('a7_tell', 'settle'))
            g.at(settle, FACE)
        else:
            g.at(t, FACE, glide_spot('back1', 2))
            g.moves.append((t, t + 2, 'step back'))
            g.at(ret, glide_spot('back', settle - ret))
            g.moves.append((ret, settle, 'retreat 6 b'))
            g.at(settle, FACE)
        # F2 (HR-23): the tell's cards follow her (she retreats while it shows: the ring hugs her upper body, C49)
        g.at(yel, K.fixed('follow_on'))
        g.fx(yel, 'yellow_tell', [part(DUST['yellow'], 0.5, 0.6, 0.5, 0, 30), part('minecraft:end_rod', 1.2, 0.05, 0.05, 0, 8)],
             at_body(1.0), src=('a7_tell', 'yellow'), t=8)
        g.at(yel, K.fixed('follow_off'))
        g.snd(yel, 'yellow_chime', src=('a7_tell', 'yellow'))

    def s_a7_throw(self, t, step, kb=0, cond=None):
        g = self.gb
        cr, sp, rel = (t + E('a7_throw', k) for k in ('crescent', 'spin', 'release'))

        def at(tt, *lines):
            g.at(tt, *[S.gate(cond, x) if cond else x for x in lines if x])
        at(t, api.play('a7_throw'), FACE)
        g.ev(t, 'clip', 'a7_throw', ('a7_throw', 0))
        at(cr, *S.fx('qi_vert', [part(DUST['lilac'], 0.2, 1.0, 0.2, 0, 16)], pos=f'{S.AT_BODY} positioned ^0.6 ^0.15 ^0.4',
                     h=19, yaw=0, c=api.C_LILAC))
        g.ev(cr, 'fx', 'qi_vert', ('a7_throw', 'crescent'))
        ring = {'disc2': 16, 'throw2': 12}.get(step, 12)
        at(sp, *S.fx('qi_ring', ring_fb(ring / 10), pos=at_body(0.8), r=ring, c=api.C_LILAC))
        g.ev(sp, 'fx', 'qi_ring', ('a7_throw', 'spin'))
        if step == 'disc1':
            g.look(sp, 'blade', 'gold', ('a7_throw', 'spin'))
            g.look(rel, 'blade', 'off', ('a7_throw', 'release'))
        if step == 'disc3':
            at(sp, *S.fx('qi_wedge', [part(DUST['lilac'], 0.4, 0.4, 0.4, 0, 12)], pos=at_body(0.85), r=14, roll=30))
            g.ev(sp, 'fx', 'qi_wedge', ('a7_throw', 'spin'))
        # F1 (HR-15): the aim locks LOCK_LEAD t before the release (g/disc/lock: the marker at the player's feet, she faces it);
        # at the release she faces the lock (not the player), g/disc/throw aims there
        lk = rel - api.LOCK_LEAD
        at(lk, fn('g/disc/lock'))
        g.ev(lk, 'lock', 'disc', ('a7_throw', 'release - LOCK_LEAD'))
        at(rel, FACE_LOCK)
        g.disc(rel, kb, step, cond)
        at(rel, *S.snd('disc_release'), *S.snd('disc_fly'))
        g.ev(rel, 'snd', 'disc_release', ('a7_throw', 'release'))
        g.ev(rel, 'snd', 'disc_fly', ('a7_throw', 'release'))

    def s_vanish(self, t):                            # A13 vanish 5 (purple glow + white ring)
        g = self.gb
        g.fx(t, 'ghost_burst', puff_fb(), at_body(0.95), src=('script', 'vanish'))
        g.fx(t, 'qi_ring', ring_fb(1.4, 'white'), at_body(0.8), src=('script', 'vanish'), r=14, c=api.C_WHITE)
        g.at(t, hide())
        g.ev(t, 'rig', 'state/hidden', ('script', 'vanish'))

    def s_reform(self, t):                            # R1 / R3: she reforms in her normal colours
        g = self.gb
        g.play(t, 'g_reform')
        g.look(t + E('g_reform', 'solid'), 'form', 'normal', ('g_reform', 'solid'))
        # F1 round 1 (HR-14): from the solid row on her tail moves her with the recovery's clip (s_solid); idle2 only when
        # the reform clip ends before that row
        solid = next((r[0] for r in self.rows if r[1] == 'solid'), None)
        te = t + E('g_reform', 'end')
        if solid is None or te < solid:
            g.at(te, api.play('idle2'))
            g.ev(te, 'clip', 'idle2', ('g_reform', 'end'))

    def s_solid(self, t, end_t):
        """R1 / R3: hittable again; the reform tail to the end (<= 12 t after the last hit) turns her to the player and
        (F1 round 1, HR-14 / VF1R-01) moves her as the recovery does (ai/tail at the row, ai/tail_step each later tick)."""
        g = self.gb
        g.at(t, f'tag @s remove {TAG_GHOST}')
        g.ev(t, 'tag', 'ghost-', ('script', 'solid'))
        g.rng(t, end_t - 1, f'function rlk:mboss/mv/turn {{max:{api.TRACK["deg"]}}}')
        assert t < end_t - 1, (self.key, t, end_t)
        g.at(t, fn('ai/tail'))
        g.rng(t + 1, end_t - 1, fn('ai/tail_step'))
        g.moves.append((t + 1, end_t - 1, 'tail move'))

    # ------------------------------------------------------------------ the whole script
    def build(self):
        g, key = self.gb, self.key
        end_t = next((r[0] for r in self.rows if r[1] == 'end'), None)
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
            elif step == 'tell':
                self.s_a7_tell(t)
            elif step in ('disc1', 'disc2', 'disc3'):
                self.s_a7_throw(t, step)
            elif step == 'vanish':
                self.s_vanish(t)
            elif step == 'reform':
                self.s_reform(t)
            elif step == 'solid':
                self.s_solid(t, end_t)
            elif step == 'end':
                g.end(t)
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
            g.cancel_lines += S.hud('warn', on=0) + [x for x in (api.arena_look('crimson'),) if x]
        return g


# ================================================================================================= the patterns
def build_r1(W):
    g_files(W)
    w = Walk('r1', W)
    w.build().write('P2: the ghost rush, the gauntlets\' opening block without shield or darkness')


def build_r3(W):
    g_files(W)
    w = Walk('r3', W)
    w.build().write('P2: the ghost glide, the gauntlets\' second block without shield or darkness')


def build_r2(W):
    """R2 월륜 일섬 (PLAN §4.4): the yellow tell, the retreat, one moon disc (kb 2); at <= R2_TWO_PCT % of her HP a second
    disc (aimed anew; the first kb 0, the last kb 2). She is solid (no ghost) throughout."""
    g_files(W)
    w = Walk('r2', W)
    g = w.gb
    two = f'if score #r2_two {OBJ} matches 1'
    one = f'unless score #r2_two {OBJ} matches 1'
    g.start_head += [
        f'# the second disc at <= {api.R2_TWO_PCT} % of her max HP (#r2_two 1): 100 x HP <= {api.R2_TWO_PCT} x max HP',
        sset('#r2_two', 0), f'scoreboard players operation #r2_a {OBJ} = @s mhpC', f'scoreboard players operation #r2_a {OBJ} *= #c100 {OBJ}',
        f'scoreboard players operation #r2_b {OBJ} = @s mhpM', sset('#r2_c', api.R2_TWO_PCT),
        f'scoreboard players operation #r2_b {OBJ} *= #r2_c {OBJ}',
        f'execute if score #r2_a {OBJ} <= #r2_b {OBJ} run {sset("#r2_two", 1)}']
    for t, step, clip, c in w.rows:
        if step == 'tell':
            w.s_a7_tell(t)
        elif step == 'throw':
            w.s_a7_throw(t, 'throw', kb=api.DISC['kb'], cond=two)
            w.s_a7_throw(t, 'throw', kb=api.DISC['kb_last_r2'], cond=one)
        elif step == 'throw2':
            w.s_a7_throw(t, 'throw2', kb=api.DISC['kb_last_r2'], cond=two)
        elif step == 'end':
            g.end(t)
    rel1 = 16 + E('a7_throw', 'release')
    rel2 = 30 + E('a7_throw', 'release')
    # F1 (HR-14, lead decision 11-05: "during any tail kept and in the recovery she walks / strafes facing and tracking the
    # player"): R2's tail after its last release is kept (its end stays); TAIL_MOVE t after it she moves as the recovery
    # does - glides in beyond 6 b, else strafes (ai/tail, ai/tail_step; the recovery keeps the move) - turning to the player
    # every tick
    W.w('p/r2/step', ['# One tick of R2\'s tail (@s = the body): turn to the player, one step of the move (mv/ok-checked).',
                      f'function rlk:mboss/mv/turn {{max:{api.TRACK["deg"]}}}', fn('ai/tail_step')])
    tm = api.TAIL_MOVE
    g.at(rel1 + tm, S.gate(one, fn('ai/tail')))
    g.at(rel2 + tm, S.gate(two, fn('ai/tail')))
    g.rng(rel1 + tm + 1, w.rows[-1][0] - 1, S.gate(one, fn('p/r2/step')))
    g.rng(rel2 + tm + 1, w.rows[-1][0] - 1, S.gate(two, fn('p/r2/step')))
    g.moves += [(rel1 + tm, w.rows[-1][0], 'tail move (one disc)'), (rel2 + tm, w.rows[-1][0], 'tail move (two discs)')]
    g.write('P2: the moon disc after the yellow tell')


def build_gauntlet(key):
    def build(W):
        g_files(W)
        w = Walk(key, W)
        w.build().write('the 60 % gauntlet' if key == 'a8' else 'the 5 % ultimate gauntlet')
    return build


BUILD = {'r1': build_r1, 'r2': build_r2, 'r3': build_r3, 'a8': build_gauntlet('a8'), 'a13': build_gauntlet('a13')}
NOTES = {'r1': 'ghost rush: tell, D1 far dash, ring / rising / leaping cuts (T2, T2, T3 kb 3), reform',
         'r2': 'yellow tell, retreat, one moon disc (two at <= 30 % HP)',
         'r3': 'ghost glide: tell, D2 low glide, sweep + X (T2, T3 kb 3), reform',
         'a8': 'the 60 % gauntlet: 9 counting cuts, the dive = the judge (deflect -> CS2, fail -> fail60 -> P2)',
         'a13': 'the 5 % ultimate: 9 counting cuts + 3 moon discs, the dive = the judge (deflect -> CS3, fail -> the instant death)'}


def _clips(key):
    return tuple(sorted({r[2] for r in api.SCRIPTS[key] if r[2] and r[0] >= 0}
                        | ({'g_reform', 'idle2'} if key in ('r1', 'r3', 'a8', 'a13', 'r2') else set())))


PATTERNS = [api.Pattern(k, S.TID[k], _clips(k), BUILD[k], notes=NOTES[k]) for k in api.P2]
assert [p.key for p in PATTERNS] == list(api.P2)
