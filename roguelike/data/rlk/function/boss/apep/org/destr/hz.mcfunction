scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
function rlk:mboss/hz/disc {r:36,tell:61,dmg:67}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_ohz
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run scoreboard players operation @s apL = #apX mb
