# TEMPORARY (release P13). @s = one falling palm at its ground point; rdRigT is its age.
execute unless entity @e[tag=rlk_raiden,scores={rdPhase=2,rdPat=13},limit=1] run return run kill @s
scoreboard players add @s rdRigT 1
execute if score @s rdRigT matches 1 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{translation:[0f,7.000000f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.200000f,3.200000f,3.200000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 5 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{translation:[0f,7.400000f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.200000f,3.200000f,3.200000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 9 run data merge entity @s {interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,0.300000f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.200000f,3.200000f,3.200000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 13 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{translation:[0f,0.700000f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.200000f,3.200000f,3.200000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 17 run data merge entity @s {interpolation_duration:6,start_interpolation:0,transformation:{translation:[0f,1.200000f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 26.. run kill @s
