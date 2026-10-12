# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/pierce
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:5,tell:14,damage:22,life:24}
execute if score @s rdTime matches 15 at @s rotated as @s run scoreboard players set @s rdAnim 21
execute if score @s rdTime matches 15 at @s rotated as @s run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 15..26 at @s rotated as @s positioned ^ ^ ^0.75 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] run tp @s ~ ~ ~
execute if score @s rdTime matches 29 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 29 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 29 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 29 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:13,damage:19,life:23}
execute if score @s rdTime matches 39 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 42 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.62 0.3
execute if score @s rdTime matches 46 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 46 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:12,damage:19,life:22}
execute if score @s rdTime matches 55 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 58 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.3
execute if score @s rdTime matches 65 at @s rotated as @s run function rlk:boss/raiden/finish
