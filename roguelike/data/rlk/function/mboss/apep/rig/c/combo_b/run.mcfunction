# combo_b: 44 t, holds the last pose. @s = rig anchor.
execute if score @s apRigT matches 45.. run return run scoreboard players set @s apRigT 45
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/combo_b/k/0
