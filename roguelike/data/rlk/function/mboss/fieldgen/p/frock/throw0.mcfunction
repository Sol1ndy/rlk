# Throw 1: slab 1 flies at lock rlk_mb_fg_p12t0 (unless the cap is reached).
execute if score #fq12SH mb matches 2.. run return run function rlk:mboss/fieldgen/p/frock/crumble0
function rlk:mboss/grp_new
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p12t0] add rlk_mb_fg_p12tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p12s,scores={mbS=1},limit=1] run function rlk:mboss/fieldgen/p/frock/throw_go
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12t0]
