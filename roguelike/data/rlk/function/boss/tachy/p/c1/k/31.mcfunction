# C1 pattern tick 31
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzEl mb = #el tk
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:42,tell:1,dmg:100}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/c1
