"""Cruise-form patterns C1-C6 of the field generator (실험성 역장 발생 장치), stage 2 (the cruise-pattern author).

    1 bomb     C1 중력 시스템·일점 상쇄 (폭격) + the slam finisher   melee / mid / far x2
    2 slam     C2 내려찍기                                         melee x2 / mid
    3 laser    C3 중력 시스템·코어 (레이저 빔)                       mid only
    4 missile  C4 중력 시스템·바위 폭탄 (미사일)                     far x3 only
    5 burst    C5 중력 시스템·지면 충격 (중력 폭발)                   mid only
    6 rock     C6 중력 시스템·파쇄 (바위 날리기, the tower)          melee / mid x2 / far
    (the fix round's balance bands, scratchpad plan.md "Fix round": C3 / C5 left the melee band, C1 / C6 joined it;
    every cruise pattern recovers 12 t, was 20)

Faithful to the scratchpad specs mb3/spec/C1_bomb_run.md .. C6_rock_tower.md and plan.md (its "Stage-2 decisions":
every recommended answer of spec/README.md section 5 is accepted):
- telegraphs: every damaging hit is a framework hazard made quiet and silent (#hzQuiet 1, #hzSfx 0) and paired in the
  same tick with the kit's ground decal of the same shape and tell (fx/tele/*), at least 10 t before its strike; the
  slab throws are blade projectiles behind a dmg-0 throw line + kit lane 10 t ahead;
- shapes, volley groups (every member made before the group's first strike: review FW-4), caps, knockback, Geo
  (the registry element) and the api.DMG coefficients of each spec's section 5; the framework options: hz/aim every
  tick and #hzRearm 10 for the C3 beams (one group), hz/resize for their bloom;
- fx and sound: the kit's presets and recipes on the specs' events (fg_fx_api.md sections 6 / 7) plus the specs' single
  vanilla layers; no layer that a recipe already plays 1-2 t away (review FX-4);
- AI: the bands and weights of spec/README.md section 2 (the core's bag), the facing / tracking spans and the aim locks
  of each spec's section 2 (C1 route + finisher re-lock, C2 lock, C4 late lock per missile, C6 arc point per burst and
  feet per throw), the body clamps (lockb / clamp_body r 16.5 for points the body moves to, lockp / clamp_walk r 20.3
  for ground targets);
- the butterfly review's bug classes: every marker a pattern summons is killed before its summon and at its end (kept
  ones through g.keep, which the core kills at p/finish / p/cancel: S1), g.release only in C5 (it never stops the AI:
  S2), the decals of the live hazards are redrawn on the first tick after a pause (FX-1: api.c_redraw; C3 its moving
  lanes), the kit's card caps (64 fx / 40 telegraph cards) hold for every pattern.

Clock: #fgPT = the clip tick of the pattern's clip (the core plays it at 0). Every rig event is read with ev_or from
the rig manifest (the real rig since the integration; the ev_or defaults are the old stub's numbers and never apply
now: the build prints a note for any default it uses), anchors with api.c_anchor (the manifest's clip anchors; the
defaults are the specs' body-frame points). Pattern scores #fq<id>*, tags
rlk_mb_fg_p<id>* + rlk_mb_fg_pat. Deviations: scratchpad mb3/fg_contract.md section 16.
"""
import math

from . import api as A
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, NS, L

BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'
TELL = 10                                                       # the telegraph floor of plan.md


def mk(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


def kill_mk(*tags):
    return [f'kill @e[type=minecraft:marker,tag={t}]' for t in tags]


def span(lo, hi, cmd):
    """An extra_tick line: cmd on every pattern clock lo..hi (extra_tick runs from clock 1; clock 0 is start)."""
    return f'execute if score #fgPT mb matches {lo}..{hi} run {cmd}'


def at_body(h, cmd, rot='~ 0'):
    """cmd at the body's axis h b up, rotated as the body (yaw)."""
    return f'execute at @s rotated as @s rotated {rot} positioned ~ ~{L.num(h, 3)} ~ run {cmd}'


def at_floor(cmd):
    return f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run {cmd}'


def pause_lines(pid):
    """p/<key>/pause: the core cleared every kit decal (fx/tele/clear); the next pattern tick redraws them."""
    return [f'# The fight froze (@s = body): the core cleared the kit decals; the first tick after the resume redraws',
            f'# those of the live hazards (#fq{pid}Pz, review FX-1).',
            f'scoreboard players set #fq{pid}Pz mb 1']


def resume_lines(g, key, pid, extra=()):
    """The first extra_tick line of a pattern: after a pause, redraw its decals once."""
    g.pw(key, 'resume', [f'# First tick after a pause (@s = body): the kit decals of the live hazards again.',
                         f'scoreboard players set #fq{pid}Pz mb 0'] + list(extra))
    return f'execute if score #fq{pid}Pz mb matches 1 run function {NS}p/{key}/resume'


# =============================================================================================
# Clip events (the manifest's; stub defaults) and the derived ticks
# C1 (bomb_run, then slam at the end of bomb_run): ports 10, run 12; 20 bombs every 2.25 t; finisher slam
C1_PORTS = ev_or('bomb_run', 'ports', 10)
C1_RUN = ev_or('bomb_run', 'run', 12)
C1_GLIDE = 45                                                   # the run: 45 t, <= 0.55 b/t (24.75 b)
C1_SPEED = 0.55
C1_BOMBS = [C1_RUN + (9 * k) // 4 for k in range(20)]          # drop ticks, 2.25 t apart
C1_FALL = 6                                                    # a bomb falls 6 t onto its decal
C1_LEAD = 4                                                    # decal 4 t before the drop: tell 10
# The bombs leave the rig's front ports (fix round FID-2): port_0 (left) and port_7 (right) of the manifest's bomb_run
# `drop` anchors (rig x left, y up, -z forward: 1.048 b to the side, 2.253 b ahead of the axis, 3.483 b up in the
# 16-degree nose-down pose) and the point between them for the centre bomb.
C1_PORT_L = A.c_anchor('bomb_run', 'drop', 'port_0', (1.048, 3.483, -2.253))
C1_PORT_R = A.c_anchor('bomb_run', 'drop', 'port_7', (-1.048, 3.483, -2.253))
C1_SIDE = (round(C1_PORT_L[0], 3), round(C1_PORT_R[0], 3), 0.0)  # L, R, C (body frame ^x = left)
C1_FWD = round(-(C1_PORT_L[2] + C1_PORT_R[2]) / 2, 3)          # ahead of the body axis (^z)
C1_PORT_H = round((C1_PORT_L[1] + C1_PORT_R[1]) / 2, 3)        # the bomb starts this high above its decal
C1_GLOW = [A.c_anchor('bomb_run', 'ports', f'port_{i}', None) for i in range(8)] if A.c_clip('bomb_run', 'anchors') else []
C1_GLOW_LIFE = C1_RUN - C1_PORTS + 2                           # the port glows: 2 t, gone 2 t into the run glide
C1_SLAM = clip_len('bomb_run')                                # the finisher's slam clip starts here
C1_SLAM_T = ev_or('slam', 'impact', 16)                        # its tell (the clip's impact)
C1_SLAM_HIT = C1_SLAM + C1_SLAM_T
C1_PLUNGE = C1_SLAM + ev_or('slam', 'plunge', 13)
C1_RISE = C1_SLAM + ev_or('slam', 'rise', 23)
C1_DST = 6.0                                                    # the finisher glides at most 6 b toward the re-lock
C1_DST_T = 10
C1_END = C1_SLAM + clip_len('slam')                            # spec F2: the slam clip plays out
assert C1_LEAD + C1_FALL >= TELL and C1_BOMBS[-1] + C1_FALL < C1_SLAM_HIT and C1_DST_T < C1_SLAM_T
# C2 (slam): column 0, plunge 13, impact 16 (stub 17), rise 23
C2_HIT = ev_or('slam', 'impact', 16)
C2_PLUNGE = ev_or('slam', 'plunge', 13)
C2_RISE = ev_or('slam', 'rise', 23)
C2_LEN = clip_len('slam')
assert C2_HIT >= TELL
# C3 (laser): drop 0, charge 4, aim 23, fire 25, off 158, retract 159; the orbit of the rig (manifest 'orbit')
C3_DROP = ev_or('laser', 'drop', 0)
C3_CHARGE = ev_or('laser', 'charge', 4)
C3_FIRE = ev_or('laser', 'fire', 25)
C3_AIM = ev_or('laser', 'aim', C3_FIRE - 2)
C3_OFF = ev_or('laser', 'off', 158)
C3_RETRACT = ev_or('laser', 'retract', C3_OFF + 1)
C3_ACT = C3_OFF - C3_FIRE                                      # active fire .. off - 1 (133 t)
C3_LEN = clip_len('laser')
_ORB = A.c_clip('laser', 'orbit', {}) or {}
C3_ORB_FROM = int(_ORB.get('from', C3_FIRE))
C3_ORB_TO = int(_ORB.get('to', C3_OFF))
C3_RATE = float(_ORB.get('rate', 5))
C3_AZ = {'e': float((_ORB.get('medal_eye') or {}).get('az0', 90)), 'g': float((_ORB.get('medal_gear') or {}).get('az0', -90))}
C3_SENSE = {'e': int((_ORB.get('medal_eye') or {}).get('sense', -1)), 'g': int((_ORB.get('medal_gear') or {}).get('sense', 1))}
C3_YAW0 = {b: -C3_AZ[b] for b in 'eg'}                          # yaw = body yaw - azimuth (azimuth: front toward the left)
C3_DYAW = {b: -C3_SENSE[b] * C3_RATE for b in 'eg'}              # yaw change per tick (+ = clockwise from above)
C3_BEAM_LEN = float((_ORB.get('beam') or {}).get('length', 3.74))
C3_SPOT_R = float((_ORB.get('beam') or {}).get('spot_r', 5.58))
_MED = A.c_anchor('laser', 'charge', 'medal_e', (2.93, 2.38, 0.0))
C3_MUZ_R, C3_MUZ_H = math.hypot(_MED[0], _MED[2]), _MED[1]       # the muzzle: r 2.93, 2.38 b up (spec section 4)
C3_PITCH = round(math.degrees(math.atan2(C3_MUZ_H - 0.05, C3_SPOT_R - C3_MUZ_R)))   # the beam's slope down (42)
C3_R0, C3_LLEN = 3.0, 2.8                                      # the hit band r 3.0 .. 5.8 (spec F3)
C3_W_BLOOM, C3_W, C3_W_LANE = 1.0, 0.6, 0.6                    # width 1.0 for 3 t at fire, then 0.6 (spec F2)
C3_BLOOM_T = 3
C3_TURN0 = max(1, C3_ORB_FROM + 1)                              # first re-aimed clock
C3_TURN1 = min(C3_OFF - 1, C3_ORB_TO)                           # last re-aimed clock


def c3_yaw(b, t):
    """The beam's yaw offset from the body at clock t (degrees)."""
    return C3_YAW0[b] + C3_DYAW[b] * max(0, min(t, C3_ORB_TO) - C3_ORB_FROM)


C3_MEETS = [t for t in range(C3_FIRE, C3_OFF) if abs(((c3_yaw('e', t) - c3_yaw('g', t)) + 180) % 360 - 180) < 1e-6]
assert C3_FIRE >= TELL and 0 < C3_ACT and C3_MEETS, C3_MEETS
# C4 (missiles): flare 0, vent 8, launch 22 .. last 35; flight 28 t (rise 14, lock at +14 = tell 14, dive 13)
C4_FLARE = ev_or('missiles', 'flare', 0)
C4_VENT = ev_or('missiles', 'vent', 8)
C4_LAUNCH = ev_or('missiles', 'launch', 22)
C4_LAST = ev_or('missiles', 'last', C4_LAUNCH + 13)
C4_N = 10
C4_T = [C4_LAUNCH + round(i * (C4_LAST - C4_LAUNCH) / (C4_N - 1)) for i in range(C4_N)]
C4_UP, C4_APEX, C4_LOCK, C4_HIT = 7, 8, 14, 28                  # missile clock: up 7 b (1-8), to the apex (8-14), lock, impact
C4_IMPACTS = [t + C4_HIT for t in C4_T]
C4_GROUPS = (range(0, 5), range(5, 10))
C4_END = max(clip_len('missiles'), C4_IMPACTS[-1] + 1)
C4_VENT_L = A.c_anchor('missiles', 'launch', 'vent_l', (2.81, 5.0, 1.16))
C4_VENT_R = A.c_anchor('missiles', 'launch', 'vent_r', (-2.81, 5.0, -1.16))
C4_TIP_L = A.c_anchor('missiles', 'flare', 'spike_tip_l', (5.33, 4.55, 0.0))
C4_TIP_R = A.c_anchor('missiles', 'flare', 'spike_tip_r', (-5.33, 4.55, 0.0))
C4_HUB = 5.2
assert all(C4_T[max(g)] + C4_LOCK < C4_T[min(g)] + C4_HIT for g in C4_GROUPS), 'FW-4: a group is complete before it strikes'
assert C4_HIT - C4_LOCK >= TELL
# C5 (coreup): spark 0, eye 1, rim 3, lift 5, up 16, beam 29, column 41, blast 48, sink 81
C5_SPARK = ev_or('coreup', 'spark', 0)
C5_EYE = ev_or('coreup', 'eye', 1)
C5_RIM = ev_or('coreup', 'rim', 3)
C5_LIFT = ev_or('coreup', 'lift', 5)
C5_UP = ev_or('coreup', 'up', 16)
C5_BEAM = ev_or('coreup', 'beam', 29)
C5_COLUMN = ev_or('coreup', 'column', 41)
C5_BLAST = ev_or('coreup', 'blast', 48)
C5_SINK = ev_or('coreup', 'sink', 81)
C5_LEN = clip_len('coreup')
C5_R = 12.0                                                    # R = 1.7 D (D 7.0); unclamped (spec F1 / Q12)
C5_CORE = A.c_anchor('coreup', 'spark', 'core', (0.0, 4.5, 0.0))[1]
C5_CORE_UP = A.c_anchor('coreup', 'beam', 'core', (0.0, 7.76, 0.0))[1]
assert C5_BLAST - C5_RIM >= TELL and C5_RIM < C5_LIFT < C5_BEAM < C5_COLUMN < C5_BLAST < C5_SINK < C5_LEN
# C6 (tower_throw): dip 0, vent 12, tower 20, band 38, bursts 55 + 6k, throws 95 + 8j, revert 142
C6_DIP = ev_or('tower_throw', 'dip', 0)
C6_VENT = ev_or('tower_throw', 'vent', 12)
C6_TOWER = ev_or('tower_throw', 'tower', 20)
C6_BAND = ev_or('tower_throw', 'band', 38)
C6_BURST = ev_or('tower_throw', 'burst', 55)
C6_THROW = ev_or('tower_throw', 'throw', 95)
C6_REVERT = ev_or('tower_throw', 'revert', 142)
C6_BURSTS = [int(t) for t in (A.c_clip('tower_throw', 'bursts') or [C6_BURST + 6 * k for k in range(8)])]
C6_THROWS = [int(t) for t in (A.c_clip('tower_throw', 'throws') or [C6_THROW + 8 * j for j in range(5)])]
C6_LEN = clip_len('tower_throw')
C6_END = max(C6_LEN, C6_THROWS[-1] + 26)                        # the last slab has landed (life 24 at 1.5 b/t)
C6_DIP_T, C6_DIP_STEP, C6_DIP_MIN = 11, 0.2, 5.0                # the dip glide toward a player >= 5 b away (spec F4)

# Bands and recovery after the fix round's balance runs (scratchpad mb3/fgfix/sim, plan.md "Fix round"): a melee player
# stands under C3's medallions (r < 2.7: out of the beam band) and jumps C5's blast, so in the melee band those two were
# free time; they are now the mid band's (4-8 b), and the melee band takes the bomb run and the rock throw (the spec's
# bands were C1 mid / far, C3 and C5 melee / mid, C6 mid / far). The bag still deals each pattern of a band once per
# cycle. Every cruise pattern recovers 12 t (was 20).
CRU_RECOVER = 12
PATTERNS = [
    Pattern(1, 'bomb', '중력 시스템·일점 상쇄', 'c', 'bomb_run', bands=('melee', 'mid', 'far'), weight={'far': 2},
            recover=CRU_RECOVER, max_len=C1_END + 7, length=C1_END),
    Pattern(2, 'slam', '내려찍기', 'c', 'slam', bands=('melee', 'mid'), weight={'melee': 2},
            recover=CRU_RECOVER, max_len=C2_LEN + 7, length=C2_LEN),
    Pattern(3, 'laser', '중력 시스템·코어', 'c', 'laser', bands=('mid',), weight={'mid': 2},
            recover=CRU_RECOVER, max_len=C3_LEN + 6, length=C3_LEN),
    Pattern(4, 'missile', '중력 시스템·바위 폭탄', 'c', 'missiles', bands=('far',), weight={'far': 3},
            recover=CRU_RECOVER, max_len=C4_END + 8, length=C4_END),
    Pattern(5, 'burst', '중력 시스템·지면 충격', 'c', 'coreup', bands=('mid',),
            recover=CRU_RECOVER, max_len=C5_LEN + 8, length=C5_LEN),
    Pattern(6, 'rock', '중력 시스템·파쇄', 'c', 'tower_throw', bands=('melee', 'mid', 'far'), weight={'mid': 2},
            recover=CRU_RECOVER, max_len=C6_END + 8, length=C6_END),
]


def emit(g):
    bomb(g)
    slam(g)
    laser(g)
    missile(g)
    burst(g)
    rock(g)


def slam_vis(g, vid):
    """The slam strike (C1 finisher, C2), as the hazard marker on #hzEv 1."""
    return [f'execute if score @s mbHzV matches {vid} at @s rotated ~ 0 run {g.fx("slam")}',
            f'execute if score @s mbHzV matches {vid} at @s rotated ~ 0 run {g.fx("dust_puff")}',
            f'execute if score @s mbHzV matches {vid} at @s run {g.snd("slam")}']


# ---------------------------------------------------------------------------------------------
def bomb(g):
    """C1 일점 상쇄 (spec C1): the route is locked at 0 through the player's feet (24.75 b = 45 t x 0.55 b/t, its end
    pulled back along the line into r 16.5); the device tracks 0-9, snaps onto the route at the ports (10) and glides
    it from the run (12); a predictor marker glides the same route 4 t ahead, so each bomb's decal (hz/disc r 1.3,
    tell 10, quiet, with the kit tele_disc) is made at the predictor 4 t before its drop, exactly under its port (the
    rig's front ports port_0 / port_7: 1.05 b to each side and 2.25 b ahead of the axis, the centre bomb between them;
    fix round FID-2), and the kit bomb falls 6 t from the port onto it; 20 bombs every 2.25 t in volley groups
    of 4 (light KB, 0.8). The finisher (spec F1, Q4): at the end of bomb_run the player is locked again (lockb), the
    device glides up to 6 b toward the lock in 10 t, and the slam clip plays: decal r 5 at the destination from its
    start, strike at the clip's impact (r 5, feet up to 2.0 b, heavy KB, 1.4). The pattern ends with the slam clip
    (spec F2)."""
    key, tl = 'bomb', TL(g, 'bomb')
    P, E, F, D = 'rlk_mb_fg_p1p', 'rlk_mb_fg_p1e', 'rlk_mb_fg_p1f', 'rlk_mb_fg_p1d'
    pred, end, dst = mk(P), mk(E), mk(D)
    tags = '"rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1"'
    g.pw(key, 'route', [
        '# @s = body, at it, rotated toward the player\'s feet (pitch 0): the route end E (24.75 b along the line, pulled',
        '# back along it into r 16.5) and the predictor P at the body with the route yaw. Older markers go first.',
        *kill_mk(P, E, D),
        f'summon minecraft:marker ~ ~ ~ {{Tags:[{tags},"{P}"]}}',
        f'tp {pred} ~ ~ ~ ~ 0',
        f'execute positioned ^ ^ ^{L.num(C1_SPEED * C1_GLIDE)} run summon minecraft:marker ~ ~ ~ {{Tags:[{tags},"{E}"]}}',
        f'execute as {end} at @s facing entity {pred} feet run tp @s ~ ~ ~ ~ 0',
        'scoreboard players set #fq1N mb 0',
        f'execute as {end} at @s run function {NS}p/{key}/pull'])
    g.pw(key, 'pull', [
        '# @s = the route end (facing back to the start): 0.5 b steps back until inside the body disc r 16.5.',
        f'execute positioned ~ {CY} ~ if entity @e[tag=rlk_mb_arena,distance=..{L.num(A.BODY_R)},limit=1] run return 0',
        'scoreboard players add #fq1N mb 1',
        'execute if score #fq1N mb matches 60.. run return 0',
        'execute at @s rotated as @s run tp @s ^ ^ ^0.5',
        f'execute at @s run function {NS}p/{key}/pull'])
    steps = int(C1_DST / 0.5)
    g.pw(key, 'dst', [
        f'# @s = body, at it: the finisher destination D at most {L.num(C1_DST)} b from the body toward the re-lock F',
        f'# ({F}): 0.5 b steps toward F while it is farther than 0.5 b, the rest of the way when closer; then inside r 16.5.',
        *kill_mk(D),
        f'summon minecraft:marker ~ {CY} ~ {{Tags:[{tags},"{D}"]}}']
        + [f'execute as {dst} at @s if entity @e[type=minecraft:marker,tag={F},distance=0.5..,limit=1] facing entity '
           f'{mk(F)} feet rotated ~ 0 run tp @s ^ ^ ^0.5' for _ in range(steps)]
        + [f'execute as {dst} at @s if entity @e[type=minecraft:marker,tag={F},distance=..0.5,limit=1] run tp @s {mk(F)}',
           f'execute as {dst} run {g.clamp_body()}'])
    # 0: the route lock, the turn cue; 0-9 tracking (the rig turns the anchor <= 4 deg/t); 10 the snap onto the route
    tl.at(0, f'execute at @s facing entity {PLAYER} feet rotated ~ 0 run function {NS}p/{key}/route',
          g.rig('face/track'), g.sound('entity.breeze.whirl', 0.5, 0.9))
    # the ports light up (+10): the kit's port dust under the ring and a glow on each of the rig's 8 ports (the manifest's
    # bomb_run `ports` anchors, the nose-down pose: fix round FID-3). The cards stand still, so they flash only while the
    # device does (plan C1 "ports glow 2 t") and fade over the first 2 t of the run glide; the rig's charge look keeps
    # the real ports lit (verification round: with life 14 they trailed the gliding ports by up to 2.9 b)
    tl.at(C1_PORTS, f'execute at @s facing entity {end} feet run tp @s ~ ~ ~ ~ 0',
          at_body(4.5, g.fx('ports_glow')), at_body(4.5, g.snd('bomb_port')),
          *[f'execute at @s rotated as @s rotated ~ 0 positioned {A.c_bf(pt)} run '
            + g.kcard('glow', bb='center', s0=0.3, s1=0.75, life=C1_GLOW_LIFE, fade=2, col='#E1BC7E') for pt in C1_GLOW])
    tl.at(C1_RUN - C1_LEAD, f'execute as {pred} positioned as {end} run function rlk:mboss/mv/glide {{t:{C1_GLIDE}}}')
    tl.at(C1_RUN, f'execute positioned as {end} run function rlk:mboss/mv/glide {{t:{C1_GLIDE}}}',
          g.sound('entity.breeze.charge', 0.6, 0.6))
    for k, d in enumerate(C1_BOMBS):
        x, f = L.num(C1_SIDE[k % 3]), L.num(C1_FWD)
        pre = f'execute at {pred} rotated as {pred} rotated ~ 0 positioned ^{x} ^ ^{f} positioned ~ {CY} ~ run '
        lines = [g.GRP_NEW] if k % 4 == 0 else []
        lines += g.hz_opts(kb=KB['light'], grp=True, vis=11 if k % 2 == 0 else 13, quiet=1, sfx=0)
        lines += [pre + g.hz_disc(1.3, C1_LEAD + C1_FALL, DMG['c1']), pre + g.tele_disc(1.3, C1_LEAD + C1_FALL)]
        tl.at(d - C1_LEAD, *lines)
        drop = f'execute at @s rotated as {pred} rotated ~ 0 positioned ^{x} ^ ^{f} positioned ~ {CY} ~ run '
        tl.at(d, drop + g.fx('bomb_drop', h=C1_PORT_H), at_body(C1_PORT_H, g.snd('bomb_drop')),
              at_body(C1_PORT_H, g.snd('bomb_fall')) if k % 4 == 0 else None)
    # the finisher: re-lock, destination, the slam clip with its decal and hazard at the destination, the glide
    tl.at(C1_SLAM, g.play('slam'), g.lockb(), *g.keep(F), f'execute at @s run function {NS}p/{key}/dst',
          *g.hz_opts(kb=KB['heavy'], y1=2.0, vis=12, quiet=1, sfx=0),
          f'execute at {dst} positioned ~ {CY} ~ run ' + g.hz_disc(5.0, C1_SLAM_T, DMG['c1s']),
          f'execute at {dst} positioned ~ {CY} ~ rotated ~ 0 run ' + g.tele_disc(5.0, C1_SLAM_T),
          f'execute positioned as {dst} run function rlk:mboss/mv/glide {{t:{C1_DST_T}}}',
          at_body(4.5, g.snd('column_tell')))
    # the slam point: the kit's floor glow and base flare (the rig draws the gold column under the gliding device: FID-5)
    tl.at(C1_SLAM + 3, f'execute at {dst} positioned ~ {CY} ~ rotated ~ 0 run ' + g.fx('column_base'))
    tl.at(C1_SLAM + 6, at_body(4.5, g.sound('block.beacon.power_select', 0.5, 1.2)))
    tl.at(C1_PLUNGE, at_body(4.5, g.fx('plunge')), at_body(4.5, g.snd('plunge')))
    tl.at(C1_RISE, at_floor(g.fx('rise')), at_body(2.3, g.sound('block.piston.contract', 0.6, 0.8)),
          at_body(2.3, g.sound('entity.breeze.wind_burst', 0.4, 0.9)))
    tl.at(C1_END, *kill_mk(P, E, D), g.end())
    tl.write([f'# C1 일점 상쇄 (clip bomb_run, then slam at {C1_SLAM}; @s = body, at it): route locked at 0, bombs '
              f'{C1_BOMBS[0]}..{C1_BOMBS[-1]} (strikes +{C1_FALL}), the finisher re-lock and slam r 5 at {C1_SLAM_HIT}, end {C1_END}.',
              'scoreboard players set #fq1Pz mb 0'],
             ['# bomb tick.'],
             extra_tick=[resume_lines(g, key, 1, [A.c_redraw(g, key, 11, 13)]),
                         span(1, C1_PORTS - 1, g.rig('face/track'))])
    g.pw(key, 'vis', ['# @s = a C1 hazard (#hzEv 1 = its strike): 11 / 13 a bomb (11 with the burst sound: every 2nd bomb),',
                      '# 12 the finisher slam.',
                      'execute unless score #hzEv mb matches 1 run return 0',
                      'execute if score @s mbHzV matches 11 at @s rotated ~ 0 run ' + g.fx('bomb_burst'),
                      'execute if score @s mbHzV matches 11 at @s run ' + g.snd('bomb_burst'),
                      'execute if score @s mbHzV matches 13 at @s rotated ~ 0 run ' + g.fx('bomb_burst')]
         + slam_vis(g, 12))
    g.pw(key, 'pause', pause_lines(1))
    g.pw(key, 'cancel', ['# Everything of C1 (route markers, the destination; the kept re-lock goes with the core\'s p/cancel).',
                         'kill @e[tag=rlk_mb_fg_p1]', *kill_mk(F)])


# ---------------------------------------------------------------------------------------------
def slam(g):
    """C2 내려찍기 (spec C2): the nose turns to the player and the feet are locked at 0 (lockb: inside r 16.5, kept),
    the device glides onto the lock in 10 t while the rig's gold column falls under it (the kit marks the lock with a
    floor glow and a base flare, column_base: fix round FID-5); the decal r 5 is at the lock from 0 and the
    slam strikes at the clip's impact (r 5, feet up to 2.0 b, heavy KB, 1.4). The dash is the answer."""
    key, tl = 'slam', TL(g, 'slam')
    A2 = 'rlk_mb_fg_p2a'
    sel = mk(A2)
    tl.at(0, g.rig('face/player'), g.lockb(), *g.keep(A2), f'tag {sel} add rlk_mb_fg_pat',
          *g.hz_opts(kb=KB['heavy'], y1=2.0, vis=21, quiet=1, sfx=0),
          f'execute at {sel} positioned ~ {CY} ~ run ' + g.hz_disc(5.0, C2_HIT, DMG['c2']),
          f'execute at {sel} positioned ~ {CY} ~ rotated ~ 0 run ' + g.tele_disc(5.0, C2_HIT),
          f'execute positioned as {sel} run function rlk:mboss/mv/glide {{t:10}}',
          at_body(4.5, g.snd('column_tell')))
    tl.at(3, f'execute at {sel} positioned ~ {CY} ~ rotated ~ 0 run ' + g.fx('column_base'))       # FID-5
    tl.at(8, at_body(4.5, g.sound('block.beacon.power_select', 0.5, 1.2)))
    tl.at(C2_PLUNGE, at_body(4.5, g.fx('plunge')), at_body(4.5, g.snd('plunge')))
    tl.at(C2_RISE, at_floor(g.fx('rise')), at_body(2.3, g.sound('block.piston.contract', 0.6, 0.8)),
          at_body(2.3, g.sound('entity.breeze.wind_burst', 0.4, 0.9)))
    tl.at(C2_LEN, f'kill {sel}', g.end())
    tl.write([f'# C2 내려찍기 (clip slam; @s = body): face, lock + glide 10 t, slam r 5 at {C2_HIT}.',
              'scoreboard players set #fq2Pz mb 0'],
             ['# slam tick.'], extra_tick=[resume_lines(g, key, 2, [A.c_redraw(g, key, 21, 21)])])
    g.pw(key, 'vis', ['# @s = the slam hazard (#hzEv 1 = the impact).', 'execute unless score #hzEv mb matches 1 run return 0']
         + slam_vis(g, 21))
    g.pw(key, 'pause', pause_lines(2))
    g.pw(key, 'cancel', ['# The locked point.', f'kill @e[type=minecraft:marker,tag={A2}]'])


# ---------------------------------------------------------------------------------------------
def laser(g):
    """C3 코어 (spec C3): the medallions drop beside the core (0-4) and charge (4-23); two beam hazards are made at 0
    (hz/line from r 3.0, length 2.8: the band r 3.0-5.8 on the floor; feet -0.5..2.0 b; light KB; one volley group,
    re-armed every 10 t: at most one 0.5 hit per 10 t from both), tell = the clip's fire, active until its off; their
    start yaws and turn rates come from the rig's orbit (the eye medallion at the device's left turning +5 deg/t, the
    gear at its right -5 deg/t: they meet in front 18 t after the fire and behind 36 t later, Q5 / F1). Every tick of
    the orbit both hazards are re-aimed (hz/aim) and their kit lanes (tele_mline, r 3.0-5.8) follow. Width 1.0 for the
    3 t bloom at the fire, then 0.6 (F2). The body never turns (F4). Safe: r < 2.7 under the medallions, r > 6.1."""
    key, tl = 'laser', TL(g, 'laser')
    HZ = {'e': 'rlk_mb_fg_p3e', 'g': 'rlk_mb_fg_p3g'}
    LANE = {'e': 0, 'g': 1}
    hz = {b: mk(HZ[b]) for b in 'eg'}

    def opts():
        return g.hz_opts(act=C3_ACT, y0=-0.5, y1=2.0, kb=KB['light'], grp=True, rearm=10, sfx=0, quiet=1, vis=31)

    def beam_at(b, pos, cmd, pitch=None):
        """cmd at a point of beam b's frame (at the body, rotated as its hazard marker), optionally pitched."""
        rot = '' if pitch is None else f' rotated ~ {pitch}'
        return f'execute as {hz[b]} at {BODY} rotated as @s rotated ~ 0 positioned {pos}{rot} run {cmd}'

    muz = f'^ ^{L.num(C3_MUZ_H, 3)} ^{L.num(C3_MUZ_R, 3)}'
    spot = f'^ ^0.05 ^{L.num(C3_SPOT_R, 3)}'
    start = [g.GRP_NEW, *kill_mk(HZ['e'], HZ['g'])]
    for b in 'eg':
        start += [*opts(),
                  f'execute at @s rotated as @s rotated ~{L.num(C3_YAW0[b])} 0 positioned ^ ^ ^{L.num(C3_R0)} run '
                  + g.hz_line(C3_LLEN, C3_W, C3_FIRE, DMG['c3']),
                  g.tag_last_hz(HZ[b]),
                  f'execute at @s rotated as @s rotated ~{L.num(C3_YAW0[b])} 0 positioned ~ {CY} ~ run '
                  + g.tele_mline(LANE[b], C3_R0 + C3_LLEN, C3_W_LANE, C3_FIRE, hold=C3_ACT, back=-C3_R0)]
    tl.at(0, *start, at_body(4.5, g.snd('pods_drop')))
    tl.at(C3_DROP + 3, *[beam_at(b, muz, g.fx('pods_drop')) for b in 'eg'])
    for t in range(C3_CHARGE, C3_AIM, 5):
        tl.at(t, *[beam_at(b, muz, g.fx('laser_charge')) for b in 'eg'])
    tl.at(C3_CHARGE, at_body(4.5, g.snd('laser_charge')))
    tl.at(C3_CHARGE + 10, at_body(4.5, g.sound('block.amethyst_block.chime', 0.4, 1.8)))
    tl.at(C3_AIM, *[beam_at(b, muz, g.fx('aim_line', len=C3_BEAM_LEN), C3_PITCH) for b in 'eg'],
          at_body(4.5, g.sound('block.respawn_anchor.charge', 0.5, 1.9)))
    fire = [*[beam_at(b, muz, g.fx('laser_fire', len=C3_BEAM_LEN), C3_PITCH) for b in 'eg'],
            *[beam_at(b, spot, g.fx('laser_spot')) for b in 'eg'],
            at_body(4.5, g.snd('laser_fire'))]
    fire += [f'execute as {hz[b]} run ' + g.hz_resize(C3_LLEN, 0, C3_W_BLOOM) for b in 'eg']
    tl.at(C3_FIRE, *fire)
    tl.at(C3_FIRE + C3_BLOOM_T, *[f'execute as {hz[b]} run ' + g.hz_resize(C3_LLEN, 0, C3_W) for b in 'eg'])
    for i, t in enumerate(range(C3_FIRE, C3_OFF, 10)):
        b = 'e' if i % 2 == 0 else 'g'
        tl.at(t, beam_at(b, spot, g.snd('laser_loop')))
    for t in C3_MEETS:
        tl.at(t, beam_at('e', spot, g.fx('spark')), beam_at('e', spot, g.sound('block.amethyst_block.resonate', 0.4, 1.6)))
    off = [*[beam_at(b, muz, g.fx('laser_end'), C3_PITCH) for b in 'eg'],
           g.tele_mline_end(0), g.tele_mline_end(1), at_body(4.5, g.snd('laser_stop')),
           *kill_mk(HZ['e'], HZ['g'])]
    tl.at(C3_OFF, *off)
    tl.at(C3_RETRACT + 7, at_body(4.5, g.sound('block.piston.contract', 0.6, 0.9)))
    tl.at(C3_LEN, *kill_mk(HZ['e'], HZ['g']), g.end())
    # every orbit tick: re-aim both hazards (hz/aim, before hz/all), their lanes after them, the floor spots every 3 t
    aim = [f'# Clock {C3_TURN0}..{C3_TURN1} (@s = body): the eye beam turns {L.num(C3_DYAW["e"])}, the gear beam {L.num(C3_DYAW["g"])}',
           '# degrees (the rig orbit); hz/aim from the body at r 3.0 along the new yaw; the lanes follow; spots every 3 t.']
    for b in 'eg':
        aim += [f'execute as {hz[b]} at {BODY} rotated as @s rotated ~{L.num(C3_DYAW[b])} 0 positioned ^ ^ ^{L.num(C3_R0)} '
                f'run function rlk:mboss/hz/aim',
                f'execute as {hz[b]} rotated as @s run ' + g.tele_mline_aim(LANE[b])]
    aim += ['scoreboard players operation #fgM mb = #fgPT mb', 'scoreboard players operation #fgM mb %= #fgK3 mb']
    aim += [f'execute if score #fgM mb matches {C3_FIRE % 3} run ' + beam_at(b, spot, g.fx('laser_spot')) for b in 'eg']
    g.pw(key, 'aim', aim)
    # after a pause: the moving lanes again (tell = the ticks to the fire, or 1 while firing; held to the off)
    relane = ['# The lanes again after a pause (@s = body): tell = the ticks left to the fire (1 while firing), hold to the off.',
              f'execute if score #fgPT mb matches {C3_OFF}.. run return 0',
              f'scoreboard players set #fgX mb {C3_FIRE}', 'scoreboard players operation #fgX mb -= #fgPT mb',
              'execute if score #fgX mb matches ..0 run scoreboard players set #fgX mb 1',
              'execute store result storage rlk:mboss fg.ln.tell int 1 run scoreboard players get #fgX mb',
              f'scoreboard players set #fgM mb {C3_OFF}', 'scoreboard players operation #fgM mb -= #fgPT mb',
              'scoreboard players operation #fgM mb -= #fgX mb',
              'execute store result storage rlk:mboss fg.ln.hold int 1 run scoreboard players get #fgM mb',
              f'data modify storage rlk:mboss fg.ln merge value {{len:{int(round((C3_R0 + C3_LLEN) * 10))},'
              f'w:{int(round(C3_W_LANE * 10))},back:{-int(round(C3_R0 * 10))},el:5}}']
    for b in 'eg':
        relane += [f'data modify storage rlk:mboss fg.ln.id set value {LANE[b]}',
                   g.tele_mline_end(LANE[b]),
                   f'execute as {hz[b]} at {BODY} rotated as @s rotated ~ 0 positioned ~ {CY} ~ run '
                   f'function {A.K.FN}tele/mline with storage rlk:mboss fg.ln']
    g.pw(key, 'relane', relane)
    tl.write([f'# C3 코어 (clip laser; @s = body; the yaw never changes): two beams made at 0 (tell {C3_FIRE}), active '
              f'{C3_ACT} t, the rig orbit {L.num(C3_DYAW["e"])} / {L.num(C3_DYAW["g"])} deg/t from {C3_ORB_FROM}; meets {C3_MEETS}.',
              'scoreboard players set #fq3Pz mb 0'],
             ['# laser tick.'],
             extra_tick=[resume_lines(g, key, 3, [f'function {NS}p/{key}/relane']),
                         span(C3_TURN0, C3_TURN1, f'function {NS}p/{key}/aim')])
    g.pw(key, 'vis', ['# @s = a beam hazard (#hzEv 1 = the fire): the beams and their floor spots are drawn by the rig and the',
                      '# aim function; nothing more here.'])
    g.pw(key, 'pause', pause_lines(3))
    g.pw(key, 'cancel', ['# Both beams and their lanes (the rig draws the beams themselves).', *kill_mk(HZ['e'], HZ['g']),
                         g.tele_mline_end(0), g.tele_mline_end(1), 'kill @e[tag=rlk_mb_fg_p3]'])


# ---------------------------------------------------------------------------------------------
def missile(g):
    """C4 바위 폭탄 (spec C4, Q6): far band only. The spike tips flare (0) and the vent shaft rises (8); 10 drill missiles
    (kit prop missile) leave the vents at the launch .. last events (L_i), alternately left / right. Each one rises 7 b
    (1-8), arcs to its apex (8-14: half way to the player, 16 b up, 3 b off to the side away from its vent: the crossing
    arcs), locks the player's feet at +14 (the late lock = the weak homing: lockp, kept as rlk_mb_fg_p4t<i>; hz/disc
    r 1.5, tell 14, quiet, with the kit decal), turns onto it and dives 13 t: the impact at +28. Two volley groups
    (missiles 1-5, 6-10): at most 2 hits (0.9 each). Keep walking."""
    key, tl = 'missile', TL(g, 'missile')
    M = 'rlk_mb_fg_p4m'
    APEX = 'rlk_mb_fg_p4a'
    tags = '"rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p4"'
    for i, t in enumerate(C4_T):
        vent = C4_VENT_L if i % 2 == 0 else C4_VENT_R
        lines = [g.GRP_NEW] if i in (min(C4_GROUPS[0]), min(C4_GROUPS[1])) else []
        lines += [f'execute at @s rotated as @s rotated ~ 0 positioned {A.c_bf(vent)} run summon minecraft:item_display ~ ~ ~ '
                  f'{{Tags:[{tags},"{M}","rlk_mb_fg_p4i{i}","rlk_mb_fg_pnew"],Rotation:[0f,-90f],teleport_duration:{C4_UP}}}',
                  f'execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] run {g.kprop("missile")}',
                  'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT 0',
                  'scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS = #mbGrp mb',
                  'tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew',
                  f'execute at @s rotated as @s rotated ~ 0 positioned {A.c_bf(vent)} run {g.fx("missile_launch")}',
                  f'execute at @s rotated as @s rotated ~ 0 positioned {A.c_bf(vent)} run {g.snd("missile_launch")}']
        tl.at(t, *lines)
        T = f'rlk_mb_fg_p4t{i}'
        side = -3 if i % 2 == 0 else 3                          # away from its vent (^x = left)
        g.pw(key, f'apex{i}', [
            f'# Missile {i + 1} (@s, at it), clock {C4_APEX}: to its apex (half way to the player, 16 b up, 3 b off to the',
            '# side away from its vent) in 6 t, nose along the flight.',
            f'execute as {BODY} run function rlk:mboss/mv/dist',
            'execute store result storage rlk:mboss fg.m4.z double 0.05 run scoreboard players get #mbDist mb',
            f'data modify storage rlk:mboss fg.m4.x set value {side}',
            f'function {NS}p/{key}/apex_at with storage rlk:mboss fg.m4',
            f'data merge entity @s {{teleport_duration:{C4_LOCK - C4_APEX}}}',
            f'execute at @s facing entity {mk(APEX)} feet positioned as {mk(APEX)} run tp @s ~ ~ ~ ~ ~',
            *kill_mk(APEX)])
        g.pw(key, f'lock{i}', [
            f'# Missile {i + 1} at its apex (clock {C4_LOCK}): the late lock under the player (walk disc; kept as {T}), its decal',
            f'# and hazard (tell {C4_HIT - C4_LOCK}, its volley group = the missile\'s mbS), the nose turns onto it at once.',
            g.lockp(), *g.keep(T),
            'scoreboard players operation #hzGrp mb = @s mbS',
            *g.hz_opts(kb=KB['default'], vis=41, quiet=1, sfx=0),
            f'execute at {mk(T)} positioned ~ {CY} ~ run ' + g.hz_disc(1.5, C4_HIT - C4_LOCK, DMG['c4']),
            f'execute at {mk(T)} positioned ~ {CY} ~ rotated ~ 0 run ' + g.tele_disc(1.5, C4_HIT - C4_LOCK),
            'data merge entity @s {teleport_duration:1}',
            f'execute at @s facing entity {mk(T)} feet run tp @s ~ ~ ~ ~ ~'])
        g.pw(key, f'dive{i}', [
            f'# Missile {i + 1}, clock {C4_LOCK + 1}: the dive onto {T} (+0.6 b), one interpolated teleport of {C4_HIT - C4_LOCK - 1} t.',
            f'data merge entity @s {{teleport_duration:{C4_HIT - C4_LOCK - 1}}}',
            f'execute positioned as {mk(T)} run tp @s ~ ~0.6 ~'])
        g.pw(key, f'hit{i}', [f'# Missile {i + 1}, clock {C4_HIT}: it reached the floor (its hazard strikes this tick).',
                              f'execute at {mk(T)} run {g.snd("debris_land")}' if i == C4_N - 1 else None,
                              *kill_mk(T), 'kill @s'])
    g.pw(key, 'apex_at', [f'# Macro {{x, z}} (@s = a missile): its apex marker {APEX}.', *kill_mk(APEX),
                          f'$execute at {BODY} facing entity {PLAYER} feet rotated ~ 0 positioned ^$(x) ^16 ^$(z) run '
                          f'summon minecraft:marker ~ ~ ~ {{Tags:[{tags},"{APEX}"]}}'])
    for name, n in (('apex', C4_APEX), ('lock', C4_LOCK), ('dive', C4_LOCK + 1), ('hit', C4_HIT)):
        g.pw(key, f'{name}_d', [f'# The missile\'s own {name} function (by its index tag).']
             + [f'execute if entity @s[tag=rlk_mb_fg_p4i{i}] run return run function {NS}p/{key}/{name}{i}' for i in range(C4_N)])
    g.pw(key, 'age', [
        '# @s = a missile, at it: its clock mbT; up 7 b (1), the apex (8), the lock (14), the dive (15), the impact (28); the',
        '# smoke trail every 3 t.',
        'scoreboard players add @s mbT 1',
        f'execute if score @s mbT matches 1 run tp @s ~ ~{C4_UP} ~',
        f'execute if score @s mbT matches {C4_APEX} run function {NS}p/{key}/apex_d',
        f'execute if score @s mbT matches {C4_LOCK} run function {NS}p/{key}/lock_d',
        f'execute if score @s mbT matches {C4_LOCK + 1} run function {NS}p/{key}/dive_d',
        f'execute if score @s mbT matches {C4_HIT}.. run return run function {NS}p/{key}/hit_d',
        'scoreboard players operation #fgM mb = @s mbT', 'scoreboard players operation #fgM mb %= #fgK3 mb',
        'execute if score #fgM mb matches 0 run ' + g.fx('missile_trail')])
    # the tells: tip flares, sparks, the vent shaft (twice), the dive whistle once per group
    tips = [f'execute at @s rotated as @s rotated ~ 0 positioned {A.c_bf(tip)} run ' for tip in (C4_TIP_L, C4_TIP_R)]
    tl.at(C4_FLARE, g.rig('face/track'), *[p + g.fx('tip_flare') for p in tips], tips[0] + g.snd('tip_flare'))
    tl.at(C4_FLARE + 4, *[p + g.fx('spark') for p in tips])
    tl.at(C4_VENT, at_body(C4_HUB, g.fx('vent_shaft')), at_body(C4_HUB, g.snd('missile_vent')))
    tl.at(C4_VENT + 7, at_body(C4_HUB, g.fx('vent_shaft')), at_body(C4_HUB, g.sound('block.fire.ambient', 0.6, 0.9)))
    for grp in C4_GROUPS:
        i0 = min(grp)
        tl.at(C4_T[i0] + C4_LOCK, f'execute at {mk(f"rlk_mb_fg_p4t{i0}")} run ' + g.snd('missile_dive'))
    tl.at(C4_END, 'kill @e[tag=rlk_mb_fg_p4]', *kill_mk(*[f'rlk_mb_fg_p4t{i}' for i in range(C4_N)]), g.end())
    tl.write([f'# C4 바위 폭탄 (clip missiles; @s = body): launches {C4_T}, lock +{C4_LOCK} (tell {C4_HIT - C4_LOCK}), impact '
              f'+{C4_HIT} = {C4_IMPACTS[0]}..{C4_IMPACTS[-1]}; 2 volley groups.', 'scoreboard players set #fq4Pz mb 0'],
             ['# missile tick.'],
             extra_tick=[resume_lines(g, key, 4, [A.c_redraw(g, key, 41, 41)]),
                         span(1, C4_LAUNCH - 1, g.rig('face/track')),
                         f'execute as @e[type=minecraft:item_display,tag={M}] at @s run function {NS}p/{key}/age'])
    g.pw(key, 'vis', ['# @s = a missile decal (#hzEv 1 = its impact).', 'execute unless score #hzEv mb matches 1 run return 0',
                      'execute at @s rotated ~ 0 run ' + g.fx('missile_impact'), 'execute at @s run ' + g.snd('missile_impact')])
    g.pw(key, 'pause', pause_lines(4))
    g.pw(key, 'cancel', ['# Every missile, the apex and the kept locks.', 'kill @e[tag=rlk_mb_fg_p4]',
                         *kill_mk(*[f'rlk_mb_fg_p4t{i}' for i in range(C4_N)])])


# ---------------------------------------------------------------------------------------------
def burst(g):
    """C5 지면 충격 (spec C5): the core sparks (0), turns its eye out (1); at the rim (3) the full-area hazard is made on
    the body (hz/disc r 12, unclamped: Q12; tell = the clip's blast - rim = 45 t) with its kit decal; the core lifts
    with the gold flash (5), the dark floor disc grows 3.5 -> 12 by the blast - 15, the up-beam (29), the rim flares
    (blast - 12), the column falls (41) and hits the floor (+3); ONE blast at 48: feet up to 0.5 b (a jump clears it),
    heavy KB, 2.2; the dash i-frames work. Leave the disc, jump or dash. The bar hides from blast + 1 (g.release)."""
    key, tl = 'burst', TL(g, 'burst')
    floor = f'execute at @s positioned ~ {CY} ~ rotated ~ 0 run '
    tl.at(C5_SPARK, at_body(C5_CORE, g.fx('core_spark')), at_body(C5_CORE, g.snd('core_spark')))
    tl.at(C5_EYE, at_body(C5_CORE, g.snd('core_flip')))
    tl.at(C5_RIM, *g.hz_opts(kb=KB['heavy'], y1=0.5, vis=51, quiet=1, sfx=0),
          f'execute at @s positioned ~ {CY} ~ run ' + g.hz_disc(C5_R, C5_BLAST - C5_RIM, DMG['c5']),
          floor + g.tele_disc(C5_R, C5_BLAST - C5_RIM),
          # the marker read (spec: respawn_anchor.set_spawn 0.6/0.6, but core_lift plays that sample 2 t later: FX-4)
          floor + g.sound('block.trial_spawner.about_to_spawn_item', 0.6, 0.7))
    tl.at(C5_LIFT, at_body(C5_CORE, g.fx('core_lift')), at_body(C5_CORE, g.snd('core_lift')))
    grow = C5_BLAST - 15 - (C5_LIFT + 2)
    tl.at(C5_LIFT + 2, floor + g.fx('dark_disc', r0=3.5, r=C5_R, grow=grow, life=C5_BLAST + 1 - (C5_LIFT + 2)),
          floor + g.sound('block.beacon.power_select', 0.6, 0.6))
    tl.at(C5_UP, at_body(C5_CORE_UP, g.sound('block.crafter.craft', 0.6, 1.0)))
    tl.at(C5_BEAM, at_body(C5_CORE_UP, g.fx('up_beam')), at_body(C5_CORE_UP, g.snd('up_beam')))
    tl.at(C5_BLAST - 12, floor + g.fx('rim_flare', r=C5_R), floor + g.sound('block.amethyst_block.resonate', 0.7, 0.6))
    tl.at(C5_COLUMN, floor + g.fx('column_down', h=round(C5_CORE_UP, 2)), floor + g.snd('column_down'))
    tl.at(C5_COLUMN + 3, floor + g.fx('floor_hit'), floor + g.sound('block.amethyst_cluster.break', 0.7, 0.9),
          floor + g.sound('entity.generic.explode', 0.4, 1.3))
    tl.at(C5_BLAST + 1, g.release())
    tl.at(C5_BLAST + 6, floor + g.snd('rocks_hover'))
    tl.at(C5_BLAST + 16, floor + g.snd('rocks_hover'))
    tl.at(C5_BLAST + 29, floor + g.snd('debris_land'))
    tl.at(C5_SINK, at_body(4.5, g.sound('block.piston.contract', 0.6, 0.9)))
    tl.at(C5_SINK + 19, at_body(4.5, g.sound('block.crafter.craft', 0.5, 1.0)), at_body(4.5, g.sound('block.chain.place', 0.5, 1.0)))
    tl.at(C5_LEN, g.end())
    tl.write([f'# C5 지면 충격 (clip coreup; @s = body): disc r {L.num(C5_R)} made at {C5_RIM}, the blast at {C5_BLAST}.',
              'scoreboard players set #fq5Pz mb 0'],
             ['# burst tick.'], extra_tick=[resume_lines(g, key, 5, [A.c_redraw(g, key, 51, 51)])])
    g.pw(key, 'vis', ['# @s = the blast hazard (#hzEv 1 = the blast): the flash over the disc, the crack ring, the rocks.',
                      'execute unless score #hzEv mb matches 1 run return 0',
                      'execute at @s rotated ~ 0 run ' + g.fx('blast', r=C5_R), 'execute at @s rotated ~ 0 run ' + g.fx('rocks'),
                      'execute at @s run ' + g.snd('blast')])
    g.pw(key, 'pause', pause_lines(5))
    g.pw(key, 'cancel', ['# Nothing of its own lingers (the hazard goes with lib_clear).'])


# ---------------------------------------------------------------------------------------------
def rock(g):
    """C6 파쇄 (spec C6, Q7): the dip and roll toward the player (0; the body steps 0.2 b/t toward a player >= 5 b away
    until the vent, F4), the vent flare (12), the tower (20), the flame band (38); the device tracks the player
    (4 deg/t) until the revert. Then api.c_rocks: 8 floor bursts on the arc walker (the sweep crosses the device's
    front and ends on the player's feet; r 1.8, tell 10, jumpable 1.2 b, heavy KB, 1.3; bursts 7-8 one volley group),
    a slab torn out at each, 5 throws from slabs 1-5 (a 10 t throw line, then a blade pj 1.5 b/t, total reach 1.5 b,
    1.1) with at most 2 slab hits per run (the rest crumble), the unthrown slabs crumble at the revert."""
    key, tl = 'rock', TL(g, 'rock')
    rk = A.c_rocks(g, tl, key, 6, C6_BURSTS, C6_THROWS, DMG['c6'], DMG['c6s'], el=5)
    assert rk['done'] <= C6_END, rk['done']
    dip = f'execute at @s unless entity @e[tag=rlk_body,distance=..{L.num(C6_DIP_MIN)}] run ' + g.bstep('toward', C6_DIP_STEP)
    tl.at(C6_DIP, dip, g.rig('face/track'), at_floor(g.fx('dip')), at_body(2.8, g.snd('dip')))
    tl.at(C6_VENT, at_body(3.5, g.fx('vent_flare')), at_body(3.5, g.snd('vent_flare')))
    tl.at(C6_TOWER, at_body(3.6, g.fx('tower_up')), at_body(3.6, g.snd('tower_up')))
    tl.at(C6_TOWER + 6, at_body(4.5, g.snd('gear_click')))
    tl.at(C6_TOWER + 12, at_body(4.5, g.snd('gear_click')))
    tl.at(C6_BAND, at_body(3.9, g.fx('flame_band')))
    tl.at(C6_BAND + 6, at_body(3.9, g.snd('flame_charge')))
    tl.at(C6_BAND + 9, at_body(3.9, g.fx('flame_band')))
    tl.at(C6_REVERT, rk['crumble'], at_body(4.5, g.fx('revert')), at_body(4.5, g.snd('revert')), at_floor(g.snd('debris_land')))
    tl.at(C6_END, *rk['cancel'], g.end())
    tl.write([f'# C6 파쇄 (clip tower_throw; @s = body): bursts {C6_BURSTS}, throws {C6_THROWS}, revert {C6_REVERT}.',
              'scoreboard players set #fq6Pz mb 0'],
             ['# rock tick.'],
             extra_tick=[resume_lines(g, key, 6, [A.c_redraw(g, key, *rk['vis_ids'])]),
                         span(1, C6_DIP_T, dip), span(1, C6_REVERT, g.rig('face/track'))] + rk['tick'])
    g.pw(key, 'vis', ['# @s = a burst (#hzEv 1 = it strikes; the throw lines, hz_vis 62, draw nothing more).',
                      'execute unless score #hzEv mb matches 1 run return 0'] + rk['vis'])
    g.pw(key, 'pause', pause_lines(6))
    g.pw(key, 'cancel', ['# Walker, slabs (waiting and flying), locks.'] + rk['cancel'])
