# RINGS pattern tick 43
execute if score #ph hr matches 1 run scoreboard players set #hzEl mb 3
execute if score #ph hr matches 1 run scoreboard players set #hzKB mb 3
execute if score #ph hr matches 1 run scoreboard players set #hzSfx mb 0
execute if score #ph hr matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #ph hr matches 1 run scoreboard players set #hzNoParry mb 0
execute if score #ph hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:26,tell:1,dmg:42}
execute if score #ph hr matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/rings
execute if score #ph hr matches 7 run scoreboard players set #hzEl mb 3
execute if score #ph hr matches 7 run scoreboard players set #hzKB mb 0
execute if score #ph hr matches 7 run scoreboard players set #hzSfx mb 0
execute if score #ph hr matches 7 run scoreboard players set #hzQuiet mb 1
execute if score #ph hr matches 7 run scoreboard players set #hzNoParry mb 0
execute if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:26,tell:1,dmg:31}
execute if score #ph hr matches 7 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/rings
