"""Sequences of the human-pattern author: S1 the entrance (cocoon), S3 the revert drift, the groggy, the turn and the
chain re-form, S4 death (scratchpad specs mb2/spec/S1_entrance.md, S3_revert_groggy_reform.md, S4_death.md).

Visual and audio only. The core keeps every mechanic of these sequences (the clocks and states, the rig clips, the
cocoon prop and its removal at the burst, the sub-line title, the hitbox, the heal orbs, the debuff, the timers, the
rig kill) and calls one function here from each of its hooks (the lines marked "[seq_h: human author]" in core.py):

    intro/setup      -> seq_h/entrance/setup     (the spawn tick: the floor disc under the cocoon)
    intro_tick       -> seq_h/entrance/tick      (#mbT = intro clock = entrance clip tick + core.INTRO_CLIP)
    form/revert      -> seq_h/revert             (달빛 해제 clock 92: she is human again, 1.5-2 b up)
    groggy/begin     -> seq_h/groggy/begin       (#bfT 0)
    groggy/tick      -> seq_h/groggy/tick        (#bfT 1..300)
    recover/begin    -> seq_h/recover/begin      (#bfT 0: the turn)
    recover/tick     -> seq_h/recover/tick       (#bfT 1..42: turn 24 t, chain re-form 18 t)
    death_start      -> seq_h/death/start        (@s = body)
    death_tick       -> seq_h/death/tick         (#mbT 1..100 = death clip tick)

The release clip's own fx at 87 (shrink / flat), 91 (shatter) and the landing at 96 belong to B5 (wing.py). Files:
F:mboss/butterfly/seq_h/** (written through gen.w, owned by the module generator like every B: path).
"""
import math
import random

from . import api as A
from .api import CY

hx = A.hexrgb
BODY = 'execute at @s rotated as @s rotated ~ 0 run '
NAVY = '#394B75'
SEQ = 'seq_h'


class Clock:
    """Per-tick timeline of a sequence on a core clock (fake player `score` in mb; clock value = tick + off): one-off
    ticks go to seq_h/<name>/k/<t> behind a binary dispatch, periodic groups to seq_h/<name>/e<n>_<t0> called from
    modulo tests (core moduli #bfK<n>)."""

    def __init__(self, g, name, score, off=0):
        self.g, self.name, self.score, self.off = g, name, score, off
        self.ev, self.per = {}, []

    def at(self, t, *lines):
        for line in lines:
            if line:
                self.ev.setdefault(int(t), []).extend(line if isinstance(line, list) else line.split('\n'))

    def every(self, n, t0, t1, *lines):
        assert n in (2, 3, 4, 5, 6, 8, 10, 20, 40), n
        self.per.append((n, t0, t1, [l for x in lines for l in (x if isinstance(x, list) else [x]) if l]))

    def fn(self, rel):
        return f'function {A.NS}{SEQ}/{self.name}/{rel}'

    def w(self, rel, lines):
        self.g.w(f'{SEQ}/{self.name}/{rel}', lines)

    def _node(self, ts):
        c = lambda t: t + self.off                          # noqa: E731
        if len(ts) <= 6:
            return [f'execute if score {self.score} mb matches {c(t)} run return run {self.fn(f"k/{t}")}' for t in ts]
        mid = len(ts) // 2
        out = []
        for part in (ts[:mid], ts[mid:]):
            rel = f'd/{part[0]}_{part[-1]}'
            self.w(rel, [f'# dispatch {self.score} {c(part[0])}..{c(part[-1])}'] + self._node(part))
            out.append(f'execute if score {self.score} mb matches {c(part[0])}..{c(part[-1])} run return run {self.fn(rel)}')
        return out

    def write(self, head):
        out = list(head)
        for i, (n, t0, t1, lines) in enumerate(self.per):
            rel = f'e{i}_{n}_{t0}'
            self.w(rel, [f'# every {n} t, clock ticks {t0}..{t1}'] + lines)
            out += [f'scoreboard players operation #bfM mb = {self.score} mb', f'scoreboard players operation #bfM mb %= #bfK{n} mb',
                    f'execute if score #bfM mb matches {(t0 + self.off) % n} if score {self.score} mb matches '
                    f'{t0 + self.off}..{t1 + self.off} run {self.fn(rel)}']
        for t, lines in sorted(self.ev.items()):
            self.w(f'k/{t}', [f'# {self.name} tick {t}'] + lines)
        out += self._node(sorted(self.ev))
        self.w('tick', out)


def emit(g):
    from . import core as C                                 # the core's clock constants (already imported)
    entrance(g, C)
    groggy(g, C)
    death(g, C)


# =============================================================================================
# S1 the entrance (clip `entrance`, 106 t): the cocoon hovers over a glowing lime floor disc with curling wind streaks,
# the nameplate star at 57, the soft glow at 61 and the rising shimmer at 69 (Q21), the whiteout at 71, god rays at 75,
# the burst into white / cyan / mint crystal shards at 79, the cyan wind, the drop with sparkles and leaves, the
# landing at 90, leaves falling until she stands at 106. No damage (the core keeps her untargetable).
SHIMMER_LEAD = 2                                            # the main rising layers 2 t before the whiteout (69)


def entrance(g, C):
    burst, land, glow, white, name = C.ENT_BURST, C.ENT_LAND, C.ENT_GLOW, C.ENT_WHITE, C.NAMEPLATE
    shimmer = white - SHIMMER_LEAD
    rim = lambda life: BODY + g.kcard('ripple', '^ ^0.05 ^', '~ 90', col='#BCDDD2', s0=8.0, s1=8.2, life=life, fade=0)  # noqa: E731
    hover = (g.h_ring_dust(A.LIME, 1.6, 14, y=0.15, scale=1.2)
             + [g.dust(A.LIME_PALE, 1.0, '~ ~0.12 ~', (0.7, 0.02, 0.7), 4),
                g.dust_fade(A.WHITE, A.CYAN, 0.8, '~ ~2.2 ~', (1.0, 1.4, 1.0), 2),
                g.particle('end_rod', '~ ~2.0 ~', (0.9, 1.3, 0.9), 0.01, 1)])
    g.w(f'{SEQ}/entrance/setup', [
        '# S1 at the spawn (@s = the new body, at it, facing the arriving player): the glowing lime floor disc under the',
        '# cocoon until the burst (kit cocoon_disc), its pale rim (refreshed every 20 t), the faint hum, the first hover.',
        f'execute positioned ~ {CY} ~ run ' + g.fx('cocoon_disc', life=C.INTRO_CLIP + burst),
        rim(20), g.sound('block.beacon.ambient', 0.3, 1.6)] + hover)
    ck = Clock(g, 'entrance', '#mbT', off=C.INTRO_CLIP)
    ck.every(4, 4, burst - 3, hover)
    rnd = random.Random(57)
    for t in range(8, burst - 6, 8):                        # a curling wind streak every 8 t
        ck.at(t, BODY + g.kcard('streak', '^ ^2.0 ^', f'~{rnd.randint(0, 359)} 0', col='#E6F6F8', roll=rnd.randint(-40, 40),
                                spin=90, s0=1.5, s1=2.5, life=6, fade=2))
    for t in (20, 40, 60):
        ck.at(t, rim(min(20, C.INTRO_CLIP + burst - t)))
    for t in (0, 20, 40):
        ck.at(t, 'execute positioned ~ ~2.0 ~ run ' + g.fx('motes'))
    ck.at(40, g.sound('block.beacon.ambient', 0.3, 1.6))
    ck.at(name, BODY + g.kcard('glint', '^ ^3.9 ^', bb='center', col='#E5FBC8', s0=0.3, s1=1.4, life=6, fade=3),
          g.sound('block.amethyst_block.resonate', 0.7, 1.2), g.sound('block.beacon.ambient', 0.4, 1.6))
    # the glow (soft), the rays from the seams, the rising shimmer, the whiteout, the god rays
    ck.at(glow, 'execute positioned ~ ~2.1 ~ run ' + g.fx('cocoon_glow'),
          BODY + g.kcard('glow', '^ ^2.6 ^', bb='center', col='#CADE48', s0=0.8, s1=1.6, life=10, fade=2),
          g.sound('block.respawn_anchor.charge', 0.35, 1.6))
    ck.every(2, glow, burst - 1, g.dust(hx('#D5F086'), 1.4, '~ ~2.1 ~', (0.35, 0.9, 0.35), 6),
             g.particle('end_rod', '~ ~2.1 ~', (0.25, 0.8, 0.25), 0.06, 2))
    ck.at(shimmer, g.snd('cocoon_glow'),
          BODY + g.kcard('glow', '^ ^2.6 ^', bb='center', col='#CADE48', s0=1.0, s1=1.8, life=10, fade=2))
    ck.at(white, 'execute positioned ~ ~2.1 ~ run ' + g.fx('whiteout'), g.khud('flash_white'),
          g.dust(hx('#F8FFC0'), 2.6, '~ ~2.1 ~', (0.7, 1.2, 0.7), 30),
          g.particle('end_rod', '~ ~2.1 ~', (0.3, 0.6, 0.3), 0.12, 16),
          g.particle('flash{color:[0.97,1.0,0.75,1.0]}', '~ ~2.1 ~', (0, 0, 0), 0, 1),
          g.sound('block.beacon.activate', 0.6, 1.8))
    ck.at(white + 4, *[BODY + g.kcard('streak', '^ ^2.1 ^', '~ 0', col='#F8FFC0', roll=60 * i, s0=3.0, s1=5.0, life=4, fade=1)
                       for i in range(6)],
          g.sound('block.respawn_anchor.charge', 0.5, 1.8))
    # the burst (the core clears the cocoon prop on this tick)
    ck.at(burst, 'execute rotated as @s rotated ~ 0 positioned ~ ~2.2 ~ run ' + g.fx('cocoon_burst'), g.snd('cocoon_burst'),
          g.particle('block{block_state:"minecraft:white_stained_glass"}', '~ ~2.2 ~', (1.2, 1.5, 1.2), 0, 36),
          g.particle('block{block_state:"minecraft:light_blue_stained_glass"}', '~ ~2.2 ~', (1.0, 1.3, 1.0), 0, 22),
          g.dust(A.CYAN_DEEP, 1.2, '~ ~2.2 ~', (1.2, 1.2, 1.2), 12))
    for t in range(burst + 1, burst + 4):
        ck.at(t, g.dust_fade(A.WHITE, A.CYAN_DEEP, 1.0, '~ ~4.5 ~', (1.5, 1.0, 1.5), 6))
    # the drop: white sparkles over the floor, lime leaves, the glittering tail
    ck.at(burst + 3, g.snd('cocoon_tail'))
    rnd = random.Random(79)
    for i, t in enumerate(range(burst + 3, land, 3)):
        r, a = rnd.uniform(0.4, 2.0), rnd.uniform(0, 2 * math.pi)
        ck.at(t, g.particle('wax_off', '~ ~1.0 ~', (1.6, 0.6, 1.6), 0, 2),
              g.particle('end_rod', '~ ~3.0 ~', (1.0, 0.6, 1.0), 0.01, 1),
              *[BODY + g.kcard('leaf', f'^{x} ^3.6 ^0.2', bb='center', col='#A8DF74', s0=0.3, s1=0.35, move=(0, -2, 0),
                               life=14, fade=6) for x in (-0.4, 0.4)],
              g.kcard('glint', f'~{A.L.num(r * math.cos(a), 2)} ~0.25 ~{A.L.num(r * math.sin(a), 2)}', bb='center',
                      col='#FFFFFF', s0=0.2, s1=0.6, life=4, fade=2))
        if i:
            ck.at(t, g.sound('block.amethyst_block.chime', (0.6, 0.5)[(i - 1) % 2], (1.5, 1.7)[(i - 1) % 2]))
    # the landing crouch
    ck.at(land, g.fx('land'), g.snd('land'), g.sound('block.moss.fall', 0.9, 1.0),
          g.particle('poof', '~ ~0.15 ~', (0.6, 0.05, 0.6), 0.03, 10),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.7, 0.05, 0.7), 0, 14),
          g.kcard('ripple', '~ ~0.06 ~', '~ 90', col=A.LIME_HEX, s0=1.0, s1=3.0, life=5, fade=2))
    for t, x in zip(range(land + 4, C.ENT_LEN, 4), (0.5, -0.4, 0.2, -0.6)):
        ck.at(t, BODY + g.kcard('leaf', f'^{x} ^2.6 ^0.2', bb='center', col='#A8DF74', s0=0.3, s1=0.35, move=(0, -2.2, 0.2),
                                life=14, fade=6))
    ck.write(['# S1 entrance (@s = body, at it; #mbT = intro clock = entrance clip tick + 1; visuals and sounds only).',
              f'# Hover every 4 t, streaks every 8 t, nameplate {name}, glow {glow}, shimmer {shimmer}, whiteout {white},',
              f'# god rays {white + 4}, burst {burst}, the drop, landing {land}.'])


# =============================================================================================
# S3: the wing-shard drift at the revert (release 92), the groggy (300 t: dazed motes every 10 t, kit motes every 40 t, a
# faint lime ring at 100 / 200, the stirring at 280), the turn (24 t), the chain re-form (18 t: four navy crescent
# plates fly in and stack at her left side, the clink at +6).
def groggy(g, C):
    g.w(f'{SEQ}/revert', ['# S3 at the revert (달빛 해제 clock 92, @s = body, at it): the shattered wing shards drift around her.',
                          g.dust(hx('#E7FD7A'), 0.8, '~ ~3.0 ~', (1.5, 1.0, 1.5), 8)])
    g.w(f'{SEQ}/groggy/begin', ['# S3 groggy start (@s = body, at it, just landed with her back to the player): spent cue.',
                                g.snd('groggy')])
    ck = Clock(g, 'groggy', '#bfT')
    ck.every(10, 10, C.GROGGY, BODY + g.dust(A.LIME, 0.7, '^ ^2.4 ^', (0.5, 0.3, 0.5), 2),
             BODY + g.particle('end_rod', '^ ^2.6 ^', (0.4, 0.2, 0.4), 0.005, 1))
    ck.every(40, 40, C.GROGGY, 'execute positioned ~ ~1.6 ~ run ' + g.fx('motes'))
    for t in (100, 200):
        ck.at(t, f'execute positioned ~ {CY} ~ run ' + g.kcard('ripple', '~ ~0.06 ~', '~ 90', col=A.LIME_HEX, s0=1.5, s1=2.5,
                                                              life=8, fade=4),
              g.sound('block.beacon.ambient', 0.25, 0.8))
    ck.at(C.GROGGY - 20, *[BODY + g.kcard('glint', f'^{x} ^2.35 ^-0.2', bb='center', col='#E5FBC8', s0=0.2, s1=0.7, life=4,
                                          fade=2) for x in (0.55, -0.55)],
          g.sound('entity.breeze.idle_air', 0.3, 1.0))
    ck.write([f'# S3 groggy (@s = body, at it; #bfT 1..{C.GROGGY}; no tracking, nothing that moves her): dazed motes, the faint',
              '# rings, the stirring before the turn.'])
    g.w(f'{SEQ}/recover/begin', ['# S3 the turn begins (@s = body).', g.sound('entity.breeze.idle_air', 0.4, 1.2)])
    ck = Clock(g, 'recover', '#bfT')
    chain = '^0.7 ^1.8 ^'                                   # her left side (body frame: ^+x = left)
    hand = A.h_anchor('chain_reform', 'start', 'hand_l_a', '^0.84 ^1.98 ^0.1')
    plates = []
    for i, (phi, dy) in enumerate(((35, 0.5), (75, -0.3), (115, 0.35), (150, -0.45))):
        f = (-math.sin(math.radians(phi)), math.cos(math.radians(phi)))     # its flight direction (^x, ^z)
        x, z = 0.7 - 2.0 * f[0], -2.0 * f[1]
        plates.append(BODY + g.kcard('cres_lime', f'^{A.L.num(x, 2)} ^{A.L.num(1.8 - dy, 2)} ^{A.L.num(z, 2)}', f'~{phi} 0',
                                     col=NAVY, roll=90, s0=0.4, s1=1.1, move=(0, dy, 2.0), life=7, fade=1, dly=i))
    ck.at(C.TURN_T, f'execute rotated as @s rotated ~ 0 positioned {chain} run ' + g.fx('chain_reform'), *plates)
    ck.at(C.TURN_T + 6, g.snd('chain_reform'), BODY + g.dust(A.LIME, 1.1, chain, (0.3, 0.5, 0.3), 10),
          BODY + g.kcard('glow', hand, bb='center', col='#C2E18C', s0=0.4, s1=1.0, life=6, fade=2))
    ck.write([f'# S3 turn ({C.TURN_T} t) + chain re-form ({C.CHAIN_T} t) (@s = body, at it; #bfT 1..{C.TURN_T + C.CHAIN_T}).'])


# =============================================================================================
# S4 death (clip `death`, 100 t; stagger 0, shatter, kneel, dissolve from the manifest): the hit flash and a white
# burst, crack lines, the wings shatter (butterfly form) or the crescent plates crack (human form), the knees buckle, the
# kneel, the dissolve into rising moonlight motes and white-cyan crystal shards with a descending chime, the last motes.
# No creature voices.
def death(g, C):
    sh, kn, dv, ln = C.D_SHATTER, C.D_KNEEL, C.D_DISSOLVE, C.DEATH_LEN
    core = 'execute if score #bfForm mb matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^2.1 ^ run '
    core_b = 'execute if score #bfForm mb matches 2 at @s rotated as @s rotated ~ 0 positioned ^ ^3.2 ^ run '
    g.w(f'{SEQ}/death/start', [
        '# S4 at death_start (@s = body; the core has cancelled everything): the hit flash, a white burst at her core, the',
        '# death recipe (crystal, beacon, wind; no voices).',
        g.rig('flash'),
        core + g.kcard('burst', '~ ~ ~', bb='center', s0=0.8, s1=2.6, life=4, fade=2),
        core_b + g.kcard('burst', '~ ~ ~', bb='center', s0=0.8, s1=2.6, life=4, fade=2),
        'execute at @s run ' + g.particle('flash{color:[0.95,1.0,0.9,0.9]}', '~ ~2.0 ~', (0, 0, 0), 0, 1),
        'execute at @s run ' + g.snd('death')])
    ck = Clock(g, 'death', '#mbT')
    cracks = [g.kcard('streak', '~ ~ ~', bb='center', col='#E5FBC8', roll=r, s0=1.0, s1=1.8, life=4, fade=2) for r in (25, 95, 160)]
    ck.at(4, *[core + c for c in cracks], *[core_b + c for c in cracks], g.sound('block.amethyst_block.break', 0.6, 0.9))
    # #bfWing (the core's death_start): the wings were shown, also in a transformation past its open event (fix S3)
    ck.at(sh, f'execute if score #bfWing mb matches 1 run function {A.NS}{SEQ}/death/shatter_b',
          f'execute unless score #bfWing mb matches 1 run function {A.NS}{SEQ}/death/shatter_h')
    g.w(f'{SEQ}/death/shatter_b', ['# Butterfly form: the wings shatter into lime / opal shards (kit wing_shatter at her back).',
                                   g.particle('block{block_state:"minecraft:lime_stained_glass"}', '~ ~3.0 ~', (1.8, 1.0, 0.6), 0, 30),
                                   g.particle('block{block_state:"minecraft:white_stained_glass"}', '~ ~3.0 ~', (1.6, 1.0, 0.6), 0, 16),
                                   g.dust(A.OPAL, 1.4, '~ ~3.0 ~', (2.0, 1.2, 0.8), 20),
                                   'execute rotated as @s rotated ~ 0 positioned ^ ^2.8 ^-0.4 run ' + g.fx('wing_shatter'),
                                   g.snd('wing_shatter')])
    hands = [A.h_anchor('death', 'shatter', 'hand_r_a', '^-1.05 ^2.92 ^-0.33'), A.h_anchor('death', 'shatter', 'hand_l_a', '^0.84 ^1.95 ^-0.01')]
    shards = []
    for j, hp in enumerate(hands):
        for i in range(2):
            shards.append(BODY + g.kcard('shard', hp, f'~{(-60 if j == 0 else 60) + 50 * i} {40 + 25 * i}', col=NAVY,
                                         roll=20 * i, s0=0.4, s1=0.7, move=(0, 0.9, 0), life=8, fade=4))
    g.w(f'{SEQ}/death/shatter_h', ['# Human form: the crescent plates at her hands crack (navy shards).', *shards,
                                   g.sound('block.glass.break', 0.6, 1.2), g.sound('entity.illusioner.mirror_move', 0.5, 1.4)])
    ck.at(max(sh + 2, kn - 10), g.sound('block.amethyst_block.resonate', 0.5, 0.7))
    ck.at(kn, g.particle('poof', '~ ~0.2 ~', (0.5, 0.05, 0.5), 0.02, 8),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.6, 0.05, 0.6), 0, 10),
          *g.h_ring_dust(A.LIME, 1.0, 12, y=0.15, scale=0.9),
          g.sound('block.moss.fall', 0.8, 0.9), g.sound('entity.iron_golem.step', 0.4, 1.4))
    if dv - 1 >= kn + 4:
        ck.every(4, kn + 4, dv - 1, g.dust(A.LIME_PALE, 0.6, '~ ~1.2 ~', (0.3, 0.3, 0.3), 1))
    ck.at(dv, g.sound('block.beacon.deactivate', 0.7, 1.2), g.sound('block.amethyst_block.resonate', 0.6, 0.8))
    ck.every(2, dv, ln - 4, g.dust(A.LIME_PALE, 1.0, '~ ~1.4 ~', (0.4, 0.9, 0.4), 4),
             g.dust_fade(A.WHITE, A.CYAN, 0.9, '~ ~1.8 ~', (0.4, 0.9, 0.4), 3),
             g.particle('end_rod', '~ ~1.4 ~', (0.35, 0.8, 0.35), 0.03, 2),
             g.particle('block{block_state:"minecraft:light_blue_stained_glass"}', '~ ~1.2 ~', (0.4, 0.8, 0.4), 0, 2))
    # every kit card of the death ends before the fight cleanup's fx/clear at death tick {ln} (review fix perf-5): a card
    # made at tick m with delay d and life L is gone at the end of tick m + d + L, so m + d + L <= ln - 1 (the death
    # motes preset: d + L <= 30, the shards 10, the last glow 6)
    for t in range(dv, ln - 30, 15):
        ck.at(t, 'execute positioned ~ ~1.5 ~ run ' + g.fx('death_motes'))
    rnd = random.Random(100)
    for t in range(dv + 3, ln - 10, 6):                     # crystal shards rising from random body points
        ck.at(t, g.kcard('shard', f'~{A.L.num(rnd.uniform(-0.5, 0.5), 2)} ~{A.L.num(rnd.uniform(0.4, 2.0), 2)} '
                                  f'~{A.L.num(rnd.uniform(-0.5, 0.5), 2)}', bb='center', col='#BAF3E3', roll=rnd.randint(-30, 30),
                         s0=0.4, s1=1.0, move=(0, 2.5, 0), life=10, fade=5))
    for t, p in ((dv + 18, 1.8), (dv + 34, 1.5), (dv + 48, 1.2)):
        if t < ln:
            ck.at(t, g.sound('block.amethyst_block.chime', 0.6, p))
    ck.at(ln - 10, g.snd('death_motes'))
    ck.at(ln - 8, BODY + g.kcard('glow', '^ ^1.2 ^', bb='center', col='#E5FBC8', s0=1.0, s1=2.5, life=6, fade=3))
    ck.at(ln - 4, g.particle('end_rod', '~ ~1.2 ~', (0.3, 0.6, 0.3), 0.18, 20),
          g.dust(A.LIME_CORE, 1.6, '~ ~1.6 ~', (0.6, 1.0, 0.6), 16),
          g.sound('block.amethyst_block.chime', 0.8, 2.0))
    ck.write([f'# S4 death (@s = body, at it; #mbT 1..{ln} = the death clip tick): cracks 4, shatter {sh}, kneel {kn},',
              f'# dissolve {dv}.. (motes every 2 t, kit motes every 15 t, shards every 6 t, a descending chime), the last motes {ln - 4}.'])
