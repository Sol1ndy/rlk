# Bubble crack stage 0 (hits 0-4 of 20). Shown in the field look; stored in fgRigCrack. @s = rig anchor.
scoreboard players set @s fgRigCrack 0
execute if score @s fgRigLook matches 2 run data modify entity 524c4b4d-4647-4400-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/fieldgen/bubble_0"
