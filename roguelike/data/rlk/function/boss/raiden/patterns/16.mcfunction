# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 store result score #rdVar rd run random value 0..1
execute if score @s rdTime matches 1 if score #rdVar rd matches 0 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 if score #rdVar rd matches 0 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 if score #rdVar rd matches 0 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 1 if score #rdVar rd matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:18,damage:30,life:28}
execute if score @s rdTime matches 1 if score #rdVar rd matches 0 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:10,tell:18,damage:26,life:28}
execute if score @s rdTime matches 15 if score #rdVar rd matches 0 at @s rotated as @s run execute positioned ^ ^2.4 ^1.2 run function rlk:boss/raiden/object_vfx/object_break
execute if score @s rdTime matches 15 if score #rdVar rd matches 0 at @s rotated as @s run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 1 1.9 0.3
execute if score @s rdTime matches 16 if score #rdVar rd matches 0 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 19 if score #rdVar rd matches 0 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.8 0.68 0.3
execute if score @s rdTime matches 30 if score #rdVar rd matches 0 at @s rotated as @s run function rlk:boss/raiden/finish
execute if score @s rdTime matches 1 if score #rdVar rd matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 if score #rdVar rd matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 if score #rdVar rd matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 16
execute if score @s rdTime matches 1 if score #rdVar rd matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:5,tell:20,damage:34,life:30}
execute if score @s rdTime matches 1 if score #rdVar rd matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:12,damage:5,life:22}
execute if score @s rdTime matches 1 if score #rdVar rd matches 1 at @s rotated as @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.3
execute if score @s rdTime matches 16 if score #rdVar rd matches 1 at @s rotated as @s run function rlk:boss/raiden/line/sever
execute if score @s rdTime matches 17 if score #rdVar rd matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 17
execute if score @s rdTime matches 21 if score #rdVar rd matches 1 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.9 0.6 0.3
execute if score @s rdTime matches 21 if score #rdVar rd matches 1 at @s rotated as @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.3
execute if score @s rdTime matches 33 if score #rdVar rd matches 1 at @s rotated as @s run function rlk:boss/raiden/finish
