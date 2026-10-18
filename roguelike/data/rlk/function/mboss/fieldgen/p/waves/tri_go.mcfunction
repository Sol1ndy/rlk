# The two extra fronts of the 3rd wave (9 and 18 t after its first).
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 211
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:49,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 211
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:58,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
