# [c_rocks] Throw 2/5 tell (@s = body; the throw in 10 t): unless 2 slabs have hit already, lock the
# player's feet (rlk_mb_fg_p6t1); slab 2 flares.
execute if score #fq6SH mb matches 2.. run return run execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=2},limit=1] at @s run function rlk:mboss/fieldgen/p/rock/rk_shatter
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=2},limit=1] run return 0
function rlk:mboss/fieldgen/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p6t1]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p6t1
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p6t1] remove rlk_mb_fg_lock
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s,scores={mbS=2},limit=1] at @s run function rlk:mboss/fieldgen/p/rock/rk_tl
