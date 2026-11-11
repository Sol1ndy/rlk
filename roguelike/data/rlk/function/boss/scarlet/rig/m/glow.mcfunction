# Internal: the blade glow (sword_glow): lilac in the ghost form, else the stored blade look.
execute if score @s hrRigForm matches 1 run return run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/glow_lilac"
execute if score @s hrRigBl matches 0 run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/empty"
execute if score @s hrRigBl matches 1 run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/glow_lilac"
execute if score @s hrRigBl matches 2 run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/glow_pink"
execute if score @s hrRigBl matches 3 run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/glow_violet"
execute if score @s hrRigBl matches 4 run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/glow_gold"
execute if score @s hrRigBl matches 5 run data modify entity 524c4b4d-4852-4400-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/glow_edge"
