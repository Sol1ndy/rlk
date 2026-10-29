# blink_out: 8 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 9.. run return run scoreboard players set @s tkRigT 9
execute if score @s tkRigT matches 0 run return run function rlk:boss/tachy/rig/c/blink_out/k/0
execute if score @s tkRigT matches 3 run return run function rlk:boss/tachy/rig/c/blink_out/k/3
execute if score @s tkRigT matches 4 run return run function rlk:boss/tachy/rig/c/blink_out/k/4
execute if score @s tkRigT matches 5 run return run function rlk:boss/tachy/rig/c/blink_out/k/5
execute if score @s tkRigT matches 6 run return run function rlk:boss/tachy/rig/c/blink_out/k/6
