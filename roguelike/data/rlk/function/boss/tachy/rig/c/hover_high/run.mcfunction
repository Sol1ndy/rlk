# hover_high: 40 t, loops 0-40. @s = rig anchor.
execute if score @s tkRigT matches 40.. run scoreboard players set @s tkRigT 0
execute if score @s tkRigT matches ..9 run return run function rlk:boss/tachy/rig/c/hover_high/b/0_9
execute if score @s tkRigT matches ..16 run return run function rlk:boss/tachy/rig/c/hover_high/b/10_16
execute if score @s tkRigT matches ..24 run return run function rlk:boss/tachy/rig/c/hover_high/b/17_24
execute if score @s tkRigT matches ..31 run return run function rlk:boss/tachy/rig/c/hover_high/b/25_31
execute if score @s tkRigT matches ..39 run return run function rlk:boss/tachy/rig/c/hover_high/b/32_39
