# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 16
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:5,tell:19,damage:30,life:29}
execute if score @s rdTime matches 16 at @s rotated as @s run scoreboard players set @s rdAnim 17
execute if score @s rdTime matches 20 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.8 0.68 0.3
execute if score @s rdTime matches 32 at @s rotated as @s run function rlk:boss/raiden/finish
