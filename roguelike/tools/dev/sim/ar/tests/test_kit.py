#!/usr/bin/env python3
"""test_kit.py: the 아를레키노 fx / sound / HUD kit (stage S1K: tools/build_mboss_kn_fx.py) against one worktree.

    python3 test_kit.py <worktree>/roguelike [<resource pack>]

mcsim (lib/mcsim.py, vendored unchanged) runs the kit's own functions through lib/knfxsim.py (the Tachy kit harness +
execute summon, NBT list filters, bossbars, titles, entity merges). Vanilla order: a server tick T runs the functions
(gametime T), then gametime -> T + 1 and the scheduled functions run. Sections:
  names    every api.KIT_PRESETS / KIT_PROPS / KIT_DECALS / KIT_SOUNDS / KIT_HUD / KIT_FIXED name exists with the right
           macro-ness and arguments (the placeholders are exactly the contract args); api.K lines resolve to files
  calls    every kit call S3 (wip/ar-s3) and S2 (wip/ar-s2) generate names an existing function with exactly its args
  engine   card / cardx stages (the first-tick fix), the ager stops, the fx cap, decals never capped
  presets  every preset with test values: cards <= the manifest count, all expire; c 1 / c 2 colours; no flat effect
           card below floor + 0.25 at the documented executor heights; slash arcs never below the floor at the S3 / S2
           call heights (the clamp); vertical cards stand on (never below) the floor
  decals   the seven decals: floor y + 0.02 .. + 0.028, the flash at t - 6, gone by t + hold; the flood re-timed by a
           second call (one disc); rim tint bands inward; strip along the absolute yaw
  props    one display each, dressed in place (model, billboard, scale; no extra entity); wheel frames turn; wisp c 1
           white / c 2 red; a prop on a marker gets one follower that stays on it and goes with it; wisp_turn recolours
  clear    fx/clear removes every card and decal, closes the banner, keeps props and followers (pause)
  uninst   fx/uninstall: cards, followers, stand-ins, objectives, storage rlk:kn fx (other keys kept), bossbar, schedules
  sounds   every recipe: vanilla ids only (scratchpad rd/tests/sound_ids.txt), mboss_lib min volume, pitch 0.5..2,
           the call list equals api.KIT_SOUNDS
  hud      badge on rlk:mboss sub (empty unstyled root, glyph sibling in rlk:mboss_kn, plain name = api.BADGE),
           idempotent, re-appended after a rewrite, off; the banner bossbar = api.BANNER; every line reveals in prefixes
           and ends with api.LINES[id]; clear
  static   no negative add / remove literals, no $( in non-macro lines, lowercase ids, the glyph root rule, no
           tutorial text (only api names / lines / banner / badge strings in text components)
  demos    every fx/test/<preset>, test/prop/<name>, test/decal/<name> runs to the end on the stand-in
  rp       (with a pack) sprites, models, items, atlas entries, the 0.70 M budget, fg references, the gate icon, the font
"""
import json
import math
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = HERE.parent.parent
sys.path.insert(0, str(HERE / 'lib'))
import mcsim  # noqa: E402
import knfxsim  # noqa: E402

WT = Path(sys.argv[1]).resolve()
RP = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
sys.path.insert(0, str(WT / 'tools'))
import build_mboss_kn_fx as G  # noqa: E402
from mboss_arlecchino import api  # noqa: E402
import mboss_lib as L  # noqa: E402

FN = WT / 'data/rlk/function'
FX = FN / 'boss/arlecchino/fx'
TAG = G.TAG
OBJ = G.OBJ
NSF = 'rlk:boss/arlecchino/fx/'
SOUND_IDS = S / 'rd/tests/sound_ids.txt'
FAILS, NCHK = [], [0]
random.seed(5)


def fresh():
    return knfxsim.fresh(FN)


def check(cond, msg):
    NCHK[0] += 1
    if not cond:
        FAILS.append(msg)
        print('FAIL', msg)


def comp(s, e):
    return s.nbt[e.id]['item']['components']


def model(s, e):
    return comp(s, e)['minecraft:item_model']


def kind(s, e):
    return model(s, e).split('/')[-1]


def tint(s, e):
    return comp(s, e)['minecraft:custom_model_data']['colors'][0]


def cdata(s, e):
    return comp(s, e)['minecraft:custom_data']


def stages(s, eid):
    out = {}
    for t, i, ev in s.events:
        if i == eid and ev not in out:
            out[ev] = t
    return out


def fbody(rel):
    return (FX / f'{rel}.mcfunction').read_text(encoding='utf-8')


MAN = json.loads(api.KIT_MANIFEST.read_text(encoding='utf-8'))
FLOOR = float(api.CY)
P0 = (760.5, FLOOR + 1.4, 8.5)
TEST = dict(G.TEST_ARGS)


def targs(table, name, **over):
    a = dict(TEST, **over)
    return {k: a[k] for k in table[name]}


# ============================================================== names
for sub, table in (('p', api.KIT_PRESETS), ('decal', api.KIT_DECALS), ('hud', api.KIT_HUD), ('prop', api.KIT_PROPS)):
    for name, args in table.items():
        p = FX / f'{sub}/{name}.mcfunction'
        check(p.exists(), f'names: {sub}/{name} missing')
        if not p.exists():
            continue
        txt = p.read_text(encoding='utf-8')
        macro = any(l.startswith('$') for l in txt.split('\n'))
        check(macro == bool(args), f'names: {sub}/{name} macro-ness {macro} vs args {args}')
        used = set(re.findall(r'\$\((\w+)\)', txt))
        check(used == set(args), f'names: {sub}/{name} uses {sorted(used)}, contract {args}')
        meth = {'p': api.K.p, 'decal': api.K.decal, 'hud': api.K.hud, 'prop': api.K.prop}[sub]
        line = meth(name, **targs(table, name))
        check(line.split()[1] == f'{NSF}{sub}/{name}', f'names: api.K line {line}')
for name in api.KIT_SOUNDS:
    check((FX / f'snd/{name}.mcfunction').exists(), f'names: snd/{name}')
check(tuple(G.SOUNDS) == tuple(api.KIT_SOUNDS), 'names: sound recipes = api.KIT_SOUNDS')
for name in api.KIT_FIXED:
    check((FX / f'{name}.mcfunction').exists(), f'names: fx/{name}')
check(set(MAN['presets']) == set(api.KIT_PRESETS) and set(MAN['props']) == set(api.KIT_PROPS)
      and set(MAN['decals']) == set(api.KIT_DECALS), 'names: manifest lists')
check(api.K.fixed('clear') == f'function {NSF}clear', 'names: api.K is on (manifest present)')
for name in api.KIT_PRESETS:
    check((FX / f'test/{name}.mcfunction').exists(), f'names: demo test/{name}')
for name in api.KIT_PROPS:
    check((FX / f'test/prop/{name}.mcfunction').exists(), f'names: demo test/prop/{name}')
for name in api.KIT_DECALS:
    check((FX / f'test/decal/{name}.mcfunction').exists(), f'names: demo test/decal/{name}')
for lid in api.LINES:
    check((FX / f'hud/l/{lid}.mcfunction').exists(), f'names: line hud/l/{lid}')

# ============================================================== calls (S3 / S2 as generated with the kit on)
CALL_RE = re.compile(r'function rlk:boss/arlecchino/fx/([a-z0-9_/]+)(?: (\{[^}]*\}|with storage \S+ \S+))?')


def stage_calls(tmp, branch, mods):
    """the kit call lines one stage's generator writes (its tools from the branch, api.K forced on)"""
    out = subprocess.run(['python3', '-I', '-c', f'''
import sys, types
sys.path.insert(0, {str(tmp / branch / 'roguelike/tools')!r})
from mboss_arlecchino import api
api.K._on = lambda: True
class DW:
    def __init__(self): self.files = {{}}; self.out = types.SimpleNamespace(written=set())
    def w(self, rel, body): self.files[rel] = body if isinstance(body, list) else body.split('\\n')
W = DW()
{mods}
for rel, lines in sorted(W.files.items()):
    for ln in lines:
        if 'arlecchino/fx/' in ln: print(rel + '\\t' + ln)
'''], capture_output=True, text=True)
    return out.stdout.splitlines(), out.stderr


CALL_SRC = {
    'wip/ar-s3': ('from mboss_arlecchino import core, ai, bond, p1\nfor p in p1.PATTERNS: p.build(W)\n'
                  'ctx = core.Ctx(list(p1.PATTERNS), W, [])\nai.build(W, ctx); bond.build(W, ctx); core.build(W, ctx)'),
    'wip/ar-s2': 'from mboss_arlecchino import seq\nfor s in seq.SERVICES: s.build(W)',
}
ncalls = 0
TMPD = tempfile.TemporaryDirectory(dir=str(S / 'ar/tmp'))
for br, mods in CALL_SRC.items():
    d = Path(TMPD.name) / br.replace('/', '_')
    d.mkdir(parents=True)
    subprocess.run(f'git -C /home/user/rlk archive {br} roguelike/tools | tar -x -C {d}', shell=True, check=True)
    lines, err = stage_calls(Path(TMPD.name), br.replace('/', '_'), mods)
    check(lines, f'calls: {br} produced kit calls ({err[-300:]})')
    for row in lines:
        rel, ln = row.split('\t', 1)
        for m in CALL_RE.finditer(ln):
            path, args = m.group(1), m.group(2) or ''
            f = FX / f'{path}.mcfunction'
            check(f.exists(), f'calls: {br} {rel}: fx/{path} missing')
            if not f.exists():
                continue
            ncalls += 1
            txt = f.read_text(encoding='utf-8')
            want = set(re.findall(r'\$\((\w+)\)', txt)) if any(l.startswith('$') for l in txt.split('\n')) else set()
            if args.startswith('with'):
                continue
            got = set(re.findall(r'(\w+):', args))
            check(got == want, f'calls: {br} {rel}: fx/{path} args {sorted(got)} vs {sorted(want)}')
check(ncalls > 150, f'calls: {ncalls} kit calls checked')
TMPD.cleanup()

# ============================================================== engine
s = fresh()
T0 = s.gt
s.run(G.card('glow', '^ ^1 ^2', '~ 0', spin=90, s0=1, s1=3, life=8, fade=3, col=G.CRIM))
cs = s.cards()
check(len(cs) == 1, 'engine: one card')
e = cs[0]
check(model(s, e) == 'rlk:mboss/kn_kit/glow' and tint(s, e) == G.CRIM, 'engine: model / tint')
check({TAG, f'{TAG}_c', 'rlk_room', 'rlk_mb_aux'} <= set(e.tags), f'engine: tags {e.tags}')
check(OBJ in s.objectives and all(o in s.objectives for o in G.OBJECTIVES), 'engine: objectives made by the first card')
s.tick(12)
st = stages(s, e.id)
check(st.get('knG') == T0 + 2 and st.get('knF') == T0 + 6 and st.get('kill') == T0 + 9, f'engine: stages {st} from {T0}')
check(not s.cards() and 'rlk:boss/arlecchino/fx/e/world' not in s.sched, 'engine: card gone, the ager stopped')
check(s.sc('#n', OBJ) == 0, 'engine: count back to 0')
s = fresh()
T0 = s.gt
s.run(G.card('glow', bb='center', s0=(1, 2, 1), s1=(2, 4, 2), life=10, fade=2, dly=4, dur=3, hit=6, col2=G.CRIM,
             off=(0, 0, 2.5), move=(0, 0, 3)))
e = s.cards()[0]
cd = cdata(s, e)
check(s.nbt[e.id]['transformation']['scale'] == [0, 0, 0], 'engine: cardx hidden until its delay')
check(cd['knG']['transformation']['translation'] == [0, 0, 5.5], 'engine: cardx end translation = off + move')
s.tick(18)
st = stages(s, e.id)
check(st.get('knS') == T0 + 5 and st.get('knG') == T0 + 6 and st.get('hit') == T0 + 7 and st.get('knF') == T0 + 13
      and st.get('kill') == T0 + 15, f'engine: cardx stages {st}')
s = fresh()
for _ in range(G.CAP + 20):
    s.run(G.card('mote', life=60))
check(len(s.cards()) == G.CAP, f'engine: fx cap {len(s.cards())} == {G.CAP}')
s.run(G.decal('ring_o', r=60, t=30), pos=(760.5, FLOOR, 8.5))
check(len(s.cards(f'{TAG}_d')) == 1, 'engine: decals are never capped')
s.tick(1)
check(s.sc('#n', OBJ) == G.CAP and s.sc('#dn', OBJ) == 1, 'engine: the ager counts fx and decals apart')
s = fresh()
for _ in range(G.SOFT):
    s.run(G.card('mote', life=40))
n0 = len(s.parts)
s.run(G.fx('ambient_petals'))
s.run(G.fx('gate_flames'))
check(len(s.parts) == n0 and len(s.cards()) == G.SOFT, 'engine: ambient presets skipped from SOFT live cards')

# ============================================================== presets
HEIGHT = {'slash_arc': 1.4, 'spin_ring': 1.0, 'twirl_ring': 1.5, 'scythe_form': 1.4, 'embers_puff': 1.4, 'wheel_trail': 0.0,
          'dash_trail': 1.0, 'leap_flare': 0.3, 'dive_streak': 1.0, 'impact_burst': 0.2, 'claw': 1.0, 'wing_burst': 1.4,
          'zig_streak': 1.2, 'brand_ring': 0.0, 'brand_x': 1.0, 'threads': 0.2, 'thorns': 0.0, 'blast': 0.0, 'web': 7.5,
          'clone_trail': 0.0, 'blade_rise': 0.0, 'blade_burst': 1.0, 'cross_thorns': 0.0, 'shock_gain': 1.0, 'shock_aura': 1.3,
          'shock_hit': 1.4, 'break_burst': 1.4, 'stun_motes': 2.9, 'pillar': 0.0, 'shroud': 0.0, 'shroud_burst': 2.9, 'legs_burst': 1.8, 'moon_flare': 9.0,
          'aim_line': 1.8, 'reticle': 1.8, 'beam': 1.8, 'x_mark': 0.0, 'rapid_slash': 1.2, 'final_burst': 0.0,
          'feather_hit': 0.0, 'orb_gather': 0.0, 'orb_burst': 0.0, 'death_flames': 0.0, 'wisp_turn': 1.0,
          'gate_flames': 0.0, 'ambient_petals': 0.0}
assert set(HEIGHT) == set(api.KIT_PRESETS)


def card_bottom(s, e):
    """the lowest world y of a card at its end transformation (vertical / face / cross cards: translation y + b0 x scale
    y; flat / lance cards: their y; billboards upright)"""
    tr = cdata(s, e)['knG']['transformation']
    sc, ty = tr['scale'], tr['translation'][1]
    plane, _wh, ext = G.kind_info(kind(s, e))[:3]
    if plane in ('flat', 'lance'):
        return e.pos[1] + ty
    return e.pos[1] + ty + min(0.0, ext[2] * sc[1])


for name in api.KIT_PRESETS:
    for c in ((1, 2) if 'c' in api.KIT_PRESETS[name] else (None,)):
        over = {'c': c} if c else {}
        s = fresh()
        pos = (760.5, FLOOR + HEIGHT[name], 8.5)
        s.run(G.fx(name, **targs(api.KIT_PRESETS, name, **over)), pos=pos, rot=(30.0, 0.0))
        made = s.cards()
        check(len(made) <= MAN['presets'][name]['cards'], f'presets: {name} c {c}: {len(made)} cards > manifest '
                                                           f'{MAN["presets"][name]["cards"]}')
        if name not in G.PTCL:
            check(made, f'presets: {name} c {c} spawns cards')
        for e in made:
            pl = G.kind_info(kind(s, e))[0]
            if pl == 'flat' and kind(s, e) not in G.DECAL_KINDS:
                check(e.pos[1] >= FLOOR + 0.25 - 1e-6, f'presets: {name}: flat {kind(s, e)} at {e.pos[1] - FLOOR:.2f} b '
                                                       '(effects are not floor decals)')
            check(kind(s, e) not in G.DECAL_KINDS, f'presets: {name} uses the decal sprite {kind(s, e)}')
            if pl in ('face', 'cross') and s.nbt[e.id].get('billboard') in ('vertical', 'fixed') and name != 'x_mark':
                rot_p = e.rot[1] if len(e.rot) > 1 else 0
                if abs(rot_p) < 1e-6 and not s.nbt[e.id]['transformation']['left_rotation']['angle']:
                    check(card_bottom(s, e) >= FLOOR - 1e-6, f'presets: {name}: {kind(s, e)} reaches below the floor '
                                                            f'({card_bottom(s, e) - FLOOR:.2f})')
        s.tick(120)
        check(not s.cards() and 'rlk:boss/arlecchino/fx/e/world' not in s.sched,
              f'presets: {name} c {c}: every card expires, the ager stops')
        if c and name != 'wisp_turn':
            s = fresh()
            s.run(G.fx(name, **targs(api.KIT_PRESETS, name, **over)), pos=pos)
            pn = {p for p, _ in s.parts}
            if c == 1:
                check('minecraft:flame' in pn, f'presets: {name} Pyro flame particles {pn}')
            else:
                check(any('dust' in p for p in pn) and 'minecraft:flame' not in pn, f'presets: {name} crimson particles {pn}')
            kinds_ = {kind(s, e) for e in s.cards()}
            check(not any(k.startswith(('arc_p', 'ring_p')) for k in kinds_) if c == 2 else
                  not any(k.startswith(('arc_c', 'ring_c')) for k in kinds_), f'presets: {name} c {c} sprites {kinds_}')


def arc_lowest(s, e):
    """the lowest world y the arc band reaches (bearings +-80, unit radius x the end scale) from the card's rotation and
    roll"""
    sc = cdata(s, e)['knG']['transformation']['scale'][0]
    roll = s.nbt[e.id]['transformation']['left_rotation']['angle']
    return e.pos[1] - sc * G.arc_low(e.rot[1], math.degrees(roll))


# slash arcs at the call heights S3 / S2 use: never below the floor (the clamp), else the full reach
for h, r, pitch, roll in ((1.4, 42, 0, 0), (1.4, 42, 0, 180), (1.4, 36, -50, 90), (1.4, 40, -40, 90), (1.4, 40, -30, 100),
                          (1.4, 42, -60, 90), (1.8, 56, 0, 10), (1.8, 60, 0, 10), (1.4, 50, 0, 180), (1.2, 20, 0, 90),
                          (0.6, 20, 0, 90), (1.4, 52, 0, 0), (1.4, 36, 30, -90)):
    s = fresh()
    s.run(G.fx('slash_arc', r=r, yaw=0, pitch=pitch, roll=roll, c=1), pos=(760.5, FLOOR + h, 8.5), rot=(15.0, 0.0))
    arcs = [e for e in s.cards() if kind(s, e).startswith('arc_')]
    check(len(arcs) == 4, f'slash_arc: four frames ({len(arcs)})')
    low = min(arc_lowest(s, e) for e in arcs)
    check(low >= FLOOR - 1e-6, f'slash_arc h {h} r {r} pitch {pitch} roll {roll}: lowest {low - FLOOR:.2f} b')
    sc = cdata(s, arcs[0])['knG']['transformation']['scale'][0]
    if G.arc_low(pitch, roll) * r / 10 <= h - 0.1 - 0.05:
        check(abs(sc - r / 10) < 1e-6, f'slash_arc: full reach when it fits ({sc} vs {r / 10})')
    for e in arcs:
        check(abs(((e.rot[0] - 15) + 180) % 360 - 180) < 1e-6 and abs(e.rot[1] - pitch) < 1e-6, f'slash_arc: rotation {e.rot}')
for h, r, pitch, roll, want in ((1.4, 36, -50, 90, 3.4), (1.4, 42, -60, 90, 4.0), (1.2, 20, 0, 90, 1.8)):
    s = fresh()
    s.run(G.fx('slash_arc', r=r, yaw=0, pitch=pitch, roll=roll, c=1), pos=(760.5, FLOOR + h, 8.5))
    e = [e for e in s.cards() if kind(s, e).startswith('arc_')][0]
    sc = cdata(s, e)['knG']['transformation']['scale'][0]
    check(sc >= want and e.pos[1] - (FLOOR + h) <= G.ARC_LIFT / 100 + 1e-6, f'slash_arc: lifted, reach {sc} >= {want} '
          f'(lift {e.pos[1] - FLOOR - h:.2f})')
s = fresh()
s.run(G.fx('slash_arc', r=36, yaw=0, pitch=0, roll=0, c=2), pos=P0)
seen = {}
for t in range(14):
    for e in s.cards():
        seen.setdefault(kind(s, e), []).append(t)
    s.tick(1)
check(set(seen) == {'arc_c0', 'arc_c1', 'arc_c2', 'arc_c3'}, f'slash_arc: crimson frames {sorted(seen)}')
# twirl ring / dive streak clamps
for h in (1.5, 0.9, 0.5):
    s = fresh()
    s.run(G.fx('twirl_ring'), pos=(760.5, FLOOR + h, 8.5))
    for e in s.cards():
        if kind(s, e) in ('ring_c', 'ring_p'):
            rad = cdata(s, e)['knG']['transformation']['scale'][0]
            check(e.pos[1] - rad >= FLOOR - 1e-6, f'twirl_ring at {h}: ring bottom {e.pos[1] - rad - FLOOR:.2f}')
for h, ln in ((9.0, 90), (1.0, 90), (2.5, 60)):
    s = fresh()
    s.run(G.fx('dive_streak', len=ln), pos=(760.5, FLOOR + h, 8.5))
    for e in s.cards():
        if kind(s, e) == 'streak':
            sc = cdata(s, e)['knG']['transformation']['scale']
            low = e.pos[1] - sc[2] * math.sin(math.radians(50)) - sc[1] * 0.5 * math.cos(math.radians(50))
            check(low >= FLOOR - 1e-6, f'dive_streak h {h}: lowest {low - FLOOR:.2f}')
# threads / thorns inside r; wheel trail along the aim, lit at the wheel speed
for r in (260, 60, 10):
    for name in ('threads', 'thorns'):
        s = fresh()
        y0 = FLOOR + (0.2 if name == 'threads' else 0.0)
        s.run(G.fx(name, r=r), pos=(760.5, y0, 8.5))
        cs = [e for e in s.cards() if kind(s, e) in ('thread', 'thorn')]
        check(cs and all(math.hypot(e.pos[0] - 760.5, e.pos[2] - 8.5) <= r / 10 + 1e-6 for e in cs), f'{name} r {r}: inside r')
        check(len(cs) == (4 if name == 'threads' else 6) if r < 60 else len(cs) >= 14, f'{name} r {r}: {len(cs)} cards')
        check(all(e.pos[1] >= y0 - 1e-6 for e in cs), f'{name}: base at / above the executor')
s = fresh()
T0 = s.gt
s.run(G.fx('wheel_trail', len=160), pos=(760.5, FLOOR, 8.5), rot=(90.0, 0.0))
fl = [e for e in s.cards() if kind(s, e) == 'flame']
s.tick(30)
for e in fl:
    d = abs(e.pos[0] - 760.5)
    show = stages(s, e.id).get('knS', T0)
    check(abs((show - T0) - int(d / G.WHEEL_SPEED)) <= 1, f'wheel_trail: flame at {d:.1f} b lit at {show - T0} t')

# ============================================================== decals
DY = (G.DECAL_Y - 1e-6, G.DECAL_Y + 0.008 + 1e-6)


def decal_cards(s):
    return [e for e in s.ents if e.etype == 'item_display' and (f'{TAG}_d' in e.tags or f'{TAG}_fl' in e.tags)]


for name, args in api.KIT_DECALS.items():
    a = {'r': 120, 'r0': 40, 't': 30, 'len': 280, 'w': 30, 'yaw': 37}
    s = fresh()
    T0 = s.gt
    s.run(G.decal(name, **{k: a[k] for k in args}), pos=(760.5, FLOOR, 8.5), rot=(0.0, 0.0))
    cs = decal_cards(s)
    check(cs, f'decals: {name} draws')
    for e in cs:
        dy = e.pos[1] - FLOOR
        check(DY[0] <= dy <= DY[1], f'decals: {name} card at floor + {dy:.4f}')
        check(G.kind_info(kind(s, e))[0] == 'flat' and kind(s, e) in G.DECAL_KINDS, f'decals: {name} kind {kind(s, e)}')
    s.tick(a['t'] + 40)
    if 't' in args:
        flash = []
        for e in cs:
            st = stages(s, e.id)
            if 'hit' in st:
                flash.append(st['hit'] - T0)
            elif tint(s, e) == G.WHITE and 'knS' in st:
                flash.append(st['knS'] - T0)
        # sim times are server ticks + 1 (the ager runs at the end of a tick with gametime already + 1)
        check(flash and all(x == a['t'] - api.DECAL_FLASH + 1 for x in flash), f'decals: {name} flash at t - 6 ({flash})')
        gone = [stages(s, e.id).get('kill', 9999) - T0 for e in cs]
        hold = G.FLOOD_HOLD if name == 'flood' else G.POOL_HOLD if name == 'pool' else G.DECAL_HOLD
        check(all(a['t'] < g <= a['t'] + hold + 1 for g in gone), f'decals: {name} stays past t, gone by t + {hold} ({gone})')
    check(not decal_cards(s), f'decals: {name} expires')
# strip along the absolute yaw, centred, w x len
s = fresh()
s.run(G.decal('strip', len=280, w=30, yaw=37, t=28), pos=(760.5, FLOOR, 8.5), rot=(123.0, 0.0))
e = decal_cards(s)[0]
sc = cdata(s, e)['knG']['transformation']['scale']
check(abs(e.rot[0] - 37) < 1e-6 and abs(sc[0] - 3.0) < 1e-6 and abs(sc[2] - 28.0) < 1e-6 and abs(e.pos[0] - 760.5) < 1e-6,
      f'decals: strip yaw {e.rot}, scale {sc}, centre {e.pos}')
# rim tint: bands from r inward to r0, delays growing inward
s = fresh()
T0 = s.gt
s.run(G.decal('rim_tint', r0=0, r=240, t=34), pos=(760.5, FLOOR, 8.5))
bands = sorted(decal_cards(s), key=lambda e: -cdata(s, e)['knG']['transformation']['scale'][0])
s.tick(5)
radii = [cdata(s, e)['knG']['transformation']['scale'][0] for e in bands]
check(len(bands) == G.RIM_BANDS and abs(radii[0] - 24) < 1e-6, f'decals: rim tint {len(bands)} bands from r 24 ({radii[:3]})')
s.tick(40)
shows = [stages(s, e.id).get('knS', T0) - T0 for e in bands]
check(shows == sorted(shows) and shows[-1] <= 34 - api.DECAL_FLASH, f'decals: rim tint grows inward by t - 6 ({shows})')
s = fresh()
s.run(G.decal('rim_tint', r0=120, r=240, t=34), pos=(760.5, FLOOR, 8.5))
check(all(cdata(s, e)['knG']['transformation']['scale'][0] > 12 for e in decal_cards(s)), 'decals: rim tint stops at r0')
# flood: the second call re-times the shown disc (no second disc) and flashes again
s = fresh()
T0 = s.gt
s.run(G.decal('flood', r=260, t=50), pos=(760.5, FLOOR, 8.5))
s.tick(56)
s.run(G.decal('flood', r=260, t=30), pos=(760.5, FLOOR, 8.5))
mains = s.cards(f'{TAG}_fl')
check(len(mains) == 1, f'decals: flood re-timed, one disc ({len(mains)})')
s.tick(60)
main = mains[0]
st = stages(s, main.id)
check(st.get('kill', 0) - T0 == 56 + 30 + G.FLOOD_HOLD + 1, f'decals: flood stays to the second t + 14 ({st.get("kill", 0) - T0})')
overlays = [e for e in s.ents if f'{TAG}_d' in e.tags and kind(s, e) == 'flood']
s2 = fresh()
s2.run(G.decal('flood', r=260, t=50), pos=(760.5, FLOOR, 8.5))
s2.tick(56)
s2.run(G.decal('flood', r=260, t=30), pos=(760.5, FLOOR, 8.5))
s2.tick(60)
shows = sorted(t for t, i, ev in s2.events if ev == 'knS')
check(len(shows) == 2 and shows[0] - (s2.gt - 116) == 45 and shows[1] - (s2.gt - 116) == 56 + 25, f'decals: flood flashes '
      f'at both t - 6 ({[x - (s2.gt - 116) for x in shows]})')
# donut: two outlines r0 and r
s = fresh()
s.run(G.decal('donut_o', r0=60, r=150, t=21), pos=(760.5, FLOOR, 8.5))
check(sorted(round(cdata(s, e)['knG']['transformation']['scale'][0], 3) for e in decal_cards(s)) == [6.0, 15.0], 'decals: donut r0 / r')
# only the decal functions draw decal sprites; every decal call site of S3 is a §1.5 key
for p in FX.rglob('*.mcfunction'):
    rel = p.relative_to(FX).as_posix()
    if rel.startswith(('decal/', 'test/')):
        continue
    txt = p.read_text(encoding='utf-8')
    for k in G.DECAL_KINDS:
        check(f'kind:"{k}"' not in txt, f'decals: {rel} draws the decal sprite {k}')

# ============================================================== props
for name, (doc, kd, col, bb, scl, anim) in G.PROPS.items():
    s = fresh()
    s.run(f'summon minecraft:item_display 760.5 202.2 8.5 {{Tags:["rlk_kn_p","rlk_room"],teleport_duration:1}}')
    d = [e for e in s.ents if e.etype == 'item_display'][0]
    n0 = len(s.ents)
    line = api.K.prop(name, **({'c': 2} if name == 'wisp' else {}))
    s.run(line, ex=d)
    check(len(s.ents) == n0, f'props: {name} dressed in place (no extra entity)')
    nb = s.nbt[d.id]
    check(nb['item']['components']['minecraft:item_model'] == G.NS_TEX + kd and nb['billboard'] == bb
          and nb['transformation']['scale'] == list(scl), f'props: {name} look {nb.get("billboard")}')
    if name == 'wisp':
        check(nb['item']['components']['minecraft:custom_model_data']['colors'] == [G.SPIRIT[2]], 'props: wisp c 2 red')
        s.run(api.K.prop('wisp', c=1), ex=d)
        check(s.nbt[d.id]['item']['components']['minecraft:custom_model_data']['colors'] == [G.WHITE], 'props: wisp c 1 white')
    s.run(line, ex=d)
    check(len(s.ents) == n0, f'props: {name} re-dress idempotent')
    if anim == 'w':
        s.tick(5)
        frames = [ev[6:] for t, i, ev in s.events if i == d.id and ev.startswith('model:')]
        check(len(set(frames)) == 4, f'props: wheel turns its four frames ({frames})')
        d.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.tick(3)
        check('rlk:boss/arlecchino/fx/e/anim' not in s.sched, 'props: the anim chain stops with the last prop')
    if name in ('blade', 'clone'):
        ext = G.kind_info(kd)[2]
        check(ext[2] >= 0, f'props: {name} stands on its display (never below it)')
# a prop on a marker: one follower that stays on it and goes with it
for name in ('wisp', 'moon_halo'):
    s = fresh()
    s.run('summon minecraft:marker 760.5 202 8.5 {Tags:["rlk_kn_wisp","rlk_kn_wisp_0"]}')
    m = [e for e in s.ents if e.etype == 'marker'][0]
    line = api.K.prop(name, **({'c': 1} if name == 'wisp' else {}))
    s.run(line, ex=m, pos=tuple(m.pos))
    fol = s.cards(G.FOLLOW)
    check(len(fol) == 1, f'props: {name} on a marker: one follower ({len(fol)})')
    s.run(line, ex=m, pos=tuple(m.pos))
    fol = s.cards(G.FOLLOW)
    check(len(fol) == 1, f'props: {name} re-called: still one follower')
    f = fol[0]
    check(s.nbt[f.id]['item']['components']['minecraft:item_model'] == G.NS_TEX + G.PROPS[name][1], f'props: {name} follower look')
    m.pos = [770.0, 205.0, 3.0]
    s.tick(2)
    check(math.dist(f.pos, m.pos) < 1e-6, f'props: {name} follower stays on the marker {f.pos}')
    if name == 'wisp':
        s.run(api.K.p('wisp_turn', c=2), ex=m, pos=tuple(m.pos))
        check(tint(s, f) == G.SPIRIT[2], 'props: wisp_turn c 2 turns the follower red')
        s.run(api.K.p('wisp_turn', c=1), ex=m, pos=tuple(m.pos))
        check(tint(s, f) == G.WHITE, 'props: wisp_turn c 1 white again')
        s.run(f'function {NSF}clear')
        check(f.alive, 'props: fx/clear (pause) keeps the follower')
    s.run('kill @e[type=minecraft:marker]')
    s.tick(2)
    check(not s.cards(G.FOLLOW), f'props: {name} follower gone with its marker')
s = fresh()
s.run('summon minecraft:item_display 760.5 202.2 8.5 {Tags:["rlk_kn_wisp","rlk_kn_wisp1"]}')
d = [e for e in s.ents if e.etype == 'item_display'][0]
s.run(api.K.prop('wisp', c=1), ex=d)
s.run(api.K.p('wisp_turn', c=2), ex=d, pos=tuple(d.pos))
check(tint(s, d) == G.SPIRIT[2], 'props: wisp_turn on a dressed display')

# ============================================================== clear (pause / death_start / cleanup)
s = fresh()
s.run(G.fx('slash_arc', r=36, yaw=0, pitch=0, roll=0, c=1))
s.run(G.decal('flood', r=260, t=50), pos=(760.5, FLOOR, 8.5))
s.run(G.hud('banner', on=1))
s.run(f'function {NSF}clear')
check(not s.cards(), 'clear: every card and decal')
check(s.sc('#n', OBJ) == 0 and s.sc('#dn', OBJ) == 0, 'clear: counts zeroed')
check(s.bossbars.get(G.BANNER_BAR, {}).get('visible') is False, 'clear: the banner is closed')
s = fresh()
s.run(G.fx('impact_burst', r=36, c=1))
s.setsc(('e', s.player.id), 'dead', 1)
s.tick(1)
check(not s.cards(), 'clear: a dead player clears the cards')

# ============================================================== uninstall
s = fresh()
s.storage.setdefault('rlk:kn', {})['core'] = {'x': 1}
s.run(f'function {NSF}test/stage', pos=(760.5, FLOOR, 20.5))
s.run(G.fx('pillar', r=12))
s.run('summon minecraft:marker 760.5 202 8.5 {Tags:["rlk_kn_wisp"]}')
s.run(api.K.prop('wisp', c=1), ex=[e for e in s.ents if e.etype == 'marker'][0])
s.run(G.hud('badge', on=1))
s.run(G.hud('banner', on=1))
s.run(G.hud('line', id=3))
s.run(f'function {NSF}uninstall')
check(not s.cards() and not s.cards(G.FOLLOW) and not [e for e in s.ents if G.DEMO in e.tags], 'uninstall: cards, followers, stand-ins')
check(not (s.objectives & ({OBJ} | set(G.OBJECTIVES))), 'uninstall: objectives removed')
check(not [k for k in s.scores if k[1] in ({OBJ} | set(G.OBJECTIVES))], 'uninstall: no kit scores left')
check('fx' not in s.storage.get('rlk:kn', {}) and s.storage['rlk:kn'].get('core') == {'x': 1}, 'uninstall: storage fx only')
check(G.BANNER_BAR not in s.bossbars, 'uninstall: the banner bossbar removed')
check(not [k for k in s.sched if 'arlecchino/fx' in k], f'uninstall: schedules cleared {s.sched}')
check(not s.storage.get('rlk:mboss', {}).get('sub'), 'uninstall: the badge removed from the sub line')

# ============================================================== sounds
ids = set(SOUND_IDS.read_text().split()) if SOUND_IDS.exists() else None
check(ids is not None, f'sounds: the sound list {SOUND_IDS} exists')
for name, (doc, layers) in G.SOUNDS.items():
    check(layers, f'sounds: {name} has layers')
    txt = fbody(f'snd/{name}')
    for ev, vol, pitch in layers:
        check(ids is None or f'minecraft:{ev}' in ids, f'sounds: {name}: {ev} is not a vanilla sound id')
        check(0.5 <= pitch <= 2.0 and 0 < vol <= 1.0, f'sounds: {name}: vol {vol} pitch {pitch}')
        check(L.sound(ev, vol, pitch) in txt, f'sounds: {name}: mboss_lib.sound line (min volume rule)')
for p in FX.rglob('*.mcfunction'):
    for ln in p.read_text(encoding='utf-8').split('\n'):
        for m in re.finditer(r'playsound (\S+)', ln):
            check(ids is None or m.group(1) in ids, f'sounds: {p.name}: {m.group(1)}')

# ============================================================== hud
s = fresh()
s.storage['rlk:mboss'] = {'sub': [{'text': '붉은 피의 연회', 'color': '#E8B4BC', 'bold': True}]}
s.run(G.hud('badge', on=1))
s.run(G.hud('badge', on=1))
sub = s.storage['rlk:mboss']['sub']
bad = [x for x in sub if any(c.get('font') == G.FONT for c in x.get('extra', []))]
check(len(sub) == 2 and len(bad) == 1, f'hud: badge appended once ({len(sub)})')
b = bad[0]
check(b.get('text') == '' and set(b) == {'text', 'extra'}, f'hud: badge root empty and unstyled {sorted(b)}')
gl = [c for c in b['extra'] if c.get('font')]
check(len(gl) == 1 and gl[0]['text'] == G.glyph('badge'), 'hud: one glyph sibling in the kit font')
name = ''.join(c['text'] for c in b['extra'] if not c.get('font'))
check(name.strip() == api.BADGE[1:] and all('font' not in c for c in b['extra'] if c['text'].strip()
                                            and c['text'] != G.glyph('badge')), f'hud: badge name {name!r} = api.BADGE')
s.storage['rlk:mboss']['sub'] = [{'text': '우인단 집행관 서열 4위'}]       # a rewrite of sub (hud/sub, the framework)
s.tick(11)
sub = s.storage['rlk:mboss']['sub']
check(len(sub) == 2 and any('extra' in x for x in sub), 'hud: the badge comes back after a rewrite of sub (10 t chain)')
s.run(G.hud('badge', on=0))
check(s.storage['rlk:mboss']['sub'] == [{'text': '우인단 집행관 서열 4위'}], 'hud: badge off removes only the badge')
s.tick(11)
check(len(s.storage['rlk:mboss']['sub']) == 1, 'hud: badge stays off')
s.run(G.hud('banner', on=1))
bb = s.bossbars.get(G.BANNER_BAR)
check(bb and bb['visible'] is True and bb['players'] == '@a[tag=player]', f'hud: banner bossbar shown {bb}')
txt = ''.join(re.findall(r'text:"([^"]*)"', bb['name']))
check(txt == api.BANNER and '일반 공격' in txt and '강공격' not in txt, f'hud: banner text = api.BANNER ({txt})')
s.run(G.hud('banner', on=1))
check(len(s.bossbars) == 1, 'hud: banner re-open is idempotent')
s.run(G.hud('banner', on=0))
check(s.bossbars[G.BANNER_BAR]['visible'] is False, 'hud: banner off')
for lid, text in api.LINES.items():
    s = fresh()
    s.run(G.hud('line', id=lid))
    s.tick(80)
    subs = [re.search(r'text:"([^"]*)"', t).group(1) for _g, t in s.titles if t.startswith('subtitle {')]
    check(subs and subs[-1] == text, f'hud: line {lid} ends with api.LINES ({subs[-1:]})')
    check(all(text.startswith(x) for x in subs), f'hud: line {lid} reveals in prefixes')
    check(len(subs) == len(G.typed(text)) and len(subs) >= 2, f'hud: line {lid} {len(subs)} steps')
    hats = [x for x in s.sounds if x[0] == 'minecraft:block.note_block.hat']
    check(len(hats) == len(subs), 'hud: one quiet tick per step')
s = fresh()
s.storage['rlk:mboss'] = {'sub': []}
s.run(G.hud('badge', on=1))
s.run(G.hud('banner', on=1))
s.run(G.hud('line', id=6))
s.tick(3)
s.run(G.hud('clear'))
s.tick(20)
check(not s.storage['rlk:mboss']['sub'] and s.bossbars[G.BANNER_BAR]['visible'] is False, 'hud: clear: badge and banner off')
check(s.titles[-1][1] == 'subtitle ""' and not [k for k in s.sched if 'hud/e' in k], 'hud: clear: the line stops, blanked')

# ============================================================== static
STR_OK = set(api.LINES.values()) | {api.BANNER[:G.BANNER_SPLIT], api.BANNER[G.BANNER_SPLIT:], api.BADGE[1:], '', '  ',
                                    G.glyph('badge'), '아를레키노 sounds: '}
for p in FX.rglob('*.mcfunction'):
    rel = p.relative_to(FX).as_posix()
    txt = p.read_text(encoding='utf-8')
    for i, line in enumerate(txt.split('\n'), 1):
        s_ = line.lstrip()
        if s_.startswith('#'):
            continue
        check(not G.NEG_LIT.search(s_), f'static: {rel}:{i} negative literal')
        check(s_.startswith('$') == ('$(' in s_), f'static: {rel}:{i} macro-ness')
        for rid in re.findall(r'"(rlk:[^"]+)"', s_):
            check(rid == rid.lower(), f'static: {rel}:{i} uppercase id {rid}')
        # the glyph root rule: a component with the kit font is never a root (always inside extra:[...])
        for m in re.finditer(r'font:"([^"]+)"', s_):
            head = s_[:m.start()]
            check(head.rfind('extra:[') > head.rfind('{text:""') - 1 and 'extra:[' in head,
                  f'static: {rel}:{i} glyph font outside an extra list')
        if rel.startswith(('test/sounds',)):
            continue
        for t in re.findall(r'text:"([^"]*)"', s_):
            if '$(' in t:
                continue
            check(t in STR_OK or t.rstrip() in STR_OK or any(t and v.startswith(t) for v in api.LINES.values()),
                  f'static: {rel}:{i} text {t!r} is not a name / line / banner / badge (no tutorial text)')

# ============================================================== demos
allk = list(G.DEMOS) + [f'prop/{p}' for p in G.PROPS] + [f'decal/{d}' for d in G.DECALS]
lens = G.demo_lens()
for name in allk:
    s = fresh()
    s.run(f'function {NSF}test/stage', pos=(760.5, FLOOR, 20.5), rot=(180.0, 0.0))
    s.run(f'function {NSF}test/{name}')
    seen = 0
    for _ in range(lens[name] + 4):
        s.tick(1)
        seen = max(seen, len([e for e in s.ents if e.etype == 'item_display']))
    check(seen > 0 or name in G.PTCL, f'demos: test/{name} showed something')
    check(s.sc('#demo', OBJ) == 0, f'demos: test/{name} ran to its end')
    s.run(f'function {NSF}test/stop')
    check(not [e for e in s.ents if G.DEMO in e.tags], f'demos: test/stop removes the stand-in ({name})')
for extra in ('sounds', 'hud', 'kinds'):
    check((FX / f'test/{extra}.mcfunction').exists(), f'demos: test/{extra}')

# ============================================================== rp
if RP:
    tex = RP / 'assets/rlk/textures/mboss/kn_kit'
    px = 0
    for k, v in G.KINDS.items():
        p = tex / f'{k}.png'
        check(p.exists() and G.png_size(p) == v[1], f'rp: sprite {k}')
        if p.exists():
            px += v[1][0] * v[1][1]
    check(px == G.atlas_px() <= 700_000, f'rp: atlas {px} px <= 0.70 M')
    for k in G.ALL_KINDS:
        check((RP / f'assets/rlk/models/item/mboss/kn_kit/{k}.json').exists(), f'rp: model {k}')
        check((RP / f'assets/rlk/items/mboss/kn_kit/{k}.json').exists(), f'rp: item {k}')
    atlas = json.loads((RP / 'assets/minecraft/atlases/items.json').read_text(encoding='utf-8'))
    have = {s_.get('resource') for s_ in atlas['sources']}
    check(all(G.NS_TEX + k in have for k in G.KINDS), 'rp: atlas sources')
    check(all(G.FG_TEX + v in have for v in G.REF.values()), 'rp: fg references in the atlas')
    gid = api.GATE_ICON_MODEL.split(':')[1]
    check((RP / f'assets/rlk/items/{gid}.json').exists(), f'rp: gate icon {api.GATE_ICON_MODEL}')
    font = json.loads((RP / 'assets/rlk/font/mboss_kn.json').read_text(encoding='utf-8'))
    check(font['providers'][-1] == {'type': 'reference', 'id': 'minecraft:default'}, 'rp: font ends with minecraft:default')
    cps = [ord(ch) for p_ in font['providers'] for row in p_.get('chars', []) for ch in row]
    check(cps and all(0xEB00 <= c <= 0xEBFF for c in cps), 'rp: glyphs in U+EB00-EBFF')
    other = G.font_used_elsewhere(RP, RP / 'assets/rlk/font/mboss_kn.json')
    check(not [c for c in cps if c in other], 'rp: no glyph collision')
    for p in (RP / 'assets/rlk').rglob('*kn_kit*'):
        check(p.as_posix() == p.as_posix().lower(), f'rp: lowercase path {p}')

print(f'test_kit: {NCHK[0] - len(FAILS)}/{NCHK[0]} passed' + (f', {len(FAILS)} FAILED' if FAILS else ''))
sys.exit(1 if FAILS else 0)
