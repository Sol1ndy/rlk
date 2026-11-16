#!/usr/bin/env python3
"""Fairness fight simulator for the field generator (review scratch; read-only on a datapack COPY).

Built on mb3/tests/fgsim.py (the field generator's mcsim harness: the real module, the real fx kit, attribute
modifiers, the real low-gravity lines of rlk:tick) with the method of the butterfly fairness review
(mb2/review/fairness/sim/fsim.py, balance copy mb2/balance/fsim.py):
- the player hit path is the REAL one (rlk:cm/hit_pl2 -> player/take_damage: level scaling, defence, dash i-frames
  via dashInvT; #hzNoDodge hazards go through mboss/hurt_nd, which this sim respects: the i-frames are NOT set for
  them);
- a scripted agent moves the player every tick before the world tick: walk 0.2159 b/t, sprint 0.2807, swing slow
  0.108 (shoulder view, while atkcd > 0), dash 3 b in 3 t with 2 charges / 20 t regen / 5 t cooldown and IF ticks of
  i-frames, jumps with the arc of the player's CURRENT gravity / jump_strength attributes (vanilla 0.08 / 0.42, low
  gravity x0.5 / x1.19), never pressing a jump while swinging;
- it reacts to what it can see REACT ticks after it appears: framework hazards (hz markers, read from their scores),
  projectiles, the wave fronts (whose growth 0.55 b/t it extrapolates: the decal shows the ring), and the C3 beam band
  r 2.7-6.1 (the spec's rule: stay out of the band while the beams orbit);
- the agent ATTACKS through rlk:combat/apply (fgsim's stub: element/on_hit, the module on_hit, apply_mods with the
  module's incoming hook), so the 20-hit meter, its 6 t ICD and the field damage cut are the module's own.
Guardian (force 1) runs in the same harness with its rig calls logged (spear props kept as pj threats).
"""
import math
import os
import sys

TESTS = '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/mb3/tests'
sys.path.insert(0, TESTS)
import fgsim as G  # noqa: E402
from mcsim import Ent, Ctx  # noqa: E402

DP = os.environ.get('FDP', '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/tele/wt_fg/roguelike')
A = G.init(DP)
C0 = G.C0
CX, CY, CZ = A.CX, A.CY, A.CZ
WALK_R = 20.7
WALK, SPRINT, SWING = 0.2159, 0.2807, 0.10795
DASH_IF = int(os.environ.get('DASH_IF', '6'))
STARS = os.environ.get('STARS', '1') == '1'   # Guardian: the agent attacks her chaos stars while they exist
GLINT = os.environ.get('GLINT', '0') == '1'   # (tele/fg 10-20) no lanes any more: read the slab's flare + the lock as the lane
LANES = os.environ.get('LANES', '1') == '1'   # the agent reads the slab throw lines (dmg-0 lanes) as the coming blade     # spec 1.3: 6 t of i-frames from the press (the butterfly sim used 5)

# character models: swing intervals (atkCD per hit at 100 % attack speed, README 3), reach, coefficients
CHARS = {
    'sword':    dict(iv=[6, 10], reach=3.5, coef=[100, 120], ranged=False),          # Lumine
    'navia':    dict(iv=[11, 11, 15, 22], reach=4.5, coef=[100, 100, 130, 160], ranged=False),
    'nefer':    dict(iv=[5, 5, 5, 10], reach=3.5, coef=[61, 60, 80, 98], ranged=False),
    'bow':      dict(iv=[8], reach=30.0, coef=[100], ranged=True),                     # Yoimiya plain shots
    'catalyst': dict(iv=[10, 10, 10, 16], reach=30.0, coef=[72, 66, 90, 120], ranged=True),   # Ronova orbs
}
PL_ATK = 16                      # Lv4 item-less base atk (load: lvAtk0 10 + 2 x 3)
LV_FACTOR = 104 / (104 + 100 + 4 * 150 // 100)   # combat/lv_mult at player Lv4 vs mob Lv4 (#mobLvDef 150)


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


class FairSim(G.FSim):
    def __init__(self, root):
        super().__init__(root)
        self.hzrec = {}
        self.iframe_end = -1
        self.dodges = []          # (t, pct, pat)
        self.dmg = []             # (t, pct, el, hp_lost, pat, field stage, meter open, nododge)
        self.kb = None
        self.agent = None
        self.dealt = []           # (t, dmg dealt to the body, state key, counted)

    def pat(self):
        return self.sc('#fgPat', 'mb') or self.sc('#gdPat', 'mb') or self.sc('#bfPat', 'mb') or 0

    def call(self, fid, ctx, macro=None):
        if fid.startswith('rlk:mboss/guardian/rig/') or fid.startswith('rlk:mboss/butterfly/rig/'):
            sub = fid.split('/rig/', 1)[1]
            self.rig.append((self.t, 'x/' + sub))
            if sub == 'prop/spear':
                for e in self.ents:
                    e.tags.discard('rlk_mb_gd_prop_new')
                self.ents.append(Ent('item_display', ctx.pos, (ctx.rot[0], 0.0),
                                     ['rlk_room', 'rlk_mb_aux', 'rlk_mb_gd_prop', 'rlk_mb_gd_prop_new']))
            if sub == 'face/player' and ctx.ex is not None:
                return self.call('rlk:fgtest/face_player', ctx)
            if sub == 'face/track' and ctx.ex is not None:
                return self.call('rlk:mboss/mv/turn', ctx, {'max': 4})
            return 1
        if fid == 'rlk:cm/hit_pl2':
            pl = self.agent.player if self.agent else None
            nd = (self.sc('#mbNoDodge', 'mb') or 0) == 1
            if pl is not None:
                # the dash i-frames (dashInvT) except for a #hzNoDodge hit (mboss/hurt_nd zeroes them around the call)
                self.setsc(('e', pl.id), 'dashInvT', 1 if (self.t <= self.iframe_end and not nd) else 0)
                self.setsc('#hurtDmg', 'tmp', 0)
            pct, el = self.sc('#mbHitPct', 'mb'), self.sc('#cmEl', 'tmp')
            r = super().call(fid, ctx, macro)
            if pl is not None:
                if (self.sc('#dodged', 'tmp') or 0) == 1:
                    self.dodges.append((self.t, pct, self.pat()))
                else:
                    lost = self.sc('#hurtDmg', 'tmp') or 0
                    self.dmg.append((self.t, pct, el, lost, self.pat(), self.sc('#fgField', 'mb') or 0,
                                     self.sc('#fgOpen', 'mb') or 0, 1 if nd else 0))
                    src = self.select('@e[tag=rlk_plkb_source,limit=1]', C0)
                    k = self.sc('#cmKB', 'tmp') or 0
                    if src and k > 0:
                        yaw = math.radians(src[0].rot[0])
                        self.kb = (-math.sin(yaw), math.cos(yaw), k)
                self.setsc(('e', pl.id), 'dashInvT', 0)
                self.agent.check_death()
            return r
        if fid == 'rlk:player/heal' and self.agent:
            return super().call(fid, ctx, macro)
        r = super().call(fid, ctx, macro)
        if fid == 'rlk:mboss/hz/init' and ctx.ex is not None:
            e = ctx.ex
            g = lambda o: self.sc(('e', e.id), o)  # noqa: E731
            pl = self.agent.player if self.agent else None
            rec = dict(t=self.t, pat=self.pat(), clock=self.sc('#fgPT', 'mb'), K=g('mbHzK'), W=g('mbHzW'), D=g('mbHzD'),
                       A=g('mbHzA'), Y1=g('mbHzY1'), R=g('mbHzR'), ND=g('mbHzND'), RA=g('mbHzRA'), G=g('mbHzG'),
                       pos=tuple(e.pos), ppos=tuple(pl.pos) if pl else None, fld=self.sc('#fgField', 'mb') or 0,
                       wave='rlk_mb_fg_p21f' in e.tags)
            if pl is not None and (rec['D'] or 0) > 0 and rec['K'] in (1, 2, 3, 4):
                rec['inside'] = hz_inside(self, e, pl.pos[0], CY, pl.pos[2])
            self.hzrec[e.id] = rec
        return r


STUB_EXTRA = {
    'rlk:items/proc/taken': [], 'rlk:engravings/guard/absorb': [], 'rlk:element/shield_absorb': [],
    'rlk:player/knockback/start': [], 'rlk:cm/hurt_fx': [], 'rlk:items/proc/lion_queue': [],
    'rlk:engravings/berserk/taken': [], 'rlk:element/display': [], 'rlk:element/set_icon': [],
    'rlk:element/infuse_end': [],
}

REG_HP = {b['n']: b['hp'] for b in A.REG['boss']}
LV_HP = (100 + 30 * 3 + 5 * 9 // 100) * 400 // 100      # mob/level_apply at Lv4: x(100 + 30x + 5x^2/100)% x #mobHpMul 400 %


def new_sim(force=3, level=4, seed=1018, real_hp=False):
    G.SEED[0] = seed
    orig = G.FSim
    G.FSim = FairSim
    try:
        s, zone, player = G.setup(force=force)
    finally:
        G.FSim = orig
    s.cache.pop('rlk:cm/hit_pl2', None)          # the real hit path
    for k, v in STUB_EXTRA.items():
        s.cache[k] = list(v)
    if real_hp:
        hp = REG_HP[force] * LV_HP // 100
        s.cache['rlk:room/mob_init'] = ['scoreboard players set @s mlv 4', 'function rlk:mboss/base_stats with storage rlk:mboss cur',
                                        f'scoreboard players set @s mhpM {hp}', f'scoreboard players set @s mhpC {hp}']
    hp = 100 + 12 * (level - 1)
    for o, v in (('curHealth', hp), ('maxHealth', hp), ('def', 10 + 2 * (level - 1)), ('dashInvT', 0), ('scT', 0),
                 ('it_lion_mane', 0), ('hurtLv', 0), ('hurtElem', 0), ('elAct', 0), ('burnOn', 0), ('level', level),
                 ('shieldHP', 0), ('shieldT', 0), ('infuseT', 0), ('infuse', 0)):
        s.setsc(('e', player.id), o, v)
    for el in ('Fire', 'Water', 'Thunder', 'Ice', 'Grass', 'Void'):
        s.setsc(('e', player.id), 'a' + el, 0)
        s.setsc(('e', player.id), 'd' + el, 0)
    for k, v in (('#defK', 100), ('#defKLv', 4), ('#mobLvAtk', 14), ('#mobLvAtk2', 6), ('#rxPlayerPct', 50),
                 ('#c', 0), ('#1000', 1000), ('#st10', 10), ('#100', 100)):
        s.setsc(k, 'tmp', v)
    s.setsc('berserk', 'engN', 0)
    return s, zone, player


def world(s):
    G.world(s)
    pl = s.agent.player if s.agent else None
    if pl is not None and (s.sc(('e', pl.id), 'elAct') or 0) >= 1:
        s.setsc('#hurtDmg', 'tmp', 0)
        s.setsc(('e', pl.id), 'dashInvT', 1 if s.t <= s.iframe_end else 0)
        s.call('rlk:player/elem_tick', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        s.setsc(('e', pl.id), 'dashInvT', 0)
        lost = s.sc('#hurtDmg', 'tmp') or 0
        if lost > 0:
            s.dmg.append((s.t, 0, 'dot', lost, s.pat(), s.sc('#fgField', 'mb') or 0, s.sc('#fgOpen', 'mb') or 0, 0))
        s.agent.check_death()


def body_of(s):
    return G.body_of(s)


# ------------------------------------------------------------------------------------------- threats
def hz_inside(s, e, x, y, z, pad=0.0):
    """The framework hz/hit test (the 0.3 body pad is in the stored bounds) with an extra pad (blocks)."""
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    dy = (y - e.pos[1]) * 1000
    if dy < g('mbHzY0') or dy > g('mbHzY1'):
        return False
    K = g('mbHzK')
    dx, dz = (x - e.pos[0]) * 1000, (z - e.pos[2]) * 1000
    padm = pad * 1000
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


class Threat:
    def __init__(self, kind, fn, k1, k2, seen, src=None, y1=None, dmg=0, nododge=False):
        self.kind, self.fn, self.k1, self.k2, self.seen, self.src = kind, fn, k1, k2, seen, src
        self.y1, self.dmg, self.nododge = y1, dmg, nododge


def wave_ticks(s, e, x, z):
    """Ticks k (1 = the coming tick) on which wave front e covers a player standing at (x, z) on the floor
    (field.py waves/grow: r = 2.5 + floor(11 j / 2) / 10 at its j-th active tick, inner r - 2.5; +0.3 body pad)."""
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    if g('mbHzHit'):
        return []
    W, T, Aa = g('mbHzW'), g('mbHzT'), g('mbHzA')
    d = math.hypot(x - e.pos[0], z - e.pos[2])
    out = []
    for j in range(0, Aa):
        k = j + W - T
        if k < 1:
            continue
        rt = 25 + (11 * j) // 2 if j > 0 else 25
        r = rt / 10
        inner = max(0.0, r - 2.5 - 0.3) if j > 0 else 0.0
        if inner <= d <= r + 0.3:
            out.append(k)
    return out


def wave_ticks_virtual(s, e, x, z):
    """wave_ticks ignoring the front's own hit flag (the timing template for the triple's extra fronts)."""
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    W, T, Aa = g('mbHzW'), g('mbHzT'), g('mbHzA')
    d = math.hypot(x - e.pos[0], z - e.pos[2])
    out = []
    for j in range(0, Aa):
        k = j + W - T
        if k < 1 - 12:
            continue
        rt = 25 + (11 * j) // 2 if j > 0 else 25
        r = rt / 10
        inner = max(0.0, r - 2.5 - 0.3) if j > 0 else 0.0
        if inner <= d <= r + 0.3:
            out.append(k)
    return out


def c3_band(s, b):
    """The C3 beam band around the body (spec 2.1: r < 2.7 or r > 6.1 are safe)."""
    return lambda x, y, z, pad: (y - CY) <= 2.0 and (2.7 - pad) <= math.hypot(x - b.pos[0], z - b.pos[2]) <= (6.1 + pad)


def glint_lanes(s, now, react, out):
    """(tele/fg, telegraph rule 10-20) The slab throw lanes are gone; what the player sees 10 t before a throw is the
    hovering slab flaring (p/slab_glint) while the feet are locked: the same line as the old dmg-0 lane (from the slab's
    floor point to the locked feet, 1 b past them, half width 1.2 + the pad), threat from the throw (lock + 10) to + 14.
    Only with GLINT=1 (the strict run reads the flying blade only)."""
    reg = s.__dict__.setdefault('glint', {})
    for e in s.ents:
        if not e.alive or e.etype != 'marker':
            continue
        for pid in (6, 12):
            tg = next((t for t in e.tags if t.startswith(f'rlk_mb_fg_p{pid}t') and t[len(f'rlk_mb_fg_p{pid}t'):].isdigit()), None)
            if tg is None or (e.id, tg) in reg:
                continue
            j = int(tg[len(f'rlk_mb_fg_p{pid}t'):])
            sl = [x for x in s.ents if x.alive and f'rlk_mb_fg_p{pid}s' in x.tags and s.sc(('e', x.id), 'mbS') == j + 1]
            if sl:
                reg[(e.id, tg)] = (now, sl[0].pos[0], sl[0].pos[2], e.pos[0], e.pos[2])
    for key, (t0, sx, sz, lx, lz) in list(reg.items()):
        if now > t0 + 24:
            del reg[key]
            continue
        if now - t0 < react:
            continue
        dx, dz = lx - sx, lz - sz
        n = math.hypot(dx, dz) or 1.0
        ux, uz, ln = dx / n, dz / n, n + 1.0

        def inside(x, y, z, pad, sx=sx, sz=sz, ux=ux, uz=uz, ln=ln):
            a = (x - sx) * ux + (z - sz) * uz
            return -pad <= a <= ln + pad and abs(-(x - sx) * uz + (z - sz) * ux) <= 1.2 + pad
        out.append(Threat('lane', inside, max(1, t0 + 10 - now), t0 + 24 - now, t0, None, None, 110))


def threats(s, now, react):
    out = []
    b = body_of(s)
    if GLINT:
        glint_lanes(s, now, react, out)
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
            if D <= 0:
                # the C6 / F2 slab throw line (dmg 0, w 2.4 = the blade reach + pad): the blade launched at its strike
                # tick flies down it at 1.5 b/t (flight up to ~12 t): a lane threat from the strike on
                if rec and rec['pat'] in (6, 12) and g('mbHzK') == 4 and LANES:
                    k1 = max(1, W - T)
                    if W - T + 14 >= 1:
                        ee = e
                        out.append(Threat('lane', lambda x, y, z, pad, ee=ee: hz_inside(s, ee, x, CY, z, pad), k1, W - T + 14,
                                          seen, ee, None, 110))
                continue
            if 'rlk_mb_fg_p21f' in e.tags:
                ks = wave_ticks(s, e, s.agent.player.pos[0], s.agent.player.pos[2])
                if ks:
                    out.append(Threat('wave', None, min(ks), max(ks), seen, e, 0.7, D, True))
                # a player who knows the triple (HP < 50 %: #fq21T 1, read at the 3rd charge start) plans for the two
                # extra fronts (+6 / +12 t) before their own decals appear (10 t before their centre strike)
                if s.agent.tri_aware and rec and rec.get('clock') in (135, 136) and (s.sc('#fq21T', 'mb') or 0) == 1:
                    for m in (1, 2):
                        ksx = [k + 6 * m for k in wave_ticks_virtual(s, e, s.agent.player.pos[0], s.agent.player.pos[2])]
                        if ksx:
                            out.append(Threat('wave', None, min(ksx), max(ksx), seen, e, 0.7, D, True))
                continue
            if rec and rec['pat'] == 3 and g('mbHzK') == 4 and g('mbHzRA') > 0 and b is not None:
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
            out.append(Threat('hz', lambda x, y, z, pad, ee=ee: hz_inside(s, ee, x, y, z, pad), max(1, k1), k2, seen, ee,
                              g('mbHzY1') / 1000, D, g('mbHzND') == 1))
        elif 'rlk_mb_pj' in e.tags:
            g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
            if g('mbPjHit') or g('mbPjD') <= 0:
                continue
            ee = e
            out.append(Threat('pj', lambda x, y, z, pad, ee=ee: pj_test(s, ee, x, y, z, pad), 1, 3, now, ee, None, g('mbPjD')))
    return out


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
    """policy: 'stand' (never moves, never attacks), 'melee' (chase to 2.5 b, attack in reach), 'ranged' (keep 8-11 b,
    attack always); dodge 'none' / 'walk' (walk, jump) / 'dash' (walk, jump, dash); react = ticks from a telegraph's
    first tick to the reaction; char = CHARS key (swing intervals, reach, coefficients)."""

    def __init__(self, s, player, policy='melee', dodge='walk', react=5, char='sword', sprint=False, iframes=DASH_IF,
                 jump_waves=True, hit_boss=True, tri_aware=True):
        self.tri_aware = tri_aware
        self.s, self.player, self.policy, self.dodge, self.react = s, player, policy, dodge, react
        self.ch = CHARS[char]
        self.char = char
        self.sprint, self.iframes = sprint, iframes
        self.jump_waves, self.hit_boss = jump_waves, hit_boss
        s.agent = self
        self.charges, self.regen, self.cool = 2, 0, 0
        self.dash_left, self.dash_dir = 0, (0, 0)
        self.atkcd, self.combo = 0, 0
        self.jump_t, self.jump_arc = -1, ARC_V
        self.planned_dash = None
        self.planned_jump = None          # tick of the planned press
        self.stats = dict(ticks=0, hittable=0, attack=0, swings=0, hits=0, dodge_ticks=0, dashes=0, jumps=0, inreach=0,
                          unavoid=[], walk_fail=[], nowalk=[], wave_jumps=[], wave_nojump=[], deaths=[],
                          st_ticks={}, st_hits={}, st_dealt={})
        self.nowalk_seen = set()

    def check_death(self):
        s, pl = self.s, self.player
        if (s.sc(('e', pl.id), 'curHealth') or 0) <= 0:
            self.stats['deaths'].append(s.t)
            s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))

    def pos(self):
        return self.player.pos[0], self.player.pos[2]

    def clampw(self, x, z):
        dx, dz = x - CX, z - CZ
        r = math.hypot(dx, dz)
        if r > WALK_R:
            x, z = CX + dx * WALK_R / r, CZ + dz * WALK_R / r
        return x, z

    def hittable(self):
        s = self.s
        b = body_of(s)
        if b is None or (s.sc('#mbSt', 'mb') or 0) != 1:
            return False, b
        if 'rlk_mb_inv' in b.tags or 'rlk_mb_dying' in b.tags:
            return False, b
        return True, b

    def state_key(self):
        s = self.s
        if (s.sc('#mbId', 'mb') or 0) != 3:
            return 'gd'
        st = s.sc('#fgSt', 'mb') or 0
        if st in (3, 4, 6):
            return 'groggy'
        if (s.sc('#fgOpen', 'mb') or 0) == 1:
            return 'field'
        if (s.sc('#fgField', 'mb') or 0) >= 1:
            return 'fieldx'           # warp / pack-up (meter closed)
        return 'cruise'

    def safe_at(self, ths, x, z, y=0.0, pad=0.25):
        return not any(t.fn(x, CY + y, z, pad) for t in ths if t.fn)

    def escape_point(self, ths, maxd=14.0):
        x0, z0 = self.pos()
        best = None
        for i in range(48):
            a = 2 * math.pi * i / 48
            for k in range(1, int(maxd / 0.25) + 1):
                d = k * 0.25
                x, z = self.clampw(x0 + d * math.cos(a), z0 + d * math.sin(a))
                if self.safe_at(ths, x, z):
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
        pl.pos[1] = CY + y
        ok, b = self.hittable()
        st['ticks'] += 1
        sk = self.state_key()
        st['st_ticks'][sk] = st['st_ticks'].get(sk, 0) + 1
        if ok:
            st['hittable'] += 1
        ths = [] if self.dodge == 'none' else threats(s, now, self.react)
        waves = [t for t in ths if t.kind == 'wave']
        ths = [t for t in ths if t.kind != 'wave']
        x0, z0 = self.pos()
        cur = [t for t in ths if t.fn(x0, CY + y, z0, 0.15) and t.k1 <= 40]
        moved = False
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
                    # no single press clears every window: clear as many front ticks as possible
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
                        st['nowalk'].append((now, t.kind, t.dmg, round(esc[0], 2), round(cover, 2), kmin, self.atkcd, s.pat()))
            # a jump that clears every current threat (e.g. F2 bursts in low gravity, C5 in vanilla)
            jump_ok = []
            if self.jump_t < 0 and all(t.y1 is not None and t.y1 < 3.4 for t in cur):
                jump_ok = jump_press(self.cur_arc(), [(t.k1, t.k2, t.y1) for t in cur])
            if esc and esc[0] <= cover + 1e-6:
                self.walk_to(esc[1], esc[2], v)
                moved = True
            elif jump_ok and self.dodge in ('walk', 'dash') and (self.atkcd == 0 or jump_ok[-1] >= self.atkcd):
                p = jump_ok[0] if self.atkcd == 0 else min(x for x in jump_ok if x >= self.atkcd)
                if p == 0:
                    self.press_jump()
                else:
                    self.planned_jump = now + p
                if esc:
                    self.walk_to(esc[1], esc[2], v)
                moved = True
            elif esc and self.dodge == 'dash' and self.charges > 0 and self.cool == 0 and not all(t.nododge for t in cur):
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
                        st['unavoid'].append((now, [(t.kind, t.dmg) for t in cur], k1, k2, s.pat()))
                        self.walk_to(esc[1], esc[2], v)
                else:
                    self.walk_to(esc[1], esc[2], v)
                moved = True
            else:
                if esc:
                    st['walk_fail'].append((now, [(t.kind, t.dmg) for t in cur], round(esc[0], 2), round(cover, 2), s.pat()))
                    self.walk_to(esc[1], esc[2], v)
                moved = True
        star = None
        if STARS and b is not None:
            sts = [e for e in s.ents if e.alive and 'rlk_mb_gd_star' in e.tags]
            if sts:
                star = min(sts, key=lambda e: math.hypot(e.pos[0] - x0, e.pos[2] - z0))
        tgt = star if star is not None else b
        if not moved and self.dash_left == 0 and tgt is not None and self.policy != 'stand':
            b_ = tgt
            bx, bz = b_.pos[0], b_.pos[2]
            d = math.hypot(bx - x0, bz - z0)
            soon = [t for t in ths if t.k1 <= 25]
            if self.policy == 'melee':
                want = min(2.5, self.ch['reach'] - 1.0)
                if d > want:
                    v = SPRINT if self.atkcd == 0 else SWING
                    step = min(v, d - want)
                    nx, nz = self.clampw(x0 + (bx - x0) / d * step, z0 + (bz - z0) / d * step)
                    if self.safe_at(soon, nx, nz, pad=0.3):
                        pl.pos[0], pl.pos[2] = nx, nz
            elif self.policy == 'ranged':
                if d < 8.0 or d > 11.0:
                    sgn = -1 if d < 8.0 else 1
                    v = SWING if self.atkcd > 0 else WALK
                    nx, nz = self.clampw(x0 + (bx - x0) / d * v * sgn, z0 + (bz - z0) / d * v * sgn)
                    if math.hypot(nx - x0, nz - z0) < 0.05 and sgn < 0:
                        tx, tz = -(bz - z0) / d, (bx - x0) / d
                        nx, nz = self.clampw(x0 + tx * v, z0 + tz * v)
                    if self.safe_at(soon, nx, nz, pad=0.3):
                        pl.pos[0], pl.pos[2] = nx, nz
        # attack decision (after moving)
        x1, z1 = self.pos()
        if star is not None:
            b, ok = star, True
        if b is not None and self.policy != 'stand' and not cur:
            d3 = math.dist((b.pos[0], b.pos[1], b.pos[2]), (x1, pl.pos[1], z1))
            inreach = d3 <= self.ch['reach']
            if inreach:
                st['inreach'] += 1
            hold = False
            if self.planned_jump is not None:
                nxt = self.ch['iv'][self.combo % len(self.ch['iv'])]
                if self.planned_jump - now < nxt + 1:
                    hold = True            # keep the jump free: no new swing that would still run at the press
            if inreach and ok and self.atkcd == 0 and not hold:
                iv = self.ch['iv'][self.combo % len(self.ch['iv'])]
                coef = self.ch['coef'][self.combo % len(self.ch['coef'])]
                self.combo += 1
                self.atkcd = iv
                st['swings'] += 1
                if self.hit_boss:
                    self.strike(b, coef, sk)
            if self.atkcd > 0:
                st['attack'] += 1
        s.iframe_end = max(s.iframe_end, -1)

    def strike(self, b, coef, sk):
        s, st = self.s, self.stats
        dmg = max(1, int(PL_ATK * coef / 100 * LV_FACTOR))
        if 'rlk_mb_gd_star' in b.tags:
            sk = 'star'
        b0 = s.sc('#fgBrk', 'mb') or 0
        dealt = G.hit(s, b, 0, dmg)
        counted = (s.sc('#fgBrk', 'mb') or 0) > b0
        if dealt is not None and dealt >= 0:
            st['hits'] += 1
            st['st_hits'][sk] = st['st_hits'].get(sk, 0) + 1
            st['st_dealt'][sk] = st['st_dealt'].get(sk, 0) + dealt
            s.dealt.append((s.t + 1, dealt, sk, 1 if counted else 0))

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
        self.atkcd = 0
        self.dash_left = 3
        self.dash_dir = direction
        s.iframe_end = s.t + 1 + self.iframes - 1
        self.stats['dashes'] += 1
        x, z = self.clampw(self.player.pos[0] + direction[0], self.player.pos[2] + direction[1])
        self.player.pos[0], self.player.pos[2] = x, z
        self.dash_left = 2
        return True


class Track:
    """Per-tick record of the fight's state (field windows, meter, breaks)."""

    def __init__(self, s):
        self.s = s
        self.fields = []       # dict(open=t, close=t, broke=bool, hits=[t of counts], hp_open)
        self.cur = None
        self.prev_open = 0
        self.prev_brk = 0
        self.tri = []          # ticks of #fq21T 1
        self.dead_t = None

    def tick(self):
        s = self.s
        o = s.sc('#fgOpen', 'mb') or 0
        brk = s.sc('#fgBrk', 'mb') or 0
        if o == 1 and self.prev_open != 1:
            b = body_of(s)
            self.cur = dict(open=s.t, close=None, broke=False, counts=[], hp=(s.sc(('e', b.id), 'mhpC') if b else None))
            self.fields.append(self.cur)
        if self.cur is not None and brk > self.prev_brk:
            self.cur['counts'].append(s.t)
        if o != 1 and self.prev_open == 1 and self.cur is not None:
            self.cur['close'] = s.t
            self.cur['broke'] = (s.sc('#fgSt', 'mb') or 0) == 6
            self.cur = None
        if (s.sc('#fq21T', 'mb') or 0) == 1 and (not self.tri or self.tri[-1] < s.t - 200):
            self.tri.append(s.t)
        if self.dead_t is None and (s.sc('#mbSt', 'mb') or 0) in (2, 3) and s.t > 200:
            self.dead_t = s.t
        self.prev_open, self.prev_brk = o, brk


def fight(force=3, policy='melee', dodge='walk', react=5, n=3600, seed=1018, level=4, char='sword', sprint=False,
          iframes=DASH_IF, real_hp=False, until_dead=False, jump_waves=True, hit_boss=True, tri_aware=True):
    s, zone, player = new_sim(force=force, level=level, seed=seed, real_hp=real_hp)
    G.press_gate(s, zone)
    for _ in range(400):
        world(s)
        if (s.sc('#mbSt', 'mb') or 0) == 1:
            break
    ag = Agent(s, player, policy, dodge, react, char, sprint, iframes, jump_waves, hit_boss, tri_aware)
    tr = Track(s)
    t0 = s.t
    s.dmg.clear()
    for _ in range(n):
        ag.step()
        world(s)
        tr.tick()
        if until_dead and tr.dead_t is not None:
            break
    return s, ag, tr, t0
