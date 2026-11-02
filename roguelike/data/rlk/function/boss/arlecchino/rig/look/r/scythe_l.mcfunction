# Internal: scythe_l shown in form p2 (hand / world), else the empty model (form p1 or gone).
execute if score @s knRigForm matches 1 unless score @s knRigWl matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-00000000000b item.components."minecraft:item_model" set value "rlk:player_motion/weapons/scythe"
execute if score @s knRigForm matches 1 if score @s knRigWl matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/empty"
execute if score @s knRigForm matches 0 run data modify entity 524c4b4d-4b4e-4100-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/empty"
