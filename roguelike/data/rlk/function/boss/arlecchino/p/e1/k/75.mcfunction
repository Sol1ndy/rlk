# E1 pattern tick 75
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:52,a:90,tell:1,dmg:36}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/e1
