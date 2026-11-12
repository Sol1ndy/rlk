# One W2 crescent here (@s = body, at her chest): a vertical crescent pj (sphere hr 1.3, 1.1 b/t, 30 t,
# wall stop) aimed down at the player's chest (feet + 0.9: the hit point 0.9 b below it meets the feet), T2.
kill @e[type=minecraft:marker,tag=rlk_tk_aim]
execute at @e[tag=rlk_body,limit=1] positioned ~ ~0.9 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w2","rlk_tk_air","rlk_tk_aim"]}
execute facing entity @e[type=minecraft:marker,tag=rlk_tk_aim,limit=1] feet run execute if score #el tk matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w2","rlk_tk_air","rlk_tk_pj","rlk_tk_new"],teleport_duration:1}
execute facing entity @e[type=minecraft:marker,tag=rlk_tk_aim,limit=1] feet run execute if score #el tk matches 1 run execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/fx/prop/crescent_v_1
execute facing entity @e[type=minecraft:marker,tag=rlk_tk_aim,limit=1] feet run execute if score #el tk matches 3 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w2","rlk_tk_air","rlk_tk_pj","rlk_tk_new"],teleport_duration:1}
execute facing entity @e[type=minecraft:marker,tag=rlk_tk_aim,limit=1] feet run execute if score #el tk matches 3 run execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/fx/prop/crescent_v_3
execute facing entity @e[type=minecraft:marker,tag=rlk_tk_aim,limit=1] feet as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/p/w2/launch
kill @e[type=minecraft:marker,tag=rlk_tk_aim]
