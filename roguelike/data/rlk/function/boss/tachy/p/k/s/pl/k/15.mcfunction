# K stage pl tick 15
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzEl mb 3
execute rotated as @s rotated ~ 0 at @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:35,tell:1,dmg:170}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/k
