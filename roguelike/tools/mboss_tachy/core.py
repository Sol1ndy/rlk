"""Core of the 타키 (Tachy) module (OWNER: S3; plan S:tk/PLAN.md §4.3, §5; contract S:tk/contract.md §3): the 17 hooks
+ test/help, init / uninstall, the phase machine intro -> P1 -> (floor 70 %) M1 -> T1 -> P2 -> (35 %) M2 -> T2 -> P3 ->
death, #mbFloor, the incoming multipliers (mantle 20 %, stun 150 %, G3 stagger 130 %), the HUD (sub line, badge, gauge),
music phases, pause / resume / reload / cleanup per phase, the kit wiring, the rig stand-in rig_stub/** (while S2's
manifest is missing) and the stand-in sequences core/sq/** (while S2's seq.SERVICES lacks one), the test commands.

Scores (objective tk): api.CORE_FP plus the S3 extras of S:tk/requests/s3.md (#clk, #cd_<key>, #ai_*, #t*, #c*, #fl70,
#fl35, #hud_*, #rigc / #rigt of the stand-in rig). #pat: 1..11 a pattern (its test id), 50 G1 swap, 51 mantle, 52 mantle
break + stun, 53 nova, 54 transition, 55 intro replay (test 26); #stag the G3 stagger.
"""
import help_lib as H

from . import api
from . import s3lib as S
from . import elem as E
from . import ai as AI

L, K = api.L, api.K
OBJ = api.OBJ
fn, sset = S.fn, S.sset
NS = api.NS
CY = api.CY
PH = api.PH
SWAP_PAT, MANTLE_PAT, BREAK_PAT, NOVA_PAT, TR_PAT, REPLAY_PAT = 50, 51, 52, 53, 54, 55
INTRO_LEN = api.CLIPS['intro'][0]
TITLE = {PH['p1']: '망토', PH['m1']: '과부하 외피', PH['t1']: '날개 전개', PH['p2']: '날개', PH['m2']: '과부하 외피',
         PH['t2']: '심연', PH['p3']: '심연'}
TITLE_HEX = {PH['p1']: '#F2C230', PH['m1']: '#FFD86B', PH['t1']: '#F2C230', PH['p2']: '#F2C230', PH['m2']: '#FFD86B',
             PH['t2']: '#E0365F', PH['p3']: '#E0365F'}
CONSTS = (2, 5, 10, 36, 60, 64, 100, 577, 1000)
FLOOR_PCT = dict(zip(('fl70', 'fl35'), api.FLOORS))
FORM_OF_PH = [('cape', (0, 2)), ('winged', (3, 5)), ('abyss', (6, 8))]


class Ctx:
    """What the build knows: the present patterns (melee + S4's), the S4 / S2 files written, the services."""

    def __init__(self, pats, w4, services):
        self.pats = {p.key: p for p in pats}
        self.present = sorted((k for k in self.pats if k != 'mantle'), key=lambda k: S.TID[k])
        self.w4 = w4
        self.services = {s.name: s for s in services}

    def has_s4(self, rel):
        return (api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve() in self.w4.out.written

    def has_pat_file(self, key, rel):
        if key in api.MELEE:
            return False
        return self.has_s4(f'p/{key}/{rel}')


def at_body(cmd):
    return f'execute as {S.BODY} at @s run {cmd}'


def seq_or_stand(ctx, name, part):
    """The S2 sequence call seq/<name>/<part>, or the core stand-in core/sq/<name>/<part>."""
    if name in ctx.services:
        return fn(f'seq/{name}/{part}')
    return fn(f'core/sq/{name}/{part}')


def build(W, ctx):
    w = W.w
    present = ctx.present
    # ---------------------------------------------------------------------------------------------- init / vars
    w('init', ['# The module objective + constants (spawn, reload; idempotent). Removed by uninstall.',
               f'scoreboard objectives add {OBJ} dummy']
      + [sset(f'#c{c}', c) for c in CONSTS] + [sset('#cn1', -1), sset('#cn1000', -1000)])
    vars_ = ['# Every module fake player to its fight-start value (spawn).']
    for k in ('#ph', '#pat', '#pt', '#done', '#swt', '#aut', '#sh', '#sht', '#shicd', '#core', '#stun', '#stag', '#last',
              '#last2', '#rear', '#far', '#dec', '#rec', '#sq', '#sqdone', '#fl', '#flnext', '#tst', '#lock', '#clk',
              '#ai_pht', '#ai_mv', '#ai_d2', '#hud_g', '#hud_c'):
        vars_.append(sset(k, 0))
    vars_ += [sset('#el', api.G1_START), sset('#taken', 100), sset('#kgap', 9), sset('#ai_fp', 1),
              sset('#ai_swl', api.G1_FORCE_SWAP[1]), sset('#ai_d2', 100000)]
    vars_ += [sset(f'#cd_{k}', 0) for k in present]
    w('core/vars', vars_)
    # ---------------------------------------------------------------------------------------------- spawn / setup
    w('spawn', [
        '# Hook spawn (@s = the arena marker at the centre of tk_lift). The body (mboss/body: husk scale 1.25, click shield,',
        '# miniboss economy) stands at the centre facing south (yaw 0), toward the player arriving at the south edge.',
        'execute rotated 0 0 run function rlk:mboss/body',
        at_body(fn('core/setup'))])
    w('core/setup', ['# @s = the new body: module state, the rig, Pyro blade (G1 start), the intro waits for intro_tick.',
                     fn('init'), fn('core/vars'), 'scoreboard players set @s aFire 0', 'scoreboard players set @s aThunder 0',
                     'scoreboard players set @s dFire 0', 'scoreboard players set @s dThunder 0',
                     api.rig('init'), api.rig('spawn'), api.rig('look/form/cape'), api.rig('look/visor/up_off'),
                     api.rig('look/edge/off'), api.rig('look/hands/open'),
                     fn(f'el/set{api.G1_START}'), api.rig('look/visor/up_off'), api.rig('look/edge/off'),
                     'data modify storage rlk:mboss sub set value []'])
    w('core/looks', ['# The rig looks of the current state (reload, phase steps, tests; @s = body).']
      + [f'execute if score #ph {OBJ} matches {a}..{b} run {api.rig(f"look/form/{f}")}' for f, (a, b) in FORM_OF_PH]
      + [fn('el/visor'), fn('el/edge'), api.rig('look/chest/off'), api.rig('look/hands/grip'), api.rig('state/normal')])
    # floors
    fl = ['# The HP floors (absolute HP) of the 70 % and 35 % phase steps from the max HP (@s = body; one pool, phases [100]).']
    for name, pct in FLOOR_PCT.items():
        fl += [f'scoreboard players operation #{name} {OBJ} = @s mhpM', f'scoreboard players operation #{name} {OBJ} /= #c100 {OBJ}',
               f'scoreboard players set #t {OBJ} {pct}', f'scoreboard players operation #{name} {OBJ} *= #t {OBJ}',
               f'execute if score #{name} {OBJ} matches ..0 run scoreboard players set #{name} {OBJ} 1']
    w('core/floors', fl)
    w('core/floor_hit', [
        '# The framework clamped a hit at #mbFloor (#mbFloorHit 1): the phase step is reserved for the next decision',
        '# (#flnext 1 = M1 -> T1 -> P2 at 70 %, 2 = M2 -> T2 -> P3 at 35 %). The floor stays until the mantle moves it.',
        'scoreboard players set #mbFloorHit mb 0',
        f'execute if score #fl {OBJ} matches 1 run return run function {NS}core/floor_2',
        f'execute if score #fl {OBJ} matches 0 run {sset("#flnext", 1)}',
        f'execute if score #fl {OBJ} matches 0 run {sset("#fl", 1)}'])
    w('core/floor_2', [sset('#fl', 2), sset('#flnext', 2)])
    # ---------------------------------------------------------------------------------------------- intro
    w('intro_tick', [
        f'# Hook intro_tick (@s = body, #mbT 1..; rlk_mb_inv). The intro sequence ({INTRO_LEN} t clip, seq/intro or the stand-in)',
        '# on the clock #sq tk; music phase 1 at 176, the push ring (no damage) at 178; the fight at the end.',
        f'execute if score #mbT mb matches 1 run {fn("core/intro/begin")}',
        f'execute unless score #mbT mb matches 1 run scoreboard players add #sq {OBJ} 1',
        f'execute unless score #mbT mb matches 1 run {seq_or_stand(ctx, "intro", "tick")}',
        f'execute if score #sq {OBJ} matches {api.ev("intro", "music")} run {L.music(1)}',
        f'execute if score #sq {OBJ} matches {api.ev("intro", "ring")} at @s run {L.push_ring(4.0, 4)}',
        f'execute if score #sqdone {OBJ} matches 1 run {fn("core/intro/done")}',
        f'execute if score #sq {OBJ} matches {INTRO_LEN + 2}.. run {fn("core/intro/done")}',
        api.rig('tick')])
    w('core/intro/begin', ['# Intro tick 0 (@s = body).', sset('#sq', 0), sset('#sqdone', 0), sset('#ph', PH['intro']),
                           seq_or_stand(ctx, 'intro', 'start')])
    w('core/intro/done', [
        '# The intro is over (its end, the framework cap, a reload or a test; @s = body): the fight state, P1, the floors.',
        'function rlk:mboss/intro_end',
        f'execute unless score #ph {OBJ} matches {PH["intro"]} run return 0',
        sset('#ph', PH['p1']), sset('#sq', 0), sset('#sqdone', 0), sset('#pat', 0), fn('core/floors'),
        f'execute if score #fl {OBJ} matches 0 run scoreboard players operation #mbFloor mb = #fl70 {OBJ}',
        fn('ai/phase'), fn('core/looks'), fn('ai/sample'), fn('ai/rec_start'), sset('#rec', 20), fn('el/badge'), fn('hud/sub')])
    w('core/intro/reload', ['# /reload during the intro: straight to its end (standing, sword lit), music phase 1.',
                            seq_or_stand(ctx, 'intro', 'cancel'), fn('core/intro/done'), L.music(1)])
    # ---------------------------------------------------------------------------------------------- the fight tick
    w('tick', [
        '# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==',
        '# the pattern clock #pt).',
        f'execute if score #ph {OBJ} matches {PH["intro"]} run {fn("core/intro/done")}',
        f'execute if score #ph {OBJ} matches {PH["p1"]}..{PH["p3"]} run {fn("core/fight")}',
        api.rig('tick')])
    fight = [
        '# One fight tick (@s = body): module clock, G3 backfire, the floor, the G1 aura, AI samples, then the running state.',
        f'scoreboard players add #clk {OBJ} 1',
        f'scoreboard players add #ai_pht {OBJ} 1',
        f'execute if score #core {OBJ} matches 2 run {fn("el/backfire")}',
        'execute unless score #mbSt mb matches 1 run return 0',
        f'execute if score #mbFloorHit mb matches 1 run {fn("core/floor_hit")}',
        f'scoreboard players add #aut {OBJ} 1',
        f'execute if score #aut {OBJ} matches {api.G1_REFRESH_T}.. run {fn("el/refresh")}',
        f'scoreboard players add #swt {OBJ} 1',
        f'scoreboard players operation #t {OBJ} = #clk {OBJ}',
        f'scoreboard players operation #t {OBJ} %= #c{AI.SAMPLE_EVERY} {OBJ}',
        f'execute if score #t {OBJ} matches 0 run {fn("ai/sample")}',
        f'execute if score #stag {OBJ} matches 1.. run return run {fn("core/stag_tick")}',
        f'execute if score #lock {OBJ} matches 1 if score #pat {OBJ} matches 0 run return 0',
        f'execute if score #pat {OBJ} matches 1..11 run return run {fn("core/pat_tick")}',
        f'execute if score #pat {OBJ} matches {SWAP_PAT} run return run {fn("el/swap_tick")}',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT} run return run {fn("mantle/tick")}',
        f'execute if score #pat {OBJ} matches {BREAK_PAT} run return run {fn("mantle/break_tick")}',
        f'execute if score #pat {OBJ} matches {NOVA_PAT} run return run {fn("mantle/nova_tick")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} run return run {fn("core/tr/tick")}',
        f'execute if score #pat {OBJ} matches {REPLAY_PAT} run return run {fn("core/replay/tick")}',
        fn('ai/recover')]
    w('core/fight', fight)
    w('core/stag_tick', ['# G3 stagger countdown (@s = body); then the recovery.',
                         f'scoreboard players remove #stag {OBJ} 1',
                         f'execute if score #stag {OBJ} matches ..0 run {fn("core/stag_end")}'])
    w('core/stag_end', [sset('#stag', 0), sset('#taken', 100), sset('#pat', 0), fn('ai/rec_start'), fn('hud/sub')])
    # patterns: start / run / end / cancel
    pt = ['# The running pattern (@s = body): #pt + 1, the core wrapper core/run/<key> (G3 window tags + p/<key>/tick).',
          f'scoreboard players add #pt {OBJ} 1']
    for k in present:
        pt.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"core/run/{k}")}')
    pt.append(f'execute if score #done {OBJ} matches 1 run {fn("core/pat_end")}')
    w('core/pat_tick', pt)
    for k in present:
        tid = S.TID[k]
        w(f'core/run/{k}', [f'# {k.upper()} one tick (@s = body).'] + E.g3_lines(k, tid) + [fn(f'p/{k}/tick')])
        cdl = []
        for fp in (1, 2, 3):
            cdl += [f'execute if score #ai_fp {OBJ} matches {fp} run {sset("#t", AI.cooldown(k, fp))}']
        start = [f'# Start {k.upper()} {api.PATTERN_NAMES[k]} (@s = body; the AI, the rear / far rules, tests).',
                 fn('core/stop_move'), sset('#pat', tid), sset('#pt', 0), sset('#done', 0), sset('#core', 0),
                 f'scoreboard players operation #last2 {OBJ} = #last {OBJ}', sset('#last', tid)]
        start += [sset('#kgap', 0)] if k == 'k' else [f'scoreboard players add #kgap {OBJ} 1']
        start += cdl + [f'scoreboard players operation #cd_{k} {OBJ} = #clk {OBJ}', f'scoreboard players operation #cd_{k} {OBJ} += #t {OBJ}']
        start += E.g3_start_lines(k) + [fn('hud/sub'), fn(f'p/{k}/start')]
        w(f'core/start/{k}', start)
        w(f'core/hz_tag/{k}', [f'# @s = a hazard of {k.upper()} just made: the pattern tags (its cancel kills it).',
                               f'tag @s add {api.TAGS["pat"]}', f'tag @s add {S.tag_p(k)}'])
    w('core/stop_move', ['# The body stops gliding / prowling (@s = body).', 'execute if entity @s[tag=rlk_mb_mv] run function rlk:mboss/mv/stop'])
    pend = ['# The pattern set #done (@s = body): its G3 tag off, the post-pattern G1 swap (always after K, 50 % after a C),',
            '# else the recovery.',
            f'tag @s remove {api.TAGS["core"]}', sset('#done', 0), sset('#pat', 0), f'scoreboard players set #pt {OBJ} 0']
    if 'k' in present:
        pend.append(f'execute if score #last {OBJ} matches {S.TID["k"]} run return run {fn("el/swap_start")}')
    pend += [f'execute if score #last {OBJ} matches {AI.C_TIDS[0]}..{AI.C_TIDS[-1]} store result score #t {OBJ} run random value 1..100',
             f'execute if score #last {OBJ} matches {AI.C_TIDS[0]}..{AI.C_TIDS[-1]} if score #t {OBJ} matches ..{api.G1_SWAP_AFTER_C} '
             f'run return run {fn("el/swap_start")}',
             fn('ai/rec_start'), fn('hud/sub')]
    w('core/pat_end', pend)
    cd = ['# Cancel the running pattern (any executor; idempotent): its own cancel (hazards, markers, glide, looks).']
    for k in present:
        cd.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"p/{k}/cancel")}')
    w('core/cancel_d', cd)
    w('core/cancel_pat', ['# Cancel the running pattern (G3 backfire, reload, tests; @s = body): recovery follows.',
                          fn('core/cancel_d'), f'tag @s remove {api.TAGS["core"]}', sset('#pat', 0), sset('#done', 0),
                          fn('core/stop_move'), fn('el/edge'), api.rig('look/chest/off'), fn('ai/rec_start')])
    w('core/dash/probe', [
        '# Dash probe (@s = body, rotated as it): a marker rlk_tk_dp walks forward in 0.5 b steps while the next spot passes',
        '# mv/ok (inside the arena safe disc - 0.5 b, feet and head free), at most #t tk steps; #t2 tk = steps taken.',
        'kill @e[type=minecraft:marker,tag=rlk_tk_dp]',
        'execute at @s rotated as @s rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_dp"]}',
        'execute at @s rotated as @s rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] run tp @s ~ ~ ~ ~ 0',
        sset('#t2', 0),
        f'execute as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] at @s run {fn("core/dash/step")}'])
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
    # ---------------------------------------------------------------------------------------------- transitions
    tr_start = ['# The transition after a mantle (@s = body): M1 -> T1 날개 전개, M2 -> T2 심연; invulnerable throughout.',
                f'execute if score #ph {OBJ} matches {PH["m1"]} run {sset("#ph", PH["t1"])}',
                f'execute if score #ph {OBJ} matches {PH["m2"]} run {sset("#ph", PH["t2"])}',
                sset('#pat', TR_PAT), sset('#pt', 0), sset('#sq', 0), sset('#sqdone', 0), sset('#taken', 100),
                'tag @s add rlk_mb_inv', fn('core/stop_move'),
                f'execute if score #ph {OBJ} matches {PH["t1"]} run {seq_or_stand(ctx, "t1", "start")}',
                f'execute if score #ph {OBJ} matches {PH["t2"]} run {seq_or_stand(ctx, "t2", "start")}', fn('hud/sub')]
    w('core/tr/start', tr_start)
    t1len, t2len = api.CLIPS['t1_wings'][0], api.CLIPS['t2_abyss'][0]
    w('core/tr/tick', [
        '# Transition tick (#pat 54): the sequence on #sq; T1 push ring (no damage) at its flare, T2 music phase 2 at its swap.',
        f'scoreboard players add #sq {OBJ} 1',
        f'execute if score #ph {OBJ} matches {PH["t1"]} run {seq_or_stand(ctx, "t1", "tick")}',
        f'execute if score #ph {OBJ} matches {PH["t2"]} run {seq_or_stand(ctx, "t2", "tick")}',
        f'execute if score #ph {OBJ} matches {PH["t1"]} if score #sq {OBJ} matches {api.ev("t1_wings", "flare")} at @s run {L.push_ring(4.0, 4)}',
        f'execute if score #ph {OBJ} matches {PH["t2"]} if score #sq {OBJ} matches {api.ev("t2_abyss", "swap")} run {L.music(2)}',
        f'execute if score #sqdone {OBJ} matches 1 run return run {fn("core/tr/end")}',
        f'execute if score #ph {OBJ} matches {PH["t1"]} if score #sq {OBJ} matches {t1len + 40}.. run return run {fn("core/tr/end")}',
        f'execute if score #ph {OBJ} matches {PH["t2"]} if score #sq {OBJ} matches {t2len + 40}.. run {fn("core/tr/end")}'])
    w('core/tr/end', [
        '# The transition is over (or a reload / test finishes it; @s = body): P2 (T1) or P3 (T2, the HP floor off).',
        'tag @s remove rlk_mb_inv',
        f'execute if score #ph {OBJ} matches {PH["t1"]} run {sset("#ph", PH["p2"])}',
        f'execute if score #ph {OBJ} matches {PH["t2"]} run scoreboard players set #mbFloor mb 0',
        f'execute if score #ph {OBJ} matches {PH["t2"]} run {sset("#ph", PH["p3"])}',
        sset('#pat', 0), sset('#sq', 0), sset('#sqdone', 0), sset('#aut', api.G1_REFRESH_T),
        fn('ai/phase'), fn('core/looks'), fn('ai/rec_start'), sset('#rec', 10), fn('hud/sub')])
    # intro replay (test 26)
    w('core/replay/start', ['# Test 26: the intro again (@s = body, invulnerable), then the fight goes on.',
                            sset('#pat', REPLAY_PAT), sset('#sq', 0), sset('#sqdone', 0), 'tag @s add rlk_mb_inv',
                            api.rig('look/visor/up_off'), api.rig('look/edge/off'), seq_or_stand(ctx, 'intro', 'start')])
    w('core/replay/tick', [f'scoreboard players add #sq {OBJ} 1', seq_or_stand(ctx, 'intro', 'tick'),
                           f'execute if score #sqdone {OBJ} matches 1 run return run {fn("core/replay/end")}',
                           f'execute if score #sq {OBJ} matches {INTRO_LEN + 2}.. run {fn("core/replay/end")}'])
    w('core/replay/end', [seq_or_stand(ctx, 'intro', 'cancel'), 'tag @s remove rlk_mb_inv', sset('#pat', 0), sset('#sq', 0),
                          sset('#sqdone', 0), fn('core/looks'), fn('ai/rec_start')])
    # ---------------------------------------------------------------------------------------------- stand-in sequences
    stand_ins(W, ctx)
    # ---------------------------------------------------------------------------------------------- hooks
    w('on_hit', [
        '# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm known; scores only). G2: the mantle gauge;',
        '# G3: the first reaction on her inside a core window flags the backfire (handled by the next fight tick).',
        f'execute if entity @s[tag={api.TAGS["mantle"]}] run {fn("mantle/hit")}',
        f'execute if entity @s[tag={api.TAGS["core"]}] if score #rx tmp matches 1.. if score #core {OBJ} matches 0 run {sset("#core", 2)}'])
    w('aux_hit', ['# Hook aux_hit: Tachy has no aux objects (framework default).'])
    w('incoming', [
        '# Hook incoming (@s = body inside combat/apply_mods; the framework floor runs after it): damage taken x #taken %',
        f'# (100; mantle {api.G2_TAKEN_PCT}, stun {api.G2_STUN_TAKEN_PCT}, G3 stagger {api.G3_STAGGER_TAKEN_PCT}).',
        f'execute if score #taken {OBJ} matches 100 run return 0',
        f'scoreboard players operation #dmg tmp *= #taken {OBJ}',
        f'scoreboard players operation #dmg tmp /= #c100 {OBJ}'])
    pause = ['# Hook pause (the fight froze): the kit cards go; patterns with a pause hook (S4).'] + \
        ([K.fixed('clear')] if K.fixed('clear') else [])
    resume = ['# Hook resume (@s = body): patterns with a resume hook (S4); during the mantle the cocoon card again (pause',
              '# cleared the kit cards; the gauge redraws it), during the nova the rest of its swell (S4 p/mantle/nova/resume).']
    for k in present:
        if ctx.has_pat_file(k, 'pause'):
            pause.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"p/{k}/pause")}')
        if ctx.has_pat_file(k, 'resume'):
            resume.append(f'execute if score #pat {OBJ} matches {S.TID[k]} run {fn(f"p/{k}/resume")}')
    if S.fx_plain('cocoon', [], pct=100):
        resume += [f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {sset("#hud_c", -1)}',
                   f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {fn("mantle/gauge")}']
    if ctx.has_s4('p/mantle/nova/resume'):
        resume.append(f'execute if score #pat {OBJ} matches {NOVA_PAT} run {fn("p/mantle/nova/resume")}')
    w('pause', pause)
    w('resume', resume)
    w('core/stop_all', [
        '# Everything of the fight state stops (death, cleanup; any executor): the pattern, the mantle, a transition, tags.',
        fn('core/cancel_d'), fn('mantle/cancel'),
        f'execute if score #pat {OBJ} matches {TR_PAT} if score #ph {OBJ} matches {PH["t1"]} run {seq_or_stand(ctx, "t1", "cancel")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} if score #ph {OBJ} matches {PH["t2"]} run {seq_or_stand(ctx, "t2", "cancel")}',
        f'execute if score #pat {OBJ} matches {REPLAY_PAT} run {seq_or_stand(ctx, "intro", "cancel")}',
        f'kill @e[tag={api.TAGS["pat"]}]', f'kill @e[tag={api.TAGS["air"]}]',
        f'tag @e[tag={api.TAGS["core"]}] remove {api.TAGS["core"]}', f'tag @e[tag={api.TAGS["mantle"]}] remove {api.TAGS["mantle"]}',
        sset('#pat', 0), sset('#stag', 0), sset('#stun', 0), sset('#taken', 100), sset('#done', 0)])
    w('death_start', [
        '# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, stopped the music): every state',
        '# stops, the kit cards go, the death sequence (seq/death or the clip) on #sq; the special win path follows.',
        fn('core/stop_all')] + ([K.fixed('clear')] if K.fixed('clear') else []) + [
        'scoreboard players set #mbFloor mb 0', sset('#ph', PH['death']), sset('#sq', 0), sset('#sqdone', 0),
        fn('core/stop_move'), seq_or_stand(ctx, 'death', 'start')])
    w('death_tick', ['# Hook death_tick (@s = body, #mbT 1.. until cur.death).', f'scoreboard players add #sq {OBJ} 1',
                     seq_or_stand(ctx, 'death', 'tick'), api.rig('tick')])
    cl = ['# Hook cleanup (no executor; idempotent): every state, hazard and marker of the module, the kit cards and HUD,',
          '# the rig, the module scores (init makes them again) and storage core.*.',
          fn('core/stop_all')]
    for s in sorted(ctx.services):
        cl.append(fn(f'seq/{s}/cancel'))
    cl += [K.fixed('clear'), *S.hud('clear'), at_body(api.rig('kill')),
           f'kill @e[tag={api.TAGS["part"]}]', f'kill @e[tag={api.TAGS["prop"]}]', 'kill @e[type=minecraft:marker,tag=rlk_tk_dp]',
           f'scoreboard players reset * {OBJ}', f'data remove storage {api.STORAGE} core']
    w('cleanup', [x for x in cl if x])
    un = ['# Hook uninstall (no executor; every enabled module): the kit, the rig, the module entities, objective tk, storage.']
    un += [K.fixed('uninstall'), api.rig('uninstall'), f'kill @e[tag={api.TAGS["pat"]}]', f'kill @e[tag={api.TAGS["air"]}]',
           f'kill @e[tag={api.TAGS["part"]}]', f'kill @e[tag={api.TAGS["prop"]}]', f'kill @e[tag={api.TAGS["fx"]}]',
           f'scoreboard objectives remove {OBJ}', f'data remove storage {api.STORAGE} core']
    w('uninstall', [x for x in un if x])
    w('reload', [
        '# Hook reload (@s = body after /reload: the rig parts, hazards, markers and kit cards are gone; scores are kept).',
        '# intro -> its end; a pattern -> cancelled + recovery; a swap -> finished; a mantle -> gauge and time kept;',
        '# a break / stun goes on; a nova -> the transition; a transition -> finished; the intro replay -> ended.',
        fn('init'), api.rig('init'), api.rig('spawn'), sset('#lock', 0),
        f'execute if score #ph {OBJ} matches {PH["intro"]} run return run {fn("core/intro/reload")}',
        f'execute if score #ph {OBJ} matches {PH["death"]} run return 0',
        f'execute if score #pat {OBJ} matches 1..11 run {fn("core/cancel_pat")}',
        f'execute if score #pat {OBJ} matches {SWAP_PAT} run {fn("el/swap_end")}',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT}..{NOVA_PAT} run {fn("mantle/reload")}',
        f'execute if score #pat {OBJ} matches {TR_PAT} run {fn("core/tr/end")}',
        f'execute if score #pat {OBJ} matches {REPLAY_PAT} run {fn("core/replay/end")}',
        f'execute if score #stag {OBJ} matches 1.. run {api.play("stagger")}',
        fn('core/looks'), f'execute unless entity @s[tag={api.TAGS["mantle"]}] run {fn("el/badge")}', fn('hud/sub'),
        f'execute if score #pat {OBJ} matches 0 if score #stag {OBJ} matches 0 run {fn("ai/rec_start")}'])
    w('bars', ['# Hook bars (@s = body, every tick in intro / fight): the under-bar = the mantle gauge (gold) or the stun.',
               f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {fn("hud/bar_gauge")}',
               f'execute if score #pat {OBJ} matches {BREAK_PAT} if score #stun {OBJ} matches 1.. run {fn("hud/bar_stun")}'])
    w('hud/bar_gauge', [f'scoreboard players operation #buSub bu = #sh {OBJ}', f'scoreboard players set #buSubMax bu {api.G2_GAUGE}',
                        'scoreboard players set #buSubCol bu 8'])
    w('hud/bar_stun', [f'scoreboard players operation #buSub bu = #stun {OBJ}', f'scoreboard players set #buSubMax bu {api.G2_STUN_T}',
                       'scoreboard players set #buSubCol bu 8'])
    sub = ['# The boss-bar sub line (@s any; on every state change): phase title + the running pattern name (names only).',
           'data modify storage rlk:mboss sub set value []']
    for ph, t in TITLE.items():
        sub.append(f'execute if score #ph {OBJ} matches {ph} run data modify storage rlk:mboss sub set value '
                   f'[{{text:"{t}",color:"{TITLE_HEX[ph]}",bold:true}}]')
    names = {S.TID[k]: api.PATTERN_NAMES[k] for k in present}
    names[SWAP_PAT] = api.TEST_HELP_NAMES[24]
    for pid, nm in sorted(names.items()):
        sub.append(f'execute if score #pat {OBJ} matches {pid} run data modify storage rlk:mboss sub append value '
                   f'{{text:"  ·  {nm}",color:"#E8E2D0",bold:false}}')
    w('hud/sub', sub)
    w('hz_vis', ['# Hook hz_vis: Tachy hazards are quiet (#hzQuiet 1, no #hzVis): nothing to draw.'])
    pj = ['# Hook pj_end (@s = a projectile prop, #pjEv; #pjKeep preset): the pattern that launched it, if it has a pj_end.']
    for k in present:
        if ctx.has_pat_file(k, 'pj_end'):
            pj.append(f'execute if entity @s[tag={S.tag_p(k)}] run return run {fn(f"p/{k}/pj_end")}')
    if ctx.has_s4('p/mantle/pj_end'):
        pj.append(f'execute if entity @s[tag={S.tag_p("mantle")}] run return run {fn("p/mantle/pj_end")}')
    w('pj_end', pj)
    tests(W, ctx)
    if not api.rig_real():
        rig_stub(W)


def stand_ins(W, ctx):
    """core/sq/<name>/{start,tick,cancel} for every sequence S2's seq.SERVICES does not provide yet: the clip, its length,
    the few state changes the fight needs (looks, the arena look job at T2's dark, the title at the intro ignite)."""
    w = W.w
    spec = {
        'intro': ('intro', {api.ev('intro', 'visor'): [api.rig('look/visor/down_pyro')],
                            api.ev('intro', 'ignite'): [api.rig('look/edge/pyro'),
                                                        'title @a[tag=player] times 6 40 12',
                                                        f'title @a[tag=player] subtitle ["",{{text:"{api.SUB}",color:"#E8E2D0"}}]',
                                                        f'title @a[tag=player] title ["",{{text:"{api.NAME}",color:"{api.COLOR}",bold:true}}]']}),
        't1': ('t1_wings', {api.ev('t1_wings', 'split'): [api.rig('look/form/winged')]}),
        't2': ('t2_abyss', {api.ev('t2_abyss', 'flare'): [api.rig('look/visor/down_abyss')],
                            api.ev('t2_abyss', 'dark'): [x for x in (api.arena_look('abyss'),
                                                                     'effect give @a[tag=player] minecraft:blindness 1 0 true') if x],
                            api.ev('t2_abyss', 'swap'): [api.rig('look/form/abyss')]}),
        'death': ('death', {api.ev('death', 'knee'): S.placed(S.snd('death_knee'), 'at @s'),
                            api.ev('death', 'ash'): S.placed(S.snd('death_ash'), 'at @s')}),
    }
    for name in api.SEQS:
        if name in ctx.services:
            continue
        clip, evs = spec[name]
        ln = api.CLIPS[clip][0]
        w(f'core/sq/{name}/start', [f'# Stand-in sequence {name} (S2 seq.py has none yet): the clip {clip} ({ln} t), sq 0.',
                                    sset('#sqdone', 0), api.play(clip)])
        tick = [f'# Stand-in {name} tick (#sq tk 1..{ln}).']
        for t in sorted(evs):
            for c in evs[t]:
                tick.append(f'execute if score #sq {OBJ} matches {t} {c[8:]}' if c.startswith('execute ')
                            else f'execute if score #sq {OBJ} matches {t} run {c}')
        tick.append(f'execute if score #sq {OBJ} matches {ln}.. run {sset("#sqdone", 1)}')
        w(f'core/sq/{name}/tick', tick)
        w(f'core/sq/{name}/cancel', [f'# Stand-in {name} cancel: nothing of its own lingers.'])


def tests(W, ctx):
    w = W.w
    present = ctx.present
    w('test', ['# Hook test {id:N} (as the player, /function rlk:boss/test/pattern {id:N}); the list: test/help.',
               f'$scoreboard players set #tst {OBJ} $(id)',
               at_body(fn('test/run'))])
    run = ['# @s = body: the test #tst (api.TEST_IDS).']
    for k in present:
        run.append(f'execute if score #tst {OBJ} matches {S.TID[k]} run return run {fn(f"test/go/{k}")}')
        w(f'test/go/{k}', [f'execute unless function {NS}core/force run return 0', fn(f'core/start/{k}')])
    for tid, rel in ((20, 'test/mantle_b'), (21, 'test/mantle_f'), (22, 'test/tr1'), (23, 'test/tr2'), (24, 'test/swap'),
                     (25, 'test/g3'), (26, 'test/intro'), (27, 'test/death'), (30, 'test/ph2'), (31, 'test/ph3'),
                     (40, 'test/el1'), (41, 'test/el3'), (80, 'test/floor'), (99, 'test/freeze')):
        run.append(f'execute if score #tst {OBJ} matches {tid} run return run {fn(rel)}')
    w('test/run', run)
    w('core/force', [
        '# Tests: make the fight state ready for a forced action (@s = body). Fails during a mantle / transition / replay.',
        f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT}.. run return fail',
        f'execute if score #pat {OBJ} matches 1..11 run {fn("core/cancel_pat")}',
        f'execute if score #pat {OBJ} matches {SWAP_PAT} run {sset("#pat", 0)}',
        f'execute if score #stag {OBJ} matches 1.. run {fn("core/stag_end")}',
        'return 1'])
    mantle_go = [f'execute unless function {NS}core/force run return 0',
                 f'execute if score #ph {OBJ} matches {PH["p1"]} run {sset("#fl", 1)}',
                 f'execute if score #ph {OBJ} matches {PH["p1"]} run {sset("#flnext", 1)}',
                 f'execute if score #ph {OBJ} matches {PH["p2"]}.. run {sset("#fl", 2)}',
                 f'execute if score #ph {OBJ} matches {PH["p2"]}.. run {sset("#flnext", 2)}',
                 fn('mantle/start')]
    w('test/mantle_b', ['# Test 20: the mantle of the next phase step, gauge 1 (the next hit breaks it).'] + mantle_go + [sset('#sh', 1)])
    w('test/mantle_f', ['# Test 21: the mantle of the next phase step, 1 t left (the nova).'] + mantle_go + [sset('#sht', 1)])
    w('test/tr1', ['# Test 22: T1 날개 전개 now (then P2).', f'execute unless function {NS}core/force run return 0',
                   sset('#fl', 1), sset('#ph', PH['m1']), 'scoreboard players operation #mbFloor mb = #fl35 tk', fn('core/tr/start')])
    w('test/tr2', ['# Test 23: T2 심연 now (then P3).', f'execute unless function {NS}core/force run return 0',
                   sset('#fl', 2), sset('#ph', PH['m2']), 'scoreboard players set #mbFloor mb 1', fn('core/tr/start')])
    w('test/swap', ['# Test 24: the G1 swap now.', f'execute unless function {NS}core/force run return 0', fn('el/swap_start')])
    g3 = ['# Test 25: A1 with a reaction inside its core window (the backfire next tick).',
          f'execute unless function {NS}core/force run return 0']
    g3 += [fn('core/start/a1'), sset('#core', 2)] if 'a1' in present else []
    w('test/g3', g3)
    w('test/intro', ['# Test 26: the intro again (invulnerable).', f'execute unless function {NS}core/force run return 0',
                     fn('core/replay/start')])
    w('test/death', ['# Test 27: the death (true damage of her whole HP).', f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                     'scoreboard players operation #mbTrueEl mb = #el tk', 'function rlk:mboss/true_pct {pct:100}'])
    for n, ph, fl, form_floor in ((30, 'p2', 1, 'fl35'), (31, 'p3', 2, None)):
        lines = [f'# Test {n}: straight to {ph.upper()} (HP at most the floor above it).', f'execute unless function {NS}core/force run return 0',
                 sset('#fl', fl), sset('#flnext', 0), sset('#ph', PH[ph]), fn('mantle/cancel'),
                 f'execute if score @s mhpC > #{"fl70" if ph == "p2" else "fl35"} {OBJ} run scoreboard players operation @s mhpC = '
                 f'#{"fl70" if ph == "p2" else "fl35"} {OBJ}']
        lines += [f'scoreboard players operation #mbFloor mb = #{form_floor} {OBJ}'] if form_floor else ['scoreboard players set #mbFloor mb 0']
        if ph == 'p3':
            lines += [x for x in (api.arena_look('abyss'),) if x] + [L.music(2)]
        lines += [fn('ai/phase'), fn('core/looks'), sset('#pat', 0), fn('ai/rec_start'), fn('hud/sub')]
        w(f'test/ph{ph[1]}', lines)
    for e in (api.PYRO, api.ELECTRO):
        w(f'test/el{e}', [f'# Test {40 if e == api.PYRO else 41}: the blade element now (no swap clip).', fn(f'el/set{e}')])
    w('test/floor', ['# Test 80: HP = the next floor + 1.',
                     f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                     f'execute if score #fl {OBJ} matches 0 run scoreboard players operation @s mhpC = #fl70 {OBJ}',
                     f'execute if score #fl {OBJ} matches 1 run scoreboard players operation @s mhpC = #fl35 {OBJ}',
                     f'execute if score #fl {OBJ} matches ..1 run scoreboard players add @s mhpC 1'])
    w('test/freeze', ['# Test 99: freeze / unfreeze the AI (a running pattern finishes).',
                      f'execute store success score #lock {OBJ} unless score #lock {OBJ} matches 1'])
    rows = [H.head('/function rlk:boss/test/pattern {id:…}', f'{api.NAME} 시험 번호')]
    for tid, name in api.TEST_HELP_NAMES.items():
        key = api.TEST_IDS[tid]
        if tid <= 11 and key not in present:
            continue
        rows.append(H.row(f'/function rlk:boss/test/pattern {{id:{tid}}}', tid, name))
    rows.append(H.note('lock {id:1~11}: 그 패턴만 반복 · {id:0} 해제'))
    w('test/help', rows)


def rig_stub(W):
    """rig_stub/**: every rig call name of the contract while S2's manifest is missing. play/<clip> and start/<clip> set
    #rigc tk to the clip id (and #rigt tk to -1: the next tick shows tick 0); face/* turn the anchor; no visuals except a
    faint marker column so the body can be found in game."""
    w = W.w
    for c in api.RIG_CALLS:
        if c == 'tick':
            w('rig_stub/tick', ['# Stand-in rig tick (@s = body): the shown clip tick #rigt tk; a faint column marks the body.',
                                f'scoreboard players add #rigt {OBJ} 1',
                                'execute if score #rigt tk matches 0.. run particle minecraft:dust{color:[0.95,0.72,0.2],scale:1.0} '
                                '~ ~1.2 ~ 0.12 0.45 0.12 0 2 force @a[tag=player]'])
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
