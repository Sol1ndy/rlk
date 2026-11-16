#!/usr/bin/env python3
"""test_clips_h1c.py: the 12 new fight clips of the 홍련 rebuild (lane H1c; hr_design.md §2.2-§2.3, §8.2, §8.5) as shipped.

    python3 test_clips_h1c.py <roguelike dir> [-v]          (run from a copy outside the datapack, tools/dev/sim/README.md §1)

Reads the built rig only: tools/scarlet_rig_manifest.json (clips, support, retarget), the anchor table
(F:boss/scarlet/rig/an/load: hand_l hand_r blade_tip blade_mid chest head hat_crown scabbard_mouth per clip tick, local
"^left ^up ^forward") and the key files (the pelvis and the hat state). The builder already fails on a part under the
floor, a turn above 120 deg per tick, the blade in her body at an event, a fist / hilt in her head or torso
(tools/scarlet_rig_api.md §8); this suite checks what the design asks of the new clips on top of that:

  contract  names / lengths / events = api.CLIPS, owner H1, authored (no placeholder), a footage source, the sword held in
            her left hand all through, every correction guard inside its bound, two-hand contacts <= 0.12 b
  joins     tick 0 and the last tick = the stance (idle; idle2 for the P2 clips) within the anchor tolerances of test_rig;
            q_air 0 = q_grab 20 = q_grab 21 (the grab hands over; the module branches at 21), grog_in 12 = `down` 0 (the hat on DOWN's spot)
  root      no root motion: the pelvis stays within 0.16 b of the anchor's axis at every tick
  air       airborne spans: nb one span <= 44 t, q_air two spans <= 38 t each (§8.5), none in the ground clips
  hits      per hazard of §2.2 the blade does what the hazard's shape needs at its hit tick: a forward cut crosses her
            front between hit - 1 and hit + 1 (or points along it) with its tip >= 1.2 b out, a ring / dome cut is flat
            (|elevation| <= 30 deg), out at chest height and she is turning, a band / dive cut comes down through the tick,
            the thrusts point at the target at full reach, the grab's hand is out before her
  cues      at every parry cue tick (hit - 7 of a parryable hit) and every flash tick the blade is not hidden end-on to the
            F5 camera (seen length >= 0.45 b of its 1.44 b from the lens 3.4 b behind and 3.35 b over a player 6 b away;
            from below when she is airborne), so the glint at blade_mid shows on a readable blade
"""
import json
import math
import re
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
VERBOSE = '-v' in sys.argv[2:]
sys.path.insert(0, str(WT / 'tools'))
from mboss_scarlet import api  # noqa: E402

MAN = json.loads((WT / 'tools/scarlet_rig_manifest.json').read_text(encoding='utf-8'))
RIG = WT / 'data/rlk/function/boss/scarlet/rig'
NEW = ('grog_in', 'd4', 'tri', 'rings', 'ult', 'hcut', 'blue', 'kcut', 'mx', 'nb', 'q_grab', 'q_air')
P2 = ('mx', 'nb', 'q_grab', 'q_air')            # P2-only clips: they start and end in the P2 stance (idle2)
FAILS, NCHK = [], [0]


def check(cond, msg, detail=''):
    NCHK[0] += 1
    if not cond:
        FAILS.append(msg)
        print('FAIL', msg, detail)
    elif VERBOSE:
        print('ok  ', msg, detail)


# ----------------------------------------------------------------------------- the anchor table and the key files
AN = {}
for line in (RIG / 'an/load.mcfunction').read_text(encoding='utf-8').splitlines():
    m = re.match(r'data modify storage rlk:hr rig\.an\[(\d+)\]\.(\w+) set value (\[.*\])$', line)
    if m:
        AN[(int(m.group(1)), m.group(2))] = [[float(v.lstrip('^') or 0) for v in s_.split()] for s_ in json.loads(m.group(3))]


def an(clip, name, t):
    """anchor `name` of clip tick t: (left, up, forward) blocks from her feet, in her own frame"""
    return AN[(MAN['clips'][clip]['id'], name)][t]


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def blade(clip, t):
    """(unit direction mid -> tip, tip, mid)"""
    mid, tip = an(clip, 'blade_mid', t), an(clip, 'blade_tip', t)
    d = sub(tip, mid)
    n = math.sqrt(sum(x * x for x in d)) or 1
    return [x / n for x in d], tip, mid


def bearing(p):
    """degrees from her front, + toward her right (left is ^x +)"""
    return math.degrees(math.atan2(-p[0], p[2]))


def elev(d):
    return math.degrees(math.asin(max(-1, min(1, d[1]))))


NUM = re.compile(r'-?[\d.]+(?:e-?\d+)?')
UUID = {p['name']: p['uuid'] for p in MAN['parts']}
KEY = re.compile(r'data merge entity (\S+) \{start_interpolation:0,interpolation_duration:(\d+),transformation:(.*)\}$')


def pelvis_track(clip):
    """the shipped pelvis translation per tick (the client's linear interpolation between its keys)"""
    L = MAN['clips'][clip]['len']
    out, frm, to, t0, d = [], None, None, 0, 0
    for t in range(L + 1):
        f = RIG / 'c' / clip / 'k' / f'{t}.mcfunction'
        if f.exists():
            for line in f.read_text(encoding='utf-8').splitlines():
                m = KEY.match(line)
                if m and m.group(1) == UUID['pelvis']:
                    cur = out[-1] if out else None
                    tr = [float(x) for x in NUM.findall(re.search(r'translation:\[([^\]]*)\]', m.group(3)).group(1))]
                    frm, to, t0, d = cur, tr, t, int(m.group(2))
        if to is None:
            out.append(None)
        elif d == 0 or frm is None or t >= t0 + d:
            out.append(to)
        else:
            u = (t - t0) / d
            out.append([a + (b - a) * u for a, b in zip(frm, to)])
    return out


def hat_states(clip):
    cur, out = None, []
    for t in range(MAN['clips'][clip]['len'] + 1):
        f = RIG / 'c' / clip / 'k' / f'{t}.mcfunction'
        if f.exists():
            for line in f.read_text(encoding='utf-8').splitlines():
                m = re.match(r'scoreboard players set @s hrRigHat (\d)$', line)
                if m:
                    cur = api.LOOKS['hat'][int(m.group(1))]
        out.append(cur)
    return out


# ============================================================== contract
BOUND = MAN['retarget']['bounds']
for c in NEW:
    k = MAN['clips'].get(c)
    check(k is not None, f'contract: {c} is in the rig manifest')
    if not k:
        continue
    ln, lp, ev = api.CLIPS[c]
    check(k['len'] == ln and k['loop'] is None and k['events'] == ev, f'contract: {c} len / events = api.CLIPS', f'{k["len"]} {k["events"]}')
    check(k['owner'] == 'H1' and k['authored'] and not k.get('placeholder'), f'contract: {c} is authored (owner H1, no placeholder)')
    check(bool(k['source']), f'contract: {c} names its footage')
    check(k['key_files'] >= min(ln, 10) and k['keys_per_tick'] >= 3, f'contract: {c} is animated', f'{k["key_files"]} key files, {k["keys_per_tick"]} keys / t')
    sup, ret = MAN['support'][c], MAN['retarget']['clips'][c]
    check(sup['held'] == [[0, ln]], f'contract: {c}: the sword in her left hand all through', str(sup['held']))
    over = {g: v for g, v in ret['corrections'].items() if v >= BOUND.get(g.rstrip('+-'), 1e9) - 1e-6}
    check(not over, f'contract: {c}: every correction guard inside its bound', str(over))
    check(ret['contacts'].get('twohand', 0) <= 0.12 and ret['stretch'] <= 1.0005, f'contract: {c}: two-hand contact <= 0.12 b, no IK stretch',
          str(ret['contacts']))
    check(all(0 <= t < ln for t in ev.values()), f'contract: {c}: every event inside the clip')
check(api.CLIPS['q_grab'][2] == {'glint': 0, 'ghost': 4, 'star': 8, 'lock': 13, 'go': 16, 'grab': 20}, 'contract: q_grab has §8.2\'s events (star 8)')

# ============================================================== joins (no pop into / out of the stance clips)
TOL = {'head': .06, 'chest': .06, 'hat_crown': .12, 'hand_l': .12, 'hand_r': .12, 'scabbard_mouth': .14, 'blade_mid': .2, 'blade_tip': .25}


def meets(a, ta, b, tb):
    return {n: round(dist(an(a, n, ta), an(b, n, tb)), 3) for n in TOL if dist(an(a, n, ta), an(b, n, tb)) > TOL[n]}


for c in NEW:
    ln = api.CLIPS[c][0]
    st = 'idle2' if c in P2 else 'idle'
    if c == 'q_air':
        for tg in (api.ev('q_grab', 'grab'), getattr(api, 'Q_AIR_T0', 21)):      # (the module takes the branch at Q_AIR_T0)
            bad = meets(c, 0, 'q_grab', tg)
            check(not bad, f'joins: q_air 0 = q_grab {tg} (the grab hands over to the throw)', str(bad))
    elif c != 'grog_in':            # (grog_in starts from any pose: blend 2)
        bad = meets(c, 0, st, 0)
        check(not bad, f'joins: {c} 0 = {st} 0', str(bad))
    if c == 'grog_in':
        bad = meets(c, ln, 'down', 0)
        check(not bad, 'joins: grog_in 12 = down 0 (lying, the hat beside her leg)', str(bad))
        hs = hat_states(c)
        check(hs[5] == 'worn' and hs[6] == 'world' and hs[ln] == 'world', 'joins: grog_in: the hat leaves her head at hat_off 6', f'{hs[5]} {hs[6]}')
        h6, h10, h12 = (an(c, 'hat_crown', t) for t in (5, 10, 12))
        check(dist(h10, h12) < .02 and h12[1] < .5 and dist(h6, h10) > 1.0, 'joins: grog_in: the hat flies 6-10 and lies still from land 10',
              f'{h6} {h10} {h12}')
        check(an(c, 'head', ln)[1] < .6 and an(c, 'head', ln)[2] < -.8, 'joins: grog_in ends on her back, the head behind her feet', str(an(c, 'head', ln)))
    else:
        bad = meets(c, ln, st, 0)
        check(not bad, f'joins: {c} {ln} = {st} 0', str(bad))

# ============================================================== root (the module moves her; a clip only poses her)
for c in NEW:
    tr = [p for p in pelvis_track(c) if p]
    far = max(math.hypot(p[0], p[2]) for p in tr)
    lim = 0.3 if c == 'grog_in' else 0.16       # (she topples backward where she stands: the hips slide back a little)
    check(far <= lim, f'root: {c}: the pelvis stays over the anchor ({far:.3f} b <= {lim})')

# ============================================================== air (§8.5: no clip holds her out of reach longer)
AIR = {'nb': [(44, 'leap 2 .. land 46')], 'q_air': [(38, 'rise 2 .. land 40'), (38, 'leap 46 .. land2 84')]}
for c in NEW:
    spans = MAN['support'][c]['air']
    want = AIR.get(c, [])
    if c in ('tri', 'hcut', 'blue', 'kcut', 'mx', 'q_grab'):      # (the lunges' two or three ticks off the ground)
        check(all(b - a + 1 <= 6 for a, b in spans), f'air: {c}: only its lunge leaves the ground', str(spans))
        continue
    check(len(spans) == len(want), f'air: {c}: {len(want)} airborne span(s)', str(spans))
    for (a, b), (cap, what) in zip(spans, want):
        check(b - a + 1 <= cap, f'air: {c}: {what} airborne {b - a + 1} t <= {cap}', f'{a}-{b}')
E = api.ev
check(E('nb', 'land') - E('nb', 'leap') == 44 and E('q_air', 'land') - E('q_air', 'rise') == 38 and E('q_air', 'land2') - E('q_air', 'leap') == 38,
      'air: the contract\'s airborne windows are 44 / 38 / 38 t')
sa = MAN['support']['nb']['air'][0] if MAN['support']['nb']['air'] else (0, 0)
check(sa[0] >= E('nb', 'leap') and sa[1] <= E('nb', 'land'), 'air: nb is off the ground only between leap and land', str(sa))
for (a, b), (e0, e1) in zip(MAN['support']['q_air']['air'], (('rise', 'land'), ('leap', 'land2'))):
    check(a >= E('q_air', e0) - 1 and b <= E('q_air', e1), f'air: q_air is off the ground only between {e0} and {e1}', f'{a}-{b}')

# ============================================================== hits (the swing does what the hazard's shape needs)
FWD = [('d4', 'h2'), ('d4', 'h3'), ('d4', 'h4'), ('tri', 'h1'), ('tri', 'h2'), ('tri', 'h3'), ('hcut', 'cut'), ('kcut', 'cut'),
       ('ult', 'cut1'), ('ult', 'cut2')]
for c, e in FWD:
    t = E(c, e)
    b0, b1 = bearing(blade(c, t - 1)[1]), bearing(blade(c, t + 1)[1])
    d, tip, _mid = blade(c, t)
    crosses = (b0 * b1 < 0 and abs(b0 - b1) < 300) or abs(bearing(tip)) <= 35
    out = math.hypot(tip[0], tip[2])
    check(crosses, f'hits: {c} {e}@{t}: the cut crosses her front through the hit tick', f'tip bearing {b0:.0f} -> {bearing(tip):.0f} -> {b1:.0f}')
    check(out >= 1.2 or (c, e) in (('d4', 'h3'),), f'hits: {c} {e}@{t}: the tip is {out:.2f} b out')
    swept = math.degrees(math.acos(max(-1, min(1, sum(x * y for x, y in zip(blade(c, t - 1)[0], blade(c, t + 1)[0]))))))
    check(swept >= 60, f'hits: {c} {e}@{t}: the blade is in full swing ({swept:.0f} deg over hit - 1 .. hit + 1)')
# the vertical cuts come down through the tick
for c, e in (('d4', 'h3'),):
    t = E(c, e)
    check(blade(c, t - 2)[1][1] - blade(c, t + 1)[1][1] >= 1.2 and blade(c, t)[1][2] >= 1.0, f'hits: {c} {e}@{t}: the tip comes down before her',
          f'{blade(c, t - 2)[1]} -> {blade(c, t + 1)[1]}')
t = E('d4', 'h2')
check(blade('d4', t + 1)[1][1] - blade('d4', t - 2)[1][1] >= 1.2, 'hits: d4 h2: the fan rises', f'{blade("d4", t - 2)[1]} -> {blade("d4", t + 1)[1]}')
# the thrusts: the blade along her aim at full reach
for c, e in (('tri', 'h0'), ('blue', 'hit')):
    t = E(c, e)
    d, tip, _mid = blade(c, t)
    check(d[2] >= .93 and tip[2] >= 1.9 and abs(tip[0]) <= .5, f'hits: {c} {e}@{t}: the thrust points along her aim, the tip {tip[2]:.2f} b ahead',
          f'dir {[round(x, 2) for x in d]}')
# the rings and the dome: flat, out at chest height, she is turning
RING = [('d4', 'h1')] + [('rings', f'r{i}') for i in range(1, 6)] + [('mx', 'dome')]
for c, e in RING:
    t = E(c, e)
    d, tip, mid = blade(c, t)
    out = math.hypot(tip[0], tip[2])
    check(abs(elev(d)) <= 30 and out >= 1.2, f'hits: {c} {e}@{t}: the blade is flat and out ({elev(d):.0f} deg, tip {out:.2f} b)')
    check(0.7 <= mid[1] <= 1.7, f'hits: {c} {e}@{t}: at chest height (blade_mid {mid[1]:.2f} b up)')
    turn = abs(((bearing(an(c, 'hand_r', t + 1)) - bearing(an(c, 'hand_r', t - 1)) + 180) % 360) - 180) + \
        abs(((bearing(blade(c, t + 1)[1]) - bearing(blade(c, t - 1)[1]) + 180) % 360) - 180)
    check(turn >= 90, f'hits: {c} {e}@{t}: she is turning through the hit ({turn:.0f} deg of hand + blade bearing over 2 t)')
# the X: two strokes about the tick, the first rising, the second falling
t = E('mx', 'x')
check(blade('mx', t - 1)[1][1] - blade('mx', t - 3)[1][1] >= 1.0 and blade('mx', t + 1)[1][1] - blade('mx', t + 3)[1][1] >= 1.0,
      'hits: mx x: a rising stroke before the tick, a falling one after it',
      f'{[round(blade("mx", k)[1][1], 2) for k in range(t - 3, t + 4)]}')
# the bands and the dive: the blade comes down through the tick
for c, e, drop in (('nb', 'b1', 1.2), ('nb', 'b2', 1.2), ('nb', 'b3', 1.0), ('q_air', 'beam', 1.2), ('q_air', 'pillar', 1.0)):
    t = E(c, e)
    y0, y1 = blade(c, t - 2)[1][1], blade(c, t + 1)[1][1]
    d = blade(c, t + 1)[0]
    check(y0 - y1 >= drop and elev(d) <= -15, f'hits: {c} {e}@{t}: the blade comes down ({y0:.2f} -> {y1:.2f} b, {elev(d):.0f} deg after the tick)')
# the dive: the blade stays point down before her while she comes down with it (the grip drops through the hit tick)
t = E('q_air', 'hit')
g0, g1 = an('q_air', 'hand_l', E('q_air', 'dive'))[1], an('q_air', 'hand_l', E('q_air', 'land'))[1]
check(g0 - g1 >= .8 and elev(blade('q_air', t)[0]) <= -20 and blade('q_air', t)[1][2] >= .6,
      f'hits: q_air hit@{t}: she comes down behind the blade (the grip {g0:.2f} -> {g1:.2f} b, the blade {elev(blade("q_air", t)[0]):.0f} deg)')
b1, b2 = bearing(blade('nb', E('nb', 'b1') + 2)[1]), bearing(blade('nb', E('nb', 'b2') + 2)[1])
check(b1 < -10 and b2 > 10 and abs(bearing(blade('nb', E('nb', 'b3'))[1])) <= 20,
      f'hits: nb: the three cuts end to her left, to her right and straight ahead ({b1:.0f}, {b2:.0f}, {bearing(blade("nb", E("nb", "b3"))[1]):.0f} deg)')
# the dive's wind-up: the blade reversed, point down before her
d, tip, mid = blade('q_air', E('q_air', 'lock2'))
check(elev(d) <= -70 and mid[2] >= .25, f'hits: q_air lock2: the blade held point down before her ({elev(d):.0f} deg)')
# the sky call: the blade straight up from apex2 to the lock
for t in (E('q_air', 'apex2') + 2, E('q_air', 'star'), E('q_air', 'lock3')):
    d, tip, _m = blade('q_air', t)
    check(elev(d) >= 75 and tip[1] >= 3.0, f'hits: q_air t{t}: the blade thrust up at the sky ({elev(d):.0f} deg, tip {tip[1]:.2f} b)')
# the grab: the right hand out before her through the reach and at the grab; the throw: both hands high
for t in (E('q_grab', 'star'), E('q_grab', 'lock'), E('q_grab', 'grab')):
    h, ch = an('q_grab', 'hand_r', t), an('q_grab', 'chest', t)
    check(h[2] - ch[2] >= .3, f'hits: q_grab t{t}: the right hand reaches out before her ({h[2] - ch[2]:.2f} b ahead of her chest)')
h, hd = an('q_air', 'hand_r', E('q_air', 'rise')), an('q_air', 'head', E('q_air', 'rise'))
check(h[1] >= hd[1] - .15 and an('q_air', 'blade_tip', E('q_air', 'rise'))[1] >= 2.6, 'hits: q_air rise 2: both arms thrown upward',
      f'hand_r {h[1]:.2f}, head {hd[1]:.2f}, tip {an("q_air", "blade_tip", 2)[1]:.2f}')
# the iai of U: the blade laid back at her right hip, drawn across, held out at her left, cut back
d, tip, mid = blade('ult', E('ult', 'star1'))
check(bearing(tip) >= 110 and elev(d) <= 0 and an('ult', 'hand_l', E('ult', 'star1'))[0] < 0, 'hits: ult: the iai stance (the blade back at her right hip)',
      f'tip bearing {bearing(tip):.0f}')
for t in (E('ult', 'web') + 2, E('ult', 'star2'), E('ult', 'cut2') - 4):
    d, tip, _m = blade('ult', t)
    check(-140 <= bearing(tip) <= -70 and math.hypot(tip[0], tip[2]) >= 1.6, f'hits: ult t{t}: the blade held out at her left through the web',
          f'bearing {bearing(tip):.0f}, {math.hypot(tip[0], tip[2]):.2f} b')
# kcut: the blade hidden behind her, its tip up over her back
d, tip, mid = blade('kcut', E('kcut', 'glow'))
check(tip[2] < -.2 and tip[1] > an('kcut', 'head', E('kcut', 'glow'))[1], 'hits: kcut: the blade behind her, its tip over her back', str(tip))
check(an('kcut', 'chest', E('kcut', 'glow'))[1] <= .95 and an('hcut', 'chest', E('hcut', 'lock'))[1] <= 1.0, 'hits: kcut / hcut: the low crouches',
      f'chest {an("kcut", "chest", 12)[1]:.2f} / {an("hcut", "chest", 19)[1]:.2f} b up')
# grog_in: the guard smashed open (the blade and the right hand flung apart)
check(dist(an('grog_in', 'hand_l', 2), an('grog_in', 'hand_r', 2)) >= 1.0, 'hits: grog_in 2: the arms flung wide',
      f'{dist(an("grog_in", "hand_l", 2), an("grog_in", "hand_r", 2)):.2f} b apart')

# ============================================================== cues (the blade readable from the F5 camera at the cue ticks)
CUES = [('d4', f'lock{i}', 0) for i in range(1, 5)] + [('tri', f'lock{i}', 0) for i in range(1, 4)] + \
    [('rings', f'lock{i}', 0) for i in range(1, 6)] + [('mx', 'lock2', 0), ('nb', 'lock1', 5), ('nb', 'lock2', 5), ('nb', 'lock3', 5),
                                                         ('q_air', 'lock1', 5), ('q_air', 'lock2', 5),
                                                         # the flash ticks of the unparriable ones (the body carries the tell)
                                                         ('ult', 'yellow', 0), ('ult', 'star1', 0), ('ult', 'star2', 0), ('hcut', 'sparkle', 0),
                                                         ('blue', 'blue', 0), ('kcut', 'sparkle', 0), ('mx', 'star', 0), ('q_air', 'star', 5)]
PLAYER_D = 6.0
for c, e, up in CUES:
    t = E(c, e)
    # tri lock0 (the thrust chamber) and blue's chamber point at the player by design: the hit is a thrust
    d, tip, mid = blade(c, t)
    lens = [0.0, 3.35 - up, PLAYER_D + 3.4]            # the F5 lens in her frame (she `up` b over the floor)
    v = sub(mid, lens)
    n = math.sqrt(sum(x * x for x in v))
    v = [x / n for x in v]
    along = sum(x * y for x, y in zip(d, v))
    seen = 1.44 * math.sqrt(max(0.0, 1 - along * along))
    check(seen >= 0.45, f'cues: {c} {e}@{t}: the blade shows {seen:.2f} b of its length to the F5 lens')
    behind = mid[2] < an(c, 'chest', t)[2] - 0.15 and abs(mid[0]) < 0.3 and abs(mid[1] - an(c, 'chest', t)[1]) < 0.35
    check(not behind, f'cues: {c} {e}@{t}: blade_mid is not hidden behind her body', str([round(x, 2) for x in mid]))

print(f'test_clips_h1c: {NCHK[0] - len(FAILS)}/{NCHK[0]} passed' + (f', {len(FAILS)} FAILED' if FAILS else ''))
sys.exit(1 if FAILS else 0)
