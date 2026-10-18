"""Shared API of the field generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입) module generator (core <-> pattern
modules).

Stable on purpose: the pattern authors (cruise.py, field.py) import this and never edit it. The runtime side of the
same contract (score names, entry points, cancel rules) is documented in the scratchpad file mb3/fg_contract.md.
Copied from tools/mboss_butterfly/api.py and renamed (#bf* -> #fg*, rlk_mb_bf_* -> rlk_mb_fg_*); the butterfly
package is not touched. Fixed on the way (scratchpad mb2/review/core_findings.json): Gen.keep kills the tag's old
marker before re-tagging and every kept marker carries rlk_mb_fg_kept, which p/finish and p/cancel kill (S1);
Gen.release only hides the pattern bar, it never stops the AI (S2).

Units follow the framework: Python helpers take blocks and ticks; at the runtime boundary the framework uses tenths
of a block and damage as a % of the registry base hit (atk 12 x dmgMul 110: 100 = 13 raw).

Rig. The module codes against the rig API rlk:mboss/fieldgen/rig/... (init, spawn, tick, kill, play/<clip>,
form/<dormant|cruise|field|coreup|tower|laser|deployed>, look/<idle|charge|field|groggy|off>, crack/<0..4>,
face/player, face/track, flash, prop/clear) and reads clips, events, parts and props from
tools/mboss_fieldgen_rig_manifest.json (the rig generator's, branch wip/fg-rig). While that file does not exist,
STUB = True: the manifest is tools/mboss_fieldgen/stub_rig_manifest.json and every rig call goes to the stand-in
rlk:mboss/fieldgen/rig_stub/ written by stub_rig.py. Both stub files are removable; with the real manifest present
the build ignores them and deletes F:mboss/fieldgen/rig_stub/.

FX. The effect engine is the fx / audio / HUD kit (tools/build_mboss_fg_fx.py, functions
rlk:mboss/fieldgen/fx/{card,cardx,p/*,tele/*,snd/*,hud/*,prop/*}, font rlk:mboss_fg; API in the scratchpad file
mb3/fg_fx_api.md). Its Python call builders are re-exported here as api.K and on Gen (g.fx, g.snd, g.kcard, g.tele_*,
g.kprop, g.khud), so pattern modules never import the kit themselves. Every helper returns one function line to run in
the executor context the kit documents (position = the event point, rotation = the aim). The core wires the kit's
hooks and HUD (fg_contract.md section 15); its own remaining visuals are vanilla particles and sounds in
F:mboss/fieldgen/cfx/** (core.py).
"""
from pathlib import Path
import json
import math
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402
import build_mboss_fg_fx as K  # noqa: E402  (the fx kit: call builders and tables only, no files written on import)

ID = 'fieldgen'
NS = f'rlk:mboss/{ID}/'
REG = L.load_registry()
ARENA = REG['arena']
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']
BOSS = next(b for b in REG['boss'] if b['id'] == ID)

# ---------------------------------------------------------------------------------------------
# Rig manifest (real or stub) and the clip table.
REAL_MANIFEST = _TOOLS / 'mboss_fieldgen_rig_manifest.json'
STUB_MANIFEST = Path(__file__).resolve().parent / 'stub_rig_manifest.json'
STUB = not REAL_MANIFEST.exists()
MANIFEST = STUB_MANIFEST if STUB else REAL_MANIFEST
_MAN = json.loads(MANIFEST.read_text(encoding='utf-8'))
RIG_DIR = 'rig_stub' if STUB else 'rig'
CLIPS = {c['name']: {'id': c['id'], 'len': c['len'], 'loop': c.get('loop', False), 'next': c.get('next'),
                     'events': dict(c.get('events', {}))} for c in _MAN['clips']}
LOOKS = ['idle', 'charge', 'field', 'groggy', 'off']                          # rig API look/<name>
RIG_FORMS = ['dormant', 'cruise', 'field', 'coreup', 'tower', 'laser', 'deployed']   # rig API form/<name>
CRACKS = range(0, 5)                                                          # rig API crack/<0..4>
PARTS = [p['name'] if isinstance(p, dict) else p for p in _MAN.get('parts', [])]
PROPS = list(_MAN.get('props', []))
RIG_OBJECTIVES = list(_MAN.get('objectives', []))
FALLBACKS = []          # (clip, event, default) used because the manifest lacks the event (printed by the build)
NEED_CLIPS = ('entrance', 'idle_cruise', 'glide', 'bomb_run', 'slam', 'laser', 'missiles', 'coreup', 'tower_throw',
              'warp_out', 'warp_in_field', 'wave', 'field_idle', 'field_erupt', 'field_end', 'break', 'groggy',
              'recover', 'death')
assert all(c in CLIPS for c in NEED_CLIPS), sorted(set(NEED_CLIPS) - set(CLIPS))


def ev(clip, event):
    """Clip tick of a rig event, e.g. ev('slam', 'impact') == 17. Pattern clocks (#fgPT) are 0 on the tick the core
    plays the pattern's clip, so #fgPT == clip tick."""
    return CLIPS[clip]['events'][event]


def ev_or(clip, event, default):
    """ev() with a fallback for an event the manifest does not name (recorded in FALLBACKS, printed by the build)."""
    e = CLIPS.get(clip, {}).get('events', {})
    if event in e:
        return e[event]
    FALLBACKS.append((clip, event, default))
    return default


def clip_len(clip):
    return CLIPS[clip]['len']


def part_sel(name):
    """Selector of a named rig part (fx anchor), e.g. part_sel('core'); None when the rig has no such part."""
    if name not in PARTS:
        return None
    return f'@e[type=minecraft:item_display,tag=rlk_mb_fg_{name},limit=1]'


# ---------------------------------------------------------------------------------------------
# Balance (plan.md "Rotation"). Damage = % of the registry base hit (atk x dmgMul).
DMG = {
    'c1': 80, 'c1s': 140,          # C1 일점 상쇄: each bomb (one hit per volley group of 4) / the finisher slam
    'c2': 140,                     # C2 내려찍기: slam r 5
    'c3': 50,                      # C3 코어: per beam touch (one volley group, re-armed every 10 t)
    'c4': 90,                      # C4 바위 폭탄: each missile (2 volley groups of 5)
    'c5': 220,                     # C5 지면 충격: the full-area blast
    'c6': 130, 'c6s': 110,         # C6 파쇄: each floor burst / each slab throw
    'f1': 120,                     # F1 감소 영역 (field): each eruption (one hit per event)
    'f2': 130, 'f2s': 110,         # F2 파쇄 (field): bursts / slabs
    'wave': 120,                   # 「인력 충격파」: each front
}
KB = {'default': 3, 'light': 2, 'heavy': 4, 'none': 0}

# Range bands (as the Guardian and the butterfly), horizontal distance body -> player body, blocks.
MELEE = 4.0     # melee: d <= 4
FAR = 8.0       # mid: 4 < d < 8, far: d >= 8
BANDS = {'melee': 1, 'mid': 2, 'far': 3}
STATES = {'c': 1, 'f': 2}       # the bag a pattern belongs to: cruise / field
EL_GEO = 5                      # every hit is Geo (registry el 5); no element RES on the boss

# Body and arena radii (blocks from the arena axis).
WALK_R = ARENA['walk'] - 0.7    # 20.3: locked ground-hazard targets (the player's walk disc, framework @WALKP@)
BODY_R = 16.5                   # the device's body (anchor) never goes farther out: spikes clear the wall ring


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def kit_colour(c):
    """A colour for the fx kit (an RGB int) from an int, '#RRGGBB' or (r, g, b) 0..1."""
    if isinstance(c, str):
        return int(c.lstrip('#'), 16)
    if isinstance(c, int):
        return c
    r, g, b = (max(0, min(255, round(255 * float(x)))) for x in c)
    return (r << 16) | (g << 8) | b


GOLD_HEX = BOSS['color']                  # #E8C46A: nameplate, gold glows
GOLD = hexrgb('#FADEA8')                  # beams, columns
GOLD_DEEP = hexrgb('#E6B25A')
AMBER = hexrgb('#C98A2E')
WHITE_GOLD = hexrgb('#FDFBD1')
VIOLET_HEX = '#C58BFF'                    # the field / meter (bossui under-bar colour 1)
VIOLET = hexrgb('#9C86E8')
VIOLET_DEEP = hexrgb('#6C64E3')
ROCK = hexrgb('#AF846E')
LINE_HEX = '#F2E2B0'                      # typed captions (mechanics only: a machine, no voice lines)

# HUD glyphs of the kit font rlk:mboss_fg (U+E700-E7FF; the kit owns the font, K.GLYPHS): the field badge E700, the
# pips E701 empty / E702 full / E703 just counted, the big break badge E704, the 2 px group-gap space E7F1, the "N/20"
# digits E720-E72A (K.digits). The meter line itself (badge, 역장, pips, digits, the first-field hint) is the kit's
# hud/put_sub; the core writes only the break line's badge.
FONT = K.FONT
GLYPH = {'badge': K.glyph('badge'), 'pip_empty': K.glyph('pip0'), 'pip_full': K.glyph('pip1'), 'pip_new': K.glyph('pip2'),
         'break': K.glyph('break_big'), 'gap': K.SP_GAP}
assert [ord(GLYPH[k]) for k in ('badge', 'pip_empty', 'pip_full', 'pip_new', 'break', 'gap')] == \
    [0xE700, 0xE701, 0xE702, 0xE703, 0xE704, 0xE7F1], GLYPH
METER_N = 20                    # the 20-hit break meter (user decision; replaces the 3 Pneuma hits)


def rest_anchor(form, name, default):
    """Height / offset of a named rig anchor in a rest form, from the real manifest's form_states.<form>.rest_anchors
    (rig coordinates: x left, y up, -z forward); `default` (an (x, y, z) tuple) while the stub manifest has none."""
    a = _MAN.get('form_states', {}).get(form, {}).get('rest_anchors', {}).get(name)
    return tuple(float(v) for v in a) if a else tuple(default)


# The core of the field form (the bubble the meter cracks): kit hud/meter_hit runs positioned here above the body.
# The real rig puts it at 4.1 (spec README 1.1, Q13); the kit's own docs say 3.84 (its stub rig).
CORE_FIELD_H = rest_anchor('field', 'core', (0, 4.1, 0))[1]


class Pattern:
    """One pattern a module provides.

    id      stable number: 1-6 cruise patterns C1-C6, 11-12 field patterns F1-F2, 21 「인력 충격파」 (service, started by
            the core at the field's start and end), 20 / 22 the core's field opening / pack-up (service)
    key     directory name F:mboss/fieldgen/p/<key>/
    label   Korean name shown on the boss bar sub-line while it runs
    state   'c' cruise or 'f' field: the bag (and the device state) it runs in
    kind    'normal' (in its state's shuffle bag) or 'service' (started by the core)
    clip    the rig clip the core plays at clock 0 (#fgPT 0 = clip tick 0)
    bands   range bands the bag may pick it in: subset of ('melee', 'mid', 'far')
    lead    ticks before the clip: start runs at #fgPT = -lead
    recover idle ticks after it ends before the next decision
    max_len safety end: the core finishes the pattern at this #fgPT even if it never called p/end
    length  expected end (#fgPT of its p/end) for the boss-bar progress; default max_len - 4
    weight  {band: n} draw weight in that band (default 1 everywhere)
    """

    def __init__(self, id, key, label, state, clip, kind='normal', bands=(), lead=0, recover=20, max_len=120,
                 length=None, weight=None):
        assert kind in ('normal', 'service')
        assert state in STATES, state
        assert kind == 'service' or bands, key
        assert all(b in BANDS for b in bands), bands
        assert clip in CLIPS, (key, clip)
        assert 0 <= lead <= 20
        self.id, self.key, self.label, self.kind, self.state = id, key, label, kind, state
        self.clip, self.bands, self.lead = clip, tuple(bands), int(lead)
        self.recover, self.max_len = recover, max_len
        self.length = length if length is not None else max_len - 4
        assert 0 < self.length <= max_len, (key, self.length, max_len)
        self.weight = {b: int((weight or {}).get(b, 1)) for b in self.bands}
        assert all(1 <= w <= 9 for w in self.weight.values()), (key, self.weight)
        assert set(weight or {}) <= set(self.bands), (key, weight)
        self.el = EL_GEO


# ---------------------------------------------------------------------------------------------
class Gen:
    """Writer handed to every emit(gen). Paths are relative to F:mboss/fieldgen/."""

    def __init__(self, out):
        self.out = out
        self.files = set()

    # -- files
    def w(self, rel, lines):
        if isinstance(lines, str):
            lines = lines.strip('\n').split('\n')
        flat = []
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                flat.extend(ln)
            elif ln is not None:
                flat.extend(ln.split('\n'))
        self.out.write(f'mboss/{ID}/{rel}', flat)
        self.files.add(rel)

    def pw(self, key, name, lines):
        """Write F:mboss/fieldgen/p/<key>/<name> (pattern modules write only these)."""
        self.w(f'p/{key}/{name}', lines)

    def has(self, rel):
        return rel in self.files

    # -- references
    @staticmethod
    def fn(rel):
        return f'function {NS}{rel}'

    @staticmethod
    def rig(call):
        """A rig API call (rig/<call>; the stub rig while STUB)."""
        return f'function {NS}{RIG_DIR}/{call}'

    @staticmethod
    def play(clip):
        assert clip in CLIPS, clip
        return f'function {NS}{RIG_DIR}/play/{clip}'

    @staticmethod
    def look(name):
        assert name in LOOKS, name
        return f'function {NS}{RIG_DIR}/look/{name}'

    @staticmethod
    def form(name):
        """Instant rig form (reloads, tests; clips switch forms themselves)."""
        assert name in RIG_FORMS, name
        return f'function {NS}{RIG_DIR}/form/{name}'

    @staticmethod
    def crack(n):
        assert n in CRACKS, n
        return f'function {NS}{RIG_DIR}/crack/{n}'

    @staticmethod
    def prop(name):
        """rig/prop/<name> when the rig provides that prop (manifest props), else None."""
        return f'function {NS}{RIG_DIR}/prop/{name}' if name in PROPS else None

    @staticmethod
    def end():
        """The pattern is done: the core finishes it after this tick (fg_contract.md §4)."""
        return f'function {NS}p/end'

    @staticmethod
    def release():
        """The dangerous part is over: the pattern bar hides while the pattern finishes a harmless tail. The slot
        stays busy until end(); the AI is never stopped by it (the butterfly's S2 bug is not copied)."""
        return f'function {NS}p/release'

    @staticmethod
    def set_len(t):
        """The pattern now knows its real end (#fgPT of its end()): the boss-bar progress uses it."""
        return f'scoreboard players set #fgPLen mb {int(t)}'

    # -- positions (core utilities; see fg_contract.md §7)
    @staticmethod
    def lockp():
        """Marker rlk_mb_fg_lock on the floor under the player, pulled inside the walk disc r 20.3 (core u/lockw;
        a player hugging the wall is still covered). Keep it with keep(tag, 'rlk_mb_fg_lock')."""
        return f'function {NS}u/lockw'

    @staticmethod
    def lockb():
        """Marker rlk_mb_fg_lock on the floor under the player, pulled inside the body disc r 16.5 (a point the body
        moves to: core u/lockb). Keep it with keep(tag, 'rlk_mb_fg_lock')."""
        return f'function {NS}u/lockb'

    @staticmethod
    def keep(new_tag, src='rlk_mb_fg_lock'):
        """Re-tag the marker of the last lockp()/lockb() so the next call keeps it. The tag's marker of an earlier run
        is killed first, and the kept marker also carries rlk_mb_fg_kept, which the core kills when the pattern ends
        or is cancelled (so no run ever aims at an older run's marker: the butterfly's S1 bug)."""
        return [f'kill @e[type=minecraft:marker,tag={new_tag}]',
                f'tag @e[type=minecraft:marker,tag={src}] add rlk_mb_fg_kept',
                f'tag @e[type=minecraft:marker,tag={src}] add {new_tag}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] remove {src}']

    @staticmethod
    def clamp_walk():
        """As @s = a ground-target marker: pulled toward the arena axis until inside the walk disc (r 20.3)."""
        return f'function {NS}u/clamp_w'

    @staticmethod
    def clamp_body():
        """As @s = a marker the body will move to: pulled toward the axis until inside r 16.5."""
        return f'function {NS}u/clamp_b'

    @staticmethod
    def bstep(kind, d):
        """Body step (as / at the body): 'toward' / 'away' (the player) or 'fwd' (its yaw), d blocks, only when the
        new spot is free and inside r 16.5 (core u/okb)."""
        assert kind in ('toward', 'away', 'fwd'), kind
        return f'function {NS}u/{kind} {{d:{L.num(float(d))}}}'

    @staticmethod
    def tag_last_hz(tag):
        """After a hz/* call: tag the hazard just made (#hzLast) so the pattern can re-aim / resize / cancel it."""
        return f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add {tag}'

    # -- timeline helpers on the pattern clock #fgPT
    @staticmethod
    def at(t, cmd):
        if isinstance(t, tuple):
            return f'execute if score #fgPT mb matches {t[0]}..{t[1]} run {cmd}'
        return f'execute if score #fgPT mb matches {t} run {cmd}'

    @staticmethod
    def every(n, cmd, start=0):
        """Every n ticks of #fgPT (core constants #fgK<n>; n in 2, 3, 4, 5, 6, 8, 10, 20)."""
        assert n in (2, 3, 4, 5, 6, 8, 10, 20)
        return (f'scoreboard players operation #fgM mb = #fgPT mb\n'
                f'scoreboard players operation #fgM mb %= #fgK{n} mb\n'
                f'execute if score #fgM mb matches {start} run {cmd}')

    # -- the fx kit (THE effect engine; fg_fx_api.md). Every helper returns one function line (fx/...) to run in the
    # executor context the kit documents: positioned at the event point (floor points at the floor top), rotated as
    # the aim. Pair every kit telegraph with its framework hazard made in the same tick with the same tell, and
    # g.hz_opts(quiet=1) (+ sfx=0 when the kit recipes give the sound), so the framework outline does not double it.
    kit = K
    fx = staticmethod(K.fx)                  # preset fx/p/<name>, e.g. g.fx('slam'), g.fx('bomb_drop', h=3.8)
    snd = staticmethod(K.snd)                # sound recipe fx/snd/<name>, e.g. g.snd('slam')
    kprop = staticmethod(K.prop)             # as @s = a module-owned item_display: the kit look fx/prop/<name>
    #                                          (g.prop(name) is the RIG's prop, not the kit's)
    klook = staticmethod(K.look)             # as @s = an item_display: a kit kind's model + tint (fx/look)
    khud = staticmethod(K.hud)               # fx/hud/<name> (pops, flashes, notices; the meter / flags are the core's)
    tele_disc = staticmethod(K.tele_disc)    # ground telegraph decals (visual only; blocks in, tenths out)
    tele_ring = staticmethod(K.tele_ring)
    tele_sector = staticmethod(K.tele_sector)
    tele_line = staticmethod(K.tele_line)
    tele_wave = staticmethod(K.tele_wave)    # the 「인력 충격파」 ring (fg_fx_api.md 4.1)
    tele_mline = staticmethod(K.tele_mline)  # moving lanes id 0-7 (C3; fg_fx_api.md 4.2)
    tele_mline_aim = staticmethod(K.tele_mline_aim)
    tele_mline_turn = staticmethod(K.tele_mline_turn)
    tele_mline_end = staticmethod(K.tele_mline_end)
    TELE_CLEAR = f'function {K.FN}tele/clear'   # every kit decal (the core runs it on pause, break, death, test cuts)

    @staticmethod
    def kcard(kind, pos='~ ~ ~', rot='~ ~', col=K.WHITE, col2=-1, **kw):
        """One kit card (fx/card, or fx/cardx with dly / dur / hit / col2 / off / vector sizes): K.card with the tints
        given as an RGB int, '#RRGGBB' or (r, g, b) 0..1. Painted kinds keep their footage colours under white (the
        default); neutral kinds (glow, glint, mote, streak, ripple) take any colour. Kinds: fg_fx_api.md section 3."""
        return K.card(kind, pos, rot, col=kit_colour(col), col2=kit_colour(col2) if col2 != -1 else -1, **kw)

    # -- vanilla fx and sound
    @staticmethod
    def sound(event, vol=1.0, pitch=1.0):
        return L.sound(event, vol, pitch)

    @staticmethod
    def dust(rgb, scale=1.0, pos='~ ~ ~', delta=(0, 0, 0), n=1, speed=0):
        c = L.colour_list(rgb)
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:dust{{color:{c},scale:{L.num(float(scale), 2)}}} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def particle(name, pos='~ ~ ~', delta=(0, 0, 0), speed=0, n=1):
        d = ' '.join(L.num(float(v), 3) for v in delta)
        return f'particle minecraft:{name} {pos} {d} {L.num(float(speed), 3)} {int(n)} force @a[tag=player]'

    @staticmethod
    def ring_dust(rgb, r, n, y=0.15, scale=1.0, cnt=1):
        """Dust points on a horizontal circle of radius r around the execution position (rotation-free)."""
        out = []
        for i in range(n):
            a = math.radians(360 * i / n)
            out.append(Gen.dust(rgb, scale, f'~{L.num(r * math.sin(a), 2)} ~{L.num(y, 2)} ~{L.num(r * math.cos(a), 2)}',
                                (0, 0, 0), cnt))
        return out

    @staticmethod
    def say(text, colour=LINE_HEX, gap=2, hold=40, snd=1):
        return L.say(text, colour, gap, hold, snd)

    # -- hazards (blocks; see mboss_lib.hz_*). Call positioned on the floor point, rotated = aim.
    hz_opts = staticmethod(L.hz_opts)          # + nododge=1 (#hzNoDodge), rearm=N (#hzRearm)
    hz_disc = staticmethod(L.hz_disc)
    hz_ring = staticmethod(L.hz_ring)
    hz_sector = staticmethod(L.hz_sector)
    hz_line = staticmethod(L.hz_line)
    hz_full = staticmethod(L.hz_full)
    hz_aim = staticmethod(L.hz_aim)            # as a live hazard: re-aim (position + yaw of the context)
    hz_resize = staticmethod(L.hz_resize)      # as a live hazard: new radii / line length and width
    tell_line = staticmethod(L.tell_line)
    # -- projectiles (framework pj; blocks per tick / blocks), steering and volley groups
    pj_opts = staticmethod(L.pj_opts)
    pj_launch = staticmethod(L.pj_launch)
    pj_steer = staticmethod(L.pj_steer)
    GRP_NEW = L.GRP_NEW


class TL:
    """Per-tick timeline of one pattern (as the butterfly's): lines are grouped into p/<key>/k/<t> (t < 0: k/m<-t>,
    the lead before the clip) and reached through a small binary dispatch tree on #fgPT, so a tick runs a handful
    of score tests, not every line.

        tl = TL(g, 'slam'); tl.at(8, cmd, ...); tl.span(10, 14, cmd); tl.write(start_head, tick_head, t0=-lead)

    write() puts the lines of tick t0 (the start clock: 0, or -lead) into start; every later tick goes through the
    dispatch from tick. extra_tick lines run on every tick before the dispatch (per-tick work: aim, growth)."""

    def __init__(self, g, key):
        self.g, self.key, self.ev = g, key, {}

    def at(self, t, *lines):
        for line in lines:
            if not line:
                continue
            for one in (line.split('\n') if isinstance(line, str) else line):
                if one:
                    self.ev.setdefault(int(t), []).append(one)

    def span(self, t0, t1, *lines):
        for t in range(t0, t1 + 1):
            self.at(t, *lines)

    def fn(self, rel):
        return f'function {NS}p/{self.key}/{rel}'

    @staticmethod
    def tname(t):
        return f'k/{t}' if t >= 0 else f'k/m{-t}'

    def _node(self, ts):
        if len(ts) <= 6:
            return [f'execute if score #fgPT mb matches {t} run return run {self.fn(self.tname(t))}' for t in ts]
        mid = len(ts) // 2
        a, b = ts[:mid], ts[mid:]
        out = []
        for part in (a, b):
            name = f'd/{part[0]}_{part[-1]}'.replace('-', 'm')
            self.g.pw(self.key, name, [f'# dispatch #fgPT {part[0]}..{part[-1]}'] + self._node(part))
            out.append(f'execute if score #fgPT mb matches {part[0]}..{part[-1]} run return run {self.fn(name)}')
        return out

    def write(self, start_head, tick_head, t0=0, extra_tick=()):
        for t, lines in sorted(self.ev.items()):
            if t > t0:
                self.g.pw(self.key, self.tname(t), [f'# {self.key} clock {t}'] + lines)
        self.g.pw(self.key, 'start', list(start_head) + self.ev.get(t0, []))
        ts = sorted(t for t in self.ev if t > t0)
        self.g.pw(self.key, 'tick', list(tick_head) + list(extra_tick) + self._node(ts))


# =============================================================================================
# Shared stub helper: the walking floor bursts, the lifted slabs and the slab throws of 파쇄 (C6 rock in cruise,
# F2 frock in the field form). Pattern authors may replace it by their own code (writes only p/<key>/**).
def rocks(g, tl, key, pid, burst0, n_burst=8, gap=6, throw0=None, n_throw=5, throw_gap=8, dmg=130, dmg_s=110):
    """Register on the TL `tl` of pattern `key` (id pid): n_burst floor bursts walking onto the player, the first
    striking at clock burst0 and then every `gap` t (each hz/disc r 1.8, tell 10, jumpable #hzY1 1.2, heavy KB, made
    10 t ahead at the walker marker: the first 6 b from the player on the device's side, each next 2.5 b toward the
    player's current position); a slab rises at every burst (tuff display, up 4 b over 15 t); from throw0 one slab
    every throw_gap t flies at the player's locked feet (dmg-0 tell_line 10 t ahead, then a blade pj at 1.5 b/t,
    hr 0.8 -> reach 1.45 b: the framework blade reaches hr + 0.65 (review FW-1), so hr is not the reach). Unthrown
    slabs crumble in the pattern's end / cancel (they carry rlk_mb_fg_pat). Returns the clock by which the last slab
    has landed. Tags rlk_mb_fg_p<pid>w (walker), p<pid>s (slab), p<pid>f (flying slab), p<pid>t<j> (throw locks)."""
    W, S = f'rlk_mb_fg_p{pid}w', f'rlk_mb_fg_p{pid}s'
    walker = f'@e[type=minecraft:marker,tag={W},limit=1]'
    body = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
    tags = f'"rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p{pid}"'
    throw0 = throw0 if throw0 is not None else burst0 + 40
    assert n_throw <= n_burst and throw0 >= burst0 + gap * (n_throw - 1) + 16, (throw0, burst0)
    g.pw(key, 'walker', [
        f'# The burst walker {W}: on the floor 6 b from the player toward the device, inside the walk disc.',
        f'kill @e[type=minecraft:marker,tag={W}]',
        f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {{Tags:[{tags},"{W}"]}}',
        f'execute as {walker} at @s facing entity {body} feet rotated ~ 0 positioned ^ ^ ^6 run tp @s ~ ~ ~',
        f'execute as {walker} run {g.clamp_walk()}'])
    g.pw(key, 'burst', [
        '# One floor burst at the walker (10 t telegraph, jumpable), its slab (hidden until the strike), then the',
        '# walker steps 2.5 b toward the player (onto the player when closer).',
        f'scoreboard players add #fq{pid}K mb 1',
        g.hz_opts(kb=KB['heavy'], y1=1.2, vis=pid * 10 + 1),
        f'execute at {walker} run {g.hz_disc(1.8, 10, dmg)}',
        f'execute at {walker} run summon minecraft:item_display ~ ~0.45 ~ {{Tags:[{tags},"{S}","rlk_mb_fg_pnew"],'
        'teleport_duration:15,brightness:{block:12,sky:15},item:{id:"minecraft:tuff",count:1},'
        'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}',
        'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT -10',
        f'scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS = #fq{pid}K mb',
        'tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew',
        f'execute as {walker} at @e[tag=rlk_body,limit=1] if entity @s[distance=..2.5] run return run tp @s ~ {CY} ~',
        f'execute as {walker} at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2.5 run tp @s ~ {CY} ~'])
    g.pw(key, 'slabs', [
        '# Every waiting slab of this pattern (from its tick): its own clock mbT; 0 = its burst struck: it rises 4 b.',
        f'execute as @e[type=minecraft:item_display,tag={S}] at @s run function {NS}p/{key}/slab'])
    g.pw(key, 'slab', [
        'scoreboard players add @s mbT 1',
        'execute if score @s mbT matches 0 run data merge entity @s {start_interpolation:0,interpolation_duration:12,'
        'transformation:{translation:[0f,0f,0f],left_rotation:[0.08f,0.2f,0f,0.976f],right_rotation:[0f,0f,0f,1f],scale:[2.2f,0.9f,0.6f]}}',
        'execute if score @s mbT matches 0 run tp @s ~ ~4 ~',
        'execute if score @s mbT matches 0 run ' + g.particle('block{block_state:"minecraft:tuff"}', '~ ~ ~', (0.6, 0.2, 0.6), 0, 12),
        'scoreboard players operation #fgM mb = @s mbT',
        'scoreboard players operation #fgM mb %= #fgK4 mb',
        'execute if score @s mbT matches 1.. if score #fgM mb matches 0 run ' + g.particle('falling_dust{block_state:"minecraft:tuff"}', '~ ~-0.3 ~', (0.5, 0.1, 0.5), 0, 1)])
    g.pw(key, 'tl_line', [
        '# @s = the slab about to be thrown: the throw line from its floor point toward the locked feet (dmg 0, 10 t).',
        'function rlk:mboss/mv/dist',
        'execute store result storage rlk:mboss fg.tl.len int 1 run scoreboard players get #mbDist mb',
        'data modify storage rlk:mboss fg.tl merge value {w:24,tell:10,dmg:0}',
        f'execute positioned ~ {CY} ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p{pid}tl,limit=1] feet run function rlk:mboss/hz/line with storage rlk:mboss fg.tl'])
    g.pw(key, 'throw_go', [
        '# @s = the slab: a blade projectile at the locked feet (its own volley group).',
        f'scoreboard players set @s mbId {pid}',
        f'tag @s remove {S}',
        f'tag @s add rlk_mb_fg_p{pid}f',
        'data merge entity @s {teleport_duration:1}',
        g.pj_opts(shape=1, kb=KB['default'], wall=1, grp=True),
        f'execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p{pid}tl,limit=1] feet run {g.pj_launch(1.5, 24, dmg_s, 0.8)}',
        g.sound('entity.breeze.shoot', 0.9, 0.6), g.sound('block.tuff.break', 1.0, 0.7)])
    for j in range(n_throw):
        T = f'rlk_mb_fg_p{pid}t{j}'
        g.pw(key, f'throw_tell{j}', [
            f'# Throw {j + 1} tell (@s = body): lock the player\'s feet ({T}) and draw the line from slab {j + 1}.',
            g.lockp(), g.keep(T),
            f'tag @e[type=minecraft:marker,tag={T}] add rlk_mb_fg_p{pid}tl',
            f'execute as @e[type=minecraft:item_display,tag={S},scores={{mbS={j + 1}}},limit=1] at @s run function {NS}p/{key}/tl_line',
            f'tag @e[type=minecraft:marker,tag={T}] remove rlk_mb_fg_p{pid}tl'])
        g.pw(key, f'throw{j}', [
            f'# Throw {j + 1}: slab {j + 1} flies at lock {T}.',
            g.GRP_NEW,
            f'tag @e[type=minecraft:marker,tag={T}] add rlk_mb_fg_p{pid}tl',
            f'execute as @e[type=minecraft:item_display,tag={S},scores={{mbS={j + 1}}},limit=1] run function {NS}p/{key}/throw_go',
            f'kill @e[type=minecraft:marker,tag={T}]'])
    g.pw(key, 'pj_end', [
        '# A thrown slab ends (#pjEv 1 floor / wall, 2 life): it shatters. A hit (4) lets it fly on (default, harmless).',
        'execute if score #pjEv mb matches 1..2 at @s run ' + g.particle('block{block_state:"minecraft:tuff"}', '~ ~ ~', (0.6, 0.3, 0.6), 0, 16),
        'execute if score #pjEv mb matches 1..2 at @s run ' + g.sound('block.tuff.break', 1.2, 0.6),
        'execute if score #pjEv mb matches 1..2 run scoreboard players set #pjKeep mb 0'])
    tl.at(burst0 - 11, f'scoreboard players set #fq{pid}K mb 0', f'function {NS}p/{key}/walker')
    for k in range(n_burst):
        tl.at(burst0 + gap * k - 10, f'function {NS}p/{key}/burst')
    for j in range(n_throw):
        tl.at(throw0 + throw_gap * j - 10, f'function {NS}p/{key}/throw_tell{j}')
        tl.at(throw0 + throw_gap * j, f'function {NS}p/{key}/throw{j}')
    return throw0 + throw_gap * (n_throw - 1) + 26


def rocks_cancel(pid):
    """Lines that remove everything rocks() made (cancel / end)."""
    return [f'kill @e[tag=rlk_mb_fg_p{pid}]', f'kill @e[type=minecraft:marker,tag=rlk_mb_fg_p{pid}w]']
