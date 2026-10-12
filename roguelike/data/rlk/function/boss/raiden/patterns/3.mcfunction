# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/noemyeong
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 21
execute if score @s rdTime matches 1 at @s rotated as @s run playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.3
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/movement/blink_start
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:2,tell:12,damage:16,life:22}
execute if score @s rdTime matches 19 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 22 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.1 0.65 0.3
execute if score @s rdTime matches 28 at @s rotated as @s run function rlk:boss/raiden/movement/blink_start
execute if score @s rdTime matches 37 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 37 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 37 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 37 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:15,life:22}
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdAnim 4
execute if score @s rdTime matches 56 at @s rotated as @s run function rlk:boss/raiden/finish
