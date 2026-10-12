# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/cleave_all
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:11,damage:19,life:21}
execute if score @s rdTime matches 9 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 12 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 17 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 17 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 17 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 17 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:11,damage:19,life:21}
execute if score @s rdTime matches 25 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 28 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 33 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 33 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:22,life:20}
execute if score @s rdTime matches 40 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 50 at @s rotated as @s run function rlk:boss/raiden/finish
