"""Phase-2 patterns of 아를레키노 → 「두 세계 불의 잔재」 페르엘 (PLAN §6; OWNER: S4): Q0 낙하 공격, Q1 사형장으로의 초대,
Q2 불꽃이 타오르는 낫, Q3 붉은 죽음의 무도회, Q4 떠오르는 재액의 달, Q5 붉은 피의 연회 (q5a 형벌의 핏값 / q5b 붉은 피의
사형), Q6 핏빛 연회 (footage sheets S:ar/ref/p2_*.jpg).

Contract (api.Pattern, contract §3.4): PATTERNS = [api.Pattern(key, tid, clips, build) for key in api.P2]; build(W) writes only
p/<key>/** (W = api.Writer('S4', api.OWN['S4'])); every hit tick comes from api.ev, every shape / tier / Bond-of-Life flag
from api.HITS with api.dmg(tier, 2), dash lengths from api.DASH_LEN, heights from api.LEAP_H; Bond-of-Life hits through the
FN-1 option (s3lib.hazard / bol_opts; the documented #bolw stand-in while S1's mboss_lib lacks it); forced bonds only through
api.BOND_CALLS['force'] (S3's bond/force drops the heal orbs itself: bond/orbs is not called a second time).

Runtime (all @s = the body, at it): each pattern is a small stage machine - p/<key>/start (#pt kn 0), p/<key>/tick, the
stages p/<key>/s/<stage>/{go,tick,k/<t>} with the stage clock #<key>_c kn (0 at the stage's go, +1 each tick; the stage's
rig clip is played at its go, so the stage clock == the shown clip tick) and the stage index #<key>_s kn. One-stage patterns
(q2, q5a, q5b, q6) have #<key>_c == #pt == the clip tick, so the core's break windows of q5a / q5b (api.BREAK_WINDOWS on
#pt) line up. A hit of clip event e is a quiet hazard made at stage tick e - 1 with tell 1 (strikes at e), except the Q6
feathers (made at the volley with tell FEATHER_T: they strike where the visible feather lands) and the projectiles (pj).
p/<key>/cancel (idempotent) kills every hazard / marker / prop of the pattern (rlk_kn_p_<key>, the shared lock / probe
markers), stops the glide, puts her back on the floor (core/ground) with the rest looks; p/<key>/fin is the normal end
(#done 1, leftovers gone). p/<key>/pj_end handles the crescent / wheel events; p/<key>/resume re-dresses the kit props and
redraws the Q5A decals with the ticks left (only with the kit: without it the stand-in props keep their items).

The user's lessons are built in: the melee strings re-face and step in before every swing (a standing player takes the whole
string) and only the last hit of a cast knocks back (api.KB_CHAIN / KB_FINAL); a Q1 from mid range opens with a gliding
lunge to 2.4 b in front of the player (melee only from where it reaches); Q2 (the far rule's gap closer) dashes to 1.5 b in
front of the player and skips its slash when the player is still out of reach; dives (Q0, Q6) land 1.5 b in front of the
locked spot (core/lock_short); the rises go up, act and come down (Q4: rise 20 t, shots 50 t apart, land 16 t; Q0's 80 t
far hover and Q6's feast are PLAN §6); one display per projectile, facing its flight (the kit dresses it; stand-in items
otherwise); floor decals only Q5A's ring_o / donut_o (api.DECALS), every other hazard is quiet and read from the pose, the
crimson glow, the props and the sounds; no text. Every end point (hover, dive, dash, lunge, landing) passes mv/ok (inside
the safe disc - 0.5 b < api.MOVE_R, free feet and head); heights <= api.AIR_MAX; P2 patterns never set rlk_mb_inv.

TABLE[key] = the recorded hits (stage, stage tick, HITS key / index, tell start, volley group, knockback, bol) for the tests
(S:ar/tests/pat_p2.py).
"""
from collections import defaultdict

from . import api
from . import s3lib as S
from .s3lib import sset, fn, num, part, placed

E = api.ev
OBJ, CY, NS = api.OBJ, api.CY, api.NS
L, K = api.L, api.K
PH = 2                                   # the fight phase of every hit here (api.dmg(tier, 2))
KB0, KB1 = api.KB_CHAIN, api.KB_FINAL
PY_C, BOL_C = api.C_PYRO, api.C_BOL
FACE = 'function rlk:mboss/mv/face'
BODY, PLAYER, LOCK_M, ARENA_M, AT_BODY = S.BODY, S.PLAYER, S.LOCK_M, S.ARENA_M, S.AT_BODY
ANCHOR = f'@e[type=minecraft:marker,tag={api.TAGS["anchor"]},limit=1]'
DP = '@e[type=minecraft:marker,tag=rlk_kn_dp,limit=1]'
OK = 'function rlk:mboss/mv/ok'
STEP, STOP = 0.3, 2.6                    # step-in per tick / stop distance before a swing (her reach >= 4.2; as P1)
LOCK, LOCK1 = S.LOCK, S.LOCK_FIRST       # aim locks 6 t before a follow-up, 8 t before the first hit
LUNGE_AT, LUNGE_TO, LUNGE_T = 4.5, 2.4, 10   # Q1 / Q3 cut: a lunge when the player is beyond 4.5 b, to 2.4 b in front
CUT_Q1 = 7.0                             # Q1 stops after h3 / h5 when the player is farther (PLAN §6)
CUT_Q3 = 6.0                             # Q3: player <= 6 b -> Q1 h1-h3, else two crescents
Q3_SPREAD = 6                            # ... at +-6 deg: both pass within reach of a standing player out to their 12 b range
CRES_H = 1.2                             # crescent / wheel flight height over the floor (the P1 wheel's)
WHEEL_LIFE = 10                          # Q2 wheel: at most 10 t (15 b): the burst strikes <= 32, >= 10 t before the slash
FEATHER_T = 14                           # Q6: a feather is visible this long before it lands (PLAN: >= 14 t)
Q6_HOVER = (0.0, -10.0)                  # Q6 hover point (dx, dz from the axis): over the north half (-z)
Q4_SPOT = (12.0, 10.0, 8.0)              # Q4: she backs off to 10-14 b from the player (12 first)
Q0_SPOT = (14.0, 11.0, 8.0)              # Q0: 14 b from the player (PLAN)
SLASH_REACH = 6.0                        # Q2: the slash only when the player is this close to the dash end
HOLD_MAX = 30                            # crescents in flight: the cast waits at most this long for their return
TABLE = {}

# Vanilla stand-ins of the kit's P2 sound recipes (api.KIT_SOUNDS) while S1K's kit is missing (s3lib has the P1 ones).
SND2 = {
    'beam_aim': [('block.respawn_anchor.charge', 0.6, 1.6), ('block.beacon.power_select', 0.4, 1.8)],
    'beam_fire': [('entity.warden.sonic_boom', 0.7, 1.3), ('entity.wither.shoot', 0.6, 0.7)],
    'x_carve': [('entity.player.attack.sweep', 1.0, 0.5), ('entity.wither.shoot', 0.4, 0.6)],
    'rapid': [('entity.player.attack.sweep', 0.7, 1.4)],
    'final': [('entity.generic.explode', 1.0, 0.6), ('entity.wither.break_block', 0.6, 0.8)],
    'feather': [('item.trident.throw', 0.5, 1.5), ('entity.phantom.flap', 0.3, 1.8)],
    'orbs_gather': [('block.respawn_anchor.charge', 0.8, 0.8), ('block.beacon.ambient', 0.6, 1.4)],
    'orbs_toss': [('entity.blaze.shoot', 0.8, 0.6)],
    'orb_burst': [('entity.generic.explode', 0.9, 0.9)],
    'fall_dive': [('entity.phantom.swoop', 1.0, 0.7), ('item.firecharge.use', 0.5, 0.6)],
    'fall_impact': [('entity.generic.explode', 1.0, 0.8), ('block.anvil.land', 0.5, 0.5)],
    'rear_whip': [('entity.player.attack.sweep', 1.0, 0.8), ('entity.phantom.flap', 0.6, 1.2)],
    'crescent_throw': [('item.trident.throw', 1.0, 1.0), ('entity.player.attack.sweep', 0.6, 1.4)],
    'moon': [('block.beacon.activate', 0.8, 0.5)],
}


def snd(name, pos='at @s'):
    k = K.snd(name)
    if k:
        return placed([k], pos)
    rec = S.SND_FALLBACK.get(name) or SND2[name]
    return placed([L.sound(e, v, p) for e, v, p in rec], pos)


def look(ch, v):
    return api.rig(f'look/{ch}/{v}')


def tagn(key, *more):
    return S.tags_nbt(key, *more)


def p_of(key, tag):
    """The pattern's entities of one kind tag."""
    return f'@e[tag={S.tag_p(key)},tag={tag}]'


def floor_y(dy=0.0):
    return num(CY + dy)


def at_floor(sel):
    return f'at {sel} positioned ~ {CY} ~'


# ------------------------------------------------------------------------------------------------- props
_ROT0 = 'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f]'
_FLAT = 'left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f]'
STAND_IN = {'crescent': ('minecraft:netherite_hoe', (1.8, 1.8, 1.8), _FLAT),
            'wheel': ('minecraft:fire_charge', (2.2, 2.2, 0.2), _ROT0),
            'feather': ('minecraft:red_dye', (1.3, 1.3, 1.3), _ROT0),
            'orb': ('minecraft:redstone_block', (0.8, 0.8, 0.8), _ROT0)}


def prop_nbt(key, kind, *tags):
    """One item display per projectile / prop (the user's rule: exactly one card, facing its flight): the kit dresses it
    (fx/prop/<kind>, called right after the summon); the stand-in is the plain item."""
    t = tagn(key, *tags)
    if api.K._on():
        return f'{{Tags:{t},teleport_duration:1}}'
    item, sc, rot = STAND_IN[kind]
    return (f'{{Tags:{t},teleport_duration:1,brightness:{{sky:15,block:15}},item:{{id:"{item}",count:1}},'
            f'transformation:{{{rot},scale:[{sc[0]}f,{sc[1]}f,{sc[2]}f]}}}}')


def dress(kind, sel='@e[type=minecraft:item_display,tag=rlk_kn_new]'):
    k = K.prop(kind)
    return [f'execute as {sel} run {k}'] if k else []


# ------------------------------------------------------------------------------------------------- stage machine
class Stage:
    def __init__(self, sm, name, clip):
        self.sm, self.name, self.clip = sm, name, clip
        self.ev = defaultdict(list)
        self.rg = []
        self.trans = set()

    def at(self, t, *lines):
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                self.ev[t].extend(x for x in ln if x)
            elif ln:
                self.ev[t].append(ln)
        return self

    def rng(self, t0, t1, cmd):
        if t1 >= t0 and cmd:
            self.rg.append((t0, t1, cmd))
        return self

    def track(self, t0, t1, deg=10):
        """Turn toward the player by <= deg per tick on stage ticks t0..t1."""
        return self.rng(max(1, t0), t1, f'function rlk:mboss/mv/turn {{max:{int(deg)}}}')

    def advance(self, t0, t1, d, within):
        """Step d b forward per tick on t0..t1 while the player is farther than `within` and she is not gliding (mv/step:
        mv/ok)."""
        return self.rng(max(1, t0), t1, f'execute at @s[tag=!rlk_mb_mv] unless entity {PLAYER[:-1]},distance=..{num(within, 2)}] '
                                        f'run function rlk:mboss/mv/step {{d:{num(d, 3)}}}')

    def go(self, t, nxt, cond=None):
        """Go to stage nxt at tick t (the last thing of that tick; cond: an execute condition)."""
        line = fn(f'p/{self.sm.key}/s/{nxt}/go')
        self.at(t, S.gate(cond, f'return run {line}') if cond else line)
        self.trans.add(t)
        return self

    def end(self, t, cond=None):
        line = fn(f'p/{self.sm.key}/fin')
        self.at(t, S.gate(cond, f'return run {line}') if cond else line)
        self.trans.add(t)
        return self

    def group(self, t):
        self.at(t, L.GRP_NEW)
        self.sm.grp_n += 1
        return self.sm.grp_n

    def hit(self, hk, idx, tell, grp=0, kb=KB0, pos=None, dims=None, yaw=0, at=None, cond=None, tag=None):
        """The api.HITS[hk][idx] hazard, made at its event tick - 1 (tell 1) in this stage. tell = the stage tick of the
        first visible motion of this hit (or of the hit it follows). cond: an execute condition (variants)."""
        h = api.HITS[hk][idx]
        t = at if at is not None else E(h[0], h[1])
        assert t >= 1 and tell <= t, (hk, idx, t, tell)
        lines = S.hazard(self.sm.key, h, grp=bool(grp), kb=kb, pos=pos, dims=dims, yaw=yaw)
        if tag:
            lines.append(f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add {tag}')
        if cond:
            name = f'h/{self.name}_{t}_{len(self.sm.subs)}'
            self.at(t - 1, S.gate(cond, self.sm.sub(name, [f'# {self.sm.key.upper()} {self.name} hazard variant ({cond}).'] + lines)))
        else:
            self.at(t - 1, lines)
        if h[5]:
            self.at(t, [S.gate(cond, x) for x in S.bol_mark()] if cond else S.bol_mark())
        self.sm.hits.append(dict(stage=self.name, t=t, hk=hk, idx=idx, tell=tell, grp=grp, kb=kb, bol=h[5], shape=h[2],
                                 cond=cond))
        return t


class SM:
    """Stage machine of one P2 pattern: p/<key>/{start,tick,cancel,fin}, p/<key>/s/<stage>/{go,tick,k/<t>}, p/<key>/f/*."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.order = []
        self.stages = {}
        self.start = []
        self.cancel = []
        self.fin = []
        self.hits = []
        self.grp_n = 0
        self.subs = {}
        self.flags = set()

    def st(self, name, clip=None):
        if name not in self.stages:
            self.order.append(name)
            self.stages[name] = Stage(self, name, clip)
        return self.stages[name]

    def sub(self, name, lines):
        """A helper function p/<key>/f/<name>; returns its call line."""
        assert name not in self.subs, name
        self.subs[name] = lines
        return fn(f'p/{self.key}/f/{name}')

    def c(self):
        return f'#{self.key}_c'

    def s(self):
        return f'#{self.key}_s'

    def write(self):
        key, W, c, s = self.key, self.W, self.c(), self.s()
        name = api.PATTERN_NAMES[key]
        first = self.order[0]
        W.w(f'p/{key}/start', [f'# {key.upper()} {name} (S4, p2.py): pattern start (@s = the body, at it; #pt kn 0). Stages:',
                               '# ' + ' -> '.join(f'{n} ({self.stages[n].clip or "-"})' for n in self.order) + '.',
                               sset('#done', 0), sset(s, 0), sset(c, 0)] + self.start + [fn(f'p/{key}/s/{first}/go')])
        tick = [f'# {key.upper()} {name}: one tick (the stage machine: {s} kn = stage, {c} kn = its clock = the clip tick).',
                f'scoreboard players add {c} {OBJ} 1']
        for i, n in enumerate(self.order):
            tick.append(f'execute if score {s} {OBJ} matches {i + 1} run return run {fn(f"p/{key}/s/{n}/tick")}')
        W.w(f'p/{key}/tick', tick)
        for i, n in enumerate(self.order):
            st = self.stages[n]
            go = [f'# {key.upper()} stage {n}: tick 0 (@s = body){f", clip {st.clip}" if st.clip else ""}.', sset(s, i + 1), sset(c, 0)]
            if st.clip:
                go.append(api.play(st.clip))
            W.w(f'p/{key}/s/{n}/go', go + st.ev.get(0, []))
            tk = [f'# {key.upper()} stage {n}: one tick ({c} 1..).']
            for t0, t1, cmd in st.rg:
                rr = f'{t0}' if t0 == t1 else f'{t0}..{t1}'
                tk.append(S.gate(f'if score {c} {OBJ} matches {rr}', cmd))
            for t in sorted(k for k in st.ev if k >= 1):
                lines = st.ev[t]
                ret = 'return run ' if t in st.trans else ''
                if len(lines) == 1 and not ret and not lines[0].startswith('$'):
                    tk.append(S.gate(f'if score {c} {OBJ} matches {t}', lines[0]))
                else:
                    W.w(f'p/{key}/s/{n}/k/{t}', [f'# {key.upper()} stage {n} tick {t}'] + lines)
                    tk.append(f'execute if score {c} {OBJ} matches {t} run {ret}{fn(f"p/{key}/s/{n}/k/{t}")}')
            W.w(f'p/{key}/s/{n}/tick', tk)
        for nm, lines in self.subs.items():
            W.w(f'p/{key}/f/{nm}', lines)
        W.w(f'p/{key}/fin', [f'# {key.upper()} end (@s = body): its leftover props / markers gone, #done 1 (the core\'s recovery follows).',
                             f'kill @e[tag={S.tag_p(key)},tag=!rlk_mb_hz]', 'kill @e[type=minecraft:marker,tag=rlk_kn_dp]',
                             sset(s, 0)] + self.fin + [sset('#done', 1)])
        W.w(f'p/{key}/cancel', [f'# {key.upper()} cancel (any executor; idempotent): its hazards, markers and props, the shared lock /',
                                '# probe markers, the glide; she is back on the floor (inside mv/ok) with the rest looks.',
                                f'kill @e[tag={S.tag_p(key)}]',
                                'kill @e[type=minecraft:marker,tag=rlk_kn_lock]', 'kill @e[type=minecraft:marker,tag=rlk_kn_dp]',
                                'kill @e[type=minecraft:marker,tag=rlk_mb_lock]',
                                f'execute as {BODY[:-1]},tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
                                f'execute as {BODY} at @s run {fn("core/ground")}',
                                f'execute as {BODY} at @s run {fn("core/looks_rest")}',
                                sset(s, 0)] + self.cancel)
        TABLE[key] = self.hits
        return self


# ------------------------------------------------------------------------------------------------- shared pieces
def spot_fn(sm, name, origin, dists, angles, lift, glide_t, comment, tp=False):
    """p/<key>/f/<name> (@s = body): a spot `d` b from the player along player -> her (rotated by each angle), the floor spot
    there passing mv/ok (first of dists x angles), else the floor below her (mv/ok), else the arena centre; then a glide
    there (lift b up) over glide_t ticks (tp=True: placed at once)."""
    key = sm.key
    lines = [f'# {comment}', 'kill @e[type=minecraft:marker,tag=rlk_kn_dp]']
    for d in dists:
        for a in angles:
            lines.append(f'execute unless entity {DP} at {origin} facing entity @s feet rotated ~{a} 0 positioned ^ ^ ^{num(d)} '
                         f'positioned ~ {CY} ~ if {OK} run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_dp")}}}')
    lines += [f'execute unless entity {DP} at @s positioned ~ {CY} ~ if {OK} run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_dp")}}}',
              f'execute unless entity {DP} positioned as {ARENA_M} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ '
              f'{{Tags:{tagn(key, "rlk_kn_dp")}}}']
    if tp:
        lines.append(f'execute positioned as {DP} positioned ~ ~{num(lift)} ~ run tp @s ~ ~ ~')
    else:
        lines.append(f'execute positioned as {DP} positioned ~ ~{num(lift)} ~ run function rlk:mboss/mv/glide {{t:{int(glide_t)}}}')
    lines.append('kill @e[type=minecraft:marker,tag=rlk_kn_dp]')
    return sm.sub(name, lines)


def lunge_fn(sm):
    """p/<key>/f/lunge (@s = body): beyond LUNGE_AT b a gliding lunge to LUNGE_TO b in front of the player (on the player ->
    her line; else 3.5 / 1.5 b; mv/ok) over LUNGE_T ticks, with the dash trail; nearer: nothing."""
    key = sm.key
    if 'lunge' in sm.subs:
        return fn(f'p/{key}/f/lunge')
    lines = [f'# {key.upper()} lunge: the player beyond {num(LUNGE_AT)} b -> a {LUNGE_T} t glide to {num(LUNGE_TO)} b in front of them (on the',
             '# player -> her line, else turned 30 / 60 deg, else nearer; the spot passes mv/ok).',
             f'execute at @s if entity {PLAYER[:-1]},distance=..{num(LUNGE_AT)}] run return 0',
             'kill @e[type=minecraft:marker,tag=rlk_kn_dp]']
    for d in (LUNGE_TO, 3.5, 1.5):
        for a in (0, 30, -30, 60, -60):
            lines.append(f'execute unless entity {DP} at {PLAYER} facing entity @s feet rotated ~{a} 0 positioned ^ ^ ^{num(d)} '
                         f'positioned ~ {CY} ~ if {OK} run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_dp")}}}')
    lines += [f'execute unless entity {DP} run return 0',
              f'execute positioned as {DP} run function rlk:mboss/mv/glide {{t:{LUNGE_T}}}',
              'kill @e[type=minecraft:marker,tag=rlk_kn_dp]']
    lines += S.fx('dash_trail', [part(S.FLAME[1], 0.4, 0.5, 0.4, 0.06, 16)], pos=f'{AT_BODY} positioned ~ ~1 ~', len=60, c=PY_C)
    lines += snd('dash')
    return sm.sub('lunge', lines)


def crescents(sm, W, hk, hidx, spread=15):
    """The thrown crescents of api.HITS[hk][hidx] (pj_cres hr, speed, range): out from her chest height along her yaw (+ the
    given yaw offset), a blade-shaped projectile (shape 1), the wall stops it; at the end of the outward leg (wall / range)
    p/<key>/pj_end turns it into a returning crescent flying back to her (same volley group: one landing per throw), which
    vanishes when its leg ends. Returns ({(yaw offset, kb): call line}, life) for the single throw (0, KB0 / KB1) and the
    pair (+-spread, KB1)."""
    key = sm.key
    hr, spd, rng = api.HITS[hk][hidx][3]
    eff = (-(-int(round(spd * 100)) // 25)) * 0.25
    life = -(-int(round(rng * 100)) // int(round(eff * 100)))
    dmg = api.dmg(api.HITS[hk][hidx][4], PH)
    if 'cres_files' not in sm.flags:
        sm.flags.add('cres_files')
        for kb in (KB0, KB1):
            W.w(f'p/{key}/cres_out{kb}', [
                f'# @s = a new outward crescent (positioned / rotated as the throw): {hr} b half width, {spd} b/t, {life} t,',
                f'# wall stop, plain Pyro {api.HITS[hk][hidx][4]}, knockback {kb}, the group of #{key}_g.',
                'tag @s remove rlk_kn_new', 'tag @s add rlk_kn_out', f'scoreboard players operation #pjGrp mb = #{key}_g {OBJ}']
                + L.pj_opts(el=api.PYRO, kb=kb, wall=1, shape=1) + [L.pj_launch(spd, life, dmg, hr)] + dress('crescent', '@s'))
        W.w(f'p/{key}/pj_end', [
            f'# {key.upper()} crescent event (@s = the prop; #pjEv 1 wall, 2 range over, 4 hit the player: it flies on).',
            'execute unless score #pjEv mb matches 1..2 run return 0',
            f'execute if entity @s[tag=rlk_kn_out] run return run {fn(f"p/{key}/cres_turn")}'] + snd('wheel_catch'))
        W.w(f'p/{key}/cres_turn', [
            '# The outward crescent turns back (@s = it): a new returning crescent here, flying toward her for as many ticks',
            '# as the outward leg flew, in the same volley group (one landing per throw), no wall stop.',
            f'execute store result storage {api.STORAGE} p2.cr.life int 1 run scoreboard players get @s mbPjT',
            f'execute store result storage {api.STORAGE} p2.cr.g int 1 run scoreboard players get @s mbPjG',
            f'execute store result storage {api.STORAGE} p2.cr.kb int 1 run scoreboard players get @s mbPjB',
            f'execute at @s run summon minecraft:item_display ~ ~ ~ {prop_nbt(key, "crescent", "rlk_kn_cres", "rlk_kn_new")}',
            f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity {BODY} feet rotated ~ 0 run '
            f'{fn(f"p/{key}/cres_back")} with storage {api.STORAGE} p2.cr'])
        W.w(f'p/{key}/cres_back', [
            '# $(life) $(g) $(kb): the returning crescent (@s = the new prop, rotated toward her).',
            'tag @s remove rlk_kn_new', 'tag @s add rlk_kn_ret', '$scoreboard players set #pjGrp mb $(g)',
            '$scoreboard players set #pjKB mb $(kb)']
            + L.pj_opts(el=api.PYRO, wall=0, shape=1)
            + [f'$function rlk:mboss/pj/launch {{spd:{L.pj_speed_tenths(spd)},life:$(life),dmg:{dmg},hr:{int(round(hr * 10))}}}']
            + dress('crescent', '@s'))
    calls = {}
    for yaw, kb in ((0, KB0), (0, KB1), (spread, KB1), (-spread, KB1)):
        nm = f'cres_{"c" if yaw == 0 else ("r" if yaw > 0 else "l") + str(abs(yaw))}_kb{kb}'
        if nm in sm.subs:
            calls[(yaw, kb)] = fn(f'p/{key}/f/{nm}')
            continue
        calls[(yaw, kb)] = sm.sub(nm, [
            f'# One crescent thrown at her yaw {yaw:+d} deg (@s = body), knockback {kb}, from {num(CRES_H)} b over the floor.',
            f'execute at @s rotated as @s rotated ~{yaw} 0 positioned ^ ^ ^0.5 positioned ~ {floor_y(CRES_H)} ~ run summon '
            f'minecraft:item_display ~ ~ ~ {prop_nbt(key, "crescent", "rlk_kn_cres", "rlk_kn_new")}',
            f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s rotated as {BODY} rotated ~{yaw} 0 run '
            f'{fn(f"p/{key}/cres_out{kb}")}'])
    return calls, life


def cres_group(key):
    return [L.GRP_NEW, f'scoreboard players operation #{key}_g {OBJ} = #mbGrp mb']


def cres_fx(key, t0, t1, st):
    """Stand-in embers on the flying crescents (the kit prop carries its own), every 2 t."""
    if K.prop('crescent'):
        return
    for t in range(t0, t1 + 1, 2):
        st.at(t, f'execute as {p_of(key, "rlk_kn_cres")} at @s run {part(S.FLAME[1], 0.6, 0.15, 0.6, 0.02, 5)}')


def hold_stage(sm, name='hold', comment='crescents'):
    """Wait (idle2, facing the player) until the pattern's crescents are gone, at most HOLD_MAX ticks."""
    st = sm.st(name, 'idle2')
    st.track(1, HOLD_MAX, 10)
    st.rng(1, HOLD_MAX, S.gate(f'unless entity {p_of(sm.key, "rlk_kn_cres")}', f'return run {fn(f"p/{sm.key}/fin")}'))
    st.end(HOLD_MAX)
    return st


def q1_string(sm, W, st, hk, upto, cut_after=None, stop_var=None, last_kb_at=None):
    """The twin string of api.HITS['q1'] h1..h<upto> on stage `st` (clip q1): the lunge from mid range, h1 spin, h2 cross
    slash, h3 crescent, h4 / h5 sweeps, h6 two crescents; every swing re-faced and stepped into, only the last hit knocks
    back. stop_var: the Q1 cut decisions (#q1_k 3 / 5 when the player is beyond CUT_Q1 at h3 / h5)."""
    key = sm.key
    clip = 'q1'
    t1, t2, t3, t4, t5, t6 = (E(clip, f'h{i}') for i in range(1, 7))
    calls, life = crescents(sm, W, hk, 2)
    st.at(0, FACE, snd('step'), lunge_fn(sm))
    # the raise: within 4.5 b she walks in at 0.2 b / t (else the lunge glides her in), the aim locks 8 t before h1
    st.advance(1, t1 - 2, 0.2, STOP)
    st.track(1, t1 - LOCK1, 12)
    st.hit(hk, 0, tell=0, kb=KB0)
    st.at(t1, S.fx_spin(4.2, PY_C), snd('spin'))
    # h2 the inward cross slash
    st.advance(t1 + 2, t2 - 2, STEP, STOP)
    st.track(t1 + 1, t2 - LOCK, 14)
    st.hit(hk, 1, tell=t1, kb=KB0)
    st.at(t2, S.fx_slash(4.5, PY_C, roll=35), S.fx_slash(4.5, PY_C, roll=-35), snd('swing_heavy'))
    # h3 the thrown crescent (aim locked 6 t before); the last hit when the cast stops here
    st.track(t2 + 1, t3 - LOCK, 14)
    st.at(t3, cres_group(key), snd('crescent_throw'))
    if upto == 3:
        st.at(t3, calls[(0, KB1)])
        kb3 = KB1
    else:
        st.at(t3, S.gate(f'if score #q1_k {OBJ} matches 3', calls[(0, KB1)]),
              S.gate(f'unless score #q1_k {OBJ} matches 3', calls[(0, KB0)]))
        kb3 = None
    sm.hits.append(dict(stage=st.name, t=t3, hk=hk, idx=2, tell=t2, grp=-1, kb=kb3, bol=0, shape='pj_cres', cond=None))
    cres_fx(key, t3 + 1, t3 + 2 * life + 2, st)
    if upto == 3:
        return
    # h4 / h5 the sweeps (right, then left), each re-faced and stepped into
    st.advance(t3 + 2, t4 - 2, STEP, STOP)
    st.track(t3 + 1, t4 - LOCK, 14)
    st.hit(hk, 3, tell=t3, kb=KB0)
    st.at(t4, S.fx_slash(4.4, PY_C, roll=0), snd('swing_light'))
    st.advance(t4 + 2, t5 - 2, STEP, STOP)
    st.track(t4 + 1, t5 - LOCK, 14)
    st.hit(hk, 4, tell=t4, kb=KB1, cond=f'if score #q1_k {OBJ} matches 5')
    st.hit(hk, 4, tell=t4, kb=KB0, cond=f'unless score #q1_k {OBJ} matches 5')
    sm.hits.pop()
    sm.hits[-1]['kb'] = None
    sm.hits[-1]['cond'] = None
    st.at(t5, S.fx_slash(4.4, PY_C, roll=180), snd('swing_heavy'))
    # h6 both scythes thrown (two crescents +-15 deg, one volley group with their returns), stepped into first so a standing
    # player (<= 7 b: the cut rule) is inside the pair's reach
    st.advance(t5 + 2, t6 - 2, STEP, STOP)
    st.track(t5 + 1, t6 - LOCK, 14)
    st.at(t6, cres_group(key), calls[(15, KB1)], calls[(-15, KB1)], snd('crescent_throw'))
    sm.hits.append(dict(stage=st.name, t=t6, hk=hk, idx=5, tell=t5, grp=-1, kb=KB1, bol=0, shape='pj_cres', cond=None))
    cres_fx(key, t6 + 1, t6 + 2 * life + 2, st)


# ================================================================================================= Q0 낙하 공격
def build_q0(W):
    key = 'q0'
    sm = SM(key, W)
    go, impact, blades, end = (E('q0_dive', k) for k in ('go', 'impact', 'blades', 'end'))
    moved, wait = api.Q0_TRIGGER
    hy = api.LEAP_H['q0']
    spot = spot_fn(sm, 'spot', PLAYER, Q0_SPOT, (0, 30, -30, 60, -60, 90, -90, 135, -135, 180), hy, 0,
                   f'Q0 hover spot (@s = body): {num(Q0_SPOT[0])} b from the player on the player -> her line (else turned, else '
                   f'nearer), the floor spot passing mv/ok, {num(hy)} b up; placed there (seq/t_p2 hid her at its launch).',
                   tp=True)
    # the player's spot at the start (the trigger compares the floor positions: a jump in place is no move)
    sm.start += [f'kill @e[type=minecraft:marker,tag=rlk_kn_q0p]',
                 f'execute at {PLAYER} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_q0p")}}}']
    hv = sm.st('hover', 'q0_hover')
    hv.at(0, spot, FACE, look('glow', 'crimson'), snd('apex'))
    hv.track(1, wait, 10)
    for t in range(4, wait, 8):
        if not K._on():
            hv.at(t, f'execute at @s positioned ~ ~1.4 ~ run {part(S.DUST[2], 0.5, 0.8, 0.5, 0, 6)}')
    hv.rng(1, wait - 1, S.gate(f'at {PLAYER} positioned ~ {CY} ~ unless entity @e[type=minecraft:marker,tag=rlk_kn_q0p,'
                               f'distance=..{num(moved)}] at @s', f'return run {fn(f"p/{key}/s/dive/go")}'))
    hv.go(wait, 'dive')
    dv = sm.st('dive', 'q0_dive')
    # the trigger: the lock (the player's spot, mv/ok) moved 1.5 b toward her, the crimson streak to it over 20 t
    dv.at(0, fn('core/lockp'), fn('core/lock_short'), f'execute at @s facing entity {LOCK_M} feet run tp @s ~ ~ ~ ~ 0',
          f'execute positioned as {LOCK_M} run function rlk:mboss/mv/glide {{t:{impact - go}}}',
          S.fx('dive_streak', [part(S.DUST[2], 0.3, 0.8, 0.3, 0, 20)], pos=f'{AT_BODY} positioned ~ ~1 ~', len=int(hy * 10)),
          snd('fall_dive'))
    if not K._on():
        for t in range(2, impact, 3):
            dv.at(t, f'execute at @s run {part(S.DUST[2], 0.3, 0.8, 0.3, 0, 10)}', f'execute at @s run {part(S.FLAME[2], 0.2, 0.6, 0.2, 0.02, 6)}')
    dv.hit(key, 0, tell=0, kb=KB0, pos=at_floor(LOCK_M))
    dv.at(impact, S.fx_impact(3.0, BOL_C, pos=at_floor(LOCK_M)), snd('fall_impact', f'at {LOCK_M}'))
    # the blade eruption around the landing (r 3-7): the blades rise 6 t before
    dv.at(impact + 2, S.fx('blade_rise', [part(S.DUST[2], 4.0, 0.3, 4.0, 0, 40)], pos=f'at {LOCK_M} positioned ~ {CY} ~'),
          snd('blade_rise', f'at {LOCK_M}'))
    dv.hit(key, 1, tell=0, kb=KB1, pos=at_floor(LOCK_M))
    dv.at(blades, S.fx('thorns', [part(S.DUST[2], 3.5, 0.6, 3.5, 0, 80), part(S.FLAME[2], 3.0, 0.4, 3.0, 0.03, 30)],
                       pos=f'at {LOCK_M} positioned ~ {CY} ~', r=70), snd('rim', f'at {LOCK_M}'), look('glow', 'normal'))
    dv.end(end)
    sm.cancel.append(f'kill @e[type=minecraft:marker,tag=rlk_kn_q0p]')
    return sm.write()


# ================================================================================================= Q1 사형장으로의 초대 (P2)
def build_q1(W):
    key = 'q1'
    sm = SM(key, W)
    st = sm.st('main', 'q1')
    sm.start.append(sset('#q1_k', 0))
    t3, t5, end = E('q1', 'h3'), E('q1', 'h5'), E('q1', 'end')
    # the cut decisions (PLAN §6): beyond 7 b at h3 / h5 the cast stops after it (3 or 5 hits)
    far = f'at @s unless entity {PLAYER[:-1]},distance=..{num(CUT_Q1)}]'
    st.at(t3 - 2, f'execute {far} run {sset("#q1_k", 3)}')
    st.at(t5 - 2, f'execute unless score #q1_k {OBJ} matches 3 {far} run {sset("#q1_k", 5)}')
    q1_string(sm, W, st, key, 6)
    st.go(t3 + 6, 'hold', f'if score #q1_k {OBJ} matches 3')
    st.go(t5 + 6, 'hold', f'if score #q1_k {OBJ} matches 5')
    st.end(end)
    hold_stage(sm)
    return sm.write()


# ================================================================================================= Q2 불꽃이 타오르는 낫
def build_q2(W):
    key = 'q2'
    sm = SM(key, W)
    windup, release, go, slash, end = (E('q2', k) for k in ('windup', 'release', 'go', 'slash', 'end'))
    hr, spd, rr = api.HITS[key][0][3]
    tier = api.HITS[key][0][4]
    dmg = api.dmg(tier, PH)
    st = sm.st('main', 'q2')
    st.at(windup, FACE, snd('wheel_spin'), S.fx('embers_puff', [part(S.FLAME[1], 0.4, 0.6, 0.4, 0.03, 10)]))
    st.at(windup + 6, snd('wheel_spin'))
    # the aim locks 6 t before the release: the lock marker at the player's spot (mv/ok)
    st.track(1, release - LOCK, 10)
    st.at(release - LOCK, fn('core/lockp'), f'execute at @s facing entity {LOCK_M} feet run tp @s ~ ~ ~ ~ 0')
    burst_lines = (S.hz_opts(key, dmg, 0, kb=KB0)
                   + [f'scoreboard players operation #hzGrp mb = #{key}_g {OBJ}',
                      f'execute positioned ~ {CY} ~ run {L.hz_disc(rr, 1, dmg)}', S.hz_tag(key)]
                   + S.fx_impact(rr, PY_C, pos=f'positioned ~ {floor_y(0.2)} ~') + snd('impact', 'positioned ~ ~ ~')
                   + [f'kill {p_of(key, "rlk_kn_wheel")}', sset('#q2_b', 1)])
    W.w('p/q2/burst', [f'# Q2 the wheel bursts here (positioned at the burst point; @s any): disc({num(rr)}) {tier} plain Pyro, the',
                       f'# wheel\'s volley group (one landing for flight + burst), strikes next tick; once.',
                       f'execute if score #q2_b {OBJ} matches 1 run return 0'] + burst_lines)
    W.w('p/q2/wheel', [
        f'# Q2 the flaming wheel (@s = body): a vertical wheel pj from her chest height toward the lock ({num(hr)} b, {num(spd)} b/t,',
        f'# at most {WHEEL_LIFE} t, wall stop, {tier} plain Pyro, a new volley group); it bursts on arrival at the lock (tick check),',
        '# at a wall or at the end of its range (pj_end).',
        L.GRP_NEW, f'scoreboard players operation #{key}_g {OBJ} = #mbGrp mb', sset('#q2_b', 0),
        f'execute at @s facing entity {LOCK_M} feet rotated ~ 0 positioned ^ ^ ^0.5 positioned ~ {floor_y(CRES_H)} ~ run summon '
        f'minecraft:item_display ~ ~ ~ {prop_nbt(key, "wheel", "rlk_kn_wheel", "rlk_kn_new")}',
        f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity {LOCK_M} feet rotated ~ 0 run '
        f'{fn("p/q2/launch")}'])
    W.w('p/q2/launch', ['# @s = the new wheel (rotated toward the lock).', 'tag @s remove rlk_kn_new',
                        f'scoreboard players operation #pjGrp mb = #{key}_g {OBJ}']
        + L.pj_opts(el=api.PYRO, kb=KB0, wall=1) + [L.pj_launch(spd, WHEEL_LIFE, dmg, hr)] + dress('wheel', '@s'))
    W.w('p/q2/pj_end', ['# Q2 wheel event (@s = the prop; #pjEv 1 wall, 2 range over: it bursts here; 4 hit the player: flies on).',
                        'execute unless score #pjEv mb matches 1..2 run return 0', f'execute at @s run {fn("p/q2/burst")}'])
    st.at(release, fn('p/q2/wheel'), snd('wheel_throw'),
          S.fx('wheel_trail', [], pos=f'{AT_BODY} positioned ~ {CY} ~', len=150))
    st.rng(release + 1, release + WHEEL_LIFE + 1,
           f'execute as {p_of(key, "rlk_kn_wheel")} at @s positioned ~ {CY} ~ if entity {LOCK_M[:-1]},distance=..0.8] at {LOCK_M} '
           f'run function {NS}p/q2/burst')
    if not K.prop('wheel'):
        for t in range(release + 1, release + WHEEL_LIFE + 2, 2):
            st.at(t, f'execute as {p_of(key, "rlk_kn_wheel")} at @s run {part("minecraft:flame", 0.5, 0.6, 0.5, 0.02, 6)}')
    sm.hits.append(dict(stage='main', t=release, hk=key, idx=0, tell=windup, grp=-1, kb=KB0, bol=0, shape='pj_burst', cond=None))
    # go: the dash after it, to 1.5 b in front of the player (at most DASH_LEN, probed in 0.5 b steps through mv/ok)
    dl = api.DASH_LEN[key]
    W.w('p/q2/dash', [
        f'# Q2 dash (@s = body, 1 t before go): facing the player, to 1.5 b in front of them (at most {num(dl)} b; core/dash/probe:',
        f'# every 0.5 b step passes mv/ok), glided over {slash - go} t; the end marker rlk_kn_q2e decides the slash.',
        FACE, 'function rlk:mboss/mv/dist',
        f'scoreboard players operation #t {OBJ} = #mbDist mb',
        f'scoreboard players remove #t {OBJ} 15',
        f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches ..0 run scoreboard players set #t {OBJ} 0',
        f'execute if score #t {OBJ} matches {int(dl * 2) + 1}.. run scoreboard players set #t {OBJ} {int(dl * 2)}',
        fn('core/dash/probe'),
        f'kill @e[type=minecraft:marker,tag=rlk_kn_q2e]',
        f'execute positioned as {DP} run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_q2e")}}}',
        f'execute positioned as {DP} run function rlk:mboss/mv/glide {{t:{slash - go}}}',
        'kill @e[type=minecraft:marker,tag=rlk_kn_dp]'])
    st.at(go - 1, fn('p/q2/dash'), snd('dash_tell'))
    st.at(go, snd('dash'), S.fx('dash_trail', [part(S.FLAME[1], 0.4, 0.5, 0.4, 0.06, 16)], pos=f'{AT_BODY} positioned ~ ~1 ~',
                               len=140, c=PY_C))
    if not K._on():
        for t in range(go + 1, slash):
            st.at(t, f'execute at @s run {part(S.FLAME[1], 0.3, 0.5, 0.3, 0.04, 10)}')
    # the slash on arrival, only when the player is within reach of the dash end (no whiff): else the cast ends there
    near = f'at @e[type=minecraft:marker,tag=rlk_kn_q2e,limit=1] if entity {PLAYER[:-1]},distance=..{num(SLASH_REACH)}]'
    st.at(slash - 2, sset('#q2_sl', 0), f'execute {near} run {sset("#q2_sl", 1)}')
    st.hit(key, 1, tell=windup, kb=KB1, cond=f'if score #q2_sl {OBJ} matches 1')
    st.at(slash, S.gate(f'if score #q2_sl {OBJ} matches 1', sm.sub('slash_fx', ['# Q2 the slash on arrival (@s = body).']
                                                                + S.fx_slash(4.5, PY_C, roll=10) + snd('sweep'))))
    st.at(slash - 1, S.gate(f'unless score #q2_sl {OBJ} matches 1', api.play('idle2')))
    st.end(slash + 6, f'unless score #q2_sl {OBJ} matches 1')
    st.end(end)
    sm.start += [sset('#q2_b', 1), sset('#q2_sl', 0)]
    sm.cancel.append(sset('#q2_b', 1))
    return sm.write()


# ================================================================================================= Q3 붉은 죽음의 무도회
def build_q3(W):
    key = 'q3'
    sm = SM(key, W)
    whip, spin, end = E('q3', 'whip'), E('q3', 'spin'), E('q3', 'end')
    thr = spin + 12                    # the far follow-up: two crescents 12 t after the spin, on its follow-through
    sm.start.append(sset('#q3_k', 0))
    wp = sm.st('whip', 'q3')
    # she whips round (legs flare, the 30 deg / t turn), the spin at 14 (disc around her)
    kl = K.p('legs_burst')
    wp.at(whip, snd('rear_whip'),
          [api.rig('anchor/spine'), f'execute if entity {ANCHOR} at {ANCHOR} rotated as @s rotated ~ 0 run {kl}',
           f'execute unless entity {ANCHOR} at @s rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run {kl}'] if kl
          else [f'execute at @s positioned ~ ~1.6 ~ run {part(S.DUST[2], 1.2, 0.8, 1.2, 0, 24)}'])
    wp.track(1, 10, 30)
    wp.hit(key, 0, tell=whip, kb=KB0)
    wp.at(spin, S.fx_spin(4.6, PY_C), snd('spin'))
    # the follow-up decided 6 t before the throw: player <= 6 b -> the Q1 string h1-h3, else two crescents (as Q1 h6)
    wp.track(spin + 1, thr - LOCK, 20)
    wp.at(thr - LOCK, sset('#q3_k', 2), f'execute at @s if entity {PLAYER[:-1]},distance=..{num(CUT_Q3)}] run {sset("#q3_k", 1)}')
    calls, life = crescents(sm, W, 'q1', 5, spread=Q3_SPREAD)
    wp.at(thr, S.gate(f'if score #q3_k {OBJ} matches 2', sm.sub('far', [f'# Q3 far: two crescents +-{Q3_SPREAD} deg at the player (one volley group).']
                                                               + cres_group(key) + [calls[(Q3_SPREAD, KB1)], calls[(-Q3_SPREAD, KB1)]]
                                                               + snd('crescent_throw'))))
    sm.hits.append(dict(stage='whip', t=thr, hk='q1', idx=5, tell=spin, grp=-1, kb=KB1, bol=0, shape='pj_cres',
                        cond='far'))
    cres_fx(key, thr + 1, thr + 2 * life + 2, wp)
    wp.go(end, 'cut', f'if score #q3_k {OBJ} matches 1')
    wp.go(end, 'hold')
    cut = sm.st('cut', 'q1')
    q1_string(sm, W, cut, 'q1', 3)
    for h in sm.hits:
        if h['stage'] == 'cut':
            h['cond'] = 'near'
    cut.go(E('q1', 'h3') + 6, 'hold')
    hold_stage(sm)
    return sm.write()


# ================================================================================================= Q4 떠오르는 재액의 달
def build_q4(W):
    key = 'q4'
    sm = SM(key, W)
    top = E('q4_up', 'top')
    aim, lockt, fire, shot_end = (E('q4_shot', k) for k in ('aim', 'lock', 'fire', 'end'))
    land, land_end = E('q4_land', 'land'), api.CLIPS['q4_land'][0]
    hy = api.LEAP_H[key]
    base, missed = api.Q4_SHOTS['base'], api.Q4_SHOTS['missed']
    low_pct, low_n = api.Q4_SHOTS['low_pct']
    tid = S.TID[key]
    # shots: 1; 3 at <= 50 % of the P2 pool (mhpC x 100 <= mhpM x 50); the test (id 45: #q4_t3, set by test/go/q4) and its lock: 3
    sm.start += [sset('#q4_n', base), sset('#q4_k', 0),
                 f'execute store result score #t {OBJ} run scoreboard players get @s mhpC',
                 f'scoreboard players operation #t {OBJ} *= #c100 {OBJ}',
                 f'execute store result score #t2 {OBJ} run scoreboard players get @s mhpM',
                 f'scoreboard players set #t3 {OBJ} {low_pct}',
                 f'scoreboard players operation #t2 {OBJ} *= #t3 {OBJ}',
                 f'execute if score #t {OBJ} <= #t2 {OBJ} run {sset("#q4_n", low_n)}',
                 f'execute if score #q4_t3 {OBJ} matches 1 run {sset("#q4_n", low_n)}',
                 f'scoreboard players reset #q4_t3 {OBJ}',
                 f'execute if score #mbLock mb matches {tid} run {sset("#q4_n", low_n)}']
    spot = spot_fn(sm, 'spot', PLAYER, Q4_SPOT, (0, 30, -30, 60, -60), hy, top - 4,
                   f'Q4 rise (@s = body): back off to {num(Q4_SPOT[0])} b from the player (else turned / nearer; the floor spot '
                   f'passes mv/ok), {num(hy)} b up, glided over {top - 4} t.')
    up = sm.st('up', 'q4_up')
    up.at(0, FACE, spot, snd('leap'), S.fx('leap_flare', [part(S.FLAME[2], 0.6, 0.3, 0.6, 0.05, 16)], pos=f'{AT_BODY} positioned ~ ~0.3 ~'))
    up.track(1, top, 12)
    up.go(top, 'shot')
    sh = sm.st('shot', 'q4_shot')
    chest = sm.sub('chest', ['# The aim origin (@s = body): the rig\'s chest anchor (the stand-in: 2 b over her feet).',
                             api.rig('anchor/chest'),
                             f'execute unless entity {ANCHOR} at @s run return run summon minecraft:marker ~ ~2 ~ '
                             f'{{Tags:{tagn(key, "rlk_kn_q4c")}}}',
                             f'execute at {ANCHOR} run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_q4c")}}}'])
    CH = f'@e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1]'
    # the distance (tenths) from the chest marker to a point (the player's eyes / the lock on the floor): #q4_r kn
    dist3 = K._on() and sm.sub('dist3', [
        '# #q4_r kn = the distance in tenths from the chest marker to the execution position (dx dy dz -> Newton square root).',
        f'execute store result score #q4_x {OBJ} run data get entity {CH} Pos[0] 10',
        f'execute store result score #q4_y {OBJ} run data get entity {CH} Pos[1] 10',
        f'execute store result score #q4_z {OBJ} run data get entity {CH} Pos[2] 10',
        f'summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_q4t")}}}',
        f'execute store result score #q4_r {OBJ} run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4t,limit=1] Pos[0] 10',
        f'scoreboard players operation #q4_x {OBJ} -= #q4_r {OBJ}',
        f'execute store result score #q4_r {OBJ} run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4t,limit=1] Pos[1] 10',
        f'scoreboard players operation #q4_y {OBJ} -= #q4_r {OBJ}',
        f'execute store result score #q4_r {OBJ} run data get entity @e[type=minecraft:marker,tag=rlk_kn_q4t,limit=1] Pos[2] 10',
        f'scoreboard players operation #q4_z {OBJ} -= #q4_r {OBJ}',
        'kill @e[type=minecraft:marker,tag=rlk_kn_q4t]',
        f'scoreboard players operation #q4_x {OBJ} *= #q4_x {OBJ}', f'scoreboard players operation #q4_y {OBJ} *= #q4_y {OBJ}',
        f'scoreboard players operation #q4_z {OBJ} *= #q4_z {OBJ}',
        f'scoreboard players operation #q4_x {OBJ} += #q4_y {OBJ}', f'scoreboard players operation #q4_x {OBJ} += #q4_z {OBJ}',
        f'scoreboard players set #q4_r {OBJ} 250']
        + [ln for _ in range(8) for ln in (f'scoreboard players operation #q4_y {OBJ} = #q4_x {OBJ}',
                                            f'scoreboard players operation #q4_y {OBJ} /= #q4_r {OBJ}',
                                            f'scoreboard players operation #q4_r {OBJ} += #q4_y {OBJ}',
                                            f'scoreboard players operation #q4_r {OBJ} /= #c2 {OBJ}',
                                            f'execute if score #q4_r {OBJ} matches ..0 run scoreboard players set #q4_r {OBJ} 1')])
    # aim 0..20: the thin red aim line from her chest to the player (tracking, each call lives 3 t: every 2 t) + the reticle
    # (once: it grows, turns white-hot at the lock 20, is gone at the fire 26); lock 20; fire 26 (S1K K4 conventions)
    aim_lines = ['# Q4 the aim line (@s = body, every 2 t of the aim): from the chest anchor toward the player\'s eyes, pitch counts.',
                 f'kill @e[type=minecraft:marker,tag=rlk_kn_q4c]', chest]
    if K._on():
        aim_lines += [f'execute at {PLAYER} anchored eyes positioned ^ ^ ^ run {dist3}',
                      f'execute store result storage {api.STORAGE} p2.aim.len int 1 run scoreboard players get #q4_r {OBJ}',
                      f'execute at {CH} facing entity {PLAYER} eyes run {S.kit_with("p/", "aim_line", "p2.aim")}']
        sh_ret = sm.sub('reticle', ['# Q4 the reticle (@s = body, once per shot): at the chest anchor toward the player.',
                                    f'kill @e[type=minecraft:marker,tag=rlk_kn_q4c]', chest,
                                    f'execute at {CH} facing entity {PLAYER} eyes run {K.p("reticle")}'])
    else:
        aim_lines += [f'execute at {CH} facing entity {PLAYER} eyes positioned ^ ^ ^{d} run {part(S.DUST[2], 0.02, 0.02, 0.02, 0, 1)}'
                      for d in range(1, 16)]
        aim_lines.append(f'execute at {CH} run {part(S.DUST[2], 0.15, 0.15, 0.15, 0, 6)}')
    aim_fn = sm.sub('aim', aim_lines)
    sh.at(aim, f'scoreboard players add #q4_k {OBJ} 1', look('glow', 'crimson'), snd('beam_aim'), sh_ret if K._on() else [])
    for t in range(aim, lockt, 2):
        sh.at(t, aim_fn)
    sh.track(1, lockt - 1, 12)
    sh.at(lockt, fn('core/lockp'), f'execute at @s facing entity {LOCK_M} feet run tp @s ~ ~ ~ ~ 0', snd('beam_aim'), aim_fn)
    # fire 26: the beam line(30, 2.2) from her through the locked point (Bond of Life); the last shot of the cast knocks back
    sh.hit(key, 0, tell=aim, kb=KB1, cond=f'if score #q4_k {OBJ} = #q4_n {OBJ}')
    sh.hit(key, 0, tell=aim, kb=KB0, cond=f'unless score #q4_k {OBJ} = #q4_n {OBJ}')
    sm.hits.pop()
    sm.hits[-1]['kb'] = None
    sm.hits[-1]['cond'] = None
    beam = ['# Q4 the beam (@s = body): from the chest anchor through the lock, the burst at the lock, embers along the line.',
            f'kill @e[type=minecraft:marker,tag=rlk_kn_q4c]', chest]
    if K._on():
        beam += [f'execute at {LOCK_M} run {dist3}',
                 f'execute store result storage {api.STORAGE} p2.beam.len int 1 run scoreboard players get #q4_r {OBJ}',
                 f'execute at {CH} facing entity {LOCK_M} feet run {S.kit_with("p/", "beam", "p2.beam")}']
    if not K._on():
        beam += [f'execute at {CH} facing entity {LOCK_M} feet positioned ^ ^ ^{d} run {part(S.DUST[2], 0.25, 0.25, 0.25, 0, 4)}'
                 for d in range(1, 40, 2)]
    beam += [f'execute {AT_BODY} positioned ~ {floor_y(0.1)} ~ positioned ^ ^ ^{d} run {part(S.FLAME[2], 0.6, 0.05, 0.6, 0.01, 3)}'
             for d in range(2, 31, 3)]
    beam += S.fx_impact(2.2, BOL_C, pos=f'at {LOCK_M} positioned ~ {floor_y(0.2)} ~') + snd('beam_fire') + snd('impact', f'at {LOCK_M}')
    beam.append(f'kill @e[type=minecraft:marker,tag=rlk_kn_q4c]')
    sh.at(fire, sm.sub('beam', beam), look('glow', 'normal'))
    # the first shot missed (no landed hit the tick after it struck) -> a second one (unless three already)
    sh.at(fire + 1, f'execute if score #q4_k {OBJ} matches 1 if score #q4_n {OBJ} matches ..{missed - 1} '
                    f'unless score #hitev {OBJ} matches 1.. run {sset("#q4_n", missed)}')
    sh.go(shot_end, 'shot', f'if score #q4_k {OBJ} < #q4_n {OBJ}')
    sh.go(shot_end, 'land')
    ld = sm.st('land', 'q4_land')
    ld.at(0, f'execute at @s positioned ~ {CY} ~ if {OK} run function rlk:mboss/mv/glide {{t:{land}}}',
          f'execute at @s positioned ~ {CY} ~ unless {OK} run {fn("core/ground")}')
    ld.track(1, land, 10)
    ld.at(land, snd('step'), S.fx('embers_puff', [part(S.DUST[2], 0.6, 0.2, 0.6, 0, 12)], pos=f'{AT_BODY} positioned ~ ~0.2 ~'))
    ld.end(land_end)
    return sm.write()


# ================================================================================================= Q5 붉은 피의 연회 (P2)
Q5C = '@e[type=minecraft:marker,tag=rlk_kn_q5c,limit=1]'


def q5_open(sm, st):
    """Both variants: raise 0 (the crimson glow, the sigil ring closing on the player 6-22), brand 22 = the forced bond
    (api.BOND_CALLS['force']: + BOL_FORCE %, the brand, 3 heal orbs; the core opens the break window and the banner)."""
    key = sm.key
    brand = E(key, 'brand')
    assert brand == api.FORCE_TICK[key] == api.BREAK_WINDOWS[key][0]
    sm.start += [f'kill @e[type=minecraft:marker,tag=rlk_kn_q5c]',
                 f'execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{tagn(key, "rlk_kn_q5c")}}}']
    st.at(0, FACE, look('glow', 'crimson'), snd('brand'))
    st.at(6, S.fx('brand_ring', [], pos=f'at {PLAYER}'))
    if not K._on():
        for t in range(6, brand, 2):
            r = 3.0 - (t - 6) * 2.5 / (brand - 6)
            st.at(t, f'execute at {PLAYER} positioned ~ ~0.2 ~ run {part(S.DUST[2], r * 0.6, 0.05, r * 0.6, 0, 12)}')
    st.at(brand, api.BOND_CALLS['force'])
    return brand


def ring_dots(r, n=None):
    """Stand-in outline: crimson dust on a circle of radius r around the execution point (on the floor)."""
    n = n or max(16, int(r * 4))
    return [f'execute rotated {num(360.0 * i / n, 1)} 0 positioned ^ ^ ^{num(r, 2)} run {part(S.DUST[2], 0.05, 0.02, 0.05, 0, 1)}'
            for i in range(n)]


def build_q5a(W):
    key = 'q5a'
    sm = SM(key, W)
    st = sm.st('main', 'q5a')
    brand = q5_open(sm, st)
    ring1, hit1, donut, hit2, ring3, hit3, end = (E(key, k) for k in ('ring1', 'hit1', 'donut', 'hit2', 'ring3', 'hit3', 'end'))
    r1 = api.HITS[key][0][3][0]
    r20, r2 = api.HITS[key][1][3]
    r3 = api.HITS[key][2][3][0]
    st.track(1, ring1, 6)
    at_c = f'at {Q5C}'
    # the floor outlines (PLAN §1.5, the only P2 decals): disc 6 -> donut 6-15 -> disc 11, each flashing before its burst
    for t0, t1, name, args, dots in ((ring1, hit1, 'ring_o', dict(r=int(r1 * 10), t=hit1 - ring1), ring_dots(r1)),
                                     (donut, hit2, 'donut_o', dict(r0=int(r20 * 10), r=int(r2 * 10), t=hit2 - donut),
                                      ring_dots(r20) + ring_dots(r2)),
                                     (ring3, hit3, 'ring_o', dict(r=int(r3 * 10), t=hit3 - ring3), ring_dots(r3))):
        k = K.decal(name, **args)
        st.at(t0, placed([k], f'{at_c} positioned ~ {CY} ~') if k else [], snd('flood', at_c))
        if not k:
            nm = sm.sub(f'dots_{t0}', [f'# Q5A stand-in outline ({name} {args}) at the centre marker.']
                        + placed(dots, f'{at_c} positioned ~ {floor_y(0.1)} ~'))
            for t in range(t0, t1, 4):
                st.at(t, nm)
    st.hit(key, 0, tell=ring1, kb=KB0, pos=at_floor(Q5C))
    st.at(hit1, S.fx('blast', [part(S.DUST[2], r1 * 0.45, 0.4, r1 * 0.45, 0, 80), part('minecraft:explosion', 2, 0.3, 2, 0, 4)],
                     pos=f'{at_c} positioned ~ {CY} ~', r=int(r1 * 10)), snd('blast', at_c))
    st.hit(key, 1, tell=donut, kb=KB0, pos=at_floor(Q5C))
    st.at(hit2, S.fx('thorns', [part(S.DUST[2], r2 * 0.4, 0.5, r2 * 0.4, 0, 160)], pos=f'{at_c} positioned ~ {CY} ~', r=int(r2 * 10)),
          snd('threads', at_c))
    st.hit(key, 2, tell=ring3, kb=KB1, pos=at_floor(Q5C))
    st.at(hit3, S.fx('blast', [part(S.DUST[2], r3 * 0.45, 0.5, r3 * 0.45, 0, 200), part('minecraft:explosion', 4, 0.4, 4, 0, 8)],
                     pos=f'{at_c} positioned ~ {CY} ~', r=int(r3 * 10)), snd('blast', at_c), snd('final', at_c))
    st.at(hit3 + 8, look('glow', 'normal'))
    st.end(end)
    if K._on():
        sm.cancel.append(K.fixed('clear'))
        res = ['# Q5A resume (@s = body): the outline decal again with the ticks left to its burst (pause cleared the kit cards).']
        for t0, t1, name, extra in ((ring1, hit1, 'ring_o', {'r': int(r1 * 10)}), (donut, hit2, 'donut_o', {'r0': int(r20 * 10), 'r': int(r2 * 10)}),
                                    (ring3, hit3, 'ring_o', {'r': int(r3 * 10)})):
            nm = f'res_{t0}'
            sm.sub(nm, [f'# {name} with the ticks left (#pt {t0}..{t1 - 1}).',
                        f'data modify storage {api.STORAGE} p2.dec set value {{' + ','.join(f'{k}:{v}' for k, v in extra.items()) + ',t:0}',
                        f'scoreboard players set #t {OBJ} {t1}', f'scoreboard players operation #t {OBJ} -= #pt {OBJ}',
                        f'execute store result storage {api.STORAGE} p2.dec.t int 1 run scoreboard players get #t {OBJ}',
                        f'execute {at_c} positioned ~ {CY} ~ run {S.kit_with("decal/", name, "p2.dec")}'])
            res.append(f'execute if score #pt {OBJ} matches {t0}..{t1 - 1} run {fn(f"p/{key}/f/{nm}")}')
        W.w(f'p/{key}/resume', res)
    return sm.write()


def build_q5b(W):
    key = 'q5b'
    sm = SM(key, W)
    st = sm.st('main', 'q5b')
    brand = q5_open(sm, st)
    x, mark, final, end = (E(key, k) for k in ('x', 'mark', 'final', 'end'))
    slashes = [E(key, f's{i}') for i in range(1, 10)]
    rr, pm = api.HITS[key][9][3]
    # the vertical red X carved in front of her, facing the player (26-50)
    st.track(1, x, 10)
    st.at(x, FACE, S.fx('x_mark', [], pos=AT_BODY), snd('x_carve'))
    st.at(x + 12, snd('x_carve'))
    if not K._on():
        xd = sm.sub('x_dots', ['# Q5B stand-in X (two crimson diagonals 2 b in front of her).']
                    + [f'execute {AT_BODY} positioned ^{num(s * d)} ^{num(1.6 + d)} ^2 run {part(S.DUST[2], 0.03, 0.03, 0.03, 0, 1)}'
                       for d in (-1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6) for s in (1, -1)])
        for t in range(x, mark + 1, 3):
            st.at(t, xd)
    # the rapid slashes all around her (s1-s9, 3 t apart; one volley group per 2 slashes: <= 5 landings), stepping toward
    # the player at 0.15 b / t while farther than 3 b
    st.track(mark, slashes[-1], 8)
    st.advance(mark + 3, slashes[-1] - 1, 0.15, 3.0)
    g = 0
    for i, t in enumerate(slashes):
        if i % api.Q5B_SLASH_GROUP == 0:
            g = st.group(t - 1)
        st.hit(key, i, tell=x if i == 0 else slashes[i - 1], grp=g, kb=KB0)
        kr = K.p('rapid_slash')
        st.at(t, placed([kr], f'{AT_BODY} positioned ~ ~{S.H(1.2)} ~') if kr else S.fx_slash(5.5, PY_C, roll=40 if i % 2 else -40),
              snd('rapid'))
    # the final: the crimson aura swells 20 t before (both scythes raised from 84), pm_disc(7.5) per mille (api.HITS), non-lethal,
    # Bond of Life, dash-dodgeable
    tell = final - api.TELL_BIG
    st.at(tell, S.fx('shock_aura', [part(S.DUST[2], 0.8, 1.2, 0.8, 0, 40)], pos=f'at @s positioned ~ ~{S.H(1.4)} ~'), snd('brand'))
    if not K._on():
        for t in range(tell + 2, final, 3):
            st.at(t, f'execute at @s positioned ~ ~1.4 ~ run {part(S.DUST[2], 0.9, 1.0, 0.9, 0, 12)}')
    h = api.HITS[key][9]
    fl = (L.hz_opts(quiet=1, sfx=0, el=api.PYRO, pm=pm, pm_lethal=0, **S.bol_opts(1))
          + [f'execute {AT_BODY} positioned ~ {CY} ~ run {L.hz_disc(rr, 1, 1)}', S.hz_tag(key)])
    assert h[2] == 'pm_disc' and not api.Q5B_FINAL_LETHAL
    st.at(final - 1, fl)
    st.at(final, S.bol_mark())
    sm.hits.append(dict(stage='main', t=final, hk=key, idx=9, tell=tell, grp=0, kb=KB1, bol=1, shape='pm_disc', cond=None))
    st.at(final, S.fx('final_burst', [part(S.DUST[2], rr * 0.45, 0.6, rr * 0.45, 0, 200), part('minecraft:explosion', 3, 0.4, 3, 0, 6)],
                      pos=f'at @s positioned ~ {CY} ~', r=int(rr * 10)), snd('final'))
    st.at(final + 8, look('glow', 'normal'))
    st.end(end)
    if K._on():
        sm.cancel.append(K.fixed('clear'))
    return sm.write()


# ================================================================================================= Q6 핏빛 연회
def build_q6(W):
    key = 'q6'
    sm = SM(key, W)
    st = sm.st('main', 'q6')
    fly, gone, moon, orbs, toss, lockt, dive, impact, end = (
        E(key, k) for k in ('fly', 'gone', 'moon', 'orbs', 'toss', 'lock', 'dive', 'impact', 'end'))
    vol = [E(key, f'v{i}') for i in range(1, 7)]
    hy = api.LEAP_H[key]
    fdmg = api.dmg(api.HITS[key][0][4], PH)
    fr = api.HITS[key][0][3][0]
    n_orb, orb_rim = api.HITS[key][7][3][1], api.HITS[key][7][3][2]
    orb_r = api.HITS[key][7][3][0]
    # fly 0 -> 12 b over the arena's north half (stays hittable), the moon at 30
    hx, hz = Q6_HOVER
    st.at(fly, FACE, f'execute positioned as {ARENA_M} positioned ~{num(hx)} {floor_y(hy)} ~{num(hz)} run function rlk:mboss/mv/glide {{t:{gone - fly}}}',
          snd('leap'), S.fx('leap_flare', [part(S.FLAME[2], 0.6, 0.3, 0.6, 0.05, 20)], pos=f'{AT_BODY} positioned ~ ~0.3 ~'))
    st.track(1, dive - 1, 10)
    km = K.p('moon_flare')
    moon_m = '@e[tag=rlk_kn_moon,limit=1]'
    st.at(moon, [f'execute if entity {moon_m} at {moon_m} run {km}', f'execute unless entity {moon_m} at @s run {km}'] if km
          else [f'execute at @s positioned ~ ~4 ~ run {part(S.DUST[2], 1.6, 1.6, 1.6, 0, 60)}'], snd('moon'))
    # six volleys: one feather each from her legs (spine anchor) to the player's spot, landing FEATHER_T t later
    spine = [api.rig('anchor/spine')]
    for i, t in enumerate(vol, 1):
        mk, fth = f'rlk_kn_fl{i}', f'rlk_kn_fth{i}'
        h = api.HITS[key][i - 1]
        assert h[2] == 'pj_bolt' and E(h[0], h[1]) == t
        W.w(f'p/q6/v{i}', [
            f'# Q6 volley {i} (@s = body): the landing spot = the player\'s floor spot now; one feather from her legs flies there',
            f'# in {FEATHER_T} t (glide, facing its flight); its disc({num(fr)}) {h[4]} plain Pyro strikes when it lands (quiet hazard).',
            f'execute at {PLAYER} run summon minecraft:marker ~ {floor_y()} ~ {{Tags:{tagn(key, "rlk_kn_fl", mk)}}}'] + spine
            + [f'execute if entity {ANCHOR} at {ANCHOR} run summon minecraft:item_display ~ ~ ~ {prop_nbt(key, "feather", "rlk_kn_fth", fth, "rlk_kn_new")}',
               f'execute unless entity {ANCHOR} at @s run summon minecraft:item_display ~ ~1.6 ~ {prop_nbt(key, "feather", "rlk_kn_fth", fth, "rlk_kn_new")}']
            + [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity @e[type=minecraft:marker,tag={mk},limit=1] feet '
               'run tp @s ~ ~ ~ ~ ~']
            + dress('feather')
            + [
               f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] positioned as @e[type=minecraft:marker,tag={mk},limit=1] '
               f'positioned ~ ~0.3 ~ run function rlk:mboss/mv/glide {{t:{FEATHER_T}}}',
               'tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new']
            + S.hz_opts(key, fdmg, 0, kb=KB0)
            + [f'execute at @e[type=minecraft:marker,tag={mk},limit=1] positioned ~ {CY} ~ run {L.hz_disc(fr, FEATHER_T, fdmg)}',
               S.hz_tag(key)] + snd('feather'))
        W.w(f'p/q6/land{i}', [f'# Q6 feather {i} lands (@s = body): the burst at its spot, the feather and the spot marker gone.']
            + S.fx('feather_hit', [part(S.DUST[2], 0.6, 0.2, 0.6, 0, 16), part(S.FLAME[2], 0.4, 0.1, 0.4, 0.02, 6)],
                   pos=f'at @e[type=minecraft:marker,tag={mk},limit=1] positioned ~ {CY} ~')
            + snd('impact', f'at @e[type=minecraft:marker,tag={mk},limit=1]')
            + [f'kill @e[tag={fth}]', f'kill @e[type=minecraft:marker,tag={mk}]'])
        st.at(t, fn(f'p/q6/v{i}'))
        st.at(t + FEATHER_T, fn(f'p/q6/land{i}'))
        sm.hits.append(dict(stage='main', t=t + FEATHER_T, hk=key, idx=i - 1, tell=t, grp=0, kb=KB0, bol=0, shape='pj_bolt',
                            cond=None))
    if not K.prop('feather'):
        for t in range(vol[0] + 1, vol[-1] + FEATHER_T, 2):
            st.at(t, f'execute as {p_of(key, "rlk_kn_fth")} at @s run {part(S.DUST[2], 0.1, 0.1, 0.1, 0, 3)}')
    # orbs 110: eight crimson orbs gather around her; toss 125: they fly to the rim (r 22, 45 deg apart) and pulse there
    W.w('p/q6/orbs', [f'# Q6 the {n_orb} orbs gather around her (@s = body, airborne).']
        + [f'execute at @s rotated {int(360 * k / n_orb)} 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ '
           f'{prop_nbt(key, "orb", "rlk_kn_q6o", f"rlk_kn_q6o{k}", "rlk_kn_new")}' for k in range(n_orb)]
        + dress('orb') + ['tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new']
        + S.fx('orb_gather', [part(S.DUST[2], 1.6, 1.0, 1.6, 0, 40)], pos='at @s') + snd('orbs_gather'))
    W.w('p/q6/toss', [f'# Q6 toss (@s = body): each orb to its rim spot (r {num(orb_rim)} from the axis, bearing k x {360 // n_orb} deg), an arc',
                      f'# of {lockt - toss - 5} t; it rests there pulsing until the impact.']
        + [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o{k}] positioned as {ARENA_M} rotated {int(360 * k / n_orb)} 0 '
           f'positioned ^ ^ ^{num(orb_rim)} positioned ~ {floor_y(0.6)} ~ run function rlk:mboss/mv/leap {{t:{lockt - toss - 5},h:40}}'
           for k in range(n_orb)] + snd('orbs_toss'))
    st.at(orbs, fn('p/q6/orbs'))
    st.at(toss, fn('p/q6/toss'))
    if not K.prop('orb'):
        for t in range(orbs + 1, impact, 3):
            st.at(t, f'execute as {p_of(key, "rlk_kn_q6o")} at @s run {part(S.DUST[2], 0.25, 0.25, 0.25, 0, 4)}')
    # lock 140 (the player's spot, mv/ok, 1.5 b toward her: she lands in front of them), dive 160 over 8 t, impact 168:
    # the landing disc + every orb's disc, one volley group (Bond of Life), the last hit of the cast
    st.at(lockt, fn('core/lockp'), fn('core/lock_short'), f'execute at @s facing entity {LOCK_M} feet run tp @s ~ ~ ~ ~ 0',
          look('glow', 'crimson'), snd('dash_tell'))
    st.at(dive, f'execute positioned as {LOCK_M} run function rlk:mboss/mv/glide {{t:{impact - dive}}}',
          S.fx('dive_streak', [], pos=f'{AT_BODY} positioned ~ ~1 ~', len=int(hy * 10)), snd('fall_dive'))
    if not K._on():
        for t in range(dive + 1, impact):
            st.at(t, f'execute at @s run {part(S.DUST[2], 0.3, 0.8, 0.3, 0, 12)}')
    g = st.group(impact - 1)
    st.hit(key, 6, tell=lockt, grp=g, kb=KB1, pos=at_floor(LOCK_M))
    oh = api.HITS[key][7]
    assert oh[2] == 'orb_discs'
    oh_disc = (oh[0], oh[1], 'disc', (orb_r,), oh[4], oh[5])
    for k in range(n_orb):
        st.at(impact - 1, S.hazard(key, oh_disc, grp=True, kb=KB1, pos=f'at @e[type=minecraft:item_display,tag=rlk_kn_q6o{k},limit=1] '
                                                                       f'positioned ~ {CY} ~'))
    sm.hits.append(dict(stage='main', t=impact, hk=key, idx=7, tell=toss, grp=g, kb=KB1, bol=1, shape='orb_discs', cond=None))
    st.at(impact, S.bol_mark())
    burst = (S.fx_impact(4.0, BOL_C, pos=at_floor(LOCK_M)) + snd('fall_impact', f'at {LOCK_M}')
             + S.fx('orb_burst', [part(S.DUST[2], 2.0, 0.6, 2.0, 0, 50), part('minecraft:explosion', 1, 0.2, 1, 0, 1)],
                    pos=f'as {p_of(key, "rlk_kn_q6o")} at @s positioned ~ {CY} ~', r=int(orb_r * 10))
             + snd('orb_burst', f'at {ARENA_M}') + [f'kill {p_of(key, "rlk_kn_q6o")}'])
    st.at(impact, sm.sub('impact', ['# Q6 the impact (@s = body): the landing burst, every orb bursts.'] + burst))
    st.at(impact + 8, look('glow', 'normal'))
    st.end(end)
    if K._on():
        sm.cancel.append(K.fixed('clear'))
    return sm.write()


# ------------------------------------------------------------------------------------------------- resume (kit props)
def write_resume(W, key, kinds):
    """p/<key>/resume: the kit prop looks again (pause cleared the kit cards). Only with the kit (stand-ins keep their items)."""
    if not K._on() or not kinds:
        return
    lines = [f'# {key.upper()} resume (@s = body): the prop looks again (pause cleared the kit cards).']
    for tag, kind in kinds:
        lines.append(f'execute as {p_of(key, tag)} run {K.prop(kind)}')
    W.w(f'p/{key}/resume', lines)


def _q(key, f, kinds=()):
    def build(W):
        f(W)
        write_resume(W, key, kinds)
    return build


PATTERNS = [
    api.Pattern('q0', S.TID['q0'], ('q0_hover', 'q0_dive'), _q('q0', build_q0),
                notes='P2 opener: far hover until the player moves 1.5 b or 80 t, the dive (BoL) + blade ring (BoL)'),
    api.Pattern('q1', S.TID['q1'], ('q1', 'idle2'), _q('q1', build_q1, (('rlk_kn_cres', 'crescent'),)),
                notes='twin string, 3 / 5 / 6 hits, returning crescents'),
    api.Pattern('q2', S.TID['q2'], ('q2', 'idle2'), _q('q2', build_q2, (('rlk_kn_wheel', 'wheel'),)),
                notes='wheel burst at the lock, the dash to 1.5 b in front of the player, the slash when in reach'),
    api.Pattern('q3', S.TID['q3'], ('q3', 'q1', 'idle2'), _q('q3', build_q3, (('rlk_kn_cres', 'crescent'),)),
                notes='rear whip-spin, then Q1 h1-h3 (near) or two crescents'),
    api.Pattern('q4', S.TID['q4'], ('q4_up', 'q4_shot', 'q4_land'), _q('q4', build_q4),
                notes='rise, 1-3 beams (BoL) 50 t apart, land'),
    api.Pattern('q5a', S.TID['q5a'], ('q5a',), _q('q5a', build_q5a),
                notes='forced bond, window 22-121, disc / donut / wide disc (BoL) with ring_o / donut_o outlines'),
    api.Pattern('q5b', S.TID['q5b'], ('q5b',), _q('q5b', build_q5b),
                notes='forced bond, window 22-96, the X, rapid slashes, the non-lethal per-mille final (BoL)'),
    api.Pattern('q6', S.TID['q6'], ('q6',), _q('q6', build_q6, (('rlk_kn_fth', 'feather'), ('rlk_kn_q6o', 'orb'))),
                notes='rise, six feather volleys, eight rim orbs, the dive + orb bursts (BoL)'),
]
assert sorted(p.key for p in PATTERNS) == sorted(api.P2)
