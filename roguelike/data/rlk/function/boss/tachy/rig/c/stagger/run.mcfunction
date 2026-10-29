# stagger: 50 t, loops 10-50. @s = rig anchor.
execute if score @s tkRigT matches 50.. run scoreboard players set @s tkRigT 10
execute if score @s tkRigT matches ..9 run return run function rlk:boss/tachy/rig/c/stagger/b/0_9
execute if score @s tkRigT matches ..17 run return run function rlk:boss/tachy/rig/c/stagger/b/10_17
execute if score @s tkRigT matches ..27 run return run function rlk:boss/tachy/rig/c/stagger/b/18_27
execute if score @s tkRigT matches ..35 run return run function rlk:boss/tachy/rig/c/stagger/b/28_35
execute if score @s tkRigT matches ..43 run return run function rlk:boss/tachy/rig/c/stagger/b/36_43
execute if score @s tkRigT matches ..49 run return run function rlk:boss/tachy/rig/c/stagger/b/44_49
