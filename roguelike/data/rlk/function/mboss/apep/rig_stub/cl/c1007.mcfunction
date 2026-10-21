# burrow_strike (82 t)
execute if score @s apRigT matches 6 run function rlk:mboss/apep/rig_stub/look/tint/p1_dark
execute if score @s apRigT matches 22 run function rlk:mboss/apep/rig_stub/state/burrowed
execute if score @s apRigT matches 44 run function rlk:mboss/apep/rig_stub/state/normal
execute if score @s apRigT matches 44 run function rlk:mboss/apep/rig_stub/look/tint/none
execute if score @s apRigT matches 82.. run function rlk:mboss/apep/rig_stub/chain_to {c:1001}
