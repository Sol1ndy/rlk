# Re-applies the stored looks azRigLegs and azRigTail (after a respawn). @s = rig anchor.
execute if score @s azRigLegs matches 0 run function rlk:boss/azhdaha/rig/look/legs/geo_swap
execute if score @s azRigLegs matches 1 run function rlk:boss/azhdaha/rig/look/legs/hydro_swap
execute if score @s azRigLegs matches 2 run function rlk:boss/azhdaha/rig/look/legs/pyro_swap
execute if score @s azRigTail matches 0 run function rlk:boss/azhdaha/rig/look/tail/geo_swap
execute if score @s azRigTail matches 1 run function rlk:boss/azhdaha/rig/look/tail/cryo_swap
execute if score @s azRigTail matches 2 run function rlk:boss/azhdaha/rig/look/tail/electro_swap
