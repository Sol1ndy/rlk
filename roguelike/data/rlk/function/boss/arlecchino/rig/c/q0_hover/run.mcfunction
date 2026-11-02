# q0_hover: 40 t, loops 0-40. @s = rig anchor.
execute if score @s knRigT matches 40.. run scoreboard players set @s knRigT 0
execute if score @s knRigT matches ..17 run return run function rlk:boss/arlecchino/rig/c/q0_hover/b/0_17
execute if score @s knRigT matches ..28 run return run function rlk:boss/arlecchino/rig/c/q0_hover/b/18_28
execute if score @s knRigT matches ..37 run return run function rlk:boss/arlecchino/rig/c/q0_hover/b/29_37
