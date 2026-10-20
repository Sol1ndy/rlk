# icicle #azPT 12
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.235 ^0.653 run particle minecraft:snowflake ~ ~ ~ 0.4 0.4 0.4 0.02 4 force @a[tag=player]
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.235 ^0.653 run particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.4} ~ ~ ~ 0.3 0.3 0.3 0 3 force @a[tag=player]
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.235 ^0.653 run function rlk:mboss/azhdaha/fx/p/icicle_trail
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.235 ^0.653 run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.8 1.6 0.27
