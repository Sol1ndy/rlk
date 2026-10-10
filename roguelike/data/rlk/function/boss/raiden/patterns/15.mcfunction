# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/judgment_start
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 16
execute if score @s rdTime matches 30 at @s rotated as @s run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.6 0.5 0.3
execute if score @s rdTime matches 70 at @s rotated as @s run playsound minecraft:block.portal.ambient hostile @a[tag=player] ~ ~ ~ 0.45 0.55 0.3
execute if score @s rdTime matches 120 at @s rotated as @s run function rlk:boss/raiden/judgment_strike
execute if score @s rdTime matches 170 at @s rotated as @s run function rlk:boss/raiden/movement/arrive
execute if score @s rdTime matches 176 at @s rotated as @s run function rlk:boss/raiden/finish
