# The forearm_l hand 'brim' (stored hrRigHL = 2) in the current form. @s = the boss.
scoreboard players set @s hrRigHL 2
execute if score @s hrRigForm matches 1 run return run data modify entity 524c4b4d-4852-4400-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/scarlet/forearm_l_brim_g"
data modify entity 524c4b4d-4852-4400-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/scarlet/forearm_l_brim"
