# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_rush
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/pierce
execute if score @s rdTime matches 1 at @s rotated as @s run execute positioned ^ ^1.4 ^1.5 run function rlk:boss/raiden/fx/star
execute if score @s rdTime matches 13 at @s rotated as @s run function rlk:boss/raiden/tm/rush/lock
execute if score @s rdTime matches ..22 run return 0
execute if score @s rdTime matches 23..26 at @s rotated as @s run function rlk:boss/raiden/tm/rush/step
execute if score @s rdTime matches 23 at @s rotated as @s run function rlk:boss/raiden/fx/snd/rush
execute if score @s rdTime matches 28 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/snd/barrage
execute if score @s rdTime matches 34 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/snd/barrage
execute if score @s rdTime matches 40 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/snd/barrage
execute if score @s rdTime matches 52 at @s rotated as @s run function rlk:boss/raiden/finish
