# l_shock: 20 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 21.. run return run scoreboard players set @s tkRigT 21
execute if score @s tkRigT matches ..8 run return run function rlk:boss/tachy/rig/c/l_shock/b/0_8
execute if score @s tkRigT matches ..14 run return run function rlk:boss/tachy/rig/c/l_shock/b/9_14
execute if score @s tkRigT matches ..19 run return run function rlk:boss/tachy/rig/c/l_shock/b/15_19
