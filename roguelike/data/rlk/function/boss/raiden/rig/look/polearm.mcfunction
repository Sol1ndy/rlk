# Shogun with the polearm (rdRigW 1).
scoreboard players set @s rdRigW 1
data modify entity 524c4b4d-5244-4900-8000-00000000000d item.components."minecraft:item_model" set value "rlk:raiden/polearm"
data modify entity 524c4b4d-5244-4900-8000-00000000000e item.components."minecraft:item_model" set value "rlk:raiden/polearm_fx"
execute unless score @s rdRigS matches 1 run function rlk:boss/raiden/rig/look/shogun_models
