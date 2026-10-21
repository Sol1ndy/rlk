# Shogun with the katana (rdRigW 0). Call from the Shogun state; a Tenma clip keeps its own look.
scoreboard players set @s rdRigW 0
data modify entity 524c4b4d-5244-4900-8000-00000000000d item.components."minecraft:item_model" set value "rlk:raiden/katana"
data modify entity 524c4b4d-5244-4900-8000-00000000000e item.components."minecraft:item_model" set value "rlk:raiden/katana_fx"
execute unless score @s rdRigS matches 1 run function rlk:boss/raiden/rig/look/shogun_models
