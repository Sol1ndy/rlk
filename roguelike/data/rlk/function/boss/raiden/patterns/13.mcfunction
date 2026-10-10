# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 14
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:6,tell:12,damage:24,life:22}
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/rig/target_slam_spawn
execute if score @s rdTime matches 9 at @s rotated as @s run scoreboard players set @s rdAnim 15
execute if score @s rdTime matches 13 at @s rotated as @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.72 0.3
execute if score @s rdTime matches 19 at @s rotated as @s run scoreboard players set @s rdAnim 14
execute if score @s rdTime matches 19 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:6,tell:12,damage:24,life:22}
execute if score @s rdTime matches 19 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/rig/target_slam_spawn
execute if score @s rdTime matches 27 at @s rotated as @s run scoreboard players set @s rdAnim 15
execute if score @s rdTime matches 31 at @s rotated as @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.72 0.3
execute if score @s rdTime matches 43 at @s rotated as @s run function rlk:boss/raiden/finish
