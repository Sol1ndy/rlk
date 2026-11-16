# Internal: scythe_r shown (hand / world) or the empty model (gone).
execute if score @s knRigWr matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-00000000000a item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/empty"
execute unless score @s knRigWr matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-00000000000a item.components."minecraft:item_model" set value "rlk:player_motion/weapons/scythe"
