# 선혈의 충격 inside a break window (bond/shock, test 24; @s = body): the Banquet is cancelled (hazards, decals,
# props, banner), true damage of the pool (P1 150 / P2 125 per mille, clamped above the
# floor), the stagger clip brk (20 t) then the stun clip for 140 t (AI paused, no damage multiplier).
scoreboard players operation #brk kn = #pat kn
function rlk:boss/arlecchino/core/cancel_d
function rlk:boss/arlecchino/core/win_off
scoreboard players set #pat kn 0
scoreboard players set #done kn 0
scoreboard players set #t3 kn 150
execute if score #ph kn matches 5 run scoreboard players set #t3 kn 125
function rlk:boss/arlecchino/bond/true
execute unless score #mbSt mb matches 1 run return 0
execute at @s positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/break_burst
execute at @s run function rlk:boss/arlecchino/fx/snd/break
function rlk:boss/arlecchino/core/stun_start
