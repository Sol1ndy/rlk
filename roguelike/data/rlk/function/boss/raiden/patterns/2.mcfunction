# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:13,damage:10,life:23}
execute if score @s rdTime matches 11 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 14 at @s rotated as @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.72 0.3
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 20 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:13,damage:10,life:23}
execute if score @s rdTime matches 30 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 33 at @s rotated as @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.72 0.3
execute if score @s rdTime matches 39 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 39 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 39 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 39 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:13,damage:10,life:23}
execute if score @s rdTime matches 49 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 52 at @s rotated as @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.72 0.3
execute if score @s rdTime matches 58 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 58 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:9,tell:14,damage:13,life:24}
execute if score @s rdTime matches 69 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 80 at @s rotated as @s run function rlk:boss/raiden/finish
