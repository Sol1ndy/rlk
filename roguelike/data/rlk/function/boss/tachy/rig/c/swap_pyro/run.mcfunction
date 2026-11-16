# swap_pyro: 24 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 25.. run return run scoreboard players set @s tkRigT 25
execute if score @s tkRigT matches ..7 run return run function rlk:boss/tachy/rig/c/swap_pyro/b/0_7
execute if score @s tkRigT matches ..15 run return run function rlk:boss/tachy/rig/c/swap_pyro/b/8_15
execute if score @s tkRigT matches ..23 run return run function rlk:boss/tachy/rig/c/swap_pyro/b/16_23
