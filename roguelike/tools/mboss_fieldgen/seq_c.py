"""Sequences of the cruise-pattern author: E the entrance (dormant -> unfold -> rise) and S4 death (scratchpad specs
mb3/spec/E_entrance.md and S4_death.md).

Visual and audio only, through the fx kit (THE effect engine, fg_fx_api.md): its presets and sound recipes on the rig
events, plus the specs' single vanilla layers (mechanical / brass only: no voice; deathSnd false). The core keeps every
mechanic of these sequences (the clocks, the rig calls and clips, the untargetable intro and its end at `risen`, the
nameplate and look/idle at the eye, look/off at 12, the rig kill at the death clip's end, the death cancel / HUD
flags) and calls one function here from each hook (the lines marked "[seq_c: cruise author]" in core.py):

    intro/setup  -> seq_c/entrance/setup   (@s = the new body, the spawn tick = entrance clip tick 0)
    intro_tick   -> seq_c/entrance/tick    (#mbT = intro clock = entrance clip tick + core.INTRO_CLIP)
    death_start  -> seq_c/death/start      (@s = body, #mbT 0 = death clip tick 0)
    death_tick   -> seq_c/death/tick       (#mbT 1 .. registry death)

Every tick is read from the rig manifest (ev_or: the stub's events while the real rig is not merged), heights from
its anchors (api.c_anchor: the specs' values while the stub has none). The last death_fade is called early enough
that every kit card has expired before the framework's death_finish (registry death) and the fight cleanup's fx/clear
(the butterfly review's perf-5). Files: F:mboss/fieldgen/seq_c/** (written through gen.w, owned by the module
generator like every G: path).
"""
from . import api as A
from .api import ev_or, clip_len, CY, L

SEQ = 'seq_c'
BODY = 'execute at @s rotated as @s rotated ~ 0 '               # the body's feet, its yaw (the body frame)

# E (entrance, stub 112 / real 130 t): clank 16, pods 24, unfold 30, eye 54, turn 60, rise 80, risen 110
E_CLANK = ev_or('entrance', 'clank', 16)
E_PODS = ev_or('entrance', 'pods', 24)
E_UNFOLD = ev_or('entrance', 'unfold', 30)
E_EYE = ev_or('entrance', 'eye', 54)
E_TURN = ev_or('entrance', 'turn', 60)
E_RISE = ev_or('entrance', 'rise', 80)
E_RISEN = ev_or('entrance', 'risen', 110)
E_RING0 = A.c_anchor('entrance', 'clank', 'ring_centre', (0.0, 2.05, 0.0))[1]      # dormant ring centre
E_RING1 = A.c_anchor('entrance', 'pods', 'ring_centre', (0.0, 2.15, 0.0))[1]
E_HUB0 = E_RING0 + 0.5                                           # the top hub (2.55 at the clank)
E_HUB1 = A.c_anchor('entrance', 'unfold', 'ring_centre', (0.0, 2.7, 0.0))[1] + 0.5  # the hub top as the crown rises (3.2)
E_EYE_AT = A.c_anchor('entrance', 'eye', 'eye', (0.0, 3.0, -1.38))
E_CORE = A.c_anchor('entrance', 'risen', 'core', (0.0, 4.5, 0.0))[1]
assert 0 < E_CLANK < E_PODS <= E_UNFOLD < E_EYE <= E_TURN < E_RISE < E_RISEN, (E_CLANK, E_PODS, E_UNFOLD, E_EYE, E_RISE)
# S4 (death, stub 106 / real 110 t, hold): flicker 0, drop 20, sink 40, land 60, out 70
D_LEN = clip_len('death')
D_DROP = ev_or('death', 'drop', 20)
D_SINK = ev_or('death', 'sink', 40)
D_LAND = ev_or('death', 'land', 60)
D_OUT = ev_or('death', 'out', 70)
D_REG = A.BOSS['death']                                          # death_finish (the boxes, the cleanup) at #mbT = this
D_FADE_LIFE = 28                                                 # a death_fade card lives at most dly 6 + life 22
D_FADE2 = min(D_OUT + 12, D_REG - D_FADE_LIFE)                   # the last fade (82): gone before death_finish
D_FADE1 = min(D_OUT, D_FADE2 - 12)                               # the first one (70)
D_CORE = 4.5
D_CORE_LOW = 1.9                                                 # the core once the ring has landed
assert D_DROP < D_SINK < D_LAND and D_FADE1 < D_FADE2 and D_FADE2 + D_FADE_LIFE <= D_REG, (D_FADE1, D_FADE2, D_REG)


class Clock:
    """Per-tick timeline of a sequence on a core clock (fake player `score` in mb; clock value = tick + off): the
    ticks go to seq_c/<name>/k/<t> behind a small binary dispatch, so a tick runs a handful of score tests."""

    def __init__(self, g, name, score, off=0):
        self.g, self.name, self.score, self.off = g, name, score, off
        self.ev = {}

    def at(self, t, *lines):
        for line in lines:
            if line:
                self.ev.setdefault(int(t), []).extend(line if isinstance(line, list) else line.split('\n'))

    def fn(self, rel):
        return f'function {A.NS}{SEQ}/{self.name}/{rel}'

    def w(self, rel, lines):
        self.g.w(f'{SEQ}/{self.name}/{rel}', lines)

    def _node(self, ts):
        c = lambda t: t + self.off                              # noqa: E731
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
        for t, lines in sorted(self.ev.items()):
            self.w(f'k/{t}', [f'# {self.name} tick {t}'] + lines)
        self.w('tick', list(head) + self._node(sorted(self.ev)))


def emit(g):
    from . import core as C                                     # the core's clock constants (already imported)
    entrance(g, C)
    death(g)


def at_h(h, cmd):
    """cmd at the body's axis h b up, rotated as the body."""
    return f'{BODY}positioned ~ ~{L.num(h, 3)} ~ run {cmd}'


def at_floor(cmd, pos='~ ~ ~'):
    return f'{BODY}positioned {pos} positioned ~ {CY} ~ run {cmd}'


# =============================================================================================
def entrance(g, C):
    """E: the folded device lies dormant over its shadow (floor dust, a low hum); the clank (16) wakes it (the kit's
    awake flare at the top hub, sparks), the pods unfold (24), the crown and the halo assemble (30: flares, gear
    clicks), the eye opens (54; the core shows the nameplate), the arch turns (60), the device rises to cruise height
    (80 -> 110: the gold ground ring twice and the whirring hum) and comes online at `risen` (a flash at the core,
    the beacon). Untargetable and harmless throughout (the core)."""
    g.w(f'{SEQ}/entrance/setup', [
        '# E at the spawn (@s = the new body, at it, facing the arriving player; entrance clip tick 0): the folded device',
        '# on the floor, a little tuff dust, the low mechanical hum.',
        f'execute positioned ~ {CY} ~ run ' + g.particle('block{block_state:"minecraft:tuff"}', '~ ~0.3 ~', (1.2, 0.1, 1.2), 0, 10),
        at_h(E_RING0, g.sound('block.respawn_anchor.ambient', 0.6, 0.6))])
    ck = Clock(g, 'entrance', '#mbT', off=C.INTRO_CLIP)
    ck.at(E_CLANK - 3, at_h(E_RING0, g.sound('block.beacon.ambient', 0.4, 0.6)))           # the machinery onset
    ck.at(E_CLANK, at_h(E_HUB0, g.fx('awake')), at_h(E_HUB0, g.snd('awake_clank')))
    ck.at(E_CLANK + 5, at_h(E_HUB0, g.fx('spark')))
    ck.at(E_CLANK + 9, at_h(E_HUB0, g.fx('spark')))
    ck.at(E_PODS, at_h(E_RING1, g.fx('unfold')), at_h(E_RING1, g.snd('unfold')))
    ck.at(E_PODS + 8, at_h(E_RING1, g.sound('block.piston.extend', 0.6, 0.8)))            # the second thump
    ck.at(E_UNFOLD, at_h(E_HUB1, g.fx('crown_flare')))
    ck.at(E_UNFOLD + 8, at_h(E_HUB1, g.fx('crown_flare')))
    for d in (10, 16, 19):
        if E_UNFOLD + d < E_EYE:
            ck.at(E_UNFOLD + d, at_h(E_HUB1, g.snd('gear_click')))
    ck.at(E_EYE, f'{BODY}positioned {A.c_bf(E_EYE_AT)} run {g.fx("eye_open")}',
          f'{BODY}positioned {A.c_bf(E_EYE_AT)} run {g.snd("eye_open")}')
    if E_TURN > E_EYE:                                           # eye_open already plays the grindstone at the eye
        ck.at(E_TURN, at_h(E_HUB1, g.sound('block.grindstone.use', 0.3, 0.6)))
    ck.at(E_RISE, at_floor(g.fx('rise')), at_h(E_HUB1, g.snd('rise_hum')))
    if E_RISE + 14 < E_RISEN:
        ck.at(E_RISE + 14, at_floor(g.fx('rise')), at_h(E_HUB1, g.snd('rise_hum')))
    ck.at(E_RISEN, at_h(E_CORE, g.fx('flash')), at_h(E_CORE, g.sound('block.beacon.activate', 0.5, 1.3)))
    ck.write([f'# E on the intro clock (@s = body; #mbT = entrance clip tick + {C.INTRO_CLIP}): clank {E_CLANK}, pods {E_PODS},',
              f'# unfold {E_UNFOLD}, eye {E_EYE}, turn {E_TURN}, rise {E_RISE}, online at {E_RISEN} (the fight starts there).'])


# =============================================================================================
def death(g):
    """S4: the seam flickers out three times (0 / 6 / 12, the core's look/off at 12), the halo drops and the pods fall
    (drop: dust under the halo side, chains and copper), the ring tilts and sinks (sink: anvil and chain groan), it
    lands on its low rim (land: the dust ring, the medallions' clatter), then it scales out with gold motes (out and
    out + 12, early enough that every card is gone before death_finish). Mechanical sounds only."""
    g.w(f'{SEQ}/death/start', [
        '# S4 death clip tick 0 (@s = body; the core cancelled the pattern, cleared the decals and the HUD flags): the',
        '# first flicker of the dying seam, the power-down.',
        at_h(D_CORE, g.fx('death_flicker')), at_h(D_CORE, g.snd('death'))])
    ck = Clock(g, 'death', '#mbT')
    ck.at(6, at_h(D_CORE, g.fx('death_flicker')), at_h(D_CORE, g.sound('block.beacon.deactivate', 0.5, 1.6)))
    ck.at(12, at_h(D_CORE, g.fx('death_flicker')), at_h(D_CORE, g.sound('block.beacon.deactivate', 0.4, 1.8)))
    ck.at(D_DROP, at_floor(g.fx('dust_puff'), '^1.5 ^ ^'), at_h(2.0, g.sound('block.chain.fall', 0.6, 0.8)),
          at_h(2.0, g.sound('block.copper.fall', 0.5, 0.8)))
    ck.at(D_SINK, at_h(2.5, g.sound('block.anvil.place', 0.6, 0.5)), at_h(2.5, g.sound('block.chain.step', 0.5, 0.6)))
    ck.at(D_LAND, at_floor(g.fx('death_fall')), at_h(1.0, g.snd('death_fall')))
    ck.at(D_FADE1, at_h(D_CORE_LOW, g.fx('death_fade')))
    ck.at(D_FADE2, at_h(D_CORE_LOW, g.fx('death_fade')), at_h(D_CORE_LOW, g.snd('death_fade')))
    ck.write([f'# S4 on the death clock (@s = body; #mbT = death clip tick 1 ..): flickers 6 / 12, drop {D_DROP}, sink {D_SINK},',
              f'# land {D_LAND}, the fades {D_FADE1} / {D_FADE2} (every card gone by {D_FADE2 + D_FADE_LIFE} <= death_finish {D_REG}).'])
