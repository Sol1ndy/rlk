# stagger: 50 t, loops 10-50. @s = rig anchor.
execute if score @s tkRigT matches 50.. run scoreboard players set @s tkRigT 10
execute if score @s tkRigT matches ..9 run return run function rlk:boss/tachy/rig/c/stagger/b/0_9
execute if score @s tkRigT matches ..17 run return run function rlk:boss/tachy/rig/c/stagger/b/10_17
execute if score @s tkRigT matches ..26 run return run function rlk:boss/tachy/rig/c/stagger/b/18_26
execute if score @s tkRigT matches ..34 run return run function rlk:boss/tachy/rig/c/stagger/b/27_34
execute if score @s tkRigT matches ..42 run return run function rlk:boss/tachy/rig/c/stagger/b/35_42
execute if score @s tkRigT matches ..49 run return run function rlk:boss/tachy/rig/c/stagger/b/43_49
