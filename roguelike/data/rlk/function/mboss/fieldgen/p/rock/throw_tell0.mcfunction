# Throw 1 tell (@s = body): lock the player's feet (rlk_mb_fg_p6t0) and draw the line from slab 1.
function rlk:mboss/fieldgen/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p6t0]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p6t0
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p6t0] remove rlk_mb_fg_lock
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p6t0] add rlk_mb_fg_p6tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=1},limit=1] at @s run function rlk:mboss/fieldgen/p/rock/tl_line
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p6t0] remove rlk_mb_fg_p6tl
