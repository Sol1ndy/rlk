# combo #apPT 4
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 18
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/hz/sector {r:72,a:78,tell:10,dmg:55}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p6
