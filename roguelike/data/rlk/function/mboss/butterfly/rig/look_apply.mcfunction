# Re-applies the stored wing look bfRigLook and the crescent tell (after a respawn or a temporary flat look). @s = rig anchor.
scoreboard players set @s bfRigFlat 0
execute if score @s bfRigLook matches 0 run function rlk:mboss/butterfly/rig/look/dendro_swap
execute if score @s bfRigLook matches 1 run function rlk:mboss/butterfly/rig/look/pyro_swap
execute if score @s bfRigLook matches 2 run function rlk:mboss/butterfly/rig/look/flat_swap
execute if score @s bfRigTell matches 1 run function rlk:mboss/butterfly/rig/tell/on
