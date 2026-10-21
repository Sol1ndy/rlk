# As the dome marker (world): grow the dome on its first tick; a stray marker goes after 300 t.
scoreboard players add @s rdTime 1
execute if score @s rdTime matches 1 as @e[tag=rlk_rd_tm_dome] run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,8f,8f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdTime matches 300.. run kill @s
