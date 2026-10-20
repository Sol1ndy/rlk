# @s = body: 0.6 b/t along the lane (inside the arena), the rush disc rides the body
execute at @s positioned ^ ^ ^0.6 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute at @s as @e[type=minecraft:marker,tag=rlk_mb_az_p9rush] run tp @s ~ ~ ~
execute at @s run function rlk:mboss/azhdaha/fx/p/dust
