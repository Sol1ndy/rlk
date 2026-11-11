# Q pattern tick 20
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 202 ~ run function rlk:boss/scarlet/fx/p/claw_streaks {r:12}
