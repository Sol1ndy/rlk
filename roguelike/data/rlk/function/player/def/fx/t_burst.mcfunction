# 퍼펙트 닷지의 터짐(cb 4 로 시작): 만든 다음 틱부터 2틱 동안 1.6배로 퍼지고 사라진다
execute if score @s cb matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:2}
execute if score @s cb matches 2 store result entity @s transformation.scale[0] float 0.016 run data get entity @s transformation.scale[0] 100
execute if score @s cb matches 2 store result entity @s transformation.scale[1] float 0.016 run data get entity @s transformation.scale[1] 100
