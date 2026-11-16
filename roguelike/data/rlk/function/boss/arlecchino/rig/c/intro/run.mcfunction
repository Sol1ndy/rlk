# intro: 150 t, holds the last pose. @s = rig anchor.
execute if score @s knRigT matches 151.. run return run scoreboard players set @s knRigT 151
execute if score @s knRigT matches ..76 run return run function rlk:boss/arlecchino/rig/c/intro/b2/0_76
execute if score @s knRigT matches ..148 run return run function rlk:boss/arlecchino/rig/c/intro/b2/80_148
