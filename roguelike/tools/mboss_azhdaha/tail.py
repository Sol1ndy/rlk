"""S2-T: the tail-element patterns of 야타용왕 (plan.md 4.5, 4.6, 5 rows 41-46; s2.md 2.1, 7, 8, 10, 17, 18):

    41 서리 습격 (frost)        Cryo B3 special: 9 heptagram circles r 7.5 (t70 + 34 k, burst +22, 0.9 + stack)
    42 벼락 습격 (bolt)         Electro B3 special: 4 mask rounds (t123 / 201 / 279 / 357, markers 48 t ahead, nododge 1.2)
                                with 5 / 4 / 3 / 2 safe circles + 2 sky bolts after rounds 1-3 (r 1.6, tell 12, 0.5)
    43 쏟아지는 천화 (icicle)   Cryo emitter (bg slot T): tail_cast, the ice sphere over the back, 5 lances at +30 .. +174
    44 번개의 가루 (shell)      Electro shells: tail_cast, 8 shells into a hover cloud, 8 dives (r 2.4, tell 12, 0.6)
    45 천동만상 – 얼음 가시      Cryo P4: 3 star fields (bursts t68 / 74 / 80, r 4.0, 1.0 + stack), hail in F1 / F2 100 t
    46 천동만상 – 번개 가시      Electro P4: the hexagram zone marker + 6 lumps (t44 / 54 / 64 / 74 / 98 / 122, r 3.0, 0.7)
    AZ:xt/**                   the Cryo / Electro addon bodies of plan 4.6 (frost rings, bolt discs, the whip's ice wall
                                + hail strip, the whip's end bolts + crystal line + strip, the tail-slam strips)

Telegraphs follow plan Change note 1 (the 10-20 rule): a ground decal only for the *keep* rows: 41's heptagram, 42's
wash + safe rims, 45's star seals, 46's hexagram (a zone marker). Everything else draws no decal: the readable tell is
the clip pose / sound / the prop in flight named per row (43's lance, 44's shell + its lock flash, 46's hovering lump +
bolt), and every hit plays its impact preset at the strike (the hazards' vis hook). Every hazard keeps its internal
tell (N7: #mbDodgeOk, the brand's perfect dodge). Sizes, ticks and coefficients are plan 5's (binding).

Clocks: 41 / 42 run on the B3 clock #azB3T (absolute ticks, s2.md 7); 43's emitter on #azBgTT (0 = the sphere tick =
tail_cast fire); 44-46 on the main-slot clock #azPT (= the clip tick). Scratch scores #aq<id>* (s2.md 4.2), storage
rlk:mboss az.p<id>, entities tagged rlk_mb_az_pat + rlk_mb_az_p<id>* (addon bodies rlk_mb_az_x*).
"""
import math

from . import api as A
from .api import TL, L
from . import h_pt as H

NS = A.NS
K = A.K
BODY, PLAYER, ARENA_M = A.BODY, A.PLAYER, A.ARENA_M
CY = A.CY
DMG, KB = A.DMG, A.KB
MK, ID = H.MK, H.ID


def F(rel):
    return f'function {NS}{rel}'


def sc(n, v):
    return f'scoreboard players set {n} mb {int(v)}'


def num(v, nd=3):
    return L.num(float(v), nd)


# ============================================================================================================ timings
# 41 (B3 clock): circles at 70 + 34 k, icicle comet +18, burst +22 (plan 5 41)
FROST = [70 + 34 * k for k in range(9)]
FROST_ICE, FROST_BURST, FROST_R = 18, 22, 7.5
FROST_COMET = (1.5, 12.0, 1.5)                        # the comet starts here (blocks from the centre) and dives 4 t
# 42 (B3 clock): rounds, markers 48 t ahead, sky bolts at +30 / +42 (rounds 1-3), the safe circles per round
BOLT_ROUNDS = (123, 201, 279, 357)
BOLT_MARK = 48
BOLT_SAFE = ((5, 3.2, True), (4, 3.2, True), (3, 3.2, True), (2, 2.8, False))   # (circles, R0, one on the tail)
BOLT_SKY = (30, 42)
SKY_TELL, SKY_R = 12, 1.6
BOLT_RING = (9.0, 16.0)                               # the other circles on rings r 9-16 (12.5-16 while orbs live)
BOLT_PL_R4 = 8.0                                      # round 4: >= 8 b from the emergence spot (the centre)
# 43: tail_cast fire = the sphere; the bg clock 0 = that tick; lances at +30 .. +174; the sphere fades at +200
ICICLE_FIRE = A.ev('tail_cast', 'fire')               # 18
ICICLE_END = A.clip_len('tail_cast')                  # 34: the main-slot part ends with the clip
ICICLE_V = (30, 66, 102, 138, 174)
ICICLE_FADE = 200
ICICLE_R = 1.6
SPHERE = (0.0, 9.0, 2.0)                              # anchor + (s, y, f) in the body frame, follows
# 44: shells leave the tail tip from fire every 5 t, dives from fire + 70 every 6 t (lock 4 t before, flight 8 t)
SHELL_FIRE = ICICLE_FIRE
SHELL_N = 8
SHELL_SPAWN = [SHELL_FIRE + 5 * k for k in range(SHELL_N)]
SHELL_LAUNCH = [SHELL_FIRE + 70 + 6 * k for k in range(SHELL_N)]
SHELL_LOCK = [t - 4 for t in SHELL_LAUNCH]
SHELL_HIT = [t + 8 for t in SHELL_LAUNCH]             # tell 12 from the lock
SHELL_END = SHELL_HIT[-1] + 5                         # 143 (~ fire + 125)
SHELL_R = 2.4
SHELL_CLOUD = [(-3.6, 7.0, 5.0), (-1.2, 8.5, 6.5), (1.2, 7.0, 6.5), (3.6, 8.5, 5.0),
               (-2.4, 8.0, 8.5), (0.0, 7.0, 9.5), (2.4, 8.0, 8.5), (0.0, 9.0, 4.0)]   # (s, y, f) at spawn, body frame
# 45: launch t14, fields t26, bursts t68 / 74 / 80 (the spike lands 1 t before), hail in F1 / F2 100 t
SPIKE_LAUNCH = A.ev('spikes', 'launch')               # 14
ICE_FIELDS = 26
ICE_BURST = (68, 74, 80)
ICE_R, ICE_HAIL = 4.0, 100
ICE_END = ICE_BURST[-1] + 8                           # 88
# 46: hexagram t26 at lockv 10, lumps at t44 / 54 / 64 / 74 / 98 / 122 (lock 13 t before, bolt -3, fall 5 t)
HEX_T, HEX_R = 26, 4.8
LUMP_HIT = (44, 54, 64, 74, 98, 122)
LUMP_LOCK = 13
LUMP_GROUPS = (0, 0, 1, 1, 2, 3)
LUMP_R = 3.0
LUMP_H = 12.0
EL_END = 140

assert FROST[-1] <= A.B3_LAST and FROST[-1] + FROST_BURST <= A.B3_HIT_MAX
assert BOLT_ROUNDS[-1] <= A.B3_LAST and all(r - BOLT_MARK > A.B3_TAILUP for r in BOLT_ROUNDS)
assert all(r + s <= A.B3_HIT_MAX and r + s - SKY_TELL <= A.B3_LAST for r in BOLT_ROUNDS[:3] for s in BOLT_SKY)
assert ICICLE_V[-1] + 25 < ICICLE_FADE and min(b - a for a, b in zip(ICICLE_V, ICICLE_V[1:])) > H.flight(40)
assert SHELL_END == 143 and min(SHELL_LOCK) > SHELL_SPAWN[-1] + 9
assert A.ev('spikes', 'gold_off') == 22

P4_W = {'head_near': 2, 'head_mid': 3, 'head_far': 3, 'flank_near': 2, 'flank_far': 2, 'tail_lane': 2, 'tail_off': 2, 'paw': 1}
PATTERNS = [
    A.Pattern(41, 'frost', '서리 습격', 'special', None, phases=(3,), elem=('tail', 4), max_len=A.B3_LEN, length=A.B3_LEN - 4,
              hooks=('vis', 'b3tick', 'stop', 'reload', 'resume')),
    A.Pattern(42, 'bolt', '벼락 습격', 'special', None, phases=(3,), elem=('tail', 3), max_len=A.B3_LEN, length=A.B3_LEN - 4,
              hooks=('vis', 'b3tick', 'stop', 'reload', 'pause', 'resume')),
    A.Pattern(43, 'icicle', '쏟아지는 천화', 'bg', 'tail_cast', phases=(3,), elem=('tail', 4), cooldown=400, recover=18,
              max_len=50, length=ICICLE_END, gates=('no_bg',),
              weight={'head_mid': 3, 'head_far': 3, 'flank_far': 3, 'tail_lane': 3, 'tail_off': 3},
              hooks=('vis', 'bgtick', 'cancel_bg', 'reload')),
    A.Pattern(44, 'shell', '번개의 가루', 'normal', 'tail_cast', phases=(3,), elem=('tail', 3), cooldown=400, recover=20,
              max_len=170, length=SHELL_END,
              weight={'head_near': 1, 'head_mid': 2, 'head_far': 2, 'flank_far': 2, 'tail_lane': 2, 'tail_off': 2},
              hooks=('vis',)),
    A.Pattern(45, 'icespike', '천동만상 – 얼음 가시', 'normal', 'spikes', phases=(3,), elem=('tail', 4), recover=20,
              max_len=110, length=ICE_END, weight=P4_W, replaces=4, gates=('field_area',), hooks=('vis', 'resume')),
    A.Pattern(46, 'elspike', '천동만상 – 번개 가시', 'normal', 'spikes', phases=(3,), elem=('tail', 3), recover=20,
              max_len=150, length=EL_END, weight=P4_W, replaces=4, hooks=('vis', 'resume')),
]
P4_WEIGHTS = P4_W      # 45 / 46 carry P4's weights (plan 4.12); ai.py picks them through P4's candidate + `replaces`

# vis ids (mbHzV = id x 10 + k): the impact preset of every hit plays on its strike (Change note 1)
V41, V421, V422, V43, V44, V45, V46 = 411, 421, 422, 431, 441, 451, 461
VX_WALL, VX_LINE, VX_BOLT = 459, 468, 469             # addon hazards ride 45's / 46's vis hooks (Cryo / Electro)


def tl_tick_only(g, tl, tick, head):
    """A TL whose events are all dispatched from one hook file (no start file): the per-tick files + the tree."""
    for t, lines in sorted(tl.ev.items()):
        g.pw(tl.key, tl.tname(t), [f'# {tl.key} {tl.clock} {t}'] + lines)
    g.pw(tl.key, tick, list(head) + tl._node(sorted(tl.ev)))


def at_body(local, cmd):
    """cmd positioned at a body-frame point (s, y, f) of the anchor, rotated as the body (yaw only)."""
    s, y, f = local
    return f'execute at {BODY} rotated as {BODY} rotated ~ 0 positioned ^{num(s)} ^{num(y)} ^{num(f)} run {cmd}'


def hz(g, vis, el='tail', kb=None, grp='new', **opts):
    """The option lines of one hazard: its volley group ('new' / 'join:<score>' / 'ctx'), quiet + NoRx defaults, the
    vis id, the element (the tail element now: #azET)."""
    out = []
    if grp == 'new':
        out.append(g.GRP_NEW)
    out += g.hz_opts(grp=(grp == 'new'), vis=vis, kb=KB['default'] if kb is None else kb, **opts)
    if grp == 'ctx':
        out.append('scoreboard players operation #hzGrp mb = #azCtxGrp mb')
    elif grp.startswith('join:'):
        out.append(f'scoreboard players operation #hzGrp mb = {grp[5:]} mb')
    out += g.el_tail() if el == 'tail' else g.el(el)
    return out


# ============================================================================================================ 41 frost
C41 = H.sel('rlk_mb_az_p41c')
I41 = H.sel('rlk_mb_az_p41i', ID)


def frost(g):
    key, pid = 'frost', 41
    tl = TL(g, key, clock='#azB3T', sub='b3k')
    cx, cy, cz = FROST_COMET
    step = math.sqrt(cx * cx + cy * cy + cz * cz) / 4.0
    for c in FROST:
        tl.at(c, F('p/frost/circle'))
        tl.at(c + FROST_ICE, F('p/frost/comet'))
        for d in (1, 2, 3):
            tl.at(c + FROST_ICE + d, F('p/frost/comet_step'))
        tl.at(c + FROST_BURST, f'kill @e[type={ID},tag=rlk_mb_az_p41i]')
        tl.at(c + FROST_BURST + 1, f'kill @e[type={MK},tag=rlk_mb_az_p41c]')
    tl.write(['# 41 서리 습격 (Cryo B3 special, s2.md 7): started by the B3 frame at tail-up (#azB3T 58). Circles at '
              f'{FROST}: the heptagram (keep: outline + rune, plan Change note 1) and a disc r {FROST_R} with tell '
              f'{FROST_BURST} drawn together; the icicle comet at +{FROST_ICE} (the timing cue); the burst at +{FROST_BURST}.',
              sc('#aq41B', 0), f'kill @e[tag=rlk_mb_az_p41]'],
             ['# 41 b3tick (#azB3T, absolute): nothing is created after B3_LAST (357), nothing hits after B3_HIT_MAX (368).'],
             t0=A.B3_TAILUP, tick='b3tick')
    g.pw(key, 'circle', [
        '# @s = body, #azB3T = a circle tick. The centre: 70 % at the player (lockv lead 15, then 2 b along the velocity,',
        '# or 4 b off a standing player in a random direction), 30 % random 8-20 b from the tail; nudged off live fields',
        '# and orbit bands, kept in the walk disc; then drawn and armed (plan 5 41).',
        f'kill @e[type={MK},tag=rlk_mb_az_p41c]',
        'execute store result score #aq41R mb run random value 0..99',
        f'execute if score #aq41R mb matches ..69 run {F("p/frost/c_pl")}',
        f'execute if score #aq41R mb matches 70.. run {F("p/frost/c_rand")}',
        f'execute as {C41} at @s run {F("p/frost/nudge")}',
        f'execute as {C41} run {g.clamp_walk()}',
        f'execute at {C41} run {F("p/frost/make")}'])
    g.pw(key, 'c_pl', ['# The predictive lock (lead 15) re-tagged as the centre; moving player: 2 b further along the velocity.',
                       *g.lockv(15), *H.keep_lock('rlk_mb_az_p41c', 'rlk_mb_az_p41'),
                       f'execute if score #mbV mb matches 81.. as {C41} at @s if entity {PLAYER} facing entity {PLAYER} feet '
                       'rotated ~ 0 run tp @s ^ ^ ^-2',
                       f'execute unless score #mbV mb matches 81.. as {C41} run {F("p/frost/c_still")}'])
    g.pw(key, 'c_still', ['# @s = the centre: a standing player gets the circle 4 b off them in a random direction.',
                          'execute store result entity @s Rotation[0] float 1 run random value 0..359',
                          f'execute at {PLAYER} positioned ~ {CY} ~ rotated as @s rotated ~ 0 run tp @s ^ ^ ^4'])
    g.pw(key, 'c_rand', [f'# @s = body: a centre 8-20 b from the tail (the anchor) in a random direction.',
                         f'summon {MK} ~ {CY} ~ {{Tags:{H.tags(pid, "rlk_mb_az_p41c")}}}',
                         f'execute as {C41} store result entity @s Rotation[0] float 1 run random value 0..359',
                         'execute store result storage rlk:mboss az.p41.d int 1 run random value 8..20',
                         f'execute as {C41} at @s rotated as @s run function {NS}p/frost/mv with storage rlk:mboss az.p41'])
    g.pw(key, 'mv', ['$tp @s ^ ^ ^$(d)'])
    g.pw(key, 'nudge', [
        '# @s = the centre, at it: 4 b away from a live field within 6 b; out of an orbit band (orbs at r 6.5 / 10.5, hr',
        '# 1.3 about the orbit centre) in 0.5-b steps (<= 3 b).',
        f'execute if entity @e[type={MK},tag=rlk_mb_az_fld,distance=..6] facing entity '
        f'@e[type={MK},tag=rlk_mb_az_fld,distance=..6,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-4',
        sc('#aq41N', 0),
        f'execute if entity @e[type={MK},tag=rlk_mb_az_orb,limit=1] if entity @e[type={MK},tag=rlk_mb_az_orbc,limit=1] '
        f'at @s run {F("p/frost/nudge_o")}'])
    g.pw(key, 'nudge_o', [
        f'execute unless entity @e[type={MK},tag=rlk_mb_az_orbc,distance=5.2..7.8] unless entity '
        f'@e[type={MK},tag=rlk_mb_az_orbc,distance=9.2..11.8] run return 0',
        'scoreboard players add #aq41N mb 1', 'execute if score #aq41N mb matches 7.. run return 0',
        f'execute facing entity @e[type={MK},tag=rlk_mb_az_orbc,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-0.5',
        f'execute at @s run {F("p/frost/nudge_o")}'])
    g.pw(key, 'make', [
        f'# Positioned at the centre: the heptagram (keep, r {FROST_R}, tell {FROST_BURST}) and its hazard disc (same size and',
        '# tell), Cryo (the tail element) + a stack, own volley group; the draw sound.',
        K.tele_heptagram(FROST_R, FROST_BURST, el=4, hold=3), K.snd('frost_draw'),
        'scoreboard players operation #aq41B mb = #azB3T mb', f'scoreboard players add #aq41B mb {FROST_BURST}',
        *hz(g, V41), L.hz_disc(FROST_R, FROST_BURST, DMG['o41']), g.tag_last_hz('rlk_mb_az_p41')])
    g.pw(key, 'comet', [
        f'# +{FROST_ICE}: the icicle comet appears high over the circle and dives into its centre in 4 t (the timing cue).',
        f'kill @e[type={ID},tag=rlk_mb_az_p41i]',
        f'execute at {C41} run summon {ID} ~{num(cx)} ~{num(cy)} ~{num(cz)} {{Tags:{H.tags(pid, "rlk_mb_az_p41i")},teleport_duration:1}}',
        f'execute as {I41} run {K.prop("icicle")}',
        f'execute as {I41} at @s if entity {C41} facing entity {C41} feet run tp @s ~ ~ ~ ~ ~',
        f'execute at {I41} run {K.fx("icicle_trail")}', f'execute at {C41} run {K.snd("frost_icicle")}'])
    g.pw(key, 'comet_step', [f'execute as {I41} at @s if entity {C41} facing entity {C41} feet run tp @s ^ ^ ^{num(step)}',
                             f'execute at {I41} run {K.fx("icicle_trail")}'])
    g.pw(key, 'vis', ['# @s = a 41 hazard marker (#hzEv 1 = its strike): the ice-spike burst, frost mist and the sound.',
                      f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V41} run {F("p/frost/burst")}'])
    g.pw(key, 'burst', [K.fx('frost_burst', r=FROST_R), K.fxe('impact', 4), K.snd('frost_burst')])
    clear = [f'kill @e[type={ID},tag=rlk_mb_az_p41]', f'kill @e[type={MK},tag=rlk_mb_az_p41c]', sc('#aq41B', 0)]
    g.pw(key, 'stop', ['# B3_BURST: the special stops (its last burst landed at 364).'] + clear)
    g.pw(key, 'cancel', ['# Immediate cleanup (selectors only): props, the centre and a pending circle hazard.',
                         f'kill @e[tag=rlk_mb_az_p41]', sc('#aq41B', 0)])
    g.pw(key, 'reload', ['# /reload inside the B3: everything of ours is gone (aux entities); the schedule goes on from #azB3T',
                         '# (a circle cut mid-way never strikes).'] + clear)
    prep, call = H.tele_dyn('heptagram', {'tell': '#aq41W'}, r=FROST_R, el=4, hold=3)
    g.pw(key, 'resume', ['# Resume: the live circle\'s heptagram again with its remaining tell (the core cleared the decals).',
                         'scoreboard players operation #aq41W mb = #aq41B mb', 'scoreboard players operation #aq41W mb -= #azB3T mb',
                         f'execute unless score #aq41W mb matches 1..{FROST_BURST} run return 0'] + prep + [f'execute at {C41} run {call}'])


# ============================================================================================================ 42 bolt
SAFE = 'rlk_mb_az_p42s'
SAFE_NEW = 'rlk_mb_az_p42n'
SAFE_T = 'rlk_mb_az_p42t'


def bolt(g):
    key, pid = 'bolt', 42
    tl = TL(g, key, clock='#azB3T', sub='b3k')
    sky_i = 0
    for j, s in enumerate(BOLT_ROUNDS):
        m = s - BOLT_MARK
        tl.at(m, F(f'p/bolt/round_{j}'))
        for t in range(m + 2, s, 2):
            tl.at(t, F('p/bolt/hud'))
        tl.at(s, 'data remove storage rlk:mboss az.subx', sc('#azHudQ', 1), sc('#aq42In', 0))
        for d, p in ((4, 1.1), (8, 1.25), (12, 1.4), (16, 1.2)):
            tl.at(s + d, f'execute at {ARENA_M} run {g.sound("entity.lightning_bolt.impact", 0.8, p)}')
        tl.at(s + 1, f'kill @e[type={MK},tag={SAFE}]')
        if j < 3:
            for off in BOLT_SKY:
                tl.at(s + off - SKY_TELL, F(f'p/bolt/sky_{sky_i}'))
                tl.at(s + off + 1, f'kill @e[type={MK},tag=rlk_mb_az_p42b{sky_i}]')
                sky_i += 1
    tl.write(['# 42 벼락 습격 (Electro B3 special, s2.md 7): rounds strike at '
              f'{list(BOLT_ROUNDS)} (markers {BOLT_MARK} t before: the violet wash + green safe rims, keep); the mask hazard',
              '# (N4, nododge, 1.2 + brand, height 0-3) everywhere outside the safe circles; sky bolts at round +30 / +42.',
              sc('#aq42S', 0), sc('#aq42J', -1), sc('#aq42In', 0), 'data remove storage rlk:mboss az.subx',
              f'kill @e[tag=rlk_mb_az_p42]'],
             ['# 42 b3tick (#azB3T, absolute): the last round strikes at 357 (B3_LAST), the last sky bolt at 321.'],
             t0=A.B3_TAILUP, tick='b3tick')
    for j, (n, r0, on_tail) in enumerate(BOLT_SAFE):
        s = BOLT_ROUNDS[j]
        lines = [f'# Round {j + 1} markers (#azB3T {s - BOLT_MARK}, strike {s}): {n} safe circles r {r0} (safe within R0 + 0.3)'
                 + (': one on the tail (the anchor),' if on_tail else ': both >= 8 b from the emergence spot (the centre),'),
                 '# one relative to the player (reachable within the 48 t), the rest on rings r 9-16 >= 50 degrees apart;',
                 '# then the mask hazard and the safe markers (same tick, cm.md 13.6), the wash and the rims.',
                 f'kill @e[type={MK},tag={SAFE}]', sc('#aq42J', j), sc('#aq42S', s), sc('#aq42In', 0), sc('#aq42Dp', -1)]
        idx = 0

        def new_circle(pos_cmd):
            return [f'{pos_cmd}summon {MK} ~ {CY} ~ {{Tags:{H.tags(pid, SAFE, SAFE_NEW, SAFE_T)}}}']
        if on_tail:
            lines += new_circle(f'execute at {BODY} run ')
            lines += [f'scoreboard players set @e[type={MK},tag={SAFE_T}] mbS {idx}', f'tag @e[type={MK},tag={SAFE_T}] remove {SAFE_T}']
            idx += 1
        lines += new_circle(f'execute at {PLAYER} run ')
        lines += [f'scoreboard players set @e[type={MK},tag={SAFE_T}] mbS {idx}',
                  f'execute as @e[type={MK},tag={SAFE_T}] at @s run {F("p/bolt/pl_r4" if not on_tail else "p/bolt/pl")}',
                  f'tag @e[type={MK},tag={SAFE_T}] remove {SAFE_T}']
        idx += 1
        nring = n - idx
        lines += ['execute store result score #aq42A mb run random value 0..359']
        for i in range(nring):
            lines += new_circle(f'execute at {ARENA_M} run ')
            lines += [f'scoreboard players set @e[type={MK},tag={SAFE_T}] mbS {idx}',
                      'scoreboard players operation #aq42X mb = #aq42A mb',
                      f'scoreboard players add #aq42X mb {int(round(i * 360 / nring))}',
                      'execute store result score #aq42Y mb run random value -10..10',
                      'scoreboard players operation #aq42X mb += #aq42Y mb',
                      f'execute as @e[type={MK},tag={SAFE_T}] store result entity @s Rotation[0] float 1 run scoreboard players get #aq42X mb',
                      f'execute as @e[type={MK},tag={SAFE_T}] run {F("p/bolt/ring")}',
                      f'tag @e[type={MK},tag={SAFE_T}] remove {SAFE_T}']
            idx += 1
        assert idx == n
        lines += [f'execute at {ARENA_M} run {F(f"p/bolt/mask_{j}")}',
                  f'execute at {ARENA_M} run {K.tele_mask_wash(A.WALK, BOLT_MARK, hold=3)}']
        lines += [f'execute at @e[type={MK},tag={SAFE_NEW},scores={{mbS={i}}},limit=1] run {K.tele_safe_rim(i, r0, BOLT_MARK, hold=3)}'
                  for i in range(n)]
        lines += [f'execute at {ARENA_M} run {K.snd("bolt_marker")}', f'tag @e[type={MK},tag={SAFE_NEW}] remove {SAFE_NEW}']
        g.pw(key, f'round_{j}', lines)
        g.pw(key, f'mask_{j}', [f'# Positioned at the arena centre: the mask hazard (kind 6) r0 {r0}, tell {BOLT_MARK}, own group, its own',
                                '# safe group (#hzSafeG 0); the new circles become its safe markers (mbHzSG = #hzLast).',
                                *hz(g, V421, nododge=1, y0=0, y1=3, safe_g=0), *L.hz_mask(r0, BOLT_MARK, DMG['o42']),
                                g.tag_last_hz('rlk_mb_az_p42'),
                                f'execute as @e[type={MK},tag={SAFE_NEW}] run scoreboard players operation @s mbHzSG = #hzLast mb',
                                f'tag @e[type={MK},tag={SAFE_NEW}] add rlk_mb_hzsafe'])
    g.pw(key, 'pl', ['# @s = the player circle (at the player\'s feet): moved 5 b toward the centre (when farther), kept <= 24 b.',
                     f'execute if entity {ARENA_M.replace("limit=1", "distance=5..,limit=1")} facing entity {ARENA_M} feet rotated ~ 0 '
                     'run tp @s ^ ^ ^5', g.clamp_body(24.0)])
    g.pw(key, 'pl_r4', ['# @s = round 4\'s player circle: toward the centre by <= 5 b but never nearer than 8 b to it (the',
                        '# emergence spot); a player inside 8 b gets it pushed out to 8 b.', sc('#aq42N', 0),
                        f'execute if entity {ARENA_M.replace("limit=1", "distance=..8,limit=1")} run return run {F("p/bolt/r4_out")}',
                        f'execute at @s run {F("p/bolt/r4_in")}', g.clamp_body(24.0)])
    g.pw(key, 'r4_in', [f'execute unless entity {ARENA_M.replace("limit=1", "distance=8.5..,limit=1")} run return 0',
                        'scoreboard players add #aq42N mb 1', 'execute if score #aq42N mb matches 11.. run return 0',
                        f'execute facing entity {ARENA_M} feet rotated ~ 0 run tp @s ^ ^ ^0.5', f'execute at @s run {F("p/bolt/r4_in")}'])
    g.pw(key, 'r4_out', [f'execute unless entity {ARENA_M.replace("limit=1", "distance=..7.99,limit=1")} run return 0',
                         'scoreboard players add #aq42N mb 1', 'execute if score #aq42N mb matches 20.. run return 0',
                         f'execute at @s facing entity {ARENA_M} feet rotated ~ 0 run tp @s ^ ^ ^-0.5', f'execute at @s run {F("p/bolt/r4_out")}'])
    g.pw(key, 'ring', [
        '# @s = a ring circle (rotated to its bearing): r 9-16 from the centre (12.5-16 while orbs live: off the orbit bands),',
        '# 4 b away from a live field within 6 b, kept <= 24 b.',
        'execute store result storage rlk:mboss az.p42.d double 0.1 run random value 90..160',
        f'execute if entity @e[type={MK},tag=rlk_mb_az_orb,limit=1] store result storage rlk:mboss az.p42.d double 0.1 run random value 125..160',
        f'execute at {ARENA_M} rotated as @s run function {NS}p/bolt/mv with storage rlk:mboss az.p42',
        f'execute at @s if entity @e[type={MK},tag=rlk_mb_az_fld,distance=..6] facing entity '
        f'@e[type={MK},tag=rlk_mb_az_fld,distance=..6,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-4',
        g.clamp_body(24.0)])
    g.pw(key, 'mv', ['$tp @s ^ ^ ^$(d)'])
    # the sub-line "안전 지대 N칸" (distance to the nearest circle edge, R0 + 0.3) and the chime inside
    for nm, r0 in (('dist_a', 3.2), ('dist_b', 2.8)):
        g.pw(key, nm, [f'# The nearest safe circle from the player\'s feet: 0 inside (R0 {r0} + 0.3), else whole blocks to its edge.']
             + [f'execute at {PLAYER} if entity @e[type={MK},tag={SAFE},distance=..{num(r0 + 0.3 + k, 2)}] run return run '
                f'scoreboard players set #aq42D mb {k}' for k in range(0, 46)])
    g.pw(key, 'hud', ['# Every 2 t of a marker window: the sub-line part (rlk:mboss az.subx, s2.md 16) and the chime inside.',
                      sc('#aq42D', 99), f'execute if score #aq42J mb matches 3 run {F("p/bolt/dist_b")}',
                      f'execute unless score #aq42J mb matches 3 run {F("p/bolt/dist_a")}',
                      'execute if score #aq42D mb = #aq42Dp mb run return 0',
                      'scoreboard players operation #aq42Dp mb = #aq42D mb',
                      f'execute if score #aq42D mb matches 0 run {F("p/bolt/hud_in")}',
                      f'execute if score #aq42D mb matches 1.. run {F("p/bolt/hud_out")}', sc('#azHudQ', 1)])
    g.pw(key, 'hud_in', ['data modify storage rlk:mboss az.subx set value [{text:"  안전 지대 안",color:"#2FCF5E",bold:true}]',
                         f'execute unless score #aq42In mb matches 1 at {PLAYER} run {K.snd("safe_chime")}', sc('#aq42In', 1)])
    g.pw(key, 'hud_out', ['execute store result storage rlk:mboss az.p42.n int 1 run scoreboard players get #aq42D mb',
                          f'function {NS}p/bolt/hud_txt with storage rlk:mboss az.p42', sc('#aq42In', 0)])
    g.pw(key, 'hud_txt', ['$data modify storage rlk:mboss az.subx set value [{text:"  안전 지대 $(n)칸",color:"#C58BFF",bold:true}]'])
    for i in range(6):
        bt = f'rlk_mb_az_p42b{i}'
        g.pw(key, f'sky_{i}', [f'# Sky bolt {i + 1}: a disc r {SKY_R} at the player\'s feet now, tell {SKY_TELL}, 0.5 + brand, KB 2,',
                               '# dodgeable: the lock sound is the cue, keep moving (no ground decal: plan Change note 1).',
                               g.lockp(), *H.keep_lock(bt, 'rlk_mb_az_p42'),
                               f'execute at {H.sel(bt)} run {F("p/bolt/sky_hz")}',
                               f'execute at {H.sel(bt)} run {g.sound("block.beacon.power_select", 0.6, 2.0)}',
                               f'execute at {H.sel(bt)} run {g.sound("entity.lightning_bolt.thunder", 0.25, 1.9)}'])
    g.pw(key, 'sky_hz', [*hz(g, V422, kb=KB['o42_sky']), L.hz_disc(SKY_R, SKY_TELL, DMG['o42_sky']), g.tag_last_hz('rlk_mb_az_p42')])
    g.pw(key, 'vis', ['# @s = a 42 hazard marker on its strike: the floor-wide two-wave crackle (mask) / a single sky bolt.',
                      f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V421} run {F("p/bolt/strike")}',
                      f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V422} run {F("p/bolt/sky_fx")}'])
    g.pw(key, 'strike', [K.fx('bolt_round', r=A.WALK), K.snd('bolt_strike')])
    g.pw(key, 'sky_fx', [K.fx('bolt'), g.sound('entity.lightning_bolt.impact', 0.9, 1.25)])
    clear = [f'kill @e[type={MK},tag=rlk_mb_az_p42]', 'data remove storage rlk:mboss az.subx', sc('#azHudQ', 1),
             sc('#aq42S', 0), sc('#aq42In', 0)]
    g.pw(key, 'stop', ['# B3_BURST: the special stops (the last round struck at 357).'] + clear)
    g.pw(key, 'cancel', ['# Immediate cleanup (selectors only): circles, locks, live hazards, the sub-line part.',
                         'kill @e[tag=rlk_mb_az_p42]'] + clear[1:])
    g.pw(key, 'reload', ['# /reload inside the B3: hazards and circles are gone; a cut round never strikes, the schedule goes on.'] + clear)
    g.pw(key, 'pause', ['# Pause: the sub-line part goes (the decals are cleared by the core).', 'data remove storage rlk:mboss az.subx',
                        sc('#azHudQ', 1)])
    res = ['# Resume: the live round\'s wash and rims again with the remaining tell; the sub-line comes back on the next hud.',
           'scoreboard players operation #aq42W mb = #aq42S mb', 'scoreboard players operation #aq42W mb -= #azB3T mb',
           sc('#aq42Dp', -1), f'execute unless score #aq42W mb matches 1..{BOLT_MARK} run return 0']
    prep, call = H.tele_dyn('mask_wash', {'tell': '#aq42W'}, r=A.WALK, hold=3)
    res += prep + [f'execute at {ARENA_M} run {call}']
    for i in range(5):
        for cond, r0 in (('unless', 3.2), ('if', 2.8)):
            prep, call = H.tele_dyn('safe_rim', {'tell': '#aq42W'}, id=i, r=r0, hold=3)
            res += [f'execute {cond} score #aq42J mb matches 3 run {ln}' for ln in prep]
            res.append(f'execute {cond} score #aq42J mb matches 3 at @e[type={MK},tag={SAFE},scores={{mbS={i}}},limit=1] run {call}')
    g.pw(key, 'resume', res)


# ============================================================================================================ 43 icicle
S43 = H.sel('rlk_mb_az_p43s', ID)
L43 = H.sel('rlk_mb_az_p43l', ID)
A43 = H.sel('rlk_mb_az_p43a')


def icicle(g):
    key, pid = 'icicle', 43
    tl = TL(g, key)
    for t in range(0, ICICLE_FIRE, 2):
        tip = A.track('tail_cast', 'tail_tip')[t]
        tl.at(t, at_body(tip, g.particle('snowflake', delta=(0.4, 0.4, 0.4), speed=0.02, n=4)),
              at_body(tip, g.dust((0.62, 0.91, 0.96), 1.4, delta=(0.3, 0.3, 0.3), n=3)))
    tl.at(A.ev('tail_cast', 'charge'), at_body(A.anchor('tail_cast', 'charge', 'tail_tip'), K.fx('icicle_trail')),
          at_body(A.anchor('tail_cast', 'charge', 'tail_tip'), g.sound('block.amethyst_block.resonate', 0.8, 1.6)))
    tl.at(ICICLE_FIRE, F('p/icicle/sphere'), g.bg_start('T'))
    tl.at(ICICLE_END, g.end())
    tl.write(['# 43 쏟아지는 천화 (Cryo emitter, s2.md 8): tail_cast; ice coral at the tail tip; at fire '
              f'({ICICLE_FIRE}) the ice sphere over the back and bg slot T (lances at {list(ICICLE_V)} of the bg clock, the',
              f'# sphere fades at +{ICICLE_FADE}); the main slot ends with the clip ({ICICLE_END}).'],
             ['# 43 tick (#azPT = the tail_cast tick).'])
    bt = TL(g, key, clock='#azBgTT', sub='bk')
    for t in range(0, ICICLE_FADE, 4):
        bt.at(t, f'execute at {S43} run {K.fx("ice_sphere")}')
    for t in range(0, ICICLE_FADE, 40):
        bt.at(t, f'execute at {S43} run {K.snd("sphere_loop")}')
    for v in ICICLE_V:
        bt.at(v, F('p/icicle/launch'))
    bt.at(ICICLE_FADE, f'execute at {S43} run {K.fx("ice_sphere")}', f'execute at {S43} run {g.particle("snowflake", delta=(0.8, 0.8, 0.8), speed=0.05, n=20)}',
          f'kill @e[tag=rlk_mb_az_p43]', g.bg_end('T'))
    tl_tick_only(g, bt, 'bgtick', [
        '# 43 bgtick (#azBgTT 0 = the sphere tick): the sphere follows the anchor (0, 9, +2 in the body frame), its aura;',
        '# a lance in flight moves one step; the volleys; the fade.',
        f'execute as {S43} at {BODY} rotated as {BODY} rotated ~ 0 run tp @s ^{num(SPHERE[0])} ^{num(SPHERE[1])} ^{num(SPHERE[2])}',
        f'execute if score #aq43L mb matches 1.. run {F("p/icicle/fly")}'])
    g.pw(key, 'sphere', ['# The spiky ice sphere over the back (follows the anchor; plan 5 43).',
                         f'kill @e[type={ID},tag=rlk_mb_az_p43s]', sc('#aq43L', 0),
                         at_body(SPHERE, f'summon {ID} ~ ~ ~ {{Tags:{H.tags(pid, "rlk_mb_az_p43s")},teleport_duration:1}}'),
                         f'execute as {S43} run {K.prop("ice_sphere")}',
                         f'execute at {S43} run {K.fx("ice_sphere")}', f'execute at {S43} run {K.snd("sphere_form")}'])
    d2 = '#aq43D'
    g.pw(key, 'launch', [
        '# A lance: the player\'s feet locked now; flight = max(12, ceil(d / 1.6)) t from the sphere, no steering; the',
        f'# impact disc r {ICICLE_R} (tell = the flight, 0.7 Cryo + stack, own group) at the aim; no ground decal (the',
        '# sphere and the lance in flight are the tell, plan Change note 1).',
        f'execute unless entity {S43} run return 0',
        g.lockp(), *H.keep_lock('rlk_mb_az_p43a', 'rlk_mb_az_p43'),
        f'execute store result score #aq43X mb run data get entity {S43} Pos[0] 100',
        f'execute store result score #aq43Y mb run data get entity {S43} Pos[1] 100',
        f'execute store result score #aq43Z mb run data get entity {S43} Pos[2] 100',
        f'execute store result score #aq43DX mb run data get entity {A43} Pos[0] 100',
        f'execute store result score #aq43DY mb run data get entity {A43} Pos[1] 100',
        f'execute store result score #aq43DZ mb run data get entity {A43} Pos[2] 100',
        'scoreboard players operation #aq43DX mb -= #aq43X mb', 'scoreboard players operation #aq43DY mb -= #aq43Y mb',
        'scoreboard players operation #aq43DZ mb -= #aq43Z mb',
        f'scoreboard players operation {d2} mb = #aq43DX mb', f'scoreboard players operation {d2} mb *= #aq43DX mb',
        'scoreboard players operation #aq43T mb = #aq43DY mb', 'scoreboard players operation #aq43T mb *= #aq43DY mb',
        f'scoreboard players operation {d2} mb += #aq43T mb',
        'scoreboard players operation #aq43T mb = #aq43DZ mb', 'scoreboard players operation #aq43T mb *= #aq43DZ mb',
        f'scoreboard players operation {d2} mb += #aq43T mb',
        *H.flight_lines(d2, '#aq43F'),
        '# the per-tick step (mb) and the hazard args',
        *[ln for ax in 'XYZ' for ln in (f'scoreboard players operation #aq43S{ax} mb = #aq43D{ax} mb',
                                         f'scoreboard players operation #aq43S{ax} mb *= #c10 mb',
                                         f'scoreboard players operation #aq43S{ax} mb /= #aq43F mb',
                                         f'execute store result storage rlk:mboss az.p43.v.{ax.lower()} double 0.001 run '
                                         f'scoreboard players get #aq43S{ax} mb')],
        'scoreboard players operation #aq43L mb = #aq43F mb',
        f'data modify storage rlk:mboss az.p43.hz set value {{r:{int(round(ICICLE_R * 10))},dmg:{DMG["o43"]}}}',
        'execute store result storage rlk:mboss az.p43.hz.tell int 1 run scoreboard players get #aq43F mb',
        *hz(g, V43),
        f'execute at {A43} run function rlk:mboss/hz/disc with storage rlk:mboss az.p43.hz',
        g.tag_last_hz('rlk_mb_az_p43'),
        f'kill @e[type={ID},tag=rlk_mb_az_p43l]',
        f'execute at {S43} run summon {ID} ~ ~ ~ {{Tags:{H.tags(pid, "rlk_mb_az_p43l")},teleport_duration:1}}',
        f'execute as {L43} run {K.prop("icicle")}',
        f'execute as {L43} at @s if entity {A43} facing entity {A43} feet run tp @s ~ ~ ~ ~ ~',
        f'execute at {S43} run {g.sound("item.trident.riptide_1", 1.0, 1.6)}'])
    g.pw(key, 'fly', ['# One flight step of the live lance (the per-tick step from the launch); it vanishes on the impact tick.',
                      'scoreboard players remove #aq43L mb 1',
                      f'execute as {L43} at @s run function {NS}p/icicle/mv with storage rlk:mboss az.p43.v',
                      f'execute at {L43} run {K.fx("icicle_trail")}',
                      f'execute if score #aq43L mb matches 0 run kill @e[type={ID},tag=rlk_mb_az_p43l]',
                      f'execute if score #aq43L mb matches 0 run kill @e[type={MK},tag=rlk_mb_az_p43a]'])
    g.pw(key, 'mv', ['$tp @s ~$(x) ~$(y) ~$(z)'])
    g.pw(key, 'vis', [f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V43} run {F("p/icicle/impact")}'])
    g.pw(key, 'impact', [K.fx('frost_burst', r=ICICLE_R), g.sound('block.glass.break', 1.0, 1.0),
                         g.sound('entity.generic.explode', 0.4, 1.4)])
    g.pw(key, 'cancel', ['# The main-slot part stops (selectors only); the emitter stays when it already holds bg slot T.',
                         'execute if score #azBgT mb matches 43 run return 0', 'kill @e[tag=rlk_mb_az_p43]', sc('#aq43L', 0)])
    g.pw(key, 'cancel_bg', ['# The emitter is cancelled (a queued transition, death, cleanup, test stop): sphere, lance, aim and',
                            '# any lance hazard in flight go.', 'kill @e[tag=rlk_mb_az_p43]', sc('#aq43L', 0)])
    g.pw(key, 'reload', ['# /reload with the emitter in bg slot T: the sphere is re-made; a lance in flight is lost (its hazard too).',
                         sc('#aq43L', 0), F('p/icicle/sphere')])


# ============================================================================================================ 44 shell
def shell_sel(k, kind=ID):
    return H.sel(f'rlk_mb_az_p44s{k}', kind)


def lock_sel(k):
    return H.sel(f'rlk_mb_az_p44l{k}')


def shell(g):
    key, pid = 'shell', 44
    tl = TL(g, key)
    tip_charge = A.anchor('tail_cast', 'charge', 'tail_tip')
    tips = A.track('tail_cast', 'tail_tip')
    tl.at(0, at_body(tips[0], K.fx('spark_column', h=6.0)), at_body(tips[0], g.sound('entity.evoker.prepare_attack', 0.6, 1.6)))
    tl.at(A.ev('tail_cast', 'charge'), at_body(tip_charge, K.fx('spark_column', h=6.0)))
    for k, t in enumerate(SHELL_SPAWN):
        tip = tips[min(t, len(tips) - 1)]
        tl.at(t, at_body(tip, f'summon {ID} ~ ~ ~ {{Tags:{H.tags(pid, f"rlk_mb_az_p44s{k}")},teleport_duration:1}}'),
              f'execute as {shell_sel(k)} run {K.prop("shell")}', at_body(tip, K.snd('shell_spawn')))
        s, y, f = SHELL_CLOUD[k]
        tl.at(t + 1, f'execute as {shell_sel(k)} run data merge entity @s {{teleport_duration:8}}',
              f'execute as {shell_sel(k)} at {BODY} rotated as {BODY} rotated ~ 0 run tp @s ^{num(s)} ^{num(y)} ^{num(f)}')
        tl.at(t + 9, f'execute as {shell_sel(k)} run data merge entity @s {{teleport_duration:1}}')
    for t in range(SHELL_SPAWN[0] + 10, SHELL_LAUNCH[-1], 20):
        tl.at(t, f'execute at {BODY} run {K.snd("shell_hover")}')
    for k in range(SHELL_N):
        tl.at(SHELL_LOCK[k], F(f'p/shell/lock_{k}'))
        tl.at(SHELL_LAUNCH[k], f'execute as {shell_sel(k)} run data merge entity @s {{teleport_duration:8}}',
              f'execute as {shell_sel(k)} at {lock_sel(k)} run tp @s ~ ~0.6 ~', f'execute at {shell_sel(k)} run {K.snd("shell_dive")}')
        tl.at(SHELL_HIT[k], f'kill @e[type={ID},tag=rlk_mb_az_p44s{k}]', f'kill @e[type={MK},tag=rlk_mb_az_p44l{k}]')
    tl.at(ICICLE_END, g.play('idle'))
    tl.span(ICICLE_END, SHELL_LAUNCH[-1], 'function rlk:mboss/mv/turn {max:2}')
    tl.at(SHELL_END, g.end())
    tl.write(['# 44 번개의 가루 (Electro shells): tail_cast with the spark column (the tell), 8 shells from the tail tip every 5 t from',
              f'# fire into a hover cloud 7-9 b up over the front; each shell locks the player\'s feet 4 t before its dive',
              f'# (a flash + a sound on the shell), dives in 8 t: disc r {SHELL_R}, tell 12, 0.6 + brand, groups of 4; no ground',
              '# decal (plan Change note 1). The body idles and tracks <= 2 deg/t until the last dive.'],
             ['# 44 tick (#azPT = the tail_cast tick).'])
    for k in range(SHELL_N):
        grp = 'new' if k % 4 == 0 else 'join:#aq44G'
        g.pw(key, f'lock_{k}', [f'# Shell {k + 1}: the lock (the player\'s feet), the hazard (dive 8 t after the launch in 4 t), the cue.',
                                g.lockp(), *H.keep_lock(f'rlk_mb_az_p44l{k}', 'rlk_mb_az_p44'),
                                *hz(g, V44, grp=grp), f'execute at {lock_sel(k)} run {L.hz_disc(SHELL_R, 12, DMG["o44"])}',
                                g.tag_last_hz('rlk_mb_az_p44')]
             + (['scoreboard players operation #aq44G mb = #mbGrp mb'] if k % 4 == 0 else [])
             + [f'execute at {shell_sel(k)} run particle minecraft:flash{{color:[0.773f,0.545f,1f,1f]}} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]',
                f'execute at {shell_sel(k)} run {g.particle("electric_spark", delta=(0.3, 0.3, 0.3), speed=0.1, n=8)}',
                f'execute at {shell_sel(k)} run {g.sound("block.amethyst_block.chime", 1.0, 1.9)}'])
    g.pw(key, 'vis', [f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V44} run {F("p/shell/impact")}'])
    g.pw(key, 'impact', [K.fx('shell_dive'), K.snd('shell_impact')])
    g.pw(key, 'cancel', ['# Shells, locks and live dives go (selectors only).', 'kill @e[tag=rlk_mb_az_p44]'])


# ============================================================================================================ 45 icespike
def f45(i):
    return H.sel(f'rlk_mb_az_p45f{i}')


def spike_launch(g, pid, el):
    """t14: three spikes leave the back (launch_1..3) and shoot up out of sight (6 t)."""
    out = []
    for i in (1, 2, 3):
        p = A.anchor('spikes', 'launch', f'launch_{i}')
        out += [at_body(p, f'summon {ID} ~ ~ ~ {{Tags:{H.tags(pid, f"rlk_mb_az_p{pid}u")},teleport_duration:1}}')]
    out += [f'execute as @e[type={ID},tag=rlk_mb_az_p{pid}u] run {K.prope("spike", el)}']
    return out


def icespike(g):
    key, pid = 'icespike', 45
    tl = TL(g, key)
    tl.at(0, g.glow(True), at_body(A.REST['back'], g.particle('snowflake', delta=(1.2, 0.6, 1.2), speed=0.02, n=10)),
          f'execute unless entity @e[type={MK},tag=rlk_mb_az_p45h,limit=1] run {sc("#aq45H", 0)}')
    tl.at(SPIKE_LAUNCH, *spike_launch(g, pid, 4), K.snd('ice_launch'))
    tl.at(SPIKE_LAUNCH + 1, f'execute as @e[type={ID},tag=rlk_mb_az_p45u] run data merge entity @s {{teleport_duration:6}}',
          f'execute as @e[type={ID},tag=rlk_mb_az_p45u] at @s run tp @s ~ ~22 ~')
    tl.at(SPIKE_LAUNCH + 7, f'kill @e[type={ID},tag=rlk_mb_az_p45u]')
    tl.at(A.ev('spikes', 'gold_off'), g.glow(False))
    tl.at(ICE_FIELDS, F('p/icespike/fields'))
    for i, b in enumerate(ICE_BURST):
        tl.at(b - 7, f'execute at {f45(i)} run summon {ID} ~ ~14 ~ {{Tags:{H.tags(pid, f"rlk_mb_az_p45d{i}")},teleport_duration:1}}',
              f'execute as @e[type={ID},tag=rlk_mb_az_p45d{i}] run {K.prope("spike", 4)}',
              f'execute as @e[type={ID},tag=rlk_mb_az_p45d{i}] run data merge entity @s {{transformation:{{left_rotation:[1f,0f,0f,0f]}}}}')
        tl.at(b - 6, f'execute as @e[type={ID},tag=rlk_mb_az_p45d{i}] run data merge entity @s {{teleport_duration:5}}',
              f'execute as @e[type={ID},tag=rlk_mb_az_p45d{i}] at {f45(i)} run tp @s ~ ~2.3 ~')
        tl.at(b - 1, f'execute at {f45(i)} run {K.snd("ice_land")}', f'execute at {f45(i)} run {K.fxe("dust_ring", 4, r=1.5)}')
        if i < 2:          # the hail starts 1 t after its burst (the burst tick already carries the eruption cards)
            tl.at(b + 1, f'execute at {f45(i)} run {F("p/icespike/hail")}')
        tl.at(b + 8, f'kill @e[type={ID},tag=rlk_mb_az_p45d{i}]')
    tl.at(ICE_END, g.end())
    tl.write(['# 45 천동만상 – 얼음 가시 (Cryo, replaces P4 in phase 3): the back glows t0-22; 3 dark spikes up at t14; the star',
              f'# fields at t{ICE_FIELDS} (keep: star seal + rune, plan Change note 1) with their bursts at {list(ICE_BURST)} (the',
              f'# spike lands 1 t before), r {ICE_R}, 1.0 Cryo + stack, own group each; hail in F1 / F2 for {ICE_HAIL} t.'],
             ['# 45 tick (#azPT = the spikes clip tick).'])
    lines = ['# t26: F1 = lockv (lead 30); F2 = F1 + 5 b along the velocity (a standing player: along the boss -> player line);',
             '# F3 = random 6-10 b from the player; each in the walk disc; the star seals and their hazards.',
             *g.lockv(30), *H.keep_lock('rlk_mb_az_p45f0', 'rlk_mb_az_p45'),
             f'execute at {f45(0)} run summon {MK} ~ ~ ~ {{Tags:{H.tags(pid, "rlk_mb_az_p45f1")}}}',
             f'execute if score #mbV mb matches 81.. as {f45(1)} at @s if entity {PLAYER} facing entity {PLAYER} feet rotated ~ 0 run tp @s ^ ^ ^-5',
             f'execute unless score #mbV mb matches 81.. as {f45(1)} at @s facing entity {BODY} feet rotated ~ 0 run tp @s ^ ^ ^-5',
             f'execute at {PLAYER} run summon {MK} ~ {CY} ~ {{Tags:{H.tags(pid, "rlk_mb_az_p45f2")}}}',
             f'execute as {f45(2)} store result entity @s Rotation[0] float 1 run random value 0..359',
             'execute store result storage rlk:mboss az.p45.d int 1 run random value 6..10',
             f'execute as {f45(2)} at @s rotated as @s run function {NS}p/icespike/mv with storage rlk:mboss az.p45']
    for i, b in enumerate(ICE_BURST):
        lines += [f'execute as {f45(i)} run {g.clamp_walk()}', f'execute at {f45(i)} run {F(f"p/icespike/f{i}")}']
    g.pw(key, 'fields', lines)
    g.pw(key, 'mv', ['$tp @s ^ ^ ^$(d)'])
    for i, b in enumerate(ICE_BURST):
        tell = b - ICE_FIELDS
        g.pw(key, f'f{i}', [f'# Positioned at F{i + 1}: the star seal (keep) and its burst disc r {ICE_R}, tell {tell}, own group.',
                            K.tele_starseal(ICE_R, tell, el=4, hold=3), *hz(g, V45), L.hz_disc(ICE_R, tell, DMG['o45']),
                            g.tag_last_hz('rlk_mb_az_p45')])
    g.pw(key, 'hail', [f'# Positioned at F1 / F2 1 t after its burst: the hail field (N6) r {ICE_R} / {ICE_HAIL} t (never stacks Cryo); the',
                       '# hail keeps falling in it (one ambience chain for every live 45 hail field, every 8 t).',
                       *g.field('hail', ICE_R, ICE_HAIL, DMG['hail'], el='tail'), g.tag_last_hz('rlk_mb_az_p45h'),
                       K.fx('hail', r=ICE_R), K.snd('hail'),
                       f'execute unless score #aq45H mb matches 1 run {F("p/icespike/hail_go")}'])
    g.pw(key, 'hail_go', [sc('#aq45H', 1), *g.after(8, 'p/icespike/hail_amb')])
    amb = g.after(8, 'p/icespike/hail_amb')
    g.pw(key, 'hail_amb', ['# Hail ambience over every live 45 hail field (the field pool card is the floor read); the chain ends',
                           '# with the last field.', sc('#aq45H', 0),
                           f'execute as @e[type={MK},tag=rlk_mb_az_p45h] at @s run {K.fx("hail", r=ICE_R)}',
                           f'execute at @e[type={MK},tag=rlk_mb_az_p45h,limit=1] run {K.snd("hail")}',
                           f'execute if entity @e[type={MK},tag=rlk_mb_az_p45h,limit=1] run {sc("#aq45H", 1)}']
         + [f'execute if score #aq45H mb matches 1 run {ln}' for ln in amb])
    g.pw(key, 'vis', [f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V45} run {F("p/icespike/erupt")}',
                      f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {VX_WALL} run {F("xt/whip_sweep/wall_fx")}'])
    g.pw(key, 'erupt', [K.fx('frost_burst', r=ICE_R), K.snd('ice_erupt')])
    g.pw(key, 'cancel', ['# Spikes, field markers and pending bursts go (selectors only); the glow ends.', 'kill @e[tag=rlk_mb_az_p45]',
                         g.glow(False)])
    res = ['# Resume: the star seals of the pending bursts again with their remaining tells.']
    for i, b in enumerate(ICE_BURST):
        prep, call = H.tele_dyn('starseal', {'tell': '#aq45W'}, r=ICE_R, el=4, hold=3)
        res += [sc('#aq45W', b), 'scoreboard players operation #aq45W mb -= #azPT mb'] + prep
        res.append(f'execute if score #azPT mb matches {ICE_FIELDS}.. if score #aq45W mb matches 1.. at {f45(i)} run {call}')
    g.pw(key, 'resume', res)


# ============================================================================================================ 46 elspike
H46 = H.sel('rlk_mb_az_p46h')


def l46(i):
    return H.sel(f'rlk_mb_az_p46l{i}')


def elspike(g):
    key, pid = 'elspike', 46
    tl = TL(g, key)
    tl.at(0, g.glow(True), at_body(A.REST['back'], g.particle('electric_spark', delta=(1.2, 0.6, 1.2), speed=0.1, n=10)))
    tl.at(SPIKE_LAUNCH, *spike_launch(g, pid, 3), K.snd('spikes_launch'))
    tl.at(SPIKE_LAUNCH + 1, f'execute as @e[type={ID},tag=rlk_mb_az_p46u] run data merge entity @s {{teleport_duration:6}}',
          f'execute as @e[type={ID},tag=rlk_mb_az_p46u] at @s run tp @s ~ ~22 ~')
    tl.at(SPIKE_LAUNCH + 7, f'kill @e[type={ID},tag=rlk_mb_az_p46u]')
    tl.at(A.ev('spikes', 'gold_off'), g.glow(False))
    tl.at(HEX_T, F('p/elspike/hex1'))
    for i, t in enumerate(LUMP_HIT):
        tl.at(t - LUMP_LOCK, F(f'p/elspike/lump_{i}'))
        tl.at(t - 5, f'execute as @e[type={ID},tag=rlk_mb_az_p46p{i}] run data merge entity @s {{teleport_duration:5}}',
              f'execute as @e[type={ID},tag=rlk_mb_az_p46p{i}] at {l46(i)} run tp @s ~ ~0.7 ~')
        tl.at(t - 3, f'execute at {l46(i)} run {K.fx("bolt")}', f'execute at {l46(i)} run {K.snd("hex_bolt")}')
        tl.at(t + 1, f'kill @e[type={ID},tag=rlk_mb_az_p46p{i}]', f'kill @e[type={MK},tag=rlk_mb_az_p46l{i}]')
    tl.at(EL_END, f'kill @e[type={MK},tag=rlk_mb_az_p46h]', g.end())
    tl.write(['# 46 천동만상 – 번개 가시 (Electro, replaces P4 in phase 3): the back glows t0-22, spikes up at t14; the hexagram',
              f'# (keep: a zone marker, plan Change note 1) at lockv (lead 10) at t{HEX_T}, redrawn under a player > 8 b away',
              f'# before a lump; 6 lumps at {list(LUMP_HIT)}: each locks the player\'s feet {LUMP_LOCK} t before (the lump hovers',
              f'# over the lock, falls in the last 5 t, a bolt at -3), disc r {LUMP_R}, 0.7 + brand, groups (1,2) (3,4) 5 6.'],
             ['# 46 tick (#azPT = the spikes clip tick).'])
    g.pw(key, 'hex1', ['# t26: the hexagram at the predictive lock (lead 10); it stays to the end of the pattern.',
                       *g.lockv(10), *H.keep_lock('rlk_mb_az_p46h', 'rlk_mb_az_p46'),
                       f'execute as {H46} run {g.clamp_walk()}',
                       f'execute at {H46} run {K.tele_hexagram(HEX_R, LUMP_HIT[0] - HEX_T, el=3, hold=EL_END - LUMP_HIT[0])}',
                       f'execute at {H46} run {K.snd("hex_draw")}'])
    for i, t in enumerate(LUMP_HIT):
        grp = 'new' if i in (0, 2, 4, 5) else 'join:#aq46G'
        lk = f'rlk_mb_az_p46l{i}'
        g.pw(key, f'lump_{i}', [
            f'# Lump {i + 1} (impact t{t}): a new hexagram under a player farther than 8 b from the current one; the lock (the',
            f'# player\'s feet), the disc r {LUMP_R} (tell {LUMP_LOCK}), the lump hovering {LUMP_H:g} b over the lock.',
            f'execute at {H46} unless entity {PLAYER.replace("limit=1", "distance=..8,limit=1")} run {F(f"p/elspike/hex_{i}")}',
            f'execute unless entity {H46} run {F(f"p/elspike/hex_{i}")}',
            g.lockp(), *H.keep_lock(lk, 'rlk_mb_az_p46'),
            *hz(g, V46, grp=grp), f'execute at {H.sel(lk)} run {L.hz_disc(LUMP_R, LUMP_LOCK, DMG["o46"])}',
            g.tag_last_hz('rlk_mb_az_p46')]
            + (['scoreboard players operation #aq46G mb = #mbGrp mb'] if grp == 'new' else [])
            + [f'execute at {H.sel(lk)} run summon {ID} ~ ~{num(LUMP_H)} ~ {{Tags:{H.tags(pid, f"rlk_mb_az_p46p{i}")},teleport_duration:1}}',
               f'execute as @e[type={ID},tag=rlk_mb_az_p46p{i}] run {K.prop("elump")}',
               f'execute at {H.sel(lk)} positioned ~ ~{num(LUMP_H)} ~ run {g.particle("electric_spark", delta=(0.4, 0.4, 0.4), speed=0.1, n=6)}',
               f'execute at {H.sel(lk)} positioned ~ ~{num(LUMP_H)} ~ run {g.sound("block.amethyst_block.resonate", 0.7, 1.5)}'])
        g.pw(key, f'hex_{i}', [f'# A new hexagram under the player (lump {i + 1}): to the end of the pattern.',
                               f'kill @e[type={MK},tag=rlk_mb_az_p46h]', g.lockp(), *H.keep_lock('rlk_mb_az_p46h', 'rlk_mb_az_p46'),
                               f'execute at {H46} run {K.tele_hexagram(HEX_R, LUMP_LOCK, el=3, hold=EL_END - t)}',
                               f'execute at {H46} run {K.snd("hex_draw")}'])
    g.pw(key, 'vis', [f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {V46} run {F("p/elspike/impact")}',
                      f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {VX_BOLT} run {F("xt/bolt_fx")}',
                      f'execute if score #hzEv mb matches 1 if score @s mbHzV matches {VX_LINE} run {F("xt/whip_end/line_fx")}'])
    g.pw(key, 'impact', [K.fxe('impact', 3), K.snd('hex_impact')])
    g.pw(key, 'cancel', ['# The hexagram marker, locks, lumps, spikes and pending lumps go (selectors only); the glow ends.',
                         'kill @e[tag=rlk_mb_az_p46]', g.glow(False)])
    prep, call = H.tele_dyn('hexagram', {'hold': '#aq46W'}, r=HEX_R, tell=1, el=3)
    g.pw(key, 'resume', ['# Resume: the live hexagram again (it stays to the end of the pattern).',
                         sc('#aq46W', EL_END), 'scoreboard players operation #aq46W mb -= #azPT mb',
                         f'execute unless score #azPT mb matches {HEX_T}..{EL_END - 2} run return 0'] + prep + [f'execute at {H46} run {call}'])


# ============================================================================================================ addons (xt)
CRING = (1.5, 6.0, 0.75, 1.5)                         # frost ring front r0 -> r1 at spd, band (plan 4.6)
CRING_STRIKE = 14                                     # E + 2 from the call at E - 12
BOLT3 = (4.0, 7.0, 10.0)
BOLT_X_R = 1.8


def x_cring(g, rel, grp):
    """A frost ring (N10 front without a decal, Change note 1): the hazard now (tell 14 -> strike E+2), the kit front 1 t
    before the strike, the per-tick growth by the shared chain xt/cring/step."""
    r0, r1, spd, band = CRING
    n = int(round((r1 - r0) / spd))
    assert band >= spd
    lines = [f'# Cryo frost ring (plan 4.6): r {r0} -> {r1} at {spd} b/t, band {band}, from E+2, x_cring + a Cryo stack;',
             '# no pre-strike decal (Change note 1): the host impact and the travelling front are the read.',
             *hz(g, 0, grp=grp, act=n + 1, y1=0.7), L.hz_ring(0, r0, CRING_STRIKE, DMG['x_cring']),
             g.tag_last_hz('rlk_mb_az_x'), g.tag_last_hz('rlk_mb_az_xcr'),
             'execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr] if score @s mbHzI = #hzLast mb run scoreboard players set @s azT 0',
             *g.after(CRING_STRIKE - 1, 'xt/cring/go')]
    g.xw(rel, lines)


def x_bolts(g, rel, grp, tells, dists=BOLT3, extra=()):
    lines = [f'# Electro bolt discs r {BOLT_X_R} at {", ".join(f"{d:g}" for d in dists)} b along the context line, strikes '
             f'{", ".join(f"E{t - 12:+d}" for t in tells)}; x_bolt; no decal (Change note 1): the bolt fx on the strike.']
    first = True
    for d, t in zip(dists, tells):
        gg = grp if (grp == 'ctx' or first) else 'join:#axtG'
        lines += hz(g, VX_BOLT, grp=gg) + [f'execute positioned ^ ^ ^{num(d)} run {L.hz_disc(BOLT_X_R, t, DMG["x_bolt"])}',
                                            g.tag_last_hz('rlk_mb_az_x')]
        if first and grp == 'new':
            lines.append('scoreboard players operation #axtG mb = #mbGrp mb')
        first = False
    g.xw(rel, lines + list(extra))


def addons(g):
    # the shared frost-ring chain: the front preset 1 t before the strike, then one resize per tick
    r0, r1, spd, band = CRING
    n = int(round((r1 - r0) / spd))
    g.xw('cring/go', ['# 1 t before the strike (as the body at the ring centre): the kit\'s travelling Cryo front, the sound,',
                      '# then the growth chain from the strike + 1.',
                      K.fxe('front', 4, r0=r0, r1=r1, w=band, dur=n), g.sound('block.powder_snow.break', 1.0, 0.8),
                      g.sound('block.glass.break', 0.6, 1.4), *g.after(2, 'xt/cring/step')])
    step = ['# One growth tick of every live frost ring (azT = ticks since the strike); the chain runs while one lives.',
            'execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr] run scoreboard players add @s azT 1']
    for k in range(1, n + 1):
        r = r0 + spd * k
        step.append(f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={{azT={k}}}] run {L.hz_resize(r, max(0.0, r - band))}')
    step += [f'tag @e[type=minecraft:marker,tag=rlk_mb_az_xcr,scores={{azT={n}..}}] remove rlk_mb_az_xcr',
             *[f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_xcr,limit=1] run {ln}' for ln in g.after(1, 'xt/cring/step')]]
    g.xw('cring/step', step)
    g.xw('bolt_fx', ['# @s = an addon bolt hazard on its strike: the bolt and its crackle.', K.fx('bolt'),
                     g.sound('entity.lightning_bolt.impact', 0.7, 1.3)])
    # chin/impact: Cryo ring (own group), Electro bolts along the crack line (one group, E+12 / 15 / 18)
    x_cring(g, 'chin_impact/cryo', 'new')
    x_bolts(g, 'chin_impact/electro', 'new', (24, 27, 30))
    # jump: the ring in the landing group; wave 2: bolts toward the player in the wave-2 group (E+2 / 4 / 6)
    x_cring(g, 'jump_land/cryo', 'ctx')
    x_bolts(g, 'jump_wave2/electro', 'ctx', (14, 16, 18))
    # stomp / stomp3: rings in w1's / s1's group; bolts in w3's / s3's group
    x_cring(g, 'stomp_w1/cryo', 'ctx')
    x_bolts(g, 'stomp_w3/electro', 'ctx', (14, 16, 18))
    x_cring(g, 'stomp3_s1/cryo', 'ctx')
    x_bolts(g, 'stomp3_s3/electro', 'ctx', (14, 16, 18))
    whip_sweep(g)
    whip_end(g)
    # tailslam/impact: the strips along the line from E+2 (s2.md 15 decision 8)
    for el in ('cryo', 'electro'):
        g.xw(f'tailslam_impact/{el}', [f'# P8 {el} strip (plan 4.6): along the line (len 13, w 3.5) for 60 t from E+2, x_strip / 10 t + brand.',
                                       *g.after(14, f'xt/tailslam_impact/{el}_strip')])
        g.xw(f'tailslam_impact/{el}_strip', ['# E+2 (as the body at the tail root, rotated along the line): the strip field.',
                                             *g.field('strip', 0, 60, DMG['x_strip'], el='tail', shape='line', len=13, w=3.5)])


SIDES = ((1, 'tail_whip_l'), (-1, 'tail_whip_r'))


def whip_sweep(g):
    lines = ['# P7 whip/sweep (Cryo, plan 4.6): four ice-wall pieces on the swept arc (annular sectors r 5-12 about the tail',
             '# root), erupting 2 t behind the tail at E+2 / 4 / 6 / 8, one own group, x_wall + a stack; a hail strip (line',
             '# len 7 w 3.5, 60 t) on the band where the sweep ends follows the last piece (s2.md 15 decision 8). Context: the',
             '# tail root at E, rotated as the anchor\'s start yaw; the pieces come from the manifest track x yaw schedule.',
             g.GRP_NEW, 'scoreboard players operation #axtG mb = #mbGrp mb']
    for side, clip in SIDES:
        cond = f'execute if score #azCtxSide mb matches {side} '
        for p in H.wall_pieces(clip):
            ds, df = p['off']
            lines += [f'{cond}run {ln}' for ln in hz(g, VX_WALL, grp='join:#axtG', r0=5.0)]
            lines.append(f'{cond}positioned ^{num(ds)} ^ ^{num(df)} rotated ~{num(p["mid"], 2)} 0 run '
                         f'{L.hz_sector(A.WHIP_REACH, p["half"], 12 + p["t"], DMG["x_wall"])}')
            lines.append(f'{cond}run {g.tag_last_hz("rlk_mb_az_x")}')
        (es, ef), ey = H.whip_end(clip)
        aft = g.after(20, 'xt/whip_sweep/hail')
        lines += [f'{cond}run {aft[0]}', f'{cond}run {aft[1]}',
                  f'{cond}positioned ^{num(es)} ^ ^{num(ef)} rotated ~{num(ey, 2)} 0 positioned ^ ^ ^5 run {aft[2]}']
    g.xw('whip_sweep/cryo', lines)
    g.xw('whip_sweep/hail', ['# E+8 (as the body, 5 b along the end line from the tail root, rotated along it): the hail strip.',
                             *g.field('hail', 0, 60, DMG['x_hail'], el='tail', shape='line', len=7, w=3.5)])
    g.xw('whip_sweep/wall_fx', ['# @s = a wall piece on its strike (at the tail root, rotated to the piece\'s mid angle): ice walls.',
                                f'execute positioned ^ ^ ^6.5 run {K.fx("ice_wall")}', f'execute positioned ^ ^ ^10 run {K.fx("ice_wall")}',
                                g.sound('block.glass.break', 0.8, 0.7), g.sound('block.amethyst_cluster.break', 0.8, 0.8)])


def whip_end(g):
    ev = A.CLIPS['tail_whip_l']['events']
    e = ev['erupt']
    lines = ['# P7 whip/end (Electro, plan 4.6): 3 bolt discs r 1.8 at 4 / 8 / 12 b along the end line at E+3 and a crystal',
             '# line (hz/line len 12 w 2.4) at E+13, all one group, x_wline; the Electro strip (line len 12 w 4, 80 t, x_estrip)',
             '# from E+15; violet arcs crawl along the tail until the bolts (body fx, the tell). Context: the end-line point,',
             '# rotated along the end line.',
             g.GRP_NEW, 'scoreboard players operation #axtG mb = #mbGrp mb']
    for d in (4.0, 8.0, 12.0):
        lines += hz(g, VX_BOLT, grp='join:#axtG') + [f'execute positioned ^ ^ ^{num(d)} run {L.hz_disc(BOLT_X_R, 15, DMG["x_wline"])}',
                                                     g.tag_last_hz('rlk_mb_az_x')]
    lines += hz(g, VX_LINE, grp='join:#axtG') + [L.hz_line(12.0, 2.4, 25, DMG['x_wline']), g.tag_last_hz('rlk_mb_az_x')]
    lines += [*g.after(27, 'xt/whip_end/strip'), sc('#axtArc', 0), F('xt/whip_end/arc')]
    g.xw('whip_end/electro', lines)
    g.xw('whip_end/strip', ['# E+15 (as the body at the end-line point, rotated along it): the Electro strip.',
                            *g.field('strip', 0, 80, DMG['x_estrip'], el='tail', shape='line', len=12, w=4.0)])
    g.xw('whip_end/line_fx', ['# @s = the crystal line on its strike: violet crystals along it.', K.fxe('spike_line', 3, len=12.0),
                              g.sound('block.amethyst_cluster.break', 1.0, 1.0)])
    # the arc chain: as the body, one tick at a time from the call (E - 12) to the bolts (E + 3)
    arc = ['# Violet arcs along the raised / sweeping tail (manifest tracks, the body frame), one tick per call while the',
           '# whip runs, until the bolts strike.', 'scoreboard players add #axtArc mb 1']
    for side, clip in SIDES:
        root, tip = A.track(clip, 'tail_root'), A.track(clip, 'tail_tip')
        for t in range(e - 12, e + 4):
            pts = []
            for u in (0.35, 0.6, 0.85):
                p = tuple(root[t][i] + (tip[t][i] - root[t][i]) * u for i in range(3))
                pts.append(f'execute at @s rotated as @s rotated ~ 0 positioned ^{num(p[0])} ^{num(p[1])} ^{num(p[2])} run '
                           + g.particle('electric_spark', delta=(0.4, 0.4, 0.4), speed=0.12, n=3))
            g.xw(f'whip_end/arc_{"l" if side == 1 else "r"}{t}', pts)
            arc.append(f'execute if score #azPat mb matches 7 if score #azSide mb matches {side} if score #azPT mb matches {t} run '
                       f'{F("xt/whip_end/arc_" + ("l" if side == 1 else "r") + str(t))}')
    aft = g.after(1, 'xt/whip_end/arc')
    arc += [f'execute if score #axtArc mb matches ..15 if score #azPat mb matches 7 run {ln}' for ln in aft]
    g.xw('whip_end/arc', arc)


# ============================================================================================================ emit
def emit(g):
    frost(g)
    bolt(g)
    icicle(g)
    shell(g)
    icespike(g)
    elspike(g)
    addons(g)
