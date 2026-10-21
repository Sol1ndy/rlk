# emerge_on_p1 (24 t)
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/state/burrowed
execute if score @s apRigT matches 1 run function rlk:mboss/apep/rig_stub/state/normal
execute if score @s apRigT matches 1 run function rlk:mboss/apep/rig_stub/look/tint/none
execute if score @s apRigT matches 24.. run function rlk:mboss/apep/rig_stub/chain_to {c:1014}
