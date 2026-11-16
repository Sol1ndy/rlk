# Internal (clips): the stored edge look (tkRigE).
execute if score @s tkRigE matches 0 run data modify entity 524c4b4d-544b-4900-8000-000000000024 item.components."minecraft:item_model" set value "rlk:mboss/tachy/empty"
execute if score @s tkRigE matches 1 run data modify entity 524c4b4d-544b-4900-8000-000000000024 item.components."minecraft:item_model" set value "rlk:mboss/tachy/edge_y"
execute if score @s tkRigE matches 2 run data modify entity 524c4b4d-544b-4900-8000-000000000024 item.components."minecraft:item_model" set value "rlk:mboss/tachy/edge_p"
execute if score @s tkRigE matches 3 run data modify entity 524c4b4d-544b-4900-8000-000000000024 item.components."minecraft:item_model" set value "rlk:mboss/tachy/edge_e"
execute if score @s tkRigE matches 4 run data modify entity 524c4b4d-544b-4900-8000-000000000024 item.components."minecraft:item_model" set value "rlk:mboss/tachy/edge_g"
