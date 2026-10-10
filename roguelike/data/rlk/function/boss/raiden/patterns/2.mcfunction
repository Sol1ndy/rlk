# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:20,damage:10,life:30}
execute if score @s rdTime matches 18 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 21 at @s rotated as @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.72 0.3
execute if score @s rdTime matches 27 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 27 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 27 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 27 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:20,damage:10,life:30}
execute if score @s rdTime matches 44 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 47 at @s rotated as @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.72 0.3
execute if score @s rdTime matches 53 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 53 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 53 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 53 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:20,damage:10,life:30}
execute if score @s rdTime matches 70 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 73 at @s rotated as @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.72 0.3
execute if score @s rdTime matches 80 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 80 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:9,tell:22,damage:13,life:32}
execute if score @s rdTime matches 99 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 112 at @s rotated as @s run function rlk:boss/raiden/finish
