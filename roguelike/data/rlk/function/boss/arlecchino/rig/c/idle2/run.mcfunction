# idle2: 40 t, loops 0-40. @s = rig anchor.
execute if score @s knRigT matches 40.. run scoreboard players set @s knRigT 0
execute if score @s knRigT matches ..19 run return run function rlk:boss/arlecchino/rig/c/idle2/b/0_19
execute if score @s knRigT matches ..29 run return run function rlk:boss/arlecchino/rig/c/idle2/b/20_29
execute if score @s knRigT matches ..39 run return run function rlk:boss/arlecchino/rig/c/idle2/b/32_39
