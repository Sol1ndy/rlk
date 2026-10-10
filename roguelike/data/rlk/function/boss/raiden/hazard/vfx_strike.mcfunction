# Whole path flashes on the exact damage tick; this is instantaneous lightning.
scoreboard players set @s rdWind 1
scoreboard players set @s rdHAge -1
execute if score @s rdShape matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_1"
execute if score @s rdShape matches 2 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_2"
execute if score @s rdShape matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_3"
execute if score @s rdShape matches 4 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_4"
execute if score @s rdShape matches 5 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_5"
execute if score @s rdShape matches 6 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_6"
execute if score @s rdShape matches 7 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_7"
execute if score @s rdShape matches 8 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_8"
execute if score @s rdShape matches 9 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_9"
execute if score @s rdShape matches 10 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_10"
execute if score @s rdShape matches 12 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/strike_12"
