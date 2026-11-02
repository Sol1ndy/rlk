"""Core of the 아를레키노 module (OWNER: S3; plan S:ar/PLAN.md §4, §7; contract S:ar/contract.md §3): the 17 hooks + prep +
test/help, init / uninstall (objective kn), the phase machine intro -> P1a -> (70 % floor) E70 -> P1b -> (floor 1) T ->
repool 36 -> P2 (Q0 first) -> death, #mbFloor, music phases, the boss-bar HUD (sub line = phase sub / pattern name, the
badge 선혈의 충격), the break windows (body tag rlk_kn_win + the real-game banner), the break -> stun, pause / resume /
reload / cleanup per phase, the kit wiring (contract §3.3), the rig stand-in rig_stub/** (while S2's manifest is missing)
and the stand-in sequences core/sq/** (while S2's seq.SERVICES lacks one), the gate flames chain of prep, the tests.

#pat: a pattern's test id (api.TEST_IDS: 1-13 P1 strings, 20 E70, 41-48 P2), STUN_PAT the break stun, TR_PAT the
transition, REPLAY_PAT the intro replay (test 25). #ph: api.PH. #fl: 1 = E70 reserved (the 70 % floor was reached),
2 = T reserved (floor 1 reached); the step starts at the next decision (the running pattern finishes). #e70: 0 / 1 running
/ 2 done. Sequences: S2 owns the motion, effects, titles, dialog and the push ring of seq/<name>; the core owns phases,
invulnerability, cine, repool and music (S2 brief); the stand-ins do both while S2's are missing.
"""
import help_lib as H

from . import api
from . import s3lib as S
from . import ai as AI

L, K = api.L, api.K
OBJ = api.OBJ
fn, sset = S.fn, S.sset
NS = api.NS
CY = api.CY
PH = api.PH
STUN_PAT, TR_PAT, REPLAY_PAT = 50, 51, 52
BRK_LEN = api.CLIPS['brk'][0]
INTRO_LEN = api.CLIPS['intro'][0]
T_LEN = api.CLIPS['t_p2'][0]
T_TITLE = api.ev('t_p2', 'title')
CONSTS = (2, 5, 10, 64, 100, 577, 1000)
SUB_HEX, BADGE_HEX = '#E8E2D0', '#FF3A4A'
P2_KEYS = set(api.P2)
LINE_GAP = 80                         # a cast's dialog line is skipped when another one started less than this ago
LINE_ALWAYS = ('e70', 'f1', 'q5a', 'q5b', 'q6')   # the event / scheduled casts always speak


class Ctx:
    """What the build knows: the present patterns (S3's P1 + S4's P2), the S4 files written, the services."""

    def __init__(self, pats, w4, services):
        self.pats = {p.key: p for p in pats}
        self.present = sorted(self.pats, key=lambda k: S.TID[k])
        self.w4 = w4
        self.services = {s.name: s for s in services}
        self.groups = None
        self.groups_all = []

    def has_file(self, key, rel, w3):
        W = self.w4 if key in P2_KEYS else w3
        return (api.L.FN / f'{api.ROOT}/p/{key}/{rel}.mcfunction').resolve() in W.out.written


def at_body(cmd):
    return f'execute as {S.BODY} at @s run {cmd}'


def seq_or_stand(ctx, name, part):
    """The S2 sequence call seq/<name>/<part>, or the core stand-in core/sq/<name>/<part>."""
    if name in ctx.services:
        return fn(f'seq/{name}/{part}')
    return fn(f'core/sq/{name}/{part}')


def group_of(key):
    """The AI group of a pattern key (E70 is the core's event: its own id, no cooldown)."""
    if key == 'e70':
        return 'E70'
    return next(g for g, cols in api.GROUPS.items() if any(key in v for v in cols.values()))


def build(W, ctx):
    w = W.w
    present = ctx.present
    pats = [k for k in present if k != 'e70']
    # ---------------------------------------------------------------------------------------------- init / vars
    w('init', ['# The module objective + constants (spawn, reload; idempotent). Removed by uninstall.',
               f'scoreboard objectives add {OBJ} dummy']
      + [sset(f'#c{c}', c) for c in CONSTS] + [sset('#cn1', -1), sset('#cn1000', -1000)])
    zero = ['#ph', '#pat', '#pt', '#done', '#clk', '#sq', '#sqdone', '#bonded', '#given', '#shock', '#shk_hit', '#brk',
            '#stun', '#stun_t', '#e70', '#win', '#lines', '#last', '#last2', '#rear', '#far', '#dec', '#rec', '#fl', '#tst',
            '#lock', '#dot_t', '#orbs', '#q0_ok', '#bolw', '#hitev', '#pbol', '#ai_pht', '#ai_mv', '#ai_nf', '#ai_nq',
            '#ai_q5', '#trt', '#fl70']
    # #lines starts far in the past (the first cast speaks)
    w('core/vars', ['# Every module fake player to its fight-start value (spawn).'] + [sset(k, 0) for k in zero]
      + [sset('#ai_d2', 100000), sset('#sch_f', 1000000), sset('#sch_q5', 1000000), sset('#lines', -1000)]
      + [sset(f'#cd_{g}', 0) for g in ctx.groups_all if g in api.COOLDOWN])
    # ---------------------------------------------------------------------------------------------- spawn / setup
    w('spawn', ['# Hook spawn (@s = the arena marker at the centre of fl_ruins). The chapter body (mboss/cb/body: a boss, not a',
                '# miniboss, so the chapter kill / reward path runs; husk scale 1.4, click shield 1.2 x 2.9, no proxies) stands at',
                '# the centre facing south (yaw 0), toward the player arriving at the south edge; rlk_mb_inv until the intro ends.',
                'execute rotated 0 0 run function rlk:mboss/cb/body',
                at_body(fn('core/setup'))])
    w('core/setup', ['# @s = the new body: module state, the rig (form p1, the tea props, the scythe not yet formed).',
                     fn('init'), fn('core/vars'), api.rig('init'), api.rig('spawn'), api.rig('look/form/p1'),
                     api.rig('look/wings/off'), api.rig('look/glow/normal'), api.rig('look/weapon_r/gone'),
                     api.rig('look/weapon_l/gone'), api.rig('look/props/tea'),
                     'data modify storage rlk:mboss sub set value []'])
    w('core/looks', ['# The rig looks of the current phase (reload, phase steps, tests; @s = body).',
                     f'execute if score #ph {OBJ} matches ..{PH["t"]} run {api.rig("look/form/p1")}',
                     f'execute if score #ph {OBJ} matches {PH["p2"]}.. run {api.rig("look/form/p2")}',
                     api.rig('look/props/none'), api.rig('state/normal'), fn('core/looks_rest')])
    w('core/looks_rest', ['# The rest looks between casts (@s = body): wings folded, the scythe edge normal, the scythe(s) in hand.',
                          api.rig('look/wings/off'), api.rig('look/glow/normal'), api.rig('look/weapon_r/hand'),
                          f'execute if score #ph {OBJ} matches ..{PH["t"]} run {api.rig("look/weapon_l/gone")}',
                          f'execute if score #ph {OBJ} matches {PH["p2"]}.. run {api.rig("look/weapon_l/hand")}'])
    w('core/floors', ['# The 70 % floor (absolute HP) of the P1 pool (@s = body; the pool is phases[0] of the total).',
                      f'scoreboard players operation #fl70 {OBJ} = @s mhpM',
                      f'scoreboard players operation #fl70 {OBJ} /= #c100 {OBJ}',
                      f'scoreboard players set #t {OBJ} {api.FLOOR_E70_PCT}',
                      f'scoreboard players operation #fl70 {OBJ} *= #t {OBJ}',
                      f'execute if score #fl70 {OBJ} matches ..1 run scoreboard players set #fl70 {OBJ} 2'])
    w('core/floor_hit', [
        '# A hit reached the floor (#mbFloorHit, framework) or her HP sits on it (DoTs, reactions; @s = body): the phase step',
        '# is reserved for the next decision (#fl 1 = E70 in P1a, 2 = T in P1b). Nothing else changes now.',
        'scoreboard players set #mbFloorHit mb 0',
        f'execute unless score #fl {OBJ} matches 0 run return 0',
        f'execute if score #ph {OBJ} matches {PH["p1a"]} if score #e70 {OBJ} matches 0 run return run {sset("#fl", 1)}',
        f'execute if score #ph {OBJ} matches {PH["p1b"]} run {sset("#fl", 2)}'])
    w('core/hp_floor', [
        f'execute if score #ph {OBJ} matches {PH["p1a"]} if score @s mhpC <= #mbFloor mb run {fn("core/floor_hit")}',
        f'execute if score #ph {OBJ} matches {PH["p1b"]} if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run '
        f'{fn("core/floor_hit")}'])
    # ---------------------------------------------------------------------------------------------- intro
    w('intro_tick', [
        f'# Hook intro_tick (@s = body, #mbT 1..; rlk_mb_inv). The intro sequence ({INTRO_LEN} t clip, seq/intro or the stand-in)',
        f'# on the clock #sq kn; music phase 1 at {api.ev("intro", "music")} (core); the fight at its end.',
        f'execute if score #mbT mb matches 1 run {fn("core/intro/begin")}',
        f'execute unless score #mbT mb matches 1 run scoreboard players add #sq {OBJ} 1',
        f'execute unless score #mbT mb matches 1 run {seq_or_stand(ctx, "intro", "tick")}',
        f'execute if score #sq {OBJ} matches {api.ev("intro", "music")} run {L.music(1)}',
        f'execute if score #sqdone {OBJ} matches 1 run {fn("core/intro/done")}',
        f'execute if score #sq {OBJ} matches {INTRO_LEN + 2}.. run {fn("core/intro/done")}',
        api.rig('tick')])
    w('core/intro/begin', ['# Intro tick 0 (@s = body).', sset('#sq', 0), sset('#sqdone', 0), sset('#ph', PH['intro']),
                           seq_or_stand(ctx, 'intro', 'start')])
    w('core/intro/done', [
        '# The intro is over (its end, the framework cap, a reload or a test; @s = body): the fight state, P1a, the 70 % floor.',
        'function rlk:mboss/intro_end',
        f'execute unless score #ph {OBJ} matches {PH["intro"]} run return 0',
        sset('#ph', PH['p1a']), sset('#sq', 0), sset('#sqdone', 0), sset('#pat', 0), fn('core/floors'),
        f'scoreboard players operation #mbFloor mb = #fl70 {OBJ}',
        fn('ai/phase'), fn('core/looks'), fn('ai/sample'), fn('ai/rec_start'), sset('#rec', 20), fn('hud/sub')])
    w('core/intro/reload', ['# /reload during the intro: straight to its end (standing, the scythe drawn), title and music phase 1.',
                            seq_or_stand(ctx, 'intro', 'cancel'), L.title(*api.TITLE_P1, api.TITLE_COLOR[1]),
                            fn('core/intro/done'), L.music(1)])
    # ---------------------------------------------------------------------------------------------- the fight tick
    w('tick', [
        '# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==',
        '# the pattern clock #pt).',
        f'execute if score #ph {OBJ} matches {PH["intro"]} run {fn("core/intro/done")}',
        f'execute if score #ph {OBJ} matches {PH["p1a"]}..{PH["p2"]} run {fn("core/fight")}',
        api.rig('tick')])
    fight = [
        '# One fight tick (@s = body): the module clock, the floor, the bond (events of the last tick, the shock resolve),',
        f'# AI samples every {AI.SAMPLE_EVERY} t, then the running state (hold, stun, pattern, transition, replay, recovery).',
        f'scoreboard players add #clk {OBJ} 1',
        f'scoreboard players add #ai_pht {OBJ} 1',
        'execute unless score #mbSt mb matches 1 run return 0',
        f'execute if score #mbFloorHit mb matches 1 run {fn("core/floor_hit")}',
        f'execute if score #mbFloor mb matches 1.. run {fn("core/hp_floor")}',
        fn('bond/tick'),
        'execute unless score #mbSt mb matches 1 run return 0',
        f'scoreboard players operation #t {OBJ} = #clk {OBJ}',
        f'scoreboard players operation #t {OBJ} %= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches 0 run {fn("ai/sample")}',
        f'execute if score #pat {OBJ} matches {STUN_PAT} run return run {fn("core/stun_tick")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} run return run {fn("core/tr/tick")}',
        f'execute if score #pat {OBJ} matches {REPLAY_PAT} run return run {fn("core/replay/tick")}',
        f'execute if score #pat {OBJ} matches 1..49 run return run {fn("core/pat_tick")}',
        f'execute if score #lock {OBJ} matches 1 run return 0',
        fn('ai/recover')]
    w('core/fight', fight)
    # patterns: start / run / end / cancel
    pt = ['# The running pattern (@s = body): #pt + 1, the core wrapper core/run/<key> (break window + p/<key>/tick).',
          f'scoreboard players add #pt {OBJ} 1']
    for k in present:
        pt.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"core/run/{k}")}')
    pt.append(f'execute if score #done {OBJ} matches 1 run {fn("core/pat_end")}')
    w('core/pat_tick', pt)
    for k in present:
        tid = S.TID[k]
        g = group_of(k)
        run = [f'# {k.upper()} one tick (@s = body).']
        if k in api.BREAK_WINDOWS:
            t0, t1 = api.BREAK_WINDOWS[k]
            run += [f'execute if score #pt {OBJ} matches {t0} run {fn("core/win_on")}',
                    f'execute if score #pt {OBJ} matches {t1 + 1} run {fn("core/win_off")}']
        run.append(fn(f'p/{k}/tick'))
        w(f'core/run/{k}', run)
        lines = api.LINE_OF.get(k, ())
        start = [f'# Start {k.upper()} {api.PATTERN_NAMES[k]} (@s = body; the AI, the rules, tests): cooldown, counters, the dialog line.',
                 fn('core/stop_move'), sset('#pat', tid), sset('#pt', 0), sset('#done', 0),
                 f'scoreboard players operation #last2 {OBJ} = #last {OBJ}', sset('#last', AI.GROUP_ID[g])]
        if g in api.COOLDOWN:
            start += [f'scoreboard players operation #cd_{g} {OBJ} = #clk {OBJ}', f'scoreboard players add #cd_{g} {OBJ} {api.COOLDOWN[g]}']
        if g != 'F':
            start.append(f'scoreboard players add #ai_nf {OBJ} 1')
        if g != 'Q5':
            start.append(f'scoreboard players add #ai_nq {OBJ} 1')
        if g == 'Q5':
            start.append(sset('#ai_q5', tid))
        if lines:
            say = [f'# The dialog line of {k.upper()} (@s = body): one of api.LINE_OF (random), #lines = when.',
                   f'scoreboard players operation #lines {OBJ} = #clk {OBJ}']
            if len(lines) == 1:
                say.append(S.line_say(lines[0]))
            else:
                say.append(f'execute store result score #t {OBJ} run random value 0..{len(lines) - 1}')
                say += [S.gate(f'if score #t {OBJ} matches {i}', S.line_say(lid)) for i, lid in enumerate(lines)]
            w(f'core/line/{k}', say)
            if k in LINE_ALWAYS:
                start.append(fn(f'core/line/{k}'))
            else:
                # at each cast, unless another line started less than LINE_GAP t ago (no overlapping subtitles)
                start += [f'scoreboard players operation #t {OBJ} = #clk {OBJ}', f'scoreboard players operation #t {OBJ} -= #lines {OBJ}',
                          f'execute if score #t {OBJ} matches {LINE_GAP}.. run {fn(f"core/line/{k}")}']
        start += [fn('hud/sub'), fn(f'p/{k}/start')]
        w(f'core/start/{k}', start)
        w(f'core/hz_tag/{k}', [f'# @s = a hazard of {k.upper()} just made: the pattern tags (its cancel kills it).',
                               f'tag @s add {api.TAGS["pat"]}', f'tag @s add {S.tag_p(k)}'])
    w('core/stop_move', ['# The body stops gliding (@s = body).', 'execute if entity @s[tag=rlk_mb_mv] run function rlk:mboss/mv/stop'])
    pend = ['# The pattern set #done (@s = body): the window closed, the looks back, the schedules, the recovery.',
            fn('core/win_off'), sset('#done', 0), f'scoreboard players operation #dec {OBJ} = #pat {OBJ}', sset('#pat', 0),
            'kill @e[type=minecraft:marker,tag=rlk_kn_lock]',
            sset('#pt', 0), fn('core/looks_rest'), fn('core/ground')]
    if 'e70' in present:
        pend.append(f'execute if score #dec {OBJ} matches {S.TID["e70"]} run {fn("core/e70_end")}')
    if 'f1' in present:
        pend.append(f'execute if score #dec {OBJ} matches {S.TID["f1"]} run {fn("ai/resched_f")}')
    for q in ('q5a', 'q5b'):
        if q in present:
            pend.append(f'execute if score #dec {OBJ} matches {S.TID[q]} run {fn("ai/resched_q5")}')
    if 'q0' in present:
        pend.append(f'execute if score #dec {OBJ} matches {S.TID["q0"]} run {fn("core/q0_end")}')
    pend += [fn('ai/rec_start'), fn('hud/sub')]
    w('core/pat_end', pend)
    if 'q0' in present:
        w('core/q0_end', ['# Q0 (the P2 opener) ran: it never runs again (#q0_ok 1), the Q5 schedule starts.', sset('#q0_ok', 1),
                          fn('ai/sched_q5')])
    cd = ['# Cancel the running pattern (any executor; idempotent): its own cancel (hazards, markers, props, glide, looks).']
    for k in present:
        cd.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"p/{k}/cancel")}')
    w('core/cancel_d', cd)
    w('core/cancel_pat', ['# Cancel the running pattern (reload, tests; @s = body): recovery follows; E70 is reserved again.',
                          f'execute if score #pat {OBJ} matches {S.TID["e70"]} run {fn("core/e70_reload")}',
                          fn('core/cancel_d'), fn('core/win_off'), sset('#pat', 0), sset('#done', 0),
                          fn('core/stop_move'), fn('core/looks_rest'), fn('core/ground'), fn('ai/rec_start'), fn('hud/sub')])
    # break windows
    banner_on, banner_off = S.hud('banner', on=1), S.hud('banner', on=0)
    w('core/win_on', ['# A break window opens (#pt = its start; @s = body): the body tag the shock resolve reads, the real-game',
                      '# banner (the one allowed instruction text: the game\'s own, adapted to the normal attack).',
                      f'tag @s add {api.TAGS["win"]}', sset('#win', 1)] + banner_on)
    w('core/win_off', ['# The break window closes (its end, a cancel, the break; @s any).',
                       f'execute unless score #win {OBJ} matches 1 run return 0',
                       f'tag @e[tag={api.TAGS["win"]}] remove {api.TAGS["win"]}', sset('#win', 0)] + banner_off)
    # movement helpers
    w('core/lockp', ['# The lock marker rlk_kn_lock (pattern-tagged by its owner\'s cancel through rlk_kn_p) at the player\'s feet on',
                     '# the floor, pulled toward the arena centre until mv/ok passes (inside the safe disc, free feet and head).',
                     f'kill @e[type=minecraft:marker,tag=rlk_kn_lock]',
                     f'execute at {S.PLAYER} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ '
                     f'{{Tags:["rlk_room","rlk_mb_aux","{api.TAGS["pat"]}","rlk_kn_lock"]}}',
                     sset('#t4', 0),
                     f'execute as {S.LOCK_M} at @s run {fn("core/clamp")}'])
    w('core/lock_short', ['# The dive target (C / E; @s = body): the lock moved 1.5 b toward her (when it stays farther than 2.5 b from',
                          '# her and passes mv/ok), so she lands in front of the player, not on them; the impact is centred there.',
                          f'execute as {S.LOCK_M} at @s unless entity @e[type=minecraft:husk,tag=rlk_mb_body,distance=..2.5] '
                          f'facing entity {S.BODY} feet rotated ~ 0 positioned ^ ^ ^1.5 if function rlk:mboss/mv/ok run tp @s ~ ~ ~'])
    w('core/clamp', ['# @s = a marker on the floor: 0.5 b toward the arena centre until mv/ok passes there (at most 60 steps).',
                     'execute if function rlk:mboss/mv/ok run return 0',
                     f'scoreboard players add #t4 {OBJ} 1', f'execute if score #t4 {OBJ} matches 60.. run return 0',
                     f'execute facing entity {S.ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                     f'execute at @s run {fn("core/clamp")}'])
    w('core/air/drift', ['# Airborne drift (@s = body, at the leap apex): 0.35 b / t toward the player (horizontal) while farther than',
                         '# 1.5 b; the floor spot below the new point must pass mv/ok.',
                         f'execute at @s positioned ~ {CY} ~ if entity {S.PLAYER[:-1]},distance=..1.5] run return 0',
                         f'execute at @s facing entity {S.PLAYER} feet rotated ~ 0 positioned ^ ^ ^0.35 positioned ~ {CY} ~ if '
                         f'function rlk:mboss/mv/ok at @s facing entity {S.PLAYER} feet rotated ~ 0 positioned ^ ^ ^0.35 run tp @s ~ ~ ~'])
    w('core/ground', ['# Back on the floor at once if airborne (a cancelled leap / hover; @s = body): the spot below when mv/ok, else',
                      '# the arena centre.',
                      fn('core/stop_move'),
                      f'execute store result score #t {OBJ} run data get entity @s Pos[1] 100',
                      f'execute if score #t {OBJ} matches ..{CY * 100 + 4} run return 0',
                      f'execute at @s positioned ~ {CY} ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~',
                      f'execute positioned as {S.ARENA_M} positioned ~ {CY} ~ run tp @s ~ ~ ~'])
    w('core/dash/probe', [
        '# Dash probe (@s = body, rotated as it): a marker rlk_kn_dp walks forward in 0.5 b steps while the next spot passes',
        '# mv/ok (inside the arena safe disc - 0.5 b, feet and head free), at most #t kn steps; #t2 kn = steps taken.',
        'kill @e[type=minecraft:marker,tag=rlk_kn_dp]',
        f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ '
        f'{{Tags:["rlk_room","rlk_mb_aux","{api.TAGS["pat"]}","rlk_kn_dp"]}}',
        'execute at @s rotated as @s rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run tp @s ~ ~ ~ ~ 0',
        sset('#t2', 0),
        f'execute as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] at @s run {fn("core/dash/step")}'])
    w('core/dash/step', [
        '# One probe step (@s = the probe marker, at / rotated as it).',
        f'execute if score #t2 {OBJ} >= #t {OBJ} run return 0',
        'execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0',
        'tp @s ^ ^ ^0.5',
        f'scoreboard players add #t2 {OBJ} 1',
        f'execute at @s run {fn("core/dash/step")}'])
    w('core/dash/grow', ['# @s = a dash line hazard: its length follows the body (#hzSzR mb set by the pattern).',
                         'scoreboard players set #hzSzR0 mb 0', 'scoreboard players set #hzSzW mb 0',
                         'function rlk:mboss/hz/resize_s'])
    # ---------------------------------------------------------------------------------------------- E70
    if 'e70' in present:
        w('core/e70_go', ['# The 70 % floor was reached: E70 재가 된 만상 now (@s = body; invulnerable until its brand tick).',
                          sset('#fl', 0), sset('#e70', 1), sset('#ph', PH['e70']), 'tag @s add rlk_mb_inv',
                          fn('core/start/e70')])
        w('core/e70_brand', ['# E70 brand tick (the forced bond is the pattern\'s; @s = body): hittable again, the floor moves to 1.',
                             'tag @s remove rlk_mb_inv', 'scoreboard players set #mbFloor mb 1', sset('#e70', 2)])
        w('core/e70_end', ['# E70 is over (@s = body): P1b with the <= 70 % kit, the F schedule starts.',
                           'tag @s remove rlk_mb_inv', 'scoreboard players set #mbFloor mb 1', sset('#e70', 2),
                           sset('#ph', PH['p1b']), fn('ai/phase'), fn('ai/sched_f')])
        w('core/e70_reload', ['# E70 interrupted (reload / tests; @s = body): before its brand it is reserved again (P1a, the 70 %',
                              '# floor kept); after it the event counts as done (P1b).',
                              f'execute if score #e70 {OBJ} matches 2 run return run {fn("core/e70_end")}',
                              'tag @s remove rlk_mb_inv', sset('#e70', 0), sset('#fl', 1), sset('#ph', PH['p1a'])])
    # ---------------------------------------------------------------------------------------------- T (P1 -> P2)
    w('core/tr/start', [
        '# T: the P1 floor was reached (@s = body): the running pattern is cancelled, invulnerable + cine (player damage',
        f'# refused) throughout; the transition sequence (seq/t_p2 or the stand-in, {T_LEN} t); repool + music at {T_TITLE}.',
        fn('core/cancel_d'), fn('core/win_off'), f'kill @e[tag={api.TAGS["pat"]}]', sset('#fl', 0), sset('#ph', PH['t']),
        sset('#pat', TR_PAT), sset('#pt', 0), sset('#sq', 0), sset('#sqdone', 0), sset('#trt', 0), 'tag @s add rlk_mb_inv',
        L.cine(True), fn('core/stop_move'), fn('core/ground'), fn('core/looks_rest'),
        seq_or_stand(ctx, 't_p2', 'start'), fn('hud/sub')])
    w('core/tr/tick', [
        f'# T tick (#pat {TR_PAT}): the sequence on #sq; at {T_TITLE} the P2 pool (repool {api.PHASES[1]}) and music phase 2.',
        f'scoreboard players add #sq {OBJ} 1',
        seq_or_stand(ctx, 't_p2', 'tick'),
        f'execute if score #sq {OBJ} matches {T_TITLE} run {fn("core/tr/title")}',
        f'execute if score #sqdone {OBJ} matches 1 run return run {fn("core/tr/end")}',
        f'execute if score #sq {OBJ} matches {T_LEN + 40}.. run {fn("core/tr/end")}'])
    w('core/tr/title', ['# T title tick (or a T finished early): the P2 pool, music 2 (the title / dialog are the sequence\'s).',
                        sset('#trt', 1), L.repool(api.PHASES[1]), L.music(2)])
    w('core/tr/end', [
        '# T is over (or a reload / test finishes it; @s = body): P2, no floor; Q0 first (the decision picks it).',
        f'execute if score #trt {OBJ} matches 0 run {L.title(*api.TITLE_P2, api.TITLE_COLOR[2])}',
        f'execute if score #trt {OBJ} matches 0 run {fn("core/tr/title")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} run {seq_or_stand(ctx, "t_p2", "cancel")}',
        'tag @s remove rlk_mb_inv', L.cine(False), 'scoreboard players set #mbFloor mb 0',
        sset('#ph', PH['p2']), sset('#pat', 0), sset('#sq', 0), sset('#sqdone', 0), sset('#q0_ok', 0),
        fn('ai/phase'), fn('core/looks')]
      + ([] if 'q0' in present else [fn('core/ground'), fn('ai/sched_q5')])
      + [fn('ai/rec_start'), sset('#rec', 2), fn('hud/sub')])
    # ---------------------------------------------------------------------------------------------- break / stun
    w('core/break', [
        '# 선혈의 충격 inside a break window (bond/shock, test 24; @s = body): the Banquet is cancelled (hazards, decals,',
        f'# props, banner), true damage of the pool (P1 {api.BREAK_PM[1]} / P2 {api.BREAK_PM[2]} per mille, clamped above the',
        f'# floor), the stagger clip brk ({BRK_LEN} t) then the stun clip for {api.STUN_T} t (AI paused, no damage multiplier).',
        f'scoreboard players operation #brk {OBJ} = #pat {OBJ}',
        fn('core/cancel_d'), fn('core/win_off'), sset('#pat', 0), sset('#done', 0),
        sset('#t3', api.BREAK_PM[1]),
        f'execute if score #ph {OBJ} matches {PH["p2"]} run {sset("#t3", api.BREAK_PM[2])}',
        fn('bond/true'),
        f'execute unless score #mbSt mb matches 1 run return 0']
      + S.fx('break_burst', [S.part(S.DUST[2], 1.0, 1.2, 1.0, 0, 60), S.part('minecraft:explosion', 0.4, 0.4, 0.4, 0, 2)],
             pos=f'at @s positioned ~ ~{S.H(1.4)} ~')
      + S.placed(S.snd('break'), 'at @s')
      + [fn('core/stun_start')])
    w('core/stun_start', [f'# The stun (@s = body): brk then stun / stun2 ({api.STUN_T} t), hittable, the under-bar counts down.',
                          fn('core/stop_move'), fn('core/ground'), fn('core/looks_rest'),
                          sset('#pat', STUN_PAT), sset('#pt', 0), sset('#stun', 1), sset('#stun_t', api.STUN_T + BRK_LEN),
                          f'tag @s add {api.TAGS["stun"]}', api.play('brk'), fn('hud/sub')])
    w('core/stun_tick', [
        f'# Stun tick (#pat {STUN_PAT}, @s = body): the stun clip after the stagger, motes, the countdown.',
        f'scoreboard players add #pt {OBJ} 1',
        f'scoreboard players remove #stun_t {OBJ} 1',
        f'execute if score #pt {OBJ} matches {BRK_LEN} run {fn("core/stun_clip")}',
        f'execute if score #pt {OBJ} matches {BRK_LEN}.. if score #stun_t {OBJ} matches 1.. run {fn("core/stun_fx")}',
        f'execute if score #stun_t {OBJ} matches ..0 run {fn("core/stun_end")}'])
    w('core/stun_clip', ['# The stun clip of the form (@s = body).',
                         f'execute if score #ph {OBJ} matches {PH["p2"]} run return run {api.play("stun2")}', api.play('stun')]
      + S.placed(S.snd('stun'), 'at @s'))
    w('core/stun_fx', [f'scoreboard players operation #t {OBJ} = #stun_t {OBJ}', f'scoreboard players operation #t {OBJ} %= #c10 {OBJ}',
                       f'execute if score #t {OBJ} matches 0 run {S.fx("stun_motes", [S.part("minecraft:crit", 0.4, 0.2, 0.4, 0.1, 6)], pos=f"at @s positioned ~ ~{S.H(2.9)} ~")[0]}'])
    sch = []
    if 'f1' in present:
        sch.append(f'execute if score #brk {OBJ} matches {S.TID["f1"]} run {fn("ai/resched_f")}')
    for q in ('q5a', 'q5b'):
        if q in present:
            sch.append(f'execute if score #brk {OBJ} matches {S.TID[q]} run {fn("ai/resched_q5")}')
    w('core/stun_end', ['# The stun is over (@s = body): the Banquet schedule restarts from here, the recovery.',
                        f'tag @s remove {api.TAGS["stun"]}', sset('#stun', 0), sset('#stun_t', 0), sset('#pat', 0), sset('#pt', 0)]
      + sch + [sset('#brk', 0), fn('ai/rec_start'), fn('hud/sub')])
    # ---------------------------------------------------------------------------------------------- intro replay (test 25)
    w('core/replay/start', ['# Test 25: the intro again (@s = body, invulnerable), then the fight goes on.',
                            sset('#pat', REPLAY_PAT), sset('#sq', 0), sset('#sqdone', 0), 'tag @s add rlk_mb_inv',
                            api.rig('look/weapon_r/gone'), api.rig('look/props/tea'), seq_or_stand(ctx, 'intro', 'start')])
    w('core/replay/tick', [f'scoreboard players add #sq {OBJ} 1', seq_or_stand(ctx, 'intro', 'tick'),
                           f'execute if score #sqdone {OBJ} matches 1 run return run {fn("core/replay/end")}',
                           f'execute if score #sq {OBJ} matches {INTRO_LEN + 2}.. run {fn("core/replay/end")}'])
    w('core/replay/end', [seq_or_stand(ctx, 'intro', 'cancel'), 'tag @s remove rlk_mb_inv', sset('#pat', 0), sset('#sq', 0),
                          sset('#sqdone', 0), fn('core/looks'), fn('ai/rec_start')])
    wisps(W)
    stand_ins(W, ctx)
    hooks(W, ctx)
    hud_files(W, ctx)
    gate_files(W)
    tests(W, ctx)
    if not api.rig_real():
        rig_stub(W)


def wisps(W):
    """core/wisps: the three white flame-spirits at their rim posts (api.WISP_POSTS; two red in P2), as kit props tagged
    rlk_kn_wisp. The intro sequence brings them there (S2); the core puts them back after a /reload (aux entities are gone)
    or a skipped intro / T (tests). Without the kit there is no wisp look (nothing is summoned)."""
    lines = ['# The three wisps over their rim posts (@s any; idempotent): white, wisps 1 and 2 red from P2 on (PLAN §8.4; the',
             '# same two seq/t_p2 turns red).']
    theme = L.theme_module(api.ARENA_SPEC['theme'])
    pts = getattr(theme, 'POINTS', {}).get('wisps') if theme else None
    if K.prop('wisp', c=1):
        lines.append('kill @e[type=minecraft:item_display,tag=rlk_kn_wisp]')
        for i, (bearing, r) in enumerate(api.WISP_POSTS):
            red = i in (1, 2)
            # over the post (theme POINTS, absolute: the post itself is solid y 201-203); else the bearing at r, 1 b up
            at = (f'positioned {L.num(pts[i][0])} {L.num(pts[i][1])} {L.num(pts[i][2])}' if pts else
                  f'at {S.ARENA_M} rotated {L.num(180 + bearing)} 0 positioned ^ ^ ^{L.num(r)} positioned ~ {CY + 1} ~')
            lines.append(f'execute {at} '
                         f'run summon minecraft:item_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp{i}"]}}')
            for c, cond in ((1, f'unless score #ph {OBJ} matches {PH["p2"]}' if red else ''), (2, f'if score #ph {OBJ} matches {PH["p2"]}')):
                if c == 2 and not red:
                    continue
                cmd = f'execute as @e[type=minecraft:item_display,tag=rlk_kn_wisp{i}] run {K.prop("wisp", c=c)}'
                lines.append(S.gate(cond, cmd) if cond else cmd)
    W.w('core/wisps', lines)


def stand_ins(W, ctx):
    """core/sq/<name>/{start,tick,cancel} for every sequence S2's seq.SERVICES does not provide yet: the clip, its length,
    the titles / dialog / push ring at their events and the few looks the fight needs."""
    w = W.w
    spec = {
        'intro': ('intro', {api.ev('intro', 'embers'): [api.rig('look/props/none')],
                            api.ev('intro', 'form'): [api.rig('look/weapon_r/hand')],
                            api.ev('intro', 'title'): [L.title(*api.TITLE_P1, api.TITLE_COLOR[1]), S.line_say(1)],
                            api.ev('intro', 'push'): [f'execute at @s run {L.push_ring(4.0, 4)}']}),
        't_p2': ('t_p2', {api.ev('t_p2', 'kneel'): [api.rig('look/glow/crimson')],
                          api.ev('t_p2', 'dark'): [x for x in (api.arena_look('crimson'),
                                                               'effect give @a[tag=player] minecraft:blindness 1 0 true') if x],
                          api.ev('t_p2', 'swap'): [api.rig('look/form/p2'), api.rig('look/weapon_l/hand')],
                          api.ev('t_p2', 'title'): [L.title(*api.TITLE_P2, api.TITLE_COLOR[2]), S.line_say(11),
                                                    api.rig('look/glow/normal')]}),
        'death': ('death', {api.ev('death', 'fade'): [api.rig('look/weapon_r/gone'), api.rig('look/weapon_l/gone')],
                            api.ev('death', 'gone'): [api.rig('state/hidden')]}),
    }
    for name in api.SEQS:
        if name in ctx.services:
            continue
        clip, evs = spec[name]
        ln = api.CLIPS[clip][0]
        w(f'core/sq/{name}/start', [f'# Stand-in sequence {name} (S2 seq.py has none yet): the clip {clip} ({ln} t), sq 0.',
                                    S.sset('#sqdone', 0), api.play(clip)])
        tick = [f'# Stand-in {name} tick (#sq kn 1..{ln}).']
        for t in sorted(evs):
            for c in evs[t]:
                tick.append(S.gate(f'if score #sq {OBJ} matches {t}', c))
        tick.append(f'execute if score #sq {OBJ} matches {ln}.. run {S.sset("#sqdone", 1)}')
        w(f'core/sq/{name}/tick', tick)
        w(f'core/sq/{name}/cancel', [f'# Stand-in {name} cancel: nothing of its own lingers.'])


def hooks(W, ctx):
    w = W.w
    present = ctx.present
    w('on_hit', [
        '# Hook on_hit (@s = body inside combat/apply, before apply_mods; scores only, no recursion): a normal-attack hit',
        '# (기본 공격: #icd 1, not a skill, not a reaction, not an item proc, not true damage; contract §3.5) while 선혈의 충격',
        '# is armed is recorded; the next fight tick resolves it (bond/shock: the break inside a window, else the burst).',
        f'execute if score #shock {OBJ} matches 1 {api.NORMAL_HIT_IF} run {sset("#shk_hit", 1)}'])
    w('aux_hit', ['# Hook aux_hit: 아를레키노 has no aux objects (framework default).'])
    w('incoming', ['# Hook incoming (@s = body inside combat/apply_mods; the framework floor runs after it). No damage multipliers:',
                   '# the user removed her ranged immunity and her Pyro resistance (res {"*":10} like every element), the stun has',
                   '# no damage-taken bonus (PLAN §4.2-4.3).'])
    pause = ['# Hook pause (the fight froze): the kit cards go (the banner, decals and prop looks come back on resume).']
    pause += [x for x in (K.fixed('clear'),) if x]
    resume = ['# Hook resume (@s = body): the pattern\'s redraw (decals with the ticks left, prop looks), the banner inside a',
              '# break window, the badge (hud/sub).']
    for k in present:
        if ctx.has_file(k, 'pause', W):
            pause.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"p/{k}/pause")}')
        if ctx.has_file(k, 'resume', W):
            resume.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"p/{k}/resume")}')
    resume += [S.gate(f'if score #win {OBJ} matches 1', x) for x in S.hud('banner', on=1)] + [fn('hud/sub')]
    w('pause', pause)
    w('resume', resume)
    w('core/stop_all', [
        '# Everything of the fight state stops (death, cleanup; any executor): the pattern, a transition / replay, the stun.',
        fn('core/cancel_d'),
        f'execute if score #pat {OBJ} matches {TR_PAT} run {seq_or_stand(ctx, "t_p2", "cancel")}',
        f'execute if score #pat {OBJ} matches {REPLAY_PAT} run {seq_or_stand(ctx, "intro", "cancel")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} run {L.cine(False)}',
        fn('core/win_off'),
        f'kill @e[tag={api.TAGS["pat"]}]',
        f'tag @e[tag={api.TAGS["stun"]}] remove {api.TAGS["stun"]}',
        sset('#pat', 0), sset('#stun', 0), sset('#stun_t', 0), sset('#done', 0)])
    w('death_start', [
        '# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, stopped the music): every state',
        '# stops, the kit cards go, her bond is taken back, the death sequence (seq/death or the stand-in) on #sq.',
        fn('core/stop_all')] + [x for x in (K.fixed('clear'),) if x] + [
        fn('bond/cleanup'), 'scoreboard players set #mbFloor mb 0', sset('#ph', PH['death']), sset('#sq', 0),
        sset('#sqdone', 0), fn('core/stop_move'), fn('core/ground'), seq_or_stand(ctx, 'death', 'start')])
    w('death_tick', ['# Hook death_tick (@s = body, #mbT 1.. until cur.death).', f'scoreboard players add #sq {OBJ} 1',
                     seq_or_stand(ctx, 'death', 'tick'), api.rig('tick')])
    cl = ['# Hook cleanup (no executor; idempotent; won / cancel / defeat): every state, hazard and marker of the module, her',
          '# bond taken back (min(bol, #given)), the kit cards and HUD, the rig, the module scores (init makes them again),',
          '# storage core.*.',
          fn('core/stop_all')]
    for s in sorted(ctx.services):
        cl.append(fn(f'seq/{s}/cancel'))
    cl += [fn('bond/cleanup'), K.fixed('clear'), *S.hud('clear'), at_body(api.rig('kill')),
           f'kill @e[tag={api.TAGS["part"]}]', f'kill @e[tag={api.TAGS["prop"]}]', f'kill @e[tag={api.TAGS["pat"]}]',
           f'kill @e[type=minecraft:item,tag={api.TAGS["orb"]}]', 'kill @e[tag=rlk_kn_wisp]',
           # the kit's followers of the wisp / moon markers (fx/clear keeps them for a pause; the fight is over here)
           'kill @e[type=minecraft:item_display,tag=rlk_kn_fxf]', 'scoreboard players set #mbBolRe mb 100',
           f'scoreboard players reset * {OBJ}', f'data remove storage {api.STORAGE} core', f'data remove storage {api.STORAGE} p2']
    w('cleanup', [x for x in cl if x])
    un = ['# Hook uninstall (no executor; every enabled module): the kit, the rig, the module entities, the gate flames chain,',
          '# objective kn, storage core.*.']
    un += [K.fixed('uninstall'), api.rig('uninstall'), f'kill @e[tag={api.TAGS["pat"]}]', f'kill @e[tag={api.TAGS["part"]}]',
           f'kill @e[tag={api.TAGS["prop"]}]', f'kill @e[tag={api.TAGS["fx"]}]', f'kill @e[tag={api.TAGS["anchor"]}]',
           f'kill @e[type=minecraft:item,tag={api.TAGS["orb"]}]', 'kill @e[tag=rlk_kn_grave]', 'kill @e[tag=rlk_kn_wisp]',
           f'schedule clear {NS}gate/flames', f'scoreboard objectives remove {OBJ}', f'data remove storage {api.STORAGE} core',
           f'data remove storage {api.STORAGE} p2']
    w('uninstall', [x for x in un if x])
    w('reload', [
        '# Hook reload (@s = body after /reload: the rig parts, hazards, markers, orbs and kit cards are gone; scores are kept).',
        '# intro -> its end; a pattern -> cancelled + recovery (E70 before its brand: reserved again); T -> finished; the',
        '# intro replay -> ended; a stun -> the rest of it (the clip again).',
        fn('init'), api.rig('init'), api.rig('spawn'), sset('#lock', 0),
        f'execute if score #ph {OBJ} matches {PH["intro"]} run return run {fn("core/intro/reload")}',
        f'execute if score #ph {OBJ} matches {PH["death"]} run return 0',
        f'execute if score #pat {OBJ} matches 1..49 run {fn("core/cancel_pat")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} run {fn("core/tr/end")}',
        f'execute if score #pat {OBJ} matches {REPLAY_PAT} run {fn("core/replay/end")}',
        fn('core/looks'), fn('core/wisps'),
        f'execute if score #stun {OBJ} matches 1 run {fn("core/stun_clip")}',
        fn('hud/sub'),
        f'execute if score #pat {OBJ} matches 0 run {fn("ai/rec_start")}'])
    w('bars', ['# Hook bars (@s = body, every tick in intro / fight): the under-bar = the stun countdown.',
               f'execute if score #stun {OBJ} matches 1 run {fn("hud/bar_stun")}'])
    w('hz_vis', ['# Hook hz_vis: her hazards are quiet (#hzQuiet 1; the floor markings of PLAN §1.5 are the kit decals).'])
    pj = ['# Hook pj_end (@s = a projectile prop, #pjEv; #pjKeep preset): the pattern that launched it, if it has a pj_end.']
    for k in present:
        if ctx.has_file(k, 'pj_end', W):
            pj.append(f'execute if entity @s[tag={S.tag_p(k)}] run return run {fn(f"p/{k}/pj_end")}')
    w('pj_end', pj)


def hud_files(W, ctx):
    w = W.w
    present = ctx.present
    sub = ['# The boss-bar third line (@s any; on every state change): the phase sub (우인단 집행관 서열 4위 / 페르엘) or the',
           '# running pattern name, then the badge ◆선혈의 충격 while armed (names / the badge only; PLAN §4.6).',
           f'data modify storage rlk:mboss sub set value [{{text:"{api.TITLE_P1[1]}",color:"{SUB_HEX}",bold:false}}]',
           f'execute if score #ph {OBJ} matches {PH["p2"]}.. run data modify storage rlk:mboss sub set value '
           f'[{{text:"{api.TITLE_P2[1]}",color:"{SUB_HEX}",bold:false}}]']
    for k in present:
        sub.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run data modify storage rlk:mboss sub set value '
                   f'[{{text:"{api.PATTERN_NAMES[k]}",color:"{SUB_HEX}",bold:true}}]')
    badge_on, badge_off = S.hud('badge', on=1), S.hud('badge', on=0)
    if badge_on:
        sub += [S.gate(f'if score #shock {OBJ} matches 1', x) for x in badge_on]
        sub += [S.gate(f'unless score #shock {OBJ} matches 1', x) for x in badge_off]
    else:
        sub.append(f'execute if score #shock {OBJ} matches 1 run data modify storage rlk:mboss sub append value '
                   f'{{text:"  {api.BADGE}",color:"{BADGE_HEX}",bold:true}}')
    w('hud/sub', sub)
    w('hud/bar_stun', [f'scoreboard players operation #buSub bu = #stun_t {OBJ}',
                       f'scoreboard players set #buSubMax bu {api.STUN_T + BRK_LEN}', 'scoreboard players set #buSubCol bu 2'])


def gate_files(W):
    """prep (the gate texts, title / sub of the gate press) and the gravestone flames chain."""
    w = W.w
    theme = L.theme_module(api.ARENA_SPEC['theme'])
    grave = tuple(getattr(theme, 'GRAVE', (0.0, 1.4, 3.0))) if theme else (0.0, 1.4, 3.0)
    l1, l2, l3 = api.GATE_LINES
    w('prep', [
        '# Hook prep (@s = the kind-9 entrance zone marker, at it; cb/pp/arlecchino cleared cprep.arlecchino first): the gate',
        '# texts, the title / sub of the gate press, the crimson flames on the gravestone (the theme\'s GRAVE offset; a',
        '# self-rescheduling chain that stops when the anchor is gone; uninstall clears the schedule).',
        f'data modify storage rlk:mboss cprep.{api.ID}.gate set value {{item:"{api.BOSS["icon"]["item"]}",'
        f'model:"{api.BOSS["icon"]["model"]}",item2:"minecraft:red_candle",model2:"minecraft:red_candle",'
        f'l1:{{text:"{l1}",color:"#D0D0D0",bold:false}},l2:{{text:"{l2}",color:"{api.COLOR}",bold:true}},'
        f'l3:{{text:"{l3}",color:"#A8A8A8",bold:false}},n:{api.N}}}',
        f'data modify storage rlk:mboss cprep.{api.ID}.title set value {{text:"{api.TITLE_P1[0]}",color:"{api.COLOR}",bold:true}}',
        f'data modify storage rlk:mboss cprep.{api.ID}.sub set value {{text:"{api.TITLE_P1[1]}",color:"{SUB_HEX}",bold:false}}',
        'kill @e[type=minecraft:marker,tag=rlk_kn_grave]',
        f'summon minecraft:marker ~{L.num(grave[0])} ~{L.num(grave[1])} ~{L.num(grave[2])} {{Tags:["rlk_room","rlk_kn_grave"]}}',
        f'schedule function {NS}gate/flames 10t replace'])
    w('gate/flames', [
        '# Every 10 t while the gravestone anchor exists (room/clear kills it; uninstall clears the schedule): crimson flames.',
        'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1] run return 0',
        *S.fx('gate_flames', ['particle minecraft:crimson_spore ~ ~0.3 ~ 0.25 0.3 0.25 0 6',
                              'particle minecraft:flame ~ ~0.2 ~ 0.15 0.2 0.15 0.01 3',
                              'particle minecraft:dust{color:[0.75,0.05,0.12],scale:1.2} ~ ~0.4 ~ 0.2 0.35 0.2 0 4'],
              pos='at @e[type=minecraft:marker,tag=rlk_kn_grave,limit=1]'),
        f'schedule function {NS}gate/flames 10t replace'])


def tests(W, ctx):
    w = W.w
    present = ctx.present
    w('test', ['# Hook test {id:N} (as the player, /function rlk:boss/test/pattern {id:N}); the list: test/help.',
               f'$scoreboard players set #tst {OBJ} $(id)',
               at_body(fn('test/run'))])
    run = ['# @s = body: the test #tst (api.TEST_IDS).']
    for k in present:
        if k == 'e70':
            continue
        run.append(f'execute if score #tst {OBJ} matches {S.TID[k]} run return run {fn(f"test/go/{k}")}')
        need_p2 = ([f'execute if score #ph {OBJ} matches ..{PH["t"]} run {fn("test/ph2")}'] if k in P2_KEYS else [])
        flag = [sset('#q4_t3', 1)] if k == 'q4' else []           # test 45 = q4 with 3 shots (p/q4/start consumes it)
        w(f'test/go/{k}', [f'execute unless function {NS}core/force run return 0'] + need_p2 + flag + [fn(f'core/start/{k}')])
    for tid, rel in ((20, 'test/e70'), (21, 'bond/force'), (22, 'test/heal'), (23, 'test/shock'), (24, 'test/brk'),
                     (25, 'test/intro'), (26, 'test/tr'), (27, 'test/death'), (28, 'bond/orbs'), (29, 'test/stun'),
                     (30, 'test/ph1b'), (31, 'test/ph2'), (80, 'test/floor'), (99, 'test/hold')):
        run.append(f'execute if score #tst {OBJ} matches {tid} run return run {fn(rel)}')
    w('test/run', run)
    w('core/force', [
        '# Tests: make the fight state ready for a forced action (@s = body). Fails during a transition / replay.',
        f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
        f'execute if score #pat {OBJ} matches {TR_PAT}.. run return fail',
        f'execute if score #pat {OBJ} matches 1..49 run {fn("core/cancel_pat")}',
        f'execute if score #stun {OBJ} matches 1 run {fn("core/stun_end")}',
        'return 1'])
    w('test/e70', ['# Test 20: E70 now (from P1a: the floor counts as reached; later: the event again).',
                   f'execute unless function {NS}core/force run return 0', sset('#e70', 0)]
      + ([fn('core/e70_go')] if 'e70' in present else []))
    w('test/heal', ['# Test 22: heal the player 30 % of max HP (the existing player/heal: it clears the bond first).',
                    'execute as @a[tag=player,limit=1] run scoreboard players operation #heal tmp = @s maxHealth',
                    f'scoreboard players operation #heal tmp /= #c100 {OBJ}', f'scoreboard players set #t {OBJ} 30',
                    f'scoreboard players operation #heal tmp *= #t {OBJ}',
                    'execute as @a[tag=player,limit=1] run function rlk:player/heal'])
    w('test/shock', ['# Test 23: 선혈의 충격 armed now.', sset('#shock', 1), fn('hud/sub')])
    w('test/brk', ['# Test 24: the break now (as a counter inside a window: cancel, true damage, stun).',
                   f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                   f'execute if score #pat {OBJ} matches {TR_PAT}.. run return 0', fn('core/break')])
    w('test/intro', ['# Test 25: the intro again (invulnerable).', f'execute unless function {NS}core/force run return 0',
                     fn('core/replay/start')])
    w('test/tr', ['# Test 26: the transition T now (then P2).', f'execute unless function {NS}core/force run return 0',
                  'scoreboard players set #mbFloor mb 1', sset('#e70', 2), fn('core/tr/start')])
    w('test/death', ['# Test 27: the death (true damage of her whole HP).', f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                     f'scoreboard players set #mbTrueEl mb {api.PYRO}', 'function rlk:mboss/true_pct {pct:100}'])
    w('test/stun', ['# Test 29: the stun now (no damage).', f'execute unless function {NS}core/force run return 0', fn('core/stun_start')])
    w('test/ph1b', ['# Test 30: straight to P1b (HP at most the 70 % floor, E70 counted as done, floor 1).',
                    f'execute unless function {NS}core/force run return 0', sset('#fl', 0), sset('#e70', 2),
                    f'execute if score @s mhpC > #fl70 {OBJ} run scoreboard players operation @s mhpC = #fl70 {OBJ}',
                    'scoreboard players set #mbFloor mb 1', sset('#ph', PH['p1b']), fn('ai/phase'), fn('ai/sched_f'),
                    fn('core/looks'), sset('#pat', 0), fn('ai/rec_start'), fn('hud/sub')])
    w('test/ph2', ['# Test 31: straight to P2 (T skipped: the P2 pool, title, music, the crimson look; Q0 first).',
                   f'execute unless function {NS}core/force run return 0', sset('#fl', 0), sset('#e70', 2),
                   sset('#pat', TR_PAT), sset('#trt', 0), fn('core/tr/end'), fn('core/wisps')]
      + [x for x in (api.arena_look('crimson'),) if x])
    w('test/floor', ['# Test 80: HP = the next floor + 1 (P1a: the 70 % floor, P1b: 1, P2: 0).',
                     f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                     f'execute if score #ph {OBJ} matches {PH["p1a"]} run scoreboard players operation @s mhpC = #fl70 {OBJ}',
                     f'execute if score #ph {OBJ} matches {PH["p1b"]} run scoreboard players set @s mhpC 1',
                     f'execute if score #ph {OBJ} matches {PH["p2"]} run scoreboard players set @s mhpC 0',
                     'scoreboard players add @s mhpC 1'])
    w('test/hold', ['# Test 99: hold / release the AI (a running pattern finishes).',
                    f'execute store success score #lock {OBJ} unless score #lock {OBJ} matches 1'])
    rows = [H.head('/function rlk:boss/test/pattern {id:…}', f'{api.NAME} 시험 번호')]
    for tid, name in api.TEST_HELP_NAMES.items():
        key = api.TEST_IDS[tid]
        if key in api.P1 + api.P2 and key not in present:
            continue
        rows.append(H.row(f'/function rlk:boss/test/pattern {{id:{tid}}}', tid, name))
    rows.append(H.note('lock {id:1~13, 41~48}: 그 패턴만 반복 · {id:0} 해제'))
    w('test/help', rows)


def rig_stub(W):
    """rig_stub/**: every rig call name of the contract while S2's manifest is missing. play/<clip> and start/<clip> set
    #rigc kn to the clip id (and #rigt kn to -1: the next tick shows tick 0); face/* turn the anchor; no visuals except a
    faint crimson column so the body can be found in game."""
    w = W.w
    for c in api.RIG_CALLS:
        if c == 'tick':
            w('rig_stub/tick', ['# Stand-in rig tick (@s = body): the shown clip tick #rigt kn; a faint column marks the body.',
                                f'scoreboard players add #rigt {OBJ} 1',
                                f'execute if score #rigt {OBJ} matches 0.. run particle minecraft:dust{{color:[0.88,0.19,0.23],scale:1.0}} '
                                '~ ~1.4 ~ 0.14 0.6 0.14 0 2 force @a[tag=player]'])
        elif c == 'face/player':
            w('rig_stub/face/player', ['execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'])
        elif c == 'face/track':
            w('rig_stub/face/track', ['function rlk:mboss/mv/turn {max:4}'])
        else:
            w(f'rig_stub/{c}', [f'# Stand-in rig call {c} (S2 rig missing): no visuals.'])
    w('rig_stub/face/set', ['$tp @s ~ ~ ~ $(yaw) 0'])
    for clip in api.CLIPS:
        for kind in ('play', 'start'):
            w(f'rig_stub/{kind}/{clip}', [f'scoreboard players set #rigc {OBJ} {S.clip_id(clip)}',
                                          f'scoreboard players set #rigt {OBJ} -1'])
