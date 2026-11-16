# dive: 12 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 13.. run return run scoreboard players set @s tkRigT 13
execute if score @s tkRigT matches ..6 run return run function rlk:boss/tachy/rig/c/dive/b/0_6
execute if score @s tkRigT matches ..11 run return run function rlk:boss/tachy/rig/c/dive/b/7_11
