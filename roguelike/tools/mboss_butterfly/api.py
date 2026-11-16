"""Shared API of the Moonlit Illusion Butterfly (달빛 환영 나비) module generator (core <-> pattern modules).

Stable on purpose: the pattern authors (human.py, wing.py) import this and never edit it. The runtime side of
the same contract (score names, entry points, cancel rules) is documented in the scratchpad file
mb2/bf_contract.md. Copied from tools/mboss_guardian/api.py and renamed (#gd* -> #bf*), as the reuse study
recommends; the Guardian package is not touched.

Units follow the framework: Python helpers take blocks and ticks; at the runtime boundary the framework uses
tenths of a block and damage as a % of the registry base hit (atk).

Rig. The module codes against the rig API rlk:mboss/butterfly/rig/... (init, spawn, tick, kill, play/<clip>,
look/<dendro|pyro|flat>, form/<human|butterfly>, face/player, face/track, flash, prop/clear, optional prop/<name>)
and reads clips, events, anchors, parts and props from tools/mboss_butterfly_rig_manifest.json (written by the rig
generator tools/build_mboss_butterfly_rig.mjs; API tools/mboss_butterfly_rig_api.md), so a retimed clip reaches the
module on its next build.

FX. The effect engine is the fx / audio / HUD kit (tools/build_mboss_bf_fx.py, functions
rlk:mboss/butterfly/fx/{card,cardx,p/*,tele/*,snd/*,hud/*,prop/*}, API in the scratchpad file mb2/bf_fx_api.md). Its
Python call builders are re-exported here as api.K and on Gen (g.fx, g.snd, g.kcard, g.tele_*, g.kprop, g.khud), so
pattern modules never import the kit themselves.
"""
from pathlib import Path
import json
import math
import sys

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mboss_lib as L  # noqa: E402
import build_mboss_bf_fx as K  # noqa: E402  (the fx kit: call builders only, no files written on import)

ID = 'butterfly'
NS = f'rlk:mboss/{ID}/'
REG = L.load_registry()
ARENA = REG['arena']
CX, CY, CZ = ARENA['cx'], ARENA['cy'], ARENA['cz']
BOSS = next(b for b in REG['boss'] if b['id'] == ID)

# ---------------------------------------------------------------------------------------------
# Rig manifest and the clip table.
MANIFEST = _TOOLS / 'mboss_butterfly_rig_manifest.json'
_MAN = json.loads(MANIFEST.read_text(encoding='utf-8'))
RIG_DIR = 'rig'
CLIPS = {c['name']: {'id': c['id'], 'len': c['len'], 'loop': c.get('loop', False), 'next': c.get('next'),
                     'events': dict(c.get('events', {})), 'retime': c.get('retime'),
                     'authoredLen': c.get('authoredLen', c['len'])} for c in _MAN['clips']}
LOOKS = list(_MAN.get('looks', ['dendro', 'pyro', 'flat']))
PARTS = [p['name'] if isinstance(p, dict) else p for p in _MAN.get('parts', [])]
PROPS = list(_MAN.get('props', []))
RIG_OBJECTIVES = list(_MAN.get('objectives', []))
FALLBACKS = []          # (clip, event, default) used because the manifest lacks the event (printed by the build)


def ev(clip, event):
    """Clip tick of a rig event, e.g. ev('kick_combo', 'hit1') == 8. Pattern clocks (#bfPT) are 0 on the tick the
    core plays the pattern's clip, so #bfPT == clip tick."""
    return CLIPS[clip]['events'][event]


def ev_or(clip, event, default):
    """ev() with a fallback for an event the manifest does not name (recorded in FALLBACKS)."""
    e = CLIPS.get(clip, {}).get('events', {})
    if event in e:
        return e[event]
    FALLBACKS.append((clip, event, default))
    return default


def clip_len(clip):
    return CLIPS[clip]['len']


# Wind-up retiming (butterfly_clips.mjs RETIME, manifest `retime`; user tuning "선딜 좀 줄이고"): the damaging clips are
# authored on the spec timelines and played with about 25 % shorter wind-ups. ev() / clip_len() are played ticks; a
# pattern that times something on an authored tick (a spec timeline tick that is not a manifest event) maps it with rt().
def _warp(knots, t):
    for (a0, b0), (a1, b1) in zip(knots, knots[1:]):
        if t <= a1:
            return b0 + (b1 - b0) * (t - a0) / (a1 - a0)
    a, b = knots[-1]
    return b + (t - a)


def rt(clip, t):
    """Played clip tick of an authored clip tick (rounded half up, as the rig generator maps keys and events); the
    identity for a clip without a retime. rt('kick_combo', 40) == 32 == ev('kick_combo', 'hit2')."""
    kn = CLIPS[clip]['retime']
    return int(t) if not kn else int(math.floor(_warp(kn, t) + 0.5))


def tell_rt(t):
    """A tell length (aim lock / hazard creation -> strike) after the wind-up tuning: about 25 % shorter, never under
    the 10 t floor (plan.md). Since the telegraph rule (10-20) no ground decal shows it: the player reads the motion."""
    return max(10, int(math.floor(0.75 * t + 0.5)))


def part_sel(name):
    """Selector of a named rig part (fx anchor), e.g. part_sel('foot_r'); None when the rig has no such part."""
    if name not in PARTS:
        return None
    return f'@e[type=minecraft:item_display,tag=rlk_mb_bf_{name},limit=1]'


# ---------------------------------------------------------------------------------------------
# Balance (plan.md). Damage = % of the registry base hit (atk x dmgMul).
DMG = {
    # Balance (plan "Review-fix decisions", fairness F1, and "User feedback after the 10-18 release"): HP per minute within
    # about 20 % of the Guardian's for a standing, a melee-walking and a ranged-walking player in the reviewer's fight sim
    # (mb2/balance/bal.py). The fix round cut the butterfly form x0.7 and H1 / H2 (1.70 / 2.06 / 2.00x -> 1.12 / 1.16 /
    # 0.86x); the wind-up tuning (about 25 % shorter, more patterns per minute) brought it back to 1.16 / 1.39 / 1.09x, so
    # H1 / H2 (what hits a swinging melee player most) and the butterfly form were cut again. The player-side Burning of
    # her own Pyro / Dendro alternation is intended and counted in the sim numbers. (the fix round's numbers in brackets)
    'h1a': 55, 'h1b': 70,        # H1 달빛 발차기: flip-kick crescent / axe-kick crescent + ground wave (0.7 / 0.9)
    'h2a': 45, 'h2b': 70,        # H2 달빛 점프: 360 low sweep / kicked Dendro disc (0.6 / 0.9)
    'h3': 130,                   # H3 달빛 돌진: dash kick + ring
    'h4': 120,                   # H4 광폭한 진공: vacuum blade
    'b1': 70,                    # B1 우아한 날개: wing strike (0.8)
    'b2': 35,                    # B2 화염 날개의 습격: each fire crescent (one hit per swing)
    'b3': 80, 'b3t': 20,         # B3 날개 휩쓸개: wing slam fan (0.9) / flame trail touch (max 2)
    'b4': 100,                   # B4 달빛 축복: each homing orb (contact or burst, one hit per orb; 1.2): what reaches a ranged player
    'b5': 130,                   # B5 달빛 해제: the dome (1.5)
}
KB = {'default': 3, 'light': 2, 'heavy': 4, 'none': 0}
COCOON_HP_PCT = 20                    # 달빛 고치: % of the current HP on application (non-lethal)
COCOON_DMG, COCOON_HEAL, COCOON_CRIT = 50, 60, -100      # player DMG %, healing received %, crit points
# 달빛 고치 cure meter (user "일정 체력 이상 회복해야 하게"): while debuffed every heal adds its effective amount (after the
# -40 %, overheal included) to the meter; the debuff goes at CURE_PCT % of max HP (the meter restarts at each application)
CURE_PCT = 15
BUFF_CRIT, BUFF_CRIT_DMG = 15, 50                        # 달빛 축복 받음 (reward): CRIT RATE +15, CRIT DMG +50 (user: not DMG +50 %)
DEW_HEAL_PCT = 13                     # 달빛 이슬: % of max HP per orb (rounded up; x 0.6 under the debuff = 7.8 %: 2 orbs cure)
DEW_N = 3
DEW_R = (6.0, 14.0)                   # spawn ring around the arena centre (blocks)

# Range bands (as the Guardian), horizontal distance boss body -> player body, blocks.
MELEE = 4.0     # melee: d <= 4
FAR = 8.0       # mid: 4 < d < 8, far: d >= 8
BANDS = {'melee': 1, 'mid': 2, 'far': 3}
FORMS = {'h': 1, 'b': 2}

# ---------------------------------------------------------------------------------------------
# Elements and colours (#elem numbering: 1 pyro, 7 dendro).
EL_PYRO, EL_DENDRO = 1, 7
EL_LOOK = {EL_DENDRO: 'dendro', EL_PYRO: 'pyro'}


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


LIME_HEX = '#B6E35A'
LIME = hexrgb('#B6E35A')
LIME_PALE = hexrgb('#E5FBC8')
LIME_CORE = hexrgb('#EDF9DA')
TEAL_DARK = hexrgb('#297272')
OPAL = hexrgb('#D4F8C6')
CYAN = hexrgb('#8DEAF0')
CYAN_DEEP = hexrgb('#39B4C1')
WHITE = (1.0, 1.0, 1.0)
PYRO_GOLD = hexrgb('#FAD77C')
PYRO_MAG = hexrgb('#C680A2')
PYRO_ORANGE = hexrgb('#FF8A3D')
GOLD = hexrgb('#F4EDC9')
GOLD_RING = hexrgb('#E0DD9C')
GOLD_EMBLEM = hexrgb('#D5DD81')
COC_HEX, COC_SWIRL_HEX = '#8C525C', '#E8858A'      # 달빛 고치 badge: maroon fill, salmon swirl
COC = hexrgb(COC_HEX)
COC_SWIRL = hexrgb(COC_SWIRL_HEX)
LINE_HEX = '#D9F5A8'          # typed caption colour (mechanics only: she has no voice lines)


class Pattern:
    """One pattern a module provides.

    id      stable number: 1-4 human patterns H1-H4, 11-14 butterfly patterns B1-B4, 15 B5 달빛 해제 (service),
            20 the transformation (service, core)
    key     directory name F:mboss/butterfly/p/<key>/
    label   Korean name shown on the boss bar sub-line while it runs
    kind    'normal' (in its form's shuffle bag) or 'service' (started by the core)
    form    'h' human or 'b' butterfly: the form it runs in (the bag of that form)
    clip    the rig clip the core plays at clock 0 (#bfPT 0 = clip tick 0)
    bands   range bands the bag may pick it in: subset of ('melee', 'mid', 'far')
    el      element of its hits (1 pyro, 7 dendro): butterfly patterns switch the wing look to it before they start
    lead    ticks before the clip: start runs at #bfPT = -lead (a tell that must begin before the clip's first
            motion, e.g. H1's hit 1 at clip tick 8 with its body tell 10 t ahead -> lead 2)
    close   blocks: human melee patterns burst-run to this distance before the start, None = no
    recover idle ticks after it ends before the next decision
    max_len safety end: the core finishes the pattern at this #bfPT even if it never called p/end
    length  expected end (#bfPT of its p/end) for the boss-bar progress; default max_len - 4
    weight  {band: n} draw weight in that band (default 1 everywhere)
    """

    def __init__(self, id, key, label, form, clip, kind='normal', bands=(), el=EL_DENDRO, lead=0, close=None,
                 recover=20, max_len=120, length=None, weight=None):
        assert kind in ('normal', 'service')
        assert form in FORMS, form
        assert kind == 'service' or bands, key
        assert all(b in BANDS for b in bands), bands
        assert clip in CLIPS, (key, clip)
        assert el in (EL_PYRO, EL_DENDRO), el
        assert 0 <= lead <= 20
        self.id, self.key, self.label, self.kind, self.form = id, key, label, kind, form
        self.clip, self.bands, self.el, self.lead, self.close = clip, tuple(bands), el, int(lead), close
        self.recover, self.max_len = recover, max_len
        self.length = length if length is not None else max_len - 4
        assert 0 < self.length <= max_len, (key, self.length, max_len)
        self.weight = {b: int((weight or {}).get(b, 1)) for b in self.bands}
        assert all(1 <= w <= 9 for w in self.weight.values()), (key, self.weight)
        assert set(weight or {}) <= set(self.bands), (key, weight)


# ---------------------------------------------------------------------------------------------
class Gen:
    """Writer handed to every emit(gen). Paths are relative to F:mboss/butterfly/."""

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
        """Write F:mboss/butterfly/p/<key>/<name> (pattern modules write only these)."""
        self.w(f'p/{key}/{name}', lines)

    def has(self, rel):
        return rel in self.files

    # -- references
    @staticmethod
    def fn(rel):
        return f'function {NS}{rel}'

    @staticmethod
    def rig(call):
        """A rig API call (rig/<call>)."""
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
    def prop(name):
        """rig/prop/<name> when the rig provides that prop (manifest props), else None."""
        return f'function {NS}{RIG_DIR}/prop/{name}' if name in PROPS else None

    @staticmethod
    def end():
        """The pattern is done: the core finishes it after this tick (see bf_contract.md)."""
        return f'function {NS}p/end'

    @staticmethod
    def release():
        """The dangerous part is over: the owning state may move on while the pattern finishes a harmless tail."""
        return f'function {NS}p/release'

    @staticmethod
    def set_len(t):
        """The pattern now knows its real end (#bfPT of its end()): the boss-bar progress uses it."""
        return f'scoreboard players set #bfPLen mb {int(t)}'

    # -- positions (core utilities; see bf_contract.md)
    @staticmethod
    def dest(max_b, keep_b):
        """As the body, at it: marker rlk_mb_bf_dest on the line toward the player, at most max_b blocks from her and
        keep_b short of the player, inside the safe disc (core u/dest). Keep it with keep()."""
        return [f'scoreboard players set #bfDMax mb {int(round(max_b * 10))}',
                f'scoreboard players set #bfDKeep mb {int(round(keep_b * 10))}', f'function {NS}u/dest']

    @staticmethod
    def lockp():
        """Marker rlk_mb_bf_lock on the floor under the player, inside the safe disc (core u/lockp). Keep it with keep()."""
        return f'function {NS}u/lockp'

    KEPT = 'rlk_mb_bf_kept'      # every kept / pattern-summoned marker: p/finish and p/cancel kill them all

    @staticmethod
    def keep(new_tag, src='rlk_mb_bf_dest'):
        """Re-tag the marker of the last dest()/lockp() (src rlk_mb_bf_dest / rlk_mb_bf_lock) so the next call keeps it.
        An older marker of new_tag goes first, and the kept one also carries rlk_mb_bf_kept, which the core kills when
        the pattern ends or is cancelled (review fix S1: kept markers used to pile up, one per run, and
        `@e[tag=<kept>,limit=1]` picked the OLDEST, so every later run aimed at the first run's spot)."""
        return [f'kill @e[type=minecraft:marker,tag={new_tag}]',
                f'tag @e[type=minecraft:marker,tag={src}] add {new_tag}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] add {Gen.KEPT}',
                f'tag @e[type=minecraft:marker,tag={new_tag}] remove {src}']

    # -- timeline helpers on the pattern clock #bfPT
    @staticmethod
    def at(t, cmd):
        if isinstance(t, tuple):
            return f'execute if score #bfPT mb matches {t[0]}..{t[1]} run {cmd}'
        return f'execute if score #bfPT mb matches {t} run {cmd}'

    @staticmethod
    def at_body(t, sub):
        """sub = the rest of an execute chain after 'at @s rotated as @s rotated ~ 0' (body yaw)."""
        rng = f'{t[0]}..{t[1]}' if isinstance(t, tuple) else t
        return f'execute if score #bfPT mb matches {rng} at @s rotated as @s rotated ~ 0 {sub}'

    @staticmethod
    def every(n, cmd, start=0):
        """Every n ticks of #bfPT (core constants #bfK<n>; n in 2, 3, 4, 5, 6, 8, 10, 20)."""
        assert n in (2, 3, 4, 5, 6, 8, 10, 20)
        return (f'scoreboard players operation #bfM mb = #bfPT mb\n'
                f'scoreboard players operation #bfM mb %= #bfK{n} mb\n'
                f'execute if score #bfM mb matches {start} run {cmd}')

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
        """A gold card of Navia's engine (rlk:fx/nv: rose, star, burst, crescent, petal, shard, ring, glow; gold only,
        cap 48 shared with Navia); see tools/build_navia_fx_cards.py card_call. Prefer the kit (g.fx / g.kcard): the
        butterfly no longer uses this."""
        from build_navia_fx_cards import card_call
        return card_call(kind, pos, **kw)

    # -- the fx kit (THE effect engine; bf_fx_api.md). Every helper returns one function line (fx/... ) to run in
    # the executor context the kit documents (position = the event point, rotation = the aim).
    kit = K
    fx = staticmethod(K.fx)                  # preset fx/p/<name>, e.g. g.fx('kick_rise'), g.fx('rel_dome', r=10.0)
    snd = staticmethod(K.snd)                # sound recipe fx/snd/<name>
    kprop = staticmethod(K.prop)             # as @s = a module-owned item_display: the kit look fx/prop/<name>
    khud = staticmethod(K.hud)               # fx/hud/<name> (badges, actionbar notices, pops, screen flashes)
    # ground telegraph decals (visual only; pair with hz/* + #hzQuiet 1). Unused by the butterfly's patterns since the
    # telegraph rule (10-20: a ground telegraph only where the reference footage shows one, and it shows none for her)
    tele_disc = staticmethod(K.tele_disc)
    tele_ring = staticmethod(K.tele_ring)
    tele_sector = staticmethod(K.tele_sector)
    tele_line = staticmethod(K.tele_line)

    @staticmethod
    def kcard(kind, pos='~ ~ ~', rot='~ ~', col=K.WHITE, col2=-1, **kw):
        """One kit card (fx/card, or fx/cardx with dly / dur / hit / col2 / vector sizes): K.card with the tints given
        as an RGB int, '#RRGGBB' or (r, g, b) 0..1. Painted kinds keep their video colours under white (the default);
        neutral kinds (glow, glint, mote, streak, leaf, bfly, ripple) take any colour. Kinds: bf_fx_api.md section 3."""
        return K.card(kind, pos, rot, col=kit_colour(col), col2=kit_colour(col2) if col2 != -1 else -1, **kw)

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
    tell_line = staticmethod(L.tell_line)
    # -- projectiles (framework pj; blocks per tick / blocks), steering and volley groups
    pj_opts = staticmethod(L.pj_opts)
    pj_launch = staticmethod(L.pj_launch)
    pj_steer = staticmethod(L.pj_steer)
    GRP_NEW = L.GRP_NEW


class TL:
    """Per-tick timeline of one pattern (promoted from the Guardian's p12.py): lines are grouped into
    p/<key>/k/<t> (t < 0: k/m<-t>, the lead before the clip) and reached through a small binary dispatch tree
    on #bfPT, so a tick runs a handful of score tests, not every line.

        tl = TL(g, 'kick'); tl.at(8, cmd, ...); tl.span(10, 14, cmd); tl.write(start_head, tick_head, t0=-lead)

    write() puts the lines of tick t0 (the start clock: 0, or -lead) into start; every later tick goes through
    the dispatch from tick."""

    def __init__(self, g, key):
        self.g, self.key, self.ev = g, key, {}

    def at(self, t, *lines):
        for line in lines:
            if not line:
                continue
            for one in (line.split('\n') if isinstance(line, str) else line):
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
            return [f'execute if score #bfPT mb matches {t} run return run {self.fn(self.tname(t))}' for t in ts]
        mid = len(ts) // 2
        a, b = ts[:mid], ts[mid:]
        out = []
        for part in (a, b):
            name = f'd/{part[0]}_{part[-1]}'.replace('-', 'm')
            self.g.pw(self.key, name, [f'# dispatch #bfPT {part[0]}..{part[-1]}'] + self._node(part))
            out.append(f'execute if score #bfPT mb matches {part[0]}..{part[-1]} run return run {self.fn(name)}')
        return out

    def write(self, start_head, tick_head, t0=0):
        for t, lines in sorted(self.ev.items()):
            if t > t0:
                self.g.pw(self.key, self.tname(t), [f'# {self.key} clock {t}'] + lines)
        self.g.pw(self.key, 'start', list(start_head) + self.ev.get(t0, []))
        ts = sorted(t for t in self.ev if t > t0)
        self.g.pw(self.key, 'tick', list(tick_head) + self._node(ts))


# =============================================================================================
# Human-pattern author (H1-H4 in human.py, the S1 / S3 / S4 sequences in seq_h.py): shared helpers. Every name
# carries an h_ / H_ prefix so it never collides with the wing author's block (theirs: WALK_R, anchor, lockw).
H_WALK_R = ARENA['walk'] - 0.7        # 20.3: the player's walk disc (the framework's @WALKP@)
H_ANCHOR_FALLBACKS = []               # (clip, event, part) taken from the caller's default (no manifest anchor)


def h_anchor(clip, event, part, default):
    """Body-frame position '^x ^y ^z' of a rig anchor at a clip event (manifest clips[].anchors[event][part]: rig
    coordinates x her left, y up, -z forward, so the body frame is ^x ^y ^-z; README Q3). default ('^x ^y ^z') when
    the manifest has none at that event: the spec's body-frame point."""
    c = next((c for c in _MAN['clips'] if c['name'] == clip), {})
    a = c.get('anchors', {}).get(event, {}).get(part)
    if a is None:
        H_ANCHOR_FALLBACKS.append((clip, event, part))
        return default
    return f'^{L.num(float(a[0]), 3)} ^{L.num(float(a[1]), 3)} ^{L.num(-float(a[2]), 3)}'


def _lock_walk(tag, steps=3):
    """Lines (any executor): marker <tag> on the floor under the player, pulled inside the WALK disc (r 20.3) instead
    of the safe disc (plan Q8: a locked ground hazard still covers a player hugging the wall; the points the body moves
    to keep the r 18.5 of u/dest / mv/clamp). The player's feet are at most about 20.7 b out, so 3 steps of 0.25 b
    toward the centre are enough. Kill <tag> in the pattern's cancel."""
    sel = f'@e[type=minecraft:marker,tag={tag},limit=1]'
    out = [f'kill @e[type=minecraft:marker,tag={tag}]',
           f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","{tag}","rlk_mb_bf_kept"]}}']
    out += [f'execute as {sel} at @s unless entity @e[tag=rlk_mb_arena,distance=..{L.num(H_WALK_R)},limit=1] '
            f'facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25'] * steps
    return out


def _ring_dust(rgb, r, n, y=0.15, scale=1.0, cnt=1):
    """Dust points on a horizontal circle of radius r around the execution position (rotation-free)."""
    out = []
    for i in range(n):
        a = math.radians(360 * i / n)
        out.append(Gen.dust(rgb, scale, f'~{L.num(r * math.sin(a), 2)} ~{L.num(y, 2)} ~{L.num(r * math.cos(a), 2)}',
                            (0, 0, 0), cnt))
    return out


Gen.h_lock_walk = staticmethod(_lock_walk)
Gen.h_ring_dust = staticmethod(_ring_dust)
Gen.h_anchor = staticmethod(h_anchor)


# =============================================================================================
# Wing-pattern author (wing.py B1-B5, seq_b.py S2 / S5 / S6): shared helpers. The runtime side lives in
# F:mboss/butterfly/wx/** (written by seq_b.emit): walk-disc and body clamps, the butterfly body leash.
WX = 'wx'                     # F:mboss/butterfly/wx/** (seq_b.py)
WALK_R = 20.3                 # locked ground-hazard targets: the walk disc (plan Q8; the framework's @WALKP@)
BODY_R_B = 16.5               # her body in butterfly form (plan Q9: wing tips clear the wall ring)
REL_R = 16.0                  # the 달빛 해제 release point (plan Q9)


def _bf(v):
    """body-frame tuple -> '^x ^y ^z' (x her left, y up, z forward)"""
    return ' '.join('^' + L.num(round(float(c), 3), 3) for c in v)


def anchor_xyz(clip, event, part, default):
    """A rig fx anchor of the manifest (clips[].anchors[event][part], rig coordinates: x her left, y up, -z her front)
    as a body-frame tuple (x left, y up, z forward); `default` (body frame) when the manifest has none at that event."""
    c = next((c for c in _MAN.get('clips', []) if c.get('name') == clip), None)
    a = ((c or {}).get('anchors') or {}).get(event, {}).get(part)
    if a is None:
        return tuple(float(x) for x in default)
    return (float(a[0]), float(a[1]), -float(a[2]))


def anchor(clip, event, part, default):
    """anchor_xyz() as '^x ^y ^z' for an execute positioned in the body frame (rotated as the body, pitch 0)."""
    return _bf(anchor_xyz(clip, event, part, default))


def rest_anchor_xyz(form, part, default):
    """A part's anchor in a form's rest pose (manifest form_states[form].rest_anchors), body frame."""
    a = ((_MAN.get('form_states') or {}).get(form) or {}).get('rest_anchors', {}).get(part)
    if a is None:
        return tuple(float(x) for x in default)
    return (float(a[0]), float(a[1]), -float(a[2]))


def rest_anchor(form, part, default):
    return _bf(rest_anchor_xyz(form, part, default))


# Rest anchors of the hovering butterfly (the rig's form_states.butterfly, rounded), body frame: defaults only.
B_CORE = (0.0, 3.24, 0.23)
B_FWTIP_L, B_FWTIP_R = (3.13, 5.99, -1.33), (-3.13, 5.99, -1.33)
B_HWTIP_L, B_HWTIP_R = (2.75, 2.98, -0.56), (-2.75, 2.98, -0.56)


def lockw():
    """Marker rlk_mb_bf_lock on the floor under the player, pulled inside the WALK disc (r 20.3, plan Q8: a player
    hugging the wall is still covered); keep it with Gen.keep(tag, 'rlk_mb_bf_lock')."""
    return f'function {NS}{WX}/u/lockw'


def clamp_walk():
    """As @s = a ground-target marker: pulled toward the arena axis until inside the walk disc (r 20.3)."""
    return f'function {NS}{WX}/u/clamp_w'


def clamp_body():
    """As @s = a marker the butterfly body will move to: pulled inside r 16.5 (plan Q9)."""
    return f'function {NS}{WX}/u/clamp_b'


def clamp_release():
    """As @s = the 달빛 해제 release-point marker: pulled inside r 16 (plan Q9)."""
    return f'function {NS}{WX}/u/clamp_r'


def bstep(kind, d):
    """Butterfly body step (as / at the body): kind 'toward' / 'away' (the player) or 'fwd' (her yaw), d blocks,
    only when the new spot is inside r 16.5 and free (wx/u/okb)."""
    assert kind in ('toward', 'away', 'fwd'), kind
    return f'function {NS}{WX}/u/{kind} {{d:{L.num(float(d))}}}'
