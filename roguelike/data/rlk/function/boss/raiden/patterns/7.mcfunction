# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:8,damage:10,life:18}
execute if score @s rdTime matches 1 at @s rotated as @s run playsound minecraft:entity.warden.sonic_charge hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.3
execute if score @s rdTime matches 4 at @s rotated as @s run execute rotated ~0 0 positioned ^ ^ ^10 run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:8,life:20}
execute if score @s rdTime matches 6 at @s rotated as @s run execute rotated ~60 0 positioned ^ ^ ^10 run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:8,life:20}
execute if score @s rdTime matches 8 at @s rotated as @s run execute rotated ~120 0 positioned ^ ^ ^10 run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:8,life:20}
execute if score @s rdTime matches 10 at @s rotated as @s run execute rotated ~180 0 positioned ^ ^ ^10 run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:8,life:20}
execute if score @s rdTime matches 12 at @s rotated as @s run execute rotated ~240 0 positioned ^ ^ ^10 run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:8,life:20}
execute if score @s rdTime matches 14 at @s rotated as @s run execute rotated ~300 0 positioned ^ ^ ^10 run function rlk:boss/raiden/hazard/create {shape:3,tell:10,damage:8,life:20}
execute if score @s rdTime matches 6 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:12,tell:24,damage:26,life:34}
execute if score @s rdTime matches 27 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 30 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.3
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/finish
