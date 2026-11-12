# Internal (clips): the stored chest look (tkRigG).
execute if score @s tkRigG matches 0 run data modify entity 524c4b4d-544b-4900-8000-000000000003 item.components."minecraft:item_model" set value "rlk:mboss/tachy/empty"
execute if score @s tkRigG matches 1 run data modify entity 524c4b4d-544b-4900-8000-000000000003 item.components."minecraft:item_model" set value "rlk:mboss/tachy/grid_a"
execute if score @s tkRigG matches 2 run data modify entity 524c4b4d-544b-4900-8000-000000000003 item.components."minecraft:item_model" set value "rlk:mboss/tachy/grid_r"
execute if score @s tkRigG matches 3 run data modify entity 524c4b4d-544b-4900-8000-000000000003 item.components."minecraft:item_model" set value "rlk:mboss/tachy/grid_g"
