"""Bond of Life (생명의 계약) and 선혈의 충격 of 아를레키노 (PLAN §4, contract §3.5; OWNER: S3).

The player's bond is the existing `bol` score (F:player/bol/*; healing clears it through player/heal -> bol/absorb, the
HUD 「생명의 계약 N%」 is the player's own). This module only adds to it, reads it and, at the end of the fight, takes back
what she gave (#given, never more than is left), so a Clorinde / Arlecchino player keeps the bond of her own kit.

    bond/tick      every fight tick (@s = body): the landed bol hit (#mbHitBol; the FN-1 stand-in turns #mbHitEv on a
                   #bolw tick into it), #mbBolRe (250 % while her bond is on the player, else 100), the clear -> shock,
                   the DoT (BOL_DOT_PM per mille every BOL_DOT_T ticks, non-lethal, only after a bond she gave), the
                   shock hit resolve (#shk_hit, set by on_hit)
    bond/hit       a landed bol hit: + BOL_HIT % max HP to the bond, #bonded 1, her heal BOL_HEAL_PM per mille of mhpM
    bond/force     the forced bond (E70, F, Q5; api.BOND_CALLS, any executor): + BOL_FORCE %, no damage, no dodge, the
                   brand; skipped while the player is dead / reviving / on a selection screen / in the map; + bond/orbs
    bond/orbs      3 existing heal orbs (combat/heal_orb_spawn, 10 % each) 6-14 b from the centre, 120 deg apart, a random
                   bearing; tagged rlk_kn_orb (+ rlk_room rlk_mb_aux); older ones removed first (<= ORB_MAX alive)
    bond/shock     the shock hit: inside a break window (body tag rlk_kn_win) the break (core/break), else the 2 % burst
    bond/cleanup   min(bol, #given) taken back (player/bol/on_change only: no on_clear), the shock and the orbs gone

The removed mechanics (원거리 면역, 불 내성 70 %) do not exist anywhere: no projectile filter, no evasion, res {"*":10}.
"""
from . import api
from . import s3lib as S
from .s3lib import fn, sset

L, K = api.L, api.K
OBJ = api.OBJ
PL = '@a[tag=player,limit=1]'
SKIP = ('# skipped while the player is dead, reviving (로노바), on a selection screen or in the map (as the butterfly cocoon)',
        'execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0',
        'execute if entity @a[tag=player,scores={rnDie=1..}] run return 0',
        'execute if entity @a[tag=player,scores={pkMode=1..}] run return 0',
        'execute if entity @a[tag=player,scores={vMap=1..}] run return 0')


def true_lines(name, pm_score, comment):
    """core-side clamped true damage: #t kn = mhpM x <pm_score> / 1000, clamped so mhpC stays >= #mbFloor + 1."""
    return [f'# {comment} (@s = body): {name} = mhpM x per mille, clamped so mhpC stays >= the floor + 1 (true damage',
            '# ignores floors: the break never skips E70 / T and never kills).',
            f'scoreboard players operation #t {OBJ} = @s mhpM',
            f'execute if score #t {OBJ} matches 10000000.. run scoreboard players operation #t {OBJ} /= #c1000 {OBJ}',
            f'scoreboard players operation #t {OBJ} *= {pm_score} {OBJ}',
            f'execute if score @s mhpM matches ..9999999 run scoreboard players operation #t {OBJ} /= #c1000 {OBJ}',
            f'scoreboard players operation #t2 {OBJ} = @s mhpC',
            f'scoreboard players operation #t2 {OBJ} -= #mbFloor mb',
            f'scoreboard players remove #t2 {OBJ} 1',
            f'execute if score #mbFloor mb matches ..0 run scoreboard players operation #t2 {OBJ} = @s mhpC',
            f'execute if score #mbFloor mb matches ..0 run scoreboard players remove #t2 {OBJ} 1',
            f'scoreboard players operation #t {OBJ} < #t2 {OBJ}',
            f'execute if score #t {OBJ} matches ..0 run return 0',
            f'scoreboard players operation #mbTrue mb = #t {OBJ}',
            f'scoreboard players set #mbTrueEl mb {api.PYRO}',
            'function rlk:mboss/true_hit']


def build(W, ctx):
    w = W.w
    fn1 = api.fn1_ready()
    tick = ['# Bond of Life, every fight tick (@s = body; contract §3.5). First the events of the last tick (hazards strike after',
            '# the module tick): a landed bol hit, then the bond state, the DoT, the shock hit.']
    if not fn1:
        tick += ['# FN-1 stand-in (removed at I1): a hit that landed on a bol strike tick (#bolw, set by the pattern) is a bol hit.',
                 f'execute if score #bolw {OBJ} matches 1 if score #mbHitEv mb matches 1.. run scoreboard players set #mbHitBol mb {api.BOL_HIT}',
                 sset('#bolw', 0)]
    tick += [f'scoreboard players operation #hitev {OBJ} = #mbHitEv mb',
             'scoreboard players set #mbHitEv mb 0',
             f'execute if score #mbHitBol mb matches 1.. run {fn("bond/hit")}',
             f'execute store result score #pbol {OBJ} run scoreboard players get {PL} bol',
             f'execute if score #bonded {OBJ} matches 1 if score #pbol {OBJ} matches ..0 run {fn("bond/cleared")}',
             f'scoreboard players set #mbBolRe mb 100',
             f'execute if score #bonded {OBJ} matches 1 if score #pbol {OBJ} matches 1.. run scoreboard players set #mbBolRe mb {api.BOL_REHIT_PCT}',
             f'execute if score #bonded {OBJ} matches 1 if score #pbol {OBJ} matches 1.. run {fn("bond/dot")}',
             f'execute if score #shk_hit {OBJ} matches 1 run {fn("bond/shock")}']
    w('bond/tick', tick)
    w('bond/dot', [f'# The bond DoT (@s = body; only while HER bond is on the player): {api.BOL_DOT_PM} per mille every {api.BOL_DOT_T} t,',
                   '# Pyro (the element shield absorbs as usual), never lethal (pl_dot leaves 1 HP).',
                   f'scoreboard players add #dot_t {OBJ} 1',
                   f'execute if score #dot_t {OBJ} matches ..{api.BOL_DOT_T - 1} run return 0',
                   sset('#dot_t', 0)]
      + L.pl_dot(api.BOL_DOT_PM, api.PYRO, lethal=0)
      + S.placed(S.snd('bond_tick'), f'at {S.PLAYER}'))
    w('bond/hit', ['# A landed Bond-of-Life hit (@s = body; #mbHitBol mb = the FN-1 option value, % max HP): the bond grows, she heals.',
                   'scoreboard players operation #bolPct tmp = #mbHitBol mb',
                   'scoreboard players set #mbHitBol mb 0',
                   f'execute as {PL} run {fn("bond/add")}',
                   fn('bond/heal_her')]
      + S.placed(S.snd('bond_gain'), f'at {S.PLAYER}'))
    w('bond/add', ['# @s = the player, #bolPct tmp = % of max HP: the existing bond add (capped at #bolMax), the amount she added in',
                   '# #given (she takes back at most that at the end), her bond flag.',
                   'execute unless score @s bol matches 0.. run scoreboard players set @s bol 0',
                   f'scoreboard players operation #t {OBJ} = @s bol',
                   'function rlk:player/bol/add_pct',
                   f'scoreboard players operation #t2 {OBJ} = @s bol',
                   f'scoreboard players operation #t2 {OBJ} -= #t {OBJ}',
                   f'execute if score #t2 {OBJ} matches 1.. run scoreboard players operation #given {OBJ} += #t2 {OBJ}',
                   sset('#bonded', 1)])
    w('bond/heal_her', [f'# Her heal per landed bol hit (@s = body): {api.BOL_HEAL_PM} per mille of the phase pool, capped at mhpM.',
                        f'scoreboard players operation #t {OBJ} = @s mhpM',
                        f'execute if score #t {OBJ} matches 10000000.. run scoreboard players operation #t {OBJ} /= #c1000 {OBJ}',
                        f'scoreboard players set #t2 {OBJ} {api.BOL_HEAL_PM}',
                        f'scoreboard players operation #t {OBJ} *= #t2 {OBJ}',
                        f'execute if score @s mhpM matches ..9999999 run scoreboard players operation #t {OBJ} /= #c1000 {OBJ}',
                        f'scoreboard players operation @s mhpC += #t {OBJ}',
                        'execute if score @s mhpC > @s mhpM run scoreboard players operation @s mhpC = @s mhpM']
      + S.fx('embers_puff', [S.part(S.DUST[2], 0.4, 0.9, 0.4, 0, 18)], pos=f'at @s positioned ~ ~{S.H(1.4)} ~'))
    w('bond/force', ['# The forced bond (api.BOND_CALLS force; E70 / F1 / Q5 at their brand tick; any executor): '
                     f'+{api.BOL_FORCE} % max HP, no damage, no', '# dodge; the brand X and the red flash on the player; the heal orbs.']
      + list(SKIP)
      + [f'scoreboard players set #bolPct tmp {api.BOL_FORCE}',
         f'execute as {PL} run {fn("bond/add")}']
      + S.fx('brand_x', [S.part(S.DUST[2], 0.3, 0.5, 0.3, 0, 40), S.part('minecraft:crimson_spore', 0.4, 0.6, 0.4, 0, 30)],
             pos=f'at {S.PLAYER} positioned ~ ~1 ~')
      + S.placed(S.snd('brand') + S.snd('bond_gain'), f'at {S.PLAYER}')
      + [fn('bond/orbs')])
    # heal orbs
    w('bond/orbs', [f'# {api.ORBS} heal orbs (any executor; the existing 회복구슬, #orbHealPct each): {L.num(api.ORB_R[0])}-'
                    f'{L.num(api.ORB_R[1])} b from the arena centre,',
                    f'# 120 deg apart from a random bearing; the older ones go first (<= {api.ORB_MAX} alive).',
                    'kill @e[type=minecraft:item,tag=rlk_kn_orb]',
                    f'execute store result score #t {OBJ} run random value 0..359']
      + [ln for k in range(api.ORBS) for ln in (
          f'execute store result storage {api.STORAGE} core.orb.a int 1 run scoreboard players get #t {OBJ}',
          f'execute store result storage {api.STORAGE} core.orb.r double 0.1 run random value '
          f'{int(api.ORB_R[0] * 10)}..{int(api.ORB_R[1] * 10)}',
          f'function {api.NS}bond/orb_at with storage {api.STORAGE} core.orb',
          f'scoreboard players add #t {OBJ} {360 // api.ORBS}')]
      + [f'execute store result score #orbs {OBJ} if entity @e[type=minecraft:item,tag=rlk_kn_orb]'])
    w('bond/orb_at', ['# $(a) bearing, $(r) radius (blocks): one heal orb there, on the floor of the arena (as the arena marker).',
                      f'$execute at {S.ARENA_M} positioned ~ {api.CY} ~ rotated $(a) 0 positioned ^ ^ ^$(r) run function {api.NS}bond/orb_one'])
    w('bond/orb_one', ['# One heal orb here (the existing combat/heal_orb_spawn), tagged as hers.',
                       'function rlk:combat/heal_orb_spawn',
                       'tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_mb_aux',
                       'tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_room',
                       'tag @e[type=minecraft:item,tag=rlk_healorb,tag=!rlk_kn_orb,distance=..2] add rlk_kn_orb']
      + S.snd('orb_spawn'))
    # clear -> shock
    w('bond/cleared', ['# Her bond is gone from the player (bol 0 by any heal; @s any): 선혈의 충격 armed (one at a time, kept until',
                       '# used or the fight ends), the badge on the boss bar.',
                       sset('#bonded', 0), sset('#given', 0), sset('#dot_t', 0), sset('#shock', 1)]
      + S.fx('shock_gain', [S.part('minecraft:enchanted_hit', 0.4, 0.8, 0.4, 0.1, 20), S.part(S.DUST[2], 0.3, 0.8, 0.3, 0, 16)],
             pos=f'at {S.PLAYER} positioned ~ ~1 ~')
      + S.placed(S.snd('shock_gain'), f'at {S.PLAYER}')
      + [fn('hud/sub')])
    w('bond/shock', ['# A normal-attack hit landed while 선혈의 충격 is armed (#shk_hit, set by on_hit; @s = body): inside a break',
                     '# window the break (core/break), else the crimson burst; the shock is spent either way.',
                     sset('#shk_hit', 0),
                     f'execute unless score #shock {OBJ} matches 1 run return 0',
                     sset('#shock', 0),
                     f'execute if entity @s[tag={api.TAGS["win"]}] run return run {fn("core/break")}',
                     fn('bond/burst'),
                     f'execute if score #mbSt mb matches 1 run {fn("hud/sub")}'])
    w('bond/burst', [f'# 선혈의 충격 outside a window (@s = body): the crimson burst + true {api.SHOCK_BONUS_PCT} % of the pool (clamped).',
                     sset('#t3', api.SHOCK_BONUS_PCT * 10)]
      + S.fx('shock_hit', [S.part(S.DUST[2], 0.6, 1.0, 0.6, 0, 40), S.part('minecraft:explosion', 0.2, 0.3, 0.2, 0, 1)],
             pos=f'at @s positioned ~ ~{S.H(1.4)} ~')
      + S.placed(S.snd('shock_hit'), 'at @s')
      + [fn('bond/true')])
    w('bond/true', true_lines('the shock burst', '#t3', 'True damage of #t3 per mille'))
    w('bond/cleanup', ['# The end of the fight (cleanup / won / cancel / defeat; any executor): what she bonded is taken back',
                       '# (min(bol, #given): a Clorinde / Arlecchino player keeps the bond of her own kit; no on_clear hooks), the',
                       '# shock and her heal orbs are gone.',
                       f'execute as {PL} run {fn("bond/remove")}',
                       sset('#given', 0), sset('#bonded', 0), sset('#shock', 0), sset('#shk_hit', 0), sset('#dot_t', 0),
                       'scoreboard players set #mbBolRe mb 100', 'scoreboard players set #mbHitBol mb 0',
                       'kill @e[type=minecraft:item,tag=rlk_kn_orb]'])
    w('bond/remove', ['# @s = the player: bol -= min(bol, #given); the value-change hooks only (no clear hooks).',
                      'execute unless score @s bol matches 1.. run return 0',
                      f'scoreboard players operation #t {OBJ} = @s bol',
                      f'execute if score #t {OBJ} > #given {OBJ} run scoreboard players operation #t {OBJ} = #given {OBJ}',
                      f'execute if score #t {OBJ} matches ..0 run return 0',
                      f'scoreboard players operation @s bol -= #t {OBJ}',
                      'function rlk:player/bol/on_change'])
