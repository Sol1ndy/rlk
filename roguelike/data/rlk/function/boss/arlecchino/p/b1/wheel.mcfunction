# B1 one wheel (@s = body): a vertical flaming wheel pj (hr 1.1, 1.4 b/t, 11 t out, wall stop),
# its centre 1.2 b over the floor, T2 plain Pyro; a new volley group per leg.
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.8 positioned ~ 202.2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_b1","rlk_kn_wheel","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:fire_charge",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.2f,2.2f,0.2f]}}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run function rlk:boss/arlecchino/p/b1/launch
