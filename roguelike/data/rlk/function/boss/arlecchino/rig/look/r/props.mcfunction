# Internal: the cup and saucer models (tea) or empty.
execute if score @s knRigPr matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/cup"
execute if score @s knRigPr matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-000000000019 item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/saucer"
execute unless score @s knRigPr matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-000000000018 item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/empty"
execute unless score @s knRigPr matches 1 run data modify entity 524c4b4d-4b4e-4100-8000-000000000019 item.components."minecraft:item_model" set value "rlk:mboss/arlecchino/empty"
