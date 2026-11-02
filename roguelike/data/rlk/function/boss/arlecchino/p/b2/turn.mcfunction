# The outward wheel turns back (@s = it): a new returning wheel here, flying back along the same line for as many
# ticks as the outward leg flew (she does not move while it flies), a new volley group.
execute store result storage rlk:kn core.wb.life int 1 run scoreboard players get @s mbPjT
execute at @s rotated as @s rotated ~180 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_b2","rlk_kn_wheel","rlk_kn_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s rotated as @s run function rlk:boss/arlecchino/p/b2/back with storage rlk:kn core.wb
