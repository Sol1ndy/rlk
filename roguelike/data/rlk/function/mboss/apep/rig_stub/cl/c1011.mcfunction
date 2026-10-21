# emerge_crown_p1 (40 t)
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/state/burrowed
execute if score @s apRigT matches 5 run function rlk:mboss/apep/rig_stub/state/normal
execute if score @s apRigT matches 5 run function rlk:mboss/apep/rig_stub/look/tint/p1_dark
execute if score @s apRigT matches 20 run function rlk:mboss/apep/rig_stub/look/tint/none
execute if score @s apRigT matches 40.. run function rlk:mboss/apep/rig_stub/chain_to {c:1001}
