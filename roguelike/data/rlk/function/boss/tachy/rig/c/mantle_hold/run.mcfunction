# mantle_hold: 40 t, loops 0-40. @s = rig anchor.
execute if score @s tkRigT matches 40.. run scoreboard players set @s tkRigT 0
execute if score @s tkRigT matches ..12 run return run function rlk:boss/tachy/rig/c/mantle_hold/b/0_12
execute if score @s tkRigT matches ..22 run return run function rlk:boss/tachy/rig/c/mantle_hold/b/13_22
execute if score @s tkRigT matches ..31 run return run function rlk:boss/tachy/rig/c/mantle_hold/b/23_31
execute if score @s tkRigT matches ..39 run return run function rlk:boss/tachy/rig/c/mantle_hold/b/32_39
