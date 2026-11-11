# Q pattern tick 94
execute if score #q_hit hr matches 1 run scoreboard players set #hzEl mb 3
execute if score #q_hit hr matches 1 run scoreboard players set #hzKB mb 3
execute if score #q_hit hr matches 1 run scoreboard players set #hzSfx mb 0
execute if score #q_hit hr matches 1 run scoreboard players set #hzQuiet mb 1
execute if score #q_hit hr matches 1 run scoreboard players set #hzNoParry mb 1
execute if score #q_hit hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] rotated as @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:24,tell:1,dmg:62}
execute if score #q_hit hr matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/q
