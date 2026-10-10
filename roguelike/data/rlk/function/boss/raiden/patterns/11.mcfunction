# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:17,damage:19,life:27}
execute if score @s rdTime matches 15 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 18 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 25 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 25 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 25 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 25 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:17,damage:19,life:27}
execute if score @s rdTime matches 39 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 42 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 49 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 49 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:16,damage:22,life:26}
execute if score @s rdTime matches 62 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 73 at @s rotated as @s run function rlk:boss/raiden/finish
