# Internal: the stored stance (apRigStance) in the stored form (apRigForm).
execute if score @s apRigStance matches 0 if score @s apRigForm matches 0 run function rlk:mboss/apep/rig/stance/r/crouch_p1
execute if score @s apRigStance matches 0 if score @s apRigForm matches 1 run function rlk:mboss/apep/rig/stance/r/crouch_p3
execute if score @s apRigStance matches 1 if score @s apRigForm matches 0 run function rlk:mboss/apep/rig/stance/r/upright_p1
execute if score @s apRigStance matches 1 if score @s apRigForm matches 1 run function rlk:mboss/apep/rig/stance/r/upright_p3
