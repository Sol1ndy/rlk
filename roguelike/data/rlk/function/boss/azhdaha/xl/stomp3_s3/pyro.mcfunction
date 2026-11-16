# stomp3/s3 Pyro (plan 4.6; call t51, launch t65, land t91 on the host clock). As the body at
# the context point: three hidden lump props wait here; the launch runs as an after() timer.
kill @e[tag=rlk_mb_az_xlt]
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlt","rlk_mb_az_xltp","rlk_mb_az_xltp0"],teleport_duration:0}
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlt","rlk_mb_az_xltp","rlk_mb_az_xltp1"],teleport_duration:0}
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlt","rlk_mb_az_xltp","rlk_mb_az_xltp2"],teleport_duration:0}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xltp] run function rlk:boss/azhdaha/xl/u/lump_dress
scoreboard players set #azAftF mb 23
scoreboard players set #azAftD mb 14
function rlk:boss/azhdaha/aft/new
