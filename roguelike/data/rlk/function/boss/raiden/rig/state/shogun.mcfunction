# Shogun state: follow list, Shogun body look and the stored weapon (rdRigW). @s = the boss.
scoreboard players set @s rdRigS 0
scoreboard players set @s rdRigFl 0
scoreboard players reset @s rdRigQx
function rlk:boss/raiden/rig/look/shogun_models
execute if score @s rdRigW matches 1 run function rlk:boss/raiden/rig/look/polearm
execute unless score @s rdRigW matches 1 run function rlk:boss/raiden/rig/look/sword
