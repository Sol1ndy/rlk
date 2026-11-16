# Turn the dash clip basis (and the rig) toward the dash direction.
$execute as @e[tag=rlk_pm_basis,limit=1] at @s run tp @s ~ ~ ~ facing ~$(dx) ~ ~$(dz)
execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
