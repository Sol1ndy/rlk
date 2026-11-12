# Q pattern tick 99
execute if score #q_hit hr matches 1 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:6}
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_93] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
