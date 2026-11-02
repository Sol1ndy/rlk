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
execute at @s positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1 1.2 1 0 60 force @a[tag=player]
execute at @s positioned ~ ~1.4 ~ run particle minecraft:explosion ~ ~ ~ 0.4 0.4 0.4 0 2 force @a[tag=player]
execute at @s run playsound minecraft:entity.wither.break_block hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
function rlk:boss/arlecchino/core/stun_start
