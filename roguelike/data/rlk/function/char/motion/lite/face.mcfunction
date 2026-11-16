# The stand-in rig's heading -> the dodge direction (macro dx / dz = the unit vector, from char/motion/dash).
$execute as @e[tag=rlk_pl_basis,limit=1] at @s run tp @s ~ ~ ~ facing ~$(dx) ~ ~$(dz)
execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pl_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl] ~ ~ ~ ~ 0
