# The burst walker rlk_mb_fg_p12w: on the floor 6 b from the player toward the device, inside the walk disc.
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12w]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p12","rlk_mb_fg_p12w"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^6 run tp @s ~ ~ ~
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p12w,limit=1] run function rlk:mboss/fieldgen/u/clamp_w
