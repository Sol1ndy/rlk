# @s = 번짐 선: 굵어짐(맥동)
scoreboard players set @s sph 2
scoreboard players set @s sT 0
execute if score @s sidx matches 0 run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{translation:[0.0000f,1.7175f,0.0120f],left_rotation:[0f,0f,1.00000f,0.00000f],right_rotation:[0f,0f,0f,1f],scale:[2.0000f,0.4350f,0.010f]}}
execute if score @s sidx matches 1 run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{translation:[0.0000f,1.2825f,0.0160f],left_rotation:[0f,0f,0.00000f,1.00000f],right_rotation:[0f,0f,0f,1f],scale:[2.0000f,0.4350f,0.010f]}}
