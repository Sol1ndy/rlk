# t35: one launch, the three shells go up from the light ball (shell 1 drops as the beam at t45; shells 2 / 3
# hover high until their locks, then stand over their points: the readable tell of the none rows).
execute at @e[type=minecraft:item_display,tag=rlk_mb_ap_p33o,limit=1] run function rlk:boss/apep/fx/p/launch_flash
execute at @s run function rlk:boss/apep/fx/snd/q3_launch
execute at @e[type=minecraft:item_display,tag=rlk_mb_ap_p33o,limit=1] run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33s","rlk_mb_ap_p33s1"],teleport_duration:8,item:{id:"minecraft:paper",count:1}}
execute at @e[type=minecraft:item_display,tag=rlk_mb_ap_p33o,limit=1] run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33s","rlk_mb_ap_p33s2"],teleport_duration:8,item:{id:"minecraft:paper",count:1}}
execute at @e[type=minecraft:item_display,tag=rlk_mb_ap_p33o,limit=1] run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33s","rlk_mb_ap_p33s3"],teleport_duration:8,item:{id:"minecraft:paper",count:1}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s] run function rlk:boss/apep/fx/prop/charge_ball
kill @e[type=minecraft:item_display,tag=rlk_mb_ap_p33o]
execute at @s rotated as @s positioned ^ ^18.39 ^ as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s1] run tp @s ~ ~ ~
execute at @s rotated as @s positioned ^2.5 ^16.39 ^ as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s2] run tp @s ~ ~ ~
execute at @s rotated as @s positioned ^-2.5 ^16.39 ^ as @e[type=minecraft:item_display,tag=rlk_mb_ap_p33s3] run tp @s ~ ~ ~
