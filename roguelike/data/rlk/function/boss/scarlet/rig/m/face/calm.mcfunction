# The face 'calm' (stored hrRigFc = 0) in the current form. @s = the boss.
scoreboard players set @s hrRigFc 0
execute if score @s hrRigForm matches 1 run return run data modify entity 524c4b4d-4852-4400-8000-000000000003 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/face_calm_g"
data modify entity 524c4b4d-4852-4400-8000-000000000003 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/face_calm"
