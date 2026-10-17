"""P3 공간을 집행하는 시련 (melee spear slam) and P4 어둠 속에서 퍼지는 공간 (pull + two 360 swings).

Sources: patterns.md §5 / §6 (m1 9.85-25.05 s), plan.md K4, K14, K15, K17, K21, K25. Owner: the
P3/P4 author; writes only F:mboss/guardian/p/{slam,pull}/** through gen.pw. Display helpers are in
p34_fx.py. Clip ticks below are the rig's (tools/mboss_guardian_rig_manifest.json); the spear-tip
points were measured on the rig poses (gd_dbg) and are boss-frame offsets (x left, y up from the
floor, z forward).

User tuning (plan.md "공격 선딜 좀 짧게 하고 공격 범위를 좀 늘려봐"): the clips play with ~25 % shorter wind-ups
(guardian_clips.mjs RETIME; authored ticks of the fx go through api.rt / api.inv) and the hit areas are ~20 % larger.
Played ticks below.

P3 (clip `slam`, 64 t, melee: the core closes to 3 b first)
  0-6   raise; she keeps turning to the player (<= 12 deg/t), gold streak along the spear tip
  7     aim locked: ground ring r 6 centred 3.5 b ahead (K25 x1.2), thin gold ring decal + amber fill,
        hazard disc r 6, tell 13 -> hit at 20 (1.6, K17); ring chime
  8     charge (beacon power-select + respawn-anchor charge); 9-15 lens glints on the raised blade
  16-19 downswing gold streak; 20 impact: vertical gold pillar, white-gold flash over the ring,
        shock ring, burst, radial gold crystal blades (21-38), gold cubes + dark rock chunks
  20-42 spear planted (body still), 4-point star sparkles at the tip; 41 pull-out thud; 48-64 twirl
P4 (clips `pull` 32 t, then `swing` 46 t from tick 36; every band: melee at weight 1 (from closer than 5 b the
    core first hops back to 6.5 b, ai/back), mid 1, far 3)
  0-23  red haze, swirling mist, crimson arcs, the corrupted claw glow; red cubes float around her
  7-13  a cage of black cubes with glowing red edges stacks up the player (follows the body)
  14-19 screen (title font overlay, guardian_screen.mjs; right in first person and in the F5 seat
        view): dark-red diamond vignette closes in; 19 line-of-sight check (no range limit inside
        the arena; light and barrier blocks pass); 20 white flash, 22 orange field + white 4-point
        star, 23 red diamond; 24 the player is placed 1 b in front of her, facing her (undodgeable,
        tell 24 t >= 20, K14 tuned); arrival cubes drift and dissolve; the vignette opens again 24-30
        No line of sight at 19, or the destination blocked at 24: the cage shatters, the screen
        clears and she swings in place (the pattern still resolves). A refused pull (player dead,
        reviving, selection screen, map view): no swings, the pattern ends at 32.
  36    swing clip (K15: relocation -> wind-up 12 t); two 360 hazards r 6.8, tell 15: swing 1
        forehand at 51, swing 2 backhand (tilted, thicker) at 64, 1.2 each; gold crescents that
        follow the measured spear-tip angles, dark cubes and gold sparkles in the trail
"""
import math
import random
from collections import defaultdict

from .api import Pattern, ev, clip_len, rt, inv, DMG, KB, CY, GOLD, GOLD_PALE, GOLD_DEEP, CRIMSON, CRIMSON_DARK, NS, SCREEN
from . import p34_fx as X

SWING_GAP = 12        # relocation -> swing clip start (K15: 10-14 t)
SWING_TELL = 15       # swing hazard telegraph (was 20; user tuning: wind-ups ~25 % shorter, floor 10 t)
AREA = 1.2            # linear scale of the hit areas and their fx (user tuning: ~20 % larger)
PULL_LEN = clip_len('pull')
RELOC = ev('pull', 'relocate')
SWING_AT = RELOC + SWING_GAP
SWING_LEN = clip_len('swing')

PATTERNS = [
    Pattern(3, 'slam', '공간을 집행하는 시련', bands=('melee',), close=3.0, weight={'melee': 2}, recover=20,
            max_len=clip_len('slam') + 4),
    # every band: melee at a low weight (1 against 2 for P1 / P3; from closer than 5 b she first hops back to 6.5 b,
    # core ai/back), mid 1, far favoured over P2 (x3, like P5); the core also guarantees one P4 per stretch of normals
    # at any distance (ai/pity)
    Pattern(4, 'pull', '어둠 속에서 퍼지는 공간', bands=('melee', 'mid', 'far'), weight={'melee': 1, 'far': 3}, away=(5.0, 6.5),
            recover=22, max_len=SWING_AT + SWING_LEN + 4),
]

# colours (patterns.md §5 / §6 FX)
RING_HEX = '#EDD559'
AMBER = (0.93, 0.70, 0.27)
IMPACT_CORE = (0.99, 0.97, 0.68)       # #FCF8AE
IMPACT_MID = (0.86, 0.78, 0.45)        # #DCC773
TRAIL_CORE = (0.99, 0.96, 0.65)        # #FDF6A6
TRAIL_MID = (0.87, 0.74, 0.47)         # #DDBC78
MIST = (0.39, 0.12, 0.10)              # #641E19
AURA = (0.62, 0.27, 0.35)              # #9F465A
AURA_PINK = (0.89, 0.49, 0.58)         # #E37C95
CAGE_RED = (0.72, 0.18, 0.23)          # #B82F3A
CAGE_GLOW = (0.38, 0.0, 0.02)          # #600005
CUBE_ORANGE = (0.83, 0.29, 0.14)       # #D34B23
DARK = (0.23, 0.15, 0.12)              # #3A2620

BODY = 'rotated as @s rotated ~ 0'     # execute chain: the boss frame (pitch 0) at the body


def P(x, y, z):
    """Local position string ^x ^y ^z (x left, y up, z forward)."""
    return f'^{X.L.num(round(x, 3), 3)} ^{X.L.num(round(y, 3), 3)} ^{X.L.num(round(z, 3), 3)}'


def lerp3(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))


class TL:
    """Pattern timeline: tick -> commands, written as one file per busy tick (p/<key>/k/<t>)
    and dispatched from p/<key>/tick, so a tick costs one score test per busy tick."""

    def __init__(self, g, key):
        self.g, self.key = g, key
        self.ev = defaultdict(list)
        self.spans = []
        self.gate = {}

    def at(self, t, *cmds):
        for c in cmds:
            self.ev[int(t)].extend(c.split('\n') if isinstance(c, str) else c)

    def span(self, t0, t1, cmd, cond=''):
        self.spans.append((t0, t1, cmd, cond))

    def gated(self, t0, t1, cond):
        for t in range(t0, t1 + 1):
            self.gate[t] = cond

    def fn(self, t):
        return f'function {NS}p/{self.key}/k/{t}'

    def emit(self, header, start_extra=()):
        lines = list(header)
        for t0, t1, cmd, cond in self.spans:
            lines.append(f'execute if score #gdPT mb matches {t0}..{t1} {cond}run {cmd}')
        for t in sorted(self.ev):
            if t == 0:
                continue
            cond = self.gate.get(t, '')
            lines.append(f'execute if score #gdPT mb matches {t} {cond}run {self.fn(t)}')
            self.g.pw(self.key, f'k/{t}', [f'# {self.key} tick {t} (@s = body, at the body).'] + self.ev[t])
        return lines, list(start_extra) + self.ev.get(0, [])


def emit(g):
    slam(g)
    pull(g)


# =============================================================================================
# P3 공간을 집행하는 시련
SLAM_HZ = 3.5                      # disc centre ahead (K25)
SLAM_R = 6.0                       # K25 r 5, x1.2 (user tuning)
TIP_PLANT = (0.0, 0.0, 3.1)        # planted spear tip (rig: 0, -0.24, 3.09) on the floor
TIP_OVER = (-0.26, 6.82, 0.30)     # blade tip while held overhead (12-21)
RAISE = {2: (-3.59, 1.71, 1.08), 3: (-3.86, 2.42, 0.96), 4: (-3.93, 2.80, 0.90), 5: (-3.49, 4.11, 0.89),
         6: (-1.72, 5.96, 0.89), 7: (-0.44, 6.45, 0.87)}
DOWN = {21: (-0.26, 6.85, 0.27), 22: (-0.22, 6.60, 1.17), 23: (-0.10, 4.80, 3.25), 24: (-0.09, 4.24, 3.48),
        25: (-0.06, 2.48, 3.78), 26: (0.0, 0.1, 3.09)}
LIFT = {48: (0.0, 0.0, 3.09), 49: (-0.04, 0.12, 3.32), 50: (-0.21, 1.04, 3.72), 51: (-0.53, 2.37, 3.89),
        52: (-0.96, 3.67, 3.61), 53: (-1.33, 4.56, 3.11), 54: (-1.48, 4.87, 2.84), 55: (-0.33, 4.85, 2.67),
        56: (0.57, 4.30, 2.50), 57: (1.02, 3.46, 2.33), 58: (1.18, 2.63, 2.33), 59: (0.90, 1.83, 2.33),
        60: (0.26, 1.28, 2.33)}
P3TAG = 'rlk_mb_gd_p3'


def p3tags(*extra):
    return ['rlk_room', 'rlk_mb_aux', P3TAG] + list(extra)


def replayed(table, clip):
    """An authored per-tick point table {authored clip tick: point} resampled on the played ticks (api.rt): linear in the
    authored time, so the measured spear-tip paths follow the retimed clip."""
    ts = sorted(table)
    out = {}
    for t in range(rt(clip, ts[0]), rt(clip, ts[-1]) + 1):
        u = min(max(inv(clip, t), ts[0]), ts[-1])
        a, b = max(x for x in ts if x <= u), min(x for x in ts if x >= u)
        out[t] = table[a] if a == b else lerp3(table[a], table[b], (u - a) / (b - a))
    return out


def streak(g, path, t, rgb, scale, n=5):
    """Dust along the spear-tip path from tick t-1 to t (boss frame)."""
    a, b = path.get(t - 1, path[t]), path[t]
    out = []
    for i in range(n):
        p = lerp3(a, b, (i + 1) / n)
        out.append(f'execute {BODY} run ' + g.dust(rgb, scale, P(*p), (0.04, 0.04, 0.04), 1))
    return out


def disc_points(rng, r, n):
    pts = []
    for _ in range(n):
        rr = r * math.sqrt(rng.random())
        a = rng.random() * 2 * math.pi
        pts.append((rr * math.sin(a), rr * math.cos(a)))
    return pts


def slam(g):
    k = 'slam'
    tl = TL(g, k)
    rng = random.Random(3034)
    ring, glint, down, imp = ev(k, 'ring'), ev(k, 'glint'), ev(k, 'down'), ev(k, 'impact')
    pullt, twirl, length = ev(k, 'pull'), ev(k, 'twirl'), clip_len(k)
    assert imp - ring >= 10, 'K4 (tuned): the ring leads the impact by >= 10 t'
    W = lambda t: rt(k, t)            # authored (source) tick -> played tick
    raise_p, down_p, lift_p = replayed(RAISE, k), replayed(DOWN, k), replayed(LIFT, k)
    tip = TIP_PLANT
    at_tip = f'{BODY} positioned {P(*tip)} positioned ~ {CY} ~'
    at_hz = f'{BODY} positioned ^ ^ ^{SLAM_HZ} positioned ~ {CY} ~'
    S_RING = 2 * SLAM_R / 0.86         # Navia ring card: the ring sits at 0.86 of the half-size

    # ---- raise 0-8: she keeps turning to the player until the aim locks at the ring
    tl.span(1, ring - 1, g.rig('face/track'))
    tl.at(W(2), g.sound('entity.player.attack.sweep', 0.45, 0.6), g.sound('item.trident.riptide_1', 0.3, 1.5))
    for t in sorted(raise_p)[1:]:
        tl.at(t, *streak(g, raise_p, t, GOLD_PALE, 0.8, 4))

    # ---- ring: telegraph + hazard (disc r 6 at 3.5 b, tell 13, 1.6)
    tl.at(ring,
          f'# Aim locked: disc r {X.L.num(SLAM_R)} centred {SLAM_HZ} b ahead (K25 x1.2), ring lead {imp - ring} t -> hit on the impact (clip {imp}).',
          'scoreboard players set #hzSfx mb 0',
          f'scoreboard players set #hzVis mb {3 * 10 + 1}',
          f'scoreboard players set #hzKB mb {KB["default"]}',
          f'execute {at_hz} run {g.hz_disc(SLAM_R, imp - ring, DMG["p3"])}',
          f'execute {at_hz} run ' + g.sound('block.amethyst_block.chime', 0.8, 1.2),
          f'execute {at_hz} run ' + g.sound('block.amethyst_block.resonate', 0.5, 1.5))
    # the ring decal (summoned by vis at the marker) widens a little and turns slowly
    tl.at(ring + 1, X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3ring]',
                            X.tf((0, 0, 0), X.qmul(X.yaw_q(110), X.FLAT_UP), S_RING), imp - ring - 2))
    fill = [disc_points(rng, SLAM_R - 0.25, 17) for _ in range(3)]
    for t in range(ring, imp, 2):
        pts = fill[(t // 2) % 3]
        tl.at(t, *[f'execute {at_hz} run ' + g.dust(AMBER, 0.9, f'^{X.L.num(round(x, 2))} ^0.08 ^{X.L.num(round(z, 2))}', (0, 0, 0), 1)
                   for x, z in pts])

    # ---- 11-21: charge, lens glints on the raised blade
    tl.at(W(11), g.sound('block.beacon.power_select', 0.6, 1.5), g.sound('block.respawn_anchor.charge', 0.7, 1.5))
    for t, (s0, s1, life) in ((glint, (0.2, 1.8, 9)), (W(17), (0.1, 1.1, 6)), (W(20), (0.3, 2.3, 5))):
        tl.at(t, f'execute {BODY} run ' + g.card('star', P(*TIP_OVER), bb='center', spin=90, s0=s0, s1=s1, life=life, fade=3),
              f'execute {BODY} run ' + g.particle('end_rod', P(*TIP_OVER), (0.1, 0.1, 0.1), 0.04, 3))
    tl.at(glint, g.sound('block.amethyst_block.chime', 0.6, 2.0))
    tl.at(W(20), g.sound('block.amethyst_block.chime', 0.5, 1.8))
    for t in range(glint, down, 2):
        tl.at(t, f'execute {BODY} run ' + g.dust(GOLD, 0.8, P(TIP_OVER[0], TIP_OVER[1] - 0.6, TIP_OVER[2]), (0.12, 0.4, 0.12), 3),
              f'execute {BODY} run ' + g.particle('wax_on', P(*TIP_OVER), (0.2, 0.3, 0.2), 0, 1))

    # ---- 22-25: downswing streak
    for t in range(down, imp + 1):
        tl.at(t, *streak(g, down_p, t, GOLD_PALE, 1.3, 7), *streak(g, down_p, t, GOLD, 1.0, 4))
    tl.at(W(23), g.sound('entity.player.attack.sweep', 0.75, 0.55), g.sound('item.trident.riptide_2', 0.4, 1.3))

    # ---- 26: impact
    pil = ('rlk_mb_gd_p3pil',)
    new = 'rlk_mb_gd_p3new'
    tl.at(imp,
          '# Impact: vertical gold pillar, flash over the ring, shock ring, burst, sounds (the hazard strikes now).',
          f'execute {at_tip} run ' + X.item_display(X.card_model('glow'), p3tags(*pil), X.tf((0, 3.4, 0), s=(1.25, 7.2, 1)), bb='vertical'),
          f'execute {at_tip} run ' + X.item_display(X.card_model('glow'), p3tags(*pil), X.tf((0, 3.0, 0), s=(0.45, 6.4, 1)), bb='vertical'),
          f'execute {at_hz} run ' + X.item_display(X.card_model('glow'), p3tags('rlk_mb_gd_p3fl'), X.tf((0, 0.06, 0), X.FLAT_UP, 2 * SLAM_R)),
          f'execute {at_tip} run ' + X.item_display(X.card_model('ring'), p3tags('rlk_mb_gd_p3sw'), X.tf((0, 0.1, 0), X.FLAT_UP, 1.4)),
          f'execute {BODY} run ' + g.card('burst', P(tip[0], 1.3, tip[2]), bb='center', spin=20, s0=0.8, s1=3.6 * AREA, life=6, fade=3),
          f'execute {at_tip} run ' + g.dust(GOLD_PALE, 1.6, '~ ~1.6 ~', (0.15, 1.7, 0.15), 26),
          f'execute {at_tip} run ' + g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.3 ~', (1.3 * AREA, 0.2, 1.3 * AREA), 0, 30),
          f'execute {at_tip} run ' + g.particle('end_rod', '~ ~0.5 ~', (0.3, 0.3, 0.3), 0.18, 14),
          f'execute {at_tip} run ' + g.particle('explosion', '~ ~0.4 ~', (0.3, 0.1, 0.3), 0, 1),
          f'execute {at_hz} run ' + g.dust(IMPACT_CORE, 1.4, '~ ~0.15 ~', (2.2 * AREA, 0.05, 2.2 * AREA), 30),
          f'execute {at_tip} run ' + g.sound('entity.generic.explode', 0.8, 0.9),
          f'execute {at_tip} run ' + g.sound('block.amethyst_cluster.break', 1.0, 0.8),
          f'execute {at_tip} run ' + g.sound('item.trident.thunder', 0.3, 1.2),
          f'execute {at_tip} run ' + g.sound('block.amethyst_block.break', 0.6, 0.7))
    tl.at(imp + 1,
          X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3pil]', X.tf((0, 3.8, 0), s=(0.6, 7.9, 1)), 2),
          X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3fl]', X.tf((0, 0.06, 0), X.FLAT_UP, 2 * SLAM_R + 0.8), 1),
          X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3sw]', X.tf((0, 0.1, 0), X.qmul(X.yaw_q(60), X.FLAT_UP), 2 * (SLAM_R + 0.6) / 0.86), 4))
    tl.at(imp + 2, X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3fl]', X.tf((0, 0.06, 0), X.FLAT_UP, 0.01), 3))
    tl.at(imp + 3, X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3pil]', X.tf((0, 4.2, 0), s=(0.01, 8.4, 1)), 2))
    tl.at(imp + 5, 'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3pil]',
          'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3fl]')
    tl.at(imp + 6, 'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3sw]')

    # ---- 27-48: radial gold crystal blades jutting out of the ground around the tip
    blades = []
    for i in range(11):
        inner = i % 2 == 0
        yaw = i * (360 / 11) + rng.uniform(-9, 9)
        rho = (rng.uniform(0.5, 1.1) if inner else rng.uniform(1.6, 2.7)) * AREA
        L_ = rng.uniform(1.9, 2.7) if inner else rng.uniform(1.1, 1.7)
        lean = rng.uniform(14, 30) if inner else rng.uniform(30, 46)
        roll = rng.uniform(-12, 12)
        root = X.fwd(yaw, rho)
        root = (root[0], -0.12, root[2])
        blades.append((yaw, lean, L_, roll, root, inner))
    summ, grow, shrink = [], [], []
    for j, (yaw, lean, L_, roll, root, inner) in enumerate(blades):
        tg = f'rlk_mb_gd_p3b{j}'
        sel = f'@e[type=minecraft:item_display,tag={tg}]'
        summ.append(f'execute {at_tip} run ' + X.item_display(X.card_model('shard'), p3tags('rlk_mb_gd_p3bl', tg, new), X.shard_tf(root, yaw, lean, 0.05, roll, 1.3)))
        grow.append(X.merge(sel, X.shard_tf(root, yaw, lean, L_, roll, 1.3), 2))
        shrink.append(X.merge(sel, X.shard_tf(root, yaw, lean, 0.02, roll, 1.3), 4))
        if inner:            # crossed copy so the big blades never vanish edge-on
            tgx = f'rlk_mb_gd_p3x{j}'
            selx = f'@e[type=minecraft:item_display,tag={tgx}]'
            q = X.qmul(X.yaw_q(yaw), X.qmul(X.qaxis((1, 0, 0), lean), X.qaxis((0, 0, 1), roll)))
            summ.append(f'execute {at_tip} run ' + X.item_display(X.card_model('shard'), p3tags('rlk_mb_gd_p3bl', tgx, new), X.tf(root, q, 0.05, X.yaw_q(90))))
            grow.append(X.merge(selx, X.tf(root, q, L_, X.yaw_q(90)), 2))
            shrink.append(X.merge(selx, X.tf(root, q, 0.02, X.yaw_q(90)), 4))
    tl.at(imp + 1, '# Radial gold crystal blades (grow 28-30, hold, retract 44-48).', *summ,
          f'execute {at_tip} run tp @e[tag={new}] ~ ~ ~ ~ 0', f'tag @e[tag={new}] remove {new}',
          f'execute {at_tip} run ' + g.sound('block.amethyst_cluster.place', 0.9, 0.7),
          f'execute {at_tip} run ' + g.sound('block.pointed_dripstone.land', 0.6, 0.8))
    tl.at(imp + 2, *grow)
    tl.at(W(44), *shrink, f'execute {at_tip} run ' + g.sound('block.amethyst_cluster.step', 0.6, 1.2))
    tl.at(W(48), 'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3bl]')

    # ---- 27-42: gold cubes + dark rock chunks thrown out of the crater
    csum, c1, c2, c3 = [], [], [], []
    blocks = ['gold_block', 'raw_gold_block', 'gold_block', 'yellow_stained_glass', 'raw_gold_block', 'gold_block',
              'black_terracotta', 'blackstone', 'black_terracotta', 'polished_blackstone', 'black_terracotta']
    for j, blk in enumerate(blocks):
        tg = f'rlk_mb_gd_p3c{j}'
        sel = f'@e[type=minecraft:block_display,tag={tg}]'
        yaw = j * (360 / len(blocks)) + rng.uniform(-14, 14)
        size = rng.uniform(0.28, 0.48) if j < 6 else rng.uniform(0.22, 0.36)
        d1, h1 = rng.uniform(1.0, 2.4) * AREA, rng.uniform(1.2, 2.6)
        d2 = d1 + rng.uniform(0.6, 1.3) * AREA
        p0 = (0.0, 0.35, 0.0)
        p1 = (X.fwd(yaw, d1)[0], h1, X.fwd(yaw, d1)[2])
        p2 = (X.fwd(yaw, d2)[0], size / 2, X.fwd(yaw, d2)[2])
        ax = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        q0 = X.qaxis(ax, rng.uniform(0, 90))
        q1 = X.qmul(X.qaxis(ax, 130), q0)
        q2 = X.qmul(X.qaxis(ax, 120), q1)
        csum.append(f'execute {at_tip} run ' + X.block_display(blk, p3tags('rlk_mb_gd_p3cb', tg, new), X.cube_tf(p0, 0.05, q0)))
        c1.append(X.merge(sel, X.cube_tf(p1, size, q1), 4))
        c2.append(X.merge(sel, X.cube_tf(p2, size * 0.85, q2), 6))
        c3.append(X.merge(sel, X.cube_tf(p2, 0.01, q2), 4))
    tl.at(imp + 1, '# Gold cubes and dark rock chunks: thrown up 28-32, fall 32-38, shrink away 38-42.', *csum,
          f'execute {at_tip} run tp @e[tag={new}] ~ ~ ~ ~ 0', f'tag @e[tag={new}] remove {new}')
    tl.at(imp + 2, *c1)
    tl.at(imp + 6, *c2, f'execute {at_tip} run ' + g.sound('block.basalt.fall', 0.6, 0.8))
    tl.at(imp + 12, *c3)
    tl.at(imp + 16, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p3cb]')
    for t in range(imp + 1, imp + 7):
        tl.at(t, f'execute {at_tip} run ' + g.particle('wax_on', '~ ~0.8 ~', (1.4, 0.6, 1.4), 0, 3),
              f'execute {at_tip} run ' + g.dust(IMPACT_MID, 1.1, '~ ~0.4 ~', (1.6 * AREA, 0.3, 1.6 * AREA), 4))

    # ---- 30-47: 4-point star sparkles at the planted tip, twinkles
    spark = [(rng.uniform(-0.6, 0.6), rng.uniform(0.1, 1.7), rng.uniform(-0.5, 0.5)) for _ in range(6)]
    for n, t in enumerate(range(W(30), W(48), 3)):
        x, y, z = spark[n]
        tl.at(t, f'execute {BODY} run ' + g.card('star', P(tip[0] + x, y, tip[2] + z), bb='center', spin=45, s0=0.05,
                                                 s1=rng.uniform(0.45, 0.75), life=7, fade=3),
              f'execute {at_tip} run ' + g.particle('end_rod', '~ ~0.8 ~', (0.25, 0.6, 0.25), 0.01, 2))
    tl.at(W(42), f'execute {at_tip} run ' + g.sound('block.amethyst_block.chime', 0.5, 1.9))
    tl.at(W(45), f'execute {at_tip} run ' + g.sound('block.amethyst_block.chime', 0.4, 2.0))

    # ---- 47-53: pull-out
    tl.at(pullt - 1, f'execute {at_tip} run ' + g.sound('block.chain.break', 0.8, 0.6),
          f'execute {at_tip} run ' + g.sound('block.stone.break', 0.8, 0.8))
    tl.at(pullt,
          f'execute {at_tip} run ' + g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.2 ~', (0.3, 0.1, 0.3), 0, 12),
          f'execute {at_tip} run ' + g.particle('block{block_state:"minecraft:black_terracotta"}', '~ ~0.2 ~', (0.4, 0.1, 0.4), 0, 8),
          f'execute {at_tip} run ' + X.item_display(X.card_model('ring'), p3tags('rlk_mb_gd_p3po'), X.tf((0, 0.08, 0), X.FLAT_UP, 0.8)))
    tl.at(pullt + 1, X.merge('@e[type=minecraft:item_display,tag=rlk_mb_gd_p3po]', X.tf((0, 0.08, 0), X.FLAT_UP, 3.4), 4))
    tl.at(pullt + 6, 'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3po]')
    for t in range(pullt + 1, W(61)):
        tl.at(t, *streak(g, lift_p, t, TRAIL_CORE if t < twirl else TRAIL_MID, 0.9 if t < twirl else 0.7, 4))

    # ---- 54-70: twirl to idle
    for t in (twirl + 1, twirl + 6):
        tl.at(t, g.sound('item.trident.riptide_1', 0.35, 1.4), g.sound('entity.player.attack.sweep', 0.45, 0.7))
    tl.at(length, g.end())

    tick, start_extra = tl.emit([
        f'# P3 tick (@s = body, #gdPT = slam clip tick). Busy ticks run p/{k}/k/<t>. The body never moves:',
        f'# the core closed in to 3 b; she turns to the player until the aim locks at the ring ({ring}); the',
        f'# spear is planted {imp}-{pullt} (rig API §4).'])
    g.pw(k, 'start', [
        f'# P3 start (@s = body, within 3 b after the core\'s close-in): slam clip ({length} t: raise 0, ring {ring},',
        f'# glint {glint}, down {down}, impact {imp}, pull {pullt}, twirl {twirl}).',
        g.rig('face/player'),
        g.play(k)] + start_extra)
    g.pw(k, 'tick', tick)
    g.pw(k, 'vis', [
        '# hz_vis of the slam disc (@s = hazard marker on the floor, rotated = aim; #hzEv 0 create / 1 strike / 2 end):',
        f'# a thin gold ring decal (Navia ring card, ring at r {X.L.num(SLAM_R)}) that widens and turns until the strike.',
        f'execute if score #hzEv mb matches 0 run summon minecraft:item_display ~ ~0.04 ~ {{{X.tags(*p3tags("rlk_mb_hzfx", "rlk_mb_gd_p3ring"))},'
        f'billboard:"fixed",{X.BRIGHT},view_range:3f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,'
        f'{X.tf((0, 0, 0), X.FLAT_UP, S_RING * 0.86)},item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{X.card_model("ring")}"}}}}}}',
        'execute if score #hzEv mb matches 1.. run kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3ring]'])
    g.pw(k, 'cancel', [
        '# P3 cancel (any executor): every display of the slam carries rlk_mb_gd_p3 (hazards go with lib_clear).',
        f'kill @e[tag={P3TAG}]'])


# =============================================================================================
# P4 어둠 속에서 퍼지는 공간
P4TAG = 'rlk_mb_gd_p4'
CLAW = (-0.30, 2.95, 0.90)               # the corrupted right claw while casting (pull clip 8-32)
HOLD_TIP = (2.70, 3.26, -0.75)           # spear tip behind her left shoulder in the swing hold (5-17)
SWING_R = 6.8                            # K15 r 5-6 (was 5.5), x1.24 (user tuning: about r 6.5-7)
SW_K = SWING_R / 5.5                     # scale of the swing fx authored for r 5.5
# measured spear-tip angles (deg, 0 = her front, + = her left) on the authored swing clip ticks, mapped to the played
# ticks (the strikes sit on a 1:1 segment of the retiming, so the angles stay exact)
SW1 = {rt('swing', t): a for t, a in {18: 31, 19: -20, 20: -60, 21: -132, 22: -204, 23: -276, 24: -348, 25: -420}.items()}
SW2 = {rt('swing', t): a for t, a in {33: -63, 34: -3, 35: 57, 36: 120, 37: 179, 38: 239, 39: 311}.items()}
SW1_Y, SW2_Y = 1.9, 1.5                  # crescent planes (swing 1 level, swing 2 tilted, low in front)
SW2_TILT = (0, 11)
CAGE = [  # (spawn tick (played), centre x, y, z around the body feet, edge); authored ticks 11-20
    (rt('pull', t), x, y, z, e) for t, x, y, z, e in (
        (11, 0.12, 0.26, 0.10, 0.52), (12, -0.30, 0.30, -0.16, 0.50), (13, 0.26, 0.66, -0.28, 0.46),
        (13, -0.12, 0.72, 0.30, 0.50), (14, -0.34, 0.98, 0.08, 0.54), (15, 0.30, 1.16, 0.20, 0.50),
        (16, -0.20, 1.36, -0.30, 0.50), (17, 0.08, 1.56, 0.34, 0.46), (18, -0.30, 1.80, 0.06, 0.50),
        (19, 0.26, 1.90, -0.22, 0.48), (20, 0.00, 2.14, 0.02, 0.44))]
CAGE_EYE = 1.3                          # first person: no cage cube reaches above this
# screen overlay frames per pull tick (title font glyphs; frames and their texts: guardian_screen.mjs via the
# rig manifest): vignette closes 14-19, flash 20-21, field + star 22, red diamond 23, vignette reopens 24-30
# (authored 22-38; the retiming keeps this part 1:1, every frame stays)
SCR_FRAMES = {rt('pull', t): n for t, n in {22: 'vig0', 23: 'vig1', 24: 'vig2', 25: 'vig3', 26: 'vig4', 27: 'vig5', 28: 'flash', 29: 'flash',
              30: 'field', 31: 'diamond', 32: 'vig5', 33: 'vig5', 34: 'vig4', 35: 'vig3', 36: 'vig2', 37: 'vig1', 38: 'vig0'}.items()}
SCR_FIRST = min(SCR_FRAMES)
SCR_LAST = max(SCR_FRAMES)               # its frame fades out over 4 t


def p4tags(*extra):
    return ['rlk_room', 'rlk_mb_aux', P4TAG] + list(extra)


def pull(g):
    k = 'pull'
    tl = TL(g, k)
    rng = random.Random(4044)
    aura, cage0 = ev('pull', 'aura'), ev('pull', 'cage')
    assert RELOC - aura >= 20, 'K14 (tuned): the pull needs a tell of at least 20 t'
    W = lambda t: rt('pull', t)       # authored (source) pull tick -> played tick
    s1 = SWING_AT + ev('swing', 'swing1')
    s2 = SWING_AT + ev('swing', 'swing2')
    tell = SWING_TELL
    assert s2 - tell > SWING_AT and tell >= 10 and s1 - SWING_AT == tell
    end = SWING_AT + SWING_LEN
    new = 'rlk_mb_gd_p4new'
    body_feet = 'at @e[tag=rlk_body,limit=1]'
    # #gp4Ok: 0 before the check / pull refused, 1 line of sight + pulled, 2 no pull (blocked) but she swings in place
    tl.gated(W(28), PULL_LEN - 1, 'if score #gp4Ok mb matches 1 ')
    tl.gate[PULL_LEN] = ''
    tl.gated(PULL_LEN + 1, end, 'if score #gp4Ok mb matches 1.. ')
    assert SCREEN and set(SCR_FRAMES.values()) <= set(SCREEN['frames']), 'rig manifest: run build_mboss_guardian_rig.mjs'

    # ---- 0-31: aura behind her, swirling mist, crimson arcs, the claw; she tracks the player
    tl.span(1, RELOC - 1, g.rig('face/track'))
    tl.at(W(4), g.sound('block.fire.extinguish', 0.25, 1.7))
    tl.at(W(6), g.sound('entity.warden.sonic_charge', 0.35, 1.4))
    for t in (8, 13, 18, 23):
        tl.at(W(t), g.sound('block.fire.ambient', 0.8, 0.7 + 0.1 * ((t - 8) // 5)))
    tl.at(W(14), g.sound('block.respawn_anchor.charge', 0.6, 1.3))
    for t in range(1, PULL_LEN + 1):
        u = inv('pull', t)            # authored time: the aura is authored on the source timeline
        live = t <= RELOC
        lines = []
        nh = min(2 + int(u) // 3, 8) if live else max(1, 8 - (t - RELOC))
        lines.append(f'execute {BODY} run ' + g.dust_fade(CRIMSON, MIST, 1.6, P(0, 1.9, -0.8), (0.7, 0.9, 0.35), nh))
        if u >= 2:
            for kk in range(3 if live else 1):
                a = math.radians(u * 41 + kk * 120)
                r = 1.15 + 0.3 * math.sin(u / 3 + kk)
                y = 0.9 + kk * 0.8 + 0.4 * math.sin(u / 5 + kk)
                lines.append(f'execute {BODY} run ' + g.dust(AURA, 1.3, P(r * math.sin(a), y, r * math.cos(a)), (0.08, 0.08, 0.08), 2))
        if live and u >= 4 and t % 2 == 0 and u <= 28:
            a0, r0 = rng.uniform(0, 360), rng.uniform(0.5, 1.0)
            a1, r1 = a0 + rng.uniform(70, 140), rng.uniform(0.9, 1.5)
            p0 = (X.fwd(a0, r0)[0], rng.uniform(1.4, 3.0), X.fwd(a0, r0)[2])
            p1 = (X.fwd(a1, r1)[0], rng.uniform(1.2, 3.2), X.fwd(a1, r1)[2])
            bulge = (0.0, rng.uniform(0.3, 0.7), 0.0)
            for i in range(8):
                u = i / 7
                p = lerp3(p0, p1, u)
                b = 4 * u * (1 - u)
                p = (p[0] * (1 + 0.35 * b), p[1] + bulge[1] * b, p[2] * (1 + 0.35 * b))
                lines.append(f'execute {BODY} run ' + g.dust(AURA_PINK if i % 3 else (1.0, 0.82, 0.86), 0.7, P(*p), (0, 0, 0), 1))
        if live and u >= 6:
            lines.append(f'execute {BODY} run ' + g.dust((0.9, 0.2, 0.3), 1.0, P(*CLAW), (0.1, 0.1, 0.1), 2))
            if t % 3 == 0:
                lines.append(f'execute {BODY} run ' + g.dust((1.0, 0.75, 0.8), 0.6, P(*CLAW), (0.03, 0.03, 0.03), 1))
        if live and u >= 8 and t % 2 == 0:
            lines.append(f'execute {BODY} run ' + g.particle('crimson_spore', P(0, 1.8, 0), (1.2, 1.2, 1.2), 0, 4))
        tl.at(t, *lines)              # after the relocation: the decaying haze (gated on #gp4Ok)

    # ---- 10-15: red cubes floating around her (pop in, drift, shrink away 33-39)
    rc_sum = {}
    rc_blocks = ['red_concrete', 'red_stained_glass', 'black_concrete', 'red_concrete', 'red_stained_glass', 'black_concrete']
    for j, blk in enumerate(rc_blocks):
        t0 = W(10 + j)
        tg = f'rlk_mb_gd_p4rc{j}'
        sel = f'@e[type=minecraft:block_display,tag={tg}]'
        a = j * 60 + rng.uniform(-20, 20) + 150
        r = rng.uniform(1.1, 2.1)
        c0 = (X.fwd(a, r)[0], rng.uniform(0.7, 3.2), X.fwd(a, r)[2])
        c1 = (c0[0] * 1.15, c0[1] + rng.uniform(0.3, 0.7), c0[2] * 1.15)
        size = rng.uniform(0.22, 0.4)
        ax = (rng.uniform(-1, 1), 1, rng.uniform(-1, 1))
        q0 = X.qaxis(ax, rng.uniform(0, 60))
        q1 = X.qmul(X.qaxis(ax, 150), q0)
        tl.at(t0, f'execute {BODY} run ' + X.block_display(blk, p4tags('rlk_mb_gd_p4rc', tg, new), X.cube_tf(c0, 0.02, q0)),
              f'execute {BODY} run tp @e[tag={new}] ~ ~ ~ ~ 0', f'tag @e[tag={new}] remove {new}')
        tl.at(t0 + 1, X.merge(sel, X.cube_tf(c0, size, q0), 2))
        tl.at(t0 + 3, X.merge(sel, X.cube_tf(c1, size, q1), RELOC - t0 - 2))
        rc_sum[j] = (sel, c1, q1)
    tl.at(RELOC + 1, *[X.merge(sel, X.cube_tf(c1, 0.01, q1), 6) for sel, c1, q1 in rc_sum.values()])
    tl.at(PULL_LEN, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc]')

    # ---- 11-31: the cage of black, red-edged cubes stacking up the player (follows the body)
    tl.at(cage0, g.sound('entity.illusioner.prepare_mirror', 0.7, 0.8))
    for j, (t0, x, y, z, e) in enumerate(CAGE):
        tg = f'rlk_mb_gd_p4k{j}'
        q = X.qmul(X.yaw_q(rng.uniform(-35, 35)), X.qaxis((1, 0, 0.4), rng.uniform(-12, 12)))
        # cubes at head height only around the shoulder-view avatar: in first person they would sit on the eyes
        head = 'if entity @e[tag=rlk_av,limit=1] ' if y + e / 2 > CAGE_EYE else ''
        tl.at(t0, f'execute {head}{body_feet} run ' + X.block_display('black_concrete', p4tags('rlk_mb_gd_p4cage', tg), X.cube_tf((x, y, z), 0.05, q),
                                                              glow='#B82F3A', tp_dur=1),
              f'execute {body_feet} run ' + g.particle('block{block_state:"minecraft:black_concrete"}', f'~{X.L.num(x)} ~{X.L.num(y)} ~{X.L.num(z)}', (0.15, 0.15, 0.15), 0, 3))
        tl.at(t0 + 1, X.merge(f'@e[type=minecraft:block_display,tag={tg}]', X.cube_tf((x, y, z), e, q), 2))
    tl.span(cage0 + 1, RELOC - 1, f'execute {body_feet} run tp @e[type=minecraft:block_display,tag=rlk_mb_gd_p4cage] ~ ~ ~')
    for t in range(W(17), RELOC):
        tl.at(t, f'execute {body_feet} run ' + g.dust(CAGE_RED, 1.2, '~ ~1.1 ~', (0.45, 0.8, 0.45), 4),
              f'execute {body_feet} run ' + g.dust(CAGE_GLOW, 1.5, '~ ~1.1 ~', (0.55, 0.9, 0.55), 2))

    # ---- 22-38: screen overlay (title font glyph frames: on the camera in every view mode)
    for t, name in sorted(SCR_FRAMES.items()):
        fade = '0 1 4' if t == SCR_LAST else '0 3 0'
        # the F5 crosshair title (view/ride_tick, every 10 t) rests until the last frame has faded (vBig)
        lines = [f'scoreboard players set @a[tag=player] vBig {SCR_LAST - t + 6}',
                 f'title @a[tag=player] times {fade}', f'title @a[tag=player] title {SCREEN["frames"][name]}']
        if t == SCR_FIRST:
            lines.insert(0, '# Screen overlay: every frame is a title of 4 glyph tiles (one flat glyph for the flash).')
        if t == RELOC:
            continue                    # shown by p/pull/reloc after a successful pull
        tl.at(t, *lines)
    tl.at(W(27), '# Line of sight (K14), checked before the flash: blocked -> the cage shatters, no pull, she swings in place.',
          g.fn('p/pull/los'),
          f'execute unless score #gp4Ok mb matches 1 run {g.fn("p/pull/fizzle")}')
    tl.at(W(28), g.sound('entity.enderman.teleport', 1.0, 0.6), g.sound('block.respawn_anchor.deplete', 0.9, 1.0),
          f'execute {body_feet} run ' + g.particle('reverse_portal', '~ ~1 ~', (0.4, 0.8, 0.4), 0.05, 20))
    tl.at(W(31), g.sound('entity.illusioner.mirror_move', 1.0, 1.0))

    # ---- 32: the relocation (undodgeable): 1 b in front of her, facing her
    arr = []
    a_blocks = ['orange_concrete', 'red_concrete', 'red_stained_glass', 'orange_stained_glass', 'black_concrete', 'red_concrete', 'orange_concrete', 'black_concrete']
    for j, blk in enumerate(a_blocks):
        tg = f'rlk_mb_gd_p4a{j}'
        a = 70 + j * 30 + rng.uniform(-10, 10)       # sides and toward her: none between the player and the camera
        r = rng.uniform(0.9, 2.4)
        c0 = (X.fwd(a, r)[0], rng.uniform(0.3, 2.6), X.fwd(a, r)[2])
        c1 = (c0[0] * 1.3, c0[1] + rng.uniform(0.4, 1.0), c0[2] * 1.3)
        size = rng.uniform(0.28, 0.55)
        ax = (rng.uniform(-1, 1), 1, rng.uniform(-1, 1))
        q0 = X.qaxis(ax, rng.uniform(0, 90))
        q1 = X.qmul(X.qaxis(ax, 140), q0)
        arr.append((tg, blk, c0, c1, size, q0, q1))
    tl.at(RELOC,
          '# Relocation: cage bursts, the player is placed 1 b in front of her facing her (pull/start t 0).',
          f'execute {body_feet} run ' + g.particle('block{block_state:"minecraft:black_concrete"}', '~ ~1 ~', (0.4, 0.8, 0.4), 0, 24),
          f'execute {body_feet} run ' + g.dust(CAGE_RED, 1.4, '~ ~1 ~', (0.5, 0.9, 0.5), 16),
          'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4cage]',
          g.fn('p/pull/reloc'),
          *[f'execute if score #gp4Ok mb matches 1 {body_feet} {BODY} run ' + X.block_display(blk, p4tags('rlk_mb_gd_p4ar', tg, new), X.cube_tf(c0, size, q0))
            for tg, blk, c0, c1, size, q0, q1 in arr],
          f'execute {body_feet} {BODY} run tp @e[tag={new}] ~ ~ ~ ~ 0', f'tag @e[tag={new}] remove {new}',
          f'execute {body_feet} run ' + g.dust_fade((0.93, 0.51, 0.38), CRIMSON, 1.3, '~ ~1 ~', (1.2, 0.9, 1.2), 18),
          g.sound('block.beacon.deactivate', 0.5, 0.7))
    tl.at(RELOC + 1, *[X.merge(f'@e[type=minecraft:block_display,tag={tg}]', X.cube_tf(c1, size * 0.8, q1), 16) for tg, blk, c0, c1, size, q0, q1 in arr])
    tl.at(RELOC + 14, *[X.merge(f'@e[type=minecraft:block_display,tag={tg}]', X.cube_tf(c1, 0.01, q1), 8) for tg, blk, c0, c1, size, q0, q1 in arr])
    tl.at(RELOC + 23, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4ar]')
    tl.at(PULL_LEN, '# Pull clip over: a refused pull (#gp4Ok 0) ends the pattern here (no swings, nothing to show).',
          f'execute if score #gp4Ok mb matches 0 run {g.fn("p/pull/scr_end")}',
          f'execute if score #gp4Ok mb matches 0 run {g.set_len(PULL_LEN)}',
          f'execute if score #gp4Ok mb matches 0 run {g.end()}')

    # ---- the two 360 swings (swing clip from SWING_AT)
    tl.at(SWING_AT,
          f'# Swing clip ({SWING_LEN} t): wind-up 0-5, hold 5-{ev("swing", "swing1") - 1}, swing 1 at clip {ev("swing", "swing1")} (= {s1}), '
          f'swing 2 at clip {ev("swing", "swing2")} (= {s2}); hazards r {X.L.num(SWING_R)}, tell {tell}.',
          g.play('swing'),
          'scoreboard players set #hzSfx mb 0', 'scoreboard players set #hzAct mb 3',
          f'scoreboard players set #hzVis mb {4 * 10 + 1}',
          f'execute positioned ~ {CY} ~ {BODY} run {g.hz_sector(SWING_R, 180, tell, DMG["p4"])}',
          g.sound('item.trident.riptide_1', 0.4, 0.8))
    tl.at(s2 - tell,
          'scoreboard players set #hzSfx mb 0', 'scoreboard players set #hzAct mb 3',
          f'scoreboard players set #hzVis mb {4 * 10 + 2}',
          f'execute positioned ~ {CY} ~ {BODY} run {g.hz_sector(SWING_R, 180, tell, DMG["p4"])}')
    S_RING = 2 * SWING_R / 0.86
    for kk, t0 in ((1, SWING_AT), (2, s2 - tell)):
        tl.at(t0 + 1, X.merge(f'@e[type=minecraft:item_display,tag=rlk_mb_gd_p4r{kk}]',
                              X.tf((0, 0, 0), X.qmul(X.yaw_q(-100 if kk == 1 else 100), X.FLAT_UP), S_RING), tell - 2))
    # hold: gold glint and motes on the spear behind her shoulders
    hold = SWING_AT + rt('swing', 5)
    tl.at(hold, f'execute {BODY} run ' + g.card('star', P(*HOLD_TIP), bb='center', spin=60, s0=0.2, s1=1.4, life=8, fade=3),
          g.sound('block.amethyst_block.chime', 0.5, 1.7), g.sound('block.beacon.power_select', 0.35, 1.8))
    for t in range(hold, s1 - 1, 3):
        tl.at(t, f'execute {BODY} run ' + g.dust(GOLD, 0.8, P(HOLD_TIP[0] * 0.7, HOLD_TIP[1] * 0.85, HOLD_TIP[2] * 0.7), (0.4, 0.25, 0.3), 3),
              f'execute {BODY} run ' + g.particle('wax_on', P(*HOLD_TIP), (0.2, 0.2, 0.2), 0, 1))

    def sweep(table, base, height, mirror, tilt, layers, tagp):
        """Crescents chasing the measured tip angles: each spawns at the tip's angle and turns with
        it for 2 ticks (<= 144 deg per interpolation), then shrinks away."""
        ticks = sorted(table)
        first = ticks[1] if mirror else ticks[0]
        chain = [t for t in ticks if t >= first][::2]
        for n, c in enumerate(chain):
            if c + 2 not in table:
                break
            t0 = base + c
            h0, h1 = table[c], table[c + 2]
            for li, kscale in enumerate(layers):
                tg = f'{tagp}{n}{li}'
                sel = f'@e[type=minecraft:item_display,tag={tg}]'
                tl.at(t0, f'execute positioned ~ {CY} ~ {BODY} run '
                      + X.item_display(X.card_model('crescent'), p4tags('rlk_mb_gd_p4cr', tg, new), X.crescent_tf(h0, SWING_R - 0.15, height, mirror, tilt, kscale)),
                      f'execute positioned ~ {CY} ~ {BODY} run tp @e[tag={new}] ~ ~ ~ ~ 0', f'tag @e[tag={new}] remove {new}')
                tl.at(t0 + 1, X.merge(sel, X.crescent_tf(h1, SWING_R - 0.15, height, mirror, tilt, kscale), 2))
                q = X.crescent_q(h1, mirror, tilt)
                s = 2 * (SWING_R - 0.15) / 0.97 * kscale
                tl.at(t0 + 4, X.merge(sel, X.tf((0, height, 0), q, (-0.02 * s if mirror else 0.02 * s, 0.02 * s, 0.02 * s)), 3))
                tl.at(t0 + 7, f'kill {sel}')

    sweep(SW1, SWING_AT, SW1_Y, True, None, (1.0,), 'rlk_mb_gd_p4ca')
    sweep(SW2, SWING_AT, SW2_Y, False, SW2_TILT, (1.0, 0.78), 'rlk_mb_gd_p4cb')

    def ring_pts(r, y, n, tilt=None):
        out = []
        for i in range(n):
            a = 360 * i / n
            p = X.fwd(a, r)
            yy = y
            if tilt:
                yy = y - math.tan(math.radians(tilt[1])) * r * math.cos(math.radians(a - tilt[0]))
            out.append((p[0], yy, p[2]))
        return out

    for s, y, tilt, pitch in ((s1, SW1_Y, None, 0.7), (s2, SW2_Y, SW2_TILT, 0.65)):
        pts = ring_pts(4.6 * SW_K, y, 34, tilt)
        tl.at(s - 2, g.sound('item.trident.riptide_1', 0.4, 1.4 if s == s1 else 1.3),
              g.sound('entity.player.attack.knockback', 0.6, 0.6 if s == s1 else 0.55))
        tl.at(s, g.sound('entity.player.attack.sweep', 1.0, pitch), g.sound('item.trident.riptide_1', 0.3, 1.5),
              *[f'execute {BODY} run ' + g.dust(TRAIL_CORE, 1.3, P(*p), (0.05, 0.05, 0.05), 1) for p in pts],
              *[f'execute {BODY} run ' + g.particle('sweep_attack', P(*p), (0, 0, 0), 0, 1) for p in ring_pts(3.6 * SW_K, y, 7, tilt)])
        tl.at(s + 2, g.sound('entity.player.attack.sweep', 0.6, pitch + 0.15))
        for t in range(s + 3, s + 9):
            pts2 = [p for i, p in enumerate(ring_pts(rng.uniform(3.4, 5.0) * SW_K, y, 10, tilt)) if (i + t) % 2 == 0]
            tl.at(t, *[f'execute {BODY} run ' + g.particle('falling_dust{block_state:"minecraft:black_concrete"}', P(*p), (0.2, 0.1, 0.2), 0, 1) for p in pts2[:3]],
                  *[f'execute {BODY} run ' + g.particle('wax_on', P(*p), (0.3, 0.2, 0.3), 0, 1) for p in pts2[3:5]],
                  f'execute {BODY} run ' + g.dust(DARK, 0.9, P(0, y, 0), (3.0 * SW_K, 0.3, 3.0 * SW_K), 3))

    # recovery twirl (authored swing clip 39-51)
    for c in (42, 46):
        tl.at(SWING_AT + rt('swing', c), g.sound('item.trident.riptide_1', 0.35, 1.4), g.sound('entity.player.attack.sweep', 0.45, 0.7))
    tl.at(end, g.end())

    tick, start_extra = tl.emit([
        f'# P4 tick (@s = body, #gdPT = pull clip tick 0-{PULL_LEN}, then the swing clip from {SWING_AT}). Busy ticks run',
        f'# p/{k}/k/<t>; {W(28)}-{PULL_LEN - 1} only while #gp4Ok is 1 (line of sight at {W(27)}, pull at {RELOC}), the swings from {PULL_LEN + 1} while it',
        '# is 1 (pulled) or 2 (no line of sight / blocked destination: she swings in place).'])
    g.pw(k, 'start', [
        f'# P4 start (@s = body; from closer than 5 b the core first hopped back, ai/back): pull clip (aura 0, cage {cage0},',
        f'# relocate {RELOC}), voice line, hiss + charge.',
        'scoreboard players set #gp4Ok mb 0',
        g.rig('face/player'),
        g.play(k),
        g.voice_attack(),
        g.sound('block.fire.ambient', 1.0, 0.8),
        g.sound('block.respawn_anchor.charge', 0.7, 0.9)] + start_extra)
    g.pw(k, 'tick', tick)
    g.pw(k, 'los', [
        '# @s = body, at the body. #gp4Ok = 1 when nothing solid lies between her chest and the player\'s eyes',
        '# (0.5 b steps; blocks outside #rlk:cm_pass block it: the arena\'s light layer and barrier cap pass, the',
        '# floor and the wall ring do not; K14). No range limit: the arena is 42 b across and the pull is undodgeable.',
        'scoreboard players set #gp4Ok mb 0',
        'execute unless entity @e[tag=rlk_body,limit=1] run return 0',
        'function rlk:mboss/mv/dist',
        'scoreboard players operation #gp4Ln mb = #mbDist mb',
        'scoreboard players set #gp4K mb 5',
        'scoreboard players operation #gp4Ln mb /= #gp4K mb',
        'scoreboard players set #gp4Ok mb 1',
        f'execute positioned ~ ~2.2 ~ facing entity @e[tag=rlk_body,limit=1] eyes run {g.fn("p/pull/los_step")}'])
    g.pw(k, 'los_step', [
        '# One 0.5 b step of the line-of-sight ray (#gp4Ln steps left).',
        'execute unless block ~ ~ ~ #rlk:cm_pass run return run scoreboard players set #gp4Ok mb 0',
        'scoreboard players remove #gp4Ln mb 1',
        f'execute if score #gp4Ln mb matches 1.. positioned ^ ^ ^0.5 run {g.fn("p/pull/los_step")}'])
    g.pw(k, 'fizzle', [
        '# No line of sight at 27 (or the destination blocked at 32): the cage shatters at the player (red/black',
        '# shards, glass), the screen clears, no pull; #gp4Ok 2 = the swings still follow, in place (the pattern',
        '# resolves instead of vanishing).',
        'scoreboard players set #gp4Ok mb 2',
        'execute at @e[tag=rlk_body,limit=1] run ' + g.particle('block{block_state:"minecraft:black_concrete"}', '~ ~1 ~', (0.4, 0.8, 0.4), 0, 20),
        'execute at @e[tag=rlk_body,limit=1] run ' + g.particle('block{block_state:"minecraft:red_concrete"}', '~ ~1.2 ~', (0.5, 0.8, 0.5), 0, 14),
        'execute at @e[tag=rlk_body,limit=1] run ' + g.dust(CAGE_RED, 1.4, '~ ~1 ~', (0.5, 0.9, 0.5), 12),
        'execute at @e[tag=rlk_body,limit=1] run ' + g.sound('block.glass.break', 0.9, 0.6),
        'execute at @e[tag=rlk_body,limit=1] run ' + g.sound('block.chain.break', 0.7, 0.7),
        g.sound('entity.illusioner.mirror_move', 0.6, 0.5),
        'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4cage]',
        g.fn('p/pull/scr_end')])
    g.pw(k, 'reloc', [
        f'# @s = body, pull tick {RELOC}: the player 1 b in front of her (floor height, facing her; pull/start t 0 = at once).',
        '# Refused (dead, reviving, selection screen, map view) -> #gp4Ok 0 (the pattern ends at 40). Placed but not',
        '# moved (pull/finish found the destination blocked) -> fizzle, she swings in place.',
        f'execute store success score #gp4Ok mb {BODY} positioned ^ ^ ^1 positioned ~ {CY} ~ run function rlk:mboss/pull/start {{t:0}}',
        f'execute if score #gp4Ok mb matches 1 {BODY} positioned ^ ^ ^1 positioned ~ {CY} ~ unless entity @e[tag=rlk_body,distance=..0.6,limit=1] run return run {g.fn("p/pull/fizzle")}',
        f'execute unless score #gp4Ok mb matches 1 run return run {g.fn("p/pull/scr_end")}',
        f'scoreboard players set @a[tag=player] vBig {SCR_LAST - RELOC + 6}',
        f'title @a[tag=player] times 0 3 0',
        f'title @a[tag=player] title {SCREEN["frames"][SCR_FRAMES[RELOC]]}'])
    g.pw(k, 'scr_end', [
        '# Ends the screen overlay at once (fizzle, refused pull, pause, cancel): an empty title over it, the F5',
        '# crosshair title back (view/xhair) for a player on the seat.',
        'scoreboard players set @a[tag=player] vBig 0',
        'title @a[tag=player] times 0 1 2',
        'title @a[tag=player] title ""',
        'execute as @a[tag=player] if score #on view matches 1 if score #vmode view matches 2 if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/xhair'])
    S_RING = 2 * SWING_R / 0.86
    vis = [f'# hz_vis of the swing hazards (@s = marker at her feet; 41 swing 1, 42 swing 2): a gold ring decal at r {X.L.num(SWING_R)}',
           '# that turns (opposite ways for the two swings) until its strike.']
    for kk in (1, 2):
        vis.append(f'execute if score @s mbHzV matches {40 + kk} if score #hzEv mb matches 0 run summon minecraft:item_display ~ ~0.05 ~ '
                   f'{{{X.tags(*p4tags("rlk_mb_hzfx", f"rlk_mb_gd_p4r{kk}"))},billboard:"fixed",{X.BRIGHT},view_range:3f,shadow_radius:0f,'
                   f'teleport_duration:0,interpolation_duration:0,{X.tf((0, 0, 0), X.FLAT_UP, S_RING * 0.9)},'
                   f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{X.card_model("ring")}"}}}}}}')
        vis.append(f'execute if score @s mbHzV matches {40 + kk} if score #hzEv mb matches 1.. run kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p4r{kk}]')
    g.pw(k, 'vis', vis)
    g.pw(k, 'pause', [
        '# The fight froze (player dead or reviving; @s = body): the screen overlay goes now; the frames go on from',
        '# the clock after the resume.',
        g.fn('p/pull/scr_end')])
    g.pw(k, 'cancel', [
        '# P4 cancel (any executor): every entity of the pattern carries rlk_mb_gd_p4 (cage, cubes, crescents, ring',
        '# decals); the pull point and hazards go with lib_clear; the screen overlay ends if it runs.',
        f'kill @e[tag={P4TAG}]',
        f'execute if score #gdPT mb matches {SCR_FIRST}..{SCR_LAST} run {g.fn("p/pull/scr_end")}',
        'scoreboard players set #gp4Ok mb 0'])
