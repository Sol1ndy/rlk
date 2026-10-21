# surface_p3 (40 t)
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/state/normal
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/bright/15
execute if score @s apRigT matches 10 run function rlk:mboss/apep/rig_stub/bright/13
execute if score @s apRigT matches 40.. run function rlk:mboss/apep/rig_stub/chain_to {c:1027}
