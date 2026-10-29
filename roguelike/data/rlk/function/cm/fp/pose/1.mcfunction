# pulse_in (5틱 보간) @s = 주머니 부품
execute if entity @s[tag=rlk_fp_pod] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.855f,0.81225f,0.855f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @s[tag=rlk_fp_glow] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[0f,0.01f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.72f,0.684f,0.72f],right_rotation:[0f,0f,0f,1f]}}
