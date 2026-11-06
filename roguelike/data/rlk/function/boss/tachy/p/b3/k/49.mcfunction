# B3 pattern tick 49
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzEl mb = #el tk
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:43,a:70,tell:1,dmg:29}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/b3
