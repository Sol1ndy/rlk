# entrance_p1 (110 t)
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/state/burrowed
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/look/tint/p1_dark
execute if score @s apRigT matches 4 run function rlk:mboss/apep/rig_stub/state/normal
execute if score @s apRigT matches 30 run function rlk:mboss/apep/rig_stub/look/tint/none
execute if score @s apRigT matches 31 run function rlk:mboss/apep/rig_stub/hand/a_hand_r/p1_raised
execute if score @s apRigT matches 91 run function rlk:mboss/apep/rig_stub/hand/a_hand_r/p1_planted
execute if score @s apRigT matches 110.. run function rlk:mboss/apep/rig_stub/chain_to {c:1001}
