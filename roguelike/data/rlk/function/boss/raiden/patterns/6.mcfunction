# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:20,damage:12,life:30}
execute if score @s rdTime matches 18 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 21 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 26 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 26 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:20,damage:12,life:30}
execute if score @s rdTime matches 43 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 46 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 51 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 51 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:20,damage:12,life:30}
execute if score @s rdTime matches 68 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 71 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 76 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 76 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:20,damage:12,life:30}
execute if score @s rdTime matches 93 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 96 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.3
execute if score @s rdTime matches 106 at @s rotated as @s run function rlk:boss/raiden/finish
