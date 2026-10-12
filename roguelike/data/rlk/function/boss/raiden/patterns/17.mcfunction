# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/goemyeol
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:9,tell:14,damage:17,life:24}
execute if score @s rdTime matches 12 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 15 at @s rotated as @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 20 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:10,tell:14,damage:21,life:24}
execute if score @s rdTime matches 31 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 41 at @s rotated as @s run function rlk:boss/raiden/finish
