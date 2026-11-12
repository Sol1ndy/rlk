# ev_give: 34 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 35.. run return run scoreboard players set @s hrRigT 35
execute if score @s hrRigT matches ..6 run return run function rlk:boss/scarlet/rig/c/ev_give/b/0_6
execute if score @s hrRigT matches ..14 run return run function rlk:boss/scarlet/rig/c/ev_give/b/7_14
execute if score @s hrRigT matches ..26 run return run function rlk:boss/scarlet/rig/c/ev_give/b/15_26
execute if score @s hrRigT matches ..33 run return run function rlk:boss/scarlet/rig/c/ev_give/b/27_33
