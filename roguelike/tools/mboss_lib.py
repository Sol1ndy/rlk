"""Shared helpers for the mid-boss (중간보스) generators. Importing this module has no side effects.

Used by tools/build_mboss_core.py, tools/build_mboss_arena.py and every boss module generator
(tools/build_mboss_<id>.py). The runtime contract these helpers target is documented in
README.md (중간보스) and in the framework comments of F:mboss/*.
"""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
FN = ROOT / 'data/rlk/function'
MB = FN / 'mboss'
REGISTRY = ROOT / 'tools/mboss_registry.json'

# Hooks every boss module implements as F:mboss/<id>/<hook>.mcfunction (stubs allowed).
# 'test' is a macro hook ({id:N}); the rest take no arguments. 'uninstall' is dispatched to every enabled
# module (not only the running one): it removes what the module itself created (e.g. its rig objectives).
HOOKS = ['spawn', 'intro_tick', 'tick', 'on_hit', 'aux_hit', 'incoming', 'pause', 'resume',
         'death_start', 'death_tick', 'cleanup', 'reload', 'bars', 'hz_vis', 'pj_end', 'test', 'uninstall']
ALL_MODULE_HOOKS = {'uninstall'}
MACRO_HOOKS = {'test': ['id']}

# #elem numbering (combat/apply): 0 physical 1 pyro 2 hydro 3 electro 4 cryo 5 geo 6 anemo 7 dendro 8 void
ELEM_NAMES = ['물리', '불', '물', '번개', '얼음', '바위', '바람', '풀', '공허']
# bossui under-bar colour codes: 1 electro 2 pyro 3 hydro 4 cryo 5 geo 6 anemo 7 dendro 8 gold 9 green
ELEM_TO_BU = {0: 8, 1: 2, 2: 3, 3: 1, 4: 4, 5: 5, 6: 6, 7: 7, 8: 2}
# Telegraph particle colours per element, chosen for contrast on the pale marble floor.
HZ_COLOURS = {
    0: (0.86, 0.16, 0.18),   # physical: crimson
    1: (1.00, 0.38, 0.10),   # pyro
    2: (0.18, 0.55, 1.00),   # hydro
    3: (0.70, 0.30, 1.00),   # electro
    4: (0.30, 0.82, 0.95),   # cryo
    5: (0.90, 0.52, 0.06),   # geo: deep amber (pale gold vanishes on white marble)
    6: (0.25, 0.85, 0.70),   # anemo
    7: (0.45, 0.80, 0.15),   # dendro
    8: (0.85, 0.15, 0.40),   # void
}
STRIKE_COLOUR = (1.0, 0.97, 0.88)


def load_registry():
    data = json.loads(REGISTRY.read_text(encoding='utf-8'))
    ids, ns = set(), set()
    for b in data['boss']:
        assert b['id'] not in ids, 'duplicate id ' + b['id']
        assert b['n'] not in ns, 'duplicate n %d' % b['n']
        assert 1 <= b['n'] <= 9999
        ids.add(b['id'])
        ns.add(b['n'])
    return data


def enabled_bosses(reg=None):
    reg = reg or load_registry()
    return [b for b in reg['boss'] if b.get('enabled', True)]


class Out:
    """Writes .mcfunction files under F: and remembers them, so a generator can delete stale
    files inside the directories it owns (and only there)."""

    def __init__(self, owned_dirs=(), owned_files=()):
        self.written = set()
        self.owned_dirs = [FN / d for d in owned_dirs]
        self.owned_files = [FN / (f + '.mcfunction') for f in owned_files]

    def write(self, name, lines):
        p = FN / (name + '.mcfunction')
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(lines, str):
            text = lines.strip('\n')
        else:
            text = '\n'.join(lines)
        for i, line in enumerate(text.split('\n'), 1):
            s = line.lstrip()
            if s.startswith('$'):
                assert '$(' in s, f'{name}:{i} macro line without $(var): {s[:80]}'
            elif '$(' in s and not s.startswith('#'):
                raise AssertionError(f'{name}:{i} $(var) in a non-macro line: {s[:80]}')
        p.write_text(text + '\n', encoding='utf-8')
        self.written.add(p.resolve())
        return p

    def clean(self):
        removed = 0
        for d in self.owned_dirs:
            if not d.exists():
                continue
            for p in sorted(d.rglob('*.mcfunction')):
                if p.resolve() not in self.written:
                    p.unlink()
                    removed += 1
            for p in sorted(d.rglob('*'), reverse=True):
                if p.is_dir() and not any(p.iterdir()):
                    p.rmdir()
        for p in self.owned_files:
            if p.exists() and p.resolve() not in self.written:
                p.unlink()
                removed += 1
        return removed


def num(v, nd=4):
    if isinstance(v, int):
        return str(v)
    s = f'{v:.{nd}f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def snbt_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def colour_list(rgb):
    return '[' + ','.join(num(c, 3) + 'f' for c in rgb) + ']'


def sound(event, vol=1.0, pitch=1.0, target='@a[tag=player]', source='hostile'):
    """One vanilla playsound line at the execution position (vanilla sounds only)."""
    return f'playsound minecraft:{event} {source} {target} ~ ~ ~ {num(vol)} {num(pitch)} 0.3'


# ---------------------------------------------------------------------------------------------
# Call builders for boss modules. Distances are in blocks here and converted to the runtime's
# tenths of a block; every option that is not given keeps its framework default.

def _tenths(v):
    return int(round(v * 10))


def hz_opts(act=None, el=None, kb=None, kbdir=None, y0=None, y1=None, r0=None, back=None,
            sfx=None, vis=None, col=None, linger=None, quiet=None):
    """Lines that set the one-shot options of the next hazard (reset after each create)."""
    out = []
    pairs = [('#hzAct', act), ('#hzEl', el), ('#hzKB', kb), ('#hzKBDir', kbdir), ('#hzSfx', sfx),
             ('#hzVis', vis), ('#hzCol', col), ('#hzLinger', linger), ('#hzQuiet', quiet)]
    for k, v in pairs:
        if v is not None:
            out.append(f'scoreboard players set {k} mb {int(v)}')
    for k, v in (('#hzY0', y0), ('#hzY1', y1), ('#hzR0', r0), ('#hzBack', back)):
        if v is not None:
            out.append(f'scoreboard players set {k} mb {_tenths(v)}')
    return out


def hz_disc(r, tell, dmg):
    return f'function rlk:mboss/hz/disc {{r:{_tenths(r)},tell:{int(tell)},dmg:{int(dmg)}}}'


def hz_ring(r0, r, tell, dmg):
    return f'function rlk:mboss/hz/ring {{r0:{_tenths(r0)},r:{_tenths(r)},tell:{int(tell)},dmg:{int(dmg)}}}'


def hz_sector(r, half_angle, tell, dmg):
    return f'function rlk:mboss/hz/sector {{r:{_tenths(r)},a:{int(round(half_angle))},tell:{int(tell)},dmg:{int(dmg)}}}'


def hz_line(length, width, tell, dmg):
    return f'function rlk:mboss/hz/line {{len:{_tenths(length)},w:{_tenths(width)},tell:{int(tell)},dmg:{int(dmg)}}}'


def hz_full(tell, dmg):
    return f'function rlk:mboss/hz/full {{tell:{int(tell)},dmg:{int(dmg)}}}'


def say(text, colour='#FFFFFF', gap=2, hold=40, snd=1):
    """Typed subtitle line (framework rlk:mboss/line/say)."""
    assert '"' not in text and '\\' not in text
    return f'function rlk:mboss/line/say {{t:"{text}",c:"{colour}",gap:{int(gap)},hold:{int(hold)},snd:{int(snd)}}}'


def at_t(score, t, cmd, sel='@s', obj=None):
    """execute line gated on a timeline score."""
    if obj is None:
        return f'execute if score {score} mb matches {t} run {cmd}'
    return f'execute if score {sel} {obj} matches {t} run {cmd}'


# ---------------------------------------------------------------------------------------------
# Small affine helpers for display rigs (block_display / item_display transformation matrices).

def mat_identity():
    return [[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]]


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def mat_t(x, y, z):
    m = mat_identity()
    m[0][3], m[1][3], m[2][3] = x, y, z
    return m


def mat_s(x, y, z):
    m = mat_identity()
    m[0][0], m[1][1], m[2][2] = x, y, z
    return m


def mat_rx(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]


def mat_ry(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]


def mat_rz(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def mat_chain(*ms):
    out = mat_identity()
    for m in ms:
        out = mat_mul(out, m)
    return out


def mat_nbt(m):
    """transformation as the 16-float row-major matrix form."""
    return '[' + ','.join(num(m[i][j], 4) + 'f' for i in range(4) for j in range(4)) + ']'
