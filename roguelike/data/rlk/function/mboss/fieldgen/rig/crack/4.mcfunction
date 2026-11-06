# Bubble crack stage 4 (the burst: play break with it). Shown in the field look; stored in fgRigCrack. @s = rig anchor.
scoreboard players set @s fgRigCrack 4
execute if score @s fgRigLook matches 2 run data modify entity 524c4b4d-4647-4400-8000-00000000000b item.components."minecraft:item_model" set value "rlk:mboss/fieldgen/bubble_burst"
