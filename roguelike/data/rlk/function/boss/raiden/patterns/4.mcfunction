# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/eyes_start
execute if score @s rdTime matches 13 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/eyes_arm
execute if score @s rdTime matches 73 at @s rotated as @s run scoreboard players set @s rdAnim 18
execute if score @s rdTime matches 84 at @s rotated as @s run function rlk:boss/raiden/finish
