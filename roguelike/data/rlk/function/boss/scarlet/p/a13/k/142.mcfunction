# A13 pattern tick 142.
function rlk:boss/scarlet/rig/play/g_run
function rlk:boss/scarlet/g/spot/d4
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
function rlk:boss/scarlet/g/cut/make {s:156,t:14,dmg:37,kb:0,n:1}
