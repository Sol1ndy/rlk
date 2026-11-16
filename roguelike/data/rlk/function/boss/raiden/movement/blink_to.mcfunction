# @s boss; the execution position is the destination, pulled in to radius 20 about the arena centre.
kill @e[tag=rlk_rd_blink_dest]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_blink_dest"]}
execute as @e[tag=rlk_rd_blink_dest] at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] facing entity @s feet rotated ~ 0 positioned ^ ^ ^20 run tp @s ~ ~ ~
# A blink that has not relocated yet simply takes the new destination.
execute if score @s rdBlink matches 1..3 run return 0
scoreboard players set @s rdBlink 0
execute at @s run function rlk:boss/raiden/movement/blink_start
