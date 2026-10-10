# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:14,damage:12,life:24}
execute if score @s rdTime matches 12 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 15 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 20 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:14,damage:12,life:24}
execute if score @s rdTime matches 31 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 34 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 39 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 39 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:14,damage:12,life:24}
execute if score @s rdTime matches 50 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 53 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 58 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 58 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:14,damage:12,life:24}
execute if score @s rdTime matches 69 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 72 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 80 at @s rotated as @s run function rlk:boss/raiden/finish
