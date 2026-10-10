# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 12
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:7,tell:28,damage:25,life:38}
execute if score @s rdTime matches 26 at @s rotated as @s run scoreboard players set @s rdAnim 13
execute if score @s rdTime matches 29 at @s rotated as @s run playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 1 0.65 0.3
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/finish
