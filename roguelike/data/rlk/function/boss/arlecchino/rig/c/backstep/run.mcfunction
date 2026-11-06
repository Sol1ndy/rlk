# backstep: 12 t, holds the last pose. @s = rig anchor.
execute if score @s knRigT matches 13.. run return run scoreboard players set @s knRigT 13
execute if score @s knRigT matches ..6 run return run function rlk:boss/arlecchino/rig/c/backstep/b/0_6
execute if score @s knRigT matches ..11 run return run function rlk:boss/arlecchino/rig/c/backstep/b/8_11
