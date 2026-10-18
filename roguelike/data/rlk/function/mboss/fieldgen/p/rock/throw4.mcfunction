# Throw 5: slab 5 flies at lock rlk_mb_fg_p6t4.
function rlk:mboss/grp_new
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p6t4] add rlk_mb_fg_p6tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=5},limit=1] run function rlk:mboss/fieldgen/p/rock/throw_go
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p6t4]
