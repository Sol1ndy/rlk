# navia / physical_3: authored animation tick 26
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_body,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.002028f,1.532975f,-0.011875f],left_rotation:[-0.004073f,0.066276f,0.000289f,-0.997793f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_head,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.002028f,1.532975f,-0.011875f],left_rotation:[0.006721f,0.059803f,-0.018270f,-0.998020f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.338707f,1.408363f,-0.058359f],left_rotation:[-0.002291f,0.051031f,0.265774f,-0.962681f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.466576f,1.193684f,-0.066243f],left_rotation:[0.125291f,0.015364f,0.270192f,-0.954496f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.121645f,0.783123f,-0.036353f],left_rotation:[0.021631f,0.072872f,0.035704f,-0.996467f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.149511f,0.409430f,-0.022139f],left_rotation:[0.005359f,0.073445f,0.034510f,-0.996688f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data merge entity @e[tag=rlk_pm,tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0,transformation:{translation:[-0.175036f,1.597727f,-0.347731f],left_rotation:[0.967866f,0.239931f,0.069491f,0.028977f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.342754f,1.407595f,0.032568f],left_rotation:[0.032822f,0.076741f,-0.262666f,-0.961270f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.467741f,1.192630f,0.058422f],left_rotation:[0.159908f,0.110869f,-0.250181f,-0.948444f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.125645f,0.782877f,0.000353f],left_rotation:[0.022630f,0.073831f,-0.015334f,-0.996896f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.135857f,0.408437f,0.018122f],left_rotation:[0.006351f,0.073571f,-0.016538f,-0.997133f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
# weapon_attach world -> back: snap (no interpolation across the change)
scoreboard players set @s pmWAt 1
scoreboard players set #pmSnapW tmp 1
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.381 ^1.992 ^-0.388 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.22 ^1.685 ^-0.357 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.06 ^1.377 ^-0.325 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.101 ^1.069 ^-0.294 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.261 ^0.761 ^-0.263 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.422 ^0.453 ^-0.232 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.582 ^0.145 ^-0.201 0.04 0.05 0.04 0 2
particle minecraft:end_rod ^0.101 ^1.069 ^-0.294 0.06 0.25 0.06 0.01 2
