# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:9,life:22}
execute if score @s rdTime matches 10 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 13 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 18 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 18 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 18 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 18 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:9,life:22}
execute if score @s rdTime matches 27 at @s rotated as @s run scoreboard players set @s rdAnim 4
execute if score @s rdTime matches 30 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 35 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 35 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 35 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 35 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:1,tell:12,damage:9,life:22}
execute if score @s rdTime matches 44 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 47 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
execute if score @s rdTime matches 52 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 52 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 52 at @s rotated as @s run scoreboard players set @s rdAnim 5
execute if score @s rdTime matches 52 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:14,damage:15,life:24}
execute if score @s rdTime matches 52 at @s rotated as @s run execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:3,tell:14,damage:12,life:24}
execute if score @s rdTime matches 63 at @s rotated as @s run scoreboard players set @s rdAnim 6
execute if score @s rdTime matches 66 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.9 0.75 0.3
execute if score @s rdTime matches 66 at @s rotated as @s run playsound minecraft:item.trident.hit_ground hostile @a[tag=player] ~ ~ ~ 1 0.6 0.3
execute if score @s rdTime matches 68 store result score #rdFollow rd run random value 0..1
execute if score @s rdTime matches 72 if score #rdFollow rd matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 72 if score #rdFollow rd matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 72 if score #rdFollow rd matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 2
execute if score @s rdTime matches 72 if score #rdFollow rd matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:13,tell:12,damage:12,life:22}
execute if score @s rdTime matches 81 if score #rdFollow rd matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 3
execute if score @s rdTime matches 84 if score #rdFollow rd matches 1 at @s rotated as @s run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdTime matches 84 if score #rdFollow rd matches 1 at @s rotated as @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.1 0.9 0.3
execute if score @s rdTime matches 74 if score #rdFollow rd matches 0 at @s rotated as @s run function rlk:boss/raiden/finish
execute if score @s rdTime matches 90 if score #rdFollow rd matches 1 at @s rotated as @s run function rlk:boss/raiden/finish
