# 퍼펙트 패링의 별빛(cb 6 으로 시작): 멈춘 동안 그대로, 남은 2틱 = 2틱 동안 사라짐(그 틱에 불꽃이 날아감: fx/p3_shatter)
execute if score @s cb matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[0f,0f,0f]}}
