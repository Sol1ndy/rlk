# The nova hazard (strikes next tick).
scoreboard players set #hzEl mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzPm mb 400
scoreboard players set #hzPmL mb 0
execute at @s rotated 0 0 positioned ~ 201 ~ run function rlk:mboss/hz/full {tell:1,dmg:1}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/p/mantle/hz_tag
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_tk_nova
