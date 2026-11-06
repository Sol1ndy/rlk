# navia / physical_4: authored animation tick 43
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_body,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.000000f,1.519733f,0.069930f],left_rotation:[-0.046671f,0.000000f,0.000000f,-0.998910f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_head,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.000000f,1.519733f,0.069930f],left_rotation:[-0.011642f,-0.005566f,-0.003240f,-0.999911f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.343750f,1.395277f,0.058275f],left_rotation:[0.116882f,-0.106947f,0.185028f,-0.969879f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.427227f,1.169226f,0.124850f],left_rotation:[0.461884f,-0.166958f,0.133409f,-0.860808f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.125000f,0.773000f,0.000000f],left_rotation:[-0.148287f,0.005188f,0.034632f,-0.988324f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.150094f,0.415391f,-0.110052f],left_rotation:[-0.334802f,0.011724f,0.032998f,-0.941638f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data merge entity @e[tag=rlk_pm,tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0,transformation:{translation:[-0.220000f,1.610367f,-0.232939f],left_rotation:[0.969881f,0.241424f,0.015506f,-0.028362f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.343750f,1.395277f,0.058275f],left_rotation:[-0.000959f,0.029566f,-0.246567f,-0.968674f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.463186f,1.175675f,0.061455f],left_rotation:[0.125571f,0.061518f,-0.240593f,-0.960501f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.125000f,0.773000f,0.000000f],left_rotation:[0.017521f,-0.004710f,-0.022066f,-0.999592f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.141605f,0.398595f,0.013057f],left_rotation:[-0.069840f,-0.006619f,-0.021571f,-0.997303f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_halberd"}}
data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
scoreboard players set @s pmWModel 5
# weapon_attach hand -> back: snap (no interpolation across the change)
scoreboard players set @s pmWAt 1
scoreboard players set #pmSnapW tmp 1
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.43 ^2.004 ^-0.212 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.266 ^1.697 ^-0.228 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.103 ^1.39 ^-0.245 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.061 ^1.082 ^-0.261 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.224 ^0.775 ^-0.278 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.388 ^0.468 ^-0.295 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.552 ^0.16 ^-0.311 0.04 0.05 0.04 0 2
particle minecraft:end_rod ^0.061 ^1.082 ^-0.261 0.06 0.25 0.06 0.01 2
