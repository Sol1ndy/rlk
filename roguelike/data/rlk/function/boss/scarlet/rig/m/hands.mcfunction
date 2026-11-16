# Internal: both hands and the face in the stored form.
execute if score @s hrRigHR matches 0 run function rlk:boss/scarlet/rig/m/forearm_r/open
execute if score @s hrRigHR matches 1 run function rlk:boss/scarlet/rig/m/forearm_r/grip
execute if score @s hrRigHR matches 2 run function rlk:boss/scarlet/rig/m/forearm_r/brim
execute if score @s hrRigHL matches 0 run function rlk:boss/scarlet/rig/m/forearm_l/open
execute if score @s hrRigHL matches 1 run function rlk:boss/scarlet/rig/m/forearm_l/grip
execute if score @s hrRigHL matches 2 run function rlk:boss/scarlet/rig/m/forearm_l/brim
execute if score @s hrRigFc matches 0 run function rlk:boss/scarlet/rig/m/face/calm
execute if score @s hrRigFc matches 1 run function rlk:boss/scarlet/rig/m/face/smile
execute if score @s hrRigFc matches 2 run function rlk:boss/scarlet/rig/m/face/closed
