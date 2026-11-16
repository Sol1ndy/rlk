# wither (6틱 보간) @s = 주머니 부품
execute if entity @s[tag=rlk_fp_pod] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.27f,0.162f,0.27f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @s[tag=rlk_fp_glow] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.09f,0.054f,0.09f],right_rotation:[0f,0f,0f,1f]}}
