# The orbit centre follows the anchor at <= 0.2 b/t (frozen while #azLeap 1).
execute if score #azLeap mb matches 1 run return 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] at @s if entity @e[type=minecraft:husk,tag=rlk_mb_body,distance=..0.2,limit=1] run return run tp @s @e[type=minecraft:husk,tag=rlk_mb_body,limit=1]
execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.2 run tp @s ~ ~ ~
