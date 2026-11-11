# NB pattern tick 42
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2]
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_34]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_38] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_40] remove rlk_hr_trr
