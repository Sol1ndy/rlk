# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/stakes_start
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/cheonsu
execute if score @s rdTime matches 12 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 20 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_1
execute if score @s rdTime matches 48 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_2
execute if score @s rdTime matches 76 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_3
execute if score @s rdTime matches 104 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_1
execute if score @s rdTime matches 132 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_2
execute if score @s rdTime matches 160 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse_3
execute if score @s rdTime matches 192 at @s rotated as @s run function rlk:boss/raiden/stakes_pulse
execute if score @s rdTime matches 266 at @s rotated as @s run function rlk:boss/raiden/finish
