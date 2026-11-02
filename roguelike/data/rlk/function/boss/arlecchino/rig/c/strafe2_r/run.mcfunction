# strafe2_r: 20 t, loops 0-20. @s = rig anchor.
execute if score @s knRigT matches 20.. run scoreboard players set @s knRigT 0
execute if score @s knRigT matches ..7 run return run function rlk:boss/arlecchino/rig/c/strafe2_r/b/0_7
execute if score @s knRigT matches ..13 run return run function rlk:boss/arlecchino/rig/c/strafe2_r/b/8_13
execute if score @s knRigT matches ..19 run return run function rlk:boss/arlecchino/rig/c/strafe2_r/b/14_19
