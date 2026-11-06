# flap_up (2 t)
execute as @e[tag=rlk_ci_this,tag=rlk_ci_body] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0.5f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/ci/f_up"}}}
