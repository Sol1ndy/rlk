# 일반 가드의 작은 불꽃(cb 4 로 시작: 만든 틱 3): 남은 2틱 = 2틱 동안 사라짐
execute if score @s cb matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[0f,0f,0f]}}
