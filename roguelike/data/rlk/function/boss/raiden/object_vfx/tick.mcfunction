execute if score @s rdOvKind matches 1..2 run function rlk:boss/raiden/object_vfx/owner
execute if score @s rdOvKind matches 5 run function rlk:boss/raiden/object_vfx/owner
execute if score @s rdOvKind matches 1..2 if score #rdOvExists rd matches 0 run return run kill @s
execute if score @s rdOvKind matches 5 if score #rdOvExists rd matches 0 run return run kill @s
scoreboard players add @s rdOvAge 1
execute if score @s rdOvLife matches 1.. if score @s rdOvAge >= @s rdOvLife run return run kill @s
scoreboard players operation #rdOvFrame rd = @s rdOvAge
scoreboard players set #rdOvEight rd 8
scoreboard players operation #rdOvFrame rd %= #rdOvEight rd
execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/eye_0"
execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 4 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/eye_1"
execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/stake_0"
execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 4 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/stake_1"
execute if score @s rdOvKind matches 5 run function rlk:boss/raiden/object_vfx/cue_tick
execute if score @s rdOvKind matches 6 if score @s rdOvAge matches 2 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/swing_fade"
execute if score @s rdOvKind matches 7 if score @s rdOvAge matches 1.. run tp @s ^ ^ ^5.5
execute if score @s rdOvKind matches 7 if score @s rdOvAge matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/wave_fade"
execute if score @s rdOvKind matches 3 if score @s rdOvAge matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/object_break_fade"
execute if score @s rdOvKind matches 4 if score @s rdOvAge matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/flower_break_fade"
