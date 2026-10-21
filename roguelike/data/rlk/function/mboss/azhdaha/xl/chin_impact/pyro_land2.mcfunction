# Landing of lump 2 (t71): its fireball + fire field, then its prop and target go.
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlct2,limit=1] at @s run function rlk:mboss/azhdaha/xl/u/lump_land
kill @e[tag=rlk_mb_az_xlcp2]
kill @e[tag=rlk_mb_az_xlct2]
kill @e[tag=rlk_mb_az_xlc]
