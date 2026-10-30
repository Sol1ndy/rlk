scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
function rlk:mboss/hz/disc {r:36,tell:10,dmg:35}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_ohz
