# t32: the lunge end E (3.5 b toward the player, shorter when the player is closer; clamp r 16) and the swing-2
# frame there (the start facing kept: the wedges of swing 2 are where the body will stand).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p34e]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p34g]
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p34","rlk_mb_ap_p34e"]}
execute at @s if entity @e[tag=rlk_body,distance=..99,limit=1] unless entity @e[tag=rlk_body,distance=..5.5,limit=1] as @e[type=minecraft:marker,tag=rlk_mb_ap_p34e,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^3.5
execute at @s if entity @e[tag=rlk_body,distance=..5.5,limit=1] unless entity @e[tag=rlk_body,distance=..4.5,limit=1] as @e[type=minecraft:marker,tag=rlk_mb_ap_p34e,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^2.5
execute at @s if entity @e[tag=rlk_body,distance=..4.5,limit=1] unless entity @e[tag=rlk_body,distance=..3.5,limit=1] as @e[type=minecraft:marker,tag=rlk_mb_ap_p34e,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^1.5
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p34e,limit=1] run function rlk:boss/apep/u/clamp_glide
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p34e,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p34","rlk_mb_ap_p34g"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p34g,limit=1] at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p34f,limit=1] run tp @s ~ ~ ~ ~ 0
