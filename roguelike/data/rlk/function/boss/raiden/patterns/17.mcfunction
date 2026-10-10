# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:9,tell:24,damage:17,life:34}
execute if score @s rdTime matches 22 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 25 at @s rotated as @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 40 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:10,tell:24,damage:21,life:34}
execute if score @s rdTime matches 61 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 76 at @s rotated as @s run function rlk:boss/raiden/finish
