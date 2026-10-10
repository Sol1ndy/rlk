scoreboard players operation #rdOvLeft rd = @s rdOvLife
scoreboard players operation #rdOvLeft rd -= @s rdOvAge
execute if score #rdOvLeft rd matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/strike_slash"
