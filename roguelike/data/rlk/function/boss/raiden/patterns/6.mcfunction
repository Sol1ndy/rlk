# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/command
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:13,damage:12,life:23}
execute if score @s rdTime matches 11 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 14 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 18 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 18 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:13,damage:12,life:23}
execute if score @s rdTime matches 28 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 31 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 35 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 35 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:13,damage:12,life:23}
execute if score @s rdTime matches 45 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 48 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 52 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 52 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:13,damage:12,life:23}
execute if score @s rdTime matches 62 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 65 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 70 at @s rotated as @s run function rlk:boss/raiden/finish
