# walk2: 24 t, loops 0-24. @s = rig anchor.
execute if score @s knRigT matches 24.. run scoreboard players set @s knRigT 0
execute if score @s knRigT matches ..9 run return run function rlk:boss/arlecchino/rig/c/walk2/b/0_9
execute if score @s knRigT matches ..17 run return run function rlk:boss/arlecchino/rig/c/walk2/b/10_17
execute if score @s knRigT matches ..23 run return run function rlk:boss/arlecchino/rig/c/walk2/b/18_23
