# The feather's hit on the floor here (strikes in 16 t).
scoreboard players set #hzEl mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute rotated 0 0 run function rlk:mboss/hz/disc {r:18,tell:16,dmg:29}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/p/mantle/hz_tag
