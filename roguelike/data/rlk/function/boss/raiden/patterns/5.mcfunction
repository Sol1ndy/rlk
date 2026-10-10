# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/illusions_start
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 18 at @s rotated as @s run function rlk:boss/raiden/illusions_cue
execute if score @s rdTime matches 55 at @s rotated as @s run function rlk:boss/raiden/illusions_cue
execute if score @s rdTime matches 102 at @s rotated as @s run function rlk:boss/raiden/illusions_fail
execute if score @s rdTime matches 134 at @s rotated as @s run function rlk:boss/raiden/finish
