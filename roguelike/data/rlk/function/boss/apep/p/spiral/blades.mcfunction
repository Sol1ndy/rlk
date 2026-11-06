# t52: two low leaf-blade lanes crossing the player's spot (+-35 deg about the boss -> player
# line), each a line 14.0 x 2.2 b (#hzY1 0.7: jumpable), tell 12, 24 %, one volley group;
# quiet (none row): the blades stand glowing at the lane starts from now to the skim (the readable tell).
function rlk:boss/apep/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p35p]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p35p
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35p] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35p] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p35x]
kill @e[type=minecraft:item_display,tag=rlk_mb_ap_p35w]
function rlk:mboss/grp_new
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35p,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~215 0 positioned ^ ^ ^-7 run function rlk:boss/apep/p/spiral/blade
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35p,limit=1] facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~145 0 positioned ^ ^ ^-7 run function rlk:boss/apep/p/spiral/blade
