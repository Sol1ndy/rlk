# revival (160 t)
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/state/burrowed
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/look/form/p3
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/look/face/p3_idle
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/look/core/p3_sternum
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/look/tint/none
execute if score @s apRigT matches 60 run function rlk:mboss/apep/rig_stub/state/normal
execute if score @s apRigT matches 104 run function rlk:mboss/apep/rig_stub/hands/p3_open
execute if score @s apRigT matches 160.. run function rlk:mboss/apep/rig_stub/chain_to {c:1023}
