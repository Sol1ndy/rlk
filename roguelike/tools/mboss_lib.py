"""Shared helpers for the mid-boss (중간보스) generators. Importing this module has no side effects.

Used by tools/build_mboss_core.py, tools/build_mboss_arena.py and every boss module generator
(tools/build_mboss_<id>.py). The runtime contract these helpers target is documented in
README.md (중간보스) and in the framework comments of F:mboss/*.
"""
from pathlib import Path
import importlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
FN = ROOT / 'data/rlk/function'
MB = FN / 'mboss'
REGISTRY = ROOT / 'tools/mboss_registry.json'

# Hooks every boss module implements as F:<fn root>/<hook>.mcfunction (fn_root: mboss/<id> or the entry's "fn"; stubs allowed).
# 'test' is a macro hook ({id:N}); the rest take no arguments. 'uninstall' is dispatched to every enabled
# module (not only the running one): it removes what the module itself created (e.g. its rig objectives).
HOOKS = ['spawn', 'intro_tick', 'tick', 'on_hit', 'aux_hit', 'incoming', 'pause', 'resume',
         'death_start', 'death_tick', 'cleanup', 'reload', 'bars', 'hz_vis', 'pj_end', 'test', 'uninstall']
ALL_MODULE_HOOKS = {'uninstall'}
MACRO_HOOKS = {'test': ['id']}
# Every module also writes F:<fn root>/test/help (no macro): its test numbers with their names, shown by
# /function rlk:mboss/test/pattern {id:"help"} (and lock / the rlk:boss/test aliases) through mboss/d/test_help.
HELP_HOOKS = ['test/help']
# Chapter bosses (kind "chapter", AZ-CM) implement the 17 hooks plus these (not macros): prep = the domain entrance
# build (@s = the kind-9 zone marker, at it): writes rlk:mboss cprep.<id>.{gate,title,sub} (scratchpad az/contract/cm.md 5.3).
CHAPTER_HOOKS = ['prep']
# Special bosses (kind "special", D0 of the Tachy plan: scratchpad tk/PLAN.md §7-8, tk/contract.md): reached through a
# room rift (F:room/rift, F:mboss/sp), fought in their own arena in chapter mode, rewarded with a level-up + picks boxes.
# They implement the 17 hooks + test/help (no prep); the framework (F:mboss/sp, tools/build_mboss_core.py) runs them in
# chapter mode (#mbMode 1, #mbKind 2) and routes their incoming hook through the floor (mboss/cb/inc/<id>) as a chapter's.
SPECIAL_HOOKS = []
SPECIAL_PICKS_MAX = 3

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


RES_KEYS = {str(k) for k in range(9)} | {'*'}
# The plaza's arena box (build_mboss_arena.py: centre -24..+23, y 190..240; the core's @FL@ forceload box).
PLAZA_BOX = (-24, 190, -24, 23, 240, 23)


# Block rectangles (x0, z0, x1, z1) force-loaded outside the chapter arenas (F:load, F:room/setup, the plaza of
# F:mboss/arena): a chapter arena box (load_registry) may not share a chunk with them.
FIXED_FORCELOADS = {
    'dungeon (room/setup)': (-64, -64, 63, 63),
    'lobby (load)': (80, 14, 134, 64),
    'item room (load)': (104, 4, 104, 4),
    'plaza (mboss arena)': (176, -16, 223, 31),
}


# Vanilla music events a chapter boss may name (cm.md 10; sounds.json of 26.3, asset index 34): event -> the length of
# every track it can play, in ticks (rounded down; measured from the .ogg files, AP-FW 2026-10-21). An event with several
# tracks is a random pool: every playsound picks one, so a loop period shorter than its longest track would cut the picked
# track (APEP-08). A pool's `len` is therefore 0 (play once) or a re-pick period >= its longest track (music_len).
MUSIC_TRACKS = {
    'minecraft:music.end': [18090],
    'minecraft:music.dragon': [6883],
    'minecraft:music.overworld.deep_dark': [6870, 6068],
    'minecraft:music.nether.soul_sand_valley': [5600, 5189, 6076, 6376, 4789],
    # Tachy S1 (2026-10-29, the same asset index 34): the basalt deltas pool holds the same five nether tracks
    'minecraft:music.nether.basalt_deltas': [5600, 5189, 6076, 6376, 4789],
    'minecraft:music.overworld.lush_caves': [6627, 4031, 5923, 6881, 4104, 6859, 5617, 5210, 5571, 5502, 6400, 5935, 6254,
                                             6492, 4595],
}


def music_len(ev):
    """The registry `len` that repeats event ev without ever cutting a track: the track length of a single-track event
    (an exact loop), the longest track of a pool (a re-pick period: each replay picks a new random track; a shorter track
    leaves a silence until the period ends, as vanilla's own music gaps)."""
    return max(MUSIC_TRACKS[ev])


def load_registry():
    """The registry (schema v2), validated: unique ids / n across mid-boss and chapter entries, the chapter-entry rules of
    scratchpad az/contract/cm.md 2.2 and the arena entries of 2.3."""
    data = json.loads(REGISTRY.read_text(encoding='utf-8'))
    ids, ns = set(), set()
    arenas = data.get('arenas', {})
    assert 'plaza' not in arenas, 'arenas{} never holds the plaza (it is the top-level arena)'
    arn = set()
    # chunk rectangles (cx0, cz0, cx1, cz1) a chapter arena's forceload must never touch: its fl_off would release them
    fl_taken = {f'fixed forceload {k}': tuple(v >> 4 for v in r) for k, r in FIXED_FORCELOADS.items()}
    for aid, a in arenas.items():
        assert isinstance(a.get('n'), int) and a['n'] >= 1 and a['n'] not in arn, f'arena {aid}: n must be unique and >= 1'
        arn.add(a['n'])
        for k in ('theme', 'ver', 'cx', 'cy', 'cz', 'r', 'walk', 'safe', 'start', 'box', 'looks'):
            assert k in a, f'arena {aid}: missing {k}'
        assert a['looks'], f'arena {aid}: looks[] is empty'
        bx = a['box']
        assert bx['x0'] <= a['cx'] <= bx['x1'] and bx['z0'] <= a['cz'] <= bx['z1'] and bx['y0'] < a['cy'] <= bx['y1'], aid
        ch = (bx['x0'] >> 4, bx['z0'] >> 4, bx['x1'] >> 4, bx['z1'] >> 4)
        nch = (ch[2] - ch[0] + 1) * (ch[3] - ch[1] + 1)
        assert nch <= 256, f'arena {aid}: the box spans {nch} chunks (one forceload add takes at most 256)'
        for oid, o in fl_taken.items():
            assert ch[2] < o[0] or o[2] < ch[0] or ch[3] < o[1] or o[3] < ch[1], \
                f'arena {aid}: the box chunks overlap those of {oid} (releasing one forceload would release the other)'
        fl_taken[f'arena {aid}'] = ch
    for b in data['boss']:
        assert b['id'] not in ids, 'duplicate id ' + b['id']
        assert b['n'] not in ns, 'duplicate n %d' % b['n']
        assert 1 <= b['n'] <= 9999
        ids.add(b['id'])
        ns.add(b['n'])
        kind = b.get('kind', 'mid')
        assert kind in ('mid', 'chapter', 'special'), f'{b["id"]}: kind {kind}'
        if kind == 'special':
            for k in ('ch', 'route', 'px'):
                assert not b.get(k), f'{b["id"]}: {k} is not a special-entry field'
            assert 1 <= int(b.get('picks', 0)) <= SPECIAL_PICKS_MAX, f'{b["id"]}: a special entry needs picks 1..{SPECIAL_PICKS_MAX}'
            assert int(b.get('lvup', 0)) in (0, 1), f'{b["id"]}: lvup is 0 or 1'
            # the level-up is the reward: no kill XP on top of it (the kill's XP could level up once more first)
            assert not int(b.get('lvup', 0)) or int(b.get('xp', 0)) == 0, f'{b["id"]}: a special entry with lvup 1 needs xp 0'
            assert int(b.get('w', 0)) >= 0, f'{b["id"]}: w (the rift roll weight) must be >= 0'
            aid = b.get('arena', 'plaza')
            # a disabled special may name the arena its framework stage adds later (tk/contract.md: S1 owns arenas{})
            assert aid != 'plaza' and (aid in arenas or not b.get('enabled', True)), f'{b["id"]}: a special entry needs its own arena ({aid})'
        elif kind == 'chapter':
            for k, v in (('goldMul', 1), ('sap', 0), ('picks', 0), ('w', 0)):
                assert b.get(k) == v, f'{b["id"]}: a chapter entry needs {k} {v}'
            aid = b.get('arena', 'plaza')
            assert aid == 'plaza' or aid in arenas, f'{b["id"]}: unknown arena {aid}'
            for c in b.get('ch', []):
                assert b['minCh'] <= c <= b['maxCh'], f'{b["id"]}: ch {c} outside minCh..maxCh'
        else:
            assert not b.get('px'), f'{b["id"]}: px is for chapter entries only'
            for k in ('ch', 'route', 'phases', 'music', 'res'):
                assert k not in b, f'{b["id"]}: {k} is a chapter-entry field'
        if b.get('shield', not b.get('px', False)):
            assert 'hit' in b, f'{b["id"]}: shield needs hit {{w,h}}'
        assert set(b.get('res', {})) <= RES_KEYS, f'{b["id"]}: res keys'
        assert sum(b.get('phases', [100])) <= 100 and all(1 <= p <= 100 for p in b.get('phases', [100])), b['id']
        for ph, m in b.get('music', {}).items():
            assert ph in {str(k) for k in range(1, 10)} and m['ev'].startswith('minecraft:') and int(m['len']) >= 0, b['id']
            tr = MUSIC_TRACKS.get(m['ev'], [])
            assert not (len(tr) > 1 and 1 <= int(m['len']) < max(tr)), \
                (f'{b["id"]}: music {ph} {m["ev"]} is a pool of {len(tr)} tracks (up to {max(tr or [0])} t): len {m["len"]} would cut '
                 f'the picked track; use 0 (play once) or a re-pick period >= {max(tr or [0])} (mboss_lib.music_len, cm.md 10)')
        assert 0 <= int(b.get('pxBase', 65)) <= 240, b['id']
        ic = b.get('icon')
        assert ic is None or (isinstance(ic, dict) and 'item' in ic and 'model' in ic), f'{b["id"]}: icon must be {{item, model}}'
        for k in ('minCh', 'maxCh', 'name', 'sub', 'color', 'el'):
            assert k in b, f'{b["id"]}: missing {k}'
    roots = {}
    for b in data['boss']:
        r = fn_root(b)
        if 'fn' in b:
            assert r in (f'mboss/{b["id"]}', f'boss/{b["id"]}'), f'{b["id"]}: fn must be mboss/<id> or boss/<id>, not {r}'
            assert r != f'boss/{b["id"]}' or b.get('kind', 'mid') in ('chapter', 'special'), f'{b["id"]}: only chapter and special bosses live under boss/'
        assert r not in FN_ROOT_RESERVED, f'{b["id"]}: fn {r} is reserved'
        assert r not in roots, f'{b["id"]}: fn {r} is also the root of {roots.get(r)}'
        roots[r] = b['id']
    claimed = {}
    for b in data['boss']:
        if b.get('kind', 'mid') == 'chapter' and b.get('enabled', True) and b.get('route', True):
            for c in b.get('ch', []):
                assert c not in claimed, f'chapter {c} routed to both {claimed[c]} and {b["id"]}'
                claimed[c] = b['id']
    return data


# Function roots of the boss modules (F:<root>/<hook>). A registry entry may name its own root with "fn"; without it the
# module lives at mboss/<id> (the mid-bosses, proto, cproto). The chapter bosses live under boss/<id> (user 10-21:
# "중간보스가 아닌데" - Azhdaha boss/azhdaha, Apep boss/apep, beside Raiden's own boss/raiden). Only the function root
# moves: entity tags, scoreboards, storage and resource-pack paths keep their mboss names, so saved worlds keep working.
FN_ROOT_RESERVED = {'boss/raiden', 'boss/test'}   # Raiden's own module (not a registry boss) and the test aliases


def fn_root(b):
    """The function root of registry entry b, relative to F: (no slashes at the ends): b.fn or mboss/<id>."""
    return b.get('fn') or f'mboss/{b["id"]}'


def fn_root_of(bid, reg=None):
    """The function root of the registry entry with id bid (mboss/<bid> when the registry has no such entry: a module
    generator that runs before its registry entry exists keeps the default root)."""
    try:
        data = reg or json.loads(REGISTRY.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return f'mboss/{bid}'
    for b in data.get('boss', []):
        if b['id'] == bid:
            return fn_root(b)
    return f'mboss/{bid}'


def enabled_bosses(reg=None):
    """Every enabled entry, mid-boss and chapter boss (hook dispatchers, uninstall)."""
    reg = reg or load_registry()
    return [b for b in reg['boss'] if b.get('enabled', True)]


def mid_bosses(reg=None):
    """Enabled mid-boss entries (kind "mid"): rlk:mboss reg[] / byid, the roll."""
    return [b for b in enabled_bosses(reg) if b.get('kind', 'mid') == 'mid']


def chapter_bosses(reg=None):
    """Enabled chapter-boss entries (kind "chapter"): rlk:mboss creg[] / cbyid, routing, the gate."""
    return [b for b in enabled_bosses(reg) if b.get('kind', 'mid') == 'chapter']


def special_bosses(reg=None):
    """Enabled special-boss entries (kind "special"): the rift roll (F:mboss/sp, S1 of the Tachy plan)."""
    return [b for b in enabled_bosses(reg) if b.get('kind', 'mid') == 'special']


def arena_of(b, reg=None):
    """The arena dict of boss b with 'aid' and 'n' added: arenas[b.arena], or the plaza (the top-level arena, n 0, with
    its legacy box x 176..223, y 190..240, z -16..31)."""
    reg = reg or load_registry()
    aid = b.get('arena', 'plaza')
    if aid == 'plaza':
        a = dict(reg['arena'])
        x0, y0, z0, x1, y1, z1 = PLAZA_BOX
        a.setdefault('box', {'x0': a['cx'] + x0, 'y0': y0, 'z0': a['cz'] + z0, 'x1': a['cx'] + x1, 'y1': y1, 'z1': a['cz'] + z1})
        a.setdefault('looks', [a['theme']])
        a.update(aid='plaza', n=0)
        return a
    a = dict(reg['arenas'][aid])
    a.update(aid=aid)
    return a


def arenas(reg=None):
    """[(aid, arena dict)] with the plaza first, then the arenas{} entries by n (each dict as arena_of returns it)."""
    reg = reg or load_registry()
    out = [('plaza', arena_of({'arena': 'plaza'}, reg))]
    for aid in sorted(reg.get('arenas', {}), key=lambda k: reg['arenas'][k]['n']):
        out.append((aid, arena_of({'arena': aid}, reg)))
    return out


def arena_oob(a):
    """(y0, y1) out-of-bounds band of an arena: its 'oob' entry or cy-3 .. cy+16 (the plaza's 198..217)."""
    o = a.get('oob')
    return (o['y0'], o['y1']) if o else (a['cy'] - 3, a['cy'] + 16)


def theme_module(theme):
    """The arena theme module tools/mboss_arena_<theme>.py (imported; tools/ on sys.path), or None when the file is
    missing (the arena generator then writes stub functions, cm.md 6.3)."""
    tools = str(ROOT / 'tools')
    if not (ROOT / 'tools' / f'mboss_arena_{theme}.py').exists():
        return None
    if tools not in sys.path:
        sys.path.insert(0, tools)
    return importlib.import_module('mboss_arena_' + theme)


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


def min_volume(vol):
    """minVolume of a playsound layer (what a listener beyond its 16 x max(1, vol) b range still hears), scaled with
    the layer like Raiden's mixes: quiet layers (<= 0.25) fade out completely, the rest keep a third of their volume,
    at most 0.4. A fixed floor made every layer equally loud past 16 b and main hits quieter at 12-16 b than at 17 b."""
    if vol <= 0.25:
        return 0.0
    return round(min(0.4, vol / 3), 2)


def sound(event, vol=1.0, pitch=1.0, target='@a[tag=player]', source='hostile', min_vol=None):
    """One vanilla playsound line at the execution position (vanilla sounds only). min_vol None = min_volume(vol)."""
    mv = min_volume(vol) if min_vol is None else min_vol
    return f'playsound minecraft:{event} {source} {target} ~ ~ ~ {num(vol)} {num(pitch)} {num(float(mv), 2)}'


# ---------------------------------------------------------------------------------------------
# Call builders for boss modules. Distances are in blocks here and converted to the runtime's
# tenths of a block; every option that is not given keeps its framework default.

def _tenths(v):
    return int(round(v * 10))


def hz_opts(act=None, el=None, kb=None, kbdir=None, y0=None, y1=None, r0=None, back=None,
            sfx=None, vis=None, col=None, linger=None, quiet=None, grp=False, nododge=None, rearm=None,
            norx=None, safe_g=None, pm=None, pm_lethal=None):
    """Lines that set the one-shot options of the next hazard (reset after each create).
    grp=True: the hazard joins the current volley group #mbGrp (grp_new): one hit per group.
    nododge=1: dash i-frames do not help (#hzNoDodge). rearm=N: a hit disarms it for N ticks only (#hzRearm;
    with a volley group the whole group re-arms together: at most one hit per N ticks).
    Chapter mode (AZ-CM): norx=1: no player-side element reaction from its hit (#hzNR); safe_g=G: the safe group of a
    mask hazard (#hzSafeG, 0 = its own id; 'cur' = the group of the last hz/safe_new, #mbSafeG, cm.md 13.6).
    AP-FW: pm=N: the hit takes N per mille of the player's max HP through mboss/pl_dot instead of a % of the boss hit
    (#hzPm, 1..1000); pm_lethal=0: that hit never kills (#hzPmL; default 1 = lethal; only with pm), cm.md 13.11."""
    out = []
    if grp:
        out.append('scoreboard players operation #hzGrp mb = #mbGrp mb')
    if norx is not None:
        assert int(norx) in (0, 1)
    if safe_g == 'cur':
        out.append('scoreboard players operation #hzSafeG mb = #mbSafeG mb')
        safe_g = None
    elif safe_g is not None:
        assert int(safe_g) >= 0
    if pm is not None:
        assert 1 <= int(pm) <= 1000
    if pm_lethal is not None:
        assert pm is not None and int(pm_lethal) in (0, 1)
    pairs = [('#hzAct', act), ('#hzEl', el), ('#hzKB', kb), ('#hzKBDir', kbdir), ('#hzSfx', sfx),
             ('#hzVis', vis), ('#hzCol', col), ('#hzLinger', linger), ('#hzQuiet', quiet),
             ('#hzNoDodge', nododge), ('#hzRearm', rearm), ('#hzNR', norx), ('#hzSafeG', safe_g),
             ('#hzPm', pm), ('#hzPmL', pm_lethal)]
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


def hz_aim():
    """As a live hazard marker, positioned at its new origin, rotated = its new aim: re-aim it (framework hz/aim)."""
    return 'function rlk:mboss/hz/aim'


def hz_resize(r, r0=0.0, w=0.0):
    """As a live hazard marker: new outer / inner radius (line: length / back) and line width, blocks (w 0 = keep)."""
    return f'function rlk:mboss/hz/resize {{r:{_tenths(r)},r0:{_tenths(r0)},w:{_tenths(w)}}}'


def tell_line(length, width, tell):
    """Telegraph-only ground line (dmg 0: outline, strike flash, module visuals; never a hit)."""
    return hz_line(length, width, tell, 0)


def pj_opts(el=None, kb=None, ret=None, wall=None, shape=None, grp=False, nododge=None, norx=None):
    """Lines that set the one-shot options of the next pj/launch (reset after it). shape 0 sphere, 1 blade
    (hr = half width across the flight); grp=True joins the current volley group #mbGrp (grp_new).
    Chapter mode (AZ-CM): nododge=1: dash i-frames do not help (#pjNoDodge); norx=1: no player-side reaction (#pjNR)."""
    out = []
    for v in (nododge, norx):
        assert v is None or int(v) in (0, 1)
    for k, v in (('#pjEl', el), ('#pjKB', kb), ('#pjRet', ret), ('#pjWall', wall), ('#pjShape', shape),
                 ('#pjNoDodge', nododge), ('#pjNR', norx)):
        if v is not None:
            out.append(f'scoreboard players set {k} mb {int(v)}')
    if grp:
        out.append('scoreboard players operation #pjGrp mb = #mbGrp mb')
    return out


def pj_speed_tenths(spd):
    """The runtime speed (tenths of a block per tick) that flies exactly n = ceil(spd / 0.25) sub-steps of 0.25 b:
    pj/tick takes (4 V + 9) / 10 sub-steps, so V = int(2.5 n) maps back to n (2, 5, 7, 10, 12, 15, 17, ...). Rounding
    spd * 10 instead sent 0.75 / 1.75 / 2.75 b/t one sub-step too fast (review fix FW-2)."""
    n = max(1, math.ceil(float(spd) / 0.25 - 1e-9))
    return int(n * 2.5)


def _tenths_up(v):
    """Tenths, halves rounded up (1.25 -> 13), for the pj hit radius."""
    return int(math.floor(float(v) * 10 + 0.5 + 1e-9))


def pj_launch(spd, life, dmg, hr):
    """As the prop, positioned at the launch point, rotated = flight direction (pitch counts). spd in blocks per
    tick (flown in 0.25 b sub-steps, rounded up: 0.7 and 0.75 both fly 0.75), life ticks, dmg % of the base hit
    (0 = visual), hr hit radius (sphere) / half width (blade) in blocks."""
    return (f'function rlk:mboss/pj/launch {{spd:{pj_speed_tenths(spd)},life:{int(life)},dmg:{int(dmg)},'
            f'hr:{max(1, min(40, _tenths_up(hr)))}}}')


def pj_steer(max_deg):
    """Homing: as a live prop, at it, from the module tick: turn toward the player's chest by <= max_deg (yaw, pitch)."""
    return f'function rlk:mboss/pj/steer {{max:{int(max_deg)}}}'


GRP_NEW = 'function rlk:mboss/grp_new'


# ---------------------------------------------------------------------------------------------
# Chapter-mode call builders (AZ-CM, scratchpad az/contract/cm.md 13.10). Blocks / per-mille in, runtime units out.

def hz_mask(r0, tell, dmg):
    """Mask hazard (kind 6): hits a player whose feet are not within r0 + 0.3 b of a rlk_mb_hzsafe marker of its safe
    group. As anything (position = the hazard marker; not drawn by the framework). r0 in blocks."""
    assert 0 < r0 <= 40 and tell >= 1 and dmg >= 0
    return [f'scoreboard players set #hzR0 mb {_tenths(r0)}',
            f'function rlk:mboss/hz/mask {{tell:{int(tell)},dmg:{int(dmg)}}}']


def hz_safe_new():
    """A new mask safe group in #mbSafeG mb (negative ids, never a hazard id; cm.md 13.6). Then hz_opts(safe_g='cur')
    before each mask of the group and `scoreboard players operation <markers> mbHzSG = #mbSafeG mb` on its safe markers."""
    return 'function rlk:mboss/hz/safe_new'


def aux_opts(shield_w=None, shield_h=None, bar_y=None):
    """One-shot options of the next aux/spawn (AP-FW, cm.md 13.12, Apep FN-29), blocks: the click shield's width / height
    (default 1.2 x 2.2) and the HP bar's height offset (+ up)."""
    out = []
    if shield_w is not None:
        assert 0.1 <= shield_w <= 12
        out.append(f'scoreboard players set #auxShW mb {_tenths(shield_w)}')
    if shield_h is not None:
        assert shield_w is not None and 0.1 <= shield_h <= 12
        out.append(f'scoreboard players set #auxShH mb {_tenths(shield_h)}')
    if bar_y is not None:
        assert -10 <= bar_y <= 10 and _tenths(bar_y) != 0
        out.append(f'scoreboard players set #auxHbY mb {_tenths(bar_y)}')
    return out


def step_flat(spd):
    """As a ground walker, rotated = its heading (facing the target): one step of spd blocks, y on the fight arena's floor,
    inside walk - 0.7 (mboss/mv/step_flat, cm.md 13.12, Apep FN-30)."""
    assert 0 < spd <= 2
    return f'function rlk:mboss/mv/step_flat {{spd:{num(spd, 3)}}}'


def hz_extend(n):
    """As a live hazard marker: its active window and its life grow by n ticks (a lingering field refresh)."""
    assert 1 <= int(n) <= 72000
    return f'function rlk:mboss/hz/extend {{n:{int(n)}}}'


def lockv(lead):
    """Predictive lock: a rlk_mb_lock marker at the player + velocity x lead ticks, inside walk - 0.7 (mboss/mv/lockv)."""
    assert 0 <= int(lead) <= 40
    return f'function rlk:mboss/mv/lockv {{lead:{int(lead)}}}'


def local():
    """As the anchor: #mbLf / #mbLs mb = the player body in the anchor frame (milliblocks, f forward, s left)."""
    return 'function rlk:mboss/mv/local'


def pl_dot(pm, el, lethal=0):
    """Lines of one player DoT tick: pm per mille of the player's max HP, el = #elem for the shield efficiency."""
    assert 1 <= int(pm) <= 1000 and 0 <= int(el) <= 8 and int(lethal) in (0, 1)
    return [f'scoreboard players set #mbDotPct mb {int(pm)}', f'scoreboard players set #mbDotEl mb {int(el)}',
            f'scoreboard players set #mbDotLethal mb {int(lethal)}', 'function rlk:mboss/pl_dot']


def push_ring(r_blocks, kb, to_blocks=None):
    """Push-only ring at the execution position: players within r are moved out to `to` (default r + 0.5) over kb ticks."""
    to = r_blocks + 0.5 if to_blocks is None else to_blocks
    assert 0 < r_blocks <= 40 and r_blocks <= to <= 48 and 1 <= int(kb) <= 10
    return f'function rlk:mboss/push/ring {{r:{_tenths(r_blocks)},to:{_tenths(to)},kb:{int(kb)}}}'


def cine(on):
    """Cine on / off: boss hits on the player (mboss/hurt, pl_dot) are refused while on."""
    return 'function rlk:mboss/cine/' + ('start' if on else 'end')


def repool(pct):
    """Pool split: the body's max HP = #mbTot x pct / 100, full, the bar refills over 30 t."""
    assert 1 <= int(pct) <= 100
    return f'function rlk:mboss/repool {{pct:{int(pct)}}}'


def title(text, sub, color):
    """Rename the fight title (boss bar name, gate texts read cur.title / cur.sub)."""
    for t in (text, sub, color):
        assert '"' not in t and '\\' not in t
    return f'function rlk:mboss/title {{title:"{text}",sub:"{sub}",color:"{color}"}}'


def music(ph):
    """Play the registry music of phase ph (1..9; 0 stops)."""
    assert 0 <= int(ph) <= 9
    return f'function rlk:mboss/music/set {{ph:{int(ph)}}}'


def px_state(name):
    """Switch the hit-proxy state set (a key of the rig manifest's states)."""
    assert name.replace('_', '').isalnum()
    return f'function rlk:mboss/px/state {{set:"{name}"}}'


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
