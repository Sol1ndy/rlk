# k_leap: 14 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 15.. run return run scoreboard players set @s tkRigT 15
execute if score @s tkRigT matches ..7 run return run function rlk:boss/tachy/rig/c/k_leap/b/0_7
execute if score @s tkRigT matches ..13 run return run function rlk:boss/tachy/rig/c/k_leap/b/8_13
