execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p41i,limit=1] at @s if entity @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] feet run tp @s ^ ^ ^3.047
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p41i,limit=1] run function rlk:mboss/azhdaha/fx/p/icicle_trail
