"""Phase-3 patterns (AP-P3; plan 8.3, 7.3, 7.4, 7.10, 7.11 + the 10-20 telegraph rule of plan 14; ap_contract 0.8,
0.13, 1.3; ap_fx_api 0.11): Q1 이동 돌진 (31), Q3 증폭의 풀 (33), Q4 생명의 꼬리 (34), Q5 생명의 나선 (35) and the chain Q3s
수면 포격 (36). Writes AP:p/{mstrike,shells,tail3,spiral,surface}/** only (api.OWN['p3']).

Telegraph rule (user 10-20, plan 14 table): a ground decal only for the *keep* rows: Q1's burst (the leaf-pad trail +
the rosette ring r 4.2), Q3 shell 1 (the pale target ring following the player's feet 6 t late, then the target disc at
the lock), Q3s (the leaf ring r 3.6 at the surfacing point and the target disc r 3.0 under the player). Every other hazard
is quiet (#hzQuiet 1, Gen.hz_opts) and read from the motion, the sound and the props in the air, >= 10 t from the first
readable cue, with its impact visual on the hit tick: Q1's slam + tail whip (hoop + roll), Q3 shells 2 / 3 (the shells
hover over their points from the locks), Q4's swings (crouch / cock / tail-tip flash, the S-coil + lunge), Q5's landings
(the orbs flare at each lock and fly visibly) and its leaf blades (the blades stand at the lane ends from the lock).
No-tips rule (user 10-21): no line here tells the player what to do (the HUD shows only the core's pattern name).

Clocks: #apPT = the pattern clock (the core plays the first clip at 0). Q1 / Q3 / Q5 / Q3s start UPRIGHT; when the boss is
crouched at the start (a test cut) stand_p3 runs first and the pattern's own clock #apq<id>T = #apPT - #apq<id>O (the
clip tick) starts 14 t later. Q4: #apq34T = the tail_p3 tick (the crouch opener 8 t, + the walk 30 t when the player is
farther than 8 b). Every tick below is a played clip tick read from the rig manifest (api.ev).

Yaw: move_strike_p3 and tail_p3 carry yaw schedules (the core's yaw driver holds Rotation = yaw0 + schedule). Q1 turns the
hidden body toward the player before it surfaces and re-bases the driver (Gen.yaw_rebase(), requests/ap-p3.md RP3-1,
AP-I2).

AP-I2 also applied: RP3-6 / RI1-1 (the keep decals of Q1, Q3 shell 1 and Q3s are the outline-only tele/disc_o, their
resume redraws too) and RP1-3 for Q4 (api.wedges(..., swept=True): tail_p3's root moves too, the bare wedges missed
slivers of the swept lane).
"""
import math

from .api import Pattern, Gen, TL, PLAYER, BODY, K, L
from . import api as A

NS = A.NS
CY = A.CY
W3 = lambda n, m, f: dict(near=n, mid=m, far=f)    # noqa: E731
ev = A.ev
num = L.num
STAND = A.clip_len('stand_p3')                     # 14: the stand-first prelude
KB4 = A.KB['heavy']
KB2 = A.KB['light']


def tagl(pid, *more):
    tg = ['rlk_room', 'rlk_mb_aux', 'rlk_mb_ap_pat', f'rlk_mb_ap_p{pid}'] + list(more)
    return '[' + ','.join(f'"{t}"' for t in tg) + ']'


def marker(pid, *more):
    """Summon a pattern marker here (the caller positions it on the floor)."""
    return f'summon minecraft:marker ~ ~ ~ {{Tags:{tagl(pid, *more)}}}'


def display(pid, *more, td=2):
    """Summon a pattern item_display here (a kit prop / look dresses it next)."""
    return (f'summon minecraft:item_display ~ ~ ~ {{Tags:{tagl(pid, *more)},teleport_duration:{td},'
            'item:{id:"minecraft:paper",count:1}}')


def m1(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


def mall(tag):
    return f'@e[type=minecraft:marker,tag={tag}]'


def dsel(tag, extra=''):
    return f'@e[type=minecraft:item_display,tag={tag}{extra}]'


def near(sel, d):
    """sel (a limit=1 selector) within d b of the execution position."""
    return sel.replace('limit=1', f'distance=..{num(d)},limit=1')


def hz(shape_line, tag=None, **opts):
    """One quiet Dendro hazard (Gen.hz_opts defaults) + its tag."""
    out = Gen.hz_opts(**opts) + [shape_line]
    if tag:
        out.append(Gen.tag_last_hz(tag))
    return out


def tl_head(p, note):
    return [f'# {p.label} ({p.key}, id {p.id}; plan 8.3). {note}']


def prelude(g, p, clip):
    """Stand first when crouched (the rig's stance apRigStance 0: #apq<id>O 14), else 0; the pattern clock
    #apq<id>T = #apPT - O. Returns (start lines,
    the clock-update lines for the tick, the clip-at-0 line)."""
    o, c = f'#apq{p.id}O', f'#apq{p.id}T'
    start = [f'scoreboard players set {o} mb 0',
             f'execute if score @s apRigStance matches 0 run scoreboard players set {o} mb {STAND}',
             f'execute if score {o} mb matches {STAND} run {Gen.play("stand_p3")}',
             f'execute if score {o} mb matches {STAND} run scoreboard players add #apPLen mb {STAND}',
             f'scoreboard players operation {c} mb = #apPT mb', f'scoreboard players operation {c} mb -= {o} mb']
    clock = [f'scoreboard players operation {c} mb = #apPT mb', f'scoreboard players operation {c} mb -= {o} mb']
    at0 = f'execute if score {o} mb matches {STAND} run {Gen.play(clip)}'
    return start, clock, at0


def redraw_fn(g, key, store, r, mtag, sub='redraw', pid=0):
    """A resume hook helper: the outline-only kit disc (tele/disc_o, AP-I2 RP3-6) of a pending keep hazard again with its
    remaining tell (the core's pause hook cleared every kit telegraph). As the hazard marker (tag mtag), at it."""
    g.pw(key, sub, [f'# @s = a pending keep hazard ({mtag}): its decal again (r {r}) with the ticks left to its strike.',
                    f'scoreboard players operation #apq{pid}X mb = @s mbHzW', f'scoreboard players operation #apq{pid}X mb -= @s mbHzT',
                    f'execute if score #apq{pid}X mb matches ..0 run return 0',
                    f'data modify storage rlk:mboss ap.{store} set value {{r:{int(round(r * 10))},el:7,nd:0,hold:3,tell:1}}',
                    f'execute store result storage rlk:mboss ap.{store}.tell int 1 run scoreboard players get #apq{pid}X mb',
                    f'function {K.FN}tele/disc_o with storage rlk:mboss ap.{store}'])


def mdist_lines(sel, out, pre):
    """<out> mb = the horizontal distance @s -> sel in tenths (integer Newton square root, as mboss/mv/dist); scratch
    <pre>Dx / Dz / N / X (a function of its own: it returns early when the two points coincide)."""
    lines = [f'execute store result score {pre}Dx mb run data get entity {sel} Pos[0] 10',
             f'execute store result score {pre}X mb run data get entity @s Pos[0] 10',
             f'scoreboard players operation {pre}Dx mb -= {pre}X mb',
             f'execute store result score {pre}Dz mb run data get entity {sel} Pos[2] 10',
             f'execute store result score {pre}X mb run data get entity @s Pos[2] 10',
             f'scoreboard players operation {pre}Dz mb -= {pre}X mb',
             f'scoreboard players operation {pre}N mb = {pre}Dx mb', f'scoreboard players operation {pre}N mb *= {pre}Dx mb',
             f'scoreboard players operation {pre}X mb = {pre}Dz mb', f'scoreboard players operation {pre}X mb *= {pre}Dz mb',
             f'scoreboard players operation {pre}N mb += {pre}X mb',
             f'scoreboard players set {out} mb 0', f'execute if score {pre}N mb matches ..0 run return 0',
             f'scoreboard players set {out} mb 300']
    for _ in range(7):
        lines += [f'scoreboard players operation {pre}X mb = {pre}N mb', f'scoreboard players operation {pre}X mb /= {out} mb',
                  f'scoreboard players operation {out} mb += {pre}X mb', f'scoreboard players operation {out} mb /= #c2 mb',
                  f'execute if score {out} mb matches ..0 run scoreboard players set {out} mb 1']
    return lines


# ======================================================================================================== Q1 이동 돌진
MS = 'move_strike_p3'
Q1 = dict(mound=ev(MS, 'mound'), hide=ev(MS, 'hide'), lock=ev(MS, 'lock'), show=ev(MS, 'show'), burst=ev(MS, 'burst'),
          roll=ev(MS, 'roll'), slam=ev(MS, 'slam'), tail=ev(MS, 'tail'), sweep=ev(MS, 'sweep'), rise=ev(MS, 'rise'),
          end=A.clip_len(MS), place=38, slam_made=46, sweep_made=48, glide=0.8, roll_len=4.0, lead=10,
          burst_r=4.2, slam_r=4.2, sweep_r=12.0, sweep_y1=0.7, release=72)
Q1['burst_tell'] = Q1['burst'] - Q1['lock']                  # 12 (keep: the rosette ring from the lock)
Q1['slam_tell'] = Q1['slam'] - Q1['slam_made']               # 15
Q1['sweep_tell'] = Q1['sweep'] - Q1['sweep_made']            # 21
BURST_F = A.anchor(MS, 'burst', 'impact')[2]                 # 2.59 b ahead of the anchor at the burst
SLAM_F = A.anchor(MS, 'slam', 'impact')[2]                   # -1.16: the belly flop lands behind the anchor
assert (Q1['lock'], Q1['burst'], Q1['slam'], Q1['sweep'], Q1['end']) == (32, 44, 61, 69, 92), Q1
assert (Q1['burst_tell'], Q1['slam_tell'], Q1['sweep_tell']) == (12, 15, 21)
assert A.hidden_spans(MS) == [(16, 41)] and Q1['place'] <= Q1['show'] - 4
# where the ring of the tail opens under the water at t62-64 (rig API 7c: the belly-flop splash must cover it): a second
# splash on the tail side, local (s, f) from the manifest's tail tip at t63 / t64
_tt = [A.track(MS, 'tail_tip')[t] for t in (63, 64)]
TAIL_SPLASH = (round(sum(p[0] for p in _tt) / 2, 2), round(sum(p[2] for p in _tt) / 2, 2))


def emit_mstrike(g, p):
    key, pid = p.key, p.id
    T_ = f'rlk_mb_ap_p{pid}'
    LK, EK, SK = f'{T_}l', f'{T_}e', f'{T_}s'           # the burst point L, the roll end E, the slam point S
    HK = f'{T_}k'                                        # the burst hazard (keep: redrawn after a pause)
    start, clock, at0 = prelude(g, p, MS)
    tl = TL(g, key, clock=f'#apq{pid}T')
    tl.at(0, at0)
    tl.at(Q1['mound'], f'execute at @s positioned ~ {CY} ~ run {K.fx("leaf_mound")}', f'execute at @s run {K.snd("q1_sink")}')
    # underground: the leaf-pad trail glides toward the player (<= 0.8 b/t), then to the lock (the readable tell)
    for t in range(Q1['hide'], Q1['lock']):
        tl.at(t, f'execute at @s unless entity {near(PLAYER, 3.0)} run {Gen.move_to(PLAYER, Q1["glide"])}')
    for t in range(Q1['lock'] + 1, Q1['place']):
        tl.at(t, f'execute at @s unless entity {near(m1(LK), 1.0)} run {Gen.move_to(m1(LK), Q1["glide"])}')
    for t in range(Q1['hide'], Q1['place'] + 1, 4):
        tgt = PLAYER if t <= Q1['lock'] else m1(LK)
        tl.at(t, f'execute at @s positioned ~ {CY} ~ facing entity {tgt} feet rotated ~ 0 run {K.fx("leaf_pad")}',
              f'execute at @s run {K.snd("q1_trail")}')
    tl.at(Q1['lock'], g.fn(f'p/{key}/lock'))
    tl.at(Q1['place'], g.fn(f'p/{key}/place'))
    tl.at(Q1['burst'], f'execute at {m1(LK)} run {g.fn(f"p/{key}/burst_fx")}', f'execute at @s run {K.fx("hoop_trail")}')
    tl.at(Q1['slam_made'], f'execute at {m1(SK)} run {g.fn(f"p/{key}/slam_hz")}')
    tl.at(Q1['sweep_made'], f'execute at {m1(EK)} run {g.fn(f"p/{key}/sweep_hz")}')
    step = (Q1['roll_len']) / (Q1['slam'] - Q1['roll'])
    for t in range(Q1['roll'], Q1['slam']):
        tl.at(t, f'execute at @s unless entity {near(m1(EK), step + 0.05)} facing entity {m1(EK)} feet rotated ~ 0 '
                 f'positioned ^ ^ ^{num(step, 3)} run tp @s ~ {CY} ~')
    tl.at(Q1['slam'], f'execute at {m1(EK)} run tp @s ~ {CY} ~',
          f'execute at {m1(SK)} run {K.fx("belly_splash")}', f'execute at {m1(SK)} run {K.snd("q1_slam")}')
    tl.at(Q1['slam'] + 1, f'execute at @s rotated as @s positioned {A.loc(TAIL_SPLASH[0], TAIL_SPLASH[1])} positioned ~ {CY} ~ '
                          f'run {K.fx("belly_splash")}')
    tl.at(Q1['sweep'], f'execute at @s positioned ~ {CY} ~ run {K.fx("sweep_ring", r=Q1["sweep_r"])}',
          f'execute at @s run {K.snd("q1_slam")}')
    tl.at(Q1['rise'], f'execute at @s run {K.fx("light_sprouts")}', f'execute at @s run {K.snd("q1_rise")}')
    tl.at(Q1['release'], Gen.release())
    g.pw(key, 'lock', [
        f'# @s = body (t{Q1["lock"]}, hidden): the burst point L = the predictive lock (lead {Q1["lead"]}) clamped to r 16;',
        f'# the burst hazard r {Q1["burst_r"]} (tell {Q1["burst_tell"]}, {A.DMG["q1_burst"]} %) with its keep decal (the rosette ring,',
        '# plan 14: the leaf ring the footage shows 12 t before the burst) and the airborne rosette.',
        *Gen.lockv(Q1['lead']), f'execute as {A.LOCK} run {Gen.clamp("burst3")}', *Gen.keep(LK),
        f'execute at {m1(LK)} run {g.fn(f"p/{key}/burst_hz")}'])
    g.pw(key, 'burst_hz', ['# At L: the burst (quiet hazard + the kit decal of the keep row) and the rosette.',
                           *hz(L.hz_disc(Q1['burst_r'], Q1['burst_tell'], A.DMG['q1_burst']), tag=HK),
                           *Gen.decal('keep', K.tele_disc(Q1['burst_r'], Q1['burst_tell'], fill=0)),
                           K.fx('rosette'), K.snd('q1_rosette')])
    roll_in = Q1['roll_len'] - BURST_F
    g.pw(key, 'place', [
        f'# @s = body (t{Q1["place"]}, still hidden, 4 t before it shows): the facing f = from L toward the player (along the',
        f'# hidden path when the player stands on L); the anchor goes to L - {BURST_F} f (the clip\'s burst point lands on L),',
        f'# the roll end E = L + {num(roll_in, 3)} f (clamped to r 16), the slam point S = E {SLAM_F} f.',
        f'execute as {m1(LK)} at @s facing entity {BODY} feet run tp @s ~ ~ ~ ~180 0',
        f'execute as {m1(LK)} at @s unless entity {near(PLAYER, 1.0)} facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0',
        f'kill {mall(EK)}', f'kill {mall(SK)}',
        f'execute at {m1(LK)} positioned ^ ^ ^{num(roll_in, 3)} run {marker(pid, EK)}',
        f'execute as {m1(EK)} at @s rotated as {m1(LK)} run tp @s ~ ~ ~ ~ 0',
        f'execute as {m1(EK)} run {Gen.clamp("glide")}',
        f'execute at {m1(EK)} rotated as {m1(LK)} positioned ^ ^ ^{num(SLAM_F, 3)} run {marker(pid, SK)}',
        f'execute at {m1(LK)} positioned ^ ^ ^{num(-BURST_F, 3)} run tp @s ~ {CY} ~ ~ 0',
        '# the yaw driver holds the new facing (RP3-1, AP-I2; the schedule is 0 until t66)',
        Gen.yaw_rebase()])
    g.pw(key, 'burst_fx', ['# At L (t44): the surfacing flash, the water splash, the burst sounds (the impact visual).',
                           K.fx('surface_burst'), K.fx('water_splash'), K.snd('q1_burst')])
    g.pw(key, 'slam_hz', [
        f'# At S (t{Q1["slam_made"]}): the belly-flop slam r {Q1["slam_r"]} (tell {Q1["slam_tell"]}, hit t{Q1["slam"]}), quiet (none row: the',
        '# hoop 44-49 and the roll 49-61 are the tell); a new volley group shared with the tail whip.',
        Gen.GRP_NEW, f'scoreboard players operation #apq{pid}G mb = #mbGrp mb',
        *hz(L.hz_disc(Q1['slam_r'], Q1['slam_tell'], A.DMG['q1_slam']), tag=f'{T_}h', grp=True)])
    g.pw(key, 'sweep_hz', [
        f'# At E (t{Q1["sweep_made"]}): the 360-degree tail whip r {Q1["sweep_r"]} low (#hzY1 {Q1["sweep_y1"]}: a jump clears it), tell',
        f'# {Q1["sweep_tell"]} (hit t{Q1["sweep"]}), quiet; the slam\'s volley group (one hit at most).',
        *Gen.hz_opts(y1=Q1['sweep_y1']), f'scoreboard players operation #hzGrp mb = #apq{pid}G mb',
        L.hz_disc(Q1['sweep_r'], Q1['sweep_tell'], A.DMG['q1_slam']), Gen.tag_last_hz(f'{T_}h')])
    tl.write(tl_head(p, f'move_strike_p3: sink 8, hidden 16-41, lock {Q1["lock"]}, burst {Q1["burst"]}, slam {Q1["slam"]}, '
                        f'sweep {Q1["sweep"]}, end {Q1["end"]}.') + start + [f'kill @e[tag={T_}]', f'scoreboard players set #apq{pid}G mb 0'],
             tl_head(p, 'tick (#apq31T = the clip tick).') + clock,
             t0=-1000, extra_tick=[f'execute if score #apq{pid}T mb matches {Q1["end"]}.. run return run {g.fn(f"p/{key}/done")}'])
    g.pw(key, 'done', ['# The clip is over: its own entities go (p/finish keeps only the core\'s), then p/end.', f'kill @e[tag={T_}]',
                       Gen.end()])
    g.pw(key, 'cancel', ['# Cut (any executor): its markers go; its hazards are the framework\'s (lib_clear).', f'kill @e[tag={T_}]'])
    g.pw(key, 'resume', ['# Resume (the pause cleared the kit telegraphs): the pending burst ring again with the ticks left.',
                         f'execute as @e[type=minecraft:marker,tag={HK}] at @s run {g.fn(f"p/{key}/redraw")}'])
    redraw_fn(g, key, f'p{pid}d', Q1['burst_r'], HK, pid=pid)


# ======================================================================================================== Q3 증폭의 풀
SH = 'shells'
Q3 = dict(ring=ev(SH, 'ring'), lit=ev(SH, 'lit'), lock1=ev(SH, 'lock1'), launch=ev(SH, 'launch'), hit1=ev(SH, 'hit1'),
          cool=ev(SH, 'cool'), lock2=ev(SH, 'lock2'), lock3=ev(SH, 'lock3'), hit2=ev(SH, 'hit2'), hit3=ev(SH, 'hit3'),
          end=A.clip_len(SH), lag=6, every=2, r1=3.6, r23=3.0, lead2=8, hover=10.0, streak=6, release=97)
Q3['tell1'] = Q3['hit1'] - Q3['lock1']                      # 12
Q3['tell2'] = Q3['hit2'] - Q3['lock2']                      # 14
Q3['tell3'] = Q3['hit3'] - Q3['lock3']                      # 14
assert (Q3['lock1'], Q3['hit1'], Q3['lock2'], Q3['lock3'], Q3['hit2'], Q3['hit3'], Q3['end']) == (33, 45, 79, 82, 93, 96, 113), Q3
assert (Q3['tell1'], Q3['tell2'], Q3['tell3']) == (12, 14, 14)
BALL = A.anchor(SH, 'launch', 'ball')                        # the light ball over the crown (x left, y up, z forward)


def emit_shells(g, p):
    key, pid = p.key, p.id
    T_ = f'rlk_mb_ap_p{pid}'
    HIST, RING, L1, L2, L3 = f'{T_}q', f'{T_}r', f'{T_}a', f'{T_}b', f'{T_}c'
    BALLD, SHELL = f'{T_}o', f'{T_}s'
    HK = f'{T_}k'
    start, clock, at0 = prelude(g, p, SH)
    tl = TL(g, key, clock=f'#apq{pid}T')
    tl.at(0, at0)
    # tracking until lock 1 (3 deg/t), then the yaw stays
    for t in range(0, Q3['lock1']):
        tl.at(t, 'function rlk:mboss/mv/turn {max:3}')
    # the lagging ring (keep row): the player's feet sampled every 2 t, the ring 6 t behind them from t10
    for t in range(Q3['ring'] - Q3['lag'], Q3['lock1'], Q3['every']):
        tl.at(t, f'execute at {PLAYER} positioned ~ {CY} ~ run {marker(pid, HIST)}',
              f'scoreboard players set @e[type=minecraft:marker,tag={HIST},tag=!{T_}x] apT 0',
              f'tag @e[type=minecraft:marker,tag={HIST}] add {T_}x')
    for t in range(Q3['ring'] - Q3['lag'], Q3['lock1']):
        tl.at(t, f'scoreboard players add @e[type=minecraft:marker,tag={HIST}] apT 1')
    tl.at(Q3['ring'], g.fn(f'p/{key}/ring_on'))
    for t in range(Q3['ring'] + Q3['every'], Q3['lock1'], Q3['every']):
        tl.at(t, g.fn(f'p/{key}/ring_step'))
    tl.at(Q3['lit'], f'execute at @s rotated as @s positioned {A.loc(BALL[0], BALL[2], BALL[1])} run {display(pid, BALLD)}',
          f'execute as {dsel(BALLD)} run {K.prop("charge_ball")}', f'execute at @s run {K.snd("q3_charge")}')
    tl.at(Q3['lock1'], g.fn(f'p/{key}/lock1'))
    tl.at(Q3['launch'], g.fn(f'p/{key}/launch'))
    tl.at(Q3['hit1'] - 1, f'kill {dsel(SHELL + "1")}')
    tl.at(Q3['hit1'], f'execute at {m1(L1)} run {K.fx("beam_column", w=3.0)}', f'execute at {m1(L1)} run {K.fx("leaf_splash")}',
          f'execute at {m1(L1)} run {K.fx("spores")}', f'execute at {m1(L1)} run {K.snd("q3_impact1")}')
    tl.at(Q3['lock2'], g.fn(f'p/{key}/lock2'))
    tl.at(Q3['lock3'], g.fn(f'p/{key}/lock3'))
    for k, (lk, hit) in enumerate(((L2, Q3['hit2']), (L3, Q3['hit3'])), start=2):
        tl.at(hit - Q3['streak'], f'kill {dsel(SHELL + str(k))}',
              f'execute at {m1(lk)} run {K.fx("shell_streak", h=Q3["hover"])}')
        tl.at(hit, f'execute at {m1(lk)} run {K.fx("shell_burst")}', f'execute at {m1(lk)} run {K.snd("q3_impact2")}')
    tl.at(Q3['release'], Gen.release())
    g.pw(key, 'ring_on', ['# t10: the target ring (keep row: the pale disc the footage shows under the player) at the feet of 6 t',
                          '# ago (the oldest sample), and the ring position marker.',
                          f'execute as @e[type=minecraft:marker,tag={HIST},scores={{apT={Q3["lag"]}..}},limit=1] at @s run {marker(pid, RING)}',
                          f'execute at {m1(RING)} run ' + Gen.decal('keep', K.tele_mring(0, Q3['r1']))[0],
                          f'kill @e[type=minecraft:marker,tag={HIST},scores={{apT={Q3["lag"]}..}}]'])
    g.pw(key, 'ring_step', ['# Every 2 t to t32: the ring to the feet of 6 t ago (the kit moves it over 2 t).',
                            f'execute as @e[type=minecraft:marker,tag={HIST},scores={{apT={Q3["lag"]}..}},limit=1] at @s run tp {m1(RING)} ~ ~ ~',
                            f'execute at {m1(RING)} run {K.tele_mring_move(0, Q3["every"])}',
                            f'kill @e[type=minecraft:marker,tag={HIST},scores={{apT={Q3["lag"]}..}}]'])
    g.pw(key, 'lock1', [
        f'# t{Q3["lock1"]}: the ring stops = lock 1 (L1); shell 1 r {Q3["r1"]} (tell {Q3["tell1"]}, light KB, {A.DMG["q3_1"]} %) with the',
        '# held target disc of the keep row; the history goes.',
        f'execute at {m1(RING)} run {marker(pid, L1)}', K.tele_mring_end(0), f'kill {mall(HIST)}',
        f'execute at {m1(L1)} run {g.fn(f"p/{key}/hz1")}'])
    g.pw(key, 'hz1', [*hz(L.hz_disc(Q3['r1'], Q3['tell1'], A.DMG['q3_1']), tag=HK, kb=KB2),
                      *Gen.decal('keep', K.tele_disc(Q3['r1'], Q3['tell1'], fill=0))])
    g.pw(key, 'launch', [
        f'# t{Q3["launch"]}: one launch, the three shells go up from the light ball (shell 1 drops as the beam at t45; shells 2 / 3',
        '# hover high until their locks, then stand over their points: the readable tell of the none rows).',
        f'execute at {dsel(BALLD, ",limit=1")} run {K.fx("launch_flash")}', f'execute at @s run {K.snd("q3_launch")}',
        *[f'execute at {dsel(BALLD, ",limit=1")} run {display(pid, SHELL, SHELL + str(k), td=8)}' for k in (1, 2, 3)],
        f'execute as {dsel(SHELL)} run {K.prop("charge_ball")}', f'kill {dsel(BALLD)}',
        f'execute at @s rotated as @s positioned ^ ^{num(BALL[1] + 9.0)} ^ as {dsel(SHELL + "1")} run tp @s ~ ~ ~',
        f'execute at @s rotated as @s positioned ^2.5 ^{num(BALL[1] + 7.0)} ^ as {dsel(SHELL + "2")} run tp @s ~ ~ ~',
        f'execute at @s rotated as @s positioned ^-2.5 ^{num(BALL[1] + 7.0)} ^ as {dsel(SHELL + "3")} run tp @s ~ ~ ~'])
    hz23 = []
    for k, (lk, lockl, tell) in enumerate(((L2, Gen.lockv(Q3['lead2']), Q3['tell2']), (L3, [Gen.lockp()], Q3['tell3'])), start=2):
        lines = [f'# t{Q3["lock" + str(k)]}: lock {k} ({"lockv lead 8" if k == 2 else "lockp"}); shell {k} r {Q3["r23"]} (tell {tell}, '
                 f'{A.DMG["q3_23"]} %), quiet (none row);',
                 '# the hovering shell moves over its point (10 b up) and stays there to the streak.',
                 *lockl, *Gen.keep(lk)]
        if k == 2:
            lines += [Gen.GRP_NEW, f'scoreboard players operation #apq{pid}G mb = #mbGrp mb']
        lines += [f'execute at {m1(lk)} run {g.fn(f"p/{key}/hz{k}")}',
                  f'execute as {dsel(SHELL + str(k))} run data merge entity @s {{teleport_duration:3}}',
                  f'execute at {m1(lk)} positioned ~ ~{num(Q3["hover"])} ~ as {dsel(SHELL + str(k))} run tp @s ~ ~ ~']
        g.pw(key, f'lock{k}', lines)
        g.pw(key, f'hz{k}', [*Gen.hz_opts(), f'scoreboard players operation #hzGrp mb = #apq{pid}G mb',
                             L.hz_disc(Q3['r23'], tell, A.DMG['q3_23']), Gen.tag_last_hz(f'{T_}h')])
        hz23.append(k)
    tl.write(tl_head(p, f'shells: ring {Q3["ring"]}, lock 1 {Q3["lock1"]} -> hit {Q3["hit1"]}, locks {Q3["lock2"]} / {Q3["lock3"]} -> '
                        f'hits {Q3["hit2"]} / {Q3["hit3"]}, end {Q3["end"]}.') + start + [f'kill @e[tag={T_}]', f'scoreboard players set #apq{pid}G mb 0'],
             tl_head(p, 'tick (#apq33T = the clip tick).') + clock,
             t0=-1000, extra_tick=[f'execute if score #apq{pid}T mb matches {Q3["end"]}.. run return run {g.fn(f"p/{key}/done")}'])
    g.pw(key, 'done', ['# The clip is over: its own entities go (p/finish keeps only the core\'s), then p/end.', f'kill @e[tag={T_}]',
                       Gen.end()])
    g.pw(key, 'cancel', ['# Cut (any executor): its markers, the ball and the shells go; the ring decal ends.',
                         f'kill @e[tag={T_}]', K.tele_mring_end(0)])
    g.pw(key, 'resume', ['# Resume: the following ring (before lock 1) or the held target disc again (the pause cleared them).',
                         f'execute if score #apq{pid}T mb matches {Q3["ring"]}..{Q3["lock1"] - 1} at {m1(RING)} run '
                         + Gen.decal('keep', K.tele_mring(0, Q3['r1']))[0],
                         f'execute as @e[type=minecraft:marker,tag={HK}] at @s run {g.fn(f"p/{key}/redraw")}'])
    redraw_fn(g, key, f'p{pid}d', Q3['r1'], HK, pid=pid)


# ======================================================================================================== Q3s 수면 포격
SK_, SU, ST = 'sink_p3', 'surface_p3', 'stand_p3'
Q3S = dict(mound=ev(SK_, 'sink'), hide=ev(SK_, 'hide'), sink_end=A.clip_len(SK_), lock=26, place=34, surface=36,
           end=36 + A.clip_len(SU) + A.clip_len(ST), dist=9.0, glide=0.8, r_splash=3.6, r_shell=3.0, release=49)
Q3S['launch'] = Q3S['surface'] + ev(SU, 'launch')           # 46
Q3S['hit'] = Q3S['surface'] + ev(SU, 'hit')                 # 48
Q3S['splash_tell'] = Q3S['surface'] - Q3S['lock']           # 10
Q3S['shell_tell'] = Q3S['hit'] - Q3S['surface']             # 12
assert (Q3S['mound'], Q3S['launch'], Q3S['hit'], Q3S['end']) == (8, 46, 48, 90), Q3S
assert A.CLIPS[SU].get('next') == ST and A.hidden_spans(SK_)[0][0] == 12
MUZZLE = A.anchor(SU, 'launch', 'muzzle')                    # (0, 2.51, 4.34)


def emit_surface(g, p):
    key, pid = p.key, p.id
    T_ = f'rlk_mb_ap_p{pid}'
    SP, LK = f'{T_}u', f'{T_}l'
    HK = f'{T_}k'
    start, clock, at0 = prelude(g, p, SK_)
    tl = TL(g, key, clock=f'#apq{pid}T')
    tl.at(0, at0)
    tl.at(Q3S['mound'], f'execute at @s positioned ~ {CY} ~ run {K.fx("leaf_mound")}', f'execute at @s run {K.snd("q1_sink")}')
    for t in range(Q3S['sink_end'], Q3S['lock']):
        tl.at(t, f'execute at @s unless entity {near(PLAYER, Q3S["dist"] + 1)} run {Gen.move_to(PLAYER, Q3S["glide"])}')
    for t in range(Q3S['lock'] + 1, Q3S['place']):
        tl.at(t, f'execute at @s unless entity {near(m1(SP), 1.0)} run {Gen.move_to(m1(SP), Q3S["glide"])}')
    for t in range(Q3S['sink_end'], Q3S['surface'], 4):
        tgt = PLAYER if t <= Q3S['lock'] else m1(SP)
        tl.at(t, f'execute at @s positioned ~ {CY} ~ facing entity {tgt} feet rotated ~ 0 run {K.fx("leaf_pad")}',
              f'execute at @s run {K.snd("q1_trail")}')
    tl.at(Q3S['lock'], g.fn(f'p/{key}/lock'))
    tl.at(Q3S['place'], f'execute at {m1(SP)} run tp @s ~ {CY} ~', f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0')
    tl.at(Q3S['place'] + 1, f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0')
    tl.at(Q3S['surface'], Gen.play(SU), g.fn(f'p/{key}/surface'))
    tl.at(Q3S['launch'], g.fn(f'p/{key}/launch'))
    tl.at(Q3S['hit'], f'execute at {m1(LK)} run {K.fx("beam_column", w=2.0)}', f'execute at {m1(LK)} run {K.fx("shell_burst")}',
          f'execute at {m1(LK)} run {K.snd("q3s_impact")}')
    tl.at(Q3S['release'], Gen.release())
    g.pw(key, 'lock', [
        f'# @s = body (t{Q3S["lock"]}, hidden): the surfacing point = {Q3S["dist"]} b from the player toward the boss (lockb, clamp r 14);',
        f'# the surfacing splash r {Q3S["r_splash"]} (tell {Q3S["splash_tell"]}, {A.DMG["q3s_splash"]} %) with its keep decal (the leaf ring',
        '# the footage shows at the surfacing spot) and the circling leaves.',
        Gen.lockb(Q3S['dist']), *Gen.keep(SP),
        f'execute at {m1(SP)} run {g.fn(f"p/{key}/splash_hz")}'])
    g.pw(key, 'splash_hz', [*hz(L.hz_disc(Q3S['r_splash'], Q3S['splash_tell'], A.DMG['q3s_splash']), tag=HK),
                            *Gen.decal('keep', K.tele_disc(Q3S['r_splash'], Q3S['splash_tell'], fill=0)), K.fx('leaf_ring')])
    g.pw(key, 'surface', [
        f'# @s = body (t{Q3S["surface"]}): the surfacing splash (impact visual), the charge; lock L at the player; the shell r',
        f'# {Q3S["r_shell"]} (tell {Q3S["shell_tell"]}, {A.DMG["q3s_shell"]} %) with its keep decal (the pale disc under the player); the',
        '# light band length (muzzle -> L) for t46.',
        f'execute at @s positioned ~ {CY} ~ run {K.fx("surface_splash")}', f'execute at @s positioned ~ {CY} ~ run {K.fx("water_splash")}',
        f'execute at @s run {K.snd("q3s_surface")}', f'execute at @s run {K.snd("q3s_charge")}',
        Gen.lockp(), *Gen.keep(LK), f'execute at {m1(LK)} run {g.fn(f"p/{key}/shell_hz")}',
        g.fn(f'p/{key}/dist'),
        f'scoreboard players remove #apq{pid}D mb {int(round(MUZZLE[2] * 10))}',
        f'execute if score #apq{pid}D mb matches ..9 run scoreboard players set #apq{pid}D mb 10',
        f'execute store result storage rlk:mboss ap.p{pid}.len int 1 run scoreboard players get #apq{pid}D mb'])
    g.pw(key, 'dist', ['# @s = body: #apq36D = the horizontal distance to L in tenths.'] + mdist_lines(m1(LK), f'#apq{pid}D', f'#apq{pid}'))
    g.pw(key, 'shell_hz', [*hz(L.hz_disc(Q3S['r_shell'], Q3S['shell_tell'], A.DMG['q3s_shell']), tag=f'{T_}m'),
                           *Gen.decal('keep', K.tele_disc(Q3S['r_shell'], Q3S['shell_tell'], fill=0))])
    g.pw(key, 'launch', [f'# @s = body (t{Q3S["launch"]}): the flat shot: the light band from the muzzle toward L, the launch flash.',
                         f'execute at @s rotated as @s positioned {A.loc(MUZZLE[0], MUZZLE[2], MUZZLE[1])} facing entity {m1(LK)} feet rotated ~ 0 '
                         f'run function {K.FN}p/light_band with storage rlk:mboss ap.p{pid}',
                         f'execute at @s rotated as @s positioned {A.loc(MUZZLE[0], MUZZLE[2], MUZZLE[1])} run {K.fx("launch_flash")}',
                         f'execute at @s run {K.snd("q3s_launch")}'])
    tl.write(tl_head(p, f'sink 0-20 (hidden from 12), the surfacing point at {Q3S["lock"]}, surface {Q3S["surface"]}, shell hit '
                        f'{Q3S["hit"]}, stand 76-90.') + start + [f'kill @e[tag={T_}]'],
             tl_head(p, 'tick (#apq36T = the pattern tick after the prelude).') + clock,
             t0=-1000, extra_tick=[f'execute if score #apq{pid}T mb matches {Q3S["end"]}.. run return run {g.fn(f"p/{key}/done")}'])
    g.pw(key, 'done', ['# The clip is over: its own entities go (p/finish keeps only the core\'s), then p/end.', f'kill @e[tag={T_}]',
                       Gen.end()])
    g.pw(key, 'cancel', ['# Cut (any executor): its markers go.', f'kill @e[tag={T_}]', f'data remove storage rlk:mboss ap.p{pid}'])
    g.pw(key, 'resume', ['# Resume: the pending keep discs (surfacing splash, shell) again with the ticks left.',
                         f'execute as @e[type=minecraft:marker,tag={HK}] at @s run {g.fn(f"p/{key}/redraw")}',
                         f'execute as @e[type=minecraft:marker,tag={T_}m] at @s run {g.fn(f"p/{key}/redraw_s")}'])
    redraw_fn(g, key, f'p{pid}d', Q3S['r_splash'], HK, pid=pid)
    redraw_fn(g, key, f'p{pid}e', Q3S['r_shell'], f'{T_}m', sub='redraw_s', pid=pid)


# ======================================================================================================== Q4 생명의 꼬리
TP = 'tail_p3'
Q4 = dict(crouch=A.clip_len('crouch_p3'), walk=A.P3_WALK['max'], walk_spd=A.P3_WALK['spd'], far=A.Q4_FAR,
          cock=ev(TP, 'cock'), s1=ev(TP, 'swing1'), coil=ev(TP, 'coil'), s2=ev(TP, 'swing2'), end=A.clip_len(TP),
          lane1=2, lane2=32, lunge=(36, 40), reach=12.0, y1_1=3.0, y1_2=2.0, tip=11, shower=53, release=54)
assert (Q4['cock'], Q4['s1'], Q4['coil'], Q4['s2'], Q4['end'], Q4['crouch']) == (3, 14, 36, 46, 87, 8), Q4
SW1 = A.wedges(TP, Q4['s1'], Q4['s1'] + 7, Q4['reach'], swept=True)     # 8 wedges t14-21 (swept: RP1-3, AP-I2)
SW2 = A.wedges(TP, Q4['s2'], Q4['s2'] + 7, Q4['reach'], swept=True)     # 8 wedges t46-53 (reverse)
TIP11 = A.track(TP, 'tail_tip')[Q4['tip']]


def half_angle(w):
    return int(math.ceil((w['a1'] - w['a0']) / 2.0 + 0.5))


def arc_of(ws):
    """(mid bearing, half-angle, dir, root (s, f)) of a swing's crescent from its swept wedges."""
    lo, hi = min(w['a0'] for w in ws), max(w['a1'] for w in ws)
    first, last = ws[0], ws[-1]
    d = 1 if (last['a0'] + last['a1']) > (first['a0'] + first['a1']) else -1
    mid = ws[len(ws) // 2]['root']
    return (lo + hi) / 2.0, max(10, int(round((hi - lo) / 2.0))), d, mid


def emit_tail3(g, p):
    key, pid = p.key, p.id
    T_ = f'rlk_mb_ap_p{pid}'
    FR, FR2, EK = f'{T_}f', f'{T_}g', f'{T_}e'
    c = f'#apq{pid}T'
    tl = TL(g, key, clock=c)
    tl.at(0, Gen.play(TP), f'execute at @s run {marker(pid, FR)}', f'execute as {m1(FR)} at @s rotated as {BODY} run tp @s ~ ~ ~ ~ 0',
          f'scoreboard players operation #apq{pid}H mb = #mbHitEv mb')
    tl.at(Q4['lane1'], f'execute as {m1(FR)} at @s rotated as @s run {g.fn(f"p/{key}/sw1")}')
    tl.at(Q4['cock'], f'execute at @s run {K.snd("q4_rear")}')
    tl.at(Q4['tip'], f'execute as {m1(FR)} at @s rotated as @s positioned {A.loc(TIP11[0], TIP11[2], TIP11[1])} run {K.fx("tail_tip_flash")}')
    for (ws, t, snd, frame) in ((SW1, Q4['s1'], 'q4_swing', FR), (SW2, Q4['s2'], 'q4_swing2', FR2)):
        mid, a, d, root = arc_of(ws)
        tl.at(t, f'execute as {m1(frame)} at @s rotated as @s positioned {A.loc(root[0], root[1])} rotated ~{num(mid, 2)} 0 run '
                 f'{K.fx("crescent_trail", r=Q4["reach"], a=a, dir=d)}', f'execute at @s run {K.snd(snd)}')
    tl.at(Q4['lane2'], g.fn(f'p/{key}/lunge_pt'), f'execute as {m1(FR2)} at @s rotated as @s run {g.fn(f"p/{key}/sw2")}')
    tl.at(Q4['coil'], f'execute at @s run {K.snd("q4_rear")}')
    l0, l1 = Q4['lunge']
    for t in range(l0, l1):
        tl.at(t, f'execute at @s unless entity {near(m1(EK), 0.9)} run {Gen.move_to(m1(EK), 0.875)}')
    tl.at(l1, f'execute at {m1(EK)} run tp @s ~ {CY} ~')
    tl.at(Q4['shower'], f'execute at @s run {K.fx("glitter_shower")}')
    tl.at(Q4['release'], Gen.release())
    hit = [f'execute if score #mbHitEv mb > #apq{pid}H mb at @s run {K.snd("p5_hit")}',
           f'execute if score #mbHitEv mb > #apq{pid}H mb run {K.hud("flash_hit")}',
           f'scoreboard players operation #apq{pid}H mb = #mbHitEv mb']
    for t in list(range(Q4['s1'], Q4['s1'] + 8)) + list(range(Q4['s2'], Q4['s2'] + 8)):
        tl.at(t, *hit)
    for name, ws, made, y1, dmg in (('sw1', SW1, Q4['lane1'], Q4['y1_1'], 'q4_1'), ('sw2', SW2, Q4['lane2'], Q4['y1_2'], 'q4_2')):
        lines = [f'# As the frame marker (the start facing of tail_p3{" moved to the lunge end" if name == "sw2" else ""}), at it: the',
                 f'# per-tick swept wedges of {"swing 1" if name == "sw1" else "swing 2"} (plan 7.11 rule 3; api.wedges from the manifest\'s',
                 f'# tail track x the yaw schedule), r {Q4["reach"]}, height to {y1} b, heavy KB away, {A.DMG[dmg]} %, one volley group;',
                 '# quiet (none row: the crouch / cock + tail-tip flash, the S-coil + lunge are the tell).',
                 Gen.GRP_NEW]
        for w in ws:
            mid = (w['a0'] + w['a1']) / 2.0
            lines.append(f'execute positioned {A.loc(w["root"][0], w["root"][1])} positioned ~ {CY} ~ rotated ~{num(mid, 2)} 0 run '
                         f'{g.fn(f"p/{key}/{name}_{w["t"]}")}')
            g.pw(key, f'{name}_{w["t"]}', hz(L.hz_sector(Q4['reach'], half_angle(w), w['t'] - made, A.DMG[dmg]), tag=f'{T_}h',
                                            grp=True, y1=y1, kb=KB4, kbdir=0))
        g.pw(key, name, lines)
    g.pw(key, 'lunge_pt', [
        '# t32: the lunge end E (3.5 b toward the player, shorter when the player is closer; clamp r 16) and the swing-2',
        '# frame there (the start facing kept: the wedges of swing 2 are where the body will stand).',
        f'kill {mall(EK)}', f'kill {mall(FR2)}', f'execute at @s run {marker(pid, EK)}',
        f'execute at @s if entity {near(PLAYER, 99)} unless entity {near(PLAYER, 5.5)} as {m1(EK)} at @s facing entity {PLAYER} feet '
        'rotated ~ 0 run tp @s ^ ^ ^3.5',
        f'execute at @s if entity {near(PLAYER, 5.5)} unless entity {near(PLAYER, 4.5)} as {m1(EK)} at @s facing entity {PLAYER} feet '
        'rotated ~ 0 run tp @s ^ ^ ^2.5',
        f'execute at @s if entity {near(PLAYER, 4.5)} unless entity {near(PLAYER, 3.5)} as {m1(EK)} at @s facing entity {PLAYER} feet '
        'rotated ~ 0 run tp @s ^ ^ ^1.5',
        f'execute as {m1(EK)} run {Gen.clamp("glide")}',
        f'execute at {m1(EK)} run {marker(pid, FR2)}', f'execute as {m1(FR2)} at @s rotated as {m1(FR)} run tp @s ~ ~ ~ ~ 0'])
    o = f'#apq{pid}O'
    walk_on = f'execute if score #apq{pid} mb matches 1'
    start = [f'# {p.label} ({p.key}, id {pid}; plan 8.3 Q4): crouch_p3 (the core plays it at 0), the walk opener when the player',
             f'# is farther than {Q4["far"]} b (#apq{pid} 1: walk_p3 <= {Q4["walk"]} t at {Q4["walk_spd"]} b/t), then tail_p3 at {c} 0.',
             f'kill @e[tag={T_}]', 'function rlk:mboss/mv/dist', f'scoreboard players set #apq{pid} mb 0',
             f'execute if score #mbDist mb matches {int(A.Q4_FAR * 10) + 1}.. run scoreboard players set #apq{pid} mb 1',
             f'scoreboard players set {o} mb {Q4["crouch"]}',
             f'{walk_on} run scoreboard players set {o} mb {Q4["crouch"] + Q4["walk"]}',
             Gen.set_len(Q4['crouch'] + Q4['end']), f'{walk_on} run ' + Gen.set_len(Q4['crouch'] + Q4['walk'] + Q4['end']),
             f'scoreboard players operation {c} mb = #apPT mb', f'scoreboard players operation {c} mb -= {o} mb']
    extra = [f'scoreboard players operation {c} mb = #apPT mb', f'scoreboard players operation {c} mb -= {o} mb',
             f'execute if score {c} mb matches ..-1 run function rlk:mboss/mv/turn {{max:{A.TURN_MAX[3]}}}',
             f'{walk_on} if score #apPT mb matches {Q4["crouch"]} run {Gen.play("walk_p3")}',
             f'{walk_on} if score {c} mb matches ..-1 if score #apPT mb matches {Q4["crouch"] + 1}.. at {PLAYER} unless entity @s[distance=..5] '
             f'as {BODY} at @s run {Gen.move_to(PLAYER, Q4["walk_spd"])}',
             f'execute if score {c} mb matches {Q4["end"]}.. run return run {g.fn(f"p/{key}/done")}']
    tl.write(start, tl_head(p, 'tick (#apq34T = the tail_p3 tick; negative during the crouch / walk opener).'), t0=-1000,
             extra_tick=extra)
    g.pw(key, 'done', ['# The clip is over: its own entities go (p/finish keeps only the core\'s), then p/end.', f'kill @e[tag={T_}]',
                       Gen.end()])
    g.pw(key, 'cancel', ['# Cut (any executor): its markers go.', f'kill @e[tag={T_}]'])


# ======================================================================================================== Q5 생명의 나선
SP_ = 'spikes'
Q5 = dict(curl=ev(SP_, 'curl'), rise=ev(SP_, 'rise'), column=ev(SP_, 'column'), summon=ev(SP_, 'summon'),
          lockA=ev(SP_, 'lockA'), fireA=ev(SP_, 'fireA'), lockB=ev(SP_, 'lockB'), fireB=ev(SP_, 'fireB'), hitA=ev(SP_, 'hitA'),
          blades=ev(SP_, 'blades'), hitB=ev(SP_, 'hitB'), skim=ev(SP_, 'skim'), end=A.clip_len(SP_), r=2.0, ring=3.4,
          blade_len=14.0, blade_w=2.2, blade_y1=0.7, blade_ang=35, release=65, orb_y=0.4)
assert (Q5['lockA'], Q5['fireA'], Q5['hitA'], Q5['lockB'], Q5['fireB'], Q5['hitB'], Q5['blades'], Q5['skim'], Q5['end']) == \
    (37, 42, 49, 43, 48, 55, 52, 64, 72), Q5
Q5['tellA'] = Q5['hitA'] - Q5['lockA']                       # 12
Q5['tellB'] = Q5['hitB'] - Q5['lockB']                       # 12
Q5['tell_bl'] = Q5['skim'] - Q5['blades']                    # 12
CROWN = A.anchor(SP_, 'summon', 'crown')                     # (0, 7.95, 0.6)
# the 12 orb spots (x left, y up, z forward from the anchor; plan: +-7 b sideways, 3-10 b up): volley A = the left side
# (orbs 1-6), volley B = the right side (7-12); summoned one a tick from t19, alternating sides
ORB_SPOTS = {1: (2.5, 9.5, 0.5), 2: (4.0, 8.0, -0.5), 3: (5.5, 6.5, 0.8), 4: (6.8, 5.0, -0.3), 5: (4.8, 3.5, 1.2),
             6: (3.0, 4.8, -1.4)}
ORB_SPOTS.update({k + 6: (-x, y + 0.4, z) for k, (x, y, z) in list(ORB_SPOTS.items())})
ORB_ORDER = [1, 7, 2, 8, 3, 9, 4, 10, 5, 11, 6, 12]          # t19 .. t30
LAND = [(0.0, 0.0)] + [(Q5['ring'] * math.sin(math.radians(72 * k)), Q5['ring'] * math.cos(math.radians(72 * k)))
                       for k in range(5)]                    # the scatter: the lock + 5 on r 3.4 (x left, z forward)


def emit_spiral(g, p):
    key, pid = p.key, p.id
    T_ = f'rlk_mb_ap_p{pid}'
    ORB, LANDM, LKA, LKB, BLD, BLF = f'{T_}o', f'{T_}d', f'{T_}a', f'{T_}b', f'{T_}w', f'{T_}x'
    start, clock, at0 = prelude(g, p, SP_)
    tl = TL(g, key, clock=f'#apq{pid}T')
    tl.at(0, at0)
    for t in range(0, Q5['lockA']):
        tl.at(t, 'function rlk:mboss/mv/turn {max:3}')
    tl.at(Q5['rise'], f'execute at @s run {K.fx("charge_streaks")}', f'execute at @s run {K.snd("q5_unfold")}')
    tl.at(Q5['column'], f'execute at @s positioned ~ {CY} ~ run {K.fx("beam_column", w=1.5)}')
    for i, k in enumerate(ORB_ORDER):
        t = Q5['summon'] + i
        lines = [f'execute at @s rotated as @s positioned {A.loc(CROWN[0], CROWN[2], CROWN[1])} run {display(pid, ORB, T_ + "n", td=5)}',
                 f'execute as {dsel(T_ + "n")} run {K.prop("seed_orb")}',
                 f'scoreboard players set {dsel(T_ + "n")} apL {k}', f'tag {dsel(T_ + "n")} remove {T_}n',
                 f'execute at @s run {K.snd("q5_orb")}']
        if i:
            k0 = ORB_ORDER[i - 1]
            x, y, z = ORB_SPOTS[k0]
            lines.insert(0, f'execute at @s rotated as @s positioned {A.loc(x, z, y)} as {dsel(ORB, f",scores={{apL={k0}}}")} run tp @s ~ ~ ~')
        tl.at(t, *lines)
    kl = ORB_ORDER[-1]
    x, y, z = ORB_SPOTS[kl]
    tl.at(Q5['summon'] + len(ORB_ORDER), f'execute at @s rotated as @s positioned {A.loc(x, z, y)} as {dsel(ORB, f",scores={{apL={kl}}}")} '
                                          'run tp @s ~ ~ ~')
    for lockt, lk, ids, tag in ((Q5['lockA'], LKA, range(1, 7), 'A'), (Q5['lockB'], LKB, range(7, 13), 'B')):
        tl.at(lockt, g.fn(f'p/{key}/lock{tag.lower()}'))
        lo = ids[0]
        tl.at(lockt + 1, f'execute as @e[type=minecraft:marker,tag={LANDM},scores={{apL={lo + 3}..{lo + 5}}}] at @s run '
                         f'{g.fn(f"p/{key}/land_hz")} {{tell:{Q5["tellA"] - 1}}}')
    for t0, t1, lo, hi in ((Q5['fireA'], Q5['hitA'], 1, 6), (Q5['fireB'], Q5['hitB'], 7, 12)):
        tl.at(t0, f'execute at @s run {K.snd("q5_launch")}',
              f'execute as {dsel(ORB, f",scores={{apL={lo}..{hi}}}")} run data merge entity @s {{teleport_duration:1}}')
        for t in range(t0, t1):
            tl.at(t, f'scoreboard players set #apq{pid}R mb {t1 - t}',
                  f'execute as {dsel(ORB, f",scores={{apL={lo}..{hi}}}")} at @s run {g.fn(f"p/{key}/fly")}')
        tl.at(t1, f'execute as @e[type=minecraft:marker,tag={LANDM},scores={{apL={lo}..{hi}}}] at @s run {g.fn(f"p/{key}/land")}',
              f'kill {dsel(ORB, f",scores={{apL={lo}..{hi}}}")}', f'execute at @s run {K.snd("q5_impact")}')
    tl.at(Q5['blades'], g.fn(f'p/{key}/blades'))
    tl.at(Q5['skim'], f'execute as @e[type=minecraft:marker,tag={BLF}] at @s rotated as @s run {K.fx("leaf_skim", len=Q5["blade_len"])}',
          f'kill {dsel(BLD)}', f'execute at @s run {K.snd("q5_blades")}')
    tl.at(Q5['release'], Gen.release())
    for tag, lk, lo, lockt, tell in (('A', LKA, 1, Q5['lockA'], Q5['tellA']), ('B', LKB, 7, Q5['lockB'], Q5['tellB'])):
        lines = [f'# t{lockt}: lock {tag} = the floor under the player (lockp, no lead); 6 landing points (the lock + 5 on r {Q5["ring"]},',
                 f'# a random turn), each a disc r {Q5["r"]} (tell {tell}, {A.DMG["q5_volley"]} %), quiet (none row: the orbs flare now and',
                 '# fly visibly); volleys A and B share one volley group. The landing markers pair with the orbs by apL.',
                 Gen.lockp(), *Gen.keep(lk), f'scoreboard players set #apq{pid}J mb 0',
                 f'execute store result score #apq{pid}X mb run random value 0..71',
                 f'execute as {m1(lk)} store result entity @s Rotation[0] float 1 run scoreboard players get #apq{pid}X mb']
        if tag == 'A':
            lines += [Gen.GRP_NEW, f'scoreboard players operation #apq{pid}G mb = #mbGrp mb']
        for j, (lx, lz) in enumerate(LAND):
            lines.append(f'execute at {m1(lk)} rotated as {m1(lk)} positioned {A.loc(lx, lz)} positioned ~ {CY} ~ run '
                         f'{g.fn(f"p/{key}/land_pt")} {{k:{lo + j}}}')
        lines.append('# the disc hazards of the last three points one tick later (tell 11: the same strike tick; the per-tick budget)')
        lines += [f'execute as {dsel(ORB, f",scores={{apL={lo}..{lo + 5}}}")} at @s run {K.fx("star_flare")}',
                  f'execute at @s run {K.snd("q5_flare")}']
        g.pw(key, f'lock{tag.lower()}', lines)
    g.pw(key, 'land_pt', [f'# Macro {{k}}: one landing point here (marker apL k); the first three of a volley make their disc hazard now.',
                          marker(pid, LANDM, T_ + 'n'), f'$scoreboard players set {mall(T_ + "n")} apL $(k)',
                          f'tag {mall(T_ + "n")} remove {T_}n',
                          f'execute unless score #apq{pid}J mb matches 3.. run function {NS}p/{key}/land_hz {{tell:{Q5["tellA"]}}}',
                          f'scoreboard players add #apq{pid}J mb 1'])
    g.pw(key, 'land_hz', ['# Macro {tell}: the landing disc here in the volleys\' group (quiet: none row).',
                          *Gen.hz_opts(), f'scoreboard players operation #hzGrp mb = #apq{pid}G mb',
                          '$' + L.hz_disc(Q5['r'], 1, A.DMG['q5_volley']).replace('tell:1,', 'tell:$(tell),'),
                          Gen.tag_last_hz(f'{T_}h')])
    g.pw(key, 'fly', [
        '# @s = a flying orb, at it: one step toward its landing point (the marker with the same apL), 1 / #apq35R of the way',
        '# left (it arrives on the tick before the landing), the double-helix trail facing the flight.',
        f'scoreboard players operation #apq{pid}K mb = @s apL',
        f'execute as {mall(LANDM)} if score @s apL = #apq{pid}K mb run tag @s add {T_}t',
        f'execute facing entity {m1(T_ + "t")} feet run {K.fx("helix_trail")}',
        *[ln for i in range(3) for ln in (
            f'execute store result score #apq{pid}X mb run data get entity {m1(T_ + "t")} Pos[{i}] 1000',
            *([f'scoreboard players add #apq{pid}X mb {int(Q5["orb_y"] * 1000)}'] if i == 1 else []),
            f'execute store result score #apq{pid}Y mb run data get entity @s Pos[{i}] 1000',
            f'scoreboard players operation #apq{pid}X mb -= #apq{pid}Y mb', f'scoreboard players operation #apq{pid}X mb /= #apq{pid}R mb',
            f'scoreboard players operation #apq{pid}Y mb += #apq{pid}X mb',
            f'execute store result entity @s Pos[{i}] double 0.001 run scoreboard players get #apq{pid}Y mb')],
        f'tag {mall(T_ + "t")} remove {T_}t'])
    g.pw(key, 'land', ['# @s = a landing marker at its hit tick: the impact visual (star burst + upthrust spikes); the marker goes.',
                       K.fx('orb_impact'), 'kill @s'])
    bl = [f'# t{Q5["blades"]}: two low leaf-blade lanes crossing the player\'s spot (+-{Q5["blade_ang"]} deg about the boss -> player',
          f'# line), each a line {Q5["blade_len"]} x {Q5["blade_w"]} b (#hzY1 {Q5["blade_y1"]}: jumpable), tell {Q5["tell_bl"]}, '
          f'{A.DMG["q5_blade"]} %, one volley group;',
          '# quiet (none row): the blades stand glowing at the lane starts from now to the skim (the readable tell).',
          Gen.lockp(), *Gen.keep(f'{T_}p'), f'kill {mall(BLF)}', f'kill {dsel(BLD)}', Gen.GRP_NEW]
    for sgn in (1, -1):
        bl.append(f'execute at {m1(T_ + "p")} facing entity {BODY} feet rotated ~{180 + sgn * Q5["blade_ang"]} 0 positioned '
                  f'^ ^ ^{num(-Q5["blade_len"] / 2)} run {g.fn(f"p/{key}/blade")}')
    g.pw(key, 'blades', bl)
    g.pw(key, 'blade', ['# At a lane start, rotated = the lane: its frame marker, the standing blade (kit look), the lane hazard.',
                        marker(pid, BLF, T_ + 'n'), f'execute as {mall(T_ + "n")} run tp @s ~ ~ ~ ~ 0', f'tag {mall(T_ + "n")} remove {T_}n',
                        f'execute positioned ~ ~0.15 ~ run {display(pid, BLD, T_ + "n", td=1)}',
                        f'execute as {dsel(T_ + "n")} run data merge entity @s {{billboard:"vertical",view_range:2f,'
                        'transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.1f,1.8f,1.1f],'
                        'right_rotation:[0f,0f,0f,1f]}}',
                        f'execute as {dsel(T_ + "n")} run {K.look("leaf_blade", 0xF3F0A6)}', f'tag {dsel(T_ + "n")} remove {T_}n',
                        *Gen.hz_opts(grp=True, y1=Q5['blade_y1']),
                        L.hz_line(Q5['blade_len'], Q5['blade_w'], Q5['tell_bl'], A.DMG['q5_blade']), Gen.tag_last_hz(f'{T_}h')])
    tl.write(tl_head(p, f'spikes: orbs {Q5["summon"]}-{Q5["summon"] + 11}, locks {Q5["lockA"]} / {Q5["lockB"]} -> landings {Q5["hitA"]} / '
                        f'{Q5["hitB"]}, blades {Q5["blades"]} -> skim {Q5["skim"]}, end {Q5["end"]}.') + start
             + [f'kill @e[tag={T_}]', f'scoreboard players set #apq{pid}G mb 0'],
             tl_head(p, 'tick (#apq35T = the clip tick).') + clock,
             t0=-1000, extra_tick=[f'execute if score #apq{pid}T mb matches {Q5["end"]}.. run return run {g.fn(f"p/{key}/done")}'])
    g.pw(key, 'done', ['# The clip is over: its own entities go (p/finish keeps only the core\'s), then p/end.', f'kill @e[tag={T_}]',
                       Gen.end()])
    g.pw(key, 'cancel', ['# Cut (any executor): the orbs, blades and markers go.', f'kill @e[tag={T_}]'])


# ======================================================================================================== records
Q4_LEN = Q4['crouch'] + Q4['end']                  # 95; + 30 with the walk opener
PATTERNS = [
    Pattern(31, 'mstrike', '이동 돌진', 'normal', MS, phase=3, weight=W3(1, 2, 3),
            length=Q1['end'], recover=20, max_len=Q1['end'] + STAND + 20, last_hit=Q1['sweep'], hooks=('resume',)),
    Pattern(33, 'shells', '증폭의 풀', 'normal', SH, phase=3, weight=W3(1, 3, 3),
            length=Q3['end'], recover=20, max_len=Q3['end'] + STAND + 20, last_hit=Q3['hit3'], chain={36: 30}, hooks=('resume',)),
    Pattern(34, 'tail3', '생명의 꼬리', 'normal', ['crouch_p3', 'walk_p3', TP], phase=3, weight=W3(3, 2, 1),
            length=Q4_LEN, recover=18, max_len=Q4_LEN + Q4['walk'] + 20, last_hit=Q4['crouch'] + Q4['s2'] + 7),
    Pattern(35, 'spiral', '생명의 나선', 'normal', SP_, phase=3, weight=W3(2, 2, 2),
            length=Q5['end'], recover=20, max_len=Q5['end'] + STAND + 20, last_hit=Q5['skim'], chain={31: 40}),
    Pattern(36, 'surface', '수면 포격', 'chain', [SK_, SU, ST], phase=3,
            length=Q3S['end'], recover=20, max_len=Q3S['end'] + STAND + 20, last_hit=Q3S['hit'], hooks=('resume',)),
]
P = {p.key: p for p in PATTERNS}


def emit(g):
    emit_mstrike(g, P['mstrike'])
    emit_shells(g, P['shells'])
    emit_tail3(g, P['tail3'])
    emit_spiral(g, P['spiral'])
    emit_surface(g, P['surface'])
