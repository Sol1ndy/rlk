# elspike #azPT 14
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.2 ^6.468 ^1.877 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p46","rlk_mb_az_p46u"],teleport_duration:1}
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^-1.2 ^6.468 ^1.877 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p46","rlk_mb_az_p46u"],teleport_duration:1}
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.1 ^6.315 ^-0.931 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p46","rlk_mb_az_p46u"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p46u] run function rlk:mboss/azhdaha/fx/prop/spike/3
function rlk:mboss/azhdaha/fx/snd/spikes_launch
