# A13 pattern tick 13.
function rlk:boss/scarlet/rig/play/g_dash
function rlk:boss/scarlet/g/spot/d1
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s run function rlk:boss/scarlet/fx/snd/g_appear
function rlk:boss/scarlet/g/cut/make {s:27,t:14,dmg:37,kb:0,n:1}
