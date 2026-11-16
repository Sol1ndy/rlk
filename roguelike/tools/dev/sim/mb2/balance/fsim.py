#!/usr/bin/env python3
"""Fairness fight simulator (review scratch, read-only on the datapack copy).

mcsim runs the real mid-boss datapack (butterfly: bfsim harness; Guardian: the same harness with its rig calls logged).
The player hit path is the REAL one (cm/hit_pl2 -> player/take_damage: level scaling, defence, element reactions on
the player incl. Burning, dash i-frames via dashInvT); only the HUD / sound / item / knockback-entity side is stubbed.
A scripted agent moves the player every tick before the world tick (walk 0.216 b/t, sprint 0.281, swing slow 0.108,
jump arc, dash 3 b in 3 t with 2 charges / 20 t regen / 5 t cooldown and IF ticks of i-frames) and reacts to the
hazards it can see (hz markers, B2 landing markers, B4 orbs, the H4 blade, generic pj props) after REACT ticks.
"""
import math
import sys
from pathlib import Path

TESTS = '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/mb2/tests'
sys.path.insert(0, TESTS)
import bfsim as B  # noqa: E402
from mcsim import Ent, Ctx  # noqa: E402

import os
DP = os.environ.get('FDP', '/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/mb2/review/fairness/dp')
A = B.init(DP)
C0 = B.C0
CX, CY, CZ = A.CX, A.CY, A.CZ
WALK_R = 20.7                     # the player's feet stay inside r 20.7 (wall ring at r 21)
WALK, SPRINT, SWING = 0.2159, 0.2807, 0.10795
# [balance copy] H4's blade reach off its line: hr 1.2 + 0.65 = 1.85 before the review fixes, hr 1.5 + 0.3 = 1.8 after
BLADE_REACH = 1.8 if 'FW-1' in (Path(DP) / 'tools/build_mboss_core.py').read_text(encoding='utf-8') else 1.85


def jump_heights():
    y, v, out = 0.0, 0.42, []
    while True:
        y += v
        v = (v - 0.08) * 0.98
        if y <= 0:
            break
        out.append(y)
    return out


JUMP = jump_heights()             # feet height on ticks 1.. after the press (vanilla 0.42 jump)


class FSim(B.BSim):
    def __init__(self, root):
        super().__init__(root)
        self.hzrec = {}           # hz marker id -> dict (creation tick, pattern, clock, scores, pos, player pos)
        self.pjrec = {}
        self.iframe_end = -1      # last tick of dash i-frames
        self.dodges = []          # (t, pct)
        self.dmg = []             # (t, pct, el, hp_lost, pattern, form)
        self.kb = None            # (dirx, dirz, steps_left)
        self.agent = None

    def call(self, fid, ctx, macro=None):
        if fid.startswith('rlk:mboss/guardian/rig/'):
            sub = fid[len('rlk:mboss/guardian/rig/'):]
            self.rig.append((self.t, 'gd/' + sub))
            if sub == 'prop/spear':
                for e in self.ents:
                    e.tags.discard('rlk_mb_gd_prop_new')
                self.ents.append(Ent('item_display', ctx.pos, (ctx.rot[0], 0.0),
                                     ['rlk_room', 'rlk_mb_aux', 'rlk_mb_gd_prop', 'rlk_mb_gd_prop_new']))
            return 1
        if fid == 'rlk:cm/hit_pl2':
            pl = self.agent.player if self.agent else None
            if pl is not None:
                self.setsc(('e', pl.id), 'dashInvT', 1 if self.t <= self.iframe_end else 0)
                self.setsc('#hurtDmg', 'tmp', 0)
            pct, el = self.sc('#mbHitPct', 'mb'), self.sc('#cmEl', 'tmp')
            r = super().call(fid, ctx, macro)
            if pl is not None:
                if (self.sc('#dodged', 'tmp') or 0) == 1:
                    self.dodges.append((self.t, pct))
                    if self.hits and self.hits[-1][0] == self.t:
                        self.hits.pop()
                else:
                    lost = self.sc('#hurtDmg', 'tmp') or 0
                    self.dmg.append((self.t, pct, el, lost, self.sc('#bfPat', 'mb') or self.sc('#gdPat', 'mb') or 0,
                                     self.sc('#bfForm', 'mb')))
                    src = self.select('@e[tag=rlk_plkb_source,limit=1]', C0)
                    k = self.sc('#cmKB', 'tmp') or 0
                    if src and k > 0:
                        yaw = math.radians(src[0].rot[0])
                        self.kb = (-math.sin(yaw), math.cos(yaw), k)
                self.setsc(('e', pl.id), 'dashInvT', 0)
                self.agent.check_death()
            return r
        if fid == 'rlk:mboss/butterfly/coc/apply_pl' and self.agent:
            pl = self.agent.player
            hp0 = self.sc(('e', pl.id), 'curHealth')
            r = super().call(fid, ctx, macro)
            self.dmg.append((self.t, 0, 'coc', hp0 - self.sc(('e', pl.id), 'curHealth'), 20, 1))
            return r
        if fid == 'rlk:player/heal' and self.agent:
            pl = self.agent.player
            hp0 = self.sc(('e', pl.id), 'curHealth')
            r = super().call(fid, ctx, macro)
            self.agent.stats.setdefault('heals', []).append((self.t, self.sc(('e', pl.id), 'curHealth') - hp0))
            return r
        r = super().call(fid, ctx, macro)
        if fid == 'rlk:mboss/hz/init' and ctx.ex is not None:
            e = ctx.ex
            g = lambda o: self.sc(('e', e.id), o)  # noqa: E731
            pl = self.agent.player if self.agent else None
            rec = dict(t=self.t, pat=self.sc('#bfPat', 'mb') or self.sc('#gdPat', 'mb') or 0, clock=self.sc('#bfPT', 'mb'),
                       K=g('mbHzK'), W=g('mbHzW'), D=g('mbHzD'), A=g('mbHzA'), Y1=g('mbHzY1'), R=g('mbHzR'),
                       pos=tuple(e.pos), ppos=tuple(pl.pos) if pl else None, form=self.sc('#bfForm', 'mb'),
                       atkcd=self.agent.atkcd if self.agent else 0)
            if pl is not None and (rec['D'] or 0) > 0:
                rec['inside'] = hz_inside(self, e, pl.pos[0], CY, pl.pos[2])
                rec['esc'] = esc_single(self, e, pl.pos[0], pl.pos[2]) if rec['inside'] else 0.0
            self.hzrec[e.id] = rec
        return r


STUB_EXTRA = {
    'rlk:items/proc/taken': [], 'rlk:engravings/guard/absorb': [], 'rlk:element/shield_absorb': [],
    'rlk:player/knockback/start': [], 'rlk:cm/hurt_fx': [], 'rlk:items/proc/lion_queue': [],
    'rlk:engravings/berserk/taken': [], 'rlk:element/display': [], 'rlk:element/set_icon': [],
    'rlk:element/infuse_end': [],
}


def new_sim(force=2, level=4, seed=1018):
    """A fight world (force 2 butterfly, 1 Guardian) with an item-less player of `level` (HP 100+12(L-1), def 10+2(L-1))."""
    B.SEED[0] = seed
    B.BSim.__init__  # noqa
    orig = B.BSim
    B.BSim = FSim
    try:
        s, zone, player = B.setup(force=force)
    finally:
        B.BSim = orig
    for k, v in B.STUBS.items():
        s.cache[k] = list(v)
    s.cache.pop('rlk:cm/hit_pl2', None)          # the real hit path
    for k, v in STUB_EXTRA.items():
        s.cache[k] = list(v)
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
    """bfsim.world + the player's element tick (Burning DoT on the player)."""
    B.world(s)
    pl = s.agent.player if s.agent else None
    if pl is not None and (s.sc(('e', pl.id), 'elAct') or 0) >= 1:
        s.setsc('#hurtDmg', 'tmp', 0)
        s.setsc(('e', pl.id), 'dashInvT', 1 if s.t <= s.iframe_end else 0)
        s.call('rlk:player/elem_tick', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        s.setsc(('e', pl.id), 'dashInvT', 0)
        lost = s.sc('#hurtDmg', 'tmp') or 0
        if lost > 0:
            s.dmg.append((s.t, 0, 'dot', lost, s.sc('#bfPat', 'mb') or 0, s.sc('#bfForm', 'mb')))
        s.agent.check_death()


def body_of(s):
    return B.body_of(s)


# ------------------------------------------------------------------------------------------- threats
def hz_inside(s, e, x, y, z, pad=0.0):
    """The framework hz/hit test (the 0.3 body pad is in the stored bounds) with an extra safety pad (blocks)."""
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
    if ang >= 180:
        return True
    a = math.degrees(math.atan2(-(dx * FZ - dz * FX), fwd)) if (dx or dz) else 0.0
    # angle between d and forward
    if dx == 0 and dz == 0:
        return True
    cosang = fwd / math.sqrt(r2)
    return math.degrees(math.acos(max(-1, min(1, cosang)))) <= ang + (math.degrees(pad / max(0.5, math.sqrt(r2) / 1000)) if pad else 0)


def esc_single(s, e, x0, z0):
    """Shortest straight walk (blocks, 0.05 steps, 72 directions, inside the walk disc) out of one hazard."""
    best = 99.0
    for i in range(72):
        a = 2 * math.pi * i / 72
        d = 0.0
        while d < 25:
            d += 0.05
            x, z = x0 + d * math.cos(a), z0 + d * math.sin(a)
            if math.hypot(x - CX, z - CZ) > WALK_R:
                break
            if not hz_inside(s, e, x, CY, z):
                best = min(best, d)
                break
    return best


class Threat:
    """A region test fn(x, y, z, pad) and the hit window [k1, k2] in world ticks from now (1 = the coming tick)."""

    def __init__(self, kind, fn, k1, k2, seen, src=None, jumpable=False, dmg=0):
        self.kind, self.fn, self.k1, self.k2, self.seen, self.src = kind, fn, k1, k2, seen, src
        self.jumpable, self.dmg = jumpable, dmg


def threats(s, now, react):
    """Every damaging thing the player can see (created >= react ticks ago) with its hit window."""
    out = []
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
            if g('mbHzHit') or D <= 0:
                # H4: the blade lane telegraph (dmg 0) stands for the blade (handled below once the blade flies)
                if D <= 0 and rec and rec['pat'] == 4 and g('mbHzK') == 4 and not s.select('@e[tag=rlk_mb_bf_p4b,limit=1]', C0):
                    ee = e
                    out.append(Threat('h4lane', lambda x, y, z, pad, ee=ee: lane_test(s, ee, x, z, BLADE_REACH + pad), 8 - T, 8 - T + 30,
                                      seen, ee, False, 120))
                continue
            k1, k2 = W - T, W + Aa - 1 - T
            if k2 < 1:
                continue
            ee = e
            out.append(Threat('hz', lambda x, y, z, pad, ee=ee: hz_inside(s, ee, x, y, z, pad), max(1, k1), k2, seen, ee,
                              g('mbHzY1') <= 1100, D))
        elif 'rlk_mb_bf_p12t' in e.tags:
            # B2 landing marker i: its crescent lands at swing + 14 + i (decal from the swing)
            # [balance copy] per-swing tags since the review fix F1: marker p12t<swing><i>, crescent p12c<swing><i>
            import re as _re
            tg = next((t for t in e.tags if _re.fullmatch(r'rlk_mb_bf_p12t\d\d?', t)), None)
            if tg is None:
                continue
            i = int(tg[-1])
            c = s.select(f'@e[type=minecraft:item_display,tag=rlk_mb_bf_p12c{tg[len("rlk_mb_bf_p12t"):]},limit=1]', C0)
            if c and (s.sc(('e', c[0].id), 'mbPjHit') or 0):
                continue
            born = s.pjrec.setdefault(('b2', e.id), now)
            if now - born < react:
                continue
            # [balance copy] the landing clock is on the marker (mbT, review fix F1: the dive time scales with the
            # distance); before the fix the landing was swing + 14 + i
            mt = s.sc(('e', e.id), 'mbT')
            k = (mt - (s.sc('#bfPT', 'mb') or 0)) if mt is not None else born + 14 + i - now
            if k < 1:
                continue
            ee = e
            out.append(Threat('b2', lambda x, y, z, pad, ee=ee: math.sqrt((x - ee.pos[0]) ** 2 + (z - ee.pos[2]) ** 2 + (y - CY) ** 2) <= 1.5 + pad,
                              k, k, born, ee, True, 50))
        elif 'rlk_mb_bf_p14o' in e.tags and 'rlk_mb_pj' in e.tags:
            g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
            if g('mbPjHit') or g('mbPjD') <= 0 or g('mbT') >= 40:
                continue
            ee = e
            out.append(Threat('orb', lambda x, y, z, pad, ee=ee: math.dist((x, y, z), (ee.pos[0], ee.pos[1] - 0.9, ee.pos[2])) <= 1.1 + pad,
                              1, 2, now, ee, False, 150))
        elif 'rlk_mb_bf_p4b' in e.tags and 'rlk_mb_pj' in e.tags:
            g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
            if g('mbPjHit') or g('mbPjD') <= 0:
                continue
            ee = e
            out.append(Threat('blade', lambda x, y, z, pad, ee=ee: blade_test(ee, x, z, pad), 1, 3, now, ee, False, 120))
        elif 'rlk_mb_pj' in e.tags and 'rlk_mb_gd_prop' not in e.tags or ('rlk_mb_pj' in e.tags and 'rlk_mb_gd_prop' in e.tags):
            g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
            if any(t.startswith('rlk_mb_bf_') for t in e.tags) or g('mbPjHit') or g('mbPjD') <= 0:
                continue
            ee = e
            out.append(Threat('pj', lambda x, y, z, pad, ee=ee: pj_test(s, ee, x, y, z, pad), 1, 3, now, ee, False, g('mbPjD')))
    return out


def lane_test(s, e, x, z, half):
    g = lambda o: s.sc(('e', e.id), o) or 0  # noqa: E731
    FX, FZ = g('mbHzFX') / 1000, g('mbHzFZ') / 1000
    dx, dz = x - e.pos[0], z - e.pos[2]
    fwd = dx * FX + dz * FZ
    side = abs(dx * FZ - dz * FX)
    return fwd >= 0.5 and side <= half


def blade_test(e, x, z, pad):
    yaw = math.radians(e.rot[0])
    fx, fz = -math.sin(yaw), math.cos(yaw)
    dx, dz = x - e.pos[0], z - e.pos[2]
    fwd = dx * fx + dz * fz
    side = abs(dx * fz - dz * fx)
    return -0.5 <= fwd <= 8.0 and side <= BLADE_REACH + pad


def pj_test(s, e, x, y, z, pad):
    """Generic projectile: the next 3 ticks of straight flight (speed rounded up to 0.25 b), sphere hr+0.3 at 0.9 b
    under the prop (shape 0) or the blade line (shape 1)."""
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


# ------------------------------------------------------------------------------------------- the agent
class Agent:
    """policy: 'stand' (never moves or dodges), 'melee' (chase to 2.5 b, swing in 3.5 b), 'ranged' (keep 8-11 b, attack
    always), each with dodge in ('none', 'walk', 'dash'); react = ticks from a telegraph's first tick to the reaction;
    sprint = whether dodges may sprint (camera turned to the escape); iframes = dash i-frame ticks."""

    def __init__(self, s, player, policy='melee', dodge='dash', react=5, sprint=False, iframes=5, reach=3.5, dew=True):
        self.dew = dew
        self.s, self.player, self.policy, self.dodge, self.react = s, player, policy, dodge, react
        self.sprint, self.iframes, self.reach = sprint, iframes, reach
        s.agent = self
        self.charges, self.regen, self.cool = 2, 0, 0
        self.dash_left, self.dash_dir = 0, (0, 0)
        self.atkcd, self.combo = 0, 0
        self.jump_t = -1
        self.planned_dash = None      # (tick, dir)
        self.stats = dict(ticks=0, hittable=0, attack=0, attack_hittable=0, dodge_ticks=0, dashes=0, jumps=0,
                          inreach=0, eff=0.0, bf_ticks=0, bf_attack=0, h_ticks=0, h_attack=0, gr_ticks=0, gr_attack=0,
                          unavoid=[], walk_fail=[])
        self.last_threat_ids = set()
        self.nowalk_seen = set()

    def check_death(self):
        s, pl = self.s, self.player
        if (s.sc(('e', pl.id), 'curHealth') or 0) <= 0:
            self.stats.setdefault('deaths', []).append(s.t)
            s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))

    # -- helpers
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
        if (s.sc('#bfSt', 'mb') or 0) == 7:
            return False, b
        return True, b

    def speed(self, toward_boss=False):
        if self.atkcd > 0:
            return SWING
        if self.sprint or toward_boss:
            return SPRINT
        return WALK

    def safe_at(self, ths, x, z, y=0.0, pad=0.25):
        return not any(t.fn(x, CY + y, z, pad) for t in ths)

    def escape_point(self, ths, maxd=14.0):
        x0, z0 = self.pos()
        best = None
        for i in range(48):
            a = 2 * math.pi * i / 48
            for k in range(1, int(maxd / 0.25) + 1):
                d = k * 0.25
                x, z = self.clampw(x0 + d * math.cos(a), z0 + d * math.sin(a))
                if self.safe_at(ths, x, z):
                    # the straight path must not cross a hazard that strikes before we pass it: ignore (rare)
                    if best is None or d < best[0]:
                        best = (d, x, z)
                    break
        return best

    # -- one tick of the agent, BEFORE the world tick
    def step(self):
        s, pl = self.s, self.player
        now = s.t + 1                                # the coming world tick
        st = self.stats
        # timers
        if self.cool > 0:
            self.cool -= 1
        if self.charges < 2:
            self.regen += 1
            if self.regen >= 20:
                self.charges += 1
                self.regen = 0
        if self.atkcd > 0:
            self.atkcd -= 1
        # knockback from the last hit
        if s.kb:
            dx, dz, k = s.kb
            x, z = self.clampw(pl.pos[0] + dx * 0.1 * k, pl.pos[2] + dz * 0.1 * k)
            pl.pos[0], pl.pos[2] = x, z
            s.kb = (dx, dz, k - 1) if k > 1 else None
        # dash movement
        if self.dash_left > 0:
            x, z = self.clampw(pl.pos[0] + self.dash_dir[0], pl.pos[2] + self.dash_dir[1])
            pl.pos[0], pl.pos[2] = x, z
            self.dash_left -= 1
        # jump arc
        y = 0.0
        if self.jump_t >= 0:
            self.jump_t += 1
            if self.jump_t <= len(JUMP):
                y = JUMP[self.jump_t - 1]
            else:
                self.jump_t = -1
        pl.pos[1] = CY + y
        ok, b = self.hittable()
        st['ticks'] += 1
        form = s.sc('#bfForm', 'mb')
        groggy = (s.sc('#bfSt', 'mb') or 0) in (3, 4)
        if ok:
            st['hittable'] += 1
        # threats
        ths = [] if self.dodge == 'none' else threats(s, now, self.react)
        x0, z0 = self.pos()
        cur = [t for t in ths if t.fn(x0, CY + y, z0, 0.15) and t.k1 <= 40]
        moved = False
        attacking = False
        # B4 orbs (homing, faster than a walk): a dasher dashes THROUGH an orb that is about to touch (the dodged contact
        # pops it); a walker back-pedals straight away from it (b4_orb.py: the only walking answer)
        if self.dodge != 'none' and self.dash_left == 0:
            for t in ths:
                if t.kind != 'orb':
                    continue
                o = t.src
                hp_ = (o.pos[0], o.pos[1] - 0.9, o.pos[2])
                dist = math.dist((x0, CY + y, z0), hp_)
                if dist <= 1.1 + 0.6 and self.dodge == 'dash' and self.charges > 0 and self.cool == 0:
                    dd = math.hypot(hp_[0] - x0, hp_[2] - z0) or 1
                    self.do_dash(((hp_[0] - x0) / dd, (hp_[2] - z0) / dd))
                    break
        if self.planned_dash and self.planned_dash[0] <= now:
            self.do_dash(self.planned_dash[1])
            self.planned_dash = None
        if cur and self.dash_left == 0:
            st['dodge_ticks'] += 1
            kmin = min(t.k1 for t in cur)
            esc = self.escape_point([t for t in ths if t.k1 <= 40])
            v = SPRINT if self.sprint and self.atkcd == 0 else (SWING if self.atkcd > 0 else WALK)
            # distance coverable by the hit tick (walking; the swing slow lasts while atkcd > 0)
            cover, cd = 0.0, self.atkcd
            for k in range(kmin):
                cover += SWING if cd > 0 else (SPRINT if self.sprint else WALK)
                cd -= 1
            if esc and esc[0] > cover + 1e-6:
                for t in cur:
                    key = t.src.id if t.src else 0
                    if key not in self.nowalk_seen:
                        self.nowalk_seen.add(key)
                        st.setdefault('nowalk', []).append((now, t.kind, t.dmg, round(esc[0], 2), round(cover, 2), kmin,
                                                            self.atkcd, s.sc('#bfPat', 'mb') or s.sc('#gdPat', 'mb') or 0))
            if esc and esc[0] <= cover + 1e-6:
                self.walk_to(esc[1], esc[2], v)
                moved = True
            elif esc and self.dodge == 'dash' and self.charges > 0 and self.cool == 0:
                # dash toward the escape point; if the dash itself cannot reach it, time the i-frames on the window
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
                        st['unavoid'].append((now, [(t.kind, t.dmg, t.src.id if t.src else 0) for t in cur], k1, k2,
                                              s.sc('#bfPat', 'mb') or s.sc('#gdPat', 'mb') or 0))
                        self.walk_to(esc[1], esc[2], v)
                else:
                    self.walk_to(esc[1], esc[2], v)
                moved = True
            else:
                # jump if every current threat is jumpable and we are not swinging
                if all(t.jumpable for t in cur) and self.jump_t < 0 and self.dodge != 'none' and \
                        min(t.k1 for t in cur) >= 3 and max(t.k2 for t in cur) - min(t.k1 for t in cur) <= 5:
                    k1 = min(t.k1 for t in cur)
                    # press so that feet >= 1.0 b over [k1, k2]: heights >= 1.0 on jump ticks 3..8 (no jump while swinging)
                    if k1 == 3 and self.atkcd == 0:
                        self.jump_t = 0
                        st['jumps'] += 1
                    elif esc:
                        self.walk_to(esc[1], esc[2], v)
                elif esc:
                    st['walk_fail'].append((now, [(t.kind, t.dmg, t.src.id if t.src else 0) for t in cur], round(esc[0], 2), round(cover, 2),
                                            s.sc('#bfPat', 'mb') or s.sc('#gdPat', 'mb') or 0))
                    self.walk_to(esc[1], esc[2], v)
                moved = True
        dews = [e for e in s.ents if e.alive and 'rlk_mb_bf_dew' in e.tags and e.etype.endswith('item_display')] \
            if self.dew and self.policy != 'stand' and (s.sc('#bfCoc', 'mb') or 0) == 1 else []
        if not moved and self.dash_left == 0 and dews and not [t for t in ths if t.k1 <= 25]:
            dd = min(dews, key=lambda e: math.hypot(e.pos[0] - x0, e.pos[2] - z0))
            self.walk_to(dd.pos[0], dd.pos[2], SPRINT if self.atkcd == 0 else SWING)
            moved = True
            st['dew_ticks'] = st.get('dew_ticks', 0) + 1
        if not moved and self.dash_left == 0 and b is not None and self.policy != 'stand':
            bx, bz = b.pos[0], b.pos[2]
            d = math.hypot(bx - x0, bz - z0)
            soon = [t for t in ths if t.k1 <= 25]
            if self.policy == 'melee':
                want = 2.5
                if d > want:
                    v = SPRINT if self.atkcd == 0 else SWING
                    step = min(v, d - want)
                    nx, nz = self.clampw(x0 + (bx - x0) / d * step, z0 + (bz - z0) / d * step)
                    if self.safe_at(soon, nx, nz, pad=0.3):
                        pl.pos[0], pl.pos[2] = nx, nz
            elif self.policy == 'wall':
                # hug the wall ring (r 19.5): slide along it to keep 8-11 b from her
                r0 = math.hypot(x0 - CX, z0 - CZ)
                if r0 < 19.3:
                    tx, tz = CX + (x0 - CX) / max(r0, 1e-6) * 19.5, CZ + (z0 - CZ) / max(r0, 1e-6) * 19.5
                    if r0 < 1e-3:
                        tx, tz = CX, CZ + 19.5
                    nx, nz = self.clampw(x0 + (tx - x0) / math.hypot(tx - x0, tz - z0) * WALK, z0 + (tz - z0) / math.hypot(tx - x0, tz - z0) * WALK)
                    if self.safe_at(soon, nx, nz, pad=0.3):
                        pl.pos[0], pl.pos[2] = nx, nz
                elif d < 8.0 or d > 11.0:
                    a0 = math.atan2(z0 - CZ, x0 - CX)
                    best = None
                    for da in (-0.012, 0.012):
                        a = a0 + da
                        nx, nz = CX + 19.5 * math.cos(a), CZ + 19.5 * math.sin(a)
                        nd = math.hypot(bx - nx, bz - nz)
                        sc = abs(nd - 9.5)
                        if best is None or sc < best[0]:
                            best = (sc, nx, nz)
                    if self.safe_at(soon, best[1], best[2], pad=0.3):
                        pl.pos[0], pl.pos[2] = best[1], best[2]
            elif self.policy == 'ranged':
                if d < 8.0 or d > 11.0:
                    sgn = -1 if d < 8.0 else 1
                    v = SWING if self.atkcd > 0 else WALK
                    nx, nz = self.clampw(x0 + (bx - x0) / d * v * sgn, z0 + (bz - z0) / d * v * sgn)
                    if math.hypot(nx - x0, nz - z0) < 0.05 and sgn < 0:     # cornered at the wall: slide sideways
                        tx, tz = -(bz - z0) / d, (bx - x0) / d
                        nx, nz = self.clampw(x0 + tx * v, z0 + tz * v)
                    if self.safe_at(soon, nx, nz, pad=0.3):
                        pl.pos[0], pl.pos[2] = nx, nz
        # attack decision (after moving): melee needs reach; ranged always (in the fight)
        x1, z1 = self.pos()
        if b is not None and self.policy != 'stand' and not cur:
            d = math.hypot(b.pos[0] - x1, b.pos[2] - z1)
            inreach = d <= self.reach if self.policy == 'melee' else d <= 30
            if inreach:
                st['inreach'] += 1
            if inreach and ok:
                attacking = True
        if attacking:
            if self.atkcd == 0:
                self.combo ^= 1
                self.atkcd = 6 if self.combo else 10
            st['attack'] += 1
            mul = 0.5 if (s.sc('#bfCoc', 'mb') or 0) else (1.5 if (s.sc('#bfBuff', 'mb') or 0) else 1.0)
            st['eff'] += mul
            if form == 2:
                st['bf_attack'] += 1
            elif groggy:
                st['gr_attack'] += 1
            else:
                st['h_attack'] += 1
        if ok:
            if form == 2:
                st['bf_ticks'] += 1
            elif groggy:
                st['gr_ticks'] += 1
            else:
                st['h_ticks'] += 1
        # the i-frame state the real take_damage reads
        s.iframe_end = max(s.iframe_end, -1)

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
        s.iframe_end = s.t + 1 + self.iframes - 1      # hits on ticks now .. now + IF - 1
        self.stats['dashes'] += 1
        # the first dash step happens this tick
        x, z = self.clampw(self.player.pos[0] + direction[0], self.player.pos[2] + direction[1])
        self.player.pos[0], self.player.pos[2] = x, z
        self.dash_left = 2
        return True


def fight(force=2, policy='melee', dodge='dash', react=5, n=3600, seed=1018, level=4, sprint=False, iframes=5, dew=True, reach=3.5):
    s, zone, player = new_sim(force=force, level=level, seed=seed)
    B.press_gate(s, zone)
    for _ in range(400):
        world(s)
        if (s.sc('#mbSt', 'mb') or 0) == 1:
            break
    ag = Agent(s, player, policy, dodge, react, sprint, iframes, reach, dew)
    t0 = s.t
    s.dmg.clear()
    for _ in range(n):
        ag.step()
        world(s)
    return s, ag, t0
