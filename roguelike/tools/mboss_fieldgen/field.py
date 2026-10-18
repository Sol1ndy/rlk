"""Field-form patterns of the field generator (stage 2, the field-pattern author; specs scratchpad mb3/spec
W_gravity_waves.md, F1_reduction_zone.md, F2_field_rocks.md, accepted answers spec/README.md section 5 and plan.md
"Stage-2 decisions").

    11 fzone  F1 중력 시스템·감소 영역   9 eruption events (the footage's ticks), 1-4 dark discs r 2.8 each, one hit per event
    12 frock  F2 중력 시스템·파쇄        C6 without the tower: 8 floor bursts on an arc onto the player (7-8 one volley
                                         group), the lifted slabs, 5 slab throws (at most 2 slab hits per run)
    21 waves  「인력 충격파」 x3          service: the core runs it at the field's start (#fgWvK 1) and end (2); the 3rd wave
                                         plays wave_long (opening) / wave_drop (closing) when the rig has them; below
                                         50 % HP (or test 42) the 3rd wave fires 3 fronts 6 t apart (spec Q2)

The device sits at the arena centre for the whole field (the core put it there) and tracks the player at 3 deg/t;
low gravity is on and the meter is open while these run. Every damaging hazard is quiet (#hzQuiet 1) and silent
(#hzSfx 0) and is paired, in the same tick with the same tell, with the kit's violet field decal (el 9; every hit is
still Geo); the sounds are the kit's recipes plus the specs' single vanilla layers (never both for one event).
Every rig tick is read with ev_or() / clip_len() (stub defaults), so the timelines follow the real manifest.

Butterfly review lessons applied (scratchpad mb2/review): every marker a pattern summons is killed before its summon
and carries rlk_mb_fg_pat (killed by the core at p/finish and p/cancel); the throw locks go through g.keep (S1 /
perf-1); g.release is never used (S2); every volley group's members exist before its first strike (FW-4: an F1 event's
discs are made in one tick, F2's bursts 7-8 are made 6 t apart, before the first strikes); the slab blade reach is
derived from the framework's blade pad (FW-1, Q16); after a pause every live quiet hazard of the pattern gets its kit
decal back with the remaining tell (FX-1: the core clears the decals on pause and nothing else redraws them; the
`pause` hook sets #fq<id>P, the next pattern tick redraws); the waves' fx stay within the kit's card caps (FX-2, the
suite counts skipped card calls with the game's schedule order, FX-7).
Pattern scores #fq<id>*, tags rlk_mb_fg_p<id>* + rlk_mb_fg_pat, storage rlk:mboss fg.fz / fg.f2 / fg.f2l / fg.rd /
fg.rw.
"""
import math

from .api import (Pattern, TL, ev_or, clip_len, CLIPS, DMG, KB, CY, NS, L, CORE_FIELD_H, rest_anchor, f_clip_anchor,
                  f_body_pos, rocks_cancel)

BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'
KFN = 'function rlk:mboss/fieldgen/fx/'
EL = 9                                       # the kit's field violet decal palette (every hit stays Geo)
TURN = 'function rlk:mboss/mv/turn {max:3}'  # the field idle's tracking (face/track for the look only)
CORE_H = CORE_FIELD_H                        # 4.1: the field core
RING_H = rest_anchor('field', 'ring_centre', (0, 5.8, 0))[1]
MEDAL_E = f_body_pos(rest_anchor('field', 'medal_e', (3.85, 4.1, 0.0)))
MEDAL_G = f_body_pos(rest_anchor('field', 'medal_g', (-3.85, 4.1, 0.0)))


def tags(pid, *more):
    return ','.join(f'"{t}"' for t in ('rlk_room', 'rlk_mb_aux', 'rlk_mb_fg_pat', f'rlk_mb_fg_p{pid}') + more)


def ex(cond, line):
    """`line` under the execute sub-commands `cond` (merged when the line is an execute itself)."""
    if line.startswith('execute '):
        return f'execute {cond} {line[len("execute "):]}'
    return f'execute {cond} run {line}'


def at_core(line, h=None):
    return f'execute positioned ~ ~{L.num(float(CORE_H if h is None else h), 3)} ~ run {line}'


def body_rot(pos, line):
    return f'execute rotated as @s rotated ~ 0 positioned {pos} run {line}'


# ---------------------------------------------------------------------------------------------
# F1 감소 영역 (spec F1): the footage's event ticks (F1 fix), decals 15 t ahead, the end at 260
F1_ACT = ev_or('field_erupt', 'erupt', 22)
F1_LOCK = ev_or('field_erupt', 'lock', 12)
F1_GAPS = (0, 50, 80, 98, 119, 148, 159, 198, 209)      # decals 22 72 102 120 141 170 181 220 231, strikes + 15
F1_EVENTS = [F1_ACT + d for d in F1_GAPS]               # the decal ticks (each event's discs are made together)
F1_TELL = 15
F1_STRIKES = [t + F1_TELL for t in F1_EVENTS]           # 37 87 117 135 156 185 196 235 246 (gaps 11-50)
F1_END = F1_ACT + 238                                   # 260: the last eruption + the tilt
F1_OFF = F1_ACT + 184                                   # 206: the link beams off
assert all(11 <= b - a <= 50 for a, b in zip(F1_STRIKES, F1_STRIKES[1:])), F1_STRIKES

# F2 파쇄 in the field form (spec F2): the rig's frock clip (fallback field_erupt), C6's arc walker, cap and pair
F2_CLIP = 'frock' if 'frock' in CLIPS else 'field_erupt'
F2_BURST = ev_or('frock', 'burst', 25)                  # the first burst strikes; then every F2_GAP t
F2_THROW = ev_or('frock', 'throw', 65)                  # the first throw; then every F2_TGAP t
F2_FLAME = ev_or('frock', 'flame', 8)
F2_CRUMBLE = ev_or('frock', 'end', 100)                 # every unthrown slab crumbles
F2_END = clip_len('frock') if 'frock' in CLIPS else 110
F2_GAP, F2_N, F2_TGAP, F2_NT, F2_CAP = 6, 8, 8, 5, 2
F2_THETA = [round(90 * (7 - k) / 7) for k in range(F2_N)]    # the arc offsets 90 77 64 51 39 26 13 0 (C6 F1)
F2_PAIR = 6                                              # bursts 7-8 (index 6, 7) share one volley group
SLAB_REACH = 1.45                                        # the slab's reach from its flight line (the w 2.4 line + pad)
BLADE_PAD = 0.65                                         # the framework blade's point radius (FW-1: reach = hr + 0.65)
SLAB_HR = round(SLAB_REACH - BLADE_PAD, 2)               # 0.8 (Q16: if the blade pad changes, only BLADE_PAD moves)
SLAB_RISE = (4.0, 5.0, 6.0, 4.5, 5.5, 4.0, 6.0, 5.0)     # the slabs hover 4-6 b up (spec C6 section 7)
assert F2_THROW - 10 > F2_BURST + F2_GAP * (F2_NT - 1) + 2 and F2_CRUMBLE > F2_THROW + F2_TGAP * (F2_NT - 1)
assert F2_END >= F2_THROW + F2_TGAP * (F2_NT - 1) + 8

# 「인력 충격파」 (spec W): impacts W_IMPACT (gaps 68 / 83); waves 1-2 play `wave` and charge for its impact tick; the
# 3rd plays wave_long (opening) / wave_drop (closing) with the hazard made at the clip start (tell = its impact), or,
# with the stub rig, `wave` and a 40 t charge
W_IMP0 = ev_or('wave', 'impact', 24)
W_IMPACT = (W_IMP0, W_IMP0 + 68, W_IMP0 + 68 + 83)
W3_FB_TELL = 40
W3_CLIP = {1: 'wave_long' if 'wave_long' in CLIPS else None, 2: 'wave_drop' if 'wave_drop' in CLIPS else None}
W_TRI_GAP = 6            # plan 9; spec Q2 (accepted): 3 fronts 6 t apart, one low-gravity jump clears all three
W_SPEED = 0.55           # front speed, b/t (r = 2.5 + 0.55 k after the impact)
W_BAND = 2.5             # hit band [r - 2.5, r], 0..0.7 b high
W_ACT = 36               # active ticks (r 2.5 -> 21.75: past the wall)
W_DUR = 34               # the kit ring / fire band travel: 2.5 -> 21.2 b in 34 t, exactly the hazard's 0.55 b/t
W_R1 = W_BAND + W_SPEED * W_DUR
W_TAIL = 37              # the pattern ends 37 t after its last strike: the front has expired
VG = {1: 'unless score #fgWvK mb matches 2', 2: 'if score #fgWvK mb matches 2'}     # opening / closing variant


def _w3(v):
    clip = W3_CLIP[v]
    tell = ev_or(clip, 'impact', W3_FB_TELL) if clip else W3_FB_TELL
    start = W_IMPACT[2] - tell
    name = clip or 'wave'
    clip_at = start if clip else W_IMPACT[2] - W_IMP0
    core = f_clip_anchor(clip, 'impact', 'core', (0, CORE_H, 0))[1] if clip else CORE_H
    return dict(clip=name, real=bool(clip), tell=tell, start=start, clip_at=clip_at, end=clip_at + clip_len(name),
                core=core)


W3 = {v: _w3(v) for v in (1, 2)}
W3_SAME = W3[1] == W3[2]           # one 3rd wave for both (the stub rig): no variant guards
W_ENDS = {(v, tri): max(W_IMPACT[2] + (2 * W_TRI_GAP if tri else 0) + W_TAIL, W3[v]['end']) for v in (1, 2) for tri in (0, 1)}
W_LEN, W_MAX = W_ENDS[(1, 0)], max(W_ENDS.values())
W_CHARGE = (W_IMP0, W_IMP0, W3[1]['tell'])               # the opening's charges (the stub: 24 / 24 / 40)
assert W_IMPACT[1] - W_IMPACT[0] == 68 and W_IMPACT[2] - W_IMPACT[1] == 83
assert all(W3[v]['start'] > W_IMPACT[1] and W3[v]['clip_at'] > W_IMPACT[1] for v in (1, 2))

PATTERNS = [
    Pattern(11, 'fzone', '중력 시스템·감소 영역', 'f', 'field_erupt', bands=('melee', 'mid', 'far'), recover=14,
            max_len=F1_END + 8, length=F1_END),
    Pattern(12, 'frock', '중력 시스템·파쇄', 'f', F2_CLIP, bands=('melee', 'mid', 'far'), recover=14,
            max_len=F2_END + 8, length=F2_END),
    Pattern(21, 'waves', '「인력 충격파」', 'f', 'wave', kind='service',
            recover=0, max_len=W_MAX + 8, length=W_LEN),
]


def emit(g):
    fzone(g)
    frock(g)
    waves(g)


# ---------------------------------------------------------------------------------------------
def redraw_fns(g, key, pid, shapes):
    """FX-1: after a pause, every live quiet hazard of the pattern gets its kit decal back with the remaining tell.
    `pause` (the core calls it once when the fight freezes) sets #fq<pid>P; the next pattern tick runs `redraw`.
    shapes: [(hazard tag, decal function rd_<n>)]; rd_<n> runs as the hazard marker with #fgX = the ticks left to its
    strike (>= 1; the module tick runs before this tick's hz/all)."""
    g.pw(key, 'pause', ['# The fight froze (the core cleared the kit decals): redraw them on the first tick after the resume.',
                        f'scoreboard players set #fq{pid}P mb 1'])
    lines = ['# First pattern tick after a pause: the decals of the live quiet hazards again, with the remaining tell.',
             f'scoreboard players set #fq{pid}P mb 0']
    for tag, fn in shapes:
        lines.append(f'execute as @e[type=minecraft:marker,tag={tag}] at @s rotated as @s run function {NS}p/{key}/{fn}')
    g.pw(key, 'redraw', lines)
    return f'execute if score #fq{pid}P mb matches 1 run function {NS}p/{key}/redraw'


def tell_left():
    """As a hazard marker (module tick): #fgX = ticks to its strike (mbHzW - mbHzT - 1); return when it struck."""
    return ['scoreboard players operation #fgX mb = @s mbHzW',
            'scoreboard players operation #fgX mb -= @s mbHzT',
            'scoreboard players remove #fgX mb 1',
            'execute if score #fgX mb matches ..0 run return 0',
            'execute store result storage rlk:mboss fg.rd.tell int 1 run scoreboard players get #fgX mb']


def rd_disc(g, key, name, r):
    g.pw(key, name, [f'# @s = a live disc hazard (r {L.num(r)}): its kit decal with the remaining tell.'] + tell_left() + [
        f'data modify storage rlk:mboss fg.rd merge value {{r:{int(round(r * 10))},el:{EL},hold:3}}',
        f'execute rotated ~ 0 run {KFN}tele/disc with storage rlk:mboss fg.rd'])


# ---------------------------------------------------------------------------------------------
def fzone(g):
    """F1 감소 영역 (field_erupt): the arch locks, the medallions slide out on gold link beams (activation 0-22), then 9
    eruption events at the footage's ticks (decals at F1_EVENTS, strikes 15 t later, gaps 11-50): 1-4 discs r 2.8
    (hz/disc, tell 15, height to 3.5 b: not jumpable even in low gravity, KB 3, Geo 1.2), the first 2-3 b from the
    player's feet (a standing player is inside it, 0.1-1.1 b from its edge), the others 2-8 b, random yaws, inside
    the walk disc; all discs of an event are one volley group made in one tick (one hit per event). Each disc: the
    violet kit decal + the dark erupt_tell disc; the gold eruption, then hovering debris; one tell / eruption sound
    per event (on its first disc)."""
    key, tl, pid = 'fzone', TL(g, 'fzone'), 11
    D, Z, FST = 'rlk_mb_fg_p11d', 'rlk_mb_fg_p11z', 'rlk_mb_fg_p11f'
    g.pw(key, 'event', [
        '# One eruption event (@s = body): 1-4 discs, the first 2-3 b off the player, the others 2-8 b; one volley group.',
        g.GRP_NEW,
        'execute store result score #fq11N mb run random value 1..4',
        'execute store result storage rlk:mboss fg.fz.d double 0.1 run random value 20..30',
        'scoreboard players set #fq11F mb 1',
        f'function {NS}p/{key}/disc',
        f'function {NS}p/{key}/more'])
    g.pw(key, 'more', [
        'scoreboard players remove #fq11N mb 1',
        'execute if score #fq11N mb matches ..0 run return 0',
        'execute store result storage rlk:mboss fg.fz.d double 0.1 run random value 20..80',
        f'function {NS}p/{key}/disc',
        f'function {NS}p/{key}/more'])
    mk = f'at @e[type=minecraft:marker,tag={D},limit=1]'
    g.pw(key, 'disc', [
        '# A random yaw and the distance fg.fz.d from the player: a marker, pulled into the walk disc; the quiet hazard,',
        '# the violet decal (same tell) and the dark disc there. The event\'s first disc carries its sounds.',
        f'kill @e[type=minecraft:marker,tag={D}]',
        'execute store result storage rlk:mboss fg.fz.a double 1 run random value 0..359',
        f'function {NS}p/{key}/place with storage rlk:mboss fg.fz',
        f'execute as @e[type=minecraft:marker,tag={D}] run {g.clamp_walk()}',
        *g.hz_opts(kb=KB['default'], grp=True, quiet=1, sfx=0, vis=111),
        ex(mk, g.hz_disc(2.8, F1_TELL, DMG['f1'])),
        g.tag_last_hz(Z),
        ex('if score #fq11F mb matches 1', g.tag_last_hz(FST)),
        ex(mk + ' rotated ~ 0', g.tele_disc(2.8, F1_TELL, el=EL)),
        ex(mk, g.fx('erupt_tell')),
        ex('if score #fq11F mb matches 1 ' + mk, g.snd('erupt_tell')),
        'scoreboard players set #fq11F mb 0',
        f'kill @e[type=minecraft:marker,tag={D}]'])
    g.pw(key, 'place', [f'$execute at {PLAYER} rotated $(a) 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ {CY} ~ '
                        f'{{Tags:[{tags(pid, D)}]}}'])
    rd_disc(g, key, 'rd', 2.8)
    redraw = redraw_fns(g, key, pid, [(Z, 'rd')])
    # activation (spec F1 section 4)
    tl.at(0, body_rot(MEDAL_E, g.fx('spark')), body_rot(MEDAL_G, g.fx('spark')),
          g.sound('block.beacon.activate', 0.7, 1.3), g.sound('block.conduit.activate', 0.6, 1.2),
          g.sound('block.crafter.craft', 0.6, 0.7))
    half = lambda p: f_body_pos(tuple(v / 2 if i != 1 else v for i, v in enumerate(p)))        # noqa: E731
    tl.at(6, body_rot(half(rest_anchor('field', 'medal_e', (3.85, 4.1, 0.0))), g.fx('spark')),
          body_rot(half(rest_anchor('field', 'medal_g', (-3.85, 4.1, 0.0))), g.fx('spark')))
    tl.at(F1_LOCK, g.sound('block.chain.place', 0.5, 1.2))
    tl.at(F1_ACT, at_core(g.fx('flash')))
    for t in F1_EVENTS:
        tl.at(t, f'function {NS}p/{key}/event')
    for t in F1_STRIKES:
        tl.at(t + 25, g.snd('debris_land'))
    tl.at(F1_OFF, g.sound('block.chain.place', 0.6, 0.9), g.sound('block.copper_trapdoor.close', 0.6, 0.9))
    tl.at(F1_END, g.play('field_idle'), g.end())
    tl.write([f'# F1 감소 영역 (clip field_erupt; @s = body at the centre): decals {F1_EVENTS} (strike +{F1_TELL}), end {F1_END}.',
              'scoreboard players set #fq11P mb 0'],
             ['# fzone tick: track the player (3 deg/t), the decals again after a pause.'], extra_tick=[TURN, redraw])
    g.pw(key, 'vis', ['# @s = an eruption disc: 1 = it erupts (gold mound; the event\'s first disc plays the sound), 2 = it',
                      '# ended (the chunks hover and drift down).',
                      'execute if score #hzEv mb matches 1 run ' + g.fx('erupt'),
                      f'execute if score #hzEv mb matches 1 if entity @s[tag={FST}] run ' + g.snd('erupt'),
                      'execute if score #hzEv mb matches 2 run ' + g.fx('debris')])
    g.pw(key, 'cancel', ['# The placement marker and the discs (lib_clear usually got the hazards first).',
                         'kill @e[tag=rlk_mb_fg_p11]', f'kill @e[type=minecraft:marker,tag={Z}]', 'scoreboard players set #fq11P mb 0'])


# ---------------------------------------------------------------------------------------------
def _quat(yaw_deg, tilt_deg):
    """left_rotation of a lifted slab: a small tilt about x, then a turn about y."""
    hy, hx = math.radians(yaw_deg) / 2, math.radians(tilt_deg) / 2
    qy = (0.0, math.sin(hy), 0.0, math.cos(hy))
    qx = (math.sin(hx), 0.0, 0.0, math.cos(hx))
    x1, y1, z1, w1 = qy
    x2, y2, z2, w2 = qx
    q = (w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
         w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2)
    return ','.join(L.num(v, 4) + 'f' for v in q)


def frock(g):
    """F2 파쇄 in the field form (frock; C6 without the tower build-up): the vent column (0) and the pulsing flame band
    under the ring (8, 16) are the long read; then 8 floor bursts 6 t apart on an arc that converges on the player
    (burst k at the player's current distance from the device, clamped 2.5-18 b, at the bearing turned by
    sigma * 90 (7 - k) / 7 deg; sigma drawn once), each hz/disc r 1.8 (tell 10, jumpable: height to 1.2 b, KB 4, Geo
    1.3) with a violet decal; bursts 7-8 are one volley group (a standing player takes one burst); a kit slab tears out
    at every burst and hovers 4-6 b up; from the throw tick one slab every 8 t at the player's feet locked 10 t ahead
    (a dmg-0 line w 2.4 + the violet line decal, then a blade pj 1.5 b/t, reach 1.45 b, KB 3, Geo 1.1, life 24, its
    own group); at most 2 slab hits per run (the later throws crumble); every unthrown slab crumbles at the clip end."""
    key, tl, pid = 'frock', TL(g, 'frock'), 12
    W, S, R, Fl = 'rlk_mb_fg_p12w', 'rlk_mb_fg_p12s', 'rlk_mb_fg_p12r', 'rlk_mb_fg_p12f'
    Z, Y, TLK = 'rlk_mb_fg_p12z', 'rlk_mb_fg_p12y', 'rlk_mb_fg_p12tl'
    walker = f'@e[type=minecraft:marker,tag={W},limit=1]'
    slab = lambda j: f'@e[type=minecraft:item_display,tag={S},scores={{mbS={j}}},limit=1]'     # noqa: E731
    g.pw(key, 'place', [f'$execute at {BODY} facing entity {PLAYER} feet rotated ~$(a) 0 positioned ^ ^ ^$(d) run summon '
                        f'minecraft:marker ~ {CY} ~ {{Tags:[{tags(pid, W)}]}}'])
    for k in range(F2_N):
        th = F2_THETA[k]
        mk = f'at {walker}'
        lines = [
            f'# Burst {k + 1} decal (@s = body): the arc point {th} deg off the bearing to the player (side #fq12S), at the',
            '# player\'s distance from the device (2.5-18 b), in the walk disc; the quiet hazard + the violet decal; the',
            '# slab, hidden until the strike.' + (' Bursts 7-8 share one volley group (made before its first strike).' if k == F2_PAIR else ''),
            'function rlk:mboss/mv/dist',
            'scoreboard players operation #fq12D mb = #mbDist mb',
            'execute if score #fq12D mb matches ..24 run scoreboard players set #fq12D mb 25',
            'execute if score #fq12D mb matches 181.. run scoreboard players set #fq12D mb 180',
            'execute store result storage rlk:mboss fg.f2.d double 0.1 run scoreboard players get #fq12D mb',
            f'execute if score #fq12S mb matches 1 run data modify storage rlk:mboss fg.f2.a set value {th}',
            f'execute unless score #fq12S mb matches 1 run data modify storage rlk:mboss fg.f2.a set value {-th}',
            f'kill @e[type=minecraft:marker,tag={W}]',
            f'function {NS}p/{key}/place with storage rlk:mboss fg.f2',
            f'execute as {walker} run {g.clamp_walk()}']
        if k == F2_PAIR:
            lines.append(g.GRP_NEW)
        lines += [*g.hz_opts(kb=KB['heavy'], y1=1.2, vis=pid * 10 + 1, quiet=1, sfx=0, grp=k >= F2_PAIR),
                  ex(mk, g.hz_disc(1.8, 10, DMG['f2'])),
                  g.tag_last_hz(Z),
                  ex(mk + ' rotated ~ 0', g.tele_disc(1.8, 10, el=EL)),
                  ex(mk, g.sound('block.amethyst_block.resonate', 0.3, 1.4)),
                  ex(mk, f'summon minecraft:item_display ~ ~0.45 ~ {{Tags:[{tags(pid, S, "rlk_mb_fg_pnew")}],teleport_duration:12}}'),
                  'execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run ' + g.kprop('slab'),
                  'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew,limit=1] {transformation:{translation:[0f,0f,0f],'
                  'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}',
                  f'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS {k + 1}',
                  'tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew',
                  f'kill @e[type=minecraft:marker,tag={W}]']
        g.pw(key, f'burst{k}', lines)
        g.pw(key, f'rise{k}', [
            f'# @s = slab {k + 1}, its burst just struck: it tears out and rises {L.num(SLAB_RISE[k])} b over 12 t with a slow tumble.',
            'data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[0f,0f,0f],'
            f'left_rotation:[{_quat(25 * k + 10, 8 if k % 2 else -8)}],right_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f]}}}}',
            f'tag @s add {R}',
            f'execute positioned ~ {CY} ~ run ' + g.fx('slab_rise'),
            g.snd('slab_lift'),
            f'tp @s ~ ~{L.num(SLAB_RISE[k])} ~'])
        t_strike = F2_BURST + F2_GAP * k
        tl.at(t_strike - 10, f'function {NS}p/{key}/burst{k}')
        tl.at(t_strike + 2, f'execute as {slab(k + 1)} at @s run function {NS}p/{key}/rise{k}')
    g.pw(key, 'tl_line', [
        '# @s = the slab about to be thrown, at it: the throw line from its floor point to the locked feet (a quiet dmg-0',
        '# hz/line w 2.4, tell 10, and the violet kit line with the same tell).',
        'function rlk:mboss/mv/dist',
        'execute store result storage rlk:mboss fg.f2l.len int 1 run scoreboard players get #mbDist mb',
        f'data modify storage rlk:mboss fg.f2l merge value {{w:24,back:0,tell:10,el:{EL},hold:3,dmg:0}}',
        *g.hz_opts(quiet=1, sfx=0),
        f'execute positioned ~ {CY} ~ facing entity @e[type=minecraft:marker,tag={TLK},limit=1] feet run '
        'function rlk:mboss/hz/line with storage rlk:mboss fg.f2l',
        g.tag_last_hz(Y),
        f'execute positioned ~ {CY} ~ facing entity @e[type=minecraft:marker,tag={TLK},limit=1] feet rotated ~ 0 run '
        f'{KFN}tele/line with storage rlk:mboss fg.f2l',
        g.sound('block.chain.hit', 0.5, 0.8)])
    g.pw(key, 'throw_go', [
        f'# @s = the slab: a blade projectile at the locked feet (1.5 b/t, life 24, hr {L.num(SLAB_HR)} = reach {L.num(SLAB_REACH)} b, its own group).',
        f'scoreboard players set @s mbId {pid}',
        f'tag @s remove {S}', f'tag @s remove {R}', f'tag @s add {Fl}',
        'data merge entity @s {teleport_duration:1}',
        *g.pj_opts(shape=1, kb=KB['default'], wall=1, grp=True),
        f'execute at @s facing entity @e[type=minecraft:marker,tag={TLK},limit=1] feet run {g.pj_launch(1.5, 24, DMG["f2s"], SLAB_HR)}',
        'execute at @s rotated as @s run ' + g.fx('slab_throw'),
        g.snd('slab_throw')])
    for j in range(F2_NT):
        T = f'rlk_mb_fg_p12t{j}'
        g.pw(key, f'crumble{j}', [
            f'# The slab cap ({F2_CAP} slab hits) is reached: slab {j + 1} crumbles instead of being thrown.',
            f'execute as {slab(j + 1)} at @s positioned ~ {CY} ~ run ' + g.fx('slab_impact'),
            f'execute as {slab(j + 1)} at @s run ' + g.snd('debris_land'),
            f'kill {slab(j + 1)}', f'kill @e[type=minecraft:marker,tag={T}]'])
        g.pw(key, f'throw_tell{j}', [
            f'# Throw {j + 1} tell (@s = body): lock the player\'s feet ({T}, kept) and draw the line from slab {j + 1}.',
            f'execute if score #fq12SH mb matches {F2_CAP}.. run return run function {NS}p/{key}/crumble{j}',
            g.lockp(), *g.keep(T),
            f'tag @e[type=minecraft:marker,tag={T}] add {TLK}',
            f'execute as {slab(j + 1)} at @s run function {NS}p/{key}/tl_line',
            f'tag @e[type=minecraft:marker,tag={T}] remove {TLK}'])
        g.pw(key, f'throw{j}', [
            f'# Throw {j + 1}: slab {j + 1} flies at lock {T} (unless the cap is reached).',
            f'execute if score #fq12SH mb matches {F2_CAP}.. run return run function {NS}p/{key}/crumble{j}',
            g.GRP_NEW,
            f'tag @e[type=minecraft:marker,tag={T}] add {TLK}',
            f'execute as {slab(j + 1)} run function {NS}p/{key}/throw_go',
            f'kill @e[type=minecraft:marker,tag={T}]'])
        tl.at(F2_THROW + F2_TGAP * j - 10, f'function {NS}p/{key}/throw_tell{j}')
        tl.at(F2_THROW + F2_TGAP * j, f'function {NS}p/{key}/throw{j}')
    g.pw(key, 'crumble', ['# The clip end: every unthrown slab crumbles where it hovers.',
                          f'execute as @e[type=minecraft:item_display,tag={S}] at @s positioned ~ {CY} ~ run ' + g.fx('slab_impact'),
                          f'kill @e[type=minecraft:item_display,tag={S}]',
                          g.snd('debris_land'), g.sound('block.piston.contract', 0.5, 0.9)])
    g.pw(key, 'pj_end', [
        '# A thrown slab ends: 1 floor / wall, 2 life -> it shatters (slab_impact on the floor under it); 4 = it hit the',
        f'# player: one more slab hit toward the cap ({F2_CAP}); the slab flies on, harmless (its group struck).',
        f'execute if score #pjEv mb matches 4 run scoreboard players add #fq{pid}SH mb 1',
        f'execute if score #pjEv mb matches 1..2 at @s positioned ~ {CY} ~ run ' + g.fx('slab_impact'),
        'execute if score #pjEv mb matches 1..2 at @s run ' + g.snd('slab_impact'),
        'execute if score #pjEv mb matches 1..2 run scoreboard players set #pjKeep mb 0'])
    rd_disc(g, key, 'rd', 1.8)
    g.pw(key, 'rd_line', ['# @s = a live throw line (dmg 0): its kit line with the remaining tell.'] + tell_left() + [
        'execute store result storage rlk:mboss fg.rd.len int 0.01 run scoreboard players get @s mbHzR',
        f'data modify storage rlk:mboss fg.rd merge value {{w:24,back:0,el:{EL},hold:3}}',
        f'execute rotated ~ 0 run {KFN}tele/line with storage rlk:mboss fg.rd'])
    redraw = redraw_fns(g, key, pid, [(Z, 'rd'), (Y, 'rd_line')])
    # the build-up without the tower (spec F2 section 4)
    tl.at(0, 'scoreboard players set #fq12SH mb 0', 'scoreboard players set #fq12P mb 0',
          'execute store result score #fq12S mb run random value 0..1',
          'execute if score #fq12S mb matches 0 run scoreboard players set #fq12S mb -1',
          f'kill @e[type=minecraft:marker,tag={W}]',
          at_core(g.fx('vent_flare'), RING_H + 0.7), g.snd('vent_flare'))
    tl.at(F2_FLAME, at_core(g.fx('flame_band'), RING_H - 0.6))
    tl.at(F2_FLAME + 2, g.snd('flame_charge'))
    tl.at(F2_FLAME + 8, at_core(g.fx('flame_band'), RING_H - 0.6))
    for t in range(F2_BURST + 4, F2_CRUMBLE, 4):
        tl.at(t, f'execute as @e[type=minecraft:item_display,tag={R}] at @s run '
                 + g.particle('falling_dust{block_state:"minecraft:tuff"}', '~ ~-0.3 ~', (0.5, 0.1, 0.5), 0, 1))
    tl.at(F2_CRUMBLE, f'function {NS}p/{key}/crumble')
    tl.at(F2_END, *rocks_cancel(pid), g.play('field_idle'), g.end())
    trail = ['scoreboard players operation #fgM mb = #fgPT mb', 'scoreboard players operation #fgM mb %= #fgK2 mb',
             f'execute if score #fgM mb matches 0 as @e[type=minecraft:item_display,tag={Fl}] at @s rotated as @s run '
             + g.fx('slab_trail')]
    tl.write([f'# F2 파쇄 (clip {F2_CLIP}; @s = body at the centre): bursts strike from {F2_BURST} every {F2_GAP} t (arc onto the',
              f'# player, 7-8 one group), throws from {F2_THROW} every {F2_TGAP} t (at most {F2_CAP} slab hits), crumble {F2_CRUMBLE}, end {F2_END}.'],
             ['# frock tick: track the player (3 deg/t), the decals again after a pause, the flying slabs\' trails.'],
             extra_tick=[TURN, redraw] + trail)
    g.pw(key, 'vis', ['# @s = a floor burst (#hzEv 1 = it strikes): the crystal-spike fan, its sound.',
                      'execute unless score #hzEv mb matches 1 run return 0',
                      g.fx('floor_burst'), g.snd('floor_burst')])
    g.pw(key, 'cancel', ['# Walker, slabs (hovering and flying), locks, the pattern\'s hazards.'] + rocks_cancel(pid)
         + [f'kill @e[type=minecraft:marker,tag={Z}]', f'kill @e[type=minecraft:marker,tag={Y}]',
            'scoreboard players set #fq12P mb 0'])


# ---------------------------------------------------------------------------------------------
def waves(g):
    """「인력 충격파」 x3 (service 21): per wave the charge sphere at the core (its tell: the clip's impact tick), a 1-tick
    beam, the flare dome, then an arena-wide ring front from r 2.5 at 0.55 b/t: framework hz/ring r0 0 r 2.5 made at the
    charge start (quiet, silent, active 36 t, height to 0.7 b: a jump clears it, #hzNoDodge 1: dash i-frames do NOT help,
    KB 3, Geo 1.2), grown every tick through hz/resize_s; paired with the kit's violet tele/wave (the charge disc, then
    the front ring and its inner edge in step with the hazard) and the 3-D fire band (p/wave_band, called 1 t before the
    strike), the fire on the front every 3 t and its rumble at the point nearest the player. The 3rd wave: the opening
    plays wave_long, the closing wave_drop (the drop, the landing, the lift-off) when the rig has them. Below 50 % HP
    (or test 42) two more fronts follow the 3rd, 6 t apart (tell 10 each)."""
    key, tl, pid = 'waves', TL(g, 'waves'), 21
    F = 'rlk_mb_fg_p21f'

    def front(tell):
        return [*g.hz_opts(act=W_ACT, y1=0.7, kb=KB['default'], nododge=1, sfx=0, quiet=1),
                g.hz_ring(0.0, W_BAND, tell, DMG['wave']), g.tag_last_hz(F),
                g.tele_wave(W_BAND, W_R1, W_BAND, tell, W_DUR, el=EL)]

    def band():
        return g.fx('wave_band', r0=int(W_BAND * 10), r1=int(round(W_R1 * 10)), w=int(W_BAND * 10), dur=W_DUR)

    for tell in sorted({W_IMP0} | {W3[v]['tell'] for v in (1, 2)}):
        g.pw(key, f'mk{tell}', [f'# @s = body at the centre: a front with a {tell} t charge (the hazard, the violet ring decal, the',
                                '# charge sphere at the core, the charge hiss).'] + front(tell)
             + [at_core(g.fx('wave_charge', t=tell)), g.snd('wave_charge')])
    g.pw(key, 'mkx', ['# @s = body: an extra front of the triple 3rd wave (tell 10): the hazard, a fresh ring decal, a charge pulse.']
         + front(10) + [at_core(g.fx('wave_pulse')), g.snd('wave_charge2')])
    g.pw(key, 'grow', [
        '# @s = a live front (from tick, before hz/all): radius 2.5 + 0.55 k b at its k-th active tick (this tick\'s hit',
        '# test), inner radius r - 2.5 (tenths: r = 25 + 11 k / 2).',
        'scoreboard players operation #hzSzR mb = @s mbHzT',
        'scoreboard players operation #hzSzR mb -= @s mbHzW',
        'scoreboard players add #hzSzR mb 1',
        'execute if score #hzSzR mb matches ..0 run return 0',
        f'execute if score #hzSzR mb matches {W_ACT + 1}.. run return 0',
        'scoreboard players operation #hzSzR mb *= #fgK11 mb',
        'scoreboard players operation #hzSzR mb /= #c2 mb',
        f'scoreboard players add #hzSzR mb {int(W_BAND * 10)}',
        'scoreboard players operation #hzSzR0 mb = #hzSzR mb',
        f'scoreboard players remove #hzSzR0 mb {int(W_BAND * 10)}',
        'scoreboard players set #hzSzW mb 0',
        'function rlk:mboss/hz/resize_s'])
    g.pw(key, 'rd', [
        '# @s = a live front after a pause: not struck yet -> the ring decal with the remaining charge; expanding -> the',
        '# fire band from its next radius (the band moves from the tick after the call, so it meets the hazard).',
        'scoreboard players operation #fgX mb = @s mbHzW',
        'scoreboard players operation #fgX mb -= @s mbHzT',
        'scoreboard players remove #fgX mb 1',
        f'execute if score #fgX mb matches 1.. run return run function {NS}p/{key}/rd_tell',
        'scoreboard players operation #fgX mb = @s mbHzT',
        'scoreboard players operation #fgX mb -= @s mbHzW',
        'scoreboard players add #fgX mb 2',
        f'execute if score #fgX mb matches {W_DUR}.. run return 0',
        f'scoreboard players set #fgM mb {W_DUR}',
        'scoreboard players operation #fgM mb -= #fgX mb',
        'execute store result storage rlk:mboss fg.rw.dur int 1 run scoreboard players get #fgM mb',
        'scoreboard players operation #fgX mb *= #fgK11 mb',
        'scoreboard players operation #fgX mb /= #c2 mb',
        f'scoreboard players add #fgX mb {int(W_BAND * 10)}',
        'execute store result storage rlk:mboss fg.rw.r0 int 1 run scoreboard players get #fgX mb',
        f'data modify storage rlk:mboss fg.rw merge value {{r1:{int(round(W_R1 * 10))},w:{int(W_BAND * 10)}}}',
        f'execute positioned ~ {CY} ~ run {KFN}p/wave_band with storage rlk:mboss fg.rw'])
    g.pw(key, 'rd_tell', [
        '# @s = a front still charging after a pause: its ring decal again (#fgX ticks to the strike).',
        'execute store result storage rlk:mboss fg.rw.tell int 1 run scoreboard players get #fgX mb',
        f'data modify storage rlk:mboss fg.rw merge value {{r0:{int(W_BAND * 10)},r1:{int(round(W_R1 * 10))},w:{int(W_BAND * 10)},'
        f'dur:{W_DUR},el:{EL},hold:2}}',
        f'execute positioned ~ {CY} ~ run {KFN}tele/wave with storage rlk:mboss fg.rw'])
    redraw = redraw_fns(g, key, pid, [(F, 'rd')])
    g.pw(key, 'tri', [
        '# The 3rd wave\'s charge start: 3 fronts below 50 % HP (or with test 42, #fgTri 1).',
        'scoreboard players set #fq21T mb 0',
        'scoreboard players operation #fgX mb = @s mhpC',
        'scoreboard players operation #fgX mb *= #c2 mb',
        'execute if score #fgX mb < @s mhpM run scoreboard players set #fq21T mb 1',
        'execute if score #fgTri mb matches 1 run scoreboard players set #fq21T mb 1'])
    g.pw(key, 'fin', ['# The last front has expired: the pattern ends.', f'kill @e[type=minecraft:marker,tag={F}]', g.end()])

    def strike_fx(S, h, guard=None, main=True):
        """The fx of one front's strike S (on the body = the floor centre); guard = an execute condition."""
        G = (lambda ln: ex(guard, ln)) if guard else (lambda ln: ln)                               # noqa: E731
        tl.at(S - 1, G(band()))
        tl.at(S, G(g.fx('wave_beam', h=float(h))), G(g.snd('wave_beam')))
        if not main:
            tl.at(S + 1, G(g.fx('wave_burst')))
            return
        tl.at(S - 10, G(g.snd('wave_charge2')))
        tl.at(S + 1, G(g.fx('wave_burst')), G(g.snd('wave_burst')))
        for k in range(12):
            r = W_BAND + W_SPEED * 3 * k
            tl.at(S + 3 * k, G(g.fx('wave_fire', r=round(r, 2))),
                  G(f'execute facing entity {PLAYER} feet rotated ~ 0 positioned ^ ^ ^{L.num(r, 2)} run {g.snd("wave_ring")}'))

    def pulses(t0, S, guard=None):
        for t in range(t0 + 8, S, 8):
            ln = at_core(g.fx('wave_pulse'))
            tl.at(t, ex(guard, ln) if guard else ln)

    # wave 1 (the core plays `wave` at 0) and wave 2
    tl.at(0, f'kill @e[type=minecraft:marker,tag={F}]', 'scoreboard players set #fq21T mb 0', 'scoreboard players set #fq21P mb 0',
          f'function {NS}p/{key}/mk{W_IMP0}')
    t2 = W_IMPACT[1] - W_IMP0
    tl.at(t2, g.play('wave'), f'function {NS}p/{key}/mk{W_IMP0}')
    for t0, S in ((0, W_IMPACT[0]), (t2, W_IMPACT[1])):
        pulses(t0, S)
        strike_fx(S, CORE_H)
    # wave 3, per variant (opening / closing)
    S3 = W_IMPACT[2]
    for v in ((1,) if W3_SAME else (1, 2)):
        vg = None if W3_SAME else VG[v]
        gx = (lambda ln: ln) if W3_SAME else (lambda ln, v=v: ex(VG[v], ln))                   # noqa: E731
        w = W3[v]
        e0, e1 = W_ENDS[(v, 0)], W_ENDS[(v, 1)]
        g.pw(key, f'w3_{v}', [
            f'# The 3rd wave ({"opening" if v == 1 else "closing"}): the triple check, the front ({w["tell"]} t charge), the real end '
            f'({e0}, triple {e1}).',
            f'function {NS}p/{key}/tri', f'function {NS}p/{key}/mk{w["tell"]}',
            g.set_len(e0), f'execute if score #fq21T mb matches 1 run {g.set_len(e1)}'])
        tl.at(w['clip_at'], gx(g.play(w['clip'])))
        tl.at(w['start'], gx(f'function {NS}p/{key}/w3_{v}'))
        pulses(w['start'], S3, vg)
        strike_fx(S3, w['core'], vg)
        for m in (1, 2):
            strike_fx(S3 + m * W_TRI_GAP, w['core'], 'if score #fq21T mb matches 1' + (f' {vg}' if vg else ''), main=False)
        for (vv, tri), e in W_ENDS.items():
            if vv == v:
                tl.at(e, gx(ex(f'{"if" if tri else "unless"} score #fq21T mb matches 1', f'function {NS}p/{key}/fin')))
    for m in (1, 2):
        tl.at(S3 + m * W_TRI_GAP - 10, f'execute if score #fq21T mb matches 1 run function {NS}p/{key}/mkx')
    # the closing wave_drop: the landing and the lift-off (the field's one lift-off flash, spec S2)
    if W3[2]['real']:
        c = W3[2]['clip']
        land = W3[2]['clip_at'] + ev_or(c, 'land', ev_or(c, 'impact', W3_FB_TELL))
        lift = W3[2]['clip_at'] + ev_or(c, 'lift', 60)
        tl.at(land, f'execute {VG[2]} run ' + g.sound('block.heavy_core.place', 0.8, 0.6),
              f'execute {VG[2]} run ' + g.sound('block.anvil.land', 0.5, 0.6),
              f'execute {VG[2]} positioned ~ {CY} ~ run ' + g.fx('dust_puff'))
        tl.at(lift, f'execute {VG[2]} positioned ~ {CY} ~ run ' + g.fx('lift_off'), f'execute {VG[2]} run ' + g.snd('lift_off'),
              f'execute {VG[2]} run ' + g.snd('rise_hum'))
    tl.write([f'# 「인력 충격파」 x3 (service 21, clip wave; @s = body at the centre): impacts {W_IMPACT} (charges '
              f'{W_IMP0} / {W_IMP0} / {W3[1]["tell"]} opening, {W3[2]["tell"]} closing),',
              f'# the 3rd wave x3 below 50 % HP ({W_TRI_GAP} t apart); ends {sorted(set(W_ENDS.values()))}.'],
             ['# waves tick: track the player (3 deg/t), the decals again after a pause, the fronts grow (before hz/all).'],
             extra_tick=[TURN, redraw, f'execute as @e[type=minecraft:marker,tag={F}] run function {NS}p/{key}/grow'])
    g.pw(key, 'cancel', ['# The fronts (framework hazards; lib_clear usually got them first).', f'kill @e[type=minecraft:marker,tag={F}]',
                         'scoreboard players set #fq21P mb 0'])
