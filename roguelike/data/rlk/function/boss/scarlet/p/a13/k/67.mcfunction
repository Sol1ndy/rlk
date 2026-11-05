# A13 pattern tick 67.
function rlk:boss/scarlet/rig_stub/play/g_dash
function rlk:boss/scarlet/g/spot/d1
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
execute at @s run playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
function rlk:boss/scarlet/g/cut/make {s:80,t:13,dmg:42,kb:0,n:1}
