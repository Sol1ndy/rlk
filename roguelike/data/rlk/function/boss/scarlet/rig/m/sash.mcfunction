# Internal: the sash_tails model of the stored phase and form.
execute if score @s hrRigPh matches 0 if score @s hrRigForm matches 1 run data modify entity 524c4b4d-4852-4400-8000-000000000014 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/sash_p1_g"
execute if score @s hrRigPh matches 1 if score @s hrRigForm matches 1 run data modify entity 524c4b4d-4852-4400-8000-000000000014 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/sash_p2_g"
execute if score @s hrRigPh matches 0 unless score @s hrRigForm matches 1 run data modify entity 524c4b4d-4852-4400-8000-000000000014 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/sash_p1"
execute if score @s hrRigPh matches 1 unless score @s hrRigForm matches 1 run data modify entity 524c4b4d-4852-4400-8000-000000000014 item.components."minecraft:item_model" set value "rlk:mboss/scarlet/sash_p2"
