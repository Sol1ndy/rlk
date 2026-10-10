# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:26,damage:19,life:36}
execute if score @s rdTime matches 24 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 27 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 37 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 37 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 37 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 37 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:26,damage:19,life:36}
execute if score @s rdTime matches 60 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 63 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 74 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 74 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:24,damage:22,life:34}
execute if score @s rdTime matches 95 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 110 at @s rotated as @s run function rlk:boss/raiden/finish
