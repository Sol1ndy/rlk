# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/stakes_start
execute if score @s rdTime matches 12 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_1
execute if score @s rdTime matches 54 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_2
execute if score @s rdTime matches 88 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_3
execute if score @s rdTime matches 128 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse
execute if score @s rdTime matches 178 at @s rotated as @s run function rlk:boss/raiden/finish
