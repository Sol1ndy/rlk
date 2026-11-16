# Throw 2: slab 2 flies at lock rlk_mb_fg_p12t1 (unless the cap is reached).
execute if score #fq12SH mb matches 2.. run return run function rlk:mboss/fieldgen/p/frock/crumble1
function rlk:mboss/grp_new
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t1] add rlk_mb_fg_p12tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=2},limit=1] run function rlk:mboss/fieldgen/p/frock/throw_go
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t1]
