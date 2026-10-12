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
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 40 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:10,damage:15,life:20}
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:12,life:20}
execute if score @s rdTime matches 47 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 50 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.9 0.75 0.3
execute if score @s rdTime matches 50 at @s rotated as @s run playsound minecraft:item.trident.hit_ground hostile @a[tag=player] ~ ~ ~ 1 0.6 0.3
execute if score @s rdTime matches 52 store result score #rdFollow rd run random value 0..1
execute if score @s rdTime matches 56 if score #rdFollow rd matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 56 if score #rdFollow rd matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 56 if score #rdFollow rd matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 56 if score #rdFollow rd matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:13,tell:8,damage:12,life:18}
execute if score @s rdTime matches 61 if score #rdFollow rd matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 64 if score #rdFollow rd matches 1 at @s rotated as @s run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdTime matches 64 if score #rdFollow rd matches 1 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.1 0.9 0.3
execute if score @s rdTime matches 58 if score #rdFollow rd matches 0 at @s rotated as @s run function rlk:boss/raiden/finish
execute if score @s rdTime matches 70 if score #rdFollow rd matches 1 at @s rotated as @s run function rlk:boss/raiden/finish
