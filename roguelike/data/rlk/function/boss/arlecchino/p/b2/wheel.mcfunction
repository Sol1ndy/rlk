# B2 one wheel (@s = body): a vertical flaming wheel pj (hr 1.1, 1.4 b/t, 11 t out, wall stop),
# its centre 1.2 b over the floor, T2 plain Pyro; a new volley group per leg.
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.8 positioned ~ 202.2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_b2","rlk_kn_wheel","rlk_kn_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run function rlk:boss/arlecchino/p/b2/launch
