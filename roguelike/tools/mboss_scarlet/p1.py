"""Phase-1 patterns of 홍련 (PLAN §4.3; OWNER: S3): A1 회전 반월참, A2 역습 일섬, A3 오연 반월, A4 월하 낙참 + A5 공중 원륜,
A6 후방 섬보 (+ line 12), A9 황광 원참, A10 황광 낙참 (footage sheets S:hr/ref, PLAN §10 P1). P2 plays the same entries
with the same timings (question 5 default 'footage'); in P2 every leap / dash / blink also leaves the lilac afterimage.

Every hit tick comes from api.ev (the clip events), every shape / size / tier / knockback from api.HITS, the moves from
api.TRACK / A3_GLIDE / LEAP_H / A4_TRAVEL / A10_DRIFT / DASH_LEN / A9_BEYOND / A6_TRIGGER. Every hazard is quiet
(#hzQuiet 1), Electro 1U, without any floor decal (PLAN §1.4: none in the footage); the tells are the pose (the rig clip
from tick 0), the blade glints, the yellow tell (A9, A10), the sounds and the sword-qi at the contact tick. The aim (body
yaw, the locked spot) locks at least api.LOCK_LEAD ticks before each hit: A9's spot locks at cut - LOCK_LEAD (21; its
clip 'lock' event is 22, one tick later). Chains re-aim <= TRACK deg / t and step TRACK step b / t toward the player
(stop at TRACK min), only the last hit of a chain knocks back (the HITS kb column). Every end point (landing, dash end,
blink) passes mv/ok inside api.MOVE_R: the lock spot is pulled toward the axis until mv/ok passes (the guaranteed
fallback is the axis side of the player -> C line), dashes and the blink are probed in 0.5 b steps through mv/ok.

TABLE[key] = the recorded hits (tick, HITS index, first visible motion, volley group, kb, shape, tier, dims) for the
tests (pat_p1.py); MOVES[key] = the body move ticks.
"""
from . import api
from . import s3lib as S
from .s3lib import PB, sset, fn, num, part, placed

K = api.K

E = api.ev
OBJ = api.OBJ
CY = api.CY
FACE = 'function rlk:mboss/mv/face'
P2 = f'if score #ph {OBJ} matches {api.PH["p2"]}'
TABLE, MOVES = {}, {}
TRK = api.TRACK


def look(ch, v):
    return api.rig(f'look/{ch}/{v}')


def track_to(pb, prev, t, deg=TRK['deg']):
    """Re-face: turn toward the player from prev + 1 until LOCK_LEAD ticks before the hit at t (the aim locks there)."""
    pb.track(prev + 1, t - S.LOCK, deg)


def step_in(pb, prev, t):
    """The chain step: TRACK step b / t toward the player on prev + 2 .. t - 2 while farther than TRACK min."""
    pb.advance(prev + 2, t - 2, TRK['step'], TRK['min'])


def afterimage(length=20):
    """The lilac afterimage of a leap / dash / blink (kit afterimage {len}); P2 only (PLAN §4.4)."""
    return [S.gate(P2, c) for c in S.fx('afterimage', pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=int(length))]


def follow(lines):
    """F2 (HR-23): kit lines whose cards follow her body (fx/follow_on .. follow_off; @s = the body in a pattern tick)."""
    lines = [x for x in lines if x]
    on, off = api.K.fixed('follow_on'), api.K.fixed('follow_off')
    return [on] + lines + [off] if lines and on else lines


def at_anchor(anchor, lines):
    """Kit lines at a rig anchor (rig/anchor/<a> moves the one rlk_hr_anchor marker; the stand-in rig places it too)."""
    lines = [x for x in lines if x]
    if not lines:
        return []
    return [api.rig(f'anchor/{anchor}')] + placed(lines, f'at {S.ANCHOR_M} rotated as @s')


def lock_fn(pb, key):
    """p/<key>/lockp: the lock marker (rlk_hr_lock + the pattern tags) at the player's feet on the floor, pulled toward
    the axis until mv/ok passes (core/clamp: inside MOVE_R, feet and head free)."""
    pb.W.w(f'p/{key}/lockp', [
        f'# {key.upper()}: lock the player\'s spot (@s = the body). The marker rlk_hr_lock carries the pattern tags (its cancel',
        '# kills it); core/clamp pulls it toward the arena axis until mv/ok passes there.',
        f'kill @e[type=minecraft:marker,tag={S.LOCK_T}]',
        f'execute at {S.PLAYER} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ '
        f'{{Tags:{S.tags_nbt(api.TAGS["pat"], S.tag_p(key), S.LOCK_T)}}}',
        sset('#t4', 0),
        f'execute as {S.LOCK_M} at @s run {fn("core/clamp")}'])
    return fn(f'p/{key}/lockp')


def ground(pb):
    """A cancel of an airborne pattern puts her back on the floor (core/ground: the spot below when mv/ok, else C)."""
    pb.cancel_lines.append(f'execute as {S.BODY} at @s run {fn("core/ground")}')


def finish(pb, key):
    pb.write()
    TABLE[key] = pb.hits
    MOVES[key] = pb.motions
    return pb


# ================================================================================================= A1 회전 반월참
def build_a1(W):
    key = 'a1'
    pb = PB(key, W)
    hit, glint, fan, end = E(key, 'hit'), E(key, 'glint'), E(key, 'fan'), E(key, 'end')
    # the pivot (0-3: the brim swings round, <= 60 deg / t toward a player beside / behind her), then the tracking until
    # the aim locks at hit - LOCK_LEAD (7 = the clip's lock event)
    pb.at(0, api.play(key), 'function rlk:mboss/mv/turn {max:60}')
    pb.track(1, 3, 60)
    pb.track(4, hit - S.LOCK, TRK['deg'])
    pb.at(glint, at_anchor('blade_tip', S.fx_lines('glint', [part(S.DUST['magenta'], 0.05, 0.05, 0.05, 0, 6)], c=api.C_MAGENTA)))
    pb.at(fan, S.fx('qi_fan', [part(S.DUST['magenta'], 0.3, 0.8, 0.3, 0, 14)], pos=f'{S.AT_BODY} positioned ^ ^1.1 ^1.2',
                    h=16, c=api.C_MAGENTA), S.snd('a1_fan'))
    pb.hit(0, tell_from=0)
    pb.at(hit, S.fx_arc(api.HITS[key][0][3][0], api.C_LILAC), S.snd('a1_hit'))
    pb.end(end)
    return finish(pb, key)


# ================================================================================================= A2 역습 일섬
def build_a2(W):
    key = 'a2'
    pb = PB(key, W)
    hit, draw, end = E(key, 'hit'), E(key, 'draw'), E(key, 'end')
    pb.at(0, FACE, api.play(key),
          at_anchor('blade_mid', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    track_to(pb, 0, hit)
    pb.at(draw, S.snd('a2_draw'))
    pb.hit(0, tell_from=0)
    pb.at(hit, S.fx_arc(api.HITS[key][0][3][0], api.C_LILAC, roll=35), S.snd('a2_hit'))
    pb.end(end)
    return finish(pb, key)


# ================================================================================================= A3 오연 반월
# per hit: (event, kit visual, roll / yaw of it, b ahead of her) — h1 / h3 / h4 vertical crescents (qi_vert), h2 the downward
# diagonal (qi_arc roll -35), h5 the rising wedge (qi_wedge roll 40). F2 (HR-12): the kit stands them across her aim (the
# player's view): h1 bulging to her right (the player's LEFT, the footage's 'at Eve's left'), h3 to her left, h4 2 b out,
# toward where its thrust line reaches (still before a player at TRACK min 2.4 b: first person sees it too)
A3_FX = {'h1': ('vert', 0, 1.4), 'h2': ('arc', -35, 0), 'h3': ('vert', 180, 1.4), 'h4': ('vert', 0, 2.0), 'h5': ('wedge', 40, 0)}


def a3_fx(ev_, r):
    kind, roll, ahead = A3_FX[ev_]
    if kind == 'vert':
        return S.fx('qi_vert', [part(S.DUST['lilac'], 0.2, 1.0, 0.2, 0, 20)], pos=f'{S.AT_BODY} positioned ^ ^0.2 ^{num(ahead, 1)}',
                    h=34, yaw=roll, c=api.C_LILAC)
    if kind == 'arc':
        return S.fx_arc(r, api.C_LILAC, roll=roll)
    return S.fx('qi_wedge', [part(S.DUST['lilac'], 0.5, 0.7, 0.5, 0, 20)], pos=f'{S.AT_BODY} positioned ~ ~1.3 ~',
                r=int(round(r * 10)), roll=roll)


def build_a3(W):
    key = 'a3'
    pb = PB(key, W)
    hs = ['h1', 'h2', 'h3', 'h4', 'h5']
    end = E(key, 'end')
    reach, glide_v, glide_t = api.A3_GLIDE
    pb.at(0, FACE, api.play(key),
          at_anchor('blade_mid', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    # from 4.5-8 b she glides in A3_GLIDE b / t during 0-14 (the AI picks A3 from mid only up to MID_MAX 8 b); nearer,
    # the same steps bring her to TRACK min before h1
    pb.advance(1, glide_t - 1, glide_v, TRK['min'])
    pb.at(1, *afterimage(int(glide_v * glide_t * 10)))
    prev = 0
    for i, ev_ in enumerate(hs):
        t = E(key, ev_)
        if i == 0:
            track_to(pb, 0, t)
        else:
            track_to(pb, prev, t)
            if ev_ == 'h2':
                # the short lunge before h2 (1.5 b in 4 t), PLAN §4.3
                pb.advance(prev + 2, t - 5, TRK['step'], TRK['min'])
                pb.advance(t - 4, t - 1, 0.375, TRK['min'])
            else:
                step_in(pb, prev, t)
        pb.hit(i, tell_from=0 if i == 0 else prev)
        pb.at(t, a3_fx(ev_, api.HITS[key][i][3][0]), S.snd(f'a3_{ev_}'))
        prev = t
    pb.end(end)
    return finish(pb, key)


# ================================================================================================= A4 월하 낙참 + A5 공중 원륜
def build_a4(W):
    key = 'a4'
    pb = PB(key, W)
    leap, apex, glint, lock, flip, dive, hit = (E(key, k) for k in ('leap', 'apex', 'glint', 'lock', 'flip', 'dive', 'hit'))
    slash, lock2, ring, hit2, land, end = (E(key, k) for k in ('slash', 'lock2', 'ring', 'hit2', 'land', 'end'))
    h = api.LEAP_H[key]
    pb.at(0, FACE, api.play(key))
    pb.track(1, leap - 1, TRK['deg'])
    # the leap: rises LEAP_H b in apex - leap ticks and travels <= A4_TRAVEL b toward the player (stopping 2 b short of
    # them, probed on the floor through mv/ok), then hangs at the apex until the dive
    W.w(f'p/{key}/leap', [
        f'# A4 leap (@s = the body, tick {leap}): the floor point <= {num(api.A4_TRAVEL)} b toward the player (probe), then a',
        f'# straight rise of {num(h)} b to above it in {apex - leap} t.',
        'function rlk:mboss/mv/dist',
        f'scoreboard players operation #t {OBJ} = #mbDist mb',
        f'scoreboard players remove #t {OBJ} 20',
        f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches ..-1 run {sset("#t", 0)}',
        f'execute if score #t {OBJ} matches {int(api.A4_TRAVEL * 2) + 1}.. run {sset("#t", int(api.A4_TRAVEL * 2))}',
        f'execute at @s facing entity {S.PLAYER} feet rotated ~ 0 run {fn("core/dash/probe")}',
        f'execute positioned as {S.PROBE_M} positioned ~ {CY + h} ~ run function rlk:mboss/mv/glide {{t:{apex - leap}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'])
    pb.at(leap, fn(f'p/{key}/leap'), S.snd('leap'), *afterimage(int(h * 10)))
    pb.motions.append((leap, apex, 'leap'))
    pb.at(glint, at_anchor('blade_tip', S.fx_lines('glint', [part(S.DUST['magenta'], 0.1, 0.1, 0.1, 0, 8)], c=api.C_MAGENTA)),
          S.snd('a4_glint'))
    pb.track(apex, lock - 1, TRK['deg'])
    pb.at(lock, lock_fn(pb, key), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0')
    # F2 (HR-23): the ribbon's cards follow her (the dive 16-20 takes it down to the lock spot)
    pb.at(flip, follow(S.fx('qi_ribbon', [part(S.DUST['lilac'], 0.4, 0.6, 0.4, 0, 16)])), S.snd('a4_flip'))
    # the dive onto the locked spot (dive .. hit), the landing disc there
    pb.at(dive, f'execute positioned as {S.LOCK_M} run function rlk:mboss/mv/glide {{t:{hit - dive}}}')
    pb.motions.append((dive, hit, 'dive'))
    g = pb.group(hit - 1)
    pb.hit(0, tell_from=0, grp=g, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    pb.at(hit, S.fx('dive_impact', [part(S.DUST['lilac'], 1.0, 0.1, 1.0, 0, 30)], pos=f'at {S.LOCK_M} positioned ~ {CY + 0.1} ~',
                    r=26), S.snd('a4_impact', pos=f'at {S.LOCK_M}'))
    # A5: the straight slash line (cosmetic), the aim locks again (lock2), she spins ~1 b off the ground, the ring round her
    pb.track(hit + 1, lock2 - 1, TRK['deg'])
    # F2 (HR-12): the kit's qi_line runs across her facing (to her right): from 5 b on her left, 10 b, 1.5 b ahead of her
    # (the footage's long horizontal slash from the frame's left edge)
    pb.at(slash, S.fx('qi_line', [part(S.DUST['lilac'], 0.6, 0.1, 0.6, 0, 10)], pos=f'{S.AT_BODY} positioned ^5 ^1.2 ^1.5',
                      len=100))
    pb.at(ring, f'execute at @s positioned ~ {CY + 1} ~ run function rlk:mboss/mv/glide {{t:2}}',
          S.fx('qi_ring', [part(S.DUST['lilac'], 1.2, 0.05, 1.2, 0, 24)], pos=f'{S.AT_BODY} positioned ~ ~2.0 ~', r=30,
               c=api.C_LILAC))
    pb.at(E(key, 'ring') + 2, S.snd('a5_spin'))
    pb.motions.append((ring, ring + 2, 'rise'))
    pb.hit(1, tell_from=hit)
    pb.at(hit2, f'execute at @s positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:{land - hit2}}}')
    pb.motions.append((hit2, land, 'land'))
    pb.end(end)
    ground(pb)
    return finish(pb, key)


# ================================================================================================= A6 후방 섬보
def build_a6(W):
    key = 'a6'
    pb = PB(key, W)
    A = api.A6_TRIGGER
    gone, appear, settle = E(key, 'gone'), E(key, 'appear'), E(key, 'settle')
    back = int(A['glide'] * 2)
    side_lo, side_hi = int(A['side'][0] * 2), int(A['side'][1] * 2)
    # the blink: 12 b straight back in 3 t (probed through mv/ok); blocked short of 8 b -> 8-10 b to a side (left, then
    # right), the longest probe wins. rlk_mb_inv 0-4 is the core's (core/run/a6).
    W.w(f'p/{key}/blink', [
        f'# A6 blink (@s = the body, tick 0): probe {num(A["glide"])} b straight back from the player, else {num(A["side"][0])}-'
        f'{num(A["side"][1])} b to the left / right; glide there in {A["glide_t"]} t.',
        sset('#t', back),
        f'execute at @s facing entity {S.PLAYER} feet rotated ~180 0 run {fn("core/dash/probe")}',
        f'scoreboard players operation #{key}_n {OBJ} = #t2 {OBJ}',
        f'execute if score #{key}_n {OBJ} matches {side_lo}.. run return run {fn(f"p/{key}/go")}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        sset('#t', side_hi),
        f'execute at @s facing entity {S.PLAYER} feet rotated ~90 0 run {fn("core/dash/probe")}',
        f'execute if score #t2 {OBJ} matches {side_lo}.. run return run {fn(f"p/{key}/go")}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'execute at @s facing entity {S.PLAYER} feet rotated ~-90 0 run {fn("core/dash/probe")}',
        f'execute if score #t2 {OBJ} matches {side_lo}.. run return run {fn(f"p/{key}/go")}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        sset('#t', back),
        f'execute at @s facing entity {S.PLAYER} feet rotated ~180 0 run {fn("core/dash/probe")}',
        fn(f'p/{key}/go')])
    W.w(f'p/{key}/go', [f'# A6: glide to the probe point in {A["glide_t"]} t (the probe never leaves mv/ok ground).',
                        f'execute positioned as {S.PROBE_M} run function rlk:mboss/mv/glide {{t:{A["glide_t"]}}}',
                        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'])
    pb.at(0, FACE, api.play(key), fn(f'p/{key}/blink'),
          follow(S.fx('blink_bubble', [part('minecraft:end_rod', 0.4, 0.8, 0.4, 0.02, 12)])), S.snd('a6_blink'),
          *afterimage(int(A['glide'] * 10)))
    pb.motions.append((0, A['glide_t'], 'blink'))
    pb.at(A['glide_t'], S.snd('a6_arrive'))
    pb.at(appear, FACE)
    pb.track(appear + 1, settle, TRK['deg'])
    pb.at(A['line_t'], S.line(A['line']))
    pb.end(A['next'])
    return finish(pb, key)


# ================================================================================================= A9 황광 원참
def build_a9(W):
    key = 'a9'
    pb = PB(key, W)
    spin, ring, yellow, star, flash, go, cut, end = (E(key, k) for k in ('spin', 'ring', 'yellow', 'star', 'flash', 'go',
                                                                       'cut', 'end'))
    lock = min(E(key, 'lock'), cut - S.LOCK)
    beyond, dmax = api.A9_BEYOND, api.DASH_LEN[key]
    w = api.HITS[key][0][3][0]
    pb.at(0, FACE, api.play(key))
    pb.track(1, lock - 1, TRK['deg'])
    pb.at(ring, S.fx('qi_ring', [part(S.DUST['lilac'], 1.4, 0.05, 1.4, 0, 24)], pos=f'{S.AT_BODY} positioned ~ ~1.0 ~', r=35,
                     c=api.C_LILAC))
    pb.at(yellow, S.fx('yellow_tell', [part(S.DUST['yellow'], 0.5, 0.6, 0.5, 0, 30), part('minecraft:end_rod', 1.2, 0.05, 0.05, 0, 8)],
                       t=8), S.snd('yellow_chime'))
    pb.at(star, at_anchor('chest', S.fx_lines('star4', [part(S.DUST['lilac'], 0.2, 0.2, 0.2, 0, 10)])), S.snd('a9_star'))
    pb.at(lock, lock_fn(pb, key), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0')
    pb.at(flash, [x for x in (api.K.ovl('magenta', 0, 3, 6),) if x], S.snd('a9_flash'))
    # the iai dash (go .. cut): through the locked spot to A9_BEYOND b beyond it, <= DASH_LEN b, probed through mv/ok;
    # the start point (rlk_hr_a9s) and the length (core.a9, half blocks) for the dash line
    nb, nmax = int(beyond * 2), int(dmax * 2)
    W.w(f'p/{key}/dash', [
        f'# A9 dash (@s = the body, tick {go}): through the locked spot to {num(beyond)} b beyond it, at most {num(dmax)} b, probed',
        '# in 0.5 b steps (mv/ok; p/a9/pstep); the start marker and the probed length feed the dash line at cut - 1.',
        f'kill @e[type=minecraft:marker,tag=rlk_hr_a9s]',
        f'execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["pat"], S.tag_p(key), "rlk_hr_a9s")}}}',
        f'execute at @s facing entity {S.LOCK_M} feet run tp @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] ~ ~ ~ ~ 0',
        sset('#t', nmax), sset('#t2', 0),
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["pat"], S.PROBE_T)}}}',
        f'execute at @s facing entity {S.LOCK_M} feet as {S.PROBE_M} run tp @s ~ ~ ~ ~ 0',
        f'execute as {S.PROBE_M} at @s run {fn(f"p/{key}/pstep")}',
        f'scoreboard players operation #{key}_n {OBJ} = #t2 {OBJ}',
        f'execute positioned as {S.PROBE_M} run function rlk:mboss/mv/glide {{t:{cut - go}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'data modify storage {api.STORAGE} core.a9 set value {{len:0,w:{int(round(w * 10))},tell:1,dmg:{api.DMG[api.HITS[key][0][4]]}}}',
        f'execute store result storage {api.STORAGE} core.a9.len int 5 run scoreboard players get #{key}_n {OBJ}'])
    W.w(f'p/{key}/pstep', [
        f'# A9 probe step (@s = the probe, at / rotated as it): 0.5 b on while mv/ok passes, at most #t steps; once within 0.5 b',
        f'# of the locked spot the cap becomes {nb} more steps ({num(beyond)} b beyond it).',
        f'execute if score #t2 {OBJ} >= #t {OBJ} run return 0',
        f'execute if entity {S.LOCK_M[:-1]},distance=..0.5,tag=!rlk_hr_a9p] run {fn(f"p/{key}/past")}',
        'execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0',
        'tp @s ^ ^ ^0.5',
        f'scoreboard players add #t2 {OBJ} 1',
        f'execute at @s run {fn(f"p/{key}/pstep")}'])
    W.w(f'p/{key}/past', [f'# A9 probe at the locked spot (once): the cap = the steps so far + {nb}, at most {nmax}.',
                          f'scoreboard players operation #t {OBJ} = #t2 {OBJ}', f'scoreboard players add #t {OBJ} {nb}',
                          f'execute if score #t {OBJ} matches {nmax + 1}.. run {sset("#t", nmax)}',
                          f'tag {S.LOCK_M} add rlk_hr_a9p'])
    pb.at(go, fn(f'p/{key}/dash'), *afterimage(int(dmax * 10)))
    pb.motions.append((go, cut, 'dash'))
    # one strike group: the dash line from the start point along the dash + the disc at the locked spot (one landing)
    g = pb.group(cut - 1)
    hl = S.hz_opts(api.HITS[key][0][5], grp=True)
    hl += [f'execute at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,'
           f'limit=1] positioned ~ {CY} ~ run function rlk:mboss/hz/line with storage {api.STORAGE} core.a9', S.hz_tag(key)]
    pb.at(cut - 1, hl)
    pb.hits.append(dict(t=cut, idx=0, tell=0, grp=g, kb=api.HITS[key][0][5], shape='dash_line', tier=api.HITS[key][0][4],
                        dims=api.HITS[key][0][3]))
    pb.hit(1, tell_from=0, grp=g, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    # F2 (HR-24): the streak as long as the probed dash (core.a9.len, tenths: the hazard line's own length), not dmax
    a9s = 'at @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_a9s,limit=1] positioned ~ ~1.0 ~'
    pb.at(cut, placed([K.pw('qi_cut', f'{api.STORAGE} core.a9')] if K.pw('qi_cut', f'{api.STORAGE} core.a9')
                      else [part(S.DUST['magenta'], 2.0, 0.2, 0.2, 0, 30)], a9s),
          S.fx('qi_ring', [part(S.DUST['magenta'], 1.6, 0.05, 1.6, 0, 24)], pos=f'at {S.LOCK_M} positioned ~ ~1.0 ~', r=40,
               c=api.C_MAGENTA), S.snd('a9_cut'))
    # recovery: she stands beyond the player, back turned, then turns (cut + 12 ..)
    pb.at(cut + 1, f'kill @e[type=minecraft:marker,tag=rlk_hr_a9s]')
    pb.track(cut + 12, end - 1, TRK['deg'])
    pb.end(end)
    return finish(pb, key)


# ================================================================================================= A10 황광 낙참
def build_a10(W):
    key = 'a10'
    pb = PB(key, W)
    spring, apex, yellow, lock, dive, hit, end = (E(key, k) for k in ('spring', 'apex', 'yellow', 'lock', 'dive', 'hit', 'end'))
    h, drift = api.LEAP_H[key], api.A10_DRIFT
    rise_t = apex - spring
    pre = round(drift * rise_t, 2)
    pb.at(0, FACE, api.play(key))
    pb.track(1, spring - 1, TRK['deg'])
    # the spring: LEAP_H b straight up while drifting <= A10_DRIFT b / t toward the player (the rise is one glide to a
    # point up to drift x rise_t b toward them, never past 1.5 b of them), then per tick at the apex until the lock
    W.w(f'p/{key}/spring', [
        f'# A10 spring (@s = the body, tick {spring}): up {num(h)} b in {rise_t} t, drifting <= {num(pre)} b toward the player.',
        'function rlk:mboss/mv/dist',
        f'scoreboard players operation #t {OBJ} = #mbDist mb',
        f'scoreboard players remove #t {OBJ} 15',
        f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches ..-1 run {sset("#t", 0)}',
        f'execute if score #t {OBJ} matches {int(pre * 2) + 1}.. run {sset("#t", int(pre * 2))}',
        f'execute at @s facing entity {S.PLAYER} feet rotated ~ 0 run {fn("core/dash/probe")}',
        f'execute positioned as {S.PROBE_M} positioned ~ {CY + h} ~ run function rlk:mboss/mv/glide {{t:{rise_t}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'])
    W.w(f'p/{key}/drift', [
        f'# A10 apex drift (@s = the body, ticks {apex + 1}-{lock - 1}): {num(drift)} b toward the player while farther than 1.5 b',
        '# (horizontal; the floor point below must pass mv/ok).',
        f'execute at @s positioned ~ {CY} ~ if entity {S.PLAYER[:-1]},distance=..1.5] run return 0',
        f'execute at @s facing entity {S.PLAYER} feet rotated ~ 0 positioned ^ ^ ^{num(drift)} positioned ~ {CY} ~ if function '
        f'rlk:mboss/mv/ok at @s facing entity {S.PLAYER} feet rotated ~ 0 positioned ^ ^ ^{num(drift)} run tp @s ~ ~ ~'])
    pb.at(spring, fn(f'p/{key}/spring'), S.snd('leap'), *afterimage(int(h * 10)))
    pb.motions.append((spring, apex, 'rise'))
    pb.rng(apex + 1, lock - 1, fn(f'p/{key}/drift'))
    pb.motions.append((apex + 1, lock - 1, 'drift'))
    pb.track(apex + 1, lock - 1, 20)
    # F2 (HR-23): the tell's cards follow her through the apex drift
    pb.at(yellow, follow(S.fx('yellow_tell', [part(S.DUST['yellow'], 0.5, 0.6, 0.5, 0, 30),
                                               part('minecraft:end_rod', 1.2, 0.05, 0.05, 0, 8)], t=8)), S.snd('yellow_chime'))
    pb.at(lock, lock_fn(pb, key), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0')
    pb.at(dive, f'execute positioned as {S.LOCK_M} run function rlk:mboss/mv/glide {{t:{hit - dive}}}',
          S.fx('claw_streaks', [part(S.DUST['lilac'], 0.6, 2.0, 0.6, 0, 20)], pos=f'at {S.LOCK_M} positioned ~ {CY + 2} ~', r=15),
          S.snd('a10_dive'))
    pb.motions.append((dive, hit, 'dive'))
    pb.hit(0, tell_from=0, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    pb.at(hit, S.fx('burst_radial', [part(S.DUST['lilac'], 1.4, 0.2, 1.4, 0, 36), part('minecraft:end_rod', 0.2, 1.5, 0.2, 0.05, 10)],
                    pos=f'at {S.LOCK_M} positioned ~ {CY + 0.1} ~', r=35), S.snd('a10_impact', pos=f'at {S.LOCK_M}'))
    pb.end(end)
    ground(pb)
    return finish(pb, key)


BUILD = {'a1': build_a1, 'a2': build_a2, 'a3': build_a3, 'a4': build_a4, 'a6': build_a6, 'a9': build_a9, 'a10': build_a10}
NOTES = {'a1': 'counter (beside / behind): the flat crescent', 'a2': 'counter (in front): the hook slash',
         'a3': 'five crescents, tracking', 'a4': 'moon-leap dive + the aerial ring (A5)', 'a6': 'back-blink + line 12 (trigger only)',
         'a9': 'yellow tell, magenta flash, iai dash + disc', 'a10': 'yellow tell in the air, the plunge'}


def _mk(key):
    def build(W):
        BUILD[key](W)
    return build


PATTERNS = [api.Pattern(k, S.TID[k], (k,), _mk(k), notes=NOTES[k]) for k in api.P1]
assert [p.key for p in PATTERNS] == list(api.P1)
