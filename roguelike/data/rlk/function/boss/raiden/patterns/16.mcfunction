# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 10
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:4,tell:14,damage:30,life:24}
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:10,tell:14,damage:26,life:24}
execute if score @s rdTime matches 11 at @s rotated as @s run execute positioned ^ ^2.4 ^1.2 run function rlk:boss/raiden/object_vfx/object_break
execute if score @s rdTime matches 11 at @s rotated as @s run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 1 1.9 0.3
execute if score @s rdTime matches 12 at @s rotated as @s run scoreboard players set @s rdAnim 11
execute if score @s rdTime matches 15 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.8 0.68 0.3
execute if score @s rdTime matches 26 at @s rotated as @s run function rlk:boss/raiden/finish
