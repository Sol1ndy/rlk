# shell #azPT 23
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^8.323 ^-0.46 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p44","rlk_mb_az_p44s1"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s1,limit=1] run function rlk:mboss/azhdaha/fx/prop/shell
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^8.323 ^-0.46 run function rlk:mboss/azhdaha/fx/snd/shell_spawn
