# The forearm_l hand 'open' (stored hrRigHL = 0) in the current form. @s = the boss.
scoreboard players set @s hrRigHL 0
execute if score @s hrRigForm matches 1 run return run data modify entity 524c4b4d-4852-4400-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/scarlet/forearm_l_open_g"
data modify entity 524c4b4d-4852-4400-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/scarlet/forearm_l_open"
