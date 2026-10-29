# k_hold: 20 t, loops 0-20. @s = rig anchor.
execute if score @s tkRigT matches 20.. run scoreboard players set @s tkRigT 0
execute if score @s tkRigT matches ..7 run return run function rlk:boss/tachy/rig/c/k_hold/b/0_7
execute if score @s tkRigT matches ..13 run return run function rlk:boss/tachy/rig/c/k_hold/b/8_13
execute if score @s tkRigT matches ..19 run return run function rlk:boss/tachy/rig/c/k_hold/b/14_19
