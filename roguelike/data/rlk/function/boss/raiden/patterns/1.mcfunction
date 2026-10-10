# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:9,life:22}
execute if score @s rdTime matches 10 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 13 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 19 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 19 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 19 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 19 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:9,life:22}
execute if score @s rdTime matches 28 at @s rotated as @s run scoreboard players set @s rdAnim 4
execute if score @s rdTime matches 31 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 37 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 37 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 37 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 37 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:9,life:22}
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 49 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 55 at @s rotated as @s run scoreboard players set @s rdAnim 20
execute if score @s rdTime matches 55 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:13,damage:14,life:23}
execute if score @s rdTime matches 65 at @s rotated as @s run scoreboard players set @s rdAnim 4
execute if score @s rdTime matches 76 at @s rotated as @s run function rlk:boss/raiden/finish
