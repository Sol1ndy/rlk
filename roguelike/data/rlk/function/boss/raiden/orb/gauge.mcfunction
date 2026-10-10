scoreboard players operation @s rdObjHP = #rdOrbHP rd
execute if score @s rdObjHP matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/gauge_0"
execute if score @s rdObjHP matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/gauge_1"
execute if score @s rdObjHP matches 2 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/gauge_2"
execute if score @s rdObjHP matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/gauge_3"
execute if score @s rdObjHP matches 4 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/gauge_4"
