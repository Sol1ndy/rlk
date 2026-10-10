# @s = one floating hand, at its fixed ground origin. rdRigT is its age.
execute unless entity @e[tag=rlk_raiden,scores={rdPhase=2,rdPat=13},limit=1] run return run kill @s
scoreboard players add @s rdRigT 1
execute if score @s rdRigT matches 1 run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,7.000000f,-1.782500f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[4.600000f,4.600000f,4.600000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 11 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{translation:[0f,7.450000f,-1.782500f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[4.600000f,4.600000f,4.600000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 15 run data merge entity @s {interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,0.920000f,-1.782500f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[4.600000f,4.600000f,4.600000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 19 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{translation:[0f,1.370000f,-1.782500f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[4.600000f,4.600000f,4.600000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 23 run data merge entity @s {interpolation_duration:6,start_interpolation:0,transformation:{translation:[0f,1.820000f,0.000000f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rdRigT matches 32.. run kill @s
