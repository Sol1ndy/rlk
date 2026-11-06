# land: 16 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 17.. run return run scoreboard players set @s tkRigT 17
execute if score @s tkRigT matches ..8 run return run function rlk:boss/tachy/rig/c/land/b/0_8
execute if score @s tkRigT matches ..15 run return run function rlk:boss/tachy/rig/c/land/b/9_15
