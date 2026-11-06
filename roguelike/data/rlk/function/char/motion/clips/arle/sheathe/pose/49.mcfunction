# arle / sheathe: authored animation tick 49
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_body,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.003154f,1.520970f,0.039158f],left_rotation:[0.026190f,-0.054702f,0.000671f,0.998159f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_head,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.003154f,1.520970f,0.039158f],left_rotation:[0.082756f,-0.109092f,0.005461f,0.990566f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.344321f,1.396666f,-0.004919f],left_rotation:[0.003381f,0.324638f,-0.265188f,0.907896f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.465251f,1.181834f,0.036591f],left_rotation:[-0.268007f,0.389037f,-0.156092f,0.867443f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.125000f,0.772000f,0.000000f],left_rotation:[-0.014833f,0.000427f,-0.014829f,0.999780f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.136114f,0.397330f,0.011127f],left_rotation:[0.011343f,0.000039f,-0.014835f,0.999826f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data merge entity @e[tag=rlk_pm,tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0,transformation:{translation:[-0.090229f,1.146349f,-0.272253f],left_rotation:[0.064088f,-0.047325f,0.227980f,0.970401f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.339064f,1.395618f,0.070182f],left_rotation:[-0.005553f,-0.075421f,0.060365f,0.995307f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.368896f,1.147455f,0.075222f],left_rotation:[-0.074354f,-0.079414f,0.055007f,0.992542f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.125000f,0.772000f,0.000000f],left_rotation:[0.015706f,0.000026f,0.014835f,0.999767f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.136123f,0.397350f,-0.011777f],left_rotation:[0.033152f,0.000285f,0.014832f,0.999340f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
# weapon_attach hand -> back: snap (no interpolation across the change)
scoreboard players set @s pmWAt 1
scoreboard players set #pmSnapW tmp 1
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.459 ^0.059 ^-0.398 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.256 ^0.462 ^-0.351 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.052 ^0.865 ^-0.305 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.152 ^1.268 ^-0.258 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.356 ^1.672 ^-0.211 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.559 ^2.075 ^-0.165 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.763 ^2.478 ^-0.118 0.04 0.05 0.04 0 2
particle minecraft:end_rod ^-0.152 ^1.268 ^-0.258 0.06 0.25 0.06 0.01 2
