# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/will
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 20
execute if score @s rdTime matches 1 at @s rotated as @s run playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.3
execute if score @s rdTime matches 4 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 4 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 4 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:13,tell:12,damage:10,life:22}
execute if score @s rdTime matches 16 at @s rotated as @s run execute as @e[tag=rlk_rd_hazard,scores={rdShape=13,rdHAge=11},limit=1] at @s run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdTime matches 16 at @s rotated as @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.8 1.25 0.3
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 10 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:13,tell:12,damage:10,life:22}
execute if score @s rdTime matches 22 at @s rotated as @s run execute as @e[tag=rlk_rd_hazard,scores={rdShape=13,rdHAge=11},limit=1] at @s run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdTime matches 22 at @s rotated as @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.8 1.25 0.3
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 16 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:13,tell:12,damage:10,life:22}
execute if score @s rdTime matches 28 at @s rotated as @s run execute as @e[tag=rlk_rd_hazard,scores={rdShape=13,rdHAge=11},limit=1] at @s run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdTime matches 28 at @s rotated as @s run playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.8 1.25 0.3
execute if score @s rdTime matches 32 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 32 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 32 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 32 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:10,tell:14,damage:18,life:24}
execute if score @s rdTime matches 43 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdTime matches 46 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.2 0.6 0.3
execute if score @s rdTime matches 54 at @s rotated as @s run function rlk:boss/raiden/finish
