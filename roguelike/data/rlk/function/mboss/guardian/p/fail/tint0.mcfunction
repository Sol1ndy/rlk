# Spear 1 turns from red to the star colour.
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.8 1.5 0.3
execute if score #gdFailK1 mb matches 1 run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_pyro"
execute if score #gdFailK1 mb matches 2 run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_hydro"
execute if score #gdFailK1 mb matches 3 run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_electro"
execute if score #gdFailK1 mb matches 4 run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_cryo"
execute if score #gdFailK1 mb matches 5 run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_gold"
execute if score #gdFailK1 mb matches 6 run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s0,limit=1] item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_hydro"
