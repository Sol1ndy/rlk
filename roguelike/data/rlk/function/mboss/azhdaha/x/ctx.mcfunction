# The addon context marker rlk_az_ctx here, rotated as the context (s2.md 10.1).
kill @e[type=minecraft:marker,tag=rlk_az_ctx]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_ctx"]}
execute rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run tp @s ~ ~ ~ ~ 0
