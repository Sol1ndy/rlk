scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
function rlk:mboss/hz/sector {r:26,a:24,tell:10,dmg:47}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_ohz
