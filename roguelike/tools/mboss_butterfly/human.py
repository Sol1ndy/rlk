"""Human-form patterns of the butterfly: H1 달빛 발차기, H2 달빛 점프, H3 달빛 돌진, H4 광폭한 진공.

Stage 2 (the human-pattern author), faithful to the scratchpad specs mb2/spec/H1_kick_combo.md .. H4_vacuum.md and the
binding plan mb2/plan.md (its "Stage-2 decisions"):
- telegraphs: every hit is a framework hazard (hz/*, quiet: #hzQuiet 1, silent: #hzSfx 0, Q7) paired in the same tick
  with the kit's ground decal of the same shape and tell (fx/tele/*), at least 10 t ahead of its strike;
- damage shapes, volley groups (one hit per group), element (Dendro, the registry default), knockback and the api.DMG
  coefficients as the specs' §5; H4's blade is a framework projectile (blade shape, 0.75 b/t, no homing);
- fx: the kit presets (bf_fx_api.md §7 / §9) plus single kit cards for the spec's extra layers; sounds: the kit's
  vanilla recipes on the main events plus single vanilla layers for the rest of the spec's audio timeline;
- AI: the bands and weights of README §2, H2's close-in (core), the facing / tracking spans and the aim locks of each
  spec's §2 (a locked aim is the rotation of its marker), the walk-disc clamp (r 20.3) for the locked ground target
  of H2 (plan Q8), the body moved by the module (plan Q1: the clips carry no horizontal root travel).

Clock: #bfPT = the clip tick (the core plays the clip at clock 0); a pattern with lead L starts at -L. Rig events are
read from the rig manifest (ev_or with the spec's tick as the fallback), fx anchors with api.h_anchor (the manifest's
clips[].anchors; the spec's body-frame point where the manifest has none).
"""
import math
import random

from . import api as A
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY

TELL = 10                                     # telegraph floor (plan.md: every damaging hit >= 10 t)
K_KICK, K_JUMP, K_DASH, K_VAC = 'kick', 'jump', 'dash', 'vacuum'
L_KICK, L_JUMP, L_DASH, L_VAC = (clip_len(c) for c in ('kick_combo', 'kick_jump', 'dash_kick', 'vacuum'))
# H1 (kick_combo): run 0, hit1 8, backflip 10, hop 22, leap 34, hit2 40
H1_HIT1, H1_HIT2 = ev_or('kick_combo', 'hit1', 8), ev_or('kick_combo', 'hit2', 40)
H1_LEAD = max(0, TELL - H1_HIT1)              # hit 1 lands 8 t into the clip: its telegraph starts 2 t before the clip
H1_LOCK2 = H1_HIT2 - 14                       # 26: kick 2 aimed and telegraphed 14 t ahead (spec Q22)
H1_LEAP = H1_HIT2 - 8                         # 32: the flying leap to the landing point B (4 t)
# H2 (kick_jump): tell 0, sweep 13 (active 4 t, knee height), jump 33, orb 45, kick 52, impact 55, land 59 (plan Q2)
H2_SWEEP = ev_or('kick_jump', 'sweep', 13)
H2_JUMP = ev_or('kick_jump', 'jump', 33)
H2_IMPACT = ev_or('kick_jump', 'impact', 55)
H2_ORB = ev_or('kick_jump', 'orb', H2_IMPACT - 10)
H2_KICK = ev_or('kick_jump', 'kick', H2_IMPACT - 3)
H2_LAND = ev_or('kick_jump', 'land', H2_IMPACT + 4)
H2_LOCK = H2_IMPACT - 12                      # the disc locked on the player 12 t before the impact
H2_ACT, H2_Y1 = 4, 1.0                        # sweep: active 4 t, feet test up to 1.0 b (jumpable, Q12)
# H3 (dash_kick): charge 0, dash 10, dash_end 12, kick 15, ring 19
H3_DASH, H3_DASH_END = ev_or('dash_kick', 'dash', 10), ev_or('dash_kick', 'dash_end', 12)
H3_KICK = ev_or('dash_kick', 'kick', 15)
H3_RING = ev_or('dash_kick', 'ring', H3_KICK + 4)
H3_LOCK = 3                                   # aim lock and both decals (kick tell 12, ring tell 16)
H3_RING_ACT = 3
# H4 (vacuum): crouch 0, tell 9 (the glint: aim lock), stomp 16, blade 17, backflip 17, land 38
H4_GLINT = ev_or('vacuum', 'tell', 9)
H4_BLADE = ev_or('vacuum', 'blade', 17)
H4_STOMP = ev_or('vacuum', 'stomp', H4_BLADE - 1)
H4_BACK = ev_or('vacuum', 'backflip', H4_BLADE)
H4_LAND = ev_or('vacuum', 'land', 38)
H4_SPD, H4_LIFE = 0.75, 60                    # 0.75 b/t (3 sub-steps of 0.25 b; FW-2), 60 t
H4_HR = 1.5                                    # blade half width (the spec's 3.0 b lane): it reaches hr + 0.3 = 1.8 b off the
                                               # line, the lane decal + the body pad (FW-1; the hr 1.2 workaround is gone)
H4_EFF = 0.75                                  # effective speed (0.25 b sub-steps, rounded up)
H4_REAR, H4_P0 = 0.3, 1.0                      # rear-up 0.3 b back (12-14); the blade spawns 1.0 b ahead of her
H4_EDGE = 20.7                                 # the blade stops at the wall ring (r 21): its lane ends there
assert H2_SWEEP - TELL >= 0 and H2_LOCK > H2_JUMP and H2_ORB < H2_KICK < H2_IMPACT <= H2_LAND < L_JUMP
assert H3_LOCK < H3_DASH < H3_KICK <= H3_RING and H3_KICK - H3_LOCK >= TELL
assert 0 < H4_GLINT < H4_STOMP < H4_BLADE <= H4_BACK < H4_LAND <= L_VAC

PATTERNS = [
    Pattern(1, K_KICK, '달빛 발차기', 'h', 'kick_combo', bands=('melee', 'mid'), weight={'melee': 2}, lead=H1_LEAD,
            recover=16, max_len=L_KICK + 5, length=L_KICK),
    Pattern(2, K_JUMP, '달빛 점프', 'h', 'kick_jump', bands=('melee', 'mid'), close=3.0, recover=16,
            max_len=L_JUMP + 5, length=L_JUMP),
    Pattern(3, K_DASH, '달빛 돌진', 'h', 'dash_kick', bands=('mid', 'far'), weight={'far': 2}, recover=16,
            max_len=L_DASH + 5, length=L_DASH),
    Pattern(4, K_VAC, '광폭한 진공', 'h', 'vacuum', bands=('far', 'mid'), weight={'far': 2}, recover=18,
            max_len=L_VAC + 5, length=L_VAC),
]

# ---------------------------------------------------------------------------------------------
# small helpers
hx = A.hexrgb
BODY = 'execute at @s rotated as @s rotated ~ 0 run '            # her feet, her yaw (the body frame)
TEAL = '#297272'                                                  # the dark teal of the crescents (v1 §5)
NAVY = '#394B75'                                                  # the crescent plates


def mk(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


def kill_mk(*tags):
    return [f'kill @e[type=minecraft:marker,tag={t}]' for t in tags]


def at_mk(sel, extra=''):
    """execute prefix: on the floor at a marker, rotated as the marker (its yaw = the locked aim)."""
    return f'execute at {sel} rotated as {sel} rotated ~ 0 {extra}positioned ~ {CY} ~ run '


def aim(sel):
    """execute prefix: at her feet, rotated as the marker (the locked aim)."""
    return f'execute at @s rotated as {sel} rotated ~ 0 run '


def pair(g, pre, hz, tele, **opts):
    """A framework hazard and the kit decal of the same shape and tell in the same tick (the decal is the telegraph:
    the framework outline off with #hzQuiet 1, its strike sound off with #hzSfx 0, Q7)."""
    return [*g.hz_opts(sfx=0, quiet=1, **opts), pre + hz, pre + tele]


def snd(g, event, v, p):
    return g.sound(event, v, p)


def back_step(d):
    """One step d b straight back along her own yaw (a backflip on the locked line), inside the safe disc."""
    return f'execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^{A.L.num(d)} if function rlk:mboss/mv/ok run tp @s ~ ~ ~'


def side_step(yaw_off, d):
    """A sideways hop step (her yaw kept), as the core's strafe."""
    return (f'execute at @s rotated as @s rotated ~{yaw_off} 0 positioned ^ ^ ^{A.L.num(d)} if function rlk:mboss/mv/ok '
            'run tp @s ~ ~ ~')


def radial(g, kind, n, pos, elev, s0, s1, dist, life, fade, col='#FFFFFF', yaw0=0.0, yaw_span=360.0, seed=1,
           roll=0, bb='fixed'):
    """n kit cards flung outward from pos (the kit's radial trick: rot '~yaw 90-elev', move (0, d, 0))."""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        yaw = yaw0 + (yaw_span * (k + 0.5) / n if yaw_span < 360 else 360.0 * k / n) + rnd.uniform(-8, 8)
        el = elev if isinstance(elev, (int, float)) else rnd.uniform(*elev)
        out.append(g.kcard(kind, pos, f'~{A.L.num(yaw, 1)} {A.L.num(90 - el, 1)}', col=col, bb=bb,
                           roll=roll or rnd.randint(-15, 15), s0=s0, s1=s1, move=(0, dist, 0), life=life, fade=fade))
    return out


def dispatch(g, key, name, score, values, target):
    """p/<key>/<name>: a binary dispatch on `score` (fake player in mb) over the sorted integer values, each running
    function p/<key>/<target(v)>. Returns the function line that calls it."""
    fn = lambda rel: f'function {A.NS}p/{key}/{rel}'           # noqa: E731

    def node(vs, rel):
        if len(vs) <= 4:
            g.pw(key, rel, [f'execute if score {score} mb matches {v} run return run {fn(target(v))}' for v in vs])
            return
        mid = len(vs) // 2
        lo, hi = vs[:mid], vs[mid:]
        g.pw(key, rel, [f'execute if score {score} mb matches {lo[0]}..{lo[-1]} run return run {fn(f"{rel}_a")}',
                        f'execute if score {score} mb matches {hi[0]}..{hi[-1]} run return run {fn(f"{rel}_b")}'])
        node(lo, f'{rel}_a')
        node(hi, f'{rel}_b')
    node(sorted(values), name)
    return fn(name)


def emit(g):
    kick(g)
    jump(g)
    dash(g)
    vacuum(g)


# =============================================================================================
# H1 달빛 발차기 (spec H1_kick_combo.md): burst-run S -> A (the clip's own run, <= 4.5 b in 5 t), hit 1 = a narrow
# vertical strip (lane 4.5 x 2.4 from 0.5 behind A + a splash disc r 1.5 1.2 ahead, one group) at 8 telegraphed from -2;
# backflip 1.2 b, settle, two sideways hops, kick 2 aimed and telegraphed at 26 (half disc r 5 + ground wave 6 x 2, one
# group), the flying leap to B at 32, the axe kick at 40; 1.0 / 1.2, at most 2 hits.
def kick(g):
    R = g.rig
    k = K_KICK
    a, b = 'rlk_mb_bf_p1a', 'rlk_mb_bf_p1b'
    A_, B_ = mk(a), mk(b)
    tl = TL(g, k)
    t0 = H1_HIT1 - TELL                                       # -2
    foot_run = A.h_anchor('kick_combo', 'run', 'foot_r', '^-0.42 ^0.5 ^0.4')
    foot_hit = A.h_anchor('kick_combo', 'hit1', 'foot_r', '^-0.28 ^3.17 ^0.17')
    core_bf = A.h_anchor('kick_combo', 'backflip', 'core', '^ ^2.6 ^-0.4')
    foot_hop = A.h_anchor('kick_combo', 'hop', 'foot_r', '^-0.5 ^0.15 ^0.2')
    foot_leap = A.h_anchor('kick_combo', 'leap', 'foot_r', '^-0.4 ^1.9 ^1.2')
    lime_pale, lime = hx('#E5FBC8'), hx('#C1F788')

    # ---- hit 1: lock A (<= 4.5 b toward the player, 1.5 b short), the strip and its splash, one group
    tl.at(t0, R('face/player'), *kill_mk(a, b), g.dest(4.5, 1.5), g.keep(a), g.GRP_NEW,
          *pair(g, at_mk(A_), g.hz_line(4.0, 2.4, TELL, DMG['h1a']), g.tele_line(4.0, 2.4, TELL, back=0.5),
                grp=True, kb=KB['default'], back=0.5),
          *pair(g, at_mk(A_, 'positioned ^ ^ ^1.2 '), g.hz_disc(1.5, TELL, DMG['h1a']), g.tele_disc(1.5, TELL),
                grp=True, kb=KB['default']),
          snd(g, 'block.amethyst_block.resonate', 0.35, 1.6))
    tl.span(t0 + 1, 5, R('face/track'))
    # the burst-run S -> A (0.6-0.9 b/t)
    tl.at(0, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:5}}',
          snd(g, 'entity.breeze.jump', 0.6, 1.3), snd(g, 'block.moss_carpet.step', 0.5, 1.0),
          snd(g, 'entity.player.attack.sweep', 0.25, 1.5),
          BODY + g.kcard('leaf', '^ ^0.3 ^-0.6', bb='center', col='#A8DF74', s0=0.3, s1=0.4, move=(0, -0.3, 0), life=10, fade=4))
    for t in (0, 2, 4):
        tl.at(t, g.particle('poof', '~ ~0.1 ~', (0.25, 0.02, 0.25), 0.02, 2))
    tl.at(2, BODY + g.kcard('glint', foot_run, bb='center', col='#E5FBC8', s0=0.2, s1=0.6, life=4, fade=2))
    tl.at(3, snd(g, 'block.moss_carpet.step', 0.4, 1.1))
    tl.at(5, aim(A_) + g.particle('wax_off', '^ ^0.1 ^0.6', (0.5, 0.05, 0.5), 0, 4),
          aim(A_) + g.dust(lime_pale, 0.8, '^ ^0.1 ^0.6', (0.5, 0.1, 0.5), 6))
    tl.at(6, f'execute at @s rotated as {A_} rotated ~ 0 positioned ^ ^0.5 ^1.0 run ' + g.fx('glint'),
          snd(g, 'block.amethyst_block.chime', 0.5, 1.9))
    tl.at(7, aim(A_) + g.kcard('burst', '^ ^0.08 ^1.2', '~ 90', s0=0.5, s1=3.0, life=5, fade=2))
    # the rising flip-kick crescent (kit kick_rise; the kit's painted crescent carries the dark teal inner band of the
    # spec's underlay), the core streak seen from the front, the jagged leaf blades at its base
    tl.at(H1_HIT1, aim(A_) + g.fx('kick_rise'),
          aim(A_) + g.kcard('streak', '^ ^2.5 ^1.0', '~ 0', col='#EDF9DA', roll=80, s0=4.0, s1=5.5, life=3, fade=1),
          *[aim(A_) + c for c in radial(g, 'blade', 6, '^ ^0.1 ^1.2', (55, 78), 0.3, 1.3, 0.25, 6, 3, yaw0=-50,
                                         yaw_span=100, seed=8)],
          aim(A_) + g.dust(hx('#D7F899'), 1.2, '^ ^2 ^1.2', (0.6, 1.4, 0.3), 14),
          aim(A_) + g.particle('wax_off', '^ ^1.5 ^1.2', (0.4, 1.0, 0.3), 0, 6),
          g.snd('kick_impact'))
    # the backflip: 1.2 b away, trail crescents breaking into leaves
    tl.span(H1_HIT1 + 1, H1_HIT1 + 8, 'function rlk:mboss/mv/away {d:0.15}', BODY + g.dust(lime, 1.0, core_bf, (0.15, 0.2, 0.15), 2))
    for t in (H1_HIT1 + 1, H1_HIT1 + 4):
        tl.at(t, BODY + g.kcard('cres_lime', '^ ^1.4 ^', '~ -90', col='#BFF191', roll=90, spin=-150, s0=1.6, s1=2.4, life=4, fade=2))
    for t, x in ((H1_HIT1 + 2, 0.3), (H1_HIT1 + 5, -0.3)):
        tl.at(t, *[BODY + g.kcard('leaf', f'^{A.L.num(x + dx)} ^2.1 ^-0.2', bb='center', col='#A8DF74', s0=0.3, s1=0.4,
                                  move=(0, -1.2, 0.4), life=12, fade=6) for dx in (0, 0.25)])
    tl.at(H1_HIT1 + 3, snd(g, 'item.trident.riptide_1', 0.3, 1.6))
    land1 = H1_HIT1 + 8                                       # 16: lands
    tl.at(land1, BODY + g.fx('land'), g.particle('poof', '~ ~0.1 ~', (0.4, 0.05, 0.4), 0.02, 6),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.5, 0.05, 0.5), 0, 8),
          snd(g, 'block.moss.fall', 0.6, 1.0))
    tl.at(land1 + 2, snd(g, 'block.moss.fall', 0.35, 1.2))
    # wind-up: the kicking foot glows; two sideways hops of 0.75 b (a random side, then the other)
    tl.at(H1_LEAP - 12, 'execute store result score #bp1S mb run random value 0..1')
    for t in range(H1_LEAP - 12, H1_LEAP, 2):
        tl.at(t, BODY + g.dust(lime_pale, 0.7, foot_hop, (0.1, 0.1, 0.1), 2))
    for t0h, first in ((H1_LEAP - 10, True), (H1_LEAP - 4, False)):
        s0 = 0 if first else 1
        for t in range(t0h, t0h + 3):
            tl.at(t, f'execute if score #bp1S mb matches {s0} run ' + side_step(90, 0.25),
                  f'execute unless score #bp1S mb matches {s0} run ' + side_step(-90, 0.25))
        tl.at(t0h, g.particle('poof', '~ ~0.1 ~', (0.3, 0.02, 0.3), 0.02, 3), snd(g, 'block.moss_carpet.step', 0.5, 1.2))
    # ---- hit 2: aim at the player and lock B (the leap's landing point, <= 3.5 b, 1.2 b short), 14 t of decals
    tl.at(H1_LOCK2, R('face/player'), *kill_mk(b), g.dest(3.5, 1.2), g.keep(b), g.GRP_NEW,
          *pair(g, at_mk(B_), g.hz_sector(5.0, 90, H1_HIT2 - H1_LOCK2, DMG['h1b']),
                g.tele_sector(5.0, 90, H1_HIT2 - H1_LOCK2), grp=True, kb=KB['default']),
          *pair(g, at_mk(B_), g.hz_line(6.0, 2.0, H1_HIT2 - H1_LOCK2, DMG['h1b']),
                g.tele_line(6.0, 2.0, H1_HIT2 - H1_LOCK2), grp=True, kb=KB['default']),
          snd(g, 'block.amethyst_block.resonate', 0.35, 1.5))
    tl.at(H1_LEAP, f'execute positioned as {B_} run function rlk:mboss/mv/glide {{t:4}}',
          BODY + g.kcard('streak', '^ ^1.0 ^-1', '~90 0', col='#D7F899', s0=3.0, s1=3.5, life=4, fade=2),
          snd(g, 'entity.breeze.jump', 0.6, 1.1))
    tl.at(H1_LEAP + 2, BODY + g.kcard('streak', '^ ^1.2 ^', '~90 0', col='#EDF9DA', s0=2.0, s1=3.0, life=3, fade=1))
    tl.at(H1_HIT2 - 4, BODY + g.kcard('ripple', foot_leap, bb='center', col='#D7F899', spin=160, s0=0.4, s1=1.4, life=6, fade=2),
          snd(g, 'block.amethyst_block.resonate', 0.5, 1.6))
    tl.at(H1_HIT2 - 2, f'execute at @s rotated as @s rotated ~ 0 positioned {foot_leap} run ' + g.fx('glint'))
    # the axe kick (kit kick_axe, two crescent layers) and the ground wave (kit ground_wave: blades along 6 b)
    tl.at(H1_HIT2, aim(B_) + g.fx('kick_axe'),
          aim(B_) + g.kcard('burst', '^ ^0.08 ^2.0', '~ 90', s0=1.0, s1=4.0, life=5, fade=2),
          aim(B_) + g.particle('flash{color:[0.93,0.98,0.85,0.9]}', '^ ^0.5 ^2.0', (0, 0, 0), 0, 1),
          at_mk(B_) + g.fx('ground_wave'),
          g.snd('kick_impact'), snd(g, 'block.big_dripleaf.break', 0.6, 1.0))
    for i in range(3):
        lines = []
        for kk in (2 * i + 1, 2 * i + 2):
            lines += [at_mk(B_) + g.dust(hx(TEAL), 1.4, f'^ ^0.2 ^{kk}', (0.3, 0.1, 0.3), 3),
                      at_mk(B_) + g.dust_fade(hx('#E5FBC8'), hx(TEAL), 1.2, f'^ ^0.3 ^{kk}', (0.3, 0.2, 0.3), 4)]
        tl.at(H1_HIT2 + i, *lines)
    tl.at(H1_HIT2 + 1, at_mk(B_, 'positioned ^ ^ ^3 ') + g.snd('crescent_fly'), snd(g, 'block.azalea.break', 0.5, 1.0))
    tl.at(H1_HIT2 + 2, snd(g, 'block.azalea.break', 0.5, 1.1),
          at_mk(B_) + g.dust(hx('#B7D8AF'), 1.0, '^ ^0.2 ^3', (0.3, 0.1, 2.5), 8))
    for t in (H1_HIT2 + 3, H1_HIT2 + 6):
        tl.at(t, *[at_mk(B_) + g.kcard('leaf', f'^{A.L.num(x)} ^2.2 ^{A.L.num(z)}', bb='center', col='#A8DF74',
                                       s0=0.3, s1=0.4, move=(0, -1.5, 0.6), life=14, fade=6)
                   for x, z in ((0.4, 1.0), (-0.3, 2.2), (0.2, 3.4), (-0.5, 4.6))])
    tl.at(H1_HIT2 + 4, at_mk(B_) + g.dust(hx('#AEE08B'), 1.2, '^ ^0.2 ^3', (0.3, 0.1, 2.5), 6),
          at_mk(B_) + g.dust(hx('#B7D8AF'), 1.0, '^ ^0.2 ^3', (0.3, 0.1, 2.5), 8),
          BODY + g.fx('land'), g.snd('land'), snd(g, 'block.moss.fall', 0.6, 0.9),
          g.particle('poof', '~ ~0.1 ~', (0.4, 0.05, 0.4), 0.02, 6),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.5, 0.05, 0.5), 0, 8))
    tl.at(L_KICK, *kill_mk(a, b), g.end())
    tl.write([f'# H1 달빛 발차기 (lead {H1_LEAD}: start at clock {t0}, clip kick_combo at 0). Hit 1 {H1_HIT1}: the strip (lane',
              f'# 4.5 x 2.4 from 0.5 behind A + splash r 1.5, one group, decals from {t0}); kick 2 locked at {H1_LOCK2}, the leap',
              f'# at {H1_LEAP}, hit 2 {H1_HIT2}: half disc r 5 + ground wave 6 x 2 at B (one group); 1.0 / 1.2 Dendro.'],
             ['# H1 tick.'], t0=t0)
    g.pw(k, 'cancel', ['# Markers A / B; the kit decals (only this pattern has any while it runs).',
                       f'kill @e[type=minecraft:marker,tag={a}]', f'kill @e[type=minecraft:marker,tag={b}]',
                       f'function {A.K.FN}tele/clear'])


# =============================================================================================
# H2 달빛 점프 (spec H2_kick_jump.md): after the core's close-in to 3 b, the arm-shard / chain tell (0-13), the 360 low
# sweep r 3 at knee height (active 13-16, jumpable) telegraphed from 3, the spiral jump at 33 (glide to A, 0.8 b short of
# the player), the disc locked under the player 12 t before the impact (clamped to the walk disc), the orb at her foot,
# the star flash, the kick, the falling disc and the impact r 2.5 (heavy knockback); 0.9 / 1.4, two separate hits.
def jump(g):
    R = g.rig
    k = K_JUMP
    a, b = 'rlk_mb_bf_p2a', 'rlk_mb_bf_p2b'
    A_, L_ = mk(a), mk(b)
    tl = TL(g, k)
    hand = A.h_anchor('kick_jump', 'tell', 'hand_l_a', '^0.62 ^2.6 ^0.1')
    orb = A.h_anchor('kick_jump', 'orb', 'foot_r', '^-0.36 ^2.77 ^0.3')
    orb_k = A.h_anchor('kick_jump', 'kick', 'foot_r', '^-0.4 ^4.43 ^0.97')
    tl.at(0, R('face/player'), f'execute at @s rotated as @s rotated ~ 0 positioned {hand} run ' + g.fx('shard_tell'),
          g.snd('shard_tell'))
    tl.span(1, 10, R('face/track'))
    for t in range(0, H2_SWEEP, 2):
        tl.at(t, BODY + g.dust(hx('#B8F060'), 0.9, hand, (0.1, 0.25, 0.1), 3))
    for t in range(0, H2_SWEEP, 4):
        tl.at(t, BODY + g.particle('end_rod', hand, (0.1, 0.2, 0.1), 0.01, 1))
    # the sweep: a disc r 3 around her floor point, feet test -0.5..1.0 b, active 4 t
    tl.at(H2_SWEEP - TELL, *pair(g, f'execute positioned ~ {CY} ~ run ', g.hz_disc(3.0, TELL, DMG['h2a']), g.tele_disc(3.0, TELL),
                                 act=H2_ACT, y1=H2_Y1, kb=KB['default']),
          snd(g, 'block.amethyst_block.resonate', 0.35, 1.6))
    tl.at(H2_SWEEP - 8, snd(g, 'block.amethyst_block.chime', 0.5, 1.8))
    for t in (H2_SWEEP - 4, H2_SWEEP - 2):                   # "low": a knee-high ring outline
        tl.at(t, *g.h_ring_dust(hx('#D6FAC5'), 3.0, 18, y=0.5, scale=0.8))
    tl.at(H2_SWEEP - 3, BODY + g.kcard('streak', '^ ^0.1 ^0.3', '~ 90', col='#B8F060', s0=1.2, s1=1.6, life=3, fade=1),
          snd(g, 'block.amethyst_block.resonate', 0.4, 1.6))
    tl.at(H2_SWEEP, BODY + g.fx('sweep'), g.snd('sweep'), snd(g, 'entity.breeze.whirl', 0.6, 1.4))
    tl.at(H2_SWEEP + 1, *g.h_ring_dust(hx('#B9E4A7'), 2.8, 16, y=0.4, scale=1.0))
    tl.at(H2_SWEEP + 2, BODY + g.kcard('cres_lime', '^ ^0.5 ^', '~90 0', col='#D6FAC5', spin=170, s0=5.0, s1=6.0, life=4, fade=2),
          BODY + g.kcard('cres_lime', '^ ^0.52 ^', '~270 0', col='#D6FAC5', spin=170, s0=5.0, s1=6.0, life=4, fade=2))
    tl.at(H2_SWEEP + 4, *[BODY + c for c in radial(g, 'leaf', 6, '^ ^0.4 ^', 10, 0.3, 0.4, 2.0, 12, 6, col='#A8DF74', seed=17,
                                                    bb='fixed')],
          snd(g, 'block.moss.fall', 0.7, 0.8))
    tl.at(H2_SWEEP + 5, snd(g, 'entity.player.attack.sweep', 0.4, 1.4))
    tl.at(H2_SWEEP + 7, BODY + g.kcard('cres_lime', '^ ^0.05 ^0.6', '~ 0', col='#B9E4A7', s0=1.0, s1=1.3, life=20, fade=8))
    # the spiral jump toward the player (A, 3.5 b at most, 0.8 b short), facing re-locked, tracking until the disc lock
    tl.at(H2_JUMP - 2, R('face/player'))
    tl.span(H2_JUMP - 1, H2_LOCK, R('face/track'))
    tl.at(H2_JUMP, R('face/player'), *kill_mk(a), g.dest(3.5, 0.8), g.keep(a),
          f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:{H2_LAND - H2_JUMP}}}',
          BODY + g.fx('spiral_jump'), g.snd('spiral_jump'), snd(g, 'entity.breeze.whirl', 0.5, 1.0))
    for i in range(9):                                       # helix dust on a rising r 1.4 helix
        ang = math.radians(50 * i)
        y = 0.3 + 0.35 * i
        lines = []
        for off in (0, math.pi):
            x, z = 1.4 * math.sin(ang + off), 1.4 * math.cos(ang + off)
            lines.append(g.dust(hx('#AADB84'), 1.0, f'~{A.L.num(x, 2)} ~{A.L.num(y, 2)} ~{A.L.num(z, 2)}', (0, 0, 0), 1))
        tl.at(H2_JUMP + i, *lines)
    tl.at(H2_JUMP + 3, snd(g, 'item.elytra.flying', 0.2, 1.4))
    tl.at(H2_JUMP + 4, BODY + g.kcard('ripple', '^ ^2.4 ^', bb='center', col='#AADB84', spin=170, s0=1.5, s1=3.0, life=8, fade=3))
    tl.at(H2_JUMP + 5, snd(g, 'entity.breeze.idle_air', 0.4, 0.8))
    # the disc: locked under the player (walk disc), r 2.5, tell 12, heavy knockback; a target mark 3 b over it
    tl.at(H2_LOCK, *g.h_lock_walk(b),
          *pair(g, at_mk(L_), g.hz_disc(2.5, H2_IMPACT - H2_LOCK, DMG['h2b']), g.tele_disc(2.5, H2_IMPACT - H2_LOCK),
                kb=KB['heavy']),
          f'execute at {L_} run ' + g.kcard('glint', '~ ~3 ~', bb='center', col='#E5FBC8', s0=0.3, s1=0.8,
                                            life=H2_IMPACT - H2_LOCK, fade=3),
          f'execute at {L_} run ' + snd(g, 'block.amethyst_cluster.hit', 0.45, 1.8))
    # the orb at her raised foot, its trail, the star flash, the kick and the falling disc
    tl.at(H2_ORB, BODY + g.kcard('sphere', orb, bb='center', s0=0.6, s1=1.3, life=8, fade=2),
          BODY + g.kcard('ripple', orb, bb='center', col='#D4F8C6', spin=120, s0=1.2, s1=1.8, life=8, fade=2),
          snd(g, 'block.conduit.activate', 0.4, 1.8))
    for t in range(H2_ORB + 2, H2_KICK - 1):
        tl.at(t, BODY + g.dust(hx('#D4F8C6'), 1.0, orb, (0.15, 0.15, 0.15), 3))
    tl.at(H2_ORB + 3, snd(g, 'item.trident.riptide_1', 0.25, 1.6))
    tl.at(H2_KICK - 1, f'execute at @s rotated as @s rotated ~ 0 positioned {orb_k} run ' + g.fx('orb_star'))
    tl.at(H2_KICK, f'execute at @s rotated as @s rotated ~ 0 positioned {orb_k} run ' + g.fx('orb_kick'),
          g.snd('disc_kick'), at_mk(L_) + g.fx('disc_fall', h=2.7))
    tl.at(H2_IMPACT, at_mk(L_) + g.fx('disc_impact'),
          at_mk(L_) + g.kcard('glow', '~ ~0.06 ~', '~ 90', col='#C2ECB0', s0=4.0, s1=5.0, life=6, fade=3),
          at_mk(L_) + g.particle('flash{color:[0.76,0.93,0.69,0.8]}', '~ ~0.6 ~', (0, 0, 0), 0, 1),
          at_mk(L_) + g.dust(hx('#84C75D'), 1.6, '~ ~0.2 ~', (1.2, 0.2, 1.2), 20),
          *[at_mk(L_) + c for c in radial(g, 'leaf', 6, '~ ~0.5 ~', (15, 40), 0.3, 0.4, 2.2, 14, 6, col='#A8DF74', seed=55)],
          at_mk(L_) + g.snd('disc_impact'))
    for t in range(H2_IMPACT + 1, H2_IMPACT + 8, 2):
        tl.at(t, at_mk(L_) + g.dust(hx('#A8DF74'), 3.0, '~ ~1 ~', (1.2, 0.8, 1.2), 4),
              at_mk(L_) + g.dust(hx('#8DC07E'), 3.5, '~ ~1 ~', (1.2, 0.8, 1.2), 3))
    tl.at(H2_IMPACT + 2, at_mk(L_) + snd(g, 'block.azalea_leaves.break', 0.4, 1.2))
    tl.at(H2_LAND, BODY + g.fx('land'), g.snd('land'), snd(g, 'block.moss.fall', 0.6, 1.0),
          g.particle('poof', '~ ~0.1 ~', (0.4, 0.05, 0.4), 0.02, 6),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.5, 0.05, 0.5), 0, 8))
    tl.at(L_JUMP, *kill_mk(a, b), g.end())
    tl.write([f'# H2 달빛 점프 (clip kick_jump; after the core\'s close-in to 3 b). Sweep r 3 decal {H2_SWEEP - TELL} -> {H2_SWEEP}',
              f'# (active {H2_ACT} t, y <= {H2_Y1} b: jumpable), the jump {H2_JUMP} -> {H2_LAND}, the disc r 2.5 locked under the',
              f'# player (walk disc) at {H2_LOCK} -> impact {H2_IMPACT} (orb {H2_ORB}, kick {H2_KICK}); 0.9 / 1.4 Dendro, 2 hits.'],
             ['# H2 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]', f'kill @e[type=minecraft:marker,tag={b}]',
                       f'function {A.K.FN}tele/clear'])


# =============================================================================================
# H3 달빛 돌진 (spec H3_dash_kick.md): the mote charge (0-9), the aim locked at 3 (D <= 7 b toward the player, 1.5 b
# short; the kick disc r 1.5 1.2 b past D, tell 12, and the ring r 3.5 around D, tell 16, active 3: one group = one 1.3
# hit; the dash lane S -> D, telegraph only), the dash in 2 t, the kick at 15, the all-around ring at 19.
LANES3 = [x / 2 for x in range(2, 15)]          # dash lane lengths 1.0 .. 7.0 b (0.5 b buckets)


def dash(g):
    R = g.rig
    k = K_DASH
    a = 'rlk_mb_bf_p3a'
    D_ = mk(a)
    tl = TL(g, k)
    foot = A.h_anchor('dash_kick', 'dash_end', 'foot_r', '^-0.4 ^1.1 ^1.1')
    tl.at(0, R('face/player'), BODY + g.fx('dash_charge'), g.snd('dash_charge'))
    tl.span(1, H3_LOCK - 1, R('face/track'))
    for t in range(0, H3_DASH):
        tl.at(t, g.dust(hx('#C7DB75'), 0.6, '~ ~1.0 ~', (0.9, 0.9, 0.9), 3), g.particle('end_rod', '~ ~1.0 ~', (0.8, 0.6, 0.8), 0.02, 1))
    for t in range(5, H3_DASH):                              # the motes converge (r 1.6 -> 1.0)
        tl.at(t, *g.h_ring_dust(hx('#E6F6F8'), 1.6 - 0.15 * (t - 5), 6, y=1.2, scale=0.5))
    for t, p in ((2, 1.6), (4, 1.7), (6, 1.8), (8, 1.9)):
        tl.at(t, snd(g, 'block.amethyst_block.chime', 0.3, p))
    # the lock: D, the kick + ring group, the dash lane (dmg 0) with its length bucketed from |SD|
    lane = dispatch(g, k, 'lane', '#bp3D', range(len(LANES3)), lambda i: f'ln/{i}')
    tl.at(H3_LOCK, R('face/player'), *kill_mk(a), g.dest(7.0, 1.5), g.keep(a), g.GRP_NEW,
          *pair(g, at_mk(D_, 'positioned ^ ^ ^1.2 '), g.hz_disc(1.5, H3_KICK - H3_LOCK, DMG['h3']),
                g.tele_disc(1.5, H3_KICK - H3_LOCK), grp=True, kb=KB['default']),
          *pair(g, at_mk(D_), g.hz_disc(3.5, H3_RING - H3_LOCK, DMG['h3']), g.tele_disc(3.5, H3_RING - H3_LOCK),
                grp=True, kb=KB['default'], act=H3_RING_ACT),
          f'function {A.NS}p/{k}/dist', lane,
          snd(g, 'block.amethyst_block.resonate', 0.35, 1.6))
    # |SD| in tenths, squared -> the bucket index #bp3D (0 = 1.0 b, ..., 12 = 7.0 b; -1 = too short for a lane)
    dist = ['# @s = body: #bp3D = the lane bucket of |S D| (0.5 b steps from 1.0 b; -1 below 0.75 b).',
            f'execute store result score #bp3X mb run data get entity {D_} Pos[0] 10',
            'execute store result score #t mb run data get entity @s Pos[0] 10',
            'scoreboard players operation #bp3X mb -= #t mb',
            f'execute store result score #bp3Z mb run data get entity {D_} Pos[2] 10',
            'execute store result score #t mb run data get entity @s Pos[2] 10',
            'scoreboard players operation #bp3Z mb -= #t mb',
            'scoreboard players operation #bp3X mb *= #bp3X mb', 'scoreboard players operation #bp3Z mb *= #bp3Z mb',
            'scoreboard players operation #bp3X mb += #bp3Z mb', 'scoreboard players set #bp3D mb -1']
    for i, L in enumerate(LANES3):
        lo = math.ceil((10 * L - 2.5) ** 2)
        hi = '' if i == len(LANES3) - 1 else str(math.ceil((10 * L + 2.5) ** 2) - 1)
        dist.append(f'execute if score #bp3X mb matches {lo}..{hi} run scoreboard players set #bp3D mb {i}')
    g.pw(k, 'dist', dist)
    for i, L in enumerate(LANES3):
        pre = f'execute at @s facing entity {D_} feet rotated ~ 0 positioned ~ {CY} ~ run '
        g.pw(k, f'ln/{i}', [f'# The dash lane, {L} b from her toward D (telegraph only: dmg 0), 0.8 b wide, until the dash.']
             + pair(g, pre, g.tell_line(L, 0.8, H3_DASH - H3_LOCK), g.tele_line(L, 0.8, H3_DASH - H3_LOCK)))
    tl.at(5, snd(g, 'block.azalea_leaves.break', 0.3, 1.7))
    tl.at(H3_DASH - 2, BODY + g.kcard('glint', foot, bb='center', col='#F0FEF6', s0=0.3, s1=1.0, life=4, fade=2))
    # the dash: S -> D in 2 t, a speed streak along the path, the afterimage at the start
    tl.at(H3_DASH, f'execute positioned as {D_} run function rlk:mboss/mv/glide {{t:{H3_DASH_END - H3_DASH}}}',
          f'execute at @s facing entity {D_} feet rotated ~ 0 run ' + g.fx('dash_streak'),
          BODY + g.kcard('glow', '^ ^1.2 ^', bb='center', col='#B2FBDD', s0=1.2, s1=0.4, life=4, fade=2),
          g.snd('dash'))
    tl.at(H3_KICK - 1, aim(D_) + g.kcard('streak', '^ ^1.6 ^1.0', '~ 0', col='#F0FEF6', roll=35, s0=3.0, s1=4.0, life=3, fade=1),
          snd(g, 'entity.player.attack.sweep', 0.5, 1.2))
    tl.at(H3_KICK, aim(D_) + g.kcard('burst', '^ ^1.4 ^1.2', bb='center', s0=1.0, s1=4.0, life=4, fade=2),
          aim(D_) + g.kcard('glow', '^ ^1.4 ^1.2', bb='center', col='#F9FDE0', s0=1.5, s1=3.5, life=4, fade=2),
          aim(D_) + g.particle('flash{color:[0.98,0.99,0.88,0.9]}', '^ ^1.4 ^1.2', (0, 0, 0), 0, 1),
          g.snd('dash_kick'), snd(g, 'entity.player.attack.strong', 0.5, 1.2))
    tl.at(H3_KICK + 1, *[aim(D_) + c for c in radial(g, 'shard', 6, '^ ^1.4 ^1.2', (-20, 20), 0.6, 1.5, 1.4, 5, 2,
                                                      col='#EAFDB2', seed=16)])
    tl.at(H3_KICK + 2, snd(g, 'block.cherry_leaves.break', 0.7, 1.0))
    tl.at(H3_RING - 1, snd(g, 'entity.player.attack.sweep', 0.8, 0.7))
    # the all-around ring slash r 3.5 (kit kick_burst: crescent ring, flung blades, floor ripple) + its rim and dust
    tl.at(H3_RING, at_mk(D_) + g.fx('kick_burst'),
          at_mk(D_) + g.kcard('ripple', '^ ^1.0 ^', '~ 90', col='#E1F0A0', s0=6.0, s1=8.1, life=5, fade=2),
          *[f'execute at {D_} run ' + x for x in g.h_ring_dust(hx('#D3FAB9'), 3.3, 24, y=1.0, scale=1.2)],
          snd(g, 'block.cherry_leaves.break', 0.7, 1.1), snd(g, 'block.azalea.break', 0.6, 1.0))
    tl.at(H3_RING + 1, at_mk(D_) + g.kcard('cres_lime', '^ ^1.05 ^', '~90 0', col='#B6F392', spin=170, s0=6.4, s1=7.0, life=4, fade=2),
          at_mk(D_) + g.kcard('cres_lime', '^ ^1.05 ^', '~270 0', col='#B6F392', spin=170, s0=6.4, s1=7.0, life=4, fade=2))
    tl.at(H3_RING + 2, snd(g, 'block.cherry_leaves.break', 0.5, 1.2))
    for t in range(H3_RING + 3, H3_RING + 8, 2):
        tl.at(t, g.dust(hx('#B6F392'), 0.9, '~ ~1.0 ~', (1.5, 0.3, 1.5), 3), g.particle('end_rod', '~ ~1.0 ~', (1.2, 0.3, 1.2), 0.03, 1))
    tl.at(H3_RING + 4, *[BODY + g.kcard('leaf', f'^{x} ^1.6 ^{z}', bb='center', col='#A9ED97', s0=0.3, s1=0.4,
                                         move=(0, -1.0, 0.3), life=12, fade=5) for x, z in ((0.8, 0.4), (-0.6, -0.5), (0.2, -1.0))])
    tl.span(H3_RING + 7, L_DASH - 1, R('face/track'))
    tl.at(L_DASH, *kill_mk(a), g.end())
    tl.write([f'# H3 달빛 돌진 (clip dash_kick). Lock D at {H3_LOCK}: kick r 1.5 1.2 b past D (tell {H3_KICK - H3_LOCK}) + ring r 3.5',
              f'# around D (tell {H3_RING - H3_LOCK}, act {H3_RING_ACT}), one group = one 1.3 hit; the dash {H3_DASH}-{H3_DASH_END}, kick {H3_KICK}, ring {H3_RING}.'],
             ['# H3 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]', f'function {A.K.FN}tele/clear'])


# =============================================================================================
# H4 광폭한 진공 (spec H4_vacuum.md): crouch (0-8, tracking), the glint at 9 locks the yaw and lays the lane decal 3 b
# wide from her to the wall, the rear-up, the stomp at 16, the vertical crescent blade (the kit's vblade look, 3 wide x 4
# tall) launched at 17 along the locked line at 0.75 b/t (blade hit shape, hr 1.2, no homing, 60 t, stopped by the
# wall, one hit and it flies on), the backflip 2.5 b straight back, the landing at 38; 1.2 Dendro.
H4_TAG, H4_SEL = 'rlk_mb_bf_p4b', '@e[type=minecraft:item_display,tag=rlk_mb_bf_p4b]'
LANES4 = list(range(2, 41))                    # lane lengths 2..40 b (floor of the distance to the wall)


def h4_lane_tell(L):
    """Ticks from the glint until the blade's front reaches L b (its 0.65 b hit sphere touches ~0.6 b earlier)."""
    t = H4_BLADE - 1 + (L - (H4_P0 - H4_REAR)) / H4_EFF
    return max(TELL, math.ceil(t - 1e-9) - H4_GLINT)


def vacuum(g):
    R = g.rig
    k = K_VAC
    tl = TL(g, k)
    foot0 = A.h_anchor('vacuum', 'crouch', 'foot_r', '^-0.42 ^0.15 ^0.06')
    foot_t = A.h_anchor('vacuum', 'tell', 'foot_r', '^-0.3 ^0.21 ^0.12')
    core_b = A.h_anchor('vacuum', 'backflip', 'core', '^ ^2.4 ^0.46')
    tl.at(0, R('face/player'), f'execute at @s rotated as @s rotated ~ 0 positioned {foot0} run ' + g.fx('vac_crouch'),
          snd(g, 'block.moss_carpet.step', 0.4, 0.9))
    tl.span(1, H4_GLINT - 1, R('face/track'))
    for t in range(0, H4_GLINT, 2):
        tl.at(t, BODY + g.dust(hx('#E2FC88'), 0.8, foot0, (0.1, 0.15, 0.1), 2),
              BODY + g.dust(hx('#C9F2AD'), 0.6, foot0, (0.1, 0.3, 0.1), 1, 0.01))
    # the glint: the yaw is locked (face/player once, no tracking after), the lane to the wall
    edge = edge_search(g, k)
    lane = dispatch(g, k, 'lane', '#bp4L', LANES4, lambda L: f'ln/{L}')
    for L in LANES4:
        tell = h4_lane_tell(L)
        pre = f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run '
        g.pw(k, f'ln/{L}', [f'# The blade\'s lane, {L} b from her to the wall along the locked yaw, 3 b wide: the fill reaches the',
                            f'# far end as the blade does ({tell} t after the glint; telegraph only).']
             + pair(g, pre, g.tell_line(L, 3.0, tell), g.tele_line(L, 3.0, tell)))
    tl.at(H4_GLINT, R('face/player'), edge, lane,
          f'execute at @s rotated as @s rotated ~ 0 positioned {foot_t} run ' + g.fx('vac_glint'), g.snd('vacuum_glint'))
    # rear-up 0.3 b back on the line, the stomp
    tl.span(H4_GLINT + 3, H4_GLINT + 5, back_step(0.1))
    tl.at(H4_GLINT + 3, g.particle('poof', '~ ~0.1 ~', (0.25, 0.02, 0.25), 0.02, 2))
    tl.at(H4_GLINT + 4, snd(g, 'entity.breeze.jump', 0.4, 1.0))
    tl.at(H4_STOMP, f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.0 positioned ~ {CY} ~ run ' + g.fx('vac_stomp'),
          BODY + g.kcard('flame_tongue', '^ ^ ^1.0', bb='vertical', s0=0.4, s1=1.2, life=4, fade=2),
          BODY + g.particle('block{block_state:"minecraft:mossy_cobblestone"}', '^ ^0.2 ^1.0', (0.4, 0.2, 0.4), 0.2, 8))
    # (no stomp sound layers here: snd/vacuum_blade one tick later is the stomp + blade rise; review fix FX-4)
    # the blade: an item_display 0.9 b over the floor 1 b ahead, the kit's lime crescent, rising from its lower tip
    # (scale 0.3 -> 1 over 3 t about the tip 0.9 b under the prop), launched along the locked yaw at pitch 0
    s = 0.3
    t0 = (-1.9 * s, -0.9 + s * (1.02 + 0.9), 0.0)
    small = (f'{{translation:[{A.L.num(t0[0], 3)}f,{A.L.num(t0[1], 3)}f,0f],left_rotation:[0.5f,0.5f,0.5f,0.5f],'
             f'scale:[{A.L.num(4.4 * s, 3)}f,{A.L.num(1.0 * s, 3)}f,{A.L.num(6.8 * s, 3)}f],right_rotation:[0f,0f,0f,1f]}}')
    new = '@e[type=minecraft:item_display,tag=rlk_mb_bf_p4n,limit=1]'
    tl.at(H4_BLADE,
          f'execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^{A.L.num(H4_P0)} run summon minecraft:item_display ~ ~ ~ '
          f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p4","{H4_TAG}","rlk_mb_bf_p4n","rlk_mb_bf_p4g"],teleport_duration:1,'
          f'interpolation_duration:3,billboard:"fixed",view_range:1.5f,shadow_radius:0f,brightness:{{block:15,sky:15}},'
          f'item:{{id:"minecraft:paper",count:1}},transformation:{small}}}',
          f'execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^{A.L.num(H4_P0)} run tp {new} ~ ~ ~ ~ 0',
          f'execute as {new} run ' + g.kit.look('cres_lime'),
          f'scoreboard players set {new} mbId 4',
          *g.pj_opts(shape=1, kb=KB['default'], wall=1),
          f'execute as {new} at @s run ' + g.pj_launch(H4_SPD, H4_LIFE, DMG['h4'], H4_HR),
          'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p4n] remove rlk_mb_bf_p4n',
          'scoreboard players set #bp4B mb 1',
          g.snd('vacuum_blade'), snd(g, 'block.azalea_leaves.break', 0.6, 0.9))
    tl.at(H4_BLADE + 1, 'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4g] run data merge entity @s {start_interpolation:0}',
          'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4g] run ' + g.kprop('vblade'),
          'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p4g] remove rlk_mb_bf_p4g')
    # the backflip: 2.5 b straight back along the locked line, airborne to the landing
    tl.span(H4_BACK + 1, H4_BACK + 17, back_step(0.15))
    for t in range(H4_BACK, H4_BACK + 18, 2):
        tl.at(t, BODY + g.dust(hx('#C9F2AD'), 0.7, core_b, (0.15, 0.15, 0.15), 1))
    tl.at(H4_BACK + 3, snd(g, 'item.trident.riptide_1', 0.3, 1.6))
    tl.at(H4_LAND, BODY + g.fx('land'), g.snd('land'), snd(g, 'block.moss.fall', 0.5, 1.0),
          g.particle('poof', '~ ~0.1 ~', (0.4, 0.05, 0.4), 0.02, 6),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.5, 0.05, 0.5), 0, 8))
    tl.at(L_VAC, g.end())
    tl.write([f'# H4 광폭한 진공 (clip vacuum). The glint {H4_GLINT}: the yaw locked, the lane decal to the wall; the stomp {H4_STOMP};',
              f'# the blade at {H4_BLADE} (pj blade hr {H4_HR}, {H4_SPD} b/t -> {H4_EFF}, {H4_LIFE} t, no homing; it outlives the',
              f'# pattern: p/{k}/blades from the core ai/state); the backflip {H4_BACK + 1}-{H4_BACK + 17}, the landing {H4_LAND}; 1.2 Dendro.'],
             ['# H4 tick.'])
    g.pw(k, 'cancel', ['# The blade (and any helper of this pattern) and the kit decals.',
                       'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_p4]', 'scoreboard players set #bp4B mb 0',
                       f'function {A.K.FN}tele/clear'])
    # the blade's own tick (from the core's ai/state while #bp4B >= 1; it lives on after the pattern's end)
    g.pw(k, 'blades', ['# Core hook (ai/state, while #bp4B >= 1): every flying vacuum blade, then their count.',
                       'scoreboard players set #bp4B mb 0',
                       f'execute as {H4_SEL} at @s run function {A.NS}p/{k}/blade'])
    g.pw(k, 'blade', [
        '# @s = a blade prop, at and rotated as it (0.9 b over the floor), before the framework moves it this tick',
        f'# (core ai/state, so its age mbPjT = pattern clock - {H4_BLADE}: the trail from {H4_BLADE + 1}, every 2 t).',
        'scoreboard players add #bp4B mb 1',
        g.dust(hx('#64BC56'), 1.4, '^ ^-0.85 ^', (1.3, 0.2, 0.1), 3),
        g.dust_fade(hx('#F6FDE0'), hx('#64BC56'), 1.0, '^ ^2.9 ^', (1.0, 0.2, 0.1), 2),
        'scoreboard players operation #bfM mb = @s mbPjT', 'scoreboard players operation #bfM mb %= #bfK2 mb',
        f'execute if score #bfM mb matches 1 positioned ^ ^-0.9 ^ run ' + g.fx('vac_trail'),
        'scoreboard players operation #bfM mb = @s mbPjT', 'scoreboard players operation #bfM mb %= #bfK4 mb',
        f'execute if score #bfM mb matches 1 run function {A.NS}p/{k}/debris',
        'execute if score @s mbPjT matches 6 run ' + snd(g, 'entity.breeze.idle_air', 0.4, 1.0),
        f'execute unless entity @s[tag=rlk_mb_bf_p4s] if entity @e[tag=rlk_body,distance=..4,limit=1] run function {A.NS}p/{k}/pass'])
    g.pw(k, 'debris', ['# Every 4 t: rock debris and two lime leaves thrown up and forward, the grass rustle.',
                       g.particle('block{block_state:"minecraft:mossy_cobblestone"}', '^ ^-0.8 ^', (0.6, 0.1, 0.2), 0.15, 2),
                       g.kcard('leaf', '^0.6 ^-0.5 ^', bb='center', col='#A9E97D', s0=0.3, s1=0.4, move=(0, 1.2, 1.5), life=10, fade=5),
                       g.kcard('leaf', '^-0.6 ^-0.5 ^', bb='center', col='#A9E97D', s0=0.3, s1=0.4, move=(0, 1.2, 1.5), life=10, fade=5),
                       snd(g, 'block.grass.break', 0.5, 1.0)])
    g.pw(k, 'pass', ['# The blade rushes past the player (once per blade): the hiss and low thump at the blade.',
                     'tag @s add rlk_mb_bf_p4s', g.snd('vacuum_pass')])
    g.pw(k, 'pj_end', [
        '# @s = the blade (#pjEv 1 wall, 2 life over, 4 hit the player). A hit: a spark at the player, the blade flies on',
        '# harmlessly (#pjKeep 1, the framework default). The wall or the end of its life: it shatters.',
        f'execute if score #pjEv mb matches 4 run return run function {A.NS}p/{k}/hit',
        g.kcard('burst', '~ ~1.1 ~', bb='center', s0=1.0, s1=3.0, life=4, fade=2),
        *[f'execute rotated as @s rotated ~ 0 run ' + c for c in radial(g, 'shard', 5, '~ ~1.1 ~', (10, 50), 0.5, 1.2, 1.8, 8, 4,
                                                                         col='#A9E97D', seed=4)],
        g.particle('block{block_state:"minecraft:lime_stained_glass"}', '~ ~1.0 ~', (0.8, 1.2, 0.3), 0, 14),
        snd(g, 'block.amethyst_cluster.break', 0.6, 1.2), snd(g, 'entity.breeze.wind_burst', 0.4, 1.4),
        'scoreboard players set #pjKeep mb 0'])
    g.pw(k, 'hit', ['# The blade hit the player: a lime spark there; it flies on harmlessly to the wall.',
                    'scoreboard players set #pjKeep mb 1',
                    'execute at @e[tag=rlk_body,limit=1] run ' + g.kcard('glint', '~ ~1 ~', bb='center', col='#D6F7B9', s0=0.4, s1=1.4, life=4, fade=2),
                    'execute at @e[tag=rlk_body,limit=1] run ' + g.particle('crit', '~ ~1 ~', (0.3, 0.5, 0.3), 0.3, 8)])


def edge_search(g, k):
    """p/<k>/edge/*: a binary search over the lane lengths LANES4 for the farthest point along her yaw still inside
    r H4_EDGE (the walk disc's edge at the wall ring): #bp4L = that length (1 = shorter than every lane). Called as
    the body, at it, rotated as her yaw (pitch 0). Returns the function line of the root."""
    fn = lambda rel: f'function {A.NS}p/{k}/edge/{rel}'     # noqa: E731
    inside = f'if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{A.L.num(H4_EDGE)},limit=1]'

    def node(lo, hi):
        rel = f'{lo}_{hi}'
        if lo == hi:
            g.pw(k, f'edge/{rel}', [f'scoreboard players set #bp4L mb {lo}'])
            return rel
        mid = (lo + hi + 1) // 2
        up, dn = node(mid, hi), node(lo, mid - 1)
        g.pw(k, f'edge/{rel}', [f'# the point {lo} b ahead is inside: is {mid} b?',
                                f'execute positioned ^ ^ ^{mid} {inside} positioned ^ ^ ^-{mid} run return run {fn(up)}',
                                f'return run {fn(dn)}'])
        return rel
    root = node(1, LANES4[-1])
    return f'execute positioned ~ {CY} ~ rotated as @s rotated ~ 0 run {fn(root)}'
