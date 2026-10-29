# hover_high: 40 t, loops 0-40. @s = rig anchor.
execute if score @s tkRigT matches 40.. run scoreboard players set @s tkRigT 0
execute if score @s tkRigT matches ..10 run return run function rlk:boss/tachy/rig/c/hover_high/b/0_10
execute if score @s tkRigT matches ..18 run return run function rlk:boss/tachy/rig/c/hover_high/b/11_18
execute if score @s tkRigT matches ..26 run return run function rlk:boss/tachy/rig/c/hover_high/b/19_26
execute if score @s tkRigT matches ..34 run return run function rlk:boss/tachy/rig/c/hover_high/b/27_34
execute if score @s tkRigT matches ..39 run return run function rlk:boss/tachy/rig/c/hover_high/b/35_39
