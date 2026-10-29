# death: 130 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 131.. run return run scoreboard players set @s tkRigT 131
execute if score @s tkRigT matches ..65 run return run function rlk:boss/tachy/rig/c/death/b2/0_65
execute if score @s tkRigT matches ..129 run return run function rlk:boss/tachy/rig/c/death/b2/66_129
