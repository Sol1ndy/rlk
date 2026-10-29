# mantle_in: 24 t, holds the last pose. @s = rig anchor.
execute if score @s tkRigT matches 25.. run return run scoreboard players set @s tkRigT 25
execute if score @s tkRigT matches ..8 run return run function rlk:boss/tachy/rig/c/mantle_in/b/0_8
execute if score @s tkRigT matches ..15 run return run function rlk:boss/tachy/rig/c/mantle_in/b/9_15
execute if score @s tkRigT matches ..23 run return run function rlk:boss/tachy/rig/c/mantle_in/b/16_23
