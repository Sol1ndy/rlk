# A13 pattern tick 198.
function rlk:boss/scarlet/rig/play/g_run
function rlk:boss/scarlet/g/spot/d4
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.35 0.7 0.35 0.02 16 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:end_rod ~ ~ ~ 0.25 0.6 0.25 0.04 4 force @a[tag=player]
function rlk:boss/scarlet/g/cut/make {s:211,t:13,dmg:42,kb:0,n:1}
