# [c_rocks] Throw 2/5 (@s = body): slab 2 flies at rlk_mb_fg_p6t1 (unless the cap was reached: it crumbles).
execute if score #fq6SH mb matches 2.. run return run execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=2},limit=1] at @s run function rlk:mboss/fieldgen/p/rock/rk_shatter
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_fg_p6t1] run return 0
function rlk:mboss/grp_new
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p6t1] add rlk_mb_fg_p6tl
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=2},limit=1] run function rlk:mboss/fieldgen/p/rock/rk_go
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p6t1]
