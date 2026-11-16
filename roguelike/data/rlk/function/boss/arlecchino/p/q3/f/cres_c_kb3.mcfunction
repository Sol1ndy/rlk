# One crescent thrown at her yaw +0 deg (@s = body), knockback 3, from 1.2 b over the floor.
execute at @s rotated as @s rotated ~0 0 positioned ^ ^ ^0.5 positioned ~ 202.2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q3","rlk_kn_cres","rlk_kn_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~0 0 run function rlk:boss/arlecchino/p/q3/cres_out3
