# @s = star crystal: forms in 8 t (1.15 b), then grows slowly to 2.1 b over the timer (0.38 -> 0.7 BH,
# patterns.md §9.2); turns 3 deg per tick (teleport_duration 1 smooths it).
scoreboard players add @s mbT 1
tp @s ~ ~ ~ ~3 ~
execute if score @s mbT matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{translation:[0f,-0.325f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.15f,1.15f,1.15f]}}
execute if score @s mbT matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:338,transformation:{translation:[0f,0.15f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[2.1f,2.1f,2.1f]}}
