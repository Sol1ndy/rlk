# Only item identity changes here; the next pose interpolates from the current pose.
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/rig/skin_normal
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/rig/skin_dull
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/rig/skin_dull
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/rig/skin_normal
data modify entity @e[tag=rlk_rd_weapon,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/katana"
data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_0"
data modify entity @e[tag=rlk_rd_weapon_trail_1,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_trail_0"
data modify entity @e[tag=rlk_rd_weapon_trail_2,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_trail_0"
data modify entity @e[tag=rlk_rd_weapon_trail_3,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_trail_0"
data modify entity @e[tag=rlk_rd_giant_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_0"
data modify entity @e[tag=rlk_rd_giant_trail_1,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_trail_0"
data modify entity @e[tag=rlk_rd_giant_trail_2,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_trail_0"
data modify entity @e[tag=rlk_rd_giant_trail_3,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_trail_0"
data modify entity @e[tag=rlk_rd_palm_main_r,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/palm_open_charge_0"
data modify entity @e[tag=rlk_rd_palm_main_l,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/palm_open_charge_0"
data modify entity @e[tag=rlk_rd_palm_rear_r,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/palm_open_charge_0"
data modify entity @e[tag=rlk_rd_palm_rear_l,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/palm_open_charge_0"
data modify entity @e[tag=rlk_rd_palm_skin,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/palm_open_charge_0"
data modify entity @e[tag=rlk_rd_chakra_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/chakra_0"
