# As the broken flower, at it: the safe dome r 8 grows from the flower in 8 t (dome_tick, rig prop model).
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_tm_dome]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_dome"]}
scoreboard players set @e[tag=rlk_rd_dome] rdTime 0
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_dome"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:20f,height:12f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/prop/dome"}}}
function rlk:boss/raiden/fx/mangeop_dome
