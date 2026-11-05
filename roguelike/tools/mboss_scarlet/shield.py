"""The 5-pip shield, the judge and the two fail hits of 홍련 (PLAN §5; OWNER: S3; the S4 gauntlets call it through
api.shield()): shield/arm, shield/cut {s}, shield/tick (the core's per-tick pip check), shield/judge, ult/fail60,
ult/fatal, shield/off, and the under bar (hud/bar_shield: #buSub = pips, #buSubMax 5, colour api.BU_SHIELD).

Semantics (contract §3.6, PLAN §5.1, question 6 default PIP_RULE 'timed_dash'):
- shield/arm (any executor): #pips hr = api.PIPS (5), the under bar on (#shb 1), #gres 0, every pending pip window gone.
  The core calls it at SQ1 tick 0 and at a lead-in's refill beat (#sq_sig refill); a gauntlet never needs to.
- shield/cut {s} (@s / position = the cut marker at its lock): registers one counting cut whose strike is pattern tick s
  (#pt hr of the running gauntlet) and stores its lock point: a marker rlk_hr_pip there (objective hr = s). At #pt = s a
  pip goes when the player's dashInvT is 1..6, at #pt = s + 1 when it is 1..5 (api.PIP_DASH: a dash started by s), and
  the player's feet are within api.PIP_R (6.2 b) of the lock point; whatever the dash direction; one pip per cut; never
  below 0; kit pip_break at the player + its sound. The window closes after s + 1. Discs, the dive and uncounted cuts
  (api.cut count 0) never call it.
- shield/tick: run by the core every tick of a gauntlet, right after p/<g>/tick (the cut's own lock / strike already ran).
- shield/judge (@s any): the pip windows close, the under bar goes; #gres hr = 1 (deflect: #pips 0) or 2 (fail). The
  deflect staging is played here (kit clash_gold + light_column at the player, the deflect sound, the body's g_deflect
  clip); the fail branch is the gauntlet's (A8: ult/fail60 + g_reform; A13: the FAIL5_T staging + ult/fatal).
- ult/fail60 (position = the impact point): mboss/pl_dot api.FAIL60_PM per mille of the player's max HP, Electro,
  #mbDotLethal 0 (never kills), the push ring mboss_lib.push_ring(*api.FAIL60_PUSH) there in the same tick, the impact
  effects (kit dive_impact {r:30} + light_column) and the fail_impact sound.
- ult/fatal (@s = the player; F:boss/raiden/hazard/fatal's model): nothing while the player is reviving (rnDie >= 1);
  else player/hurt_do with all current HP (Electro), curHealth 0, player/die: it bypasses mboss/hurt, so dash i-frames and
  every shield are ignored; Ronova's one revive still applies (player/die); a death in a test ends in mboss/test/defeat
  (player/hook_respawn).
- shield/off (any executor): #pips 0, the under bar and every pip window gone (cleanup, death, a cancelled gauntlet).
"""
from . import api
from . import s3lib as S
from .s3lib import sset, fn, part

L, K = api.L, api.K
OBJ = api.OBJ
PIP_T = 'rlk_hr_pip'
PIP_M = f'@e[type=minecraft:marker,tag={PIP_T}]'


def build(W):
    w = W.w
    d0, d1 = api.PIP_DASH[0], api.PIP_DASH[1]
    r = L.num(api.PIP_R, 2)
    w('shield/arm', ['# The shield full (api.PIPS) and its under bar on; pending pip windows and the last judge result gone.',
                     sset('#pips', api.PIPS), sset('#shb', 1), sset('#gres', 0), f'kill {PIP_M}'])
    w('shield/off', ['# The shield off: no pips, no under bar, no pip window (cleanup, death, a cancelled gauntlet).',
                     sset('#pips', 0), sset('#shb', 0), f'kill {PIP_M}'])
    w('shield/cut', [
        '# {s}: a counting cut (@s / position = its marker at the lock point; S4 g/cut/lock): the pip window of strike tick s on',
        '# the gauntlet clock #pt hr, at this lock point (a marker rlk_hr_pip, objective hr = s).',
        f'execute if entity @s[tag={api.TAGS["cut"]}] at @s run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(PIP_T, "rlk_hr_pipnew")}}}',
        f'execute unless entity @s[tag={api.TAGS["cut"]}] run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(PIP_T, "rlk_hr_pipnew")}}}',
        f'$scoreboard players set @e[type=minecraft:marker,tag=rlk_hr_pipnew] {OBJ} $(s)',
        'tag @e[type=minecraft:marker,tag=rlk_hr_pipnew] remove rlk_hr_pipnew'])
    w('shield/tick', ['# Every gauntlet tick after p/<g>/tick (the core): each open pip window (@s = its marker, at the lock point).',
                      f'execute as {PIP_M} at @s run {fn("shield/pip")}'])
    w('shield/pip', [
        f'# @s = a pip window (objective hr = its strike tick s), at its lock point. #pt = s: dashInvT {d0[0]}..{d0[1]}; #pt = s + 1:',
        f'# dashInvT {d1[0]}..{d1[1]} (a dash started by s); the player\'s feet within {r} b. One pip per cut; closed after s + 1.',
        f'scoreboard players operation #t {OBJ} = @s {OBJ}',
        f'scoreboard players operation #t {OBJ} -= #pt {OBJ}',
        f'execute if score #t {OBJ} matches 1.. run return 0',
        f'execute if score #t {OBJ} matches ..-2 run return run kill @s',
        f'execute if score #pipoff {OBJ} matches 1 if score #t {OBJ} matches -1 run return run kill @s',
        f'execute if score #pipoff {OBJ} matches 1 run return 0',
        f'execute if score #t {OBJ} matches 0 if entity @a[tag=player,scores={{dashInvT={d0[0]}..{d0[1]}}},limit=1] if entity '
        f'{S.PLAYER[:-1]},distance=..{r}] run return run {fn("shield/take")}',
        f'execute if score #t {OBJ} matches -1 if entity @a[tag=player,scores={{dashInvT={d1[0]}..{d1[1]}}},limit=1] if entity '
        f'{S.PLAYER[:-1]},distance=..{r}] run return run {fn("shield/take")}',
        f'execute if score #t {OBJ} matches -1 run kill @s'])
    w('shield/take', ['# A pip goes (@s = the window, closed now): one segment of the under bar, the shards and the crack at the player.',
                      'kill @s',
                      f'execute if score #pips {OBJ} matches ..0 run return 0',
                      f'scoreboard players remove #pips {OBJ} 1']
      + S.fx('pip_break', [part(S.DUST['lilac'], 0.4, 0.5, 0.4, 0.1, 14), part('minecraft:end_rod', 0.3, 0.4, 0.3, 0.06, 6)],
             pos=f'at {S.PLAYER} positioned ~ ~1.1 ~')
      + S.snd('pip_break', pos=f'at {S.PLAYER}'))
    w('shield/judge', [
        '# The judge (the final dive\'s contact; S4 at api.JUDGE_T): the pip windows close and the under bar goes; #gres hr 1 =',
        '# deflect (the shield empty: the gold starburst + light column at the player, the deflect sound, g_deflect), 2 = fail',
        '# (the gauntlet\'s own branch follows).',
        f'kill {PIP_M}', sset('#shb', 0),
        f'execute if score #pips {OBJ} matches 1.. run return run {sset("#gres", 2)}',
        sset('#gres', 1)]
      + S.fx('clash_gold', [part('minecraft:end_rod', 0.4, 0.4, 0.4, 0.15, 24), part(S.DUST['yellow'], 0.3, 0.3, 0.3, 0, 12)],
             pos=f'at {S.PLAYER} positioned ~ ~1.3 ~')
      + S.fx('light_column', [part('minecraft:end_rod', 0.1, 1.6, 0.1, 0.02, 16)], pos=f'at {S.PLAYER}')
      + S.snd('deflect', pos=f'at {S.PLAYER}')
      + [f'execute as {S.BODY} at @s run {api.play("g_deflect")}'])
    w('ult/fail60', [
        f'# The 60 % fail hit (ULT60_LETHAL false; position = the impact point, the dive on the player): {api.FAIL60_PM} per mille',
        '# of the player\'s max HP through mboss/pl_dot (no dodge, no position check: the failed judge is the hit; #mbDotLethal 0:',
        '# it never kills), the push ring in the same tick (pl_dot has no knockback), the impact effects and sound.']
      + L.pl_dot(api.FAIL60_PM, api.ELEC, 0)
      + [L.push_ring(*api.FAIL60_PUSH)]
      + S.fx('dive_impact', [part(S.DUST['lilac'], 1.2, 0.1, 1.2, 0, 30)], pos='positioned ~ ~0.1 ~', r=30)
      + S.fx('light_column', [part('minecraft:end_rod', 0.1, 1.6, 0.1, 0.02, 16)], pos='positioned ~ ~ ~')
      + S.snd('fail_impact', pos='positioned ~ ~ ~'))
    w('ult/fatal', [
        '# The 5 % instant death (ULT5_LETHAL true; @s = the player; F:boss/raiden/hazard/fatal\'s model): skipped while the player',
        '# revives; else all current HP as the hit (the number, Electro), curHealth 0, player/die. It bypasses mboss/hurt (dash',
        '# i-frames and every shield are ignored); Ronova\'s one revive still applies; in a test the death ends in test/defeat.',
        'execute if score @s rnDie matches 1.. run return 0',
        'scoreboard players operation #hurtDmg tmp = @s curHealth',
        f'scoreboard players set #elem tmp {api.ELEC}',
        'function rlk:player/hurt_do',
        'scoreboard players set @s curHealth 0',
        'function rlk:player/die'])
    w('hud/bar_shield', ['# The under bar = the shield (bars hook): pips left of 5, electro.',
                         f'scoreboard players operation #buSub bu = #pips {OBJ}',
                         f'scoreboard players set #buSubMax bu {api.PIPS}', f'scoreboard players set #buSubCol bu {api.BU_SHIELD}'])
