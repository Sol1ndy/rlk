# spikes #azPT 14
execute rotated as @s rotated ~ 0 positioned ^1.2 ^6.468 ^1.877 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4up","rlk_mb_az_p4n"],teleport_duration:1}
execute rotated as @s rotated ~ 0 positioned ^-1.2 ^6.468 ^1.877 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4up","rlk_mb_az_p4n"],teleport_duration:1}
execute rotated as @s rotated ~ 0 positioned ^1.1 ^6.315 ^-0.931 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4up","rlk_mb_az_p4n"],teleport_duration:1}
execute rotated as @s rotated ~ 0 positioned ^-1.1 ^6.315 ^-0.931 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4up","rlk_mb_az_p4n"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] run function rlk:mboss/azhdaha/fx/prop/spike/5
tag @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] remove rlk_mb_az_p4n
execute rotated as @s rotated ~ 0 positioned ^0 ^4 ^-0.2 run function rlk:mboss/azhdaha/fx/p/gold_plume
function rlk:mboss/azhdaha/fx/snd/spikes_launch
