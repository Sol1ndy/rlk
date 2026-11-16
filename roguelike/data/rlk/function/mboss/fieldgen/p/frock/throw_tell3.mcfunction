# Throw 4 tell (@s = body): lock the player's feet (rlk_mb_fg_p12t3, kept); slab 4 flares.
execute if score #fq12SH mb matches 2.. run return run function rlk:mboss/fieldgen/p/frock/crumble3
function rlk:mboss/fieldgen/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t3]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p12t3
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t3] remove rlk_mb_fg_lock
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=4},limit=1] at @s run function rlk:mboss/fieldgen/p/frock/tl_line
