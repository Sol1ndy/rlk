# @s = one floating hand, at its fixed ground origin. rdRigT is its age.
execute unless entity @e[tag=rlk_raiden,scores={rdPhase=2,rdPat=13},limit=1] run return run kill @s
scoreboard players add @s rdRigT 1
execute if score @s rdRigT matches 1 run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,7f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 21 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{translation:[0f,7.35f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 25 run data merge entity @s {interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,1f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 31 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{translation:[0f,1.4f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[3.5f,3.5f,3.5f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 35 run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,1.8f,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 41.. run kill @s
