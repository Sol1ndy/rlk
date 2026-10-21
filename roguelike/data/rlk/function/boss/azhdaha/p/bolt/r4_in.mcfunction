execute unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=8.5..,limit=1] run return 0
scoreboard players add #aq42N mb 1
execute if score #aq42N mb matches 11.. run return 0
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.5
execute at @s run function rlk:boss/azhdaha/p/bolt/r4_in
