# Positioned / rotated at a blade launch point: one water blade prop, flown by pj/launch.
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlb","rlk_mb_az_xnb"],billboard:"fixed",teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xnb,limit=1] run function rlk:mboss/azhdaha/xl/u/blade_go
