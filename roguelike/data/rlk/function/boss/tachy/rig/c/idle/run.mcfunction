# idle: 40 t, loops 0-40. @s = rig anchor.
execute if score @s tkRigT matches 40.. run scoreboard players set @s tkRigT 0
execute if score @s tkRigT matches ..9 run return run function rlk:boss/tachy/rig/c/idle/b/0_9
execute if score @s tkRigT matches ..16 run return run function rlk:boss/tachy/rig/c/idle/b/10_16
execute if score @s tkRigT matches ..23 run return run function rlk:boss/tachy/rig/c/idle/b/17_23
execute if score @s tkRigT matches ..30 run return run function rlk:boss/tachy/rig/c/idle/b/24_30
execute if score @s tkRigT matches ..39 run return run function rlk:boss/tachy/rig/c/idle/b/31_39
