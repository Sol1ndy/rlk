# combo_a: 29 t, holds the last pose. @s = rig anchor.
execute if score @s apRigT matches 30.. run return run scoreboard players set @s apRigT 30
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/combo_a/k/0
