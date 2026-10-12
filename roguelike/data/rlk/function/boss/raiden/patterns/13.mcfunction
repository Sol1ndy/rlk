# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 14
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/shadow/spawn
execute if score @s rdTime matches 1 at @s rotated as @s run playsound minecraft:entity.warden.dig hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.3
execute if score @s rdTime matches 1..36 run function rlk:boss/raiden/shadow/follow
execute if score @s rdTime matches 37 at @s rotated as @s run function rlk:boss/raiden/shadow/lock
execute if score @s rdTime matches 45 at @s rotated as @s run scoreboard players set @s rdAnim 15
execute if score @s rdTime matches 49 at @s rotated as @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.72 0.3
execute if score @s rdTime matches 61 at @s rotated as @s run function rlk:boss/raiden/finish
