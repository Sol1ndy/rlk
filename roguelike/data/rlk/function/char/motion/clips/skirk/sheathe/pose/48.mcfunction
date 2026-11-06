# skirk / sheathe: authored animation tick 48
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_body,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.006637f,1.533452f,0.027878f],left_rotation:[0.018995f,-0.124170f,0.002082f,0.992077f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_head,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.006637f,1.533452f,0.027878f],left_rotation:[-0.001650f,-0.168957f,-0.002332f,0.985619f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.338678f,1.408745f,-0.061486f],left_rotation:[-0.106937f,-0.092082f,-0.097624f,0.985168f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.391689f,1.169228f,-0.013305f],left_rotation:[-0.483371f,-0.046617f,-0.125843f,0.865068f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.121958f,0.784000f,-0.027411f],left_rotation:[-0.016026f,-0.110064f,-0.008043f,0.993763f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_right_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[-0.129275f,0.409241f,-0.016130f],left_rotation:[0.009994f,-0.110237f,-0.005159f,0.993842f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
data merge entity @e[tag=rlk_pm,tag=rlk_pm_weapon,limit=1] {interpolation_duration:0,start_interpolation:0,transformation:{translation:[-0.288559f,1.192318f,-0.284447f],left_rotation:[0.075432f,0.005061f,-0.827793f,0.555917f],scale:[0.000000f,0.000000f,0.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_arm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.327616f,1.408342f,0.107950f],left_rotation:[-0.020324f,-0.144713f,0.067969f,0.986927f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_forearm,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.359686f,1.160859f,0.122897f],left_rotation:[-0.123426f,-0.151027f,0.052462f,0.979390f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_leg,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.121958f,0.784000f,0.027411f],left_rotation:[0.021061f,-0.110286f,0.006254f,0.993657f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
$data merge entity @e[tag=rlk_pm,tag=rlk_pm_left_shin,limit=1] {interpolation_duration:$(step),start_interpolation:0,transformation:{translation:[0.128360f,0.409362f,0.012232f],left_rotation:[0.059606f,-0.109960f,0.010529f,0.992091f],scale:[1.000000f,1.000000f,1.000000f],right_rotation:[0f,0f,0f,1f]}}
# weapon_attach world -> back: snap (no interpolation across the change)
scoreboard players set @s pmWAt 1
scoreboard players set #pmSnapW tmp 1
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.653 ^1.343 ^-0.314 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.382 ^1.231 ^-0.292 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^-0.111 ^1.119 ^-0.27 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.16 ^1.007 ^-0.248 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.43 ^0.894 ^-0.226 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.701 ^0.782 ^-0.203 0.04 0.05 0.04 0 2
particle minecraft:dust{color:[1.0,0.84,0.38],scale:0.55} ^0.972 ^0.67 ^-0.181 0.04 0.05 0.04 0 2
particle minecraft:end_rod ^0.16 ^1.007 ^-0.248 0.06 0.25 0.06 0.01 2
