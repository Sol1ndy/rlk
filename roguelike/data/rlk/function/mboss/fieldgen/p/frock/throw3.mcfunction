# Throw 4: slab 4 flies at lock rlk_mb_fg_p12t3.
function rlk:mboss/grp_new
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t3] add rlk_mb_fg_p12tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=4},limit=1] run function rlk:mboss/fieldgen/p/frock/throw_go
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t3]
