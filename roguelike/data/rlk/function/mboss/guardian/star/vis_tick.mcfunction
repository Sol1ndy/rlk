# @s = star glyph: voxel cluster -> crystal in 8 t, then slow growth to about 2 b over the timer (C9).
scoreboard players add @s mbT 1
execute if score @s mbT matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{translation:[0f,-0.6f,0f],scale:[5f,5f,5f]}}
execute if score @s mbT matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:338,transformation:{translation:[0f,-1.0f,0f],scale:[8.5f,8.5f,8.5f]}}
