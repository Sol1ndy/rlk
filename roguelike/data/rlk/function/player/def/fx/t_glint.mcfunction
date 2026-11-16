# 경고 섬광: 2틱 밝게, 그 뒤 4틱 동안 가로로 길어지며 납작해져 사라짐
execute if score @s cb matches 4 run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[1.25f,0.02f,1f]}}
