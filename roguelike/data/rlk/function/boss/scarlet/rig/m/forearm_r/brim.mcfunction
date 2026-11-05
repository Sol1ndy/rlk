# The forearm_r hand 'brim' (stored hrRigHR = 2) in the current form. @s = the boss.
scoreboard players set @s hrRigHR 2
execute if score @s hrRigForm matches 1 run return run data modify entity 524c4b4d-4852-4400-8000-000000000009 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/forearm_r_brim_g"
data modify entity 524c4b4d-4852-4400-8000-000000000009 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/forearm_r_brim"
