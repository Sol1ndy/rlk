execute at @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..25.5,limit=1] run return 0
scoreboard players add #azCl mb 1
execute if score #azCl mb matches 90.. run return 0
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~
function rlk:boss/azhdaha/u/clamp_s_s
