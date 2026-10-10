# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:8,damage:9,life:18}
execute if score @s rdTime matches 6 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 9 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 14 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:8,damage:9,life:18}
execute if score @s rdTime matches 19 at @s rotated as @s run scoreboard players set @s rdAnim 4
execute if score @s rdTime matches 22 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 27 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 27 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 27 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 27 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:8,damage:9,life:18}
execute if score @s rdTime matches 32 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 35 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 40 at @s rotated as @s run scoreboard players set @s rdAnim 20
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:9,damage:14,life:19}
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdAnim 4
execute if score @s rdTime matches 55 at @s rotated as @s run function rlk:boss/raiden/finish
