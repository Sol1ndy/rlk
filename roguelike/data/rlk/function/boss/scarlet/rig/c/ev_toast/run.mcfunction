# ev_toast: 34 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 35.. run return run scoreboard players set @s hrRigT 35
execute if score @s hrRigT matches ..10 run return run function rlk:boss/scarlet/rig/c/ev_toast/b/0_10
execute if score @s hrRigT matches ..24 run return run function rlk:boss/scarlet/rig/c/ev_toast/b/12_24
execute if score @s hrRigT matches ..32 run return run function rlk:boss/scarlet/rig/c/ev_toast/b/25_32
