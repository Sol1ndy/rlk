# grow (4틱 보간) @s = 주머니 부품
execute if entity @s[tag=rlk_fp_pod] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.675f,0.675f,0.675f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @s[tag=rlk_fp_glow] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.54f,0.54f,0.54f],right_rotation:[0f,0f,0f,1f]}}
