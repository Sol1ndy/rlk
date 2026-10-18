# waves clock 135
function rlk:mboss/fieldgen/p/waves/tri
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 211
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:40,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
execute if score #fq21T mb matches 1 run function rlk:mboss/fieldgen/p/waves/tri_go
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
function rlk:mboss/fieldgen/p/waves/charge
playsound minecraft:block.respawn_anchor.ambient hostile @a[tag=player] ~ ~ ~ 0.9 1.4 0.3
