#!/usr/bin/env python3
"""azfair.py: the fairness agent of the sim of record (plan.md 8.4; S1-HARN; scratch tool, never shipped).

Built on azsim.py (real engine functions of 8.1) and ported from the field generator's fgfair.py
(S:mb3/fgfix/sim): the same threat reading, escape search, jump planning and dash timing, so the Guardian numbers
of that sim are reproduced (guardian_m0.txt). Additions of 8.4 (each switches on by itself when the datapack has the
part; until then the Guardian runs through the same code with them idle):

- targets: the NEAREST VULNERABLE HIT PROXY in reach (framework R8: entities `rlk_mb_px` that carry `rlk_mob`;
  columns on the anchor floor, so melee reach is horizontal to the column surface); never the body point when the
  boss has proxies. Bosses without proxies: the Guardian's chaos stars first (fgfair), then the body (3-D reach);
- swing rules: 0.108 b/t while a swing runs (atkcd > 0), no sprint and no jump press while swinging, the dash cancels
  the swing; jumps the low fronts (fieldgen p21f waves and any low-band ring that grows, N10) when not swinging and
  holds new swings for a planned jump;
- the dash out of #hzNoDodge areas: a dash used as movement when walking cannot leave in time (i-frames do not help);
- stops attacking at a transition message (Azhdaha #azTr >= 1 until B3 / the next phase) and keeps >= 10 b away;
- N4 mask hazards (kind 6): reads the `rlk_mb_hzsafe` markers of the hazard and walks / dashes into the nearest;
- steers around moving discs (Hydro orbs, N5) by extrapolating each moving hazard marker's track;
- N12 push: never steps into a push capsule while #mbPushOn 1 (the framework push moves the player for real);
- the brand: no heals, so the DoT runs unless a perfect dodge cleanses it (the dash policy times its i-frames on
  one-shot strikes while branded); the brand DoT (mboss/pl_dot) is recorded apart;
- shards: picks up a `rlk_az_shard` within 6 b when the way and the spot are safe; shields are real (azsim);
- the player: item-less Lv5 (HP 148, def 18, atk 18; level=4 reproduces the earlier Lv4 sims), attack element per
  character (sword 0, Navia 5, bow 1, catalyst 8), no crits (as every earlier sim);
- policies: stand, melee (walk), ranged (walk), melee_head, melee_tail, melee_flank, ranged_flank (orbit 10-14 b);
  dodge none / walk / dash.

The Azhdaha and AZ-CM names the agent reads are in CONTRACT below: the AZ-CM ones from S:az/contract/cm.md (proxies,
mask groups, push capsules, cine, pl_dot), the module ones from plan.md 1.7 / 4.3 / 4.10 / 4.12 until s2.md and
manifest.md exist (check them whenever those change).
"""
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import azsim as Z  # noqa: E402
from mcsim import Ctx  # noqa: E402

C0 = Z.C0

# ------------------------------------------------------------------------------------------- names (contracts)
CONTRACT = dict(
    az_id='azhdaha', az_n=10,
    pat='#azPat', ph='#azPh', tr='#azTr', bur='#azBur', leg='#azLeg', tail='#azTail',
    brand_t='azBrT', brand_el='azBrE',             # player scores: brand ticks left / element (brand.py)
    shard_tag='rlk_az_shard',
    anchor_tag='rlk_mb_az_anchor',                 # if absent the body husk is the anchor
    px_tag='rlk_mb_px', px_name='rlk_mb_px_', vuln_tag='rlk_mob',
    safe_tag='rlk_mb_hzsafe', safe_grp='mbHzSG', mask_kind=6,    # cm.md 13.6
    push_on='#mbPushOn', push_path='push',          # cm.md 3.2 / 13.5: push[] = [{f0,f1,hw,px,top}] tenths, anchor frame
    cine='#mbCine',
    test_pair=90, test_p2=60, test_p3=62,           # mboss/test/pattern ids (plan.md 1.7)
)
FLANK_PX = ('chest', 'belly', 'hips', 'paw_l', 'paw_r', 'foot_l', 'foot_r')
HEAD_PX = ('head',)
TAIL_PX = ('tail1', 'tail2', 'tail3', 'tail4')
# 4.12 zone thresholds at the R1 rest; load_zone() re-derives them from the rig manifest's rest anchors (manifest.md 4.1)
ZONE = dict(head_f=3.6, flank_s0=3.0, flank_s1=9.0, tail_f=-4.8, tail_s=3.5, src='plan.md 4.12 (R1 rest)')


def load_zone(dp):
    """The 4.12 zone thresholds from the manifest (real, else the module's stub; manifest.md 1 / 4.1): HEAD f >=
    head_col.f - 0.7, FLANK |s| >= torso_hw, TAIL f < tail_root.f - 0.05 (the R1 numbers 4.3 / 3.0 / -4.75 give the
    plan's 3.6 / 3.0 / -4.8). api.py computes the module's own values; align these with it when s2.md lands."""
    import json
    from pathlib import Path
    for rel in ('tools/mboss_azhdaha_rig_manifest.json', 'tools/mboss_azhdaha/stub_rig_manifest.json'):
        p = Path(dp) / rel
        if not p.exists():
            continue
        try:
            m = json.loads(p.read_text(encoding='utf-8'))
        except ValueError:
            continue
        ra, z = m.get('rest_anchors', {}), dict(ZONE)
        if ra.get('head_col'):
            z['head_f'] = round(ra['head_col'][2] - 0.7, 3)
        if ra.get('tail_root'):
            z['tail_f'] = round(ra['tail_root'][2] - 0.05, 3)
        if m.get('torso_hw'):
            z['flank_s0'] = float(m['torso_hw'])
        z['src'] = rel
        return z
    return dict(ZONE)
MODULES = {1: ('guardian', '#gdPat'), 2: ('butterfly', '#bfPat'), 3: ('fieldgen', '#fgPat'), 99: ('proto', '#ptPat')}

WALK, SPRINT = 0.2159, 0.2807
SWING = WALK / 2                 # 0.108 b/t (plan.md 8.4): half the walk speed, as fgfair (0.10795)
DASH_IF = int(os.environ.get('DASH_IF', '6'))
STARS = os.environ.get('STARS', '1') == '1'   # Guardian: the agent attacks her chaos stars while they exist
LANES = os.environ.get('LANES', '1') == '1'   # field generator slab lanes read as the coming blade
# FIX FAIR-5 (AZ fix round): an N10 front's speed is read from the slam (a human knows how fast the P2 / P5 / P5b /
# Cryo ring / T1 fronts travel before they move): the module's g.wave writes the first-tick advance x 1000 on the front
# marker (objective mb); the agent plans its jump (or dash) from the strike instead of learning the growth from the
# first observed radius change. FRONTS=0 restores the I2 behaviour.
FRONTS = os.environ.get('FRONTS', '1') == '1'

# character models: swing intervals (atkCD per hit at 100 % attack speed), reach, coefficients, attack element
CHARS = {
    'sword':    dict(iv=[6, 10], reach=3.5, coef=[100, 120], ranged=False, el=0),          # Lumine, physical
    'navia':    dict(iv=[11, 11, 15, 22], reach=4.5, coef=[100, 100, 130, 160], ranged=False, el=5),   # Geo
    'nefer':    dict(iv=[5, 5, 5, 10], reach=3.5, coef=[61, 60, 80, 98], ranged=False, el=7),
    'bow':      dict(iv=[8], reach=30.0, coef=[100], ranged=True, el=1),                     # Yoimiya, Pyro
    'catalyst': dict(iv=[10, 10, 10, 16], reach=30.0, coef=[72, 66, 90, 120], ranged=True, el=8),   # Ronova, Void
}


def char_model(name):
    """CHARS[name]; a trailing '0' (bow0, navia0, catalyst0) is the same character attacking physical, as every
    sim before this one did (the Guardian reproduction uses it: her element record K5 reacts to Pyro hits)."""
    if name in CHARS:
        return CHARS[name]
    if name.endswith('0') and name[:-1] in CHARS:
        return dict(CHARS[name[:-1]], el=0)
    raise KeyError(name)


def arc(g=0.08, v0=0.42):
    """Feet height on the ticks after a jump press: y += v; v = (v - g) x 0.98 (vanilla)."""
    y, v, out = 0.0, v0, []
    while True:
        y += v
        v = (v - g) * 0.98
        if y <= 0:
            break
        out.append(y)
    return out


ARC_V, ARC_L = arc(), arc(0.04, 0.42 * 1.19)


# ------------------------------------------------------------------------------------------- module state
class Mod:
    """What the agent reads from the running module (pattern, phase, transition, B3, brand)."""

    def __init__(self, s):
        self.s = s

    def mid(self):
        return self.s.sc('#mbId', 'mb') or 0

    def is_az(self):
        return self.mid() == CONTRACT['az_n']

    def name(self):
        if self.is_az():
            return CONTRACT['az_id']
        return MODULES.get(self.mid(), ('boss%d' % self.mid(), None))[0]

    def pat(self):
        s = self.s
        if self.is_az():
            return s.sc(CONTRACT['pat'], 'mb') or 0
        m = MODULES.get(self.mid())
        if m and m[1]:
            return s.sc(m[1], 'mb') or 0
        return s.sc('#fgPat', 'mb') or s.sc('#gdPat', 'mb') or s.sc('#bfPat', 'mb') or 0

    def phase(self):
        s = self.s
        if (s.sc('#mbSt', 'mb') or 0) != 1:
            return 'x'
        if not self.is_az():
            return {1: 'gd', 2: 'bf', 3: 'fg'}.get(self.mid(), 'm%d' % self.mid())
        if (s.sc(CONTRACT['bur'], 'mb') or 0) >= 1:
            return 'b3'
        ph = s.sc(CONTRACT['ph'], 'mb') or 1
        if (s.sc(CONTRACT['tr'], 'mb') or 0) >= 1:
            return 'tr%d' % ph
        return 'p%d' % ph

    def transition(self):
        """Stop attacking: from the transition message (#azTr >= 1) until B3 starts or the next phase; cine too."""
        s = self.s
        if (s.sc(CONTRACT['cine'], 'mb') or 0) == 1:
            return True
        if not self.is_az():
            return False
        return (s.sc(CONTRACT['tr'], 'mb') or 0) >= 1 and (s.sc(CONTRACT['bur'], 'mb') or 0) < 1

    def branded(self, pl):
        return (self.s.sc(('e', pl.id), CONTRACT['brand_t']) or 0) >= 1


# ------------------------------------------------------------------------------------------- threats
def hz_inside(s, e, x, y, z, pad=0.0, cx=None, cz=None):
    """The framework hz/hit test (the 0.3 body pad is in the stored bounds) with an extra pad (blocks); (cx, cz)
    replaces the marker position (moving hazards)."""
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    ex = e.pos[0] if cx is None else cx
    ez = e.pos[2] if cz is None else cz
    dy = (y - e.pos[1]) * 1000
    if dy < g('mbHzY0') or dy > g('mbHzY1'):
        return False
    K = g('mbHzK')
    dx, dz = (x - ex) * 1000, (z - ez) * 1000
    padm = pad * 1000
    if K == CONTRACT['mask_kind']:
        return not in_safe(s, e, x, z, pad)
    if K == 5:
        r2 = dx * dx + dz * dz
        ri = g('mbHzRI')
        return ri <= 0 or r2 > max(0, math.sqrt(ri) - padm) ** 2
    FX, FZ = g('mbHzFX'), g('mbHzFZ')
    fwd = (dx * FX + dz * FZ) / 1000
    if K == 4:
        if fwd < g('mbHzLo') - padm or fwd > g('mbHzHi') + padm:
            return False
        side = abs((dx * FZ - dz * FX) / 1000)
        return side <= g('mbHzHW') + padm
    r2 = dx * dx + dz * dz
    if r2 > (math.sqrt(g('mbHzRR')) + padm) ** 2:
        return False
    ri = g('mbHzRI')
    if ri > 0 and r2 < max(0, math.sqrt(ri) - padm) ** 2:
        return False
    if K in (1, 2):
        return True
    ang = g('mbHzAng')
    if ang >= 180 or (dx == 0 and dz == 0):
        return True
    cosang = fwd / math.sqrt(r2)
    return math.degrees(math.acos(max(-1, min(1, cosang)))) <= ang + (math.degrees(pad / max(0.5, math.sqrt(r2) / 1000)) if pad else 0)


def safe_markers(s, e):
    """cm.md 13.6: the safe markers of mask hazard e are the `rlk_mb_hzsafe` markers whose `mbHzSG` equals the
    hazard's group (its `mbHzSG`, or its own id `mbHzI` when that is 0); the radius R0 is the hazard's (`mbHzR0`, mb)."""
    g = s.sc(('e', e.id), CONTRACT['safe_grp']) or 0
    grp = g if g >= 1 else s.sc(('e', e.id), 'mbHzI')
    r0 = (s.sc(('e', e.id), 'mbHzR0') or 0) / 1000
    return [(m.pos[0], m.pos[2], r0) for m in s.ents
            if m.alive and CONTRACT['safe_tag'] in m.tags and s.sc(('e', m.id), CONTRACT['safe_grp']) == grp]


def in_safe(s, e, x, z, pad=0.0):
    """N4: safe when the feet are within R0 + 0.3 of any safe marker of the hazard (pad shrinks the circle)."""
    return any(math.hypot(x - mx, z - mz) <= r0 + 0.3 - pad for mx, mz, r0 in safe_markers(s, e))


class Threat:
    def __init__(self, kind, fn, k1, k2, seen, src=None, y1=None, dmg=0, nododge=False, oneshot=False, tell=0):
        self.kind, self.fn, self.k1, self.k2, self.seen, self.src = kind, fn, k1, k2, seen, src
        self.y1, self.dmg, self.nododge, self.oneshot, self.tell = y1, dmg, nododge, oneshot, tell


def wave_ticks(s, e, x, z, virtual=False):
    """Ticks k (1 = the coming tick) on which the field generator's wave front e covers a player standing at (x, z)
    (field.py waves/grow: r = 2.5 + floor(11 j / 2) / 10 at its j-th active tick, inner r - 2.5; +0.3 body pad)."""
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    if g('mbHzHit') and not virtual:
        return []
    W, T, Aa = g('mbHzW'), g('mbHzT'), g('mbHzA')
    d = math.hypot(x - e.pos[0], z - e.pos[2])
    out = []
    for j in range(0, Aa):
        k = j + W - T
        if k < (1 - 12 if virtual else 1):
            continue
        rt = 25 + (11 * j) // 2 if j > 0 else 25
        r = rt / 10
        inner = max(0.0, r - 2.5 - 0.3) if j > 0 else 0.0
        if inner <= d <= r + 0.3:
            out.append(k)
    return out


def front_ticks(s, e, x, z, growth):
    """A generic expanding front (N10: hz/ring + hz/resize_s each tick): the ticks k at which the ring, growing by
    `growth` b/t from its current bounds, covers the point (body pad included in the stored bounds)."""
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    if g('mbHzHit') and g('mbHzRA') <= 0:
        return []
    W, T, Aa = g('mbHzW'), g('mbHzT'), g('mbHzA')
    d = math.hypot(x - e.pos[0], z - e.pos[2])
    ro = math.sqrt(g('mbHzRR')) / 1000
    ri = math.sqrt(g('mbHzRI')) / 1000 if g('mbHzRI') > 0 else 0.0
    out = []
    k1 = max(1, W - T)
    for k in range(k1, min(W + Aa - 1 - T, 60) + 1):
        grow = growth * max(0, k - max(0, W - T))
        if ri + grow - 0.0 <= d <= ro + grow:
            out.append(k)
    return out


def c3_band(s, b):
    """The field generator's C3 beam band around the body (spec 2.1: r < 2.7 or r > 6.1 are safe)."""
    cy = s.arena['cy']
    return lambda x, y, z, pad: (y - cy) <= 2.0 and (2.7 - pad) <= math.hypot(x - b.pos[0], z - b.pos[2]) <= (6.1 + pad)


def pj_test(s, e, x, y, z, pad):
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    v = max(1, (g('mbPjV') * 4 + 9) // 10) * 0.25
    yaw, pit = math.radians(e.rot[0]), math.radians(e.rot[1])
    d = (-math.sin(yaw) * math.cos(pit), -math.sin(pit), math.cos(yaw) * math.cos(pit))
    hr = g('mbPjR') / 10
    for k in range(0, 13):
        p = (e.pos[0] + d[0] * v * k / 4, e.pos[1] + d[1] * v * k / 4, e.pos[2] + d[2] * v * k / 4)
        if g('mbPjK') == 1:
            if abs(p[1] - 0.9 - y) < 1.5 and math.hypot(x - p[0], z - p[2]) <= hr + 0.65 + pad:
                return True
        elif math.dist((x, y, z), (p[0], p[1] - 0.9, p[2])) <= hr + 0.3 + pad:
            return True
    return False


def threats(s, ag, now, react):
    out = []
    b = Z.body_of(s)
    cy = s.arena['cy']
    for e in s.ents:
        if not e.alive:
            continue
        if 'rlk_mb_hz' in e.tags:
            g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
            rec = s.hzrec.get(e.id)
            seen = rec['t'] if rec else now
            if now - seen < react:
                continue
            W, T, Aa, D = g('mbHzW'), g('mbHzT'), g('mbHzA'), g('mbHzD')
            K = g('mbHzK')
            if D <= 0:
                # the field generator's C6 / F2 slab throw line (dmg 0): the blade flies down it from the strike
                if rec and rec['pat'] in (6, 12) and K == 4 and LANES and ag.mod.mid() == 3:
                    k1 = max(1, W - T)
                    if W - T + 14 >= 1:
                        ee = e
                        out.append(Threat('lane', lambda x, y, z, pad, ee=ee: hz_inside(s, ee, x, cy, z, pad), k1,
                                          W - T + 14, seen, ee, None, 110))
                continue
            if 'rlk_mb_fg_p21f' in e.tags:
                ks = wave_ticks(s, e, ag.player.pos[0], ag.player.pos[2])
                if ks:
                    out.append(Threat('wave', None, min(ks), max(ks), seen, e, 0.7, D, True))
                # a player who knows the triple (HP < 50 %: #fq21T 1, read at the 3rd charge start) plans for the two
                # extra fronts (+6 / +12 t) before their own decals appear (10 t before their centre strike)
                if ag.tri_aware and rec and rec.get('clock') in (135, 136) and (s.sc('#fq21T', 'mb') or 0) == 1:
                    for m in (1, 2):
                        ksx = [k + 6 * m for k in wave_ticks(s, e, ag.player.pos[0], ag.player.pos[2], True)]
                        if ksx:
                            out.append(Threat('wave', None, min(ksx), max(ksx), seen, e, 0.7, D, True))
                continue
            if rec and rec['pat'] == 3 and K == 4 and g('mbHzRA') > 0 and b is not None and ag.mod.mid() == 3:
                k1 = max(1, W - T)
                k2 = W + Aa - 1 - T
                if k2 >= 1:
                    out.append(Threat('c3', c3_band(s, b), k1, k2, seen, e, 2.0, D))
                continue
            if g('mbHzHit') and g('mbHzRA') <= 0:
                continue
            k1, k2 = W - T, W + Aa - 1 - T
            if k2 < 1:
                continue
            ee = e
            y1 = g('mbHzY1') / 1000
            nd = g('mbHzND') == 1
            oneshot = g('mbHzRA') <= 0 and W >= 12 and not nd
            grow = ag.growth.get(e.id, 0.0)
            if FRONTS and K == 2 and grow <= 0.05 and g('mbHzRA') <= 0:
                grow = (s.sc(('e', e.id), 'mb') or 0) / 1000.0
            if K == 2 and grow > 0.05:
                # a generic expanding front (N10): low band -> a jump window like the fieldgen waves
                ks = front_ticks(s, e, ag.player.pos[0], ag.player.pos[2], grow)
                if ks and y1 <= 1.2:
                    out.append(Threat('wave', None, min(ks), max(ks), seen, e, y1, D, nd))
                elif ks:
                    out.append(Threat('front', lambda x, y, z, pad, ee=ee, gr=grow, kk=min(ks): front_at(s, ee, x, z, pad, gr, kk),
                                      min(ks), max(ks), seen, ee, y1, D, nd))
                continue
            vel = ag.vel.get(e.id)
            if vel is not None and K in (1, 2, 3, 5) and (abs(vel[0]) + abs(vel[1])) > 0.02:
                # a moving disc (orbit mover N5, Hydro orbs): the extrapolated track over the next 8 ticks
                fn = (lambda x, y, z, pad, ee=ee, v=vel: any(
                    hz_inside(s, ee, x, y, z, pad, ee.pos[0] + v[0] * k, ee.pos[2] + v[1] * k) for k in range(0, 9, 2)))
                out.append(Threat('mover', fn, max(1, k1), k2, seen, ee, y1, D, nd))
                continue
            kind = 'mask' if K == CONTRACT['mask_kind'] else 'hz'
            out.append(Threat(kind, lambda x, y, z, pad, ee=ee: hz_inside(s, ee, x, y, z, pad), max(1, k1), k2, seen, ee,
                              y1, D, nd, oneshot, W))
        elif 'rlk_mb_pj' in e.tags:
            g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
            if g('mbPjHit') or g('mbPjD') <= 0:
                continue
            ee = e
            out.append(Threat('pj', lambda x, y, z, pad, ee=ee: pj_test(s, ee, x, y, z, pad), 1, 3, now, ee, None,
                              g('mbPjD'), (s.sc(('e', e.id), 'mbPjND') or 0) == 1, True, 12))
    return out


def front_at(s, e, x, z, pad, grow, k):
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    d = math.hypot(x - e.pos[0], z - e.pos[2])
    ro = math.sqrt(g('mbHzRR')) / 1000 + grow * k
    ri = (math.sqrt(g('mbHzRI')) / 1000 if g('mbHzRI') > 0 else 0.0) + grow * k
    return ri - pad <= d <= ro + pad


def jump_press(arc_h, windows, earliest=0):
    """windows: [(k1, k2, y1)] (k from the coming tick = 1). A press in the agent step of tick now+p (p >= earliest)
    puts the feet at arc_h[k - 2 - p] on tick k. Returns the list of p that clear every window."""
    ok = []
    kmin = min(w[0] for w in windows)
    for p in range(earliest, max(earliest, kmin - 1)):
        good = True
        for k1, k2, y1 in windows:
            for k in range(k1, k2 + 1):
                i = k - 2 - p
                if i < 0 or i >= len(arc_h) or arc_h[i] <= y1:
                    good = False
                    break
            if not good:
                break
        if good:
            ok.append(p)
    return ok


# ------------------------------------------------------------------------------------------- the agent
class Agent:
    """policy: stand | melee | ranged | melee_head | melee_tail | melee_flank | ranged_flank; dodge: none | walk
    (walk, jump) | dash (walk, jump, dash); react: ticks from a telegraph's first tick to the reaction; char: CHARS."""

    def __init__(self, s, player, policy='melee', dodge='walk', react=5, char='sword', sprint=False, iframes=DASH_IF,
                 jump_waves=True, hit_boss=True, tri_aware=True, level=5, nd_dash=True, shards=True):
        self.s, self.player, self.policy, self.dodge, self.react = s, player, policy, dodge, react
        self.mod = Mod(s)
        self.ch = char_model(char)
        self.char = char
        self.sprint, self.iframes = sprint, iframes
        self.jump_waves, self.hit_boss, self.tri_aware = jump_waves, hit_boss, tri_aware
        self.nd_dash, self.shards = nd_dash and dodge != 'none', shards
        self.atk = 10 + 2 * (level - 1)
        s.agent = self
        s.pat_fn = self.mod.pat
        s.ph_fn = self.mod.phase
        self.cx, self.cy, self.cz = s.arena['cx'], s.arena['cy'], s.arena['cz']
        self.walk_r = s.arena.get('walk', 21) - 0.3
        self.charges, self.regen, self.cool = 2, 0, 0
        self.dash_left, self.dash_dir = 0, (0, 0)
        self.atkcd, self.combo = 0, 0
        self.jump_t, self.jump_arc = -1, ARC_V
        self.planned_dash = None
        self.planned_jump = None
        self.orbit_dir = 1
        self.zc = None                # zone thresholds (load_zone, on the first proxied zone test)
        self.hzpos = {}               # hazard id -> last (t, x, z)
        self.vel = {}                 # hazard id -> (vx, vz) b/t
        self.growth = {}              # hazard id -> outer-radius growth b/t (rings)
        self.hzrr = {}
        self.stats = dict(ticks=0, hittable=0, attack=0, swings=0, hits=0, dodge_ticks=0, dashes=0, jumps=0,
                          inreach=0, nd_dash=0, brand_dash=0, shard_walks=0, hold_ticks=0, deaths=[], unavoid=[],
                          walk_fail=[], nowalk=[], wave_jumps=[], wave_nojump=[],
                          ph_ticks={}, ph_reach={}, ph_up={}, ph_hits={}, ph_dealt={}, tgt_hits={}, zone_ticks={},
                          pat_ticks={}, pat_up={})
        self.nowalk_seen = set()

    # -- bookkeeping
    def check_death(self):
        s, pl = self.s, self.player
        if (s.sc(('e', pl.id), 'curHealth') or 0) <= 0:
            self.stats['deaths'].append(s.t)
            s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))

    def pos(self):
        return self.player.pos[0], self.player.pos[2]

    def clampw(self, x, z):
        dx, dz = x - self.cx, z - self.cz
        r = math.hypot(dx, dz)
        if r > self.walk_r:
            x, z = self.cx + dx * self.walk_r / r, self.cz + dz * self.walk_r / r
        return x, z

    def bump(self, key, ph, v=1):
        d = self.stats[key]
        d[ph] = d.get(ph, 0) + v

    def track_hazards(self):
        """Per-hazard motion (moving discs) and ring growth (fronts), sampled every agent step."""
        s = self.s
        alive = set()
        for e in s.ents:
            if not e.alive or 'rlk_mb_hz' not in e.tags:
                continue
            alive.add(e.id)
            p = self.hzpos.get(e.id)
            if p is not None and s.t > p[0]:
                dt = s.t - p[0]
                self.vel[e.id] = ((e.pos[0] - p[1]) / dt, (e.pos[2] - p[2]) / dt)
            self.hzpos[e.id] = (s.t, e.pos[0], e.pos[2])
            rr = s.sc(('e', e.id), 'mbHzRR') or 0
            r0 = self.hzrr.get(e.id)
            if r0 is not None and rr > r0[1] and s.t > r0[0]:
                self.growth[e.id] = (math.sqrt(rr) - math.sqrt(r0[1])) / 1000 / (s.t - r0[0])
            self.hzrr[e.id] = (s.t, rr)
        for d in (self.hzpos, self.vel, self.growth, self.hzrr):
            for k in [k for k in d if k not in alive]:
                del d[k]

    # -- the boss frame, targets and zones
    def anchor(self):
        s = self.s
        a = [e for e in s.ents if e.alive and CONTRACT['anchor_tag'] in e.tags]
        return a[0] if a else Z.body_of(s)

    def frame(self, x, z):
        """(f, s) of a point in the anchor frame: f toward the head (the anchor's facing), s to its left."""
        a = self.anchor()
        if a is None:
            return 0.0, 0.0
        yaw = math.radians(a.rot[0])
        fx, fz = -math.sin(yaw), math.cos(yaw)
        lx, lz = math.cos(yaw), math.sin(yaw)
        dx, dz = x - a.pos[0], z - a.pos[2]
        return dx * fx + dz * fz, dx * lx + dz * lz

    def world_pt(self, f, sd):
        a = self.anchor()
        yaw = math.radians(a.rot[0])
        return (a.pos[0] - math.sin(yaw) * f + math.cos(yaw) * sd, a.pos[2] + math.cos(yaw) * f + math.sin(yaw) * sd)

    def proxies(self):
        s = self.s
        out = []
        for e in s.ents:
            if e.alive and CONTRACT['px_tag'] in e.tags:
                name = next((t[len(CONTRACT['px_name']):] for t in e.tags
                             if t.startswith(CONTRACT['px_name']) and t != CONTRACT['px_tag']), '?')
                out.append((e, name, CONTRACT['vuln_tag'] in e.tags, e.data.get('width', 1.8) / 2))
        return out

    def zone(self, x, z):
        """plan.md 4.12 zones for a proxy boss; angular sectors (head +-45 deg, tail +-45 deg, flank) otherwise."""
        f, sd = self.frame(x, z)
        if self.proxies():
            if self.zc is None:
                self.zc = load_zone(self.s.dp)
            Zc = self.zc
            if f >= Zc['head_f'] and abs(sd) <= 4 + 0.6 * (f - Zc['head_f']):
                return 'head'
            if f < Zc['tail_f']:
                return 'tail' if abs(sd) <= Zc['tail_s'] else 'tail_off'
            if Zc['flank_s0'] <= abs(sd) <= Zc['flank_s1']:
                return 'flank'
            return 'flank_far' if abs(sd) > Zc['flank_s1'] else 'under'
        ang = abs(math.degrees(math.atan2(sd, f)))
        return 'head' if ang <= 45 else ('tail' if ang >= 135 else 'flank')

    def targets(self):
        """[(entity, name, kind, half_width)] the agent may hit now: vulnerable proxies (proxy boss), else the
        Guardian's stars (fgfair) and the body."""
        s = self.s
        px = self.proxies()
        if px:
            return [(e, n, 'px', hw) for e, n, v, hw in px if v]
        out = []
        if STARS:
            out += [(e, 'star', 'star', 0.0) for e in s.ents if e.alive and 'rlk_mb_gd_star' in e.tags]
        b = Z.body_of(s)
        if b is not None:
            out.append((b, 'body', 'body', 0.0))
        return out

    def tdist(self, t, x, z, y=None):
        """Distance used for reach: proxy columns horizontally to the surface, stars and the body in 3-D (fgfair)."""
        e, n, kind, hw = t
        if kind == 'px':
            return max(0.0, math.hypot(e.pos[0] - x, e.pos[2] - z) - hw)
        return math.dist((e.pos[0], e.pos[1], e.pos[2]), (x, self.player.pos[1] if y is None else y, z))

    def hittable(self):
        s = self.s
        b = Z.body_of(s)
        if b is None or (s.sc('#mbSt', 'mb') or 0) != 1:
            return False, b
        if 'rlk_mb_inv' in b.tags or 'rlk_mb_dying' in b.tags:
            return False, b
        return True, b

    # -- push capsules (N12)
    def capsules(self):
        """The active push capsules (cm.md 13.5) as (f0, f1, hw) in blocks: storage push[] (tenths) while #mbPushOn 1
        (the module's per-tick request, read between ticks); an entry with `px` only while that proxy's top <= top."""
        s = self.s
        if (s.sc(CONTRACT['push_on'], 'mb') or 0) != 1:
            return []
        caps = s.storage.get('rlk:mboss', {}).get(CONTRACT['push_path'], []) or []
        out = []
        for c in caps if isinstance(caps, list) else []:
            if c.get('px'):
                tag = CONTRACT['px_name'] + str(c['px'])
                pe = [e for e in s.ents if e.alive and tag in e.tags]
                if pe and pe[0].data.get('height', 0.0) > float(c.get('top', 0)) / 10:
                    continue
            out.append((float(c.get('f0', 0)) / 10, float(c.get('f1', 0)) / 10, float(c.get('hw', 0)) / 10))
        return out

    def in_capsule(self, x, z, caps, pad=0.2):
        if not caps:
            return False
        f, sd = self.frame(x, z)
        return any(f0 - pad <= f <= f1 + pad and abs(sd) < hw + pad for f0, f1, hw in caps)

    # -- moves
    def safe_at(self, ths, x, z, y=0.0, pad=0.25):
        return not any(t.fn(x, self.cy + y, z, pad) for t in ths if t.fn)

    def escape_point(self, ths, maxd=14.0):
        x0, z0 = self.pos()
        best = None
        caps = self.capsules()
        masks = [t for t in ths if t.kind == 'mask']
        if masks:
            # N4: the escape is a safe circle of the mask hazard (any distance), else the general search
            for t in masks:
                for mx, mz, r0 in safe_markers(self.s, t.src):
                    d = math.hypot(mx - x0, mz - z0)
                    dd = max(0.0, d - max(0.0, r0 - 0.4))
                    k = dd / d if d > 1e-6 else 0
                    x, z = self.clampw(x0 + (mx - x0) * k, z0 + (mz - z0) * k)
                    if self.safe_at(ths, x, z) and (best is None or dd < best[0]):
                        best = (dd, x, z)
            if best:
                return best
            maxd = 30.0
        for i in range(48):
            a = 2 * math.pi * i / 48
            for k in range(1, int(maxd / 0.25) + 1):
                d = k * 0.25
                x, z = self.clampw(x0 + d * math.cos(a), z0 + d * math.sin(a))
                if self.safe_at(ths, x, z) and not self.in_capsule(x, z, caps):
                    if best is None or d < best[0]:
                        best = (d, x, z)
                    break
        return best

    def cur_arc(self):
        a = self.s.attr_value(self.player, 'gravity')
        return ARC_L if a < 0.06 else ARC_V

    def press_jump(self):
        if self.jump_t >= 0 or self.atkcd > 0:
            return False
        self.jump_t = 0
        self.jump_arc = self.cur_arc()
        self.stats['jumps'] += 1
        return True

    def walk_to(self, x, z, v):
        pl = self.player
        x0, z0 = self.pos()
        d = math.hypot(x - x0, z - z0)
        if d < 1e-6:
            return
        st = min(v, d)
        nx, nz = self.clampw(x0 + (x - x0) / d * st, z0 + (z - z0) / d * st)
        pl.pos[0], pl.pos[2] = nx, nz

    def do_dash(self, direction):
        if self.charges <= 0 or self.cool > 0:
            return False
        s = self.s
        self.charges -= 1
        self.cool = 5
        self.atkcd = 0                  # the dash cancels the swing
        self.dash_dir = direction
        s.iframe_end = s.t + 1 + self.iframes - 1
        self.stats['dashes'] += 1
        x, z = self.clampw(self.player.pos[0] + direction[0], self.player.pos[2] + direction[1])
        self.player.pos[0], self.player.pos[2] = x, z
        self.dash_left = 2
        return True

    def speed(self):
        return SWING if self.atkcd > 0 else (SPRINT if self.sprint else WALK)

    def step_toward(self, gx, gz, soon, stop=0.0):
        """One move toward (gx, gz) at sprint (swing speed while swinging), refused into a threat or a capsule."""
        pl = self.player
        x0, z0 = self.pos()
        d = math.hypot(gx - x0, gz - z0)
        if d <= stop + 1e-6:
            return False
        v = SPRINT if self.atkcd == 0 else SWING
        st = min(v, d - stop)
        caps = self.capsules()
        ux, uz = (gx - x0) / d, (gz - z0) / d
        # straight, else around a push capsule (the body): the first of +-30 / 60 / 90 degrees that is free
        for a in ((0,) if not caps else (0, 30, -30, 60, -60, 90, -90)):
            c, sn = math.cos(math.radians(a)), math.sin(math.radians(a))
            nx, nz = self.clampw(x0 + (ux * c - uz * sn) * st, z0 + (ux * sn + uz * c) * st)
            if self.safe_at(soon, nx, nz, pad=0.3) and not self.in_capsule(nx, nz, caps):
                pl.pos[0], pl.pos[2] = nx, nz
                return True
        return False

    def goal_point(self, prefer, zone_ok, want, soon):
        """The nearest floor point within `want` of the surface of a preferred vulnerable proxy that lies in the
        wanted zone, is safe and outside the push capsules (positional policies)."""
        x0, z0 = self.pos()
        caps = self.capsules()
        best = None
        for t in self.targets():
            e, n, kind, hw = t
            if prefer and kind == 'px' and n not in prefer:
                continue
            for ri in (want * 0.6, want):
                r = hw + ri
                for i in range(24):
                    a = 2 * math.pi * i / 24
                    x, z = self.clampw(e.pos[0] + r * math.cos(a), e.pos[2] + r * math.sin(a))
                    if not zone_ok(self.zone(x, z)):
                        continue
                    if self.in_capsule(x, z, caps) or not self.safe_at(soon, x, z, pad=0.3):
                        continue
                    d = math.hypot(x - x0, z - z0)
                    if best is None or d < best[0]:
                        best = (d, x, z)
        return best

    # -- one tick of the agent, BEFORE the world tick
    def step(self):
        s, pl = self.s, self.player
        now = s.t + 1
        st = self.stats
        if self.cool > 0:
            self.cool -= 1
        if self.charges < 2:
            self.regen += 1
            if self.regen >= 20:
                self.charges += 1
                self.regen = 0
        if self.atkcd > 0:
            self.atkcd -= 1
        if s.kb:
            dx, dz, k = s.kb
            x, z = self.clampw(pl.pos[0] + dx * 0.1 * k, pl.pos[2] + dz * 0.1 * k)
            pl.pos[0], pl.pos[2] = x, z
            s.kb = (dx, dz, k - 1) if k > 1 else None
        if self.dash_left > 0:
            x, z = self.clampw(pl.pos[0] + self.dash_dir[0], pl.pos[2] + self.dash_dir[1])
            pl.pos[0], pl.pos[2] = x, z
            self.dash_left -= 1
        y = 0.0
        if self.jump_t >= 0:
            self.jump_t += 1
            if self.jump_t <= len(self.jump_arc):
                y = self.jump_arc[self.jump_t - 1]
            else:
                self.jump_t = -1
        pl.pos[1] = self.cy + y
        self.track_hazards()
        ok, b = self.hittable()
        ph = self.mod.phase()
        pk = str(self.mod.pat())
        st['ticks'] += 1
        self.bump('ph_ticks', ph)
        self.bump('pat_ticks', pk)
        if ok:
            st['hittable'] += 1
        hold = self.mod.transition()
        if hold:
            st['hold_ticks'] += 1
        ths = [] if self.dodge == 'none' else threats(s, self, now, self.react)
        waves = [t for t in ths if t.kind == 'wave']
        ths = [t for t in ths if t.kind != 'wave']
        x0, z0 = self.pos()
        cur = [t for t in ths if t.fn(x0, self.cy + y, z0, 0.15) and t.k1 <= 40]
        moved = False
        # FIX FAIR-5: the dash policy dashes through a dodgeable ground front on its tick when a charge is ready (the
        # i-frames cover the front's pass), before trying a jump
        if waves and self.dodge == 'dash' and self.charges > 0 and self.cool == 0 and self.dash_left == 0 and self.jump_t < 0:
            dw = [t for t in waves if not t.nododge and t.k1 <= 40]
            if dw and min(t.k1 for t in dw) <= 1 and max(t.k2 for t in dw) <= self.iframes:
                src = min(dw, key=lambda t: t.k1).src
                dx, dz = x0 - src.pos[0], z0 - src.pos[2]
                dd = math.hypot(dx, dz) or 1.0
                if self.do_dash((dx / dd, dz / dd)):
                    st['front_dash'] = st.get('front_dash', 0) + 1
                    self.planned_jump = None
                    waves = [t for t in waves if t.nododge]
        # waves: a jump is the only answer (no dash, no escape); plan the press, hold the swing for it
        if waves and self.jump_waves and self.jump_t < 0:
            wins = [(t.k1, t.k2, t.y1) for t in waves if t.k1 <= 40]
            if wins:
                arc_h = self.cur_arc()
                ps = jump_press(arc_h, wins)
                if ps:
                    p = ps[len(ps) // 2] if len(ps) > 2 else ps[0]
                    self.planned_jump = now + p
                else:
                    kmin = min(w[0] for w in wins)
                    best = None
                    for p in range(0, max(1, kmin - 1)):
                        n = sum(1 for k1, k2, y1 in wins for k in range(k1, k2 + 1)
                                if 0 <= k - 2 - p < len(arc_h) and arc_h[k - 2 - p] > y1)
                        if best is None or n > best[0]:
                            best = (n, p)
                    if best:
                        self.planned_jump = now + best[1]
        if self.planned_jump is not None and self.planned_jump <= now and self.jump_t < 0:
            if self.press_jump():
                st['wave_jumps'].append(now)
                self.planned_jump = None
            elif self.planned_jump < now - 3:
                st['wave_nojump'].append(now)
                self.planned_jump = None
        if self.planned_dash and self.planned_dash[0] <= now:
            self.do_dash(self.planned_dash[1])
            self.planned_dash = None
        if cur and self.dash_left == 0:
            moved = self.dodge_step(cur, ths, now, y)
        # targets and positioning
        tg = self.targets()
        star = None
        if STARS and not self.proxies():
            sts = [t for t in tg if t[2] == 'star']
            if sts:
                star = min(sts, key=lambda t: math.hypot(t[0].pos[0] - x0, t[0].pos[2] - z0))
        soon = [t for t in ths if t.k1 <= 25]
        if not moved and self.dash_left == 0 and self.policy != 'stand' and tg:
            moved = self.position(tg, star, soon, hold, ph)
        # attack decision (after moving)
        x1, z1 = self.pos()
        zone = self.zone(x1, z1) if tg else '-'
        self.bump('zone_ticks', zone)
        inreach_t = None
        if tg:
            pick = [star] if star is not None else tg
            near = min(pick, key=lambda t: self.tdist(t, x1, z1))
            if self.tdist(near, x1, z1) <= self.ch['reach']:
                inreach_t = near
        if inreach_t is not None and ok:
            self.bump('ph_reach', ph)
            if not self.in_field(x1, z1):
                self.bump('ph_up', ph)
                self.bump('pat_up', pk)
        if tg and self.policy != 'stand' and not cur and not hold:
            if inreach_t is not None:
                st['inreach'] += 1
            hold_jump = False
            if self.planned_jump is not None:
                nxt = self.ch['iv'][self.combo % len(self.ch['iv'])]
                if self.planned_jump - now < nxt + 1:
                    hold_jump = True          # keep the jump free: no new swing that would still run at the press
            if inreach_t is not None and (ok or inreach_t[2] == 'star') and self.atkcd == 0 and not hold_jump:
                iv = self.ch['iv'][self.combo % len(self.ch['iv'])]
                coef = self.ch['coef'][self.combo % len(self.ch['coef'])]
                self.combo += 1
                self.atkcd = iv
                st['swings'] += 1
                if self.hit_boss:
                    self.strike(inreach_t, coef, ph)
            if self.atkcd > 0:
                st['attack'] += 1

    def in_field(self, x, z):
        """Inside a lingering or moving hazard (fields, strips, hail, orbs): the 6.2 uptime excludes these ticks."""
        s = self.s
        for e in s.ents:
            if e.alive and 'rlk_mb_hz' in e.tags and (s.sc(('e', e.id), 'mbHzD') or 0) > 0:
                lingering = (s.sc(('e', e.id), 'mbHzRA') or 0) > 0
                v = self.vel.get(e.id)
                moving = v is not None and abs(v[0]) + abs(v[1]) > 0.02
                if (lingering or moving) and hz_inside(s, e, x, self.cy, z, 0.0):
                    return True
        return False

    def dodge_step(self, cur, ths, now, y):
        s, st = self.s, self.stats
        x0, z0 = self.pos()
        st['dodge_ticks'] += 1
        kmin = min(t.k1 for t in cur)
        esc = self.escape_point([t for t in ths if t.k1 <= 40])
        v = SPRINT if self.sprint and self.atkcd == 0 else (SWING if self.atkcd > 0 else WALK)
        cover, cd = 0.0, self.atkcd
        for k in range(kmin):
            cover += SWING if cd > 0 else (SPRINT if self.sprint else WALK)
            cd -= 1
        if esc and esc[0] > cover + 1e-6:
            for t in cur:
                key = t.src.id if t.src else 0
                if key not in self.nowalk_seen:
                    self.nowalk_seen.add(key)
                    st['nowalk'].append((now, t.kind, t.dmg, round(esc[0], 2), round(cover, 2), kmin, self.atkcd, s.pat_fn()))
        jump_ok = []
        if self.jump_t < 0 and all(t.y1 is not None and t.y1 < 3.4 for t in cur):
            jump_ok = jump_press(self.cur_arc(), [(t.k1, t.k2, t.y1) for t in cur])
        branded = self.mod.is_az() and self.mod.branded(self.player)
        # the perfect dasher while branded: time the i-frames on a one-shot strike (cleanse), plan.md 4.10 3.
        if (branded and self.dodge == 'dash' and self.charges > 0 and self.cool == 0
                and all(t.oneshot and not t.nododge for t in cur)):
            k1 = kmin
            k2 = max(t.k2 for t in cur if t.k1 == kmin)
            press = max(now, now + k2 - 1 - (self.iframes - 1))
            if press <= now + k1 - 1:
                d = (esc[1] - x0, esc[2] - z0) if esc else (0.0, 0.0)
                n = math.hypot(*d) or 1.0
                dirv = (d[0] / n, d[1] / n)
                if self.planned_dash is None:
                    st['brand_dash'] += 1
                if press == now:
                    self.do_dash(dirv)
                    self.planned_dash = None
                else:
                    self.planned_dash = (press, dirv)
                return True
        if esc and esc[0] <= cover + 1e-6:
            self.walk_to(esc[1], esc[2], v)
            return True
        if jump_ok and self.dodge in ('walk', 'dash') and (self.atkcd == 0 or jump_ok[-1] >= self.atkcd):
            p = jump_ok[0] if self.atkcd == 0 else min(x for x in jump_ok if x >= self.atkcd)
            if p == 0:
                self.press_jump()
            else:
                self.planned_jump = now + p
            if esc:
                self.walk_to(esc[1], esc[2], v)
            return True
        if (esc and self.nd_dash and all(t.nododge for t in cur) and self.charges > 0 and self.cool == 0
                and esc[0] <= 3.0 + max(0, kmin - 3) * WALK):
            # an undodgeable area: i-frames do not help, but the dash moves 3 b and cancels the swing
            d = esc[0]
            self.do_dash(((esc[1] - x0) / max(d, 1e-6), (esc[2] - z0) / max(d, 1e-6)))
            st['nd_dash'] += 1
            return True
        if esc and self.dodge == 'dash' and self.charges > 0 and self.cool == 0 and not all(t.nododge for t in cur):
            d = esc[0]
            k1 = kmin
            k2 = max(t.k2 for t in cur if t.k1 == kmin)
            dirx, dirz = (esc[1] - x0) / max(d, 1e-6), (esc[2] - z0) / max(d, 1e-6)
            reach_by_dash = d <= 3.0 + max(0, kmin - 3) * WALK
            if reach_by_dash and kmin <= 3 + int(max(0, d - 3.0) / WALK) + 2:
                self.do_dash((dirx, dirz))
            elif not reach_by_dash:
                press = max(now, now + k2 - 1 - (self.iframes - 1))
                if press <= now + k1 - 1:
                    if press == now:
                        self.do_dash((dirx, dirz))
                    else:
                        self.planned_dash = (press, (dirx, dirz))
                        self.walk_to(esc[1], esc[2], v)
                else:
                    st['unavoid'].append((now, [(t.kind, t.dmg) for t in cur], k1, k2, s.pat_fn()))
                    self.walk_to(esc[1], esc[2], v)
            else:
                self.walk_to(esc[1], esc[2], v)
            return True
        if esc:
            st['walk_fail'].append((now, [(t.kind, t.dmg) for t in cur], round(esc[0], 2), round(cover, 2), s.pat_fn()))
            self.walk_to(esc[1], esc[2], v)
        return True

    def position(self, tg, star, soon, hold, ph):
        """Policy movement (no threat at the feet). Returns True when the agent moved."""
        pl = self.player
        x0, z0 = self.pos()
        st = self.stats
        a = self.anchor()
        # stop attacking at the transition message: keep >= 10 b from the anchor
        if hold and a is not None:
            d = math.hypot(a.pos[0] - x0, a.pos[2] - z0)
            if d < 10.0:
                gx, gz = (x0 + (x0 - a.pos[0]) / max(d, 1e-6) * 2, z0 + (z0 - a.pos[2]) / max(d, 1e-6) * 2)
                if d < 1e-6 or not self.step_toward(*self.clampw(gx, gz), soon):
                    tx, tz = -(a.pos[2] - z0) / max(d, 1e-6), (a.pos[0] - x0) / max(d, 1e-6)
                    self.step_toward(*self.clampw(x0 + tx, z0 + tz), soon)
            return True
        # shards: pick up a shard within 6 b when it and the way to it are safe
        if self.shards:
            sh = [e for e in self.s.ents if e.alive and CONTRACT['shard_tag'] in e.tags
                  and math.hypot(e.pos[0] - x0, e.pos[2] - z0) <= 6.0]
            if sh:
                e = min(sh, key=lambda e: math.hypot(e.pos[0] - x0, e.pos[2] - z0))
                if self.safe_at(soon, e.pos[0], e.pos[2], pad=0.3):
                    st['shard_walks'] += 1
                    self.step_toward(e.pos[0], e.pos[2], soon)
                    return True
        tgt = star if star is not None else min(tg, key=lambda t: self.tdist(t, x0, z0))
        e = tgt[0]
        pol = self.policy
        if pol == 'melee':
            want = min(2.5, self.ch['reach'] - 1.0)
            if tgt[2] == 'px':
                d = self.tdist(tgt, x0, z0)
                if d > want:
                    self.step_toward(e.pos[0], e.pos[2], soon, stop=tgt[3] + want)
                return False
            # fgfair's chase of the body / star point (kept bit for bit for the Guardian reproduction)
            bx, bz = e.pos[0], e.pos[2]
            d = math.hypot(bx - x0, bz - z0)
            if d > want:
                v = SPRINT if self.atkcd == 0 else SWING
                step = min(v, d - want)
                nx, nz = self.clampw(x0 + (bx - x0) / d * step, z0 + (bz - z0) / d * step)
                if self.safe_at(soon, nx, nz, pad=0.3) and not self.in_capsule(nx, nz, self.capsules()):
                    pl.pos[0], pl.pos[2] = nx, nz
            return False
        if pol == 'ranged':
            ref = a if (tgt[2] == 'px' and a is not None) else e
            bx, bz = ref.pos[0], ref.pos[2]
            d = math.hypot(bx - x0, bz - z0)
            if d < 8.0 or d > 11.0:
                sgn = -1 if d < 8.0 else 1
                v = SWING if self.atkcd > 0 else WALK
                nx, nz = self.clampw(x0 + (bx - x0) / d * v * sgn, z0 + (bz - z0) / d * v * sgn)
                if math.hypot(nx - x0, nz - z0) < 0.05 and sgn < 0:
                    tx, tz = -(bz - z0) / d, (bx - x0) / d
                    nx, nz = self.clampw(x0 + tx * v, z0 + tz * v)
                if self.safe_at(soon, nx, nz, pad=0.3) and not self.in_capsule(nx, nz, self.capsules()):
                    pl.pos[0], pl.pos[2] = nx, nz
            return False
        if pol == 'ranged_flank':
            # orbit at 10-14 b from the anchor (tangential walk, radial correction), reversing at a blocked step
            ref = a if a is not None else e
            dx, dz = x0 - ref.pos[0], z0 - ref.pos[2]
            d = math.hypot(dx, dz) or 1e-6
            ux, uz = dx / d, dz / d
            tx, tz = -uz * self.orbit_dir, ux * self.orbit_dir
            rad = 0.0 if 10.0 <= d <= 14.0 else (1.0 if d < 10.0 else -1.0)
            v = SWING if self.atkcd > 0 else WALK
            mx, mz = tx + ux * rad, tz + uz * rad
            n = math.hypot(mx, mz) or 1.0
            nx, nz = self.clampw(x0 + mx / n * v, z0 + mz / n * v)
            if (math.hypot(nx - x0, nz - z0) < 0.5 * v or not self.safe_at(soon, nx, nz, pad=0.3)
                    or self.in_capsule(nx, nz, self.capsules())):
                self.orbit_dir *= -1
            else:
                pl.pos[0], pl.pos[2] = nx, nz
            return False
        # positional melee: head / tail / flank (plan.md 4.12 zones; angular sectors for a boss without proxies)
        want = min(2.5, self.ch['reach'] - 1.0)
        if pol == 'melee_head':
            prefer, zok = HEAD_PX, (lambda zn: zn == 'head')
        elif pol == 'melee_tail':
            prefer, zok = TAIL_PX, (lambda zn: zn == 'tail')
        else:
            prefer, zok = FLANK_PX, (lambda zn: zn == 'flank')
        if not any(t[2] == 'px' and t[1] in prefer for t in tg):
            prefer = ()
        g = self.goal_point(prefer, zok, want, soon)
        if g is None:
            g = self.goal_point((), zok, want + 1.0, soon)
        if g is not None and g[0] > 0.3:
            self.step_toward(g[1], g[2], soon)
        return False

    def strike(self, t, coef, ph):
        s, st = self.s, self.stats
        e, n, kind, hw = t
        dmg = max(1, self.atk * coef // 100)
        landed, dealt, killed = Z.strike(s, e, dmg, elem=self.ch['el'], ranged=self.ch['ranged'])
        if landed and kind != 'star':
            st['hits'] += 1
            self.bump('ph_hits', ph)
            self.bump('ph_dealt', ph, dealt)
            self.bump('tgt_hits', n)
            s.dealt.append([s.t + 1, dealt, ph, s.pat_fn(), n])
        elif landed:
            self.bump('tgt_hits', n)


# ------------------------------------------------------------------------------------------- one fight
class Track:
    def __init__(self, s):
        self.s = s
        self.dead_t = None
        self.t_start = s.t

    def tick(self):
        s = self.s
        if self.dead_t is None and (s.sc('#mbSt', 'mb') or 0) in (2, 3) and s.t > self.t_start + 20:
            self.dead_t = s.t


BOSS_FORCE = {'guardian': 1, 'butterfly': 2, 'fieldgen': 3, 'proto': 99}


def fight(boss='guardian', policy='melee', dodge='walk', react=5, n=3600, seed=1018, level=5, char='sword',
          real_hp=False, until_dead=False, pair=None, phases=None, mob_lv=None, iframes=DASH_IF, sprint=False,
          jump_waves=True, hit_boss=True, tri_aware=True, nd_dash=True, dp=None):
    """One fight. boss: guardian / butterfly / fieldgen / proto (mid-boss gate) or azhdaha / cproto (chapter mode).
    phases: [(test pattern id or None, ticks), ...] (Azhdaha: forced phases); pair 0-3 forces the element pair.
    mob_lv: the boss level (default 4 for mid-bosses as every earlier sim, 6 for chapter-1 bosses)."""
    dp = dp or Z.dp_root()
    chapter = boss not in BOSS_FORCE
    lv = mob_lv or (6 if chapter else 4)
    b = Z.boss_entry(dp, boss)
    hp = (b['hp'] * Z.LV_HP(lv) // 100) if (real_hp and b) else 100000
    s, zone, player = Z.setup(force=0 if chapter else BOSS_FORCE[boss], lv=lv, hp=hp, seed=seed, player_level=level, dp=dp)
    s.arena = Z.arena_of(dp, b)
    s.dealt = []
    if chapter:
        Z.chapter_entry(s, boss)
    elif not Z.to_fight(s, zone):
        raise RuntimeError('mid-boss did not start')
    ag = Agent(s, player, policy, dodge, react, char, sprint, iframes, jump_waves, hit_boss, tri_aware, level, nd_dash)
    if pair is not None and ag.mod.is_az():
        Z.G.test(s, player, CONTRACT['test_pair'] + pair)
    tr = Track(s)
    t0 = s.t
    s.dmg.clear()
    s.dodges.clear()
    plan = phases or [(None, n)]
    for pid, ticks in plan:
        if pid is not None and ag.mod.is_az():
            Z.G.test(s, player, pid)
        for _ in range(ticks):
            ag.step()
            Z.world(s)
            tr.tick()
            if until_dead and tr.dead_t is not None:
                break
        if until_dead and tr.dead_t is not None:
            break
    return s, ag, tr, t0


if __name__ == '__main__' and not (len(sys.argv) > 1 and sys.argv[1] == 'probes'):
    import time
    t = time.time()
    s, ag, tr, t0 = fight(policy=sys.argv[1] if len(sys.argv) > 1 else 'melee',
                          dodge=sys.argv[2] if len(sys.argv) > 2 else 'walk', n=int(sys.argv[3]) if len(sys.argv) > 3 else 1200)
    lost = sum(d[3] for d in s.dmg)
    print('HP lost', lost, 'hits', len(s.dmg), 'dealt', sum(d[1] for d in s.dealt), 'deaths', len(ag.stats['deaths']),
          'secs', round(time.time() - t, 1))


# ------------------------------------------------------------------------------------------- probes
def probes(dp=None):
    """Unit probes of the 8.4 features that switch on with the Azhdaha module / AZ-CM, on synthetic entities in a
    world without a live fight (so the framework does not tick them): proxies, N4 safe circles, moving discs, an
    expanding low front, push capsules, shards, the transition hold, the branded dasher. Exit 1 on a failure."""
    from mcsim import Ent
    fails = []

    def ck(name, ok, info=''):
        print(('ok   ' if ok else 'FAIL ') + name, info)
        if not ok:
            fails.append(name)

    def world0(level=5):
        s, zone, pl = Z.setup(force=1, player_level=level, dp=dp)
        s.arena = dict(Z.registry(s.dp)['arena'])
        s.dealt = []
        body = Ent('husk', (200.0, 201.0, 8.0), (0.0, 0.0), ['rlk_mb_body', 'rlk_mob', 'boss', 'rlk_room'])
        s.ents.append(body)
        for o, v in (('mhpM', 100000), ('mhpC', 100000), ('mlv', 6)):
            s.setsc(('e', body.id), o, v)
        s.setsc('#mbSt', 'mb', 1)
        s.setsc('#mbId', 'mb', CONTRACT['az_n'])
        pl.pos[:] = [200.0, 201.0, 16.0]
        return s, pl, body

    def hz(s, pos, K, W=20, A=1, D=100, R=30, R0=0, Y1=20, ND=0, RA=0, I=None, rr=None, ri=None):
        e = Ent('marker', pos, (0.0, 0.0), ['rlk_mb_hz', 'rlk_room'])
        s.ents.append(e)
        hid = I if I is not None else 9000 + e.id
        for o, v in (('mbHzK', K), ('mbHzW', W), ('mbHzT', 0), ('mbHzA', A), ('mbHzD', D), ('mbHzY0', -1000),
                     ('mbHzY1', Y1 * 100), ('mbHzR', R * 100), ('mbHzR0', R0 * 100), ('mbHzND', ND), ('mbHzRA', RA),
                     ('mbHzHit', 0), ('mbHzI', hid), ('mbHzFX', 0), ('mbHzFZ', 1000), ('mbHzAng', 180)):
            s.setsc(('e', e.id), o, v)
        rro = (R * 100 + 300) if rr is None else rr
        s.setsc(('e', e.id), 'mbHzRR', rro * rro)
        s.setsc(('e', e.id), 'mbHzRI', 0 if ri is None else ri * ri)
        s.hzrec[e.id] = dict(t=s.t - 10, pat=0, clock=0, K=K, W=W, D=D, A=A, Y1=Y1 * 100, R=R * 100, ND=ND, RA=RA)
        return e

    # 1. proxies: nearest vulnerable column in reach (horizontal to the surface), never the body point
    s, pl, body = world0()
    ag = Agent(s, pl, 'melee', 'walk')
    cols = []
    for name, (x, z, w, vul) in {'head': (200.0, 12.3, 2.8, True), 'chest': (200.0, 10.1, 4.6, True),
                                 'tail2': (200.0, -2.1, 2.2, False)}.items():
        e = Ent('interaction', (x, 201.0, z), (0.0, 0.0), ['rlk_mb_px', 'rlk_mb_px_' + name, 'rlk_room']
                + (['rlk_mob'] if vul else []))
        e.data.update(width=w, height=3.0)
        s.ents.append(e)
        cols.append(e)
        for o in ('mhpM', 'mhpC', 'mhp0'):
            s.setsc(('e', e.id), o, 10 ** 6)
    tg = ag.targets()
    ck('targets = vulnerable proxies only', sorted(t[1] for t in tg) == ['chest', 'head'], str([t[1] for t in tg]))
    pl.pos[:] = [200.0, 201.0, 15.9]
    near = min(tg, key=lambda t: ag.tdist(t, 200.0, 15.9))
    ck('nearest proxy by surface distance', near[1] == 'head' and abs(ag.tdist(near, 200.0, 15.9) - 2.2) < 1e-6,
       f'{near[1]} {ag.tdist(near, 200.0, 15.9):.2f}')
    ck('zone at the head front (4.12)', ag.zone(200.0, 15.9) == 'head', ag.zone(200.0, 15.9))
    ck('zone at the flank', ag.zone(205.0, 9.0) == 'flank', ag.zone(205.0, 9.0))
    ck('zone on the tail lane', ag.zone(200.5, 1.0) == 'tail', ag.zone(200.5, 1.0))
    for _ in range(40):
        ag.step()
        s.t += 1
    ck('melee walker swings at the head proxy, never the body', ag.stats['tgt_hits'].get('head', 0) >= 3
       and ag.stats['tgt_hits'].get('body', 0) == 0,
       str(ag.stats['tgt_hits']))
    # positional policy: melee_flank walks to a flank point in reach of chest / belly / hips / paws / feet
    s, pl, body = world0()
    for name, (x, z, w) in {'head': (200.0, 12.3, 2.8), 'chest': (200.0, 10.1, 4.6), 'hips': (200.0, 4.6, 4.4),
                            'tail1': (200.0, 1.65, 2.6)}.items():
        e = Ent('interaction', (x, 201.0, z), (0.0, 0.0), ['rlk_mb_px', 'rlk_mb_px_' + name, 'rlk_room', 'rlk_mob'])
        e.data.update(width=w, height=3.0)
        s.ents.append(e)
        for o in ('mhpM', 'mhpC', 'mhp0'):
            s.setsc(('e', e.id), o, 10 ** 6)
    ag = Agent(s, pl, 'melee_flank', 'walk')
    for _ in range(120):
        ag.step()
        s.t += 1
    ck('melee_flank reaches the flank and hits flank proxies', ag.zone(*ag.pos()) == 'flank'
       and sum(ag.stats['tgt_hits'].get(n, 0) for n in FLANK_PX) >= 3 and 'body' not in ag.stats['tgt_hits'], f'{ag.zone(*ag.pos())} {ag.stats["tgt_hits"]}')
    s, pl, body = world0()
    for name, (x, z, w) in {'head': (200.0, 12.3, 2.8), 'tail1': (200.0, 1.65, 2.6), 'tail2': (200.0, -2.1, 2.2)}.items():
        e = Ent('interaction', (x, 201.0, z), (0.0, 0.0), ['rlk_mb_px', 'rlk_mb_px_' + name, 'rlk_room', 'rlk_mob'])
        e.data.update(width=w, height=3.0)
        s.ents.append(e)
        for o in ('mhpM', 'mhpC', 'mhp0'):
            s.setsc(('e', e.id), o, 10 ** 6)
    ag = Agent(s, pl, 'melee_tail', 'walk')
    for _ in range(200):
        ag.step()
        s.t += 1
    ck('melee_tail reaches the tail lane and hits tail proxies', ag.zone(*ag.pos()) == 'tail'
       and sum(ag.stats['tgt_hits'].get(n, 0) for n in TAIL_PX) >= 3 and 'body' not in ag.stats['tgt_hits'], f'{ag.zone(*ag.pos())} {ag.stats["tgt_hits"]}')
    # 2. N4 mask: the agent goes to the nearest safe circle of the hazard
    s, pl, body = world0()
    ag = Agent(s, pl, 'stand', 'walk')
    m = hz(s, (200.0, 201.0, 8.0), CONTRACT['mask_kind'], W=60, A=1, R=0, R0=15)
    s.setsc(('e', m.id), CONTRACT['safe_grp'], 0)            # group 0 = the hazard's own id (cm.md 13.6)
    hid = s.sc(('e', m.id), 'mbHzI')
    for (x, z) in ((206.0, 16.0), (190.0, 8.0)):
        c = Ent('marker', (x, 201.0, z), (0.0, 0.0), [CONTRACT['safe_tag'], 'rlk_room', 'rlk_mb_aux'])
        s.ents.append(c)
        s.setsc(('e', c.id), CONTRACT['safe_grp'], hid)
    other = Ent('marker', (200.0, 201.0, 17.0), (0.0, 0.0), [CONTRACT['safe_tag'], 'rlk_room', 'rlk_mb_aux'])
    s.ents.append(other)
    s.setsc(('e', other.id), CONTRACT['safe_grp'], hid + 1)  # another group's circle next to the player: not safe
    for _ in range(59):
        ag.step()
        s.t += 1
        s.setsc(('e', m.id), 'mbHzT', s.t - 1)
    d = math.hypot(pl.pos[0] - 206.0, pl.pos[2] - 16.0)
    ck('N4: walks into the nearest safe circle (r 1.5 + 0.3)', d <= 1.8, f'dist {d:.2f}')
    # 3. a moving disc (orb): the agent steps out of its extrapolated track
    s, pl, body = world0()
    ag = Agent(s, pl, 'stand', 'walk')
    pl.pos[:] = [200.0, 201.0, 16.0]
    o = hz(s, (196.0, 201.0, 16.0), 1, W=1, A=400, D=35, R=15, RA=10)
    hits = 0
    for _ in range(40):
        o.pos[0] += 0.25
        ag.step()
        s.t += 1
        s.setsc(('e', o.id), 'mbHzT', s.t - 1)
        hits += 1 if hz_inside(s, o, pl.pos[0], 201.0, pl.pos[2]) else 0
    ck('moving disc: steered out of the orb track', hits <= 3 and ag.vel.get(o.id, (0, 0))[0] > 0.2, f'ticks inside {hits}')
    # 4. an expanding low front (N10): planned jump
    s, pl, body = world0()
    ag = Agent(s, pl, 'stand', 'walk')
    pl.pos[:] = [200.0, 201.0, 16.0]
    f = hz(s, (200.0, 201.0, 8.0), 2, W=1, A=40, D=90, R=3, Y1=7, rr=3300, ri=1700)
    for _ in range(30):
        ag.step()
        s.t += 1
        s.setsc(('e', f.id), 'mbHzT', s.t - 1)
        rr = int(math.sqrt(s.sc(('e', f.id), 'mbHzRR'))) + 400
        ri = int(math.sqrt(s.sc(('e', f.id), 'mbHzRI'))) + 400
        s.setsc(('e', f.id), 'mbHzRR', rr * rr)
        s.setsc(('e', f.id), 'mbHzRI', ri * ri)
    ck('expanding low front: growth read, jump pressed', ag.stats['jumps'] >= 1 and 0.35 < ag.growth.get(f.id, 0) < 0.45,
       f'jumps {ag.stats["jumps"]} growth {ag.growth.get(f.id, 0):.2f}')
    # 5. push capsules: no step into a capsule while #mbPushOn 1
    s, pl, body = world0()
    ag = Agent(s, pl, 'melee', 'walk')
    s.setsc(CONTRACT['push_on'], 'mb', 1)
    s.storage.setdefault('rlk:mboss', {})[CONTRACT['push_path']] = [dict(f0=-38, f1=26, hw=28),
                                                                   dict(f0=26, f1=54, hw=16, px='head', top=35)]
    hd = Ent('interaction', (200.0, 201.0, 12.3), (0.0, 0.0), ['rlk_mb_px', 'rlk_mb_px_head', 'rlk_room'])
    hd.data.update(width=2.8, height=5.0)                    # the head is up (top 5.0 > 3.5): its capsule is off
    s.ents.append(hd)
    pl.pos[:] = [200.0, 201.0, 14.0]
    inside = 0
    for _ in range(60):
        ag.step()
        s.t += 1
        inside += 1 if ag.in_capsule(pl.pos[0], pl.pos[2], ag.capsules(), pad=0.0) else 0
    caps1 = ag.capsules()
    hd.data['height'] = 3.0
    caps2 = ag.capsules()
    ck('push capsule: the walker never enters it; the head capsule only while the head is low', inside == 0
       and ag.in_capsule(200.0, 9.0, caps1) and len(caps1) == 1 and len(caps2) == 2, f'ticks inside {inside}')
    # 6. shard pickup within 6 b
    s, pl, body = world0()
    ag = Agent(s, pl, 'melee', 'walk')
    pl.pos[:] = [205.0, 201.0, 16.0]
    sh = Ent('item_display', (209.0, 201.0, 18.0), (0.0, 0.0), [CONTRACT['shard_tag'], 'rlk_mb_aux', 'rlk_room'])
    s.ents.append(sh)
    for _ in range(25):
        ag.step()
        s.t += 1
    ck('shard: walks onto a shard within 6 b', math.hypot(pl.pos[0] - 209.0, pl.pos[2] - 18.0) < 0.3,
       f'dist {math.hypot(pl.pos[0] - 209.0, pl.pos[2] - 18.0):.2f}')
    # 7. transition message: no attacks, keeps >= 10 b
    s, pl, body = world0()
    ag = Agent(s, pl, 'melee', 'walk')
    pl.pos[:] = [200.0, 201.0, 10.5]
    s.setsc(CONTRACT['tr'], 'mb', 1)
    for _ in range(80):
        ag.step()
        s.t += 1
    d = math.hypot(pl.pos[0] - 200.0, pl.pos[2] - 8.0)
    ck('transition: stops attacking, keeps >= 10 b', ag.stats['swings'] == 0 and d >= 9.9, f'swings {ag.stats["swings"]} d {d:.1f}')
    s.setsc(CONTRACT['tr'], 'mb', 0)
    for _ in range(120):
        ag.step()
        s.t += 1
    ck('transition over: attacks again', ag.stats['swings'] >= 1, f'swings {ag.stats["swings"]}')
    # 8. branded dasher: times the i-frames on a one-shot strike (cleanse) instead of walking out
    s, pl, body = world0()
    ag = Agent(s, pl, 'stand', 'dash')
    pl.pos[:] = [200.0, 201.0, 16.0]
    s.setsc(('e', pl.id), CONTRACT['brand_t'], 3)
    st = hz(s, (200.0, 201.0, 16.0), 1, W=14, A=1, D=100, R=2)
    for _ in range(16):
        ag.step()
        s.t += 1
        s.setsc(('e', st.id), 'mbHzT', s.t - 1)
    hit_t = 14 + 1                       # the strike tick (mbHzT = s.t - 1 reaches W)
    ck('branded dasher: i-frames cover the strike tick', ag.stats['brand_dash'] == 1 and s.iframe_end >= hit_t
       and ag.stats['dashes'] == 1,
       f'brand_dash {ag.stats["brand_dash"]} iframes to {s.iframe_end} strike ~{hit_t}')
    # 9. an undodgeable area: the walker dashes out when walking (swing-slowed) is too slow
    s, pl, body = world0()
    ag = Agent(s, pl, 'stand', 'walk')
    pl.pos[:] = [200.0, 201.0, 16.0]
    ag.atkcd = 10
    hz(s, (200.0, 201.0, 16.0), 1, W=8, A=1, D=100, R=25, ND=1)
    for _ in range(4):
        ag.step()
        s.t += 1
    ck('undodgeable area: dash used as movement', ag.stats['nd_dash'] == 1 and ag.atkcd == 0, f'nd_dash {ag.stats["nd_dash"]}')
    print(f'{len(fails)} failure(s)')
    return fails


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'probes':
    sys.exit(1 if probes() else 0)
