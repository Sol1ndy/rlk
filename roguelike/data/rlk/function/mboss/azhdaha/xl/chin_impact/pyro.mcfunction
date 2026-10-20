# chin/impact Pyro (plan 4.6; call t23, launch t43, land t69 on the host clock). As the body at
# the context point: three hidden lump props wait here; the launch runs as an after() timer.
kill @e[tag=rlk_mb_az_xlc]
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlc","rlk_mb_az_xlcp","rlk_mb_az_xlcp0"],teleport_duration:0}
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlc","rlk_mb_az_xlcp","rlk_mb_az_xlcp1"],teleport_duration:0}
summon minecraft:item_display ~ ~1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlc","rlk_mb_az_xlcp","rlk_mb_az_xlcp2"],teleport_duration:0}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlcp] run function rlk:mboss/azhdaha/xl/u/lump_dress
scoreboard players set #azAftF mb 2
scoreboard players set #azAftD mb 20
function rlk:mboss/azhdaha/aft/new
