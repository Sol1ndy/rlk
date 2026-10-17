# @s = the dive marker D, outside the arena: the other side of U.
execute if score #gp1S mb matches 0 at @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~-75 0 positioned ^ ^ ^5.5 run tp @s ~ 201 ~
execute if score #gp1S mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~75 0 positioned ^ ^ ^5.5 run tp @s ~ 201 ~
