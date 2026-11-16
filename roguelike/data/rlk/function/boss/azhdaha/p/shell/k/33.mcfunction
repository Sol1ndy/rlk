# shell #azPT 33
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.862 ^-2.167 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p44","rlk_mb_az_p44s3"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p44s3,limit=1] run function rlk:boss/azhdaha/fx/prop/shell
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9.862 ^-2.167 run function rlk:boss/azhdaha/fx/snd/shell_spawn
