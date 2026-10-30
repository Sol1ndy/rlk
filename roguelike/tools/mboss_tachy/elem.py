"""Elemental gimmicks of 타키 (Tachy) (PLAN §5; OWNER: S3): G1 쌍극 칼날 (permanent self-aura, swap), G2 과부하 외피 (the
mantle state machine, mantle/**), G3 불안정한 핵 (core windows on #pt, the backfire). Genshin systems only: the aura is the
boss's own element gauge (aFire / aThunder, 1000 = 1U, refreshed every 20 t when < 400: a score write + elAct 1, never a
damage event, so her own aura / swap never reacts); every player element reacts with one of the two auras (Hydro vaporize /
electro-charged, Cryo melt / superconduct, Dendro burning / quicken, Anemo swirl, Geo crystallize, Pyro <-> Electro
overload, Void its void reactions); no element immunity anywhere (registry res {"*":10}).

Writes el/**, mantle/** and the G3 lines of core/run/<key> (core.py calls g3_lines). Runtime: @s = the body, at it.
"""
from . import api
from . import s3lib as S

L, K = api.L, api.K
OBJ = api.OBJ
fn, sset = S.fn, S.sset
PY, EL = api.PYRO, api.ELECTRO
BADGE_TXT = {PY: ('◈' + api.EL_NAME[PY], api.EL_HEX[PY]), EL: ('◈' + api.EL_NAME[EL], api.EL_HEX[EL]), 9: ('◈외피', '#F2C230')}
SWAP_CLIP = {PY: 'swap_pyro', EL: 'swap_electro'}         # the clip that swaps TO this element
SWAP_EV = {PY: api.ev('swap_pyro', 'ignite'), EL: api.ev('swap_electro', 'spark')}
SWAP_LEN = api.CLIPS['swap_pyro'][0]
assert SWAP_LEN == api.CLIPS['swap_electro'][0] and SWAP_EV[PY] == SWAP_EV[EL]
AURA = {PY: 'aFire', EL: 'aThunder'}
MANTLE_PAT, BREAK_PAT, NOVA_PAT = 51, 52, 53
SWAP_PAT = 50
BREAK_LEN = api.CLIPS['mantle_break'][0]                  # 40: then the stun clip
STUN_END = BREAK_LEN + api.G2_STUN_T                       # 160
NOVA_LEN = api.CLIPS['mantle_nova'][0]                     # 44 (stand-in nova without S4)
IN_LEN = api.CLIPS['mantle_in'][0]


def badge_lines(code):
    """The boss-bar badge (kit fx/hud/badge; a plain extra[] text while the kit is missing; no glyph font)."""
    k = S.hud('badge', el=code)
    if k:
        return k
    t, c = BADGE_TXT[code]
    return [f'data modify storage rlk:mboss extra set value [{{text:"  {t}",color:"{c}",bold:true}}]']


def g3_lines(key, tid):
    """core/run/<key>: the body carries rlk_tk_core on pattern ticks t0..t1-1 of api.G3_WINDOWS[key] (t0 = 0 is tagged by
    core/start/<key>); never during a mantle, and not again after this pattern's backfire (#core 1)."""
    if key not in api.G3_WINDOWS:
        return []
    t0, t1 = api.G3_WINDOWS[key]
    out = []
    if t0 >= 1:
        out.append(f'execute if score #pt {OBJ} matches {t0} if score #core {OBJ} matches 0 unless entity @s[tag=rlk_tk_mantle] '
                   f'run tag @s add {api.TAGS["core"]}')
    out.append(f'execute if score #pt {OBJ} matches {t1} run tag @s remove {api.TAGS["core"]}')
    return out


def g3_start_lines(key):
    if key in api.G3_WINDOWS and api.G3_WINDOWS[key][0] == 0:
        return [f'execute unless entity @s[tag=rlk_tk_mantle] run tag @s add {api.TAGS["core"]}']
    return []


def build(W, ctx):
    """ctx: core.Ctx (present patterns, S4 mantle files)."""
    w = W.w
    # ---------------------------------------------------------------------------------------------- G1
    for e in (PY, EL):
        o = EL if e == PY else PY
        w(f'el/set{e}', [
            f'# G1: the blade element is {api.EL_NAME[e]} (@s = body). Her own aura {AURA[e]} = 1U, the other one 0 (a score',
            '# write: no damage event, so her own change never reacts); the blade edge / visor looks, the badge.',
            sset('#el', e), sset('#swt', 0), sset('#aut', 0),
            f'scoreboard players set @s {AURA[e]} {api.G1_AURA}',
            f'scoreboard players set @s {AURA[o]} 0',
            'scoreboard players set @s elAct 1',
            fn('el/edge'), fn('el/visor'),
            f'execute unless entity @s[tag={api.TAGS["mantle"]}] run {fn("el/badge")}'])
    w('el/badge', ['# The element badge on the boss-bar name line (@s any).']
      + [f'execute if score #el {OBJ} matches {e} run {ln}' for e in (PY, EL) for ln in badge_lines(e)])
    w('el/edge', ['# The blade edge look of the current element (@s = body).',
                  f'execute if score #el {OBJ} matches {PY} run {api.rig("look/edge/pyro")}',
                  f'execute if score #el {OBJ} matches {EL} run {api.rig("look/edge/electro")}'])
    w('el/visor', ['# The visor look: the abyss skull from T2 on, else the current element (@s = body).',
                   f'execute if score #ph {OBJ} matches {api.PH["t2"]}.. run return run {api.rig("look/visor/down_abyss")}',
                   f'execute if score #el {OBJ} matches {PY} run {api.rig("look/visor/down_pyro")}',
                   f'execute if score #el {OBJ} matches {EL} run {api.rig("look/visor/down_electro")}'])
    w('el/refresh', [
        f'# G1 aura refresh (every {api.G1_REFRESH_T} t from core/fight, @s = body): the current element back to 1U when below',
        f'# {api.G1_REFRESH_BELOW} (a reaction consumed it); elAct 1 keeps the element tick on her.',
        sset('#aut', 0),
        f'execute if score #el {OBJ} matches {PY} if score @s aFire matches ..{api.G1_REFRESH_BELOW - 1} run scoreboard players set @s aFire {api.G1_AURA}',
        f'execute if score #el {OBJ} matches {EL} if score @s aThunder matches ..{api.G1_REFRESH_BELOW - 1} run scoreboard players set @s aThunder {api.G1_AURA}',
        'scoreboard players set @s elAct 1'])
    w('el/flip', ['# The other element now (swap ignite / spark, the mantle alternation; @s = body).',
                  f'execute if score #el {OBJ} matches {PY} run return run {fn(f"el/set{EL}")}',
                  fn(f'el/set{PY}')])
    # swap (24 t, stationary: the punish window)
    w('el/swap_start', [
        f'# G1 swap (@s = body): {SWAP_LEN} t standing; she drags the blade through her palm, the edge changes at tick {SWAP_EV[PY]}.',
        sset('#pat', SWAP_PAT), sset('#pt', 0), sset('#done', 0),
        f'execute if score #el {OBJ} matches {PY} run {api.play(SWAP_CLIP[EL])}',
        f'execute if score #el {OBJ} matches {EL} run {api.play(SWAP_CLIP[PY])}']
      + [f'execute if score #el {OBJ} matches {PY} run {x}' for x in S.snd('swap_electro')]
      + [f'execute if score #el {OBJ} matches {EL} run {x}' for x in S.snd('swap_pyro')]
      + [fn('hud/sub')])
    fx_swap = []
    for e in (PY, EL):
        fx_swap += [f'execute if score #el {OBJ} matches {e} run {x}' if not x.startswith('execute ')
                    else x.replace('execute ', f'execute if score #el {OBJ} matches {e} ', 1)
                    for x in S.fx_plain('swap_fx', [f'execute at @s run particle {S.EL_PART[e]} ~ ~1.2 ~ 0.4 0.6 0.4 0.05 24 force @a[tag=player]'],
                                        el=e)]
    w('el/swap_tick', [f'# G1 swap tick (#pat {SWAP_PAT}).',
                       f'scoreboard players add #pt {OBJ} 1',
                       f'execute if score #pt {OBJ} matches {SWAP_EV[PY]} run {fn("el/swap_do")}',
                       f'execute if score #pt {OBJ} matches {SWAP_LEN}.. run {fn("el/swap_end")}'])
    w('el/swap_do', ['# The edge changes (swap event): the new element, its burst.', fn('el/flip')] + fx_swap)
    w('el/swap_end', ['# End of the swap (or a reload during it): the recovery.', sset('#pat', 0), fn('ai/rec_start'),
                      fn('hud/sub')])
    # ---------------------------------------------------------------------------------------------- G3 backfire
    w('el/backfire', [
        '# G3 backfire (@s = body; on_hit flagged #core 2: the first reaction on her inside a core window): the pattern is',
        f'# cancelled, a burst at her chest, true damage {api.G3_TRUE_PCT} % of her max HP, stagger {api.G3_STAGGER_T} t taking '
        f'{api.G3_STAGGER_TAKEN_PCT} %. Once per pattern.',
        sset('#core', 1),
        f'execute unless score #pat {OBJ} matches 1..11 run return 0',
        fn('core/cancel_pat')]
      + S.fx_plain('core_burst', ['execute at @s run particle minecraft:explosion_emitter ~ ~1.4 ~ 0 0 0 0 1 force @a[tag=player]',
                                  'execute at @s run particle minecraft:flame ~ ~1.4 ~ 0.3 0.3 0.3 0.2 40 force @a[tag=player]'],
                     pos=f'~ ~{S.H(1.4)} ~')
      + [f'execute at @s run {x}' if not x.startswith('execute') else x for x in S.snd('core_backfire')]
      + [f'scoreboard players operation #mbTrueEl mb = #el {OBJ}',
         f'function rlk:mboss/true_pct {{pct:{api.G3_TRUE_PCT}}}',
         'execute unless score #mbSt mb matches 1 run return 0',
         '# true damage skips the HP floor: a backfire below it still reserves the phase step',
         'execute if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run scoreboard players set #mbFloorHit mb 1',
         sset('#stag', api.G3_STAGGER_T), sset('#taken', api.G3_STAGGER_TAKEN_PCT), api.play('stagger')]
      + [f'execute at @s run {x}' if not x.startswith('execute') else x for x in S.snd('stagger')])
    # ---------------------------------------------------------------------------------------------- G2 mantle
    feather = ctx.has_s4('p/mantle/feather')
    nova = ctx.has_s4('p/mantle/nova/start')
    # The gauge itself is the boss-bar under-bar (hook bars -> hud/bar_gauge, as every boss); the kit's name-line gauge
    # cells (fx/hud/gauge) are not shown (I1: one gauge only). Here: the cocoon card cracks in 4 steps.
    gauge = ['# The mantle gauge changed (@s = body): the cocoon card of its quarter (the gauge is the boss-bar under-bar).',
             f'scoreboard players operation #hud_g {OBJ} = #sh {OBJ}']
    for lo, hi, pct in ((76, 1000, 100), (51, 75, 75), (26, 50, 50), (-1000, 25, 25)):
        for ln in S.fx_plain('cocoon', [], pos=f'~ ~{S.H(1.2)} ~', pct=pct):
            gauge.append(f'execute if score #sh {OBJ} matches {lo}..{hi} unless score #hud_c {OBJ} matches {pct} run {ln}'
                         if not ln.startswith('execute ') else
                         ln.replace('execute ', f'execute if score #sh {OBJ} matches {lo}..{hi} unless score #hud_c {OBJ} matches {pct} ', 1))
        gauge.append(f'execute if score #sh {OBJ} matches {lo}..{hi} run scoreboard players set #hud_c {OBJ} {pct}')
    w('mantle/gauge', gauge)
    w('mantle/start', [
        '# G2 과부하 외피 (@s = body; the phase step reserved by a floor: #flnext 1 = M1 at 70 %, 2 = M2 at 35 %). She wraps',
        f'# herself in the wings; gauge {api.G2_GAUGE}, she takes {api.G2_TAKEN_PCT} % damage, time {api.G2_TIME["m1"]} / {api.G2_TIME["m2"]} t;',
        '# the HP floor moves to the next one (M1: 35 %; M2: 1 HP until P3) so the mantle damage counts.',
        f'execute if score #flnext {OBJ} matches 1 run {sset("#ph", api.PH["m1"])}',
        f'execute if score #flnext {OBJ} matches 1 run {sset("#sht", api.G2_TIME["m1"])}',
        f'execute if score #flnext {OBJ} matches 1 run scoreboard players operation #mbFloor mb = #fl35 {OBJ}',
        f'execute if score #flnext {OBJ} matches 2.. run {sset("#ph", api.PH["m2"])}',
        f'execute if score #flnext {OBJ} matches 2.. run {sset("#sht", api.G2_TIME["m2"])}',
        f'execute if score #flnext {OBJ} matches 2.. run scoreboard players set #mbFloor mb 1',
        sset('#flnext', 0), sset('#pat', MANTLE_PAT), sset('#pt', 0), sset('#sh', api.G2_GAUGE), sset('#shicd', 0),
        sset('#taken', api.G2_TAKEN_PCT), sset('#core', 1), sset('#hud_g', -1), sset('#hud_c', -1),
        f'tag @s remove {api.TAGS["core"]}', f'tag @s add {api.TAGS["mantle"]}',
        api.play('mantle_in')]
      + [f'execute at @s run {x}' if not x.startswith('execute') else x for x in S.snd('mantle_wrap')]
      + badge_lines(9) + [fn('mantle/gauge'), fn('hud/sub')])
    tick = [f'# G2 mantle tick (#pat {MANTLE_PAT}): hold clip, timers, aura alternation every {api.G2_ALT_T} t (in sync with the veins),',
            f'# a feather every {api.G2_FEATHER_EVERY} t (S4 p/mantle/feather), the gauge HUD; break at 0, failure at the time limit.',
            f'scoreboard players add #pt {OBJ} 1',
            f'execute if score #pt {OBJ} matches {IN_LEN} run {api.play("mantle_hold")}',
            f'execute if score #shicd {OBJ} matches 1.. run scoreboard players remove #shicd {OBJ} 1',
            f'scoreboard players remove #sht {OBJ} 1',
            f'scoreboard players operation #t {OBJ} = #pt {OBJ}',
            f'scoreboard players operation #t {OBJ} %= #c{api.G2_ALT_T} {OBJ}',
            f'execute if score #t {OBJ} matches 0 run {fn("el/flip")}']
    if feather:
        tick += [f'scoreboard players operation #t {OBJ} = #pt {OBJ}',
                 f'scoreboard players operation #t {OBJ} %= #c{api.G2_FEATHER_EVERY} {OBJ}',
                 f'execute if score #t {OBJ} matches 0 run {fn("p/mantle/feather")}']
    tick += [f'execute unless score #sh {OBJ} = #hud_g {OBJ} run {fn("mantle/gauge")}',
             f'execute if score #sh {OBJ} matches ..0 run return run {fn("mantle/break")}',
             f'execute if score #sht {OBJ} matches ..0 run return run {fn("mantle/fail")}']
    w('mantle/tick', tick)
    w('mantle/hit', [
        '# G2 gauge from a player hit (on_hit, @s = body inside combat/apply: scores only). Any reaction triggered on her -'
        f'{api.G2_RX};',
        f'# an electro-charged / burning tick -{api.G2_DOT}; any other hit -{api.G2_HIT} (once per {api.G2_HIT_ICD} t).',
        f'execute if score #rx tmp matches 1.. run return run scoreboard players remove #sh {OBJ} {api.G2_RX}',
        f'execute if score #tfm tmp matches 1 if score #elem tmp matches 3 if score @s ecI matches 0 if score @s aWater matches 1.. '
        f'run return run scoreboard players remove #sh {OBJ} {api.G2_DOT}',
        f'execute if score #tfm tmp matches 1 if score #elem tmp matches 1 if score @s burnOn matches 1 if score @s burnI matches 0 '
        f'run return run scoreboard players remove #sh {OBJ} {api.G2_DOT}',
        f'execute if score #shicd {OBJ} matches 1.. run return 0',
        f'scoreboard players remove #sh {OBJ} {api.G2_HIT}',
        sset('#shicd', api.G2_HIT_ICD)])
    w('mantle/off', ['# The mantle state off (break, failure; @s = body): the gauge goes, the element badge comes back.',
                     f'tag @s remove {api.TAGS["mantle"]}', sset('#taken', 100)] + S.hud('clear') + [fn('el/badge')])
    w('mantle/break', [
        f'# G2 break (@s = body): the cocoon cracks and she drops (mantle_break {BREAK_LEN} t), then stunned {api.G2_STUN_T} t taking',
        f'# {api.G2_STUN_TAKEN_PCT} % damage; the player gets {api.G2_ENERGY} energy. The transition follows.',
        fn('mantle/off'), sset('#pat', BREAK_PAT), sset('#pt', 0), sset('#sh', 0), api.play('mantle_break')]
      + [f'execute at @s run {x}' if not x.startswith('execute') else x for x in S.snd('mantle_break')]
      + S.fx_plain('cocoon_crack', ['execute at @s run particle minecraft:end_rod ~ ~1.2 ~ 0.6 0.8 0.6 0.1 40 force @a[tag=player]'])
      + [f'scoreboard players set #enAdd tmp {api.G2_ENERGY * 100}',
         'execute as @a[tag=player,limit=1] run function rlk:char/energy_add', fn('hud/sub')])
    w('mantle/break_tick', [
        f'# G2 break + stun (#pat {BREAK_PAT}): clip, then the stun clip from {BREAK_LEN}; the transition at {STUN_END}.',
        f'scoreboard players add #pt {OBJ} 1',
        f'execute if score #pt {OBJ} matches {BREAK_LEN} run {api.play("stun")}',
        f'execute if score #pt {OBJ} matches {BREAK_LEN} run {sset("#stun", api.G2_STUN_T)}',
        f'execute if score #pt {OBJ} matches {BREAK_LEN} run {sset("#taken", api.G2_STUN_TAKEN_PCT)}',
        f'execute if score #stun {OBJ} matches 1.. run scoreboard players remove #stun {OBJ} 1',
        f'execute if score #pt {OBJ} matches {STUN_END}.. run {fn("mantle/end")}'])
    fail = [f'# G2 failure (@s = body; the time ran out): the nova (S4 p/mantle/nova: {NOVA_LEN} t tell, dash-dodgeable, '
            f'pl_dot {api.NOVA_PM} per mille, non-lethal);',
            '# without S4 the clip alone (no hazard). No stun. The transition follows.',
            fn('mantle/off'), sset('#pat', NOVA_PAT), sset('#pt', 0), sset('#done', 0)]
    fail += [fn('p/mantle/nova/start')] if nova else [api.play('mantle_nova')]
    w('mantle/fail', fail + [fn('hud/sub')])
    nt = [f'# G2 nova tick (#pat {NOVA_PAT}).', f'scoreboard players add #pt {OBJ} 1']
    nt += [fn('p/mantle/nova/tick')] if nova else [f'execute if score #pt {OBJ} matches {NOVA_LEN}.. run {sset("#done", 1)}']
    nt += [f'execute if score #done {OBJ} matches 1 run return run {fn("mantle/end")}',
           f'execute if score #pt {OBJ} matches {NOVA_LEN + 60}.. run {fn("mantle/end")}']
    w('mantle/nova_tick', nt)
    w('mantle/end', ['# The mantle is over (break + stun, or the nova): the transition of this phase step (M1 -> T1, M2 -> T2).',
                     sset('#stun', 0), sset('#taken', 100), fn('core/tr/start')])
    cancel = ['# Every mantle thing away (death, cleanup, tests; any executor): S4 feathers / nova, the state tag.']
    if ctx.has_s4('p/mantle/cancel'):
        cancel.append(fn('p/mantle/cancel'))
    if ctx.has_s4('p/mantle/nova/cancel'):
        cancel.append(fn('p/mantle/nova/cancel'))
    cancel += [f'tag @e[tag={api.TAGS["mantle"]}] remove {api.TAGS["mantle"]}', sset('#stun', 0)]
    w('mantle/cancel', cancel)
    w('mantle/reload', [
        '# /reload during the mantle (@s = body; the rig and every marker are new): the gauge and the time are kept, the',
        '# clip comes back; a break / stun goes on; a running nova (its markers are gone) ends: the transition.',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {api.play("mantle_hold")}',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {sset("#hud_g", -1)}',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {sset("#hud_c", -1)}',
        f'execute if score #pat {OBJ} matches {MANTLE_PAT} run {fn("mantle/badge9")}',
        f'execute if score #pat {OBJ} matches {BREAK_PAT} if score #pt {OBJ} matches {BREAK_LEN}.. run {api.play("stun")}',
        f'execute if score #pat {OBJ} matches {BREAK_PAT} if score #pt {OBJ} matches ..{BREAK_LEN - 1} run {api.play("mantle_break")}',
        f'execute if score #pat {OBJ} matches {NOVA_PAT} run {fn("mantle/end")}'])
    w('mantle/badge9', ['# The mantle badge again (reload).'] + badge_lines(9))
