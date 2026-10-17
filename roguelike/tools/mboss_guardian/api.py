"""Shared API of the Corrupted Guardian module generator (core <-> pattern modules).

Stable on purpose: pattern authors (p12.py, p34.py, p56.py) import this and never edit it. The
runtime side of the same contract (score names, entry points, cancel rules) is documented in the
scratchpad file mboss/gd_contract.md.

Units follow the framework: Python helpers take blocks and ticks; at the runtime boundary the
framework uses tenths of a block and damage as a % of the registry base hit (atk).
"""
from pathlib import Path
import json
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402

ID = 'guardian'
NS = f'rlk:mboss/{ID}/'
REG = L.load_registry()
ARENA = REG['arena']
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']
BOSS = next(b for b in REG['boss'] if b['id'] == ID)

# ---------------------------------------------------------------------------------------------
# Rig clips (tools/mboss_guardian_rig_manifest.json, written by build_mboss_guardian_rig.mjs).
_MAN = json.loads((_TOOLS / 'mboss_guardian_rig_manifest.json').read_text(encoding='utf-8'))
CLIPS = {c['name']: {'id': c['id'], 'len': c['len'], 'loop': c['loop'], 'next': c['next'],
                     'events': dict(c['events'])} for c in _MAN['clips']}


def ev(clip, event):
    """Clip tick of a rig event, e.g. ev('thrust', 'hit1') == 28. Pattern clocks (#gdPT) start at
    0 on the tick the pattern's start function plays its first clip, so #gdPT == clip tick."""
    return CLIPS[clip]['events'][event]


def clip_len(clip):
    return CLIPS[clip]['len']


# ---------------------------------------------------------------------------------------------
# Balance (plan.md K17, K16). Damage = % of the registry base hit (atk x dmgMul).
DMG = {
    'entrance': 100,
    'p1a': 100, 'p1b': 115,       # P1 thrust 1 / thrust 2
    'p2': 130,                    # P2 javelin line
    'p3': 160,                    # P3 slam disc
    'p4': 120,                    # P4 each 360 degree swing
    'p5': 180,                    # P5 fly-slam disc
    'gold': 165,                  # P6 gold sweep (timeout)
    'ench': 250,                  # P6 enchanted sweep (+ the recorded element)
    'fail': 220,                  # each chaos fail spear
}
KB = {'p1b': 4, 'ench': 4, 'default': 3, 'light': 2}   # knockback steps (K16)

# Range bands (K2), horizontal distance boss body -> player body, blocks.
MELEE = 4.0     # melee: d <= 4
FAR = 8.0       # mid: 4 < d < 8, far: d >= 8
BANDS = {'melee': 1, 'mid': 2, 'far': 3}

# ---------------------------------------------------------------------------------------------
# Elements (#elem numbering) and colours.
EL_KEY = {1: 'pyro', 2: 'hydro', 3: 'electro', 4: 'cryo'}
EL_KO = {1: '불', 2: '물', 3: '번개', 4: '얼음'}
EL_HEX = {0: '#F4D07C', 1: '#FF8A4C', 2: '#5CC8FF', 3: '#E484FC', 4: '#A2FEFD', 5: '#F4D07C'}
EL_RGB = {k: tuple(int(v[i:i + 2], 16) / 255 for i in (1, 3, 5)) for k, v in EL_HEX.items()}
# bossui under-bar colour codes (mboss_lib.ELEM_TO_BU)
EL_BU = {1: 2, 2: 3, 3: 1, 4: 4}
# chaos star kinds: 1-4 = active star of that element, 5 = inert gold (slot A), 6 = inert blue (slot B)
STAR_HEX = {1: '#FF8A4C', 2: '#5CC8FF', 3: '#D282FA', 4: '#A2FEFD', 5: '#FCE582', 6: '#A6CEFD'}
STAR_RGB = {k: tuple(int(v[i:i + 2], 16) / 255 for i in (1, 3, 5)) for k, v in STAR_HEX.items()}
STAR_KO = {1: '불', 2: '물', 3: '번개', 4: '얼음', 5: '타성(금)', 6: '타성(청)'}
# Framework hazard colour index (#hzCol) per star kind: element palette, inert gold = geo amber,
# inert blue = hydro blue.
STAR_HZCOL = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 2}

GOLD = (0.99, 0.86, 0.45)
GOLD_DEEP = (0.89, 0.71, 0.24)
GOLD_PALE = (1.0, 0.96, 0.75)
CRIMSON = (0.75, 0.10, 0.18)
CRIMSON_DARK = (0.39, 0.12, 0.10)
RED_EDGE = (0.99, 0.33, 0.33)
LINE_HEX = '#F2D488'          # typed subtitle colour of her voice lines


class Pattern:
    """One pattern a module provides.

    id      stable number (1-5 normal patterns P1-P5; 11-19 service patterns run by the core)
    key     directory name F:mboss/guardian/p/<key>/
    label   Korean name shown on the boss bar sub-line while it runs
    kind    'normal' (in the rotation's shuffle bag) or 'service' (started by the core: sweeps,
            fail spears)
    bands   range bands the bag may pick it in: subset of ('melee', 'mid', 'far')
    close   blocks: close in to this distance before the start (melee patterns), None = no
    recover idle ticks after it ends before the next decision
    max_len safety end: the core finishes the pattern at this #gdPT even if it never called p/end
    """

    def __init__(self, id, key, label, kind='normal', bands=(), close=None, recover=20, max_len=120):
        assert kind in ('normal', 'service')
        assert kind == 'service' or bands, key
        assert all(b in BANDS for b in bands), bands
        self.id, self.key, self.label, self.kind = id, key, label, kind
        self.bands, self.close, self.recover, self.max_len = tuple(bands), close, recover, max_len


# ---------------------------------------------------------------------------------------------
class Gen:
    """Writer handed to every emit(gen). Paths are relative to F:mboss/guardian/."""

    def __init__(self, out):
        self.out = out
        self.files = set()

    # -- files
    def w(self, rel, lines):
        if isinstance(lines, str):
            lines = lines.strip('\n').split('\n')
        self.out.write(f'mboss/{ID}/{rel}', list(lines))
        self.files.add(rel)

    def pw(self, key, name, lines):
        """Write F:mboss/guardian/p/<key>/<name> (pattern modules write only these)."""
        self.w(f'p/{key}/{name}', lines)

    def has(self, rel):
        return rel in self.files

    # -- references
    @staticmethod
    def fn(rel):
        return f'function {NS}{rel}'

    @staticmethod
    def rig(call):
        return f'function {NS}rig/{call}'

    @staticmethod
    def play(clip):
        assert clip in CLIPS, clip
        return f'function {NS}rig/play/{clip}'

    @staticmethod
    def end():
        """The pattern is done: the core finishes it after this tick (see gd_contract.md)."""
        return f'function {NS}p/end'

    @staticmethod
    def voice_attack():
        """One of the two attack lines, at most once per 20 s (shared cooldown)."""
        return f'function {NS}voice/attack'

    # -- timeline helpers on the pattern clock #gdPT
    @staticmethod
    def at(t, cmd):
        if isinstance(t, tuple):
            return f'execute if score #gdPT mb matches {t[0]}..{t[1]} run {cmd}'
        return f'execute if score #gdPT mb matches {t} run {cmd}'

    @staticmethod
    def at_body(t, sub):
        """sub = the rest of an execute chain after 'at @s rotated as @s rotated ~ 0' (body yaw)."""
        rng = f'{t[0]}..{t[1]}' if isinstance(t, tuple) else t
        return f'execute if score #gdPT mb matches {rng} at @s rotated as @s rotated ~ 0 {sub}'

    @staticmethod
    def every(n, cmd, start=0):
        """Every n ticks of #gdPT (needs the core constant #gdK<n>; n in 2, 3, 4, 5, 6, 8)."""
        return (f'scoreboard players operation #gdM mb = #gdPT mb\n'
                f'scoreboard players operation #gdM mb %= #gdK{n} mb\n'
                f'execute if score #gdM mb matches {start} run {cmd}')

    # -- fx and sound
    @staticmethod
    def sound(event, vol=1.0, pitch=1.0):
        return L.sound(event, vol, pitch)

    @staticmethod
    def dust(rgb, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1, speed=0):
        c = L.colour_list(rgb)
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:dust{{color:{c},scale:{L.num(float(scale), 2)}}} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def dust_fade(rgb0, rgb1, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1):
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return (f'particle minecraft:dust_color_transition{{from_color:{L.colour_list(rgb0)},to_color:{L.colour_list(rgb1)},'
                f'scale:{L.num(float(scale), 2)}}} {pos} {d} 0 {int(n)} force @a[tag=player]')

    @staticmethod
    def particle(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0, n=1):
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:{name} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def card(kind, pos, **kw):
        """A gold Geo card (Navia's rlk:fx/nv engine: rose, star, burst, crescent, petal, shard,
        ring, glow); see tools/build_navia_fx_cards.py card_call for the arguments."""
        from build_navia_fx_cards import card_call
        return card_call(kind, pos, **kw)

    @staticmethod
    def say(text, colour=LINE_HEX, gap=2, hold=40, snd=1):
        return L.say(text, colour, gap, hold, snd)

    # -- hazards (blocks; see mboss_lib.hz_*). Call positioned on the floor point, rotated = aim.
    hz_opts = staticmethod(L.hz_opts)
    hz_disc = staticmethod(L.hz_disc)
    hz_ring = staticmethod(L.hz_ring)
    hz_sector = staticmethod(L.hz_sector)
    hz_line = staticmethod(L.hz_line)
    hz_full = staticmethod(L.hz_full)
