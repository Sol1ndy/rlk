"""The P1 kit of 홍련 on the new combat (hr_design §2.1-2.2; lane H1): A1 회전 반월참, A2 역습 일섬, A3 오연 반월, A3s 쌍월참,
A4 월하 낙참 + 공중 원륜, A6 후방 섬보 (+ line 12), A9 황광 원참, A10 황광 낙참, D4 원월 사연, TRI 돌진 삼월참, RINGS 회전 월륜,
ULT 공간 참 (only after RINGS at a full gauge), HCUT 황광 섬월, BLUE 청광 돌파, KCUT 황광 난참. P2 plays the same entries
(shorter cooldowns and recoveries) + p_ghost.py's three.

Every hit tick comes from api.ev (the clip events), every shape / size / tier / knockback / parry class from api.HITS. A
parryable hit (P) is announced by the parry cue exactly api.CUE_LEAD t before it (the pink glint at her blade + its chime,
PB.hit adds it), an unparriable hit (N) by the module's own flash on her chest (api.FLASH_AT: yellow >= 12 t before, purple
exactly 12 t before, blue: the sphere 15 t) and is made with hz_opts(noparry=1). Every hazard is quiet (#hzQuiet 1),
Electro 1U, without any floor decal. The aim (body yaw, the locked spot) locks api.LOCK_LEAD ticks before each hit; chains
re-aim <= TRACK deg / t and step TRACK step b / t toward the player (stop at TRACK min); only the last hit of a chain
knocks back. Every end point (landing, dash end, blink) passes mv/ok inside api.MOVE_R. A perfect parry on the last / single
hit of a ground pattern ends it early (PB.pp_window -> core/pp: the flinch, api.PP_FLINCH t).

TABLE[key] = the recorded hits (tick, HITS index, first visible motion, volley group, kb, shape, tier, dims, parry, cue,
flash, phase) for the tests (pat_p1.py); MOVES[key] = the body move ticks; CUES / FLASHES[key] the cue / flash ticks.
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
TABLE, MOVES, CUES, FLASHES, PPW = {}, {}, {}, {}, {}
TRAILS = {}                         # F1 (HR-28): key -> the pattern ticks of its trail (tests)
TAILS = {}                          # F1 round 1 (HR-14): key -> the pattern tick her tail move starts (ai/tail; tests)
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


def trail(pb, ticks, length=15):
    """F1 (HR-28, lead decision 11-05): the trail of a leap / spring / dive along her motion, in both phases (PLAN §4.3 A4 /
    A10; the P2-only afterimage stays on A3 / A6 / A9, §4.4): the kit afterimage {len} at her body on each of `ticks` (the
    move's start, middle and end: the fading silhouettes trace the path; each with a short streak)."""
    for t in ticks:
        pb.at(t, S.fx('afterimage', pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=int(length)))
        TRAILS.setdefault(pb.key, []).append(t)


def tail(pb, last_hit, end, moved=0):
    """F1 (HR-14, lead decision 11-05): the pattern ends PAT_END (8-12 t after its last hit); in the tail kept she turns to
    track the player on every tick and (F1 round 1, VF1R-01: "she walks / strafes facing and tracking the player") after
    api.TAIL_MOVE t of the clip's follow-through (and not before `moved`: A4 lands first) moves as the recovery does
    (ai/tail: walk / P2 glide in beyond 6 b, else a strafe, with its clip; ai/tail_step each later tick); the AI recovery
    keeps that move (the punish window)."""
    pb.track(last_hit + 1, end - 1, TRK['deg'])
    t = max(last_hit + api.TAIL_MOVE, moved)
    assert last_hit < t < end - 1, (pb.key, last_hit, t, end)
    pb.at(t, fn('ai/tail'))
    pb.rng(t + 1, end - 1, fn('ai/tail_step'))
    pb.motions.append((t + 1, end - 1, 'tail move'))
    TAILS[pb.key] = t
    pb.end(end)


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
    CUES[key], FLASHES[key], PPW[key] = sorted(pb.cues), sorted(pb.flashes, key=lambda x: x[1]), pb.pp
    TRAILS[key] = sorted(set(TRAILS.get(key, [])))
    return pb


# ================================================================================================= A1 회전 반월참
A1_ROLL = -25        # V2 (HR-48): the hit crescent's roll (A2 35, A3 h2 -35); -25 = the flattest that stands across the aim


def build_a1(W):
    key = 'a1'
    pb = PB(key, W)
    hit, fan, end = E(key, 'hit'), E(key, 'fan'), api.PAT_END[key]
    # the pivot (0-3: the brim swings round, <= 60 deg / t toward a player beside / behind her), then the tracking until
    # the aim locks at hit - LOCK_LEAD (7 = the clip's lock event)
    pb.at(0, api.play(key), 'function rlk:mboss/mv/turn {max:60}')
    pb.track(1, 3, 60)
    pb.track(4, hit - S.LOCK, TRK['deg'])
    # V2 (HR-48, D4-02 / DF-01): the fan back at S2a's h 16 (toward the footage's ~ 1-body-height fan; S2d's x 0.78 made it
    # 13: 189 card px from the default F5 camera), centred at the body + 1.1 so its foot stays 0.3 b over the floor
    pb.at(fan, S.fx('qi_fan', [part(S.DUST['magenta'], 0.3, 0.8, 0.3, 0, 14)], pos=f'{S.AT_BODY} positioned ^ ^1.1 ^1.2',
                    h=16, c=api.C_MAGENTA), S.snd('a1_fan'))
    pb.hit(0, tell_from=0)
    # V2 (HR-48): the crescent rolled A1_ROLL (it stands across her aim, as A2's): flat at the body + 1.0 it lay 0.62 b under
    # the first-person eye and wrapped round the player, >= 1 500 card px on one tick of seven in first person
    pb.at(hit, S.fx_arc(api.HITS[key][0][3][0], api.C_LILAC, roll=A1_ROLL), S.snd('a1_hit'))
    pb.pp_window(hit)
    tail(pb, hit, end)
    return finish(pb, key)


# ================================================================================================= A2 역습 일섬
def build_a2(W):
    key = 'a2'
    pb = PB(key, W)
    hit, draw, glow, end = E(key, 'hit'), E(key, 'draw'), E(key, 'glow'), api.PAT_END[key]
    pb.at(0, FACE, api.play(key),
          at_anchor('blade_mid', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    track_to(pb, 0, hit)
    pb.at(draw, S.snd('a2_draw'))
    # F1 (HR-22, lead decision 11-05): the lilac glow along the blade 6-11 (PLAN §4.3, the clip's 'glow' event; the blade look
    # is the module's, contract §3.2), off at the hit and in the cancel (A6 may cancel the windup while it glows)
    pb.at(glow, look('blade', 'lilac'))
    pb.cancel_lines.append(f'execute as {S.BODY} run {look("blade", "off")}')
    pb.hit(0, tell_from=0)
    pb.at(hit, S.fx_arc(api.HITS[key][0][3][0], api.C_LILAC, roll=35), S.snd('a2_hit'), look('blade', 'off'))
    pb.pp_window(hit)
    tail(pb, hit, end)
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
        return S.fx('qi_vert', [part(S.DUST['lilac'], 0.2, 1.0, 0.2, 0, 20)], pos=f'{S.AT_BODY} positioned ^ ^0.15 ^{num(ahead, 1)}',
                    h=27, yaw=roll, c=api.C_LILAC)
    if kind == 'arc':
        return S.fx_arc(r, api.C_LILAC, roll=roll)
    return S.fx('qi_wedge', [part(S.DUST['lilac'], 0.5, 0.7, 0.5, 0, 20)], pos=f'{S.AT_BODY} positioned ~ ~1.0 ~',
                r=int(round(r * 10)), roll=roll)


def build_a3(W, key='a3'):
    """A3 오연 반월 (five crescents) and A3s 쌍월참 (the same opening cut after h2: the player cannot tell the two apart
    before tick 38): clip a3, the hits of api.HITS[key]."""
    pb = PB(key, W)
    hs = [h[1] for h in api.HITS[key]]
    end = api.PAT_END[key]
    reach, glide_v, glide_t = api.A3_GLIDE
    pb.at(0, FACE, api.play('a3'),
          at_anchor('blade_mid', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    # from 4.5-8 b she glides in A3_GLIDE b / t during 0-14 (the AI picks them from mid only up to MID_MAX 8 b); nearer,
    # the same steps bring her to TRACK min before h1
    pb.advance(1, glide_t - 1, glide_v, TRK['min'])
    pb.at(1, *afterimage(int(glide_v * glide_t * 10)))
    prev = 0
    for i, ev_ in enumerate(hs):
        t = E('a3', ev_)
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
    pb.pp_window(prev)
    tail(pb, prev, end)
    return finish(pb, key)


def build_a3s(W):
    return build_a3(W, 'a3s')


# ================================================================================================= A4 월하 낙참 + A5 공중 원륜
def build_a4(W):
    key = 'a4'
    pb = PB(key, W)
    leap, apex, lock, flip, dive, hit = (E(key, k) for k in ('leap', 'apex', 'lock', 'flip', 'dive', 'hit'))
    slash, lock2, ring, hit2, land = (E(key, k) for k in ('slash', 'lock2', 'ring', 'hit2', 'land'))
    end = api.PAT_END[key]
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
    pb.at(leap, fn(f'p/{key}/leap'), S.snd('leap'))
    trail(pb, (leap, (leap + apex) // 2, apex))         # F1 (HR-28): both phases, along the rise
    pb.motions.append((leap, apex, 'leap'))
    # (the old magenta glint at the clip's `glint` 7 is gone: a pink glint is the parry cue now, at 13 and 27)
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
    pb.at(slash, S.fx('qi_line', [part(S.DUST['lilac'], 0.6, 0.1, 0.6, 0, 10)], pos=f'{S.AT_BODY} positioned ^5 ^0.95 ^1.5',
                      len=100))
    pb.at(ring, f'execute at @s positioned ~ {CY + 1} ~ run function rlk:mboss/mv/glide {{t:2}}',
          S.fx('qi_ring', [part(S.DUST['lilac'], 1.2, 0.05, 1.2, 0, 24)], pos=f'{S.AT_BODY} positioned ~ ~1.55 ~', r=30,
               c=api.C_LILAC))
    pb.at(E(key, 'ring') + 2, S.snd('a5_spin'))
    pb.motions.append((ring, ring + 2, 'rise'))
    pb.hit(1, tell_from=hit)
    pb.at(hit2, f'execute at @s positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:{land - hit2}}}')
    pb.motions.append((hit2, land, 'land'))
    tail(pb, hit2, end, moved=land)
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


# ================================================================================================= the dash-through helper
DS_T = api.TAGS['a9s']                       # the dash start marker (one dash pattern runs at a time)
DS_M = f'@e[type=minecraft:marker,tag={DS_T},limit=1]'
DASH_STO = f'{api.STORAGE} core.dash'


def dash_through(pb, key, go, cut, row=0, grp=True):
    """The dash of A9 / HCUT / BLUE / KCUT (@s = the body, tick `go`): through the locked spot to api.DASH_BEYOND b beyond it,
    at most api.DASH_LEN b, probed in 0.5 b steps through mv/ok; she glides there in cut - go ticks. The start marker
    (rlk_hr_a9s, rotated along the dash) and the probed length (storage core.dash {len,w,tell,dmg}) feed the dash-line
    hazard of api.HITS[key][row], made at cut - 1 (strikes at cut; grp: it joins the volley group the caller opened with
    pb.group(cut - 1) - a line alone must not join a stale group). Returns the hazard lines' position prefix."""
    W = pb.W
    beyond, dmax = api.DASH_BEYOND[key], api.DASH_LEN[key]
    h = api.HITS[key][row]
    assert h[2] == 'dash_line', (key, row)
    w = h[3][0]
    nb, nmax = int(beyond * 2), int(dmax * 2)
    W.w(f'p/{key}/dash', [
        f'# {key.upper()} dash (@s = the body, tick {go}): through the locked spot to {num(beyond)} b beyond it, at most {num(dmax)} b, probed',
        f'# in 0.5 b steps (mv/ok; p/{key}/pstep); the start marker and the probed length feed the dash line at tick {cut - 1}.',
        f'kill @e[type=minecraft:marker,tag={DS_T}]',
        f'execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["pat"], S.tag_p(key), DS_T)}}}',
        f'execute at @s facing entity {S.LOCK_M} feet run tp {DS_M} ~ ~ ~ ~ 0',
        sset('#t', nmax), sset('#t2', 0),
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["pat"], S.PROBE_T)}}}',
        f'execute at @s facing entity {S.LOCK_M} feet as {S.PROBE_M} run tp @s ~ ~ ~ ~ 0',
        f'execute as {S.PROBE_M} at @s run {fn(f"p/{key}/pstep")}',
        f'scoreboard players operation #{key}_n {OBJ} = #t2 {OBJ}',
        f'execute positioned as {S.PROBE_M} run function rlk:mboss/mv/glide {{t:{cut - go}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'data modify storage {DASH_STO} set value {{len:0,w:{int(round(w * 10))},tell:1,dmg:{api.DMG[h[4]]}}}',
        f'execute store result storage {DASH_STO}.len int 5 run scoreboard players get #{key}_n {OBJ}'])
    W.w(f'p/{key}/pstep', [
        f'# {key.upper()} probe step (@s = the probe, at / rotated as it): 0.5 b on while mv/ok passes, at most #t steps; once within',
        f'# 0.5 b of the locked spot the cap becomes {nb} more steps ({num(beyond)} b beyond it).',
        f'execute if score #t2 {OBJ} >= #t {OBJ} run return 0',
        f'execute if entity {S.LOCK_M[:-1]},distance=..0.5,tag=!rlk_hr_a9p] run {fn(f"p/{key}/past")}',
        'execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0',
        'tp @s ^ ^ ^0.5',
        f'scoreboard players add #t2 {OBJ} 1',
        f'execute at @s run {fn(f"p/{key}/pstep")}'])
    W.w(f'p/{key}/past', [f'# {key.upper()} probe at the locked spot (once): the cap = the steps so far + {nb}, at most {nmax}.',
                          f'scoreboard players operation #t {OBJ} = #t2 {OBJ}', f'scoreboard players add #t {OBJ} {nb}',
                          f'execute if score #t {OBJ} matches {nmax + 1}.. run {sset("#t", nmax)}',
                          f'tag {S.LOCK_M} add rlk_hr_a9p'])
    pb.at(go, fn(f'p/{key}/dash'))
    pb.motions.append((go, cut, 'dash'))
    ds = f'at {DS_M} rotated as {DS_M}'
    hl = S.hz_opts(h[5], grp=grp, noparry=1 if h[6] == 'N' else 0)
    hl += [f'execute {ds} positioned ~ {CY} ~ run function rlk:mboss/hz/line with storage {DASH_STO}', S.hz_tag(key)]
    pb.at(cut - 1, hl)
    pb.at(cut + 1, f'kill @e[type=minecraft:marker,tag={DS_T}]')
    return ds


def reach_clamp(key):
    """After the lock (@s = the body, facing the lock marker): a locked spot farther than the dash can carry her (DASH_LEN -
    DASH_BEYOND) is pulled in along her aim to that distance, so the cut never lands where she does not go."""
    r = num(api.DASH_LEN[key] - api.DASH_BEYOND[key], 2)
    return (f'execute at @s positioned ~ {CY} ~ unless entity {S.LOCK_M[:-1]},distance=..{r}] rotated as @s rotated ~ 0 '
            f'positioned ^ ^ ^{r} run tp {S.LOCK_M} ~ ~ ~')


def lock_dash(pb, key):
    """The lock step of a dash pattern: the marker at the player's spot, she faces it, the reach clamp."""
    return [lock_fn(pb, key), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0', reach_clamp(key)]


def streak(ds, h=0.8, c='magenta'):
    """The dash streak as long as the probed dash (kit qi_cut with storage core.dash: len in tenths)."""
    k = K.pw('qi_cut', DASH_STO)
    return placed([k] if k else [part(S.DUST[c], 2.0, 0.2, 0.2, 0, 30)], f'{ds} positioned ~ ~{num(h, 2)} ~')


# ================================================================================================= A9 황광 원참
def build_a9(W):
    key = 'a9'
    pb = PB(key, W)
    ring, flash, go, cut = (E(key, k) for k in ('ring', 'flash', 'go', 'cut'))
    end = api.PAT_END[key]
    lock = min(E(key, 'lock'), cut - S.LOCK)
    pb.at(0, FACE, api.play(key))
    pb.track(1, lock - 1, TRK['deg'])
    pb.at(ring, S.fx('qi_ring', [part(S.DUST['lilac'], 1.4, 0.05, 1.4, 0, 24)], pos=f'{S.AT_BODY} positioned ~ ~0.8 ~', r=35,
                     c=api.C_LILAC))
    pb.at(lock, lock_dash(pb, key))
    pb.at(flash, [x for x in (api.K.ovl('magenta', 0, 3, 6),) if x], S.snd('a9_flash'))
    # one strike group: the dash line from the start point along the dash + the disc at the locked spot (one landing);
    # the flashes of the group are the row 0's: yellow 8, purple 16 (exactly 12 t before the cut)
    g = pb.group(cut - 1)
    ds = dash_through(pb, key, go, cut)
    pb.at(go, *afterimage(int(api.DASH_LEN[key] * 10)))
    pb.note_hit(0, cut, tell_from=0, grp=g)
    pb.hit(1, tell_from=0, grp=g, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    pb.at(cut, streak(ds),
          S.fx('qi_ring', [part(S.DUST['magenta'], 1.6, 0.05, 1.6, 0, 24)], pos=f'at {S.LOCK_M} positioned ~ ~1.0 ~', r=40,
               c=api.C_MAGENTA), S.snd('a9_cut'))
    tail(pb, cut, end)
    return finish(pb, key)


# ================================================================================================= A10 황광 낙참
def build_a10(W):
    key = 'a10'
    pb = PB(key, W)
    spring, apex, lock, dive, hit = (E(key, k) for k in ('spring', 'apex', 'lock', 'dive', 'hit'))
    end = api.PAT_END[key]
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
    pb.at(spring, fn(f'p/{key}/spring'), S.snd('leap'))
    trail(pb, (spring, (spring + apex) // 2, apex))     # F1 (HR-28): both phases, along the rise
    pb.motions.append((spring, apex, 'rise'))
    pb.rng(apex + 1, lock - 1, fn(f'p/{key}/drift'))
    pb.motions.append((apex + 1, lock - 1, 'drift'))
    pb.track(apex + 1, lock - 1, 20)
    pb.at(lock, lock_fn(pb, key), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0')
    pb.at(dive, f'execute positioned as {S.LOCK_M} run function rlk:mboss/mv/glide {{t:{hit - dive}}}',
          S.fx('claw_streaks', [part(S.DUST['lilac'], 0.6, 2.0, 0.6, 0, 20)], pos=f'at {S.LOCK_M} positioned ~ {CY + 2} ~', r=15),
          S.snd('a10_dive'),
          S.fx('qi_line', [part(S.DUST['lilac'], 0.1, 0.6, 0.1, 0, 10)],
               pos=f'at @s positioned ~ ~0.8 ~ facing entity {S.LOCK_M} feet rotated ~-90 ~', len=int(api.LEAP_H[key] * 10 + 10)))
    trail(pb, (dive, dive + 1))
    pb.motions.append((dive, hit, 'dive'))
    # the yellow flash (in the air, on her chest: api.FLASH_AT) comes with the hit row
    pb.hit(0, tell_from=0, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    pb.at(hit, S.fx('burst_radial', [part(S.DUST['lilac'], 1.4, 0.2, 1.4, 0, 36), part('minecraft:end_rod', 0.2, 1.5, 0.2, 0.05, 10)],
                    pos=f'at {S.LOCK_M} positioned ~ {CY + 0.1} ~', r=35), S.snd('a10_impact', pos=f'at {S.LOCK_M}'))
    tail(pb, hit, end)
    ground(pb)
    return finish(pb, key)


# ================================================================================================= D4 원월 사연
def build_d4(W):
    """The ring round her, then a fan, a vertical line and a slash (video P-d; gaps 20 / 10 / 10)."""
    key = 'd4'
    pb = PB(key, W)
    hs = [E(key, f'h{i}') for i in (1, 2, 3, 4)]
    end = api.PAT_END[key]
    pb.at(0, FACE, api.play(key),
          at_anchor('chest', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    prev = 0
    for i, t in enumerate(hs):
        track_to(pb, prev, t)
        if i:
            step_in(pb, prev, t)
        else:
            pb.advance(1, t - S.LOCK, TRK['step'], TRK['min'])
        pb.hit(i, tell_from=0 if i == 0 else prev)
        r = api.HITS[key][i][3][0]
        if i == 0:        # the ring at chest height
            pb.at(t, S.fx('qi_ring', [part(S.DUST['lilac'], 1.5, 0.05, 1.5, 0, 26), part('minecraft:sweep_attack', 1.0, 0.05, 1.0, 0, 3)],
                          pos=f'{S.AT_BODY} positioned ~ ~1.1 ~', r=30, c=api.C_LILAC), S.snd('g_ring'))
        elif i == 1:      # the narrow fan
            pb.at(t, S.fx('qi_fan', [part(S.DUST['lilac'], 0.3, 0.8, 0.3, 0, 14)], pos=f'{S.AT_BODY} positioned ^ ^1.1 ^1.2',
                          h=16, c=api.C_LILAC), S.snd('a3_h2'))
        elif i == 2:      # the vertical line
            pb.at(t, S.fx('qi_vert', [part(S.DUST['lilac'], 0.2, 1.0, 0.2, 0, 20)], pos=f'{S.AT_BODY} positioned ^ ^0.15 ^2.0',
                          h=27, yaw=0, c=api.C_LILAC), S.snd('a3_h4'))
        else:             # the closing slash
            pb.at(t, S.fx_arc(r, api.C_LILAC, roll=-30), S.snd('a3_h5'))
        prev = t
    pb.pp_window(prev)
    tail(pb, prev, end)
    return finish(pb, key)


# ================================================================================================= TRI 돌진 삼월참
def build_tri(W):
    """A lunge along the locked aim (<= 6 b, the line hazard along it), then three wide crescents (video P-i)."""
    key = 'tri'
    pb = PB(key, W)
    lock0, go, h0 = E(key, 'lock0'), E(key, 'go'), E(key, 'h0')
    hs = [E(key, f'h{i}') for i in (1, 2, 3)]
    end = api.PAT_END[key]
    reach, glide_v, glide_t = api.TRI_GLIDE
    dmax = api.DASH_LEN[key]
    pb.at(0, FACE, api.play(key),
          at_anchor('blade_mid', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    # beyond 6 b she glides in 0.3 b / t during 0-12 (toward the player until the aim locks at 7, then along the locked aim)
    pb.track(1, lock0 - 1, TRK['deg'])
    pb.advance(1, go - 1, glide_v, reach)
    W.w(f'p/{key}/lunge', [
        f'# TRI lunge (@s = the body, tick {go}): along the locked aim to 1.5 b before the player, at most {num(dmax)} b (probe, mv/ok),',
        f'# in {h0 - go} t.',
        'function rlk:mboss/mv/dist',
        f'scoreboard players operation #t {OBJ} = #mbDist mb',
        f'scoreboard players remove #t {OBJ} 15',
        f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches ..-1 run {sset("#t", 0)}',
        f'execute if score #t {OBJ} matches {int(dmax * 2) + 1}.. run {sset("#t", int(dmax * 2))}',
        f'execute at @s rotated as @s rotated ~ 0 run {fn("core/dash/probe")}',
        f'execute positioned as {S.PROBE_M} run function rlk:mboss/mv/glide {{t:{h0 - go}}}',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]'])
    # the line along the lunge: made at `go` from her spot before the move (tell 2), the cue at h0 - 7 = the lock
    pb.hit(0, tell_from=0, made=go)
    pb.at(go, fn(f'p/{key}/lunge'), S.snd('lunge'), S.fx('afterimage', pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=int(dmax * 10)))
    pb.motions.append((go, h0, 'lunge'))
    pb.at(h0, S.fx('qi_line', [part(S.DUST['lilac'], 0.2, 0.2, 1.5, 0, 16)], pos=f'{S.AT_BODY} positioned ^ ^0.95 ^-5 rotated ~-90 0',
                   len=60), S.snd('a2_hit'))
    prev = h0
    for i, t in enumerate(hs):
        track_to(pb, prev, t)
        step_in(pb, prev, t)
        pb.hit(i + 1, tell_from=prev)
        r = api.HITS[key][i + 1][3][0]
        pb.at(t, S.fx_arc(r, api.C_LILAC, roll=(30, -30, 30)[i]), S.snd(('a3_h1', 'a3_h3', 'a3_h5')[i]))
        prev = t
    pb.pp_window(prev)
    tail(pb, prev, end)
    return finish(pb, key)


# ================================================================================================= RINGS 회전 월륜
def build_rings(W):
    """Four ring cuts round her (P2: five), 10 t apart; she steps toward the player before each. At a full gauge the AI
    forces it and ULT follows (#ultq: it then ends api.ULT_AFTER t after its last ring and the core starts ult)."""
    key = 'rings'
    pb = PB(key, W)
    P1c = f'if score #ph {OBJ} matches {api.PH["p1"]}'
    P2c = f'if score #ph {OBJ} matches {api.PH["p2"]}'
    ULT, NOULT = f'if score #ultq {OBJ} matches 1', f'unless score #ultq {OBJ} matches 1'
    pb.at(0, FACE, api.play(key),
          at_anchor('blade_mid', S.fx_lines('glint', [part(S.DUST['lilac'], 0.1, 0.1, 0.1, 0, 6)], c=api.C_LILAC)))
    ring_fx = lambda: (S.fx('qi_ring', [part(S.DUST['lilac'], 1.3, 0.05, 1.3, 0, 24), part('minecraft:sweep_attack', 0.9, 0.05, 0.9, 0, 3)],  # noqa: E731
                            pos=f'{S.AT_BODY} positioned ~ ~1.1 ~', r=26, c=api.C_LILAC) + S.snd('g_ring'))
    ts = [E(key, f'r{i}') for i in (1, 2, 3, 4, 5)]
    prev = 0
    for i, t in enumerate(ts):
        cond = P2c if i == 4 else None
        ln = f'function rlk:mboss/mv/turn {{max:{TRK["deg"]}}}'
        st = (f'execute at @s unless entity {S.PLAYER[:-1]},distance=..{num(TRK["min"], 2)}] run function rlk:mboss/mv/step '
              f'{{d:{num(TRK["step"], 3)}}}')
        for a in range(prev + 1, t - S.LOCK + 1):
            pb.at(a, S.gate(cond, ln) if cond else ln, S.gate(cond, st) if cond else st)
        pb.motions.append((prev + 1, t - S.LOCK, 'step'))
        if i < 3:
            pb.hit(i, tell_from=0 if i == 0 else prev)
            pb.at(t, ring_fx())
        elif i == 3:
            pb.hit(3, tell_from=prev)          # P1: the last ring (T2, kb 3)
            pb.hit(4, tell_from=prev)          # P2: a chain ring
            pb.at(t, ring_fx())
        else:
            pb.hit(5, tell_from=prev)          # P2 only: the last ring
            pb.at(t, [S.gate(P2c, x) for x in ring_fx()])
        prev = t
    e1, e2 = api.RINGS_END[1], api.RINGS_END[2]
    u1, u2 = ts[3] + api.ULT_AFTER, ts[4] + api.ULT_AFTER
    # the ends: P1 r4 + 10 (or + ULT_AFTER when ult follows), P2 r5 + 10 (or + ULT_AFTER)
    pb.pp_window(ts[3], cond=P1c)
    pb.pp_window(ts[4], cond=P2c)
    for fp, last, cnd, e, u in ((1, ts[3], P1c, e1, u1), (2, ts[4], P2c, e2, u2)):
        turn = f'function rlk:mboss/mv/turn {{max:{TRK["deg"]}}}'
        pb.rng(last + 1, e - 1, S.gate(cnd, turn))
        tm = last + api.TAIL_MOVE
        pb.at(tm, S.gate(f'{cnd} {NOULT}', fn('ai/tail')))
        pb.rng(tm + 1, e - 1, S.gate(f'{cnd} {NOULT}', fn('ai/tail_step')))
        pb.motions.append((tm + 1, e - 1, f'tail move (P{fp})'))
        pb.at(u, S.gate(f'{cnd} {ULT}', sset('#done', 1)))
        if fp == 1:
            pb.at(e, S.gate(cnd, sset('#done', 1)))
    TAILS[key] = ts[3] + api.TAIL_MOVE
    pb.end(e2)
    return finish(pb, key)


# ================================================================================================= ULT 공간 참 (U)
def build_ult(W):
    """The space-cut ultimate (video U): yellow 0, purple 12, the first cut 24 (white, the web), purple 34, the second cut
    46 (white, the burst): two whole-arena hits, both unparriable (a perfect dodge avoids each); the gauge is spent at the
    second cut. Only after RINGS at a full gauge. She is hittable throughout."""
    key = 'ult'
    pb = PB(key, W)
    cut1, web, cut2 = E(key, 'cut1'), E(key, 'web'), E(key, 'cut2')
    end = api.PAT_END[key]
    full = f'{S.AT_BODY} positioned ~ {CY} ~'
    pb.at(0, sset('#ultq', 0), api.play(key))
    pb.track(1, cut1 - S.LOCK, TRK['deg'])
    pb.hit(0, tell_from=0, pos=full)
    pb.at(cut1, [x for x in (K.ovl('white', 0, 2, 2),) if x], S.snd('ult_cut1'))
    pb.at(web, S.fx('ult_web', [part(S.DUST['white'], 6.0, 1.5, 6.0, 0, 80), part(S.DUST['lilac'], 6.0, 1.5, 6.0, 0, 60)],
                    pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', t=cut2 - web + 2),
          [x for x in (K.ovl('web', 2, cut2 - web - 4, 2),) if x])
    pb.hit(1, tell_from=0, pos=full)
    pb.at(cut2, sset(api.GAUGE_FP, 0), [x for x in (K.ovl('white', 0, 3, 6),) if x],
          S.fx('ult_burst', [part(S.DUST['white'], 8.0, 1.5, 8.0, 0.2, 100)], pos=f'{S.AT_BODY} positioned ~ ~1.2 ~'),
          S.fx('burst_radial', [part(S.DUST['lilac'], 2.5, 0.2, 2.5, 0, 50)], pos=f'{S.AT_BODY} positioned ~ ~0.1 ~', r=60),
          S.snd('ult_cut2'))
    # the second cut strikes after this module tick: its own landed hit must not charge the spent gauge
    pb.at(cut2 + 1, sset(api.GAUGE_FP, 0))
    tail(pb, cut2, end)
    return finish(pb, key)


# ================================================================================================= HCUT 황광 섬월
def build_hcut(W):
    """The far yellow dash-cut (video P-h): yellow 2, a sparkle on her 8-16, the lock 19, the dash through the lock 24-26
    (<= 16 b), the dash line + a flat disc at the lock (one group)."""
    key = 'hcut'
    pb = PB(key, W)
    sparkle, lock, go, cut = (E(key, k) for k in ('sparkle', 'lock', 'go', 'cut'))
    end = api.PAT_END[key]
    assert lock == cut - S.LOCK
    pb.at(0, FACE, api.play(key))
    pb.track(1, lock - 1, TRK['deg'])
    for t in range(sparkle, sparkle + 9, 4):
        pb.at(t, at_anchor('blade_tip', S.fx_lines('glint', [part(S.DUST['white'], 0.08, 0.08, 0.08, 0, 6)], c=api.C_WHITE)))
    pb.at(lock, lock_dash(pb, key))
    g = pb.group(cut - 1)
    ds = dash_through(pb, key, go, cut)
    pb.at(go, S.snd('g_dash'), S.fx('afterimage', pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=int(api.DASH_LEN[key] * 10)))
    pb.note_hit(0, cut, tell_from=0, grp=g)
    pb.hit(1, tell_from=0, grp=g, pos=f'at {S.LOCK_M} rotated as @s positioned ~ {CY} ~')
    pb.at(cut, streak(ds, 0.7),
          S.fx('qi_ring', [part(S.DUST['magenta'], 1.8, 0.05, 1.8, 0, 28)], pos=f'at {S.LOCK_M} positioned ~ ~0.7 ~', r=45,
               c=api.C_MAGENTA), S.snd('a9_cut'))
    tail(pb, cut, end)
    return finish(pb, key)


# ================================================================================================= BLUE 청광 돌파
def build_blue(W):
    """The blue lunge (video P-blue): a yellow ring that turns into a blue sphere round her (flash_blue, 4-19), the lock 15,
    the lunge through the lock 20-22 (<= 9 b): the dash line."""
    key = 'blue'
    pb = PB(key, W)
    lock, go, hit = (E(key, k) for k in ('lock', 'go', 'hit'))
    end = api.PAT_END[key]
    assert lock == hit - S.LOCK
    pb.at(0, FACE, api.play(key))
    pb.track(1, lock - 1, TRK['deg'])
    pb.at(lock, lock_dash(pb, key))
    ds = dash_through(pb, key, go, hit, grp=False)
    pb.at(go, S.snd('lunge'), S.fx('afterimage', pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=int(api.DASH_LEN[key] * 10)))
    pb.note_hit(0, hit, tell_from=0)
    pb.at(hit, streak(ds, 0.9, 'lilac'), S.snd('a2_hit'))
    tail(pb, hit, end)
    return finish(pb, key)


# ================================================================================================= KCUT 황광 난참
def build_kcut(W):
    """The big yellow dash-through (video P-k): a low crouch, the big yellow flash 3, a pink sparkle 9, the lilac body glow
    12-19, the lock 15, the dash through the lock 20-22 (<= 10 b): the dash line + three lines crossing the lock (one hit)."""
    key = 'kcut'
    pb = PB(key, W)
    sparkle, glow, lock, go, cut = (E(key, k) for k in ('sparkle', 'glow', 'lock', 'go', 'cut'))
    end = api.PAT_END[key]
    assert lock == cut - S.LOCK
    pb.flash_args['yellow'] = {'t': 110}           # the big yellow: the kit reads t >= 100 as the Ø 2.0 b tell for t - 100 t (HI)
    pb.at(0, FACE, api.play(key))
    pb.track(1, lock - 1, TRK['deg'])
    pb.at(sparkle, at_anchor('blade_tip', S.fx_lines('glint', [part(S.DUST['white'], 0.08, 0.08, 0.08, 0, 6)], c=api.C_WHITE)))
    pb.at(glow, look('blade', 'lilac'))
    pb.at(go, look('blade', 'off'))
    pb.cancel_lines.append(f'execute as {S.BODY} run {look("blade", "off")}')
    pb.at(lock, lock_dash(pb, key))
    g = pb.group(cut - 1)
    ds = dash_through(pb, key, go, cut)
    pb.at(go, S.snd('kcut_go'), S.fx('afterimage', pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=int(api.DASH_LEN[key] * 10)))
    pb.note_hit(0, cut, tell_from=0, grp=g)
    ln = api.HITS[key][1][3][0]
    for i, yaw in enumerate(api.KCUT_YAW):
        at = f'at {S.LOCK_M} rotated as {DS_M} rotated ~{yaw} 0 positioned ^ ^ ^-{num(ln / 2)} positioned ~ {CY} ~'
        pb.hit(i + 1, tell_from=0, grp=g, pos=at)
        pb.at(cut, S.fx('qi_line', [part(S.DUST['magenta'], 0.2, 0.2, 2.5, 0, 20)],
                        pos=f'at {S.LOCK_M} rotated as {DS_M} rotated ~{yaw - 90} 0 positioned ^{num(ln / 2)} ^0.9 ^', len=int(ln * 10)))
    pb.at(cut, streak(ds), S.snd('a9_cut'))
    tail(pb, cut, end)
    return finish(pb, key)


BUILD = {'a1': build_a1, 'a2': build_a2, 'a3': build_a3, 'a3s': build_a3s, 'a4': build_a4, 'a6': build_a6, 'a9': build_a9,
         'a10': build_a10, 'd4': build_d4, 'tri': build_tri, 'rings': build_rings, 'ult': build_ult, 'hcut': build_hcut,
         'blue': build_blue, 'kcut': build_kcut}
NOTES = {'a1': 'counter (beside / behind): the flat crescent', 'a2': 'counter (in front): the hook slash',
         'a3': 'five crescents, tracking', 'a3s': 'the same opening, two crescents',
         'a4': 'moon-leap dive + the aerial ring (A5)', 'a6': 'back-blink + line 12 (trigger only)',
         'a9': 'yellow + purple, magenta flash, iai dash + disc', 'a10': 'yellow in the air, the plunge',
         'd4': 'ring, fan, vertical, slash', 'tri': 'the lunge line + three wide crescents',
         'rings': 'four ring cuts (P2 five); at a full gauge ult follows', 'ult': 'the space cut: two whole-arena hits',
         'hcut': 'yellow, the far dash + the flat disc', 'blue': 'the blue sphere, the lunge line',
         'kcut': 'the big yellow, the dash-through + three crossing lines'}


def _mk(key):
    def build(W):
        BUILD[key](W)
    return build


PATTERNS = [api.Pattern(k, S.TID[k], ('a3',) if k == 'a3s' else (k,), _mk(k), notes=NOTES[k]) for k in api.P1]
assert [p.key for p in PATTERNS] == list(api.P1)
