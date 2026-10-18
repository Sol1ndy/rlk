# Throw 2 tell (@s = body): lock the player's feet (rlk_mb_fg_p12t1, kept) and draw the line from slab 2.
execute if score #fq12SH mb matches 2.. run return run function rlk:mboss/fieldgen/p/frock/crumble1
function rlk:mboss/fieldgen/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t1]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p12t1
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t1] remove rlk_mb_fg_lock
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t1] add rlk_mb_fg_p12tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=2},limit=1] at @s run function rlk:mboss/fieldgen/p/frock/tl_line
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t1] remove rlk_mb_fg_p12tl
