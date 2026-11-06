# A13 pattern tick 128.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
function rlk:boss/scarlet/g/spot/tell
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
