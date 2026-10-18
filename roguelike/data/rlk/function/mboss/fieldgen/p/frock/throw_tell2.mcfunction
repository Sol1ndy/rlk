# Throw 3 tell (@s = body): lock the player's feet (rlk_mb_fg_p12t2, kept) and draw the line from slab 3.
execute if score #fq12SH mb matches 2.. run return run function rlk:mboss/fieldgen/p/frock/crumble2
function rlk:mboss/fieldgen/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t2]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p12t2
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t2] remove rlk_mb_fg_lock
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t2] add rlk_mb_fg_p12tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=3},limit=1] at @s run function rlk:mboss/fieldgen/p/frock/tl_line
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t2] remove rlk_mb_fg_p12tl
