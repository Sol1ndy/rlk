# quick_out (3틱 보간) @s = 주머니 부품
execute if entity @s[tag=rlk_fp_pod] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.044f,1.10664f,1.044f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @s[tag=rlk_fp_glow] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.008f,1.06848f,1.008f],right_rotation:[0f,0f,0f,1f]}}
