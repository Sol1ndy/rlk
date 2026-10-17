"""P5 하늘을 심판하는 자 (fly-slam), P6 guard sweeps (gold / enchanted) and the chaos fail spears.

Sources: patterns.md §7, §8.1-8.8, §9.4-9.5, m1.md F (26.45-31.5 s), m2.md (clips A/B), m4.md, plan.md K4,
K6, K12, K16, K17, K26. Clips `flyslam` (91 t), `sweep` (39 t), `sweep_e` (45 t); the fail spears run on the
chaos fail clock (T0 = timer full) while the core plays chaos_fail / chaos_land / chaos_raise. Every hit lands
on a clip event (or the fail schedule) and is telegraphed >= 10 t. User tuning (plan.md): the clips play with
~25 % shorter wind-ups (guardian_clips.mjs RETIME; authored ticks of the fx go through api.rt / api.inv), the fail
schedule runs x0.75, and every hit area (with its decal and fx) is ~20 % larger. Played ticks below.

P5 하늘을 심판하는 자  (far)
  0-9    black-brown cubes climb the raised shaft; 5 glint on the spear head (star card, chime).
  9-12   gold spiral ribbons wind up around her, a glow at her feet, rising shimmer.
  12-14  a vertical gold beam (11 b, white core) erupts through her with crescent arcs; ascent whoosh.
  14     take-off to +8 b (rig) with a dark-cube trail, the attack line, no leash from here.
  15     the ring locks under the player (take-off + 1, K26), clamped into the safe disc and then to within
         21 - 5.5 b of the axis (the ring stays inside the walkable arena and still covers a player at the wall):
         28 gold rim bars grow r 1 -> 5.5 over 16-21 (m1 27.48-27.73 s), a translucent amber glow fill and a star.
  16     hazard: disc r 5.5, 180 %, strikes at 31 (15 t, the clip impact). She is untargetable 16-30.
  18-29  the body (hitbox) glides under the ring (she flies over it, trailing cubes); 20-28 gold 4-point
         sparkles and gold dust fall onto the centre; a progress circle reaches the rim at the strike;
         23 falling whistle.
  29-31  descent pillar from the sky onto the ring centre;  31 IMPACT: white flash of the rim, burst,
         shock ring, gold and rock debris, tumbling gold / dark cubes, boom + iron door crash.
  32-36  gold flame-like shards burst out;  37-41 the ground spike ring (gold crystal shards 0.6-1.5 b
         out to r 5.6, inner first) with crystal crackle;  spikes linger to ~67 with sparkles.
  63     the spear comes out of the floor (chain thud, stone);  70-82 twirl trail, whooshes;  91 idle.

P6 sweeps (service, started by the core from guard mode; the blade is synced to the rig clips)
  The hit is split into angle slices that strike on the tick the rig's blade sweeps over them (measured
  from the rig poses, p56_spear.json), so a player on her left is hit first and one on her right last;
  one hit per sweep across the slices (a hit or an i-frame dodge on one slice consumes the others).
  Gold (11, timeout): sweep clip; 200 deg front arc r 6 from her left to her right, slices at 15-19
  (front at 17, m2 hit at timeout+23 before the tuning), 165 %, knockback 3. Gold rim bars (flash white as the
  blade passes), a progress arc, 9 riptide swell, layered gold crescent ribbon (#CC9C3C / #E4B43C / #FCFC84 /
  white) + two crescent cards, a row of vertical gold crystal spikes along the arc edge, gold and rock
  chips, dark-red cubes; sweep whoosh 15, crunch 17 (dripstone, basalt, quiet explode).
  Enchanted (12, record complete R = clip 0): sweep_e clip; same arc in the recorded element: enchant line
  through her and along the spear + waist ring burst at 3-4 (beacon thump, short sonic charge), element
  glow on the wind-up, slices at 16-22 (front at 18), 250 % + the element, knockback 4; element crescent
  ribbon and strike fx inside the arc (electro forked bolts and violet shards, pyro flame bursts, hydro
  splashes, cryo ice shards), lingering ground fx to R+37; element sounds.

Fail spears (service, pattern 13; clock 0 = T0; spear j = 0, 1 for each surviving star, 23 t apart; the m4
schedule x0.75)
  17+23j  the target locks on the player (pulled to within 21 - 3.4 b of the axis, so the disc stays inside the
          walkable arena and still covers the player); a gold cube column forms above it, fed by a gold chain
          from her chest; forming roar (respawn anchor, beacon, amethyst, sonic charge).
  19+23j  the giant red copy of her spear grows out of the column point-down (tip 3.8 b above the
          target); the red concave 4-point star decal (crimson fill, black rim, pink streaks) centred on
          the target, one arm toward the arena centre, side arms opening +-3.2 -> +-11.4 b in 6 t;
          hazard: disc r 3.4 (K12 cylinder x1.2), 220 %, the star's element, strikes at 37+23j (18 t).
          Spear 1 says the attack line.
  27-30   hang drone; 28 (+2 for blue) the spear turns from red to the star colour (gold; blue via
          violet; element colours), chime;  33 pre-drop whistle.
  37+23j  drop in 1 t + IMPACT: flash column, starburst rays; 38 dome of light (r 1.75); 39 the X of
          crossed light beams, spike field (gold +-8 b) / ice-water splash (+-4.8 b) / flames / sparks,
          rock debris and cubes, per-kind blast sounds; residue (crimson floor + gold or blue cracks)
          to ~+33; the spear stays planted 20 t, then dissolves upward (57) and is gone at 67+23j.

Owner of this file: the P5/P6 pattern author. Writes only F:mboss/guardian/p/{flyslam,sweep_g,sweep_e,
fail}/** through gen.pw. Entities carry rlk_room, rlk_mb_aux and rlk_mb_gd_p5 / p11 / p12 / p13 (cancel
kills by that tag; the hazards these patterns create are tagged too); fake players are #gp5* / #gp11* /
#gp12* / #gp13*. Helpers: p56_fx.py; spear points: p56_spear.json (p56_measure.py).
"""
import json
import math
import random
from pathlib import Path

from .api import (Pattern, ev, clip_len, rt, inv, DMG, KB, CY, NS, GOLD, GOLD_PALE, GOLD_DEEP, RED_EDGE, CRIMSON,
                  CRIMSON_DARK, STAR_HZCOL)
from . import p56_fx as X
from .p56_fx import n3, loc, polar, lerp, add, sub, mul, tf, tags, qaxis, qrot

SPEAR = json.loads((Path(__file__).resolve().parent / 'p56_spear.json').read_text(encoding='utf-8'))

# fail spear schedule (m4 §4, K12: column 23, decal + lock 25, impact 49, 31 t apart), x0.75 (user tuning: wind-ups
# ~25 % shorter): column 17, decal + lock 19, impact 37 (tell 18), 23 t apart
FAIL_COL, FAIL_DECAL, FAIL_GAP, FAIL_TELL = 17, 19, 23, 18
FAIL_HIT = FAIL_DECAL + FAIL_TELL
FAIL_REL = 10                     # she departs (p/release) this long after the last impact (m4: +90)
FAIL_R = 3.4                      # K12 r 2.5-3 (was 2.8), x1.2
WALK_R = 21                       # the walkable arena: a fail disc / the P5 ring never crosses it
AREA = 1.2                        # linear scale of the hit areas and their fx (user tuning)


def fail_t(t):
    """Fail clock tick of spear 1 for an m4 tick between the decal (25) and the impact (49) of the source schedule."""
    return FAIL_DECAL + int(math.floor((t - 25) * FAIL_TELL / 24 + 0.5))


def clamp_in(sel, r):
    """As the marker sel (on the floor): pulled radially toward the arena axis until it is within r of it (an area
    of radius WALK_R - r centred there stays inside the walkable arena and still covers a player at the wall)."""
    return (f'execute as {sel} at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{r:g}] '
            f'at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^{r:g} run tp @s ~ {CY} ~')

PATTERNS = [
    Pattern(5, 'flyslam', '하늘을 심판하는 자', bands=('far',), weight={'far': 3}, recover=22, max_len=clip_len('flyslam') + 4),
    Pattern(11, 'sweep_g', '파수 모드 – 휘두르기', kind='service', recover=20, max_len=clip_len('sweep') + 4),
    Pattern(12, 'sweep_e', '파수 모드 – 원소 휘두르기', kind='service', recover=20, max_len=clip_len('sweep_e') + 4),
    Pattern(13, 'fail', '파괴 실패 – 거대한 창', kind='service', recover=20,
            max_len=FAIL_DECAL + FAIL_GAP + FAIL_TELL + 40, length=FAIL_HIT + FAIL_GAP + 31),
]

BODY = 'at @s rotated as @s rotated ~ 0'
FACE = 'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'
WHITE = (1.0, 1.0, 0.99)
DARK = (0.23, 0.15, 0.13)
BROWN_BLK = 'block{block_state:"minecraft:brown_terracotta"}'
GOLD_BLK = 'block{block_state:"minecraft:gold_block"}'
RED_BLK = 'block{block_state:"minecraft:red_concrete"}'
BLACK_BLK = 'block{block_state:"minecraft:black_concrete"}'


def sp(clip, t, part='tip'):
    row = SPEAR[clip][t]
    return tuple(row[part]) if row and part in row else None


def hz_tag(pid, extra=None):
    """Tag the hazard just created (#hzLast) so the pattern's cancel removes it too."""
    sel = 'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add '
    out = [sel + f'rlk_mb_gd_p{pid}']
    if extra:
        out.append(sel + extra)
    return out


def emit(g):
    flyslam(g)
    sweep(g, gold=True)
    sweep(g, gold=False)
    fail(g)


# =============================================================================================
# P5 하늘을 심판하는 자
def flyslam(g):
    k, pid = 'flyslam', 5
    tl = X.TL(g, k)
    E = lambda n: ev(k, n)
    glint, beam, take, ring, gone, dive, imp = E('glint'), E('beam'), E('takeoff'), E('ring'), E('gone'), E('dive'), E('impact')
    spikes, pull, twirl, end = E('spikes'), E('pull'), E('twirl'), clip_len(k)
    lock = take + 1                                  # K26: the ring locks at take-off + 1 t
    R, NB = 5.5, 28                                  # K26 r 4.5, x1.22 (user tuning)
    K5 = R / 4.5                                     # scale of the fx authored for r 4.5
    W = lambda t: rt(k, t)                           # authored (source) tick -> played tick
    M = '@e[type=minecraft:marker,tag=rlk_mb_gd_p5t,limit=1]'
    ATM = f'at {M}'
    rnd = random.Random(55)

    # -- 0-12: black-brown cubes climb the raised shaft; dark dust along it
    for ta in range(2, 13, 2):
        t = W(ta)
        gp, tip = sp(k, t, 'grip'), sp(k, min(W(ta + 5), beam))
        dy = tip[1] - gp[1]
        specs = X.cube_set(500 + ta, 2, ['dark', 'brown', 'dark', 'crimson', 'rock', 'dark'], (0.06, 0.3, 0.06),
                           (0.09, 0.2), (dy * 0.7, dy * 0.95), up=5.0, dirv=(0, 1, 0), delay=1)
        X.cubes(tl, pid, f'5c{ta}', t, specs, f'{BODY} positioned {loc(gp)}', 6)
        for s in (0.25, 0.55, 0.85):
            tl.at(t, f'execute {BODY} positioned {loc(lerp(gp, sp(k, t), s))} run '
                  + g.dust_fade((0.36, 0.22, 0.16), DARK, 0.8, '~ ~ ~', (0.05, 0.12, 0.05), 1))
    tl.at(1, g.sound('block.amethyst_block.resonate', 0.35, 1.6), g.sound('item.trident.riptide_1', 0.25, 1.5))

    # -- 6: glint on the spear head (white-gold 4-point flare)
    gl = lerp(sp(k, glint, 'head'), sp(k, glint, 'tip'), 0.45)
    tl.at(glint,
          f'execute {BODY} run ' + g.card('star', loc(gl), bb='center', spin=45, s0=0.2, s1=1.7, life=6, fade=3),
          f'execute {BODY} run ' + g.card('glow', loc(gl), bb='center', s0=0.4, s1=1.2, life=5, fade=3),
          f'execute {BODY} positioned {loc(gl)} run ' + g.particle('end_rod', '~ ~ ~', (0.08, 0.08, 0.08), 0.05, 6),
          g.sound('block.amethyst_block.chime', 0.9, 2.0), g.sound('block.beacon.power_select', 0.3, 1.9))
    for t in range(glint + 1, W(12), 2):
        tl.at(t, f'execute {BODY} positioned {loc(sp(k, t))} run ' + g.dust(GOLD_PALE, 0.6, '~ ~ ~', (0.1, 0.1, 0.1), 2))

    # -- authored 12-16: gold spiral ribbons around her, glow at her feet
    for t in range(W(12), beam + 1):
        for hx in range(2):
            for j in range(8):
                h = 0.25 + 3.3 * j / 7
                a = (inv(k, t) - 12) * 70 + j * 46 + hx * 180
                r = 1.05 - 0.25 * j / 7
                col = (0.976, 0.910, 0.647) if (j + hx) % 2 else (0.796, 0.647, 0.510)
                tl.at(t, f'execute {BODY} positioned {loc(polar(a, r, h))} run ' + g.dust(col, 0.9, '~ ~ ~', (0.02, 0.02, 0.02), 1))
    tl.at(W(12), f'execute {BODY} run ' + g.card('glow', '^ ^0.06 ^', rot='~ 90', s0=0.6, s1=2.8, life=9, fade=3),
          g.sound('block.beacon.power_select', 0.5, 1.5), g.sound('block.amethyst_block.resonate', 0.6, 1.4))

    # -- 16-19: the vertical beam (11 b, white core) through her, crescent arcs; 19 it shoots up
    btag = ('rlk_mb_gd_p5b',)
    for blk, w in (('minecraft:yellow_stained_glass', 0.62), ('minecraft:white_concrete', 0.16)):
        tl.at(beam, f'execute at @s run ' + X.bd(blk, (-w / 2, 0, -w / 2), X.QI, (w, 0.2, w), X.base_tags(pid, *btag, f'rlk_mb_gd_p5b{int(w * 100)}')))
        tl.at(beam + 1, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b{int(w * 100)},limit=1] run data merge entity @s '
                        f'{{start_interpolation:0,interpolation_duration:2,transformation:{tf((-w / 2, 0, -w / 2), X.QI, (w, 11.0, w))}}}')
        tl.at(take, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b{int(w * 100)},limit=1] run data merge entity @s '
                    f'{{start_interpolation:0,interpolation_duration:4,transformation:{tf((-w / 8, 9.0, -w / 8), X.QI, (w / 4, 6.0, w / 4))}}}')
    tl.at(take + 4, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p5b]')
    tl.at(beam, f'execute {BODY} run ' + g.card('crescent', '^ ^1.5 ^', spin=160, s0=2.4, s1=3.2, life=5, fade=2),
          f'execute {BODY} run ' + g.card('crescent', '^ ^2.7 ^', roll=180, spin=150, s0=2.0, s1=2.9, life=5, fade=2),
          g.dust(GOLD_PALE, 1.6, '~ ~3 ~', (0.15, 3.0, 0.15), 30),
          g.sound('block.beacon.activate', 0.7, 1.6))
    tl.at(beam + 1, f'execute {BODY} run ' + g.card('crescent', '^ ^2.1 ^', roll=180, spin=-160, s0=2.6, s1=3.4, life=5, fade=2),
          g.particle('end_rod', '~ ~4 ~', (0.15, 2.5, 0.15), 0.05, 14),
          g.sound('entity.ender_dragon.flap', 0.9, 1.3), g.sound('item.trident.riptide_3', 0.8, 1.0))
    tl.at(beam + 2, g.dust((0.796, 0.647, 0.510), 1.4, '~ ~5 ~', (0.2, 3.5, 0.2), 20))

    # -- 19-23: take-off with a dark-cube trail; the attack line; no leash during the flight
    tl.at(take, g.voice_attack(), 'scoreboard players set #mbNoLeash mb 1',
          g.particle(RED_BLK, '~ ~1.2 ~', (0.5, 0.4, 0.5), 0, 12))
    for t in range(take, gone + 2):
        py = SPEAR[k][t]['pelvis'][1]
        tl.at(t, g.dust_fade(RED_EDGE, CRIMSON_DARK, 1.5, f'~ ~{n3(py - 0.4)} ~', (0.3, 0.6, 0.3), 5),
              g.particle(BLACK_BLK, f'~ ~{n3(py - 0.6)} ~', (0.25, 0.4, 0.25), 0, 3))
    specs = X.cube_set(519, 9, ['dark', 'crimson', 'dark', 'red', 'brown', 'dark', 'red'], (0.35, 1.6, 0.35),
                       (0.14, 0.34), (0.4, 1.3), up=-0.6, delay=3)
    X.cubes(tl, pid, '5t', take + 1, specs, 'at @s positioned ~ ~3.4 ~', 12)

    # -- 20: lock under the player (clamped into the safe disc); ring rim bars at r 1, fill, emblem
    lk = [f'# @s = body (clip tick {lock} = take-off + 1, K26): the landing point locks under the player.',
          'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p5t]',
          f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {{Tags:{tags(*X.base_tags(pid, "rlk_mb_gd_p5t"))}}}',
          f'execute as {M} run function rlk:mboss/mv/clamp',
          '# the ring stays inside the walkable arena (it still covers a player standing at the wall)',
          clamp_in(M, WALK_R - R)]

    def ring_bar(kk, r):
        th = kk * 360 / NB
        ln = 2 * r * math.sin(math.radians(180 / NB)) * 1.1
        return X.bar_tf(th, r, ln, 0.12 + 0.012 * r, 0.045, 0.02)

    for kk in range(NB):
        tr, q, sc = ring_bar(kk, 1.0)
        lk.append(f'execute {ATM} run ' + X.bd('minecraft:gold_block', tr, q, sc,
                                                X.base_tags(pid, 'rlk_mb_gd_p5r', f'rlk_mb_gd_p5r{kk}')))
    lk += [f'execute {ATM} run ' + g.card('glow', '~ ~0.04 ~', rot='0 90', s0=2.0, s1=2 * R, life=ring + 5 - lock + 1),
           f'execute {ATM} run ' + g.card('star', '~ ~0.05 ~', rot='0 90', spin=45, s0=0.6, s1=2.6 * K5, life=imp - lock),
           f'execute {ATM} run ' + g.sound('block.amethyst_block.resonate', 0.6, 1.2),
           f'execute {ATM} run ' + g.dust(GOLD, 1.2, '~ ~0.1 ~', (0.5, 0.02, 0.5), 10)]
    g.pw(k, 'lock', lk)
    tl.at(lock, g.fn('p/flyslam/lock'))

    # -- ring: the hazard (disc r R, strikes at the clip impact) and the rim growth; untargetable
    grow = [f'# @s = body (clip tick {ring}): hazard + ring growth r 1 -> {R} over 5 t (m1 27.48-27.73 s).',
            *g.hz_opts(sfx=0, quiet=1, kb=KB['default'], linger=2),
            f'execute {ATM} run {g.hz_disc(R, imp - ring, DMG["p5"])}',
            *hz_tag(pid, 'rlk_mb_gd_p5h'),
            'tag @s add rlk_mb_inv']
    for kk in range(NB):
        tr, q, sc = ring_bar(kk, R)
        grow.append(f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5r{kk},limit=1] run data merge entity @s '
                    f'{{start_interpolation:0,interpolation_duration:5,transformation:{tf(tr, q, sc)}}}')
    g.pw(k, 'ring', grow)
    tl.at(ring, g.fn('p/flyslam/ring'))
    tl.at(ring + 5, f'execute {ATM} run ' + g.card('glow', '~ ~0.04 ~', rot='0 90', s0=2 * R, s1=2 * R, life=imp - ring - 5))

    # -- 23-39: the body glides under the ring (she flies over it); sky trail
    tl.at(gone, f'execute at @s facing entity {M} feet run tp @s ~ ~ ~ ~ 0',
          f'execute positioned as {M} run function rlk:mboss/mv/glide {{t:{dive - gone}}}')
    for t in range(gone + 1, dive):
        py = SPEAR[k][t]['pelvis'][1]
        tl.at(t, g.dust_fade(RED_EDGE, CRIMSON_DARK, 1.3, f'~ ~{n3(py)} ~', (0.25, 0.35, 0.25), 3))
        if t % 3 == 0:
            tl.at(t, g.particle(BLACK_BLK, f'~ ~{n3(py - 0.4)} ~', (0.2, 0.3, 0.2), 0, 2),
                  g.dust(GOLD, 1.0, f'~ ~{n3(py + 0.8)} ~', (0.3, 0.3, 0.3), 2))

    # -- 22-40: progress circle reaching the rim at the strike; 26-38 falling sparkles; 31 whistle
    for t in range(ring + 1, imp, 3):
        r = R * (t - ring) / (imp - ring)
        n = max(8, int(2 * math.pi * r / 0.7))
        tl.at(t, *[f'execute {ATM} positioned {loc(polar(360 * j / n, r, 0.12))} run ' + g.dust(GOLD_PALE, 0.8, '~ ~ ~', (0, 0, 0), 1)
                   for j in range(n)])
    for t in range(W(26), W(39), 2):
        a, rr, h = rnd.uniform(0, 360), rnd.uniform(0.2, 1.8) * K5, rnd.uniform(6.5, 8.5)
        p = polar(a, rr, h)
        tl.at(t, f'execute {ATM} run ' + g.card('star', f'~{n3(p[0])} ~{n3(h)} ~{n3(p[2])}', bb='center', spin=90,
                                                s0=0.32, s1=0.55, move=(0, -(h - 0.4), 0), life=9, fade=2),
              f'execute {ATM} run ' + g.particle('falling_dust{block_state:"minecraft:gold_block"}', '~ ~7 ~', (1.6, 0.8, 1.6), 0, 4),
              f'execute {ATM} run ' + g.particle('end_rod', '~ ~5 ~', (0.8, 1.5, 0.8), 0, 1))
    tl.at(W(31), f'execute {ATM} run ' + g.sound('block.beacon.deactivate', 0.8, 1.8))

    # -- 39-41: descent pillar onto the ring centre
    for blk, w, nm in (('minecraft:yellow_stained_glass', 0.8, 'po'), ('minecraft:white_concrete', 0.22, 'pi')):
        tl.at(dive, f'execute {ATM} run ' + X.bd(blk, (-w / 2, 13.0, -w / 2), X.QI, (w, 1.0, w), X.base_tags(pid, 'rlk_mb_gd_p5p', f'rlk_mb_gd_p5{nm}')))
        tl.at(dive + 1, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5{nm},limit=1] run data merge entity @s '
                        f'{{start_interpolation:0,interpolation_duration:1,transformation:{tf((-w / 2, 0.0, -w / 2), X.QI, (w, 14.0, w))}}}')
        tl.at(imp + 1, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5{nm},limit=1] run data merge entity @s '
                       f'{{start_interpolation:0,interpolation_duration:3,transformation:{tf((0, 0.0, 0), X.QI, (0.0, 16.0, 0.0))}}}')
    tl.at(imp + 4, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p5p]')
    tl.at(dive, f'execute {ATM} run ' + g.sound('entity.phantom.swoop', 0.6, 1.4),
          f'execute {ATM} run ' + g.dust((0.992, 0.961, 0.706), 1.8, '~ ~6 ~', (0.15, 5.0, 0.15), 30))

    # -- 41: IMPACT
    hit = [f'# @s = body on the ring centre (clip tick {imp}): the hazard strikes this tick (framework).',
           'tag @s remove rlk_mb_inv',
           'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5r] run data merge entity @s {block_state:{id:"minecraft:white_stained_glass"}}',
           g.card('burst', '~ ~1.3 ~', bb='center', spin=20, s0=0.8, s1=4.6 * K5, life=6, fade=3),
           g.card('glow', '~ ~1.6 ~', bb='center', s0=2.0, s1=7.0 * K5, life=5, fade=2),
           g.card('ring', '~ ~0.12 ~', rot='~ 90', s0=1.0, s1=10.5 * K5, life=8, fade=3),
           g.dust(WHITE, 2.4, '~ ~1 ~', (0.8, 0.8, 0.8), 30),
           g.dust((0.992, 0.961, 0.706), 1.8, '~ ~0.4 ~', (2.0 * K5, 0.2, 2.0 * K5), 40),
           g.particle('explosion', '~ ~0.6 ~', (1.2 * K5, 0.2, 1.2 * K5), 0, 3),
           g.particle(GOLD_BLK, '~ ~0.4 ~', (2.2 * K5, 0.3, 2.2 * K5), 0.2, 40),
           g.particle(BROWN_BLK, '~ ~0.4 ~', (1.6 * K5, 0.3, 1.6 * K5), 0.25, 24),
           g.sound('entity.generic.explode', 1.0, 0.9), g.sound('entity.zombie.attack_iron_door', 0.7, 0.6)]
    g.pw(k, 'impact', hit)
    tl.at(imp, g.fn('p/flyslam/impact'))
    tl.at(imp + 1, g.sound('block.amethyst_cluster.break', 0.9, 0.8), 'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p5t]')
    tl.at(imp + 2, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p5r]')
    specs = X.cube_set(541, 12, ['gold', 'goldb', 'rock', 'dark', 'amber', 'gold', 'rock', 'crimson'], (1.0 * K5, 0.3, 1.0 * K5),
                       (0.22, 0.5), (1.6 * K5, 3.6 * K5), up=0.5, delay=2)
    X.cubes(tl, pid, '5i', imp, specs, 'at @s positioned ~ ~0.5 ~', 14)

    # -- 42-46: gold flame-like shards burst outward; 47-51 the ground spike ring
    for j, a in enumerate(range(0, 360, 45)):
        a2 = a + rnd.uniform(-15, 15)
        tl.at(imp + 1 + j % 2, f'execute {BODY} rotated ~{n3(a2)} 0 run '
              + g.card('shard', f'^ ^0.05 ^{n3(rnd.uniform(0.5, 0.9))}', rot=f'~ {int(rnd.uniform(25, 45))}',
                       s0=0.3, s1=rnd.uniform(1.4, 2.1), life=7, fade=3))
    for t in (imp + 1, imp + 3, imp + 5):
        tl.at(t, g.dust_fade((1.0, 0.92, 0.55), (0.95, 0.55, 0.15), 1.6, '~ ~0.8 ~', (1.0 * K5, 0.6, 1.0 * K5), 14))
    pts = sorted(((rnd.uniform(1.6, 4.6) * K5, rnd.uniform(0, 360), rnd.uniform(0.6, 1.5)) for _ in range(16)))
    for r, a, size in pts:
        t = spikes + int((r / K5 - 1.6) / 3.0 * 4)
        tl.at(t, f'execute {BODY} rotated ~{n3(a)} 0 run ' + g.card('shard', f'^ ^0.02 ^{n3(r)}', bb='vertical',
                                                                    s0=size * 0.7, s1=size, life=W(77) - t, fade=6),
              f'execute {BODY} rotated ~{n3(a)} 0 positioned ^ ^0.2 ^{n3(r)} run ' + g.particle(GOLD_BLK, '~ ~ ~', (0.2, 0.1, 0.2), 0.1, 4))
    tl.at(spikes, g.sound('block.pointed_dripstone.land', 1.0, 1.0), g.sound('block.amethyst_cluster.place', 1.0, 1.0))
    tl.at(spikes + 2, g.sound('block.pointed_dripstone.land', 0.8, 1.2))
    tl.at(spikes + 4, g.sound('block.pointed_dripstone.land', 0.7, 0.9), g.sound('block.amethyst_cluster.place', 0.6, 1.3))
    for t in range(spikes + 4, pull + 1, 4):
        tl.at(t, g.particle('wax_on', '~ ~0.8 ~', (3.0 * K5, 0.5, 3.0 * K5), 0, 3), g.dust(GOLD, 0.9, '~ ~0.5 ~', (3.0 * K5, 0.4, 3.0 * K5), 4))

    # -- 73: the spear comes out of the floor; 80-92 twirl trail
    po = pull + 2
    tl.at(po, g.sound('block.chain.break', 0.8, 0.6), g.sound('block.stone.break', 0.9, 0.8),
          g.particle(GOLD_BLK, '~ ~0.2 ~', (0.3, 0.1, 0.3), 0.15, 12), g.particle(BROWN_BLK, '~ ~0.2 ~', (0.3, 0.1, 0.3), 0.15, 8))
    for t in range(twirl + 1, twirl + 14):
        a, b = sp(k, t - 1), sp(k, t)
        for s in (0.5, 1.0):
            tl.at(t, f'execute {BODY} positioned {loc(lerp(a, b, s))} run ' + g.dust((0.992, 0.957, 0.584), 0.8, '~ ~ ~', (0.03, 0.03, 0.03), 1))
    tl.at(twirl + 4, g.sound('item.trident.riptide_1', 0.45, 1.4), g.sound('entity.player.attack.sweep', 0.35, 0.8))
    tl.at(twirl + 10, g.sound('item.trident.riptide_1', 0.35, 1.5))
    tl.at(end, g.end())

    tl.write([f'# P5 하늘을 심판하는 자 start (@s = body, player far): flyslam clip ({end} t). See p56.py for the timeline.',
              'kill @e[tag=rlk_mb_gd_p5]',
              FACE,
              g.play(k)],
             ['# P5 tick (@s = body, #gdPT = clip tick).'])
    g.pw(k, 'cancel', ['# P5 cancel (any executor): ring, pillar, beam, cubes, markers and its hazard; the core resets',
                       '# rlk_mb_inv and the leash.',
                       'kill @e[tag=rlk_mb_gd_p5]'])


# =============================================================================================
# P6 sweeps
# blade slices (strike tick, from deg, to deg; + = her left), measured on the rig blade (p56_spear.json) on the
# authored clip ticks and mapped to the played ones (the blade sits on a 1:1 segment of the retiming)
SLICES = {clip: [(rt(clip, t), a0, a1) for t, a0, a1 in sl] for clip, sl in {
    'sweep': [(20, 100, 55), (21, 55, 30), (22, 30, -5), (23, -5, -39), (24, -39, -100)],
    'sweep_e': [(21, 100, 75), (22, 75, 25), (23, 25, 3), (24, 3, -18), (25, -18, -39), (26, -39, -81), (27, -81, -100)],
}.items()}
SW_R, SW_PAD = 6.0, 5          # r (K6 4.5-5, was 5; x1.2); pad ~ the 0.3 b body half-width at r 3
SW_K = SW_R / 5.0              # scale of the sweep fx authored for r 5
# ribbon palettes: deep, mid, core (white-hot), light
PAL_SW = {0: ((0.80, 0.61, 0.24), (0.89, 0.71, 0.24), (0.99, 0.99, 0.95), (0.99, 0.99, 0.52)),
          1: ((0.78, 0.25, 0.10), (1.0, 0.54, 0.30), (1.0, 0.95, 0.85), (1.0, 0.80, 0.50)),
          2: ((0.16, 0.47, 0.78), (0.36, 0.78, 1.0), (0.93, 0.99, 1.0), (0.70, 0.92, 1.0)),
          3: ((0.42, 0.33, 0.80), (0.71, 0.33, 0.99), (0.99, 0.89, 0.99), (0.89, 0.52, 0.99)),
          4: ((0.30, 0.62, 0.76), (0.55, 0.90, 0.95), (0.96, 1.0, 1.0), (0.64, 1.0, 0.99))}
# translucent crescent slabs left behind by the blade (main body, white-hot outer edge)
SLAB_BLK = {0: ('minecraft:yellow_stained_glass', 'minecraft:white_stained_glass'),
            1: ('minecraft:orange_stained_glass', 'minecraft:yellow_stained_glass'),
            2: ('minecraft:light_blue_stained_glass', 'minecraft:white_stained_glass'),
            3: ('minecraft:magenta_stained_glass', 'minecraft:white_stained_glass'),
            4: ('minecraft:white_stained_glass', 'minecraft:light_blue_stained_glass')}
# Rim of the sweep: opaque saturated bars on a black under-bar (a dark outline 0.06 b wide), so the full extent
# reads from the first tick on the white marble and on the pink centre star alike (glass rims vanished there).
RIM_BLK = {0: 'minecraft:gold_block', 1: 'minecraft:orange_concrete', 2: 'minecraft:blue_concrete',
           3: 'minecraft:purple_concrete', 4: 'minecraft:light_blue_concrete'}
RIM_OUT = 'minecraft:black_concrete'
# progress arc: saturated, darker than the element palette (pale cyan / pale gold vanish on marble), with a dark
# companion row just outside it
ARC_COL = {0: (0.90, 0.52, 0.06), 1: (1.0, 0.38, 0.10), 2: (0.10, 0.36, 0.95), 3: (0.62, 0.22, 0.95), 4: (0.05, 0.62, 0.82)}
ARC_DARK = (0.10, 0.06, 0.08)
EL_SHARD = {1: 'minecraft:orange_stained_glass', 2: 'minecraft:light_blue_stained_glass',
            3: 'minecraft:purple_stained_glass', 4: 'minecraft:packed_ice'}


def bolt_points(rnd, top, segs=5, jit=0.35, n=3):
    """A forked zigzag from (x, top, z) local to the ground: list of (x, y, z) offsets."""
    pts, x, z = [], 0.0, 0.0
    prev = (0.0, top, 0.0)
    for s in range(1, segs + 1):
        y = top * (1 - s / segs)
        nx, nz = (x + rnd.uniform(-jit, jit), z + rnd.uniform(-jit, jit)) if s < segs else (x * 0.3, z * 0.3)
        cur = (nx, y, nz)
        for i in range(n):
            pts.append(lerp(prev, cur, (i + 1) / n))
        prev, x, z = cur, nx, nz
    return pts


def sweep(g, gold):
    key = 'sweep_g' if gold else 'sweep_e'
    clip = 'sweep' if gold else 'sweep_e'
    pid = 11 if gold else 12
    tl = X.TL(g, key)
    slices = SLICES[clip]
    first, last = slices[0][0], slices[-1][0]
    end = clip_len(clip)
    rnd = random.Random(pid * 7)
    W = lambda t: rt(clip, t)          # authored (source) tick -> played tick
    els = (0,) if gold else (1, 2, 3, 4)
    SL = f'@e[type=minecraft:marker,tag=rlk_mb_gd_p{pid}h]'
    etl = {e: {} for e in els}

    def eat(t, e, *lines):
        """Element-specific timeline lines: straight into the timeline for the gold sweep; grouped into
        p/sweep_e/e<e>/<t> behind one element test per tick for the enchanted sweep."""
        if gold:
            tl.at(t, *lines)
        else:
            etl[e].setdefault(t, []).extend(lines)

    # -- rim decal (per element): 20 arc bars at r 5 from +100 to -100 deg + the two edge spokes; each
    #    arc bar carries the tag of the slice whose blade passes over it (it flashes white then)
    def slice_of(th):
        for i, (t, a0, a1) in enumerate(slices):
            if a0 >= th >= a1:
                return i
        return len(slices) - 1

    for e in els:
        rim = [f'# Rim decal of the sweep (@s = body, at it, rotated as it): {RIM_BLK[e]} on a black outline.']
        for i in range(20):
            th = 95 - 10 * i
            tr, q, sc = X.bar_tf(th, SW_R + 0.01, 1.0 * SW_K, 0.27, 0.03, 0.008)
            rim.append(X.bd(RIM_OUT, tr, q, sc, X.base_tags(pid, f'rlk_mb_gd_p{pid}b', f'rlk_mb_gd_p{pid}o', 'rlk_mb_gd_bnew')))
            tr, q, sc = X.bar_tf(th, SW_R - 0.05, 0.95 * SW_K, 0.15, 0.045, 0.02)
            rim.append(X.bd(RIM_BLK[e], tr, q, sc, X.base_tags(pid, f'rlk_mb_gd_p{pid}b', f'rlk_mb_gd_p{pid}b{slice_of(th)}', 'rlk_mb_gd_bnew')))
        for th in (100, -100):
            tr, q, sc = X.spoke_tf(th, 0.75, SW_R + 0.05, 0.26, 0.03, 0.008)
            rim.append(X.bd(RIM_OUT, tr, q, sc, X.base_tags(pid, f'rlk_mb_gd_p{pid}b', f'rlk_mb_gd_p{pid}o', 'rlk_mb_gd_bnew')))
            tr, q, sc = X.spoke_tf(th, 0.8, SW_R, 0.14, 0.045, 0.02)
            rim.append(X.bd(RIM_BLK[e], tr, q, sc, X.base_tags(pid, f'rlk_mb_gd_p{pid}b', f'rlk_mb_gd_p{pid}e', 'rlk_mb_gd_bnew')))
        rim += ['tp @e[type=minecraft:block_display,tag=rlk_mb_gd_bnew] ~ ~ ~ ~ 0',
                'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_bnew] remove rlk_mb_gd_bnew']
        g.pw(key, f'rim{e}', rim)

    # -- slices: one sector hazard per blade slice, struck on the tick the blade passes
    st = [f'# @s = body: {len(slices)} blade slices of the 200 deg arc r {SW_R} (strike ticks {first}-{last}).']
    for (t, a0, a1) in slices:
        c, half = (a0 + a1) / 2, int(round((a0 - a1) / 2 + SW_PAD))
        st += g.hz_opts(sfx=0, quiet=1, kb=KB['default'] if gold else KB['ench'], linger=2)
        if not gold:
            st += ['scoreboard players operation #hzEl mb = #gdSwEl mb', 'scoreboard players operation #hzCol mb = #gdSwEl mb']
        st.append(f'execute at @s rotated as @s rotated ~{n3(-c)} 0 positioned ~ {CY} ~ run '
                  + g.hz_sector(SW_R, half, t, DMG['gold'] if gold else DMG['ench']))
        st += hz_tag(pid, f'rlk_mb_gd_p{pid}h')
    g.pw(key, 'slices', st)

    # -- one hit per sweep: a hit (or a dodge) on any slice consumes the rest (body tick runs before hz/all)
    tl.span(first + 1, last + 1, f'execute if entity {SL.replace("]", ",scores={mbHzHit=1..}]")} run scoreboard players set {SL.replace(",limit=1", "")} mbHzHit 1')

    # -- progress arc (telegraph timing): a saturated arc with a dark row just outside it, growing from her to
    #    the rim; it reaches the rim at the end of the tell (the tick before the first slice strikes)
    tell_end = first - 1
    for t in sorted(set(range(2, tell_end, 2)) | {tell_end}):
        r = SW_R * t / tell_end
        n = max(6, int(math.radians(200) * r / 0.55))
        for e in els:
            eat(t, e, *[f'execute {BODY} positioned {loc(polar(100 - 200 * j / (n - 1), r, 0.1))} run '
                       + g.dust(ARC_COL[e], 0.95, '~ ~ ~', (0, 0, 0), 1) for j in range(n)],
                *[f'execute {BODY} positioned {loc(polar(100 - 200 * (j + 0.5) / (n - 1), r + 0.16, 0.08))} run '
                  + g.dust(ARC_DARK, 0.7, '~ ~ ~', (0, 0, 0), 1) for j in range(0, n - 1, 2)])

    # -- wind-up: glow on the spear head
    for t in range(1 if gold else ev(clip, 'windup'), first):
        hd = sp(clip, t, 'head')
        for e in els:
            eat(t, e, f'execute {BODY} positioned {loc(hd)} run ' + g.dust(PAL_SW[e][1], 1.0, '~ ~ ~', (0.15, 0.15, 0.15), 2))

    # -- per slice strike fx (per element)
    for i, (t, a0, a1) in enumerate(slices):
        for e in els:
            fx = [f'# Slice {i} (clip tick {t}, {a0} -> {a1} deg){"" if gold else ", element " + str(e)}: blade fx.',
                  f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p{pid}b{i}] run data merge entity @s {{block_state:{{id:"minecraft:white_concrete"}}}}']
            # the crescent body: translucent slabs at waist height (higher on her left), white-hot outer edge
            for th in range(95, -96, -10):
                if slice_of(th) != i:
                    continue
                y = 0.72 + 0.5 * (th + 95) / 190
                for blk, rr, ww, dy in ((SLAB_BLK[e][0], 3.6 * SW_K, 1.5 * SW_K, 0.0), (SLAB_BLK[e][1], 4.5 * SW_K, 0.32 * SW_K, 0.03)):
                    tr, q, sc = X.bar_tf(th, rr, 0.82 * SW_K, ww, 0.05, y + dy)
                    fx.append(f'execute {BODY} run ' + X.bd(blk, tr, q, sc, X.base_tags(pid, f'rlk_mb_gd_p{pid}w', f'rlk_mb_gd_p{pid}w{i}', 'rlk_mb_gd_wnew')))
            fx += [f'execute {BODY} run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_wnew] ~ ~ ~ ~ 0',
                   'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_wnew] remove rlk_mb_gd_wnew']
            n = max(2, int(abs(a0 - a1) / 7) + 1)
            for j in range(n):
                a = a0 + (a1 - a0) * j / (n - 1)
                for r, col, sc in ((2.9 * SW_K, PAL_SW[e][0], 1.5), (3.5 * SW_K, PAL_SW[e][1], 1.7), (4.1 * SW_K, PAL_SW[e][2], 1.3), (4.6 * SW_K, PAL_SW[e][3], 1.4)):
                    y = 1.2 - 0.14 * (r / SW_K - 2.9) - 0.15 * (j / n)
                    fx.append(f'execute {BODY} positioned {loc(polar(a, r, y))} run ' + g.dust(col, sc, '~ ~ ~', (0.06, 0.08, 0.06), 1))
            if gold:
                for _ in range(2):
                    a, r, size = rnd.uniform(a1, a0), rnd.uniform(4.55, 5.0) * SW_K, rnd.uniform(0.6, 1.5)
                    fx += [f'execute {BODY} rotated ~{n3(-a)} 0 run ' + g.card('shard', f'^ ^0.02 ^{n3(r)}', bb='vertical',
                                                                            s0=size * 0.6, s1=size, life=10, fade=4),
                           f'execute {BODY} rotated ~{n3(-a)} 0 positioned ^ ^0.2 ^{n3(r)} run ' + g.particle(GOLD_BLK, '~ ~ ~', (0.25, 0.1, 0.25), 0.15, 6)]
                am = (a0 + a1) / 2
                fx += [f'execute {BODY} rotated ~{n3(-am)} 0 positioned ^ ^0.3 ^{n3(4.2 * SW_K)} run ' + g.particle(BROWN_BLK, '~ ~ ~', (0.6, 0.1, 0.6), 0.2, 5),
                       f'execute {BODY} rotated ~{n3(-am)} 0 positioned ^ ^0.3 ^{n3(4.2 * SW_K)} run ' + g.particle(RED_BLK, '~ ~ ~', (0.5, 0.2, 0.5), 0.1, 3),
                       f'execute {BODY} rotated ~{n3(-am)} 0 positioned ^ ^0.6 ^{n3(4.4 * SW_K)} run ' + g.particle('wax_on', '~ ~ ~', (0.6, 0.4, 0.6), 0, 2)]
            else:
                fx += element_strike(g, rnd, e, a0, a1, SW_K)
            g.pw(key, f's{i}' if gold else f's{i}_{e}', fx)
            tl.at(t, g.fn(f'p/{key}/s{i}') if gold else f'execute if score #gdSwEl mb matches {e} run {g.fn(f"p/{key}/s{i}_{e}")}')
        tl.at(t + 3, f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p{pid}b{i}]')
        tl.at(t + 1, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p{pid}w{i}] run data merge entity @s '
                     f'{{start_interpolation:0,interpolation_duration:4,transformation:{{scale:[{n3(0.82 * SW_K)}f,0.01f,0.04f]}}}}')
        tl.at(t + 5, f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p{pid}w{i}]')
    tl.at(last + 3, f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p{pid}b]')

    if gold:
        # gold crescent cards following the blade (roll 180 = a left-to-right swing, spin + = to her right)
        tl.at(first, f'execute {BODY} run ' + g.card('crescent', '^ ^1.0 ^', rot='~-135 0', roll=180, spin=155, s0=9.6 * SW_K, s1=10.2 * SW_K, life=6, fade=2),
              f'execute {BODY} run ' + g.card('crescent', '^ ^0.55 ^', rot='~-120 0', roll=180, spin=140, s0=8.2 * SW_K, s1=8.8 * SW_K, life=7, fade=3))
        specs = X.cube_set(1101, 7, ['crimson', 'dark', 'red', 'rock', 'gold', 'dark'], (1.6 * SW_K, 0.2, 1.0 * SW_K), (0.14, 0.32), (0.8, 2.0),
                           up=0.6, delay=3)
        X.cubes(tl, pid, '11c', W(22), specs, f'{BODY} positioned ^-0.6 ^0.4 ^{n3(4.0 * SW_K)}', 12)
        tl.at(W(12), g.sound('item.trident.riptide_2', 0.7, 0.7))
        tl.at(first, g.sound('entity.player.attack.sweep', 1.0, 0.6), g.sound('item.trident.riptide_1', 0.35, 1.2))
        tl.at(W(22), g.sound('block.pointed_dripstone.land', 1.0, 0.9), g.sound('block.basalt.break', 0.9, 0.8),
              g.sound('entity.generic.explode', 0.35, 1.3))
        tl.at(W(23), g.sound('block.pointed_dripstone.land', 0.7, 1.15))
        tl.at(W(24), g.sound('block.amethyst_cluster.break', 0.5, 1.2))
        for t in range(W(26), W(33), 3):
            tl.at(t, f'execute {BODY} positioned ^ ^0.6 ^{n3(3.6 * SW_K)} run ' + g.particle('wax_on', '~ ~ ~', (2.4 * SW_K, 0.4, 1.4 * SW_K), 0, 3))
    else:
        # enchant (4-6): a light line through her and along the spear, a waist ring burst
        for e in els:
            for t in sorted({W(x) for x in (4, 5, 6)}):
                gp, tip = sp(clip, t, 'grip'), sp(clip, t)
                ln = [f'execute {BODY} positioned ^{n3(-2.6 + 0.4 * j)} ^1.75 ^0.35 run '
                      + g.dust_fade(WHITE, PAL_SW[e][1], 1.1, '~ ~ ~', (0, 0.01, 0), 1) for j in range(14)]
                ln += [f'execute {BODY} positioned {loc(lerp(gp, tip, s / 7))} run ' + g.dust(PAL_SW[e][3], 0.9, '~ ~ ~', (0.02, 0.02, 0.02), 1)
                       for s in range(8)]
                eat(t, e, *ln)
            eat(W(5), e, *[f'execute {BODY} positioned {loc(polar(a, 1.5, 1.35))} run ' + g.dust(PAL_SW[e][2] if a % 60 else PAL_SW[e][1], 1.0, '~ ~ ~', (0, 0, 0), 1)
                       for a in range(0, 360, 20)])
            pt = {1: ('small_flame', 0.01), 2: ('falling_water', 0), 3: ('electric_spark', 0.08), 4: ('snowflake', 0.01)}[e]
            for t in range(W(7), W(21), 2):
                eat(t, e, f'execute {BODY} positioned {loc(sp(clip, t))} run ' + g.particle(pt[0], '~ ~ ~', (0.25, 0.25, 0.25), pt[1], 2))
            # lingering ground fx to R+42 inside the arc
            for t in range(W(29), W(43), 3):
                for _ in range(2):
                    a, r = rnd.uniform(-95, 95), rnd.uniform(1.8, 4.6) * SW_K
                    eat(t, e, *[f'execute {BODY} rotated ~{n3(-a)} 0 positioned ^ ^0.08 ^{n3(r)} run ' + x for x in linger_fx(g, rnd, e)])
        tl.at(W(4), g.sound('block.beacon.activate', 0.7, 1.2))
        tl.at(W(5), g.sound('entity.warden.sonic_charge', 0.3, 1.6))
        tl.at(W(15), g.sound('item.trident.riptide_1', 0.7, 0.8))
        tl.at(first, g.sound('entity.player.attack.sweep', 1.0, 0.6), g.sound('item.trident.riptide_2', 0.4, 1.4))
        snd = {1: [(23, 'item.firecharge.use', 0.9, 0.8), (23, 'entity.blaze.shoot', 0.45, 0.7), (26, 'block.fire.ambient', 0.9, 1.0)],
               2: [(23, 'entity.player.splash.high_speed', 0.9, 1.0), (23, 'entity.generic.splash', 0.5, 1.3), (26, 'entity.player.splash', 0.5, 1.4)],
               3: [(23, 'entity.lightning_bolt.impact', 0.5, 1.8), (24, 'entity.lightning_bolt.impact', 0.35, 2.0),
                   (26, 'block.copper_bulb.turn_on', 0.6, 1.5), (27, 'entity.breeze.wind_burst', 0.3, 1.6)],
               4: [(23, 'block.glass.break', 0.9, 1.3), (23, 'block.powder_snow.break', 1.0, 1.0), (26, 'block.amethyst_block.chime', 0.7, 1.8)]}
        for e, lst in snd.items():
            for t, s, v, p in lst:
                tl.at(W(t), f'execute if score #gdSwEl mb matches {e} run ' + g.sound(s, v, p))

    for e in ([] if gold else els):
        for t, lines in sorted(etl[e].items()):
            g.pw(key, f'e{e}/{t}', [f'# {key} clip tick {t}, element {e}'] + lines)
            tl.at(t, f'execute if score #gdSwEl mb matches {e} run {g.fn(f"p/{key}/e{e}/{t}")}')
    what = 'Gold sweep (guard timeout)' if gold else 'Enchanted sweep (record complete; the core already turned the spear)'
    head = [f'# {what} start (@s = body): {clip} clip ({end} t). See p56.py for the timeline.',
            f'kill @e[tag=rlk_mb_gd_p{pid}]',
            FACE,
            g.play(clip),
            g.fn(f'p/{key}/slices')]
    if gold:
        head.append(f'execute {BODY} run {g.fn(f"p/{key}/rim0")}')
    else:
        head += [f'execute if score #gdSwEl mb matches {e} {BODY} run {g.fn(f"p/{key}/rim{e}")}' for e in els]
    tl.at(end, g.end())
    tl.write(head, [f'# {what} tick (@s = body, #gdPT = clip tick).'])
    g.pw(key, 'cancel', [f'# {what} cancel (any executor): rim bars, cubes, its slice hazards.',
                         f'kill @e[tag=rlk_mb_gd_p{pid}]'])


def element_strike(g, rnd, e, a0, a1, k=1.0):
    """Element strike fx inside the slice a0 -> a1 (@s = body); k = the arc radius over the authored r 5."""
    out = []
    a, r = rnd.uniform(min(a0, a1), max(a0, a1)), rnd.uniform(3.0, 4.3) * k
    at = f'execute {BODY} rotated ~{n3(-a)} 0 positioned ^ ^ ^{n3(r)} run '
    core, mid, deep = PAL_SW[e][2], PAL_SW[e][1], PAL_SW[e][0]
    shard = f'block{{block_state:"{EL_SHARD[e]}"}}'
    if e == 3:                                    # forked bolts + violet shards
        for j, p in enumerate(bolt_points(rnd, rnd.uniform(3.0, 3.8))):
            out.append(at + g.dust(core if j % 3 == 0 else mid, 0.9 if j % 3 == 0 else 1.2, f'^{n3(p[0])} ^{n3(p[1])} ^{n3(p[2])}', (0, 0, 0), 1))
        out += [at + g.particle('electric_spark', '~ ~0.2 ~', (0.4, 0.1, 0.4), 0.35, 10),
                at + g.particle(shard, '~ ~0.5 ~', (0.3, 0.3, 0.3), 0.25, 6),
                at + g.particle('end_rod', '~ ~0.4 ~', (0.3, 0.2, 0.3), 0.08, 3)]
    elif e == 1:                                  # flame bursts
        out += [at + g.particle('flame', '~ ~0.6 ~', (0.35, 0.8, 0.35), 0.04, 12),
                at + g.particle('lava', '~ ~0.2 ~', (0.3, 0.1, 0.3), 0, 2),
                at + g.particle('small_flame', '~ ~0.3 ~', (0.5, 0.2, 0.5), 0.02, 6),
                at + g.dust(mid, 1.6, '~ ~1 ~', (0.15, 0.8, 0.15), 6)]
    elif e == 2:                                  # splashes
        out += [at + g.particle('splash', '~ ~0.3 ~', (0.7, 0.2, 0.7), 0, 30),
                at + g.particle('falling_water', '~ ~1.2 ~', (0.5, 0.8, 0.5), 0, 10),
                at + g.particle('bubble_pop', '~ ~0.5 ~', (0.5, 0.4, 0.5), 0.02, 6),
                at + g.dust(mid, 1.5, '~ ~0.8 ~', (0.3, 0.5, 0.3), 8)]
    else:                                         # ice shards
        out += [at + g.particle('snowflake', '~ ~0.8 ~', (0.5, 0.8, 0.5), 0.03, 14),
                at + g.particle(shard, '~ ~0.5 ~', (0.4, 0.4, 0.4), 0.2, 10),
                at + g.particle('item_snowball', '~ ~0.5 ~', (0.3, 0.3, 0.3), 0.05, 4),
                at + g.dust(core, 1.4, '~ ~0.9 ~', (0.1, 0.7, 0.1), 8)]
    return out


def linger_fx(g, rnd, e):
    """Lingering ground fx at the execution point (on the floor)."""
    mid, light = PAL_SW[e][1], PAL_SW[e][3]
    if e == 3:                                    # small ground arcs
        pts = []
        x, z = 0.0, 0.0
        for j in range(5):
            nx, nz = x + rnd.uniform(-0.3, 0.3), z + rnd.uniform(0.15, 0.35)
            pts.append(g.dust(mid if j % 2 else light, 0.8, f'^{n3(nx)} ^{n3(rnd.uniform(0, 0.15))} ^{n3(nz)}', (0, 0, 0), 1))
            x, z = nx, nz
        return pts + [g.particle('electric_spark', '~ ~0.1 ~', (0.3, 0.05, 0.3), 0.2, 3)]
    if e == 1:
        return [g.particle('small_flame', '~ ~0.1 ~', (0.5, 0.05, 0.5), 0.01, 4), g.particle('smoke', '~ ~0.3 ~', (0.3, 0.1, 0.3), 0.01, 2)]
    if e == 2:
        return [g.particle('falling_water', '~ ~0.4 ~', (0.4, 0.2, 0.4), 0, 4)] + [
            g.dust(light, 0.7, f'^{n3(0.55 * math.sin(math.radians(a)))} ^0.02 ^{n3(0.55 * math.cos(math.radians(a)))}', (0, 0, 0), 1)
            for a in range(0, 360, 60)]
    return [g.particle('snowflake', '~ ~0.2 ~', (0.5, 0.1, 0.5), 0.01, 4), g.dust(light, 0.9, '~ ~0.05 ~', (0.5, 0.02, 0.5), 4)]


# =============================================================================================
# chaos fail spears
# star kinds: 1-4 element, 5 inert gold, 6 inert blue -> palette (core, mid, deep), beam glass, style, crack colour
KIND = {1: ((1.0, 0.86, 0.66), (1.0, 0.54, 0.30), (0.78, 0.25, 0.10), 'minecraft:orange_stained_glass', 'fire', (0.97, 0.55, 0.15)),
        2: ((0.85, 0.96, 1.0), (0.36, 0.78, 1.0), (0.16, 0.47, 0.78), 'minecraft:light_blue_stained_glass', 'water', (0.22, 0.45, 0.85)),
        3: ((0.99, 0.89, 0.99), (0.89, 0.52, 0.99), (0.55, 0.24, 0.78), 'minecraft:magenta_stained_glass', 'spark', (0.70, 0.35, 0.95)),
        4: ((0.94, 1.0, 1.0), (0.64, 1.0, 0.99), (0.30, 0.66, 0.78), 'minecraft:white_stained_glass', 'ice', (0.45, 0.80, 0.95)),
        5: ((1.0, 0.99, 0.68), (0.84, 0.67, 0.18), (0.63, 0.39, 0.19), 'minecraft:yellow_stained_glass', 'gold', (0.97, 0.83, 0.15)),
        6: ((0.82, 0.93, 1.0), (0.24, 0.43, 0.80), (0.18, 0.23, 0.75), 'minecraft:light_blue_stained_glass', 'water', (0.22, 0.38, 0.77))}
TINT1 = {1: 'pyro', 2: 'hydro', 3: 'electro', 4: 'cryo', 5: 'gold', 6: 'electro'}   # red -> (violet ->) star colour
TINT2 = {6: 'hydro'}
DECAL_W = 1.3 * AREA              # half width of the star arms at the centre (x1.2 with the disc)
# readable on the pink centre star and the white marble: opaque crimson fill, black rim (a pink rim vanished there)
DECAL_FILL, DECAL_RIM = 'minecraft:red_concrete', 'minecraft:black_concrete'
RING_N = 24                       # bars of the damage ring at FAIL_R
DECAL_FB = (4.5 * AREA, 7.5 * AREA)   # half length of the front/back arm pair, decal -> decal + 6
DECAL_SS = (2.7 * AREA, 9.5 * AREA)   # half length of the side arm pair (m4: +-2.7 -> > +-9 in 6 t), x1.2


def fail(g):
    k, pid = 'fail', 13
    tl = X.TL(g, k)
    rnd = random.Random(1313)
    F = lambda rel: g.fn(f'p/fail/{rel}')

    # ---- per kind (positioned at the target, rotated as it = toward the arena centre)
    for kind, (core, mid, deep, glass, style, crack) in KIND.items():
        # impact flash: column + starburst rays
        hit = [f'# Impact of a kind-{kind} spear ({style}) at the target: flash column and starburst rays.']
        for blk, w, nm in ((glass, 1.3 * AREA, 'fo'), ('minecraft:white_concrete', 0.45 * AREA, 'fi')):
            hit.append(X.bd(blk, (-w / 2, 0, -w / 2), X.QI, (w, 16.0, w), X.base_tags(pid, 'rlk_mb_gd_p13f', 'rlk_mb_gd_p13fnew')))
        for a in range(0, 360, 45):
            for el, rr in ((10, 1.4 * AREA), (25, 2.4 * AREA), (10, 3.4 * AREA), (35, 4.2 * AREA)):
                hit.append(f'execute rotated ~{a + (el % 7)} 0 positioned ^ ^{n3(0.4 + rr * math.tan(math.radians(el)) * 0.5)} ^{n3(rr)} run '
                           + g.dust(core if rr < 3 * AREA else mid, 1.6 if rr < 3 * AREA else 1.2, '~ ~ ~', (0.05, 0.05, 0.05), 1))
        hit += [g.dust(WHITE, 2.6, '~ ~1 ~', (0.5, 1.2, 0.5), 30),
                g.particle('end_rod', '~ ~1 ~', (0.3, 0.6, 0.3), 0.25, 14)]
        if style == 'gold':
            hit.append(g.card('burst', '~ ~1.4 ~', bb='center', spin=20, s0=1.0, s1=4.8, life=6, fade=3))
        g.pw(k, f'hit{kind}', hit)
        # dome of light r 1.45 x1.2
        DR = 1.45 * AREA
        dome = [f'# Dome of light (kind {kind}), r {DR:.2f} (m4 2.9 b wide and tall, x1.2 with the disc).']
        for el, n in ((0, 14), (30, 12), (60, 7), (88, 1)):
            for j in range(n):
                p = polar(360 * j / n + el, DR * math.cos(math.radians(el)), DR * math.sin(math.radians(el)))
                dome.append(f'positioned {loc(p)}')
        dome = [dome[0]] + [f'execute {d} run ' + g.dust(mid, 2.6, '~ ~ ~', (0.08, 0.08, 0.08), 1) for d in dome[1:]]
        dome += [g.dust(core, 2.0, '~ ~0.7 ~', (0.45 * AREA, 0.45 * AREA, 0.45 * AREA), 16)]
        if style == 'gold':
            dome.append(g.card('glow', '~ ~0.9 ~', bb='center', s0=2.4, s1=3.4, life=4, fade=2))
        g.pw(k, f'dome{kind}', dome)
        # blast: X beams, spike field / splash / flames / sparks, rocks
        bl = [f'# Blast of a kind-{kind} spear ({style}): X of crossed light beams, field, debris.']
        hc, tilt, L = 2.4 * AREA, 28, 10.0
        for sgn in (1, -1):
            q = qaxis((0, 0, 1), -sgn * tilt)
            w = 0.42
            off = qrot(q, (w / 2, 0, w / 2))
            base = (-sgn * hc * math.tan(math.radians(tilt)), 0.0, 0.0)
            bl.append(X.bd(glass, sub(base, off), q, (w, L, w), X.base_tags(pid, 'rlk_mb_gd_p13x', 'rlk_mb_gd_p13xnew')))
        bl += ['tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] ~ ~ ~ ~ 0',
               'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13xnew] remove rlk_mb_gd_p13xnew',
               g.particle('explosion', '~ ~0.8 ~', (1.0, 0.4, 1.0), 0, 3),
               g.particle(BROWN_BLK, '~ ~0.5 ~', (1.6 * AREA, 0.4, 1.6 * AREA), 0.3, 20)]
        if style == 'gold':
            for _ in range(12):
                a, r, size = rnd.uniform(0, 360), rnd.uniform(1.5, 8.0), rnd.uniform(1.0, 3.0)
                bl.append(f'execute rotated ~{n3(a)} 0 run ' + g.card('shard', f'^ ^0.02 ^{n3(r)}', bb='vertical', s0=size * 0.5, s1=size,
                                                                      life=int(rnd.uniform(16, 22)), fade=6))
            bl += [g.particle(GOLD_BLK, '~ ~0.4 ~', (3.0 * AREA, 0.3, 3.0 * AREA), 0.2, 40),
                   g.dust(core, 1.6, '~ ~1.5 ~', (3.0 * AREA, 1.2, 3.0 * AREA), 30),
                   g.sound('entity.generic.explode', 1.0, 0.7), g.sound('block.amethyst_cluster.break', 1.0, 0.6),
                   g.sound('block.pointed_dripstone.land', 1.0, 1.0), g.sound('entity.lightning_bolt.thunder', 0.3, 1.6),
                   g.sound('block.basalt.break', 0.9, 0.8)]
        elif style in ('water', 'ice'):
            for _ in range(10):
                a, r = rnd.uniform(0, 360), rnd.uniform(0.8, 4.0) * AREA
                bl.append(f'execute rotated ~{n3(a)} 0 positioned ^ ^0.9 ^{n3(r)} run ' + g.dust(core, 1.5, '~ ~ ~', (0.05, 0.8, 0.05), 6))
            ice = 'block{block_state:"minecraft:packed_ice"}' if style == 'ice' else 'block{block_state:"minecraft:blue_ice"}'
            bl += [g.particle('splash', '~ ~0.4 ~', (2.4 * AREA, 0.4, 2.4 * AREA), 0, 60),
                   g.particle('falling_water', '~ ~1.5 ~', (2.4 * AREA, 1.2, 2.4 * AREA), 0, 20),
                   g.particle(ice, '~ ~0.6 ~', (2.0 * AREA, 0.6, 2.0 * AREA), 0.25, 30),
                   g.dust(mid, 1.8, '~ ~1 ~', (2.0 * AREA, 0.8, 2.0 * AREA), 30),
                   g.sound('entity.generic.explode', 0.9, 0.8), g.sound('block.glass.break', 1.0, 0.7),
                   g.sound('entity.player.splash.high_speed', 0.9, 1.0), g.sound('block.powder_snow.break', 1.0, 1.0)]
            if style == 'ice':
                bl.append(g.particle('snowflake', '~ ~1 ~', (2.4 * AREA, 1.0, 2.4 * AREA), 0.04, 30))
        elif style == 'fire':
            bl += [g.particle('flame', '~ ~0.8 ~', (2.4 * AREA, 1.0, 2.4 * AREA), 0.05, 40), g.particle('lava', '~ ~0.4 ~', (2.0 * AREA, 0.3, 2.0 * AREA), 0, 10),
                   g.particle('large_smoke', '~ ~1 ~', (1.6 * AREA, 0.8, 1.6 * AREA), 0.02, 10), g.dust(mid, 1.8, '~ ~1 ~', (2.4 * AREA, 1.0, 2.4 * AREA), 30),
                   g.sound('entity.generic.explode', 1.0, 0.8), g.sound('item.firecharge.use', 1.0, 0.7),
                   g.sound('entity.blaze.shoot', 0.6, 0.6)]
        else:                                   # spark
            for j in range(3):
                a = 120 * j + rnd.uniform(-30, 30)
                r = rnd.uniform(1.5, 3.5) * AREA
                for m, p in enumerate(bolt_points(rnd, rnd.uniform(3.5, 5.0), segs=6, jit=0.45, n=2)):
                    bl.append(f'execute rotated ~{n3(a)} 0 positioned ^{n3(p[0])} ^{n3(p[1])} ^{n3(r + p[2])} run '
                              + g.dust(core if m % 3 == 0 else mid, 1.1, '~ ~ ~', (0, 0, 0), 1))
            bl += [g.particle('electric_spark', '~ ~0.8 ~', (2.4 * AREA, 0.8, 2.4 * AREA), 0.4, 40), g.particle('end_rod', '~ ~1 ~', (1.6 * AREA, 0.8, 1.6 * AREA), 0.1, 12),
                   g.dust(mid, 1.8, '~ ~1 ~', (2.4 * AREA, 1.0, 2.4 * AREA), 30),
                   g.sound('entity.generic.explode', 0.9, 0.8), g.sound('entity.lightning_bolt.impact', 1.0, 0.6),
                   g.sound('entity.lightning_bolt.thunder', 0.3, 1.6), g.sound('block.copper_bulb.turn_on', 0.7, 1.2)]
        g.pw(k, f'blast{kind}', bl)
        # after-blast crackle / shimmer
        if style == 'gold':
            g.pw(k, f'tail{kind}', [g.sound('block.pointed_dripstone.land', 0.8, 1.2), g.particle('wax_on', '~ ~1 ~', (2.5, 1.0, 2.5), 0, 6)])
        elif style in ('water', 'ice'):
            g.pw(k, f'tail{kind}', [g.sound('block.amethyst_block.chime', 0.8, 1.6 + 0.1 * (kind % 4)), g.particle('end_rod', '~ ~1 ~', (2.0, 1.0, 2.0), 0.02, 4)])
        elif style == 'fire':
            g.pw(k, f'tail{kind}', [g.sound('block.fire.ambient', 0.8, 1.0), g.particle('small_flame', '~ ~0.3 ~', (2.0, 0.2, 2.0), 0.01, 8)])
        else:
            g.pw(k, f'tail{kind}', [g.sound('block.copper_bulb.turn_on', 0.5, 1.6), g.particle('electric_spark', '~ ~0.3 ~', (2.0, 0.2, 2.0), 0.2, 8)])
        # residue: crimson (or blue) floor + glowing cracks radiating >= 8 b
        floor = (0.34, 0.15, 0.13) if style in ('gold', 'fire', 'spark') else (0.23, 0.38, 0.77)
        res = [f'# Residue (kind {kind}): tinted floor and glowing cracks.', g.dust(floor, 2.6, '~ ~0.08 ~', (2.4 * AREA, 0.02, 2.4 * AREA), 10)]
        for a in range(0, 360, 45):
            for r in (1.6, 3.6, 6.0, 8.0):
                res.append(f'execute rotated ~{n3(a + 9 * math.sin(r))} 0 positioned ^ ^0.06 ^{n3(r)} run ' + g.dust(crack, 1.0, '~ ~ ~', (0.12, 0, 0.12), 1))
        g.pw(k, f'res{kind}', res)

    # ---- per kind tint of the spear (as the spear)
    for kind in KIND:
        g.pw(k, f'tint1_{kind}', [f'# As spear (kind {kind}): red -> {TINT1[kind]}.',
                                  f'data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_{TINT1[kind]}"'])
    for kind, m in TINT2.items():
        g.pw(k, f'tint2_{kind}', [f'# As spear (kind {kind}): -> {m}.',
                                  f'data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_{m}"'])

    # ---- decal streak functions (positioned at the target, rotated as it): pink light streaks on the rims
    steps = list(range(FAIL_DECAL + 1, FAIL_DECAL + 7, 2)) + [None]
    for st in steps:
        if st is None:
            fb, ss = DECAL_FB[1], DECAL_SS[1]
        else:
            u = (st - FAIL_DECAL) / 6
            fb, ss = lerp((DECAL_FB[0], DECAL_SS[0]), (DECAL_FB[1], DECAL_SS[1]), u)
        pts = X.rhombus_edges(0, fb + 0.3, DECAL_W + 0.2, 3) + X.rhombus_edges(90, ss + 0.3, DECAL_W + 0.2, 3)
        g.pw(k, f'streak{st if st else "f"}', ['# Pink light streaks standing on the decal rims.'] + [
            f'execute positioned {loc(p, 0.45)} run ' + g.dust_fade((0.88, 0.33, 0.46), (0.53, 0.18, 0.30), 0.9, '~ ~ ~', (0.03, 0.35, 0.03), 2)
            for p in pts])

    # ---- per spear j
    for j in (0, 1):
        b = FAIL_GAP * j
        T = f'@e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1]'
        Kc = f'@e[type=minecraft:marker,tag=rlk_mb_gd_p13k{j},limit=1]'
        S = f'@e[type=minecraft:item_display,tag=rlk_mb_gd_p13s{j},limit=1]'
        KS = f'#gp13K{j}'
        cond = f'if score #gdFailN mb matches {j + 1}..'
        ATT = f'at {T} rotated as {T}'
        J = lambda rel: g.fn(f'p/fail/j{j}/{rel}')

        def pw(rel, lines):
            g.pw(k, f'j{j}/{rel}', lines)

        def at(t, *lines):
            tl.at(t + b, *[f'execute {cond} run {x}' for x in lines])

        # 23: lock + gold cube column above the target (lower half)
        col = X.cube_set(1330 + j, 6, ['goldb', 'gold', 'goldb', 'amber', 'goldb'], (0.12, 0.0, 0.12), (0.55, 0.9), (0, 0))
        hs = (6.0, 6.9, 7.9, 8.9, 9.9, 11.0)
        colsum = []
        for m, c in enumerate(col):
            s = c['s']
            t0 = mul(qrot(c['q0'], (0.05, 0.05, 0.05)), -1)
            nbt = (f'{{Tags:{tags(*X.base_tags(pid, f"rlk_mb_gd_p13c{j}", f"rlk_mb_gd_p13c{j}_{m}"))},'
                   f'block_state:{{id:"{X.CUBE_BLOCK[c["kind"]]}"}},brightness:{{sky:15,block:15}},view_range:2f,shadow_radius:0f,'
                   f'teleport_duration:0,interpolation_duration:0,transformation:{tf(t0, c["q0"], (0.1, 0.1, 0.1))}}}')
            colsum.append((m, f'execute {ATT} positioned ^{n3(c["off"][0])} ^{n3(hs[m])} ^{n3(c["off"][2])} run summon minecraft:block_display ~ ~ ~ {nbt}',
                           tf(mul(qrot(c['q0'], (s / 2, s / 2, s / 2)), -1), c['q0'], (s, s, s))))
        pw('lock', [f'# Spear {j + 1} (T0+{FAIL_COL + b}): the target locks on the player (decal frame: toward the arena centre);',
                    '# a gold cube column starts above it.',
                    f'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j}]',
                    f'scoreboard players operation {KS} mb = #gdFailK{j + 1} mb',
                    f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {{Tags:{tags(*X.base_tags(pid, f"rlk_mb_gd_p13t{j}"))}}}',
                    f'# the disc (r {FAIL_R:g}) stays inside the walkable arena and still covers a player standing at the wall',
                    clamp_in(T, WALK_R - FAIL_R),
                    f'execute as {T} at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                    f'execute at {T} run summon minecraft:marker ~ ~11 ~ {{Tags:{tags(*X.base_tags(pid, f"rlk_mb_gd_p13k{j}"))}}}']
           + [c[1] for c in colsum[:3]]
           + [f'execute {ATT} run ' + g.particle(GOLD_BLK, '~ ~7 ~', (0.3, 1.0, 0.3), 0.05, 10),
              g.sound('block.respawn_anchor.charge', 0.6, 0.9)])
        at(FAIL_COL, J('lock'))
        # chain from her chest to the column top
        pw('chain', ['# A gold chain step from her chest toward the column top (recursive, <= 30 steps).',
                     'scoreboard players add #gp13D mb 1',
                     g.dust((0.98, 0.91, 0.56), 1.3, '~ ~ ~', (0.05, 0.05, 0.05), 1),
                     g.dust_fade(RED_EDGE, CRIMSON_DARK, 1.0, '~ ~ ~', (0.08, 0.08, 0.08), 1),
                     'execute if score #gp13D mb matches 30.. run return 0',
                     f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_gd_p13k{j},distance=..0.9] run return 0',
                     f'execute positioned ^ ^ ^0.75 run {J("chain")}'])
        pw('form', [f'# Spear {j + 1} (T0+{FAIL_COL + 1 + b}): column upper half, the chain from her, the forming roar.']
           + [c[1] for c in colsum[3:]]
           + [f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p13c{j}_{m},limit=1] run data merge entity @s '
              f'{{start_interpolation:0,interpolation_duration:2,transformation:{full}}}' for m, _, full in colsum[:3]]
           + ['scoreboard players set #gp13D mb 0',
              f'execute at @s positioned ~ ~{"6.0" if j == 0 else "3.0"} ~ facing entity {Kc} feet run {J("chain")}',
              f'execute {ATT} run ' + g.sound('block.respawn_anchor.charge', 0.8, 0.8),
              f'execute {ATT} run ' + g.sound('block.beacon.power_select', 0.6, 0.6),
              f'execute {ATT} run ' + g.sound('block.amethyst_block.resonate', 0.8, 0.8),
              f'execute {ATT} run ' + g.sound('entity.warden.sonic_charge', 0.3, 1.2)])
        at(FAIL_COL + 1, J('form'))
        at(FAIL_COL + 2, *[f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p13c{j}_{m},limit=1] run data merge entity @s '
                           f'{{start_interpolation:0,interpolation_duration:2,transformation:{full}}}' for m, _, full in colsum[3:]])
        # 25: decal + hazard + the giant red spear
        dec = [f'# Spear {j + 1} (T0+{FAIL_DECAL + b}): the hazard (disc r {FAIL_R}, {DMG["fail"]} %, the star\'s element), the red',
               '# concave 4-point star decal on the player (front arm toward the arena centre) and the giant red spear',
               '# growing out of the column, point down, its tip 3.8 b above the target.',
               *g.hz_opts(sfx=0, kb=KB['default'], linger=2)]
        for kind in range(1, 7):
            if kind <= 4:
                dec.append(f'execute if score {KS} mb matches {kind} run scoreboard players set #hzEl mb {kind}')
            dec.append(f'execute if score {KS} mb matches {kind} run scoreboard players set #hzCol mb {STAR_HZCOL[kind]}')
        dec += [f'execute at {T} run {g.hz_disc(FAIL_R, FAIL_TELL, DMG["fail"])}',
                *hz_tag(pid)]
        for nm, yaw, hl, hw, y, blk in (('fr', 0, DECAL_FB[0] + 0.35, DECAL_W + 0.25, 0.012, DECAL_RIM),
                                        ('ff', 0, DECAL_FB[0], DECAL_W, 0.036, DECAL_FILL),
                                        ('sr', 90, DECAL_SS[0] + 0.35, DECAL_W + 0.25, 0.012, DECAL_RIM),
                                        ('sf', 90, DECAL_SS[0], DECAL_W, 0.036, DECAL_FILL)):
            tr, rL, rS, rR = X.rhombus_tf(yaw, hl, hw, 0.02, y)
            dec.append(f'execute at {T} run summon minecraft:block_display ~ ~ ~ {{Tags:{tags(*X.base_tags(pid, f"rlk_mb_gd_p13d{j}", f"rlk_mb_gd_p13d{j}{nm}", "rlk_mb_gd_p13dnew"))},'
                       f'block_state:{{id:"{blk}"}},brightness:{{sky:15,block:15}},view_range:2f,shadow_radius:0f,teleport_duration:0,'
                       f'interpolation_duration:0,transformation:{tf(tr, rL, rS, rR)}}}')
        # the damage disc itself: a crimson ring at r FAIL_R on a black outline (the star's diagonals end inside it)
        for m in range(RING_N):
            th = 360 * m / RING_N
            for blk, rr, ww, hh, yy in ((DECAL_RIM, FAIL_R + 0.07, 0.3, 0.02, 0.05), (DECAL_FILL, FAIL_R, 0.15, 0.025, 0.062)):
                tr, q, sc = X.bar_tf(th, rr + ww / 2, 2 * math.pi * FAIL_R / RING_N + 0.06, ww, hh, yy)
                dec.append(f'execute at {T} run ' + X.bd(blk, tr, q, sc, X.base_tags(pid, f'rlk_mb_gd_p13d{j}', 'rlk_mb_gd_p13dnew')))
        dec += [f'execute {ATT} run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13dnew] ~ ~ ~ ~ 0',
                'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13dnew] remove rlk_mb_gd_p13dnew',
                f'execute {ATT} positioned ~ ~11.9 ~ run {g.rig("prop/spear")}',
                'execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] run data merge entity @s '
                '{transformation:{translation:[0f,0f,0f],left_rotation:[1f,0f,0f,0f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]},'
                'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/guardian/prop_spear_red"}}}',
                f'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13s{j}',
                'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13',
                f'execute {ATT} run ' + g.dust((0.80, 0.16, 0.28), 1.6, '~ ~0.15 ~', (1.0, 0.02, 1.0), 16),
                f'execute {ATT} run ' + g.particle(RED_BLK, '~ ~9 ~', (0.3, 1.5, 0.3), 0, 12)]
        if j == 0:
            dec.append(g.voice_attack())
        pw('decal', dec)
        at(FAIL_DECAL, J('decal'))
        # 26: the side arms open, the spear grows to scale 5.5
        op = [f'# Spear {j + 1}: decal arms open over 6 t (m4 f110-126), the blade grows to full size in 4 t.']
        for nm, yaw, hl, hw, y in (('fr', 0, DECAL_FB[1] + 0.35, DECAL_W + 0.25, 0.012), ('ff', 0, DECAL_FB[1], DECAL_W, 0.036),
                                   ('sr', 90, DECAL_SS[1] + 0.35, DECAL_W + 0.25, 0.012), ('sf', 90, DECAL_SS[1], DECAL_W, 0.036)):
            tr, rL, rS, rR = X.rhombus_tf(yaw, hl, hw, 0.02, y)
            op.append(f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p13d{j}{nm},limit=1] run data merge entity @s '
                      f'{{start_interpolation:0,interpolation_duration:6,transformation:{tf(tr, rL, rS, rR)}}}')
        op += [f'execute as {S} run data merge entity @s {{start_interpolation:0,interpolation_duration:4,'
               'transformation:{translation:[0f,0f,0f],left_rotation:[1f,0f,0f,0f],scale:[5.5f,5.5f,5.5f],right_rotation:[0f,0f,0f,1f]}}',
               f'execute {ATT} run ' + g.particle(GOLD_BLK, '~ ~8 ~', (0.3, 2.0, 0.3), 0.05, 10)]
        pw('open', op)
        at(FAIL_DECAL + 1, J('open'))
        for st in steps:
            if st is not None:
                at(st, f'execute {ATT} run {F(f"streak{st}")}')
        for t in range(FAIL_DECAL + 7, FAIL_HIT, 2):
            at(t, f'execute {ATT} run {F("streakf")}')
        # 29-31: the column cubes melt into the blade
        at(FAIL_COL + 6, *[f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p13c{j}_{m},limit=1] run data merge entity @s '
                           f'{{start_interpolation:0,interpolation_duration:3,transformation:{tf((0, 0, 0), X.QI, (0, 0, 0))}}}' for m in range(6)])
        at(FAIL_COL + 9, f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p13c{j}]')
        # hang, colour change, whistle
        at(fail_t(35), f'execute {ATT} run ' + g.sound('block.beacon.ambient', 0.7, 0.5))
        tint = [f'# Spear {j + 1}: red -> the star colour (m4 +37..+40, played +{fail_t(37)}..+{fail_t(40)}), top to bottom, chime.',
                f'execute {ATT} run ' + g.sound('block.amethyst_block.chime', 0.9, 1.5)]
        for kind in KIND:
            tint.append(f'execute if score {KS} mb matches {kind} as {S} run {F(f"tint1_{kind}")}')
            tint += [f'execute if score {KS} mb matches {kind} {ATT} positioned ~ ~{n3(11.0 - 1.4 * m)} ~ run '
                     + g.dust(KIND[kind][0], 1.3, '~ ~ ~', (0.25, 0.3, 0.25), 3) for m in range(5)]
        pw('tint', tint)
        at(fail_t(37), J('tint'))
        at(fail_t(40), *[f'execute if score {KS} mb matches {kind} as {S} run {F(f"tint2_{kind}")}' for kind in TINT2],
           f'execute {ATT} run ' + g.dust((0.92, 0.94, 1.0), 1.0, '~ ~7 ~', (0.25, 2.5, 0.25), 8))
        at(fail_t(44), f'execute {ATT} run ' + g.sound('item.trident.riptide_3', 0.5, 1.4))
        # 49: drop (<= 1 t) + impact
        drop = [f'# Spear {j + 1} (T0+{FAIL_HIT + b}): it drops in 1 t (teleport_duration 1) and strikes; the hazard resolves this tick.',
                f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p13d{j}]',
                f'execute as {S} at @s run tp @s ~ ~-4.2 ~']
        for kind in KIND:
            drop.append(f'execute if score {KS} mb matches {kind} {ATT} run {F(f"hit{kind}")}')
        drop += [f'execute {ATT} run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p13fnew] ~ ~ ~ ~ 0',
                 f'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13fnew] add rlk_mb_gd_p13f{j}',
                 'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13fnew] remove rlk_mb_gd_p13fnew',
                 f'execute {ATT} run ' + g.sound('item.trident.hit_ground', 1.0, 0.5),
                 f'execute {ATT} run ' + g.sound('entity.lightning_bolt.impact', 0.6, 0.8)]
        pw('drop', drop)
        at(FAIL_HIT, J('drop'))
        at(FAIL_HIT + 1, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p13f{j}] run data merge entity @s '
                         '{start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,16f,0f],right_rotation:[0f,0f,0f,1f]}}',
           *[f'execute if score {KS} mb matches {kind} {ATT} run {F(f"dome{kind}")}' for kind in KIND])
        at(FAIL_HIT + 4, f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p13f{j}]')
        bl = [f'# Spear {j + 1} (T0+{FAIL_HIT + 2 + b}): the blast of its kind; the X beams take this spear\'s tag.']
        bl += [f'execute if score {KS} mb matches {kind} {ATT} run {F(f"blast{kind}")}' for kind in KIND]
        bl += [f'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_p13x,tag=!rlk_mb_gd_p13x0,tag=!rlk_mb_gd_p13x1] add rlk_mb_gd_p13x{j}']
        pw('blast', bl)
        at(FAIL_HIT + 2, J('blast'))
        specs = X.cube_set(1349 + j, 9, ['rock', 'dark', 'gold', 'rock', 'goldb', 'crimson', 'brown'], (1.2 * AREA, 0.3, 1.2 * AREA), (0.2, 0.5),
                           (1.5 * AREA, 3.4 * AREA), up=0.6, delay=2)
        X.cubes(tl, pid, f'13r{j}', FAIL_HIT + 2 + b, specs, f'at {T} positioned ~ ~0.5 ~', 14, cond=cond)
        at(FAIL_HIT + 3, f'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p13x{j}] run data merge entity @s '
                         '{start_interpolation:0,interpolation_duration:5,transformation:{scale:[0f,10f,0f]}}')
        at(FAIL_HIT + 9, f'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p13x{j}]')
        for t in (FAIL_HIT + 4, FAIL_HIT + 6, FAIL_HIT + 9, FAIL_HIT + 12, FAIL_HIT + 15):
            at(t, *[f'execute if score {KS} mb matches {kind} {ATT} run {F(f"tail{kind}")}' for kind in KIND])
        for t in range(FAIL_HIT + 5, FAIL_HIT + 34, 4):
            at(t, *[f'execute if score {KS} mb matches {kind} {ATT} run {F(f"res{kind}")}' for kind in KIND])
        # planted ~20 t, dissolves upward into cubes over 10 t, gone 30 t after the impact
        diss = [f'# Spear {j + 1}: dissolves upward into cubes.',
                f'execute as {S} run data merge entity @s {{start_interpolation:0,interpolation_duration:10,'
                'transformation:{translation:[0f,3f,0f],left_rotation:[1f,0f,0f,0f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}',
                f'execute {ATT} run ' + g.sound('block.amethyst_cluster.break', 0.35, 1.6)]
        for kind in KIND:
            blk = 'block{block_state:"minecraft:gold_block"}' if kind in (1, 5) else f'block{{block_state:"{KIND[kind][3]}"}}'
            diss.append(f'execute if score {KS} mb matches {kind} {ATT} run ' + g.particle(blk, '~ ~4 ~', (0.3, 3.0, 0.3), 0.05, 16))
        diss.append(f'execute {ATT} run ' + g.particle(BLACK_BLK, '~ ~4 ~', (0.3, 3.0, 0.3), 0.05, 8))
        pw('dissolve', diss)
        at(FAIL_HIT + 20, J('dissolve'))
        at(FAIL_HIT + 25, f'execute {ATT} run ' + g.particle(RED_BLK, '~ ~6 ~', (0.3, 2.5, 0.3), 0.05, 8))
        at(FAIL_HIT + 30, f'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s{j}]',
           f'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j}]', f'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p13k{j}]')

    last1, last2 = FAIL_HIT + 31, FAIL_HIT + FAIL_GAP + 31
    # m4: she leaves the centre about 10 t after the last impact while the giant spear still stands; the slot keeps
    # running the harmless tail (dissolve, residue) until the end
    tl.at(FAIL_HIT + FAIL_REL, f'execute if score #gdFailN mb matches 1 run {g.release()}')
    tl.at(FAIL_HIT + FAIL_GAP + FAIL_REL, f'execute if score #gdFailN mb matches 2.. run {g.release()}')
    tl.at(last1, f'execute if score #gdFailN mb matches 1 run {g.end()}')
    tl.at(last2, f'execute if score #gdFailN mb matches 2.. run {g.end()}')
    tl.write(['# Fail spears start (@s = body, T0 = the chaos timer ran out; the core plays chaos_fail and the absorption).',
              '# #gdFailN surviving stars, #gdFailK1/#gdFailK2 their kinds; one spear each, 31 t apart. See p56.py.',
              'kill @e[tag=rlk_mb_gd_p13]',
              'scoreboard players set #gp13D mb 0',
              f'execute if score #gdFailN mb matches 1 run {g.set_len(last1)}'],
             ['# Fail spears tick (@s = body, #gdPT = ticks since T0).',
              f'execute unless score #gdFailN mb matches 1.. run return run {g.end()}'])
    g.pw(k, 'cancel', ['# Fail spears cancel (any executor): spears, targets, decals, columns, beams, cubes, hazards.',
                       'kill @e[tag=rlk_mb_gd_p13]',
                       'scoreboard players set #gp13D mb 0'])
