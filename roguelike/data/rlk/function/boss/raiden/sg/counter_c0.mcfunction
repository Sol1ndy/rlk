execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdSgCk matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/counter_s0
execute if score @s rdSgCk matches 1 at @s rotated as @s run function rlk:boss/raiden/sg/counter_p0
