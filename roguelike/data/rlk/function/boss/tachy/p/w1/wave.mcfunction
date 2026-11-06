# One W1 crescent here (@s = body; rotated = her yaw, pitch 0): a horizontal blade pj (#pjShape 1, hr 3.5, 1.25 b/t,
# 32 t, wall stop), height 0.9 b (rows 0 .. 1.65 b: jumping does not clear it), T2, the blade element.
execute if score #el tk matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w1","rlk_tk_air","rlk_tk_pj","rlk_tk_new"],teleport_duration:1}
execute if score #el tk matches 1 run execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/fx/prop/crescent_h_1
execute if score #el tk matches 3 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w1","rlk_tk_air","rlk_tk_pj","rlk_tk_new"],teleport_duration:1}
execute if score #el tk matches 3 run execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/fx/prop/crescent_h_3
execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/p/w1/launch
