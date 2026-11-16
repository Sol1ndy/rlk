# icicle #azPT 6
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.789 ^1.019 run particle minecraft:snowflake ~ ~ ~ 0.4 0.4 0.4 0.02 4 force @a[tag=player]
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.789 ^1.019 run particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.4} ~ ~ ~ 0.3 0.3 0.3 0 3 force @a[tag=player]
