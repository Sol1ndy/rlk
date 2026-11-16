# navia / burst: authored animation tick 101
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_body,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.000000f,1.527886f,0.013089f],left_rotation:[0.008727f,0.000000f,0.000000f,0.999962f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_head,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.000000f,1.527886f,0.013089f],left_rotation:[-0.002315f,0.025747f,0.022306f,0.999417f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.343750f,1.402905f,0.010908f],left_rotation:[-0.024808f,0.020620f,-0.073268f,0.996790f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.380010f,1.155897f,0.024027f],left_rotation:[-0.137488f,0.028781f,-0.070462f,0.987575f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.125000f,0.778000f,0.000000f],left_rotation:[-0.005236f,0.000164f,-0.010470f,0.999931f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.132852f,0.403103f,0.003928f],left_rotation:[0.007853f,0.000027f,-0.010472f,0.999914f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data merge entity @e[tag=rlk_pm,tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0,transformation:{translation:[-0.220000f,1.595287f,-0.295781f],left_rotation:[-0.970259f,-0.241839f,-0.006333f,-0.008467f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.343750f,1.402905f,0.010908f],left_rotation:[-0.024808f,-0.020620f,0.073268f,0.996790f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.380010f,1.155897f,0.024027f],left_rotation:[-0.137488f,-0.028781f,0.070462f,0.987575f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.125000f,0.778000f,0.000000f],left_rotation:[-0.021294f,0.034552f,0.011556f,0.999109f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.134211f,0.403440f,0.015657f],left_rotation:[0.022307f,0.035023f,0.010038f,0.999087f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_halberd"}}
data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
scoreboard players set @s pmWModel 5
# weapon_attach hand -> back: snap (no interpolation across the change)
scoreboard players set @s pmWAt 1
scoreboard players set #pmSnapW tmp 1
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.43 ^1.99 ^-0.304 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.266 ^1.682 ^-0.298 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.103 ^1.374 ^-0.291 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.061 ^1.067 ^-0.284 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.224 ^0.759 ^-0.277 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.388 ^0.451 ^-0.271 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.552 ^0.143 ^-0.264 0.04 0.05 0.04 0 2
particle minecraft:end_rod ^0.061 ^1.067 ^-0.284 0.06 0.25 0.06 0.01 2
