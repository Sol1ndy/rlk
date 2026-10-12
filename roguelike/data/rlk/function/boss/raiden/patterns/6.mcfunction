# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/command
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:9,damage:12,life:19}
execute if score @s rdTime matches 7 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 10 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 14 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:9,damage:12,life:19}
execute if score @s rdTime matches 20 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 23 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 27 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 27 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:9,damage:12,life:19}
execute if score @s rdTime matches 33 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 36 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 40 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:9,damage:12,life:19}
execute if score @s rdTime matches 46 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 49 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 54 at @s rotated as @s run function rlk:boss/raiden/finish
