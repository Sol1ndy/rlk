# Re-applies the stored look fgRigLook and crack stage (after a respawn or a temporary clip look). @s = rig anchor.
scoreboard players set @s fgRigTmp 0
execute if score @s fgRigLook matches 0 run function rlk:mboss/fieldgen/rig/look/idle_swap
execute if score @s fgRigLook matches 1 run function rlk:mboss/fieldgen/rig/look/charge_swap
execute if score @s fgRigLook matches 2 run function rlk:mboss/fieldgen/rig/look/field_swap
execute if score @s fgRigLook matches 3 run function rlk:mboss/fieldgen/rig/look/groggy_swap
execute if score @s fgRigLook matches 4 run function rlk:mboss/fieldgen/rig/look/off_swap
