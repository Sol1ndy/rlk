# Q pattern tick 99
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air74_93]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air74_95] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute if score #q_hit hr matches 1 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:6}
