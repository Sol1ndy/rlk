# Two genuine jagged meshes flicker on the exact blade, including held windup poses.
scoreboard players operation #rdFx rdRigT = @s rdRigT
scoreboard players operation #rdFx rdRigT %= #four rdRigT
execute if score #rdFx rdRigT matches 0 unless score @s rdAnim matches 5..6 run data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_0"
execute if score #rdFx rdRigT matches 0 if score @s rdAnim matches 5..6 run data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/polearm_0"
execute if score #rdFx rdRigT matches 0 run data modify entity @e[tag=rlk_rd_giant_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_0"
execute if score #rdFx rdRigT matches 0 run data modify entity @e[tag=rlk_rd_chakra_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/chakra_0"
execute if score #rdFx rdRigT matches 0 if score @s rdAnim matches 7 run function rlk:boss/raiden/rig/charge_mesh/7_0
execute if score #rdFx rdRigT matches 0 if score @s rdAnim matches 12 run function rlk:boss/raiden/rig/charge_mesh/12_0
execute if score #rdFx rdRigT matches 0 if score @s rdAnim matches 14 run function rlk:boss/raiden/rig/charge_mesh/14_0
execute if score #rdFx rdRigT matches 0 if score @s rdAnim matches 16 run function rlk:boss/raiden/rig/charge_mesh/16_0
execute if score #rdFx rdRigT matches 2 unless score @s rdAnim matches 5..6 run data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_1"
execute if score #rdFx rdRigT matches 2 if score @s rdAnim matches 5..6 run data modify entity @e[tag=rlk_rd_weapon_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/polearm_1"
execute if score #rdFx rdRigT matches 2 run data modify entity @e[tag=rlk_rd_giant_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/katana_1"
execute if score #rdFx rdRigT matches 2 run data modify entity @e[tag=rlk_rd_chakra_fx,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_weapon/chakra_1"
execute if score #rdFx rdRigT matches 2 if score @s rdAnim matches 7 run function rlk:boss/raiden/rig/charge_mesh/7_1
execute if score #rdFx rdRigT matches 2 if score @s rdAnim matches 12 run function rlk:boss/raiden/rig/charge_mesh/12_1
execute if score #rdFx rdRigT matches 2 if score @s rdAnim matches 14 run function rlk:boss/raiden/rig/charge_mesh/14_1
execute if score #rdFx rdRigT matches 2 if score @s rdAnim matches 16 run function rlk:boss/raiden/rig/charge_mesh/16_1
