# Landing of lump 2 (t93): its fireball + fire field, then its prop and target go.
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xltt2,limit=1] at @s run function rlk:boss/azhdaha/xl/u/lump_land
kill @e[tag=rlk_mb_az_xltp2]
kill @e[tag=rlk_mb_az_xltt2]
kill @e[tag=rlk_mb_az_xlt]
