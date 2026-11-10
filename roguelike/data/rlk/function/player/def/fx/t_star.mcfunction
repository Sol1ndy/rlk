# 별빛: 남은 4틱 = 2틱 동안 1.5배로 커지고, 남은 2틱 = 2틱 동안 사라짐
execute if score @s cb matches 4 run data merge entity @s {start_interpolation:0,interpolation_duration:2}
execute if score @s cb matches 4 store result entity @s transformation.scale[0] float 0.015 run data get entity @s transformation.scale[0] 100
execute if score @s cb matches 4 store result entity @s transformation.scale[1] float 0.015 run data get entity @s transformation.scale[1] 100
execute if score @s cb matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[0f,0f,0f]}}
