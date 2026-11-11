# A8 pattern tick 75.
function rlk:boss/scarlet/g/cut/aim {s:88}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a8","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_a8b76"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[-0.1969f,0.6849f,0.3228f],left_rotation:[-0.6918f,-0.6277f,0.1964f,0.298f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16771496]}}}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_67]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_69] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
