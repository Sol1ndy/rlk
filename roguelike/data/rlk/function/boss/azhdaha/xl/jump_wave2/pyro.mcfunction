# jump/wave2 Pyro (plan 4.6; call t20, launch t32, land t58 on the host clock). As the body at
# the context point: three hidden lump props wait here; the launch runs as an after() timer.
kill @e[tag=rlk_mb_az_xlw]
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlw","rlk_mb_az_xlwp","rlk_mb_az_xlwp0"],teleport_duration:0}
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlw","rlk_mb_az_xlwp","rlk_mb_az_xlwp1"],teleport_duration:0}
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlw","rlk_mb_az_xlwp","rlk_mb_az_xlwp2"],teleport_duration:0}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlwp] run function rlk:boss/azhdaha/xl/u/lump_dress
scoreboard players set #azAftF mb 9
scoreboard players set #azAftD mb 12
function rlk:boss/azhdaha/aft/new
