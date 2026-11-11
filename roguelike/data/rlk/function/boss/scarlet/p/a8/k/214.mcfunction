# A8 pattern tick 214.
function rlk:boss/scarlet/rig/play/g_dive
function rlk:boss/scarlet/rig/look/form/normal
tag @s remove rlk_hr_ghost
function rlk:boss/scarlet/g/spot/over
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~6 ~ run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
