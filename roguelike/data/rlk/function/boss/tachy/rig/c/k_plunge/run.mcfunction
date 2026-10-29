# k_plunge: 20 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 21.. run return run scoreboard players set @s tkRigT 21
execute if score @s tkRigT matches ..6 run return run function rlk:boss/tachy/rig/c/k_plunge/b/0_6
execute if score @s tkRigT matches ..13 run return run function rlk:boss/tachy/rig/c/k_plunge/b/7_13
execute if score @s tkRigT matches ..19 run return run function rlk:boss/tachy/rig/c/k_plunge/b/14_19
