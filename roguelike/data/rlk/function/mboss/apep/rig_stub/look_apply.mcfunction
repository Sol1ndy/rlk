# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Every stored channel again (spawn, unpark, reload).
execute if score @s apRigForm matches 0 run function rlk:mboss/apep/rig_stub/look/form/p1
execute if score @s apRigForm matches 1 run function rlk:mboss/apep/rig_stub/look/form/p3
execute if score @s apRigFace matches 0 run function rlk:mboss/apep/rig_stub/look/face/p1_bud
execute if score @s apRigFace matches 1 run function rlk:mboss/apep/rig_stub/look/face/p3_idle
execute if score @s apRigFace matches 2 run function rlk:mboss/apep/rig_stub/look/face/p3_charge
execute if score @s apRigFace matches 3 run function rlk:mboss/apep/rig_stub/look/face/p3_dim
execute if score @s apRigFace matches 4 run function rlk:mboss/apep/rig_stub/look/face/hidden
execute if score @s apRigCore matches 0 run function rlk:mboss/apep/rig_stub/look/core/p1_bulb
execute if score @s apRigCore matches 1 run function rlk:mboss/apep/rig_stub/look/core/p3_sternum
execute if score @s apRigGlow matches 0 run function rlk:mboss/apep/rig_stub/look/core_glow/idle
execute if score @s apRigGlow matches 1 run function rlk:mboss/apep/rig_stub/look/core_glow/lit
execute if score @s apRigTint matches 0 run function rlk:mboss/apep/rig_stub/look/tint/none
execute if score @s apRigTint matches 1 run function rlk:mboss/apep/rig_stub/look/tint/p1_dark
execute if score @s apRigTint matches 2 run function rlk:mboss/apep/rig_stub/look/tint/p1_brown
execute if score @s apRigTint matches 3 run function rlk:mboss/apep/rig_stub/look/tint/withered
execute if score @s apRigTint matches 4 run function rlk:mboss/apep/rig_stub/look/tint/p3_dim
execute if score @s apRigBright matches 0 run function rlk:mboss/apep/rig_stub/bright/13
execute if score @s apRigBright matches 1 run function rlk:mboss/apep/rig_stub/bright/15
function rlk:mboss/apep/rig_stub/shape
