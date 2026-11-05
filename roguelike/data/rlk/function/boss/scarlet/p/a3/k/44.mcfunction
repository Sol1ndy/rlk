# A3 pattern tick 44
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:40,a:50,tell:1,dmg:29}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a3
