# Q6 the 8 orbs gather around her (@s = body, airborne).
execute at @s rotated 0 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o0","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 45 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o1","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 90 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o2","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 135 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o3","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 180 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o4","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 225 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o5","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 270 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o6","rlk_kn_new"],teleport_duration:1}
execute at @s rotated 315 0 positioned ^ ^1.4 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q6","rlk_kn_q6o","rlk_kn_q6o7","rlk_kn_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] run function rlk:boss/arlecchino/fx/prop/orb
tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new
execute at @s run function rlk:boss/arlecchino/fx/p/orb_gather
execute at @s run function rlk:boss/arlecchino/fx/snd/orbs_gather
