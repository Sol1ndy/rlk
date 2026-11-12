scoreboard players add @s rdSfxAge 1
execute if score @s rdSfxAge >= @s rdSfxLife run return run kill @s
execute if score @s rdSfxAge matches 1 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{scale:[22f,19f,22f],translation:[0f,0.15f,0f]}}
execute if score @s rdSfxAge matches 5 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{scale:[27f,20f,27f],translation:[0f,-0.4f,0f]}}
execute if score @s rdSfxAge matches 10 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{scale:[30f,3f,30f],translation:[0f,0f,0f]}}
