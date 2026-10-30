# burst (2틱 보간) @s = 주머니 부품
execute if entity @s[tag=rlk_fp_pod] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.305f,1.1745f,1.305f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @s[tag=rlk_fp_glow] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.35f,1.215f,1.35f],right_rotation:[0f,0f,0f,1f]}}
