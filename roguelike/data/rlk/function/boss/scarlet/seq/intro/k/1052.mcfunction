# intro: the timeline at #sq 1052 (@s = the body).
execute positioned 884.0 201 5.0 run kill @e[type=minecraft:item_display,tag=rlk_hr_deco,distance=..1]
function rlk:boss/scarlet/rig/look/props/none
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
function rlk:boss/scarlet/seq/intro/m/walk
function rlk:boss/scarlet/fx/snd/grass_step
