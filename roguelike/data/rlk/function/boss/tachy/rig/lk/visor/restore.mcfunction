# Internal (clips): the stored visor look (tkRigV).
execute if score @s tkRigV matches 0 run data modify entity 524c4b4d-544b-4900-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/tachy/empty"
execute if score @s tkRigV matches 1 run data modify entity 524c4b4d-544b-4900-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/tachy/skull_p"
execute if score @s tkRigV matches 2 run data modify entity 524c4b4d-544b-4900-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/tachy/skull_e"
execute if score @s tkRigV matches 3 run data modify entity 524c4b4d-544b-4900-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/tachy/skull_a"
execute if score @s tkRigV matches 4 run data modify entity 524c4b4d-544b-4900-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/tachy/empty"
