# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 14
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:6,tell:28,damage:24,life:38}
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/rig/target_slam_spawn
execute if score @s rdTime matches 25 at @s rotated as @s run scoreboard players set @s rdAnim 15
execute if score @s rdTime matches 29 at @s rotated as @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.72 0.3
execute if score @s rdTime matches 43 at @s rotated as @s run scoreboard players set @s rdAnim 14
execute if score @s rdTime matches 43 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:6,tell:28,damage:24,life:38}
execute if score @s rdTime matches 43 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/rig/target_slam_spawn
execute if score @s rdTime matches 67 at @s rotated as @s run scoreboard players set @s rdAnim 15
execute if score @s rdTime matches 71 at @s rotated as @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.72 0.3
execute if score @s rdTime matches 83 at @s rotated as @s run function rlk:boss/raiden/finish
